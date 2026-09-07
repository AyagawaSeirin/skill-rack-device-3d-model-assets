"""Synthetic GLB fixtures; no renderer or third-party modules required."""

import hashlib
import importlib.util
import json
from pathlib import Path
import struct
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "inspect_glb.py"
SPEC = importlib.util.spec_from_file_location("inspect_glb", SCRIPT)
INSPECT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(INSPECT)


def chunk(kind, payload, padding=b" "):
    payload += padding * (-len(payload) % 4)
    return struct.pack("<II", len(payload), kind) + payload


def glb(document, binary=None, extra=b""):
    body = chunk(INSPECT.JSON_CHUNK, json.dumps(document).encode())
    if binary is not None:
        body += chunk(INSPECT.BIN_CHUNK, binary, b"\0")
    body += extra
    return struct.pack("<4sII", b"glTF", 2, len(body) + 12) + body


def model():
    return {"asset": {"version": "2.0"}, "buffers": [{"byteLength": 36}],
            "bufferViews": [{"buffer": 0, "byteLength": 36}],
            "accessors": [{"bufferView": 0, "componentType": 5126, "type": "VEC3", "count": 3,
                           "min": [0, 0, 0], "max": [1, 1, 0]}],
            "meshes": [{"primitives": [{"attributes": {"POSITION": 0}}]}],
            "nodes": [{"mesh": 0, "extras": {"component_type": "port"}}, {"mesh": 0}],
            "materials": [{"name": "metal"}, {"name": "lens", "alphaMode": "BLEND",
                                                "pbrMetallicRoughness": {"baseColorFactor": [1, 1, 1, 0.5]}}]}


class InspectorTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.path = Path(self.directory.name) / "fixture.glb"

    def inspect(self, payload, **kwargs):
        self.path.write_bytes(payload)
        return INSPECT.inspect_file(self.path, **kwargs)

    def test_counts_defaults_hash_and_transparent_material_allowed(self):
        payload = glb(model(), bytes(36))
        report = self.inspect(payload, self_contained=True, opaque_names=["metal"])
        self.assertTrue(report["ok"], report)
        self.assertEqual(report["sha256"], hashlib.sha256(payload).hexdigest())
        self.assertEqual(report["counts"]["triangles_unique_meshes"], 1)
        self.assertEqual(report["counts"]["triangles_node_instances"], 2)
        self.assertEqual(report["component_type_counts"]["nodes"], {"port": 1})
        self.assertEqual(report["materials"][0]["alpha_mode"], "OPAQUE")
        self.assertEqual(report["materials"][1]["base_color_alpha"], 0.5)
        self.assertEqual(report["declared_position_bounds"]["accessor_count"], 1)
        self.assertIn("accessor-local", report["declared_position_bounds"]["space"])
        self.assertNotIn("accessors", report["declared_position_bounds"])

    def test_include_position_bounds(self):
        report = self.inspect(glb(model(), bytes(36)), include_position_bounds=True)
        self.assertTrue(report["ok"], report)
        bounds = report["declared_position_bounds"]
        self.assertEqual(bounds["accessor_count"], 1)
        self.assertEqual(bounds["accessors"], [{"accessor": 0, "min": [0, 0, 0], "max": [1, 1, 0]}])

    def test_real_truncations_and_chunk_bounds(self):
        valid = glb(model(), bytes(36))
        bad_chunk = bytearray(valid)
        struct.pack_into("<I", bad_chunk, 12, len(valid))
        trailing = bytearray(valid + b"xx")
        struct.pack_into("<I", trailing, 8, len(trailing))
        for payload, expected in ((b"glTF", "truncated GLB header"),
                                  (valid[:-1], "declared length"),
                                  (bad_chunk, "chunk payload exceeds"),
                                  (trailing, "truncated chunk header")):
            with self.subTest(expected=expected):
                report = self.inspect(payload)
                self.assertFalse(report["ok"])
                self.assertIn(expected, report["errors"][0])

    def test_alignment_order_duplicates_and_unknown_chunks(self):
        empty = {"asset": {"version": "2.0"}}
        valid = glb(empty, extra=chunk(0x12345678, b"abcd"))
        self.assertTrue(self.inspect(valid)["ok"])
        duplicate = glb(empty, extra=chunk(INSPECT.JSON_CHUNK, b"{}"))
        self.assertIn("duplicate", self.inspect(duplicate)["errors"][0])
        late_bin = glb(empty, extra=chunk(123, b"abcd") + chunk(INSPECT.BIN_CHUNK, b"abcd"))
        self.assertIn("second chunk", self.inspect(late_bin)["errors"][0])
        unaligned = bytearray(glb(empty))
        size = struct.unpack_from("<I", unaligned, 12)[0]
        struct.pack_into("<I", unaligned, 12, size - 1)
        self.assertIn("aligned", self.inspect(unaligned)["errors"][0])

    def test_required_bin_and_buffer_overflow(self):
        self.assertIn("missing BIN", self.inspect(glb(model()))["errors"][0])
        self.assertIn("exceeds BIN", self.inspect(glb(model(), bytes(32)))["errors"][0])
        doc = model()
        doc["bufferViews"][0]["byteOffset"] = 4
        self.assertIn("bufferView 0 exceeds", self.inspect(glb(doc, bytes(36)))["errors"][0])

    def test_bin_padding(self):
        for size in (1, 2, 3, 4):
            doc = {"asset": {"version": "2.0"}, "buffers": [{"byteLength": size}]}
            self.assertTrue(self.inspect(glb(doc, bytes(size)))["ok"])
        doc["buffers"][0]["byteLength"] = 1
        self.assertIn("padding exceeds", self.inspect(glb(doc, bytes(8)))["errors"][0])
        self.assertIn("padding must be zero", self.inspect(glb(doc, b"aXXX"))["errors"][0])

    def test_external_buffers_and_images_fail_only_self_contained_contract(self):
        doc = model()
        doc["buffers"][0]["uri"] = "never-read.bin"
        doc["images"] = [{"uri": "never-read.png"}, {"bufferView": 0, "mimeType": "image/png"}]
        payload = glb(doc)
        report = self.inspect(payload)
        self.assertTrue(report["ok"])
        self.assertEqual(len(report["warnings"]), 3)
        report = self.inspect(payload, self_contained=True)
        self.assertFalse(report["ok"])
        self.assertEqual(len(report["errors"]), 3)

    def test_data_uri_buffer_bounds_and_embedded_image(self):
        doc = {"asset": {"version": "2.0"}, "buffers": [{"byteLength": 3, "uri": "data:application/octet-stream;base64,YWJj"}],
               "images": [{"uri": "data:image/png;base64,YWJj"}]}
        self.assertTrue(self.inspect(glb(doc), self_contained=True)["ok"])
        doc["buffers"][0]["byteLength"] = 4
        self.assertIn("exceeds embedded", self.inspect(glb(doc))["errors"][0])

    def test_opaque_contract_each_failure_and_missing_name(self):
        failures = [{"alphaMode": "BLEND"}, {"doubleSided": True},
                    {"pbrMetallicRoughness": {"baseColorFactor": [1, 1, 1, 0.9]}},
                    { "extensions": {"KHR_materials_transmission": {"transmissionFactor": 0.1}}},
                    {"pbrMetallicRoughness": {"baseColorFactor": [1, 1, 1, 1.1]}},
                    {"extensions": {"KHR_materials_transmission": {"transmissionFactor": -0.1}}}]
        for change in failures:
            doc = model()
            doc["materials"][0].update(change)
            with self.subTest(change=change):
                self.assertTrue(self.inspect(glb(doc, bytes(36)))["ok"])
                report = self.inspect(glb(doc, bytes(36)), opaque_names=["metal"])
                self.assertFalse(report["ok"])
                self.assertEqual(len(report["errors"]), 1)
        report = self.inspect(glb(model(), bytes(36)), opaque_names=["typo"])
        self.assertIn("name not found", report["errors"][0])

    def test_strip_fan_and_indexed_counts(self):
        doc = model()
        doc["accessors"].append({"count": 6, "componentType": 5123, "type": "SCALAR"})
        primitive = doc["meshes"][0]["primitives"][0]
        primitive["indices"] = 1
        for mode, triangles in ((4, 2), (5, 4), (6, 4), (1, 0)):
            primitive["mode"] = mode
            report = self.inspect(glb(doc, bytes(36)))
            self.assertTrue(report["ok"], report)
            self.assertEqual(report["counts"]["triangles_unique_meshes"], triangles)

    def test_json_failure_and_negative_reference(self):
        malformed = chunk(INSPECT.JSON_CHUNK, b"not json")
        payload = struct.pack("<4sII", b"glTF", 2, 12 + len(malformed)) + malformed
        self.assertIn("JSONDecodeError", self.inspect(payload)["errors"][0])
        payload = glb({"asset": {"version": "2.0"}}).replace(b'"2.0"', b'"xxx"')
        self.assertFalse(self.inspect(payload)["ok"])
        doc = model()
        doc["nodes"][0]["mesh"] = -1
        self.assertIn("invalid integer", self.inspect(glb(doc, bytes(36)))["errors"][0])

    def test_numeric_overflow_stays_machine_readable_failure(self):
        payload = glb({"asset": {"version": "2.0"}, "extras": {"value": "overflow"}})
        payload = payload.replace(b'"overflow"', b'1e999     ')
        report = self.inspect(payload)
        self.assertFalse(report["ok"])
        self.assertIn("non-finite", report["errors"][0])
        json.dumps(report, allow_nan=False)

    def test_cli_json_report_exit_status_and_input_protection(self):
        payload = glb(model(), bytes(36))
        self.path.write_bytes(payload)
        output = self.path.with_suffix(".json")
        command = [sys.executable, str(SCRIPT), str(self.path), "--self-contained", "--opaque-material", "metal"]
        result = subprocess.run(command + ["--output", str(output)], text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout), json.loads(output.read_text()))
        self.assertNotIn("accessors", json.loads(result.stdout)["declared_position_bounds"])
        result = subprocess.run(command + ["--include-position-bounds"], text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(len(json.loads(result.stdout)["declared_position_bounds"]["accessors"]), 1)
        result = subprocess.run(command + ["--opaque-material", "missing"], text=True, capture_output=True)
        self.assertEqual(result.returncode, 1)
        self.assertFalse(json.loads(result.stdout)["ok"])
        for protected in (self.path, self.path.with_suffix(".hardlink")):
            if protected != self.path:
                protected.hardlink_to(self.path)
            result = subprocess.run(command + ["--output", str(protected)], text=True, capture_output=True)
            self.assertEqual(result.returncode, 1)
            self.assertEqual(self.path.read_bytes(), payload)


if __name__ == "__main__":
    unittest.main()
