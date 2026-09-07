#!/usr/bin/env python3
"""Read-only, stdlib GLB 2 artifact inspector; JSON stdout, exit 1 on failure.

This is a limited artifact inspector, NOT a full glTF validator. It checks GLB
chunk and bufferView byte bounds, not accessor payloads or extension semantics.
It cannot prove mesh manifoldness, model fidelity, actual holes, or UV correctness
and does not decode images. External resources are reported, never opened.
Triangle counts use declared accessor counts, include degenerate triangles, and
count all node.mesh references (not just an active scene). GPU instancing is not
expanded. Optional POSITION bounds are declared accessor-local values, not world
bounds; use --include-position-bounds to include each accessor's values.
See https://registry.khronos.org/glTF/specs/2.0/glTF-2.0.html .
"""

import argparse
import base64
from collections import Counter
import hashlib
import json
import math
from pathlib import Path
import struct
from urllib.parse import unquote_to_bytes


JSON_CHUNK, BIN_CHUNK = 0x4E4F534A, 0x004E4942


def require(condition, message):
    if not condition:
        raise ValueError(message)


def integer(value, label, minimum=0):
    require(type(value) is int and value >= minimum, f"{label}: invalid integer")
    return value


def reference(items, index, label):
    integer(index, label)
    require(index < len(items), f"{label}: index {index} out of range")
    return items[index]


def finite_float(value):
    result = float(value)
    require(math.isfinite(result), f"non-finite JSON number {value}")
    return result


def parse_glb(data):
    require(len(data) >= 12, "truncated GLB header")
    magic, version, length = struct.unpack_from("<4sII", data)
    require(magic == b"glTF" and version == 2, "expected GLB magic and version 2")
    require(length == len(data), "GLB declared length does not match file length")
    chunks, payloads, offset = [], {}, 12
    while offset < length:
        require(offset + 8 <= length, "truncated chunk header")
        size, kind = struct.unpack_from("<II", data, offset)
        end = offset + 8 + size
        require(end <= length, "chunk payload exceeds file bounds")
        require(size % 4 == 0, "chunk payload length is not 4-byte aligned")
        if not chunks:
            require(kind == JSON_CHUNK, "first chunk must be JSON")
        if kind in (JSON_CHUNK, BIN_CHUNK):
            require(kind not in payloads, "duplicate JSON or BIN chunk")
            require(kind != BIN_CHUNK or len(chunks) == 1, "BIN must be second chunk")
            payloads[kind] = data[offset + 8:end]
        chunks.append({"type": {JSON_CHUNK: "JSON", BIN_CHUNK: "BIN"}.get(kind, hex(kind)),
                       "offset": offset + 8, "byte_length": size})
        offset = end
    require(JSON_CHUNK in payloads, "missing JSON chunk")
    document = json.loads(payloads[JSON_CHUNK].decode("utf-8"),
                          parse_float=finite_float,
                          parse_constant=lambda value: require(False, f"invalid JSON number {value}"))
    require(isinstance(document, dict), "JSON root must be an object")
    require(document.get("asset", {}).get("version") == "2.0", "expected glTF asset.version 2.0")
    return document, payloads.get(BIN_CHUNK), chunks


def uri_storage(uri):
    require(isinstance(uri, str) and bool(uri), "resource URI must be a nonempty string")
    return "data_uri" if uri.startswith("data:") else "external"


