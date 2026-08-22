#!/usr/bin/env python3
"""Create a same-camera reference/render comparison sheet for visual QA."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

try:
    from PIL import Image, ImageChops, ImageDraw, ImageEnhance
except ImportError as exc:  # pragma: no cover
    raise SystemExit("Pillow is required: python -m pip install Pillow") from exc


def parse_hex_color(value: str) -> tuple[int, int, int, int]:
    text = value.strip().lstrip("#")
    if len(text) == 6:
        return tuple(int(text[index : index + 2], 16) for index in (0, 2, 4)) + (255,)
    if len(text) == 8:
        return tuple(int(text[index : index + 2], 16) for index in (0, 2, 4, 6))
    raise argparse.ArgumentTypeError("background must be #RRGGBB or #RRGGBBAA")


def composite(image: Image.Image, background: tuple[int, int, int, int]) -> Image.Image:
    rgba = image.convert("RGBA")
    canvas = Image.new("RGBA", rgba.size, background)
    canvas.alpha_composite(rgba)
    return canvas.convert("RGB")


def labeled_panel(image: Image.Image, label: str, label_height: int = 36) -> Image.Image:
    panel = Image.new("RGB", (image.width, image.height + label_height), (28, 28, 28))
    panel.paste(image, (0, label_height))
    draw = ImageDraw.Draw(panel)
    draw.text((12, 10), label, fill=(245, 245, 245))
    return panel


def mean_abs_difference(difference: Image.Image) -> float:
    grayscale = difference.convert("L")
    histogram = grayscale.histogram()
    total = grayscale.width * grayscale.height
    return round(sum(value * count for value, count in enumerate(histogram)) / total, 6)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Create reference/render/overlay/difference panels without resizing."
    )
    parser.add_argument("reference", type=Path)
    parser.add_argument("render", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--background", type=parse_hex_color, default=parse_hex_color("#D0D0D0"))
    parser.add_argument("--difference-gain", type=float, default=3.0)
    args = parser.parse_args()

    if args.difference_gain <= 0:
        parser.error("--difference-gain must be positive")
    if not args.reference.is_file():
        parser.error(f"reference not found: {args.reference}")
    if not args.render.is_file():
        parser.error(f"render not found: {args.render}")

    with Image.open(args.reference) as reference_source, Image.open(args.render) as render_source:
        if reference_source.size != render_source.size:
            parser.error(
                "reference and render pixel dimensions differ; match camera/crop/canvas instead of stretching"
            )
        reference = composite(reference_source, args.background)
        render = composite(render_source, args.background)

    overlay = Image.blend(reference, render, 0.5)
    raw_difference = ImageChops.difference(reference, render)
    shown_difference = ImageEnhance.Brightness(raw_difference).enhance(args.difference_gain)

    panels = [
        labeled_panel(reference, "EXACT REFERENCE"),
        labeled_panel(render, "ACTUAL GLB RENDER"),
        labeled_panel(overlay, "50% OVERLAY"),
        labeled_panel(shown_difference, f"DIFFERENCE x{args.difference_gain:g}"),
    ]
    panel_width, panel_height = panels[0].size
    sheet = Image.new("RGB", (panel_width * 2, panel_height * 2), (18, 18, 18))
    for index, panel in enumerate(panels):
        sheet.paste(panel, ((index % 2) * panel_width, (index // 2) * panel_height))

    args.output.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(args.output)
    summary = {
        "reference": str(args.reference),
        "render": str(args.render),
        "output": str(args.output),
        "size_px": list(reference.size),
        "mean_absolute_rgb_difference_0_to_255": mean_abs_difference(raw_difference),
        "note": "Difference is diagnostic only; exact acceptance requires feature-by-feature review.",
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
