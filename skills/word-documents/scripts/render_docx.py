#!/usr/bin/env python3
"""Render a local DOCX with explicitly selected or PATH-based office tools."""

import argparse
import json
import shutil
import subprocess
import tempfile
from pathlib import Path


def executable(value: str) -> str:
    found = shutil.which(value)
    if not found:
        raise FileNotFoundError(f"Executable not found: {value}. Install it or pass its path.")
    return found


def render(source: Path, output: Path, *, soffice: str = "soffice",
           pdftoppm: str = "pdftoppm", dpi: int = 120, timeout: int = 120) -> dict:
    source, output = source.resolve(), output.resolve()
    if not source.is_file() or source.suffix.lower() != ".docx":
        raise ValueError("Input must be an existing .docx file")
    if not 36 <= dpi <= 600 or timeout <= 0:
        raise ValueError("DPI must be 36–600 and timeout must be positive")
    office, poppler = executable(soffice), executable(pdftoppm)
    if output.exists() and (not output.is_dir() or any(output.iterdir())):
        raise ValueError("Output directory must be new or empty")
    output.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="word-preview-") as temporary:
        work = Path(temporary)
        staged = work / "document.docx"
        shutil.copyfile(source, staged)
        profile = work / "profile"
        conversion = subprocess.run(
            [office, f"-env:UserInstallation={profile.as_uri()}", "--headless",
             "--convert-to", "pdf", "--outdir", str(work), str(staged)],
            capture_output=True, text=True, timeout=timeout,
        )
        pdf = work / "document.pdf"
        if conversion.returncode or not pdf.is_file() or not pdf.stat().st_size:
            raise RuntimeError(f"DOCX conversion failed ({conversion.returncode})\n"
                               f"{conversion.stdout}\n{conversion.stderr}")
        result = subprocess.run(
            [poppler, "-png", "-r", str(dpi), str(pdf), str(work / "page")],
            capture_output=True, text=True, timeout=timeout,
        )
        if result.returncode:
            raise RuntimeError(f"Page rendering failed\n{result.stdout}\n{result.stderr}")
        pages = sorted(work.glob("page-*.png"), key=lambda p: int(p.stem.split("-")[-1]))
        if not pages or any(not page.stat().st_size for page in pages):
            raise RuntimeError("Renderer did not produce nonempty page images")
        shutil.copyfile(pdf, output / "document.pdf")
        for page in pages:
            shutil.copyfile(page, output / page.name)
    return {"pdf": str(output / "document.pdf"), "pages": [str(output / p.name) for p in pages]}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--soffice", default="soffice")
    parser.add_argument("--pdftoppm", default="pdftoppm")
    parser.add_argument("--dpi", type=int, default=120)
    parser.add_argument("--timeout", type=int, default=120, help="Seconds per subprocess")
    args = parser.parse_args()
    print(json.dumps(render(args.input, args.output_dir, soffice=args.soffice,
                            pdftoppm=args.pdftoppm, dpi=args.dpi, timeout=args.timeout)))


if __name__ == "__main__":
    main()
