#!/usr/bin/env python3
"""Perform deterministic structural checks on a website GLB asset."""

from __future__ import annotations

import argparse
import base64
import io
import json
import math
import struct
import sys
from pathlib import Path
from urllib.parse import unquote_to_bytes

try:
    from PIL import Image
except ImportError as exc:  # pragma: no cover
    raise SystemExit("Pillow is required: python -m pip install Pillow") from exc


JSON_CHUNK = 0x4E4F534A
BIN_CHUNK = 0x004E4942


def identity():
    return [
        [1.0, 0.0, 0.0, 0.0],
        [0.0, 1.0, 0.0, 0.0],
        [0.0, 0.0, 1.0, 0.0],
        [0.0, 0.0, 0.0, 1.0],
    ]


def matmul(a, b):
    return [
        [sum(a[row][k] * b[k][col] for k in range(4)) for col in range(4)]
        for row in range(4)
    ]


def transform_point(matrix, point):
    x, y, z = point
    values = [x, y, z, 1.0]
    out = [sum(matrix[row][i] * values[i] for i in range(4)) for row in range(4)]
    if out[3] and out[3] != 1.0:
        return [out[i] / out[3] for i in range(3)]
    return out[:3]


def determinant3(matrix):
    a, b, c = matrix[0][:3]
    d, e, f = matrix[1][:3]
    g, h, i = matrix[2][:3]
    return a * (e * i - f * h) - b * (d * i - f * g) + c * (d * h - e * g)


def node_matrix(node):
    if "matrix" in node:
        flat = node["matrix"]
        return [[float(flat[col * 4 + row]) for col in range(4)] for row in range(4)]

    tx, ty, tz = node.get("translation", [0.0, 0.0, 0.0])
    sx, sy, sz = node.get("scale", [1.0, 1.0, 1.0])
    x, y, z, w = node.get("rotation", [0.0, 0.0, 0.0, 1.0])
    length = math.sqrt(x * x + y * y + z * z + w * w) or 1.0
    x, y, z, w = x / length, y / length, z / length, w / length

    rotation = [
        [1 - 2 * (y * y + z * z), 2 * (x * y - z * w), 2 * (x * z + y * w), 0],
        [2 * (x * y + z * w), 1 - 2 * (x * x + z * z), 2 * (y * z - x * w), 0],
        [2 * (x * z - y * w), 2 * (y * z + x * w), 1 - 2 * (x * x + y * y), 0],
        [0, 0, 0, 1],
    ]
    scale = [
        [sx, 0, 0, 0],
        [0, sy, 0, 0],
        [0, 0, sz, 0],
        [0, 0, 0, 1],
    ]
    translation = identity()
    translation[0][3], translation[1][3], translation[2][3] = tx, ty, tz
    return matmul(translation, matmul(rotation, scale))


def parse_glb(path: Path):
    payload = path.read_bytes()
    if len(payload) < 12:
        raise ValueError("file is too short to be GLB")
    magic, version, declared_length = struct.unpack_from("<4sII", payload, 0)
    if magic != b"glTF":
        raise ValueError("invalid GLB magic")
    if version != 2:
        raise ValueError(f"unsupported GLB version {version}; expected 2")
    if declared_length != len(payload):
        raise ValueError(
            f"declared GLB length {declared_length} differs from file size {len(payload)}"
        )

    json_bytes = None
    binary_chunks = []
    offset = 12
    while offset + 8 <= len(payload):
        chunk_length, chunk_type = struct.unpack_from("<II", payload, offset)
        offset += 8
        chunk = payload[offset : offset + chunk_length]
        if len(chunk) != chunk_length:
            raise ValueError("truncated GLB chunk")
        offset += chunk_length
        if chunk_type == JSON_CHUNK:
            json_bytes = chunk
        elif chunk_type == BIN_CHUNK:
            binary_chunks.append(chunk)
    if json_bytes is None:
        raise ValueError("GLB has no JSON chunk")
    document = json.loads(json_bytes.rstrip(b"\x00 \t\r\n").decode("utf-8"))
    binary = binary_chunks[0] if binary_chunks else b""
    return document, binary, len(payload)


def decode_data_uri(uri: str):
    header, encoded = uri.split(",", 1)
    if ";base64" in header:
        return base64.b64decode(encoded)
    return unquote_to_bytes(encoded)


