#!/usr/bin/env python3
"""Produce PDF page previews with a locally installed Poppler executable."""

import argparse
import json
import shutil
import subprocess
import tempfile
from pathlib import Path


def render(source: Path, output: Path, *, pdftoppm: str = "pdftoppm",
           dpi: int = 120, timeout: int = 120) -> dict:
    source, output = source.resolve(), output.resolve()
    if not source.is_file():
        raise ValueError("Input PDF does not exist")
    if not 36 <= dpi <= 600 or timeout <= 0:
        raise ValueError("DPI must be 36–600 and timeout must be positive")
    command = shutil.which(pdftoppm)
    if not command:
        raise FileNotFoundError(f"Poppler executable not found: {pdftoppm}")
    if output.exists() and (not output.is_dir() or any(output.iterdir())):
        raise ValueError("Output directory must be new or empty")
    output.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="pdf-preview-") as temporary:
        work = Path(temporary)
        result = subprocess.run(
            [command, "-png", "-r", str(dpi), str(source), str(work / "page")],
            capture_output=True, text=True, timeout=timeout,
        )
        if result.returncode:
            raise RuntimeError(f"PDF rendering failed ({result.returncode})\n"
                               f"{result.stdout}\n{result.stderr}")
        pages = sorted(work.glob("page-*.png"), key=lambda p: int(p.stem.split("-")[-1]))
        if not pages or any(not page.stat().st_size for page in pages):
            raise RuntimeError("Poppler produced no usable page images")
        for page in pages:
            shutil.copyfile(page, output / page.name)
    return {"pages": [str(output / page.name) for page in pages]}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--pdftoppm", default="pdftoppm")
    parser.add_argument("--dpi", type=int, default=120)
    parser.add_argument("--timeout", type=int, default=120)
    args = parser.parse_args()
    print(json.dumps(render(args.input, args.output_dir, pdftoppm=args.pdftoppm,
                            dpi=args.dpi, timeout=args.timeout)))


if __name__ == "__main__":
    main()