def inspect_document(doc, binary, self_contained, opaque_names, include_position_bounds=False):
    errors, warnings, resources = [], [], {"buffers": [], "images": []}
    buffers, views = doc.get("buffers", []), doc.get("bufferViews", [])
    for i, buf in enumerate(buffers):
        size = integer(buf["byteLength"], f"buffer {i} byteLength", 1)
        storage, available = "unresolved", None
        if "uri" in buf:
            storage = uri_storage(buf["uri"])
            if storage == "data_uri":
                header, separator, encoded = buf["uri"].partition(",")
                require(separator, f"buffer {i}: malformed data URI")
                raw = unquote_to_bytes(encoded)
                available = len(base64.b64decode(raw, validate=True) if header.endswith(";base64") else raw)
        elif i == 0:
            require(binary is not None, "buffer 0 requires a missing BIN chunk")
            storage, available = "bin", len(binary)
            require(available >= size, "buffer 0 byteLength exceeds BIN payload")
            require(available - size <= 3, "BIN padding exceeds 3 bytes")
            require(not any(binary[size:]), "BIN padding must be zero")
        if available is not None:
            require(size <= available, f"buffer {i} byteLength exceeds embedded payload")
        item = {"index": i, "storage": storage, "byte_length": size, "available_bytes": available}
        if storage == "external":
            item["uri"] = buf["uri"]
        resources["buffers"].append(item)
    for i, view in enumerate(views):
        buf = reference(buffers, view["buffer"], f"bufferView {i} buffer")
        start = integer(view.get("byteOffset", 0), f"bufferView {i} byteOffset")
        size = integer(view["byteLength"], f"bufferView {i} byteLength", 1)
        require(start + size <= buf["byteLength"], f"bufferView {i} exceeds declared buffer bounds")
    for i, img in enumerate(doc.get("images", [])):
        require(("uri" in img) != ("bufferView" in img), f"image {i} needs exactly one URI or bufferView")
        if "uri" in img:
            storage = uri_storage(img["uri"])
        else:
            view = reference(views, img["bufferView"], f"image {i} bufferView")
            require(isinstance(img.get("mimeType"), str), f"image {i} bufferView needs mimeType")
            storage = resources["buffers"][view["buffer"]]["storage"]
        item = {"index": i, "storage": storage, "mime_type": img.get("mimeType")}
        if "bufferView" in img:
            item["buffer_view"] = img["bufferView"]
        elif storage == "external":
            item["uri"] = img["uri"]
        resources["images"].append(item)
    for kind, entries in resources.items():
        for entry in entries:
            if entry["storage"] in ("external", "unresolved"):
                message = f"{kind}[{entry['index']}]: {entry['storage']} resource not inspected"
                (errors if self_contained else warnings).append(message)

    accessors, meshes, nodes = (doc.get(key, []) for key in ("accessors", "meshes", "nodes"))
    mesh_triangles, bounds, modes = [], {}, Counter()
    unknown_triangles = 0
    for mesh in meshes:
        total = 0
        for primitive in mesh["primitives"]:
            mode = integer(primitive.get("mode", 4), "primitive mode")
            require(mode <= 6, "primitive mode out of range")
            modes[str(mode)] += 1
            attributes = primitive.get("attributes", {})
            if "POSITION" in attributes:
                index = attributes["POSITION"]
                pos = reference(accessors, index, "POSITION accessor")
                bounds[index] = {"accessor": index, "min": pos.get("min"), "max": pos.get("max")}
            index = primitive.get("indices", next(iter(attributes.values()), None))
            if index is None:
                unknown_triangles += int(mode in (4, 5, 6))
                continue
            accessor = reference(accessors, index, "primitive accessor")
            count = integer(accessor["count"], "primitive accessor count", 1)
            if mode == 4:
                require(count % 3 == 0, "TRIANGLES accessor count must be divisible by 3")
                total += count // 3
            elif mode in (5, 6):
                require(count >= 3, "triangle strip/fan needs at least 3 elements")
                total += count - 2
        mesh_triangles.append(total)
    instances = [reference(mesh_triangles, node["mesh"], "node mesh") for node in nodes if "mesh" in node]
    if unknown_triangles:
        warnings.append("Triangle totals omit primitives without a declared element count")
    if any("EXT_mesh_gpu_instancing" in node.get("extensions", {}) for node in nodes):
        warnings.append("EXT_mesh_gpu_instancing multiplicity is not expanded")

    materials, matched = [], set()
    for i, mat in enumerate(doc.get("materials", [])):
        extensions = mat.get("extensions", {})
        normal = mat.get("normalTexture")
        item = {"index": i, "name": mat.get("name"), "alpha_mode": mat.get("alphaMode", "OPAQUE"),
                "double_sided": mat.get("doubleSided", False),
                "base_color_alpha": mat.get("pbrMetallicRoughness", {}).get("baseColorFactor", [1, 1, 1, 1])[3],
                "transmission_factor": extensions.get("KHR_materials_transmission", {}).get("transmissionFactor", 0),
                "normal_scale": normal.get("scale", 1) if normal is not None else None,
                "extensions": extensions}
        materials.append(item)
        if item["name"] in opaque_names:
            matched.add(item["name"])
            failures = [label for label, fails in (
                ("alphaMode is not OPAQUE", item["alpha_mode"] != "OPAQUE"),
                ("doubleSided is enabled", item["double_sided"] is not False),
                ("base color alpha is not 1", type(item["base_color_alpha"]) not in (int, float) or item["base_color_alpha"] != 1),
                ("transmission is not 0", type(item["transmission_factor"]) not in (int, float) or item["transmission_factor"] != 0)) if fails]
            errors.extend(f"material {i} ({item['name']}): {failure}" for failure in failures)
    errors.extend(f"opaque material name not found: {name}" for name in sorted(set(opaque_names) - matched))
    components = {}
    for kind in ("nodes", "meshes"):
        values = [obj.get("extras", {}).get("component_type") for obj in doc.get(kind, [])
                  if isinstance(obj.get("extras", {}), dict)]
        components[kind] = dict(sorted(Counter(value for value in values if isinstance(value, str)).items()))
    position_bounds = {"space": "accessor-local; not transformed or decoded", "accessor_count": len(bounds)}
    if include_position_bounds:
        position_bounds["accessors"] = list(bounds.values())
    return {"errors": errors, "warnings": warnings, "resources": resources, "materials": materials,
            "extensions_used": doc.get("extensionsUsed", []), "extensions_required": doc.get("extensionsRequired", []),
            "counts": {"nodes": len(nodes), "meshes": len(meshes), "mesh_node_instances": len(instances),
                       "triangles_unique_meshes": sum(mesh_triangles), "triangles_node_instances": sum(instances),
                       "triangle_primitives_unaccounted": unknown_triangles, "primitive_modes": dict(modes),
                       "buffer_views": len(views), "accessors": len(accessors)},
            "component_type_counts": components,
            "declared_position_bounds": position_bounds}


