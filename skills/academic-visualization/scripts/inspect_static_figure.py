#!/usr/bin/env python3
"""Report static-figure dimensions, hashes, margins, and optional pixel diffs."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

from PIL import Image, ImageChops


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def inspect_image(
    path: Path,
    target_width_in: float | None,
    target_height_in: float | None,
    min_dpi: float | None,
) -> dict[str, Any]:
    with Image.open(path) as opened:
        image = opened.convert("RGB")
        width_px, height_px = image.size
        embedded_dpi = opened.info.get("dpi")
        if isinstance(embedded_dpi, tuple):
            embedded_dpi = [round(float(value), 3) for value in embedded_dpi[:2]]
        else:
            embedded_dpi = None

        background = Image.new("RGB", image.size, image.getpixel((0, 0)))
        content_bbox = ImageChops.difference(image, background).getbbox()
        margins = None
        if content_bbox:
            left, top, right, bottom = content_bbox
            margins = {
                "left_px": left,
                "top_px": top,
                "right_px": width_px - right,
                "bottom_px": height_px - bottom,
                "left_fraction": round(left / width_px, 5),
                "top_fraction": round(top / height_px, 5),
                "right_fraction": round((width_px - right) / width_px, 5),
                "bottom_fraction": round((height_px - bottom) / height_px, 5),
            }

    effective_dpi = None
    meets_min_dpi = None
    if target_width_in and target_height_in:
        dpi_x = width_px / target_width_in
        dpi_y = height_px / target_height_in
        effective_dpi = [round(dpi_x, 3), round(dpi_y, 3)]
        if min_dpi is not None:
            meets_min_dpi = min(dpi_x, dpi_y) >= min_dpi

    return {
        "path": str(path.resolve()),
        "sha256": sha256(path),
        "width_px": width_px,
        "height_px": height_px,
        "embedded_dpi": embedded_dpi,
        "target_size_in": (
            [target_width_in, target_height_in]
            if target_width_in and target_height_in
            else None
        ),
        "effective_dpi": effective_dpi,
        "requested_min_dpi": min_dpi,
        "meets_min_dpi": meets_min_dpi,
        "corner_background_content_bbox": content_bbox,
        "corner_background_margins": margins,
    }


def compare_images(first_path: Path, second_path: Path) -> dict[str, Any]:
    with Image.open(first_path) as first_opened, Image.open(second_path) as second_opened:
        first = first_opened.convert("RGBA")
        second = second_opened.convert("RGBA")
        if first.size != second.size:
            return {
                "same_dimensions": False,
                "first_size": list(first.size),
                "second_size": list(second.size),
                "changed_pixels": None,
                "difference_bbox": None,
            }

        difference = ImageChops.difference(first, second).convert("RGB")
        difference_bbox = difference.getbbox()
        pixel_data = (
            difference.get_flattened_data()
            if hasattr(difference, "get_flattened_data")
            else difference.getdata()
        )
        changed_pixels = sum(pixel != (0, 0, 0) for pixel in pixel_data)
        return {
            "same_dimensions": True,
            "first_size": list(first.size),
            "second_size": list(second.size),
            "changed_pixels": changed_pixels,
            "changed_fraction": round(changed_pixels / (first.width * first.height), 8),
            "difference_bbox": difference_bbox,
            "pixel_identical": changed_pixels == 0,
        }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("images", type=Path, nargs="+", help="One image to inspect or two to compare")
    parser.add_argument("--target-width-in", type=float)
    parser.add_argument("--target-height-in", type=float)
    parser.add_argument(
        "--min-dpi",
        type=float,
        help="target-specific raster threshold; omitted means report DPI without pass/fail",
    )
    args = parser.parse_args()
    if len(args.images) not in (1, 2):
        parser.error("provide one image to inspect or two images to inspect and compare")
    if (args.target_width_in is None) != (args.target_height_in is None):
        parser.error("target width and height must be provided together")
    for image_path in args.images:
        if not image_path.is_file():
            parser.error(f"image not found: {image_path}")
    return args


def main() -> None:
    args = parse_args()
    report: dict[str, Any] = {
        "images": [
            inspect_image(
                path,
                args.target_width_in,
                args.target_height_in,
                args.min_dpi,
            )
            for path in args.images
        ]
    }
    if len(args.images) == 2:
        report["comparison"] = compare_images(args.images[0], args.images[1])
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