def embedded_image_bytes(document, binary, image_def):
    if "bufferView" in image_def:
        view = document.get("bufferViews", [])[image_def["bufferView"]]
        if view.get("buffer", 0) != 0:
            return None, "image bufferView references a non-embedded buffer"
        start = view.get("byteOffset", 0)
        end = start + view["byteLength"]
        return binary[start:end], None
    uri = image_def.get("uri")
    if isinstance(uri, str) and uri.startswith("data:"):
        return decode_data_uri(uri), None
    if uri:
        return None, f"external image URI: {uri}"
    return None, "image has neither bufferView nor URI"


def inspect_images(document, binary, minimum_long_edge):
    results = []
    for index, image_def in enumerate(document.get("images", [])):
        item = {"index": index, "name": image_def.get("name"), "errors": [], "warnings": []}
        try:
            raw, problem = embedded_image_bytes(document, binary, image_def)
        except Exception as exc:
            raw, problem = None, f"cannot decode image data: {exc}"
        if problem:
            item["errors"].append(problem)
            results.append(item)
            continue
        try:
            with Image.open(io.BytesIO(raw)) as image:
                width, height = image.size
                item.update({"format": image.format, "mode": image.mode, "size_px": [width, height]})
                if max(width, height) < minimum_long_edge:
                    item["warnings"].append(
                        f"long edge {max(width, height)} px is below {minimum_long_edge} px"
                    )
                alpha = image.convert("RGBA").getchannel("A")
                histogram = alpha.histogram()
                total = width * height
                item["transparent_percent"] = round(100 * sum(histogram[:8]) / total, 5)
                item["semi_transparent_percent"] = round(100 * sum(histogram[8:255]) / total, 5)
                if item["semi_transparent_percent"] > 0.1:
                    item["warnings"].append(
                        "image contains substantial partial alpha; verify this is only edge antialiasing"
                    )
        except Exception as exc:
            item["errors"].append(f"cannot inspect embedded image: {exc}")
        results.append(item)
    return results


def material_texture_index(document, material):
    info = material.get("pbrMetallicRoughness", {}).get("baseColorTexture")
    if not info:
        return None
    texture_index = info.get("index")
    if texture_index is None or texture_index >= len(document.get("textures", [])):
        return None
    return texture_index


def inspect_materials(document, image_results):
    results = []
    textures = document.get("textures", [])
    for index, material in enumerate(document.get("materials", [])):
        pbr = material.get("pbrMetallicRoughness", {})
        alpha_mode = material.get("alphaMode", "OPAQUE")
        base_factor = pbr.get("baseColorFactor", [1, 1, 1, 1])
        unlit = "KHR_materials_unlit" in material.get("extensions", {})
        item = {
            "index": index,
            "name": material.get("name"),
            "alpha_mode": alpha_mode,
            "base_color_factor": base_factor,
            "metallic_factor": pbr.get("metallicFactor", 1.0),
            "roughness_factor": pbr.get("roughnessFactor", 1.0),
            "double_sided": material.get("doubleSided", False),
            "unlit": unlit,
            "errors": [],
            "warnings": [],
        }
        texture_index = material_texture_index(document, material)
        item["base_color_texture"] = texture_index
        source_index = None
        if texture_index is not None:
            source_index = textures[texture_index].get("source")
        item["base_color_image"] = source_index

        if alpha_mode == "BLEND":
            item["errors"].append("BLEND is unsafe for a main equipment face")
        elif alpha_mode == "MASK":
            item["warnings"].append(
                "MASK must be isolated to a verified perforated part, never a full chassis face"
            )
        if len(base_factor) >= 4 and base_factor[3] < 0.999:
            item["errors"].append("baseColorFactor alpha is below 1")
        if material.get("doubleSided", False):
            item["warnings"].append("doubleSided material can hide incorrect normals")
        if texture_index is not None and not unlit and pbr.get("metallicFactor", 1.0) > 0.1:
            item["warnings"].append(
                "photo-textured material has metallicFactor > 0.1 and may render gray/dark"
            )
        if unlit and [round(float(v), 6) for v in base_factor] != [1, 1, 1, 1]:
            item["warnings"].append("unlit material uses a non-neutral baseColorFactor")
        if source_index is not None and source_index < len(image_results):
            image_alpha = image_results[source_index].get("semi_transparent_percent", 0)
            image_transparent = image_results[source_index].get("transparent_percent", 0)
            if alpha_mode != "OPAQUE" and image_alpha > 0.1:
                item["errors"].append(
                    "non-opaque material uses a texture with substantial partial alpha"
                )
            if alpha_mode != "OPAQUE" and image_transparent > 5:
                item["warnings"].append(
                    "non-opaque material exposes a large transparent area; verify it is not the chassis"
                )
        results.append(item)
    return results