def inspect_file(path, self_contained=False, opaque_names=(), include_position_bounds=False):
    report = {"file": str(path), "ok": False, "scope": "limited artifact inspection; not full glTF validation",
              "contracts": {"self_contained": self_contained, "opaque_materials": sorted(set(opaque_names))},
              "errors": [], "warnings": []}
    try:
        data = Path(path).read_bytes()
        report.update(byte_length=len(data), sha256=hashlib.sha256(data).hexdigest())
        doc, binary, chunks = parse_glb(data)
        report["chunks"] = chunks
        report.update(inspect_document(doc, binary, self_contained, opaque_names, include_position_bounds))
        report["ok"] = not report["errors"]
    except (OSError, ValueError, KeyError, TypeError, IndexError, AttributeError) as exc:
        report["errors"].append(f"{type(exc).__name__}: {exc}")
    return report


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file", type=Path)
    parser.add_argument("--output", type=Path, help="also write the JSON report to this path")
    parser.add_argument("--self-contained", action="store_true", help="fail on external or unresolved core resources")
    parser.add_argument("--include-position-bounds", action="store_true",
                        help="include each POSITION accessor's declared local min/max values")
    parser.add_argument("--opaque-material", action="append", default=[], metavar="NAME",
                        help="require this exact material name to be opaque, single-sided, alpha 1, no transmission; repeatable")
    args = parser.parse_args(argv)
    report = inspect_file(args.file, args.self_contained, args.opaque_material, args.include_position_bounds)
    if args.output:
        try:
            require(args.output.resolve() != args.file.resolve(), "report output must differ from input")
            require(not (args.output.exists() and args.file.exists() and args.output.samefile(args.file)),
                    "report output must not be a hard link to input")
            args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        except (OSError, ValueError) as exc:
            report["errors"].append(f"report output: {exc}")
            report["ok"] = False
    print(json.dumps(report, indent=2))
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
