import importlib.util
import json
import math
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts/check_orbit.py'
spec = importlib.util.spec_from_file_location('check_orbit', SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def frames(angles):
    pitch = [math.cos(.4), math.sin(.4), 0, 0]
    return [{'q': module.multiply([math.cos(math.radians(a)/2), 0, 0,
                                  math.sin(math.radians(a)/2)], pitch)} for a in angles]


class OrbitTests(unittest.TestCase):
    def test_full_turn_both_directions_and_quaternion_signs(self):
        for direction in [-1, 1]:
            f = frames([i*15*direction for i in range(25)])
            for frame in f[::2]:
                frame['q'] = [-2*x for x in frame['q']]
            report = module.inspect(f)
            self.assertTrue(report['pass'], report)
            self.assertAlmostEqual(abs(report['signed_total_degrees']), 360)

    def test_stationary_closed_sequence_fails(self):
        self.assertFalse(module.inspect(frames([0]*25))['pass'])

    def test_back_and_forth_with_360_absolute_degrees_fails(self):
        self.assertFalse(module.inspect(frames([0, 30]*6+[0]))['pass'])

    def test_two_turns_fail(self):
        self.assertFalse(module.inspect(frames(range(0, 721, 30)))['pass'])

    def test_incomplete_or_sparse_turn_fails(self):
        self.assertFalse(module.inspect(frames(range(0, 331, 30)))['pass'])
        self.assertFalse(module.inspect(frames(range(0, 361, 90)))['pass'])

    def test_wrong_axis_and_zero_quaternion(self):
        self.assertFalse(module.inspect(frames(range(0, 361, 30)), axis=(1, 0, 0))['pass'])
        with self.assertRaises(ValueError):
            module.inspect([{'q': [0, 0, 0, 0]}]*3)

    def test_screenshot_paths_and_identical_bytes(self):
        f = frames(range(0, 361, 30))
        with tempfile.TemporaryDirectory() as d:
            for i, frame in enumerate(f):
                frame['screenshot'] = f'{i}.png'
                (Path(d)/frame['screenshot']).write_bytes(str(i).encode())
            self.assertTrue(module.inspect(f, asset_root=d)['pass'])
            for frame in f:
                (Path(d)/frame['screenshot']).write_bytes(b'same')
            self.assertFalse(module.inspect(f, asset_root=d)['pass'])
            f[0]['screenshot'] = '../outside.png'
            self.assertFalse(module.inspect(f, asset_root=d)['pass'])

    def test_cli_machine_readable_failure(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d)/'frames.json'
            path.write_text(json.dumps(frames([0, 0, 0])))
            result = subprocess.run([sys.executable, str(SCRIPT), str(path)],
                                    capture_output=True, text=True)
            self.assertEqual(result.returncode, 1)
            self.assertFalse(json.loads(result.stdout)['pass'])


if __name__ == '__main__':
    unittest.main()