def scene_roots(document):
    scenes = document.get("scenes", [])
    if scenes:
        scene_index = document.get("scene", 0)
        return scenes[scene_index].get("nodes", [])
    child_nodes = {child for node in document.get("nodes", []) for child in node.get("children", [])}
    return [index for index in range(len(document.get("nodes", []))) if index not in child_nodes]


def inspect_nodes_and_bounds(document):
    nodes = document.get("nodes", [])
    meshes = document.get("meshes", [])
    accessors = document.get("accessors", [])
    mirrored = []
    missing_bounds = []
    bounds_min = [math.inf, math.inf, math.inf]
    bounds_max = [-math.inf, -math.inf, -math.inf]
    visited_stack = set()

    def add_accessor_bounds(accessor_index, world, label):
        nonlocal bounds_min, bounds_max
        if accessor_index >= len(accessors):
            missing_bounds.append(f"{label}: invalid POSITION accessor")
            return
        accessor = accessors[accessor_index]
        if "min" not in accessor or "max" not in accessor:
            missing_bounds.append(f"{label}: POSITION accessor lacks min/max")
            return
        lo, hi = accessor["min"], accessor["max"]
        for x in (lo[0], hi[0]):
            for y in (lo[1], hi[1]):
                for z in (lo[2], hi[2]):
                    point = transform_point(world, [x, y, z])
                    for axis in range(3):
                        bounds_min[axis] = min(bounds_min[axis], point[axis])
                        bounds_max[axis] = max(bounds_max[axis], point[axis])

    def walk(node_index, parent):
        if node_index in visited_stack:
            return
        visited_stack.add(node_index)
        node = nodes[node_index]
        world = matmul(parent, node_matrix(node))
        if determinant3(world) < -1e-9:
            mirrored.append({"index": node_index, "name": node.get("name")})
        mesh_index = node.get("mesh")
        if mesh_index is not None and mesh_index < len(meshes):
            for primitive_index, primitive in enumerate(meshes[mesh_index].get("primitives", [])):
                position = primitive.get("attributes", {}).get("POSITION")
                if position is not None:
                    add_accessor_bounds(position, world, f"node {node_index} primitive {primitive_index}")
        for child in node.get("children", []):
            walk(child, world)
        visited_stack.remove(node_index)

    for root in scene_roots(document):
        walk(root, identity())

    valid = all(math.isfinite(value) for value in bounds_min + bounds_max)
    dimensions = [bounds_max[i] - bounds_min[i] for i in range(3)] if valid else None
    return {
        "mirrored_nodes": mirrored,
        "missing_accessor_bounds": missing_bounds,
        "bounds_min": bounds_min if valid else None,
        "bounds_max": bounds_max if valid else None,
        "dimensions_xyz": dimensions,
    }


def inspect_primitives(document):
    materials = document.get("materials", [])
    results = []
    for mesh_index, mesh in enumerate(document.get("meshes", [])):
        for primitive_index, primitive in enumerate(mesh.get("primitives", [])):
            material_index = primitive.get("material")
            attributes = primitive.get("attributes", {})
            uses_texture = False
            if material_index is not None and material_index < len(materials):
                uses_texture = material_texture_index(document, materials[material_index]) is not None
            item = {
                "mesh": mesh_index,
                "primitive": primitive_index,
                "material": material_index,
                "has_position": "POSITION" in attributes,
                "has_normal": "NORMAL" in attributes,
                "has_uv0": "TEXCOORD_0" in attributes,
                "errors": [],
                "warnings": [],
            }
            if "POSITION" not in attributes:
                item["errors"].append("primitive has no POSITION")
            if "NORMAL" not in attributes:
                item["warnings"].append("primitive has no NORMAL")
            if uses_texture and "TEXCOORD_0" not in attributes:
                item["errors"].append("textured primitive has no TEXCOORD_0")
            results.append(item)
    return results


