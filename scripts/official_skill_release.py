#!/usr/bin/env python3
"""Validate, build, and verify immutable RunCell official skill bundles."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import stat
import sys
import zipfile
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any, Iterable

import yaml


SCHEMA_VERSION = 1
SKILL_FILENAME = "SKILL.md"
MAX_FILE_BYTES = 512 * 1024
MAX_BUNDLE_BYTES = 5 * 1024 * 1024
MAX_FILES = 256
NAME_PATTERN = re.compile(r"^[a-z0-9][a-z0-9-]{0,63}$")
VERSION_PATTERN = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-[0-9A-Za-z.-]+)?$")
ALLOWED_TOP_LEVEL = frozenset({SKILL_FILENAME, "references", "assets", "scripts"})
FIXED_ZIP_DATETIME = (2020, 1, 1, 0, 0, 0)


class ReleaseError(ValueError):
    """A skill source or release artifact violates the official bundle contract."""


@dataclass(frozen=True)
class BundleFile:
    path: str
    size: int
    sha256: str
    source_path: Path


def _sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _safe_relative_path(value: str) -> PurePosixPath:
    candidate = PurePosixPath(value)
    if candidate.is_absolute() or not candidate.parts:
        raise ReleaseError(f"unsafe bundle path: {value!r}")
    if any(part in {"", ".", ".."} for part in candidate.parts):
        raise ReleaseError(f"unsafe bundle path: {value!r}")
    if "\\" in value or "\x00" in value:
        raise ReleaseError(f"unsafe bundle path: {value!r}")
    return candidate


def _read_skill_identity(skill_file: Path) -> tuple[str, str]:
    text = skill_file.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ReleaseError("SKILL.md must start with YAML frontmatter")
    closing = text.find("\n---", 4)
    if closing < 0:
        raise ReleaseError("SKILL.md frontmatter is not closed")
    metadata = yaml.safe_load(text[4:closing])
    if not isinstance(metadata, dict) or set(metadata) != {"name", "description"}:
        raise ReleaseError("SKILL.md frontmatter must contain only name and description")
    name = metadata.get("name")
    description = metadata.get("description")
    if not isinstance(name, str) or not NAME_PATTERN.fullmatch(name):
        raise ReleaseError("SKILL.md has an invalid skill name")
    if not isinstance(description, str) or not description.strip():
        raise ReleaseError("SKILL.md has an invalid description")
    return name, description.strip()


def collect_skill_files(skill_dir: Path, *, expected_id: str) -> tuple[BundleFile, ...]:
    skill_dir = skill_dir.resolve()
    if not skill_dir.is_dir() or skill_dir.is_symlink():
        raise ReleaseError("skill source must be a real directory")
    skill_file = skill_dir / SKILL_FILENAME
    if not skill_file.is_file() or skill_file.is_symlink():
        raise ReleaseError("skill source must contain a non-symlinked SKILL.md")
    parsed_name, _description = _read_skill_identity(skill_file)
    if parsed_name != expected_id:
        raise ReleaseError(
            f"SKILL.md name {parsed_name!r} does not match requested id {expected_id!r}"
        )

    files: list[BundleFile] = []
    total_bytes = 0
    for current_root, dirnames, filenames in os.walk(skill_dir, followlinks=False):
        current = Path(current_root)
        for dirname in list(dirnames):
            directory = current / dirname
            if directory.is_symlink():
                raise ReleaseError(f"symlinked directory is not allowed: {directory}")
            _safe_relative_path(directory.relative_to(skill_dir).as_posix())
        for filename in filenames:
            source = current / filename
            if source.is_symlink() or not source.is_file():
                raise ReleaseError(f"non-regular file is not allowed: {source}")
            relative = source.relative_to(skill_dir).as_posix()
            safe_path = _safe_relative_path(relative)
            if safe_path.parts[0] not in ALLOWED_TOP_LEVEL:
                raise ReleaseError(f"unsupported top-level skill entry: {safe_path.parts[0]}")
            size = source.stat().st_size
            if size > MAX_FILE_BYTES:
                raise ReleaseError(f"skill file exceeds {MAX_FILE_BYTES} bytes: {relative}")
            total_bytes += size
            if total_bytes > MAX_BUNDLE_BYTES:
                raise ReleaseError(f"skill source exceeds {MAX_BUNDLE_BYTES} bytes")
            files.append(
                BundleFile(
                    path=relative,
                    size=size,
                    sha256=_sha256_file(source),
                    source_path=source,
                )
            )
            if len(files) > MAX_FILES:
                raise ReleaseError(f"skill source exceeds {MAX_FILES} files")

    files.sort(key=lambda item: item.path)
    return tuple(files)


def build_manifest(*, skill_id: str, version: str, files: Iterable[BundleFile]) -> dict[str, Any]:
    return {
        "schemaVersion": SCHEMA_VERSION,
        "skillId": skill_id,
        "version": version,
        "entrypoint": SKILL_FILENAME,
        "files": [
            {"path": item.path, "sizeBytes": item.size, "sha256": item.sha256}
            for item in files
        ],
    }


def _json_bytes(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode(
        "utf-8"
    )


def _zip_info(path: str, *, executable: bool = False) -> zipfile.ZipInfo:
    info = zipfile.ZipInfo(path, FIXED_ZIP_DATETIME)
    info.compress_type = zipfile.ZIP_DEFLATED
    mode = 0o755 if executable else 0o644
    info.external_attr = (stat.S_IFREG | mode) << 16
    info.create_system = 3
    return info


def build_release(
    *, repo_root: Path, skill_id: str, version: str, output_dir: Path
) -> tuple[Path, Path]:
    if not NAME_PATTERN.fullmatch(skill_id):
        raise ReleaseError("invalid skill id")
    if not VERSION_PATTERN.fullmatch(version):
        raise ReleaseError("version must be SemVer")
    skill_dir = repo_root / "skills" / skill_id
    files = collect_skill_files(skill_dir, expected_id=skill_id)
    manifest = build_manifest(skill_id=skill_id, version=version, files=files)

    output_dir.mkdir(parents=True, exist_ok=True)
    base_name = f"{skill_id}-{version}"
    bundle_path = output_dir / f"{base_name}.zip"
    with zipfile.ZipFile(bundle_path, "w") as archive:
        archive.writestr(_zip_info("manifest.json"), _json_bytes(manifest))
        for item in files:
            archive.writestr(
                _zip_info(item.path, executable=item.path.startswith("scripts/")),
                item.source_path.read_bytes(),
            )

    bundle_size = bundle_path.stat().st_size
    if bundle_size > MAX_BUNDLE_BYTES:
        bundle_path.unlink(missing_ok=True)
        raise ReleaseError(f"release bundle exceeds {MAX_BUNDLE_BYTES} bytes")
    bundle_sha256 = _sha256_file(bundle_path)
    release = {
        "schemaVersion": SCHEMA_VERSION,
        "skillId": skill_id,
        "version": version,
        "bundleFile": bundle_path.name,
        "bundleSha256": bundle_sha256,
        "bundleSizeBytes": bundle_size,
    }
    release_path = output_dir / f"{base_name}.release.json"
    release_path.write_text(json.dumps(release, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return bundle_path, release_path


def _validate_archive(bundle_path: Path, release: dict[str, Any]) -> dict[str, Any]:
    expected_files: dict[str, dict[str, Any]] = {}
    with zipfile.ZipFile(bundle_path, "r") as archive:
        infos = archive.infolist()
        if len(infos) > MAX_FILES + 1:
            raise ReleaseError("bundle contains too many files")
        names: set[str] = set()
        for info in infos:
            safe = _safe_relative_path(info.filename)
            if info.filename in names:
                raise ReleaseError(f"duplicate bundle path: {info.filename}")
            names.add(info.filename)
            if info.is_dir():
                raise ReleaseError("directory entries are not allowed in official bundles")
            unix_mode = (info.external_attr >> 16) & 0o170000
            if unix_mode and unix_mode != stat.S_IFREG:
                raise ReleaseError(f"non-regular archive entry: {safe}")
            if info.file_size > MAX_FILE_BYTES:
                raise ReleaseError(f"archive entry exceeds size limit: {safe}")
        if "manifest.json" not in names:
            raise ReleaseError("bundle is missing manifest.json")
        manifest = json.loads(archive.read("manifest.json"))
        if (
            not isinstance(manifest, dict)
            or manifest.get("schemaVersion") != SCHEMA_VERSION
            or manifest.get("skillId") != release.get("skillId")
            or manifest.get("version") != release.get("version")
            or manifest.get("entrypoint") != SKILL_FILENAME
            or not isinstance(manifest.get("files"), list)
        ):
            raise ReleaseError("bundle manifest does not match release metadata")
        for raw in manifest["files"]:
            if not isinstance(raw, dict):
                raise ReleaseError("invalid manifest file entry")
            path = str(_safe_relative_path(str(raw.get("path", ""))))
            if path in expected_files or path == "manifest.json":
                raise ReleaseError(f"duplicate manifest file: {path}")
            expected_files[path] = raw
        if set(expected_files) | {"manifest.json"} != names:
            raise ReleaseError("bundle files do not exactly match manifest")
        for path, raw in expected_files.items():
            contents = archive.read(path)
            if raw.get("sizeBytes") != len(contents) or raw.get("sha256") != _sha256_bytes(contents):
                raise ReleaseError(f"bundle file integrity failed: {path}")
    return manifest


def verify_release(*, bundle_path: Path, release_path: Path) -> dict[str, Any]:
    release = json.loads(release_path.read_text(encoding="utf-8"))
    if not isinstance(release, dict) or release.get("schemaVersion") != SCHEMA_VERSION:
        raise ReleaseError("invalid release metadata")
    actual_size = bundle_path.stat().st_size
    actual_sha256 = _sha256_file(bundle_path)
    if release.get("bundleSizeBytes") != actual_size or release.get("bundleSha256") != actual_sha256:
        raise ReleaseError("bundle hash or size does not match release metadata")
    return _validate_archive(bundle_path, release)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    build = subparsers.add_parser("build")
    build.add_argument("--skill-id", required=True)
    build.add_argument("--version", required=True)
    build.add_argument("--output-dir", type=Path, required=True)
    build.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parent.parent)
    verify = subparsers.add_parser("verify")
    verify.add_argument("--bundle", type=Path, required=True)
    verify.add_argument("--release", type=Path, required=True)
    return parser


def main() -> int:
    args = _parser().parse_args()
    try:
        if args.command == "build":
            bundle, release = build_release(
                repo_root=args.repo_root,
                skill_id=args.skill_id,
                version=args.version,
                output_dir=args.output_dir,
            )
            print(json.dumps({"bundle": str(bundle), "release": str(release)}, sort_keys=True))
        else:
            manifest = verify_release(
                bundle_path=args.bundle,
                release_path=args.release,
            )
            print(json.dumps(manifest, sort_keys=True))
    except (OSError, ReleaseError, json.JSONDecodeError, zipfile.BadZipFile) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
