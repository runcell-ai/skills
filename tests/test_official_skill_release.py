from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest


REPO_ROOT = Path(__file__).resolve().parent.parent
MODULE_PATH = REPO_ROOT / "scripts" / "official_skill_release.py"
SPEC = importlib.util.spec_from_file_location("official_skill_release", MODULE_PATH)
assert SPEC and SPEC.loader
release_tool = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = release_tool
SPEC.loader.exec_module(release_tool)


def test_real_academic_skill_build_is_deterministic_and_verifiable(tmp_path: Path) -> None:
    first_bundle, first_release = release_tool.build_release(
        repo_root=REPO_ROOT,
        skill_id="academic-visualization",
        version="1.0.0",
        output_dir=tmp_path / "first",
    )
    second_bundle, second_release = release_tool.build_release(
        repo_root=REPO_ROOT,
        skill_id="academic-visualization",
        version="1.0.0",
        output_dir=tmp_path / "second",
    )

    assert first_bundle.read_bytes() == second_bundle.read_bytes()
    assert first_release.read_text(encoding="utf-8") == second_release.read_text(encoding="utf-8")
    manifest = release_tool.verify_release(
        bundle_path=first_bundle,
        release_path=first_release,
    )
    assert manifest["skillId"] == "academic-visualization"
    assert manifest["version"] == "1.0.0"
    assert {entry["path"] for entry in manifest["files"]} == {
        "SKILL.md",
        "assets/publication.mplstyle",
        "references/publication-style.md",
        "references/publisher-requirements.md",
        "scripts/inspect_static_figure.py",
    }


def test_tampered_bundle_is_rejected_before_extraction(tmp_path: Path) -> None:
    bundle, release = release_tool.build_release(
        repo_root=REPO_ROOT,
        skill_id="academic-visualization",
        version="1.0.0",
        output_dir=tmp_path / "dist",
    )
    bundle.write_bytes(bundle.read_bytes() + b"tampered")

    with pytest.raises(release_tool.ReleaseError, match="hash or size"):
        release_tool.verify_release(
            bundle_path=bundle,
            release_path=release,
        )


def test_symlinked_skill_resource_is_rejected(tmp_path: Path) -> None:
    skill_dir = tmp_path / "skills" / "demo"
    skill_dir.mkdir(parents=True)
    (skill_dir / "SKILL.md").write_text(
        "---\nname: demo\ndescription: Demo skill.\n---\n\n# Demo\n",
        encoding="utf-8",
    )
    outside = tmp_path / "outside.txt"
    outside.write_text("outside", encoding="utf-8")
    (skill_dir / "asset.txt").symlink_to(outside)

    with pytest.raises(release_tool.ReleaseError, match="non-regular file"):
        release_tool.collect_skill_files(skill_dir, expected_id="demo")
