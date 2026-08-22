#!/usr/bin/env python3
"""Audit six canonical rack-device PNG views before GLB construction."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

try:
    from PIL import Image
except ImportError as exc:  # pragma: no cover
    raise SystemExit("Pillow is required: python -m pip install Pillow") from exc


FACES = ("front", "rear", "left", "right", "top", "bottom")


def tight_bbox(alpha: Image.Image, threshold: int = 8):
    mask = alpha.point(lambda value: 255 if value > threshold else 0)
    return mask.getbbox()


def percent(count: int, total: int) -> float:
    return round(100.0 * count / total, 5) if total else 0.0


def count_alpha_below(alpha: Image.Image, threshold: int) -> int:
    hist = alpha.histogram()
    return sum(hist[:threshold])


def audit_face(
    path: Path,
    expected_ratio: float,
    min_long_edge: int,
    ratio_tolerance: float,
    core_alpha_limit: float,
) -> dict:
    result = {"path": str(path), "errors": [], "warnings": []}
    if not path.is_file():
        result["errors"].append("missing required PNG")
        return result

    if path.suffix.lower() != ".png":
        result["errors"].append("view must be PNG")

    with Image.open(path) as source:
        image = source.convert("RGBA")
        width, height = image.size
        alpha = image.getchannel("A")
        bbox = tight_bbox(alpha)
        result.update(
            {
                "mode": source.mode,
                "canvas_px": [width, height],
                "content_bbox_px": list(bbox) if bbox else None,
            }
        )

        if max(width, height) < min_long_edge:
            result["errors"].append(
                f"long edge {max(width, height)} px is below {min_long_edge} px"
            )
        if "A" not in source.getbands():
            result["warnings"].append(
                "image has no alpha channel; acceptable only for a fully rectangular face texture"
            )
        if bbox is None:
            result["errors"].append("image contains no visible product pixels")
            return result

        left, top, right, bottom = bbox
        content_width = right - left
        content_height = bottom - top
        actual_ratio = content_width / content_height if content_height else 0.0
        ratio_error = (
            abs(actual_ratio / expected_ratio - 1.0) if expected_ratio else 0.0
        )
        result.update(
            {
                "content_px": [content_width, content_height],
                "actual_ratio": round(actual_ratio, 6),
                "expected_ratio": round(expected_ratio, 6),
                "ratio_error_percent": round(ratio_error * 100.0, 4),
            }
        )
        if ratio_error > ratio_tolerance:
            result["errors"].append(
                f"content aspect ratio differs from physical ratio by {ratio_error * 100:.2f}%"
            )

        cropped_alpha = alpha.crop(bbox)
        inset_x = max(1, round(content_width * 0.08))
        inset_y = max(1, round(content_height * 0.08))
        core_box = (
            inset_x,
            inset_y,
            max(inset_x + 1, content_width - inset_x),
            max(inset_y + 1, content_height - inset_y),
        )
        core = cropped_alpha.crop(core_box)
        core_total = core.width * core.height
        core_below_250 = count_alpha_below(core, 250)
        core_transparent = count_alpha_below(core, 8)
        result.update(
            {
                "core_alpha_below_250_percent": percent(core_below_250, core_total),
                "core_transparent_percent": percent(core_transparent, core_total),
            }
        )
        if percent(core_below_250, core_total) > core_alpha_limit:
            result["errors"].append(
                "suspicious transparency exists inside the opaque chassis core"
            )

        full_total = content_width * content_height
        full_below_250 = count_alpha_below(cropped_alpha, 250)
        result["content_alpha_below_250_percent"] = percent(
            full_below_250, full_total
        )
        if result["content_alpha_below_250_percent"] > 0:
            result["warnings"].append(
                "transparent/semi-transparent pixels exist inside content bounds; verify they are only true holes or anti-aliased silhouette edges"
            )

    return result


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Audit six face PNGs for resolution, physical ratio, and alpha risks."
    )
    parser.add_argument("views_dir", type=Path)
    parser.add_argument("--width-mm", type=float, required=True, help="body width")
    parser.add_argument("--height-mm", type=float, required=True)
    parser.add_argument("--depth-mm", type=float, required=True, help="body depth")
    parser.add_argument(
        "--front-width-mm",
        type=float,
        help="front silhouette width when front ears are included",
    )
    parser.add_argument(
        "--rear-width-mm",
        type=float,
        help="rear silhouette width when verified rear hardware changes it",
    )
    parser.add_argument("--front-rear-min-long-edge", type=int, default=2048)
    parser.add_argument("--other-min-long-edge", type=int, default=1536)
    parser.add_argument("--ratio-tolerance", type=float, default=0.03)
    parser.add_argument(
        "--core-alpha-limit-percent",
        type=float,
        default=0.05,
        help="maximum pixels below alpha 250 in the inset chassis core",
    )
    parser.add_argument("--json-out", type=Path)
    args = parser.parse_args()

    for label, value in (
        ("width", args.width_mm),
        ("height", args.height_mm),
        ("depth", args.depth_mm),
    ):
        if value <= 0:
            parser.error(f"{label} must be positive")

    front_width = args.front_width_mm or args.width_mm
    rear_width = args.rear_width_mm or args.width_mm
    ratios = {
        "front": front_width / args.height_mm,
        "rear": rear_width / args.height_mm,
        "left": args.depth_mm / args.height_mm,
        "right": args.depth_mm / args.height_mm,
        "top": args.width_mm / args.depth_mm,
        "bottom": args.width_mm / args.depth_mm,
    }

    report = {
        "views_dir": str(args.views_dir),
        "dimensions_mm": {
            "body_width": args.width_mm,
            "front_width": front_width,
            "rear_width": rear_width,
            "height": args.height_mm,
            "body_depth": args.depth_mm,
        },
        "faces": {},
    }
    for face in FACES:
        minimum = (
            args.front_rear_min_long_edge
            if face in ("front", "rear")
            else args.other_min_long_edge
        )
        report["faces"][face] = audit_face(
            args.views_dir / f"{face}.png",
            ratios[face],
            minimum,
            args.ratio_tolerance,
            args.core_alpha_limit_percent,
        )

    report["error_count"] = sum(
        len(item["errors"]) for item in report["faces"].values()
    )
    report["warning_count"] = sum(
        len(item["warnings"]) for item in report["faces"].values()
    )
    report["status"] = "PASS" if report["error_count"] == 0 else "REWORK"

    output = json.dumps(report, ensure_ascii=False, indent=2)
    print(output)
    if args.json_out:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(output + "\n", encoding="utf-8")
    return 0 if report["error_count"] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