def compare_dimensions(actual, expected_mm, tolerance):
    result = {"expected_mm": expected_mm, "errors": [], "warnings": []}
    if not actual:
        result["errors"].append("could not compute world-space bounds")
        return result
    if any(value <= 0 for value in actual):
        result["errors"].append("computed model has a zero or negative dimension")
        return result
    scales = [actual[i] / expected_mm[i] for i in range(3)]
    mean_scale = sum(scales) / 3.0
    spread = max(abs(value / mean_scale - 1.0) for value in scales)
    result.update(
        {
            "actual_xyz": [round(value, 8) for value in actual],
            "units_per_mm_xyz": [round(value, 10) for value in scales],
            "nonuniform_ratio_error_percent": round(spread * 100.0, 4),
        }
    )
    if spread > tolerance:
        result["errors"].append(
            f"model proportions differ from expected W/H/D by {spread * 100:.2f}%"
        )
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit a GLB's structure, textures, materials, transforms, and proportions.")
    parser.add_argument("glb", type=Path)
    parser.add_argument("--expected-width-mm", type=float)
    parser.add_argument("--expected-height-mm", type=float)
    parser.add_argument("--expected-depth-mm", type=float)
    parser.add_argument("--dimension-tolerance", type=float, default=0.03)
    parser.add_argument("--min-texture-long-edge", type=int, default=1024)
    parser.add_argument("--min-basecolor-images", type=int, default=1)
    parser.add_argument("--json-out", type=Path)
    args = parser.parse_args()

    errors, warnings = [], []
    try:
        document, binary, byte_size = parse_glb(args.glb)
    except Exception as exc:
        report = {"path": str(args.glb), "status": "REWORK", "errors": [str(exc)], "warnings": []}
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 1

    images = inspect_images(document, binary, args.min_texture_long_edge)
    materials = inspect_materials(document, images)
    primitives = inspect_primitives(document)
    geometry = inspect_nodes_and_bounds(document)

    if geometry["mirrored_nodes"]:
        errors.append("negative-determinant node transforms can mirror UVs/normals")
    if geometry["missing_accessor_bounds"]:
        warnings.append("some POSITION accessors lack bounds; world bounds may be incomplete")

    external_buffers = [
        buffer.get("uri")
        for buffer in document.get("buffers", [])
        if buffer.get("uri") and not buffer.get("uri", "").startswith("data:")
    ]
    if external_buffers:
        errors.append("GLB references external buffers and is not self-contained")

    unique_basecolor_images = {
        item["base_color_image"]
        for item in materials
        if item.get("base_color_image") is not None
    }
    if len(unique_basecolor_images) < args.min_basecolor_images:
        errors.append(
            f"only {len(unique_basecolor_images)} unique base-color images; expected at least {args.min_basecolor_images}"
        )

    expected_values = [args.expected_width_mm, args.expected_height_mm, args.expected_depth_mm]
    dimensions = None
    if any(value is not None for value in expected_values):
        if not all(value is not None and value > 0 for value in expected_values):
            parser.error("provide all three positive expected W/H/D dimensions together")
        dimensions = compare_dimensions(
            geometry["dimensions_xyz"], expected_values, args.dimension_tolerance
        )
        errors.extend(dimensions["errors"])
        warnings.extend(dimensions["warnings"])

    for group in (images, materials, primitives):
        for item in group:
            errors.extend(item.get("errors", []))
            warnings.extend(item.get("warnings", []))

    report = {
        "path": str(args.glb),
        "byte_size": byte_size,
        "asset": document.get("asset", {}),
        "extensions_used": document.get("extensionsUsed", []),
        "extensions_required": document.get("extensionsRequired", []),
        "counts": {
            "scenes": len(document.get("scenes", [])),
            "nodes": len(document.get("nodes", [])),
            "meshes": len(document.get("meshes", [])),
            "primitives": len(primitives),
            "materials": len(materials),
            "textures": len(document.get("textures", [])),
            "images": len(images),
            "unique_basecolor_images": len(unique_basecolor_images),
        },
        "geometry": geometry,
        "dimension_check": dimensions,
        "images": images,
        "materials": materials,
        "primitives": primitives,
        "external_buffers": external_buffers,
        "errors": sorted(set(errors)),
        "warnings": sorted(set(warnings)),
    }
    report["error_count"] = len(report["errors"])
    report["warning_count"] = len(report["warnings"])
    report["status"] = "PASS" if not report["errors"] else "REWORK"

    output = json.dumps(report, ensure_ascii=False, indent=2)
    print(output)
    if args.json_out:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(output + "\n", encoding="utf-8")
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
