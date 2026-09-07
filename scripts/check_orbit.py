#!/usr/bin/env python3
"""Read-only check of recorded fixed-axis, single-turn viewport quaternions.

Input: a JSON frame list or {"frames": [...]}, q=[w,x,y,z]. This validates
recorded math, not desktop-tool provenance, picture content, or actual input.
Only fixed-pitch monotonic one-turn paths are supported; no arbitrary orbit.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
import sys


def unit(values, length):
    if not isinstance(values, (list, tuple)) or len(values) != length:
        raise ValueError(f'Expected {length} numeric components')
    if any(isinstance(x, bool) or not isinstance(x, (float, int)) for x in values):
        raise ValueError('Components must be numbers')
    if not all(math.isfinite(x) for x in values):
        raise ValueError('Non-finite component')
    norm = math.hypot(*values)
    if norm < 1e-12:
        raise ValueError('Zero-length vector/quaternion')
    return [x / norm for x in values]


def multiply(a, b):
    w, x, y, z = a
    v, i, j, k = b
    return [w*v-x*i-y*j-z*k, w*i+x*v+y*k-z*j,
            w*j-x*k+y*v+z*i, w*k+x*j-y*i+z*v]


def angle(a, b):
    dot = sum(x*y for x, y in zip(a, b))
    return math.degrees(2*math.acos(min(1.0, abs(dot))))


def inspect(frames, axis=(0, 0, 1), tolerance=1.0, max_step=45.0, asset_root=None):
    if isinstance(frames, dict):
        frames = frames.get('frames')
    if not isinstance(frames, list) or len(frames) < 3:
        raise ValueError('At least three ordered frames required')
    if not (math.isfinite(tolerance) and 0 < tolerance < 10):
        raise ValueError('Tolerance must be finite and between 0 and 10 degrees')
    if not (math.isfinite(max_step) and 0 < max_step < 180):
        raise ValueError('Maximum step must be finite and between 0 and 180 degrees')
    axis = unit(axis, 3)
    quats = [unit(f.get('q'), 4) if isinstance(f, dict) else unit(None, 4) for f in frames]
    errors, steps, hashes = [], [], []
    for index, (previous, current) in enumerate(zip(quats, quats[1:]), 1):
        # Sign equivalence avoids false360degree jumps from q -> -q.
        delta = multiply(current, [previous[0], *[-x for x in previous[1:]]])
        if delta[0] < 0:
            delta = [-x for x in delta]
        vector_length = math.hypot(*delta[1:])
        degrees = math.degrees(2*math.atan2(vector_length, max(0, delta[0])))
        if degrees < 1e-4:
            errors.append(f'Frame {index}: stalled orientation')
            signed, deviation = 0.0, None
        else:
            alignment = sum(delta[i+1]*axis[i] for i in range(3)) / vector_length
            deviation = math.degrees(math.acos(min(1.0, abs(alignment))))
            signed = math.copysign(degrees, alignment)
            if deviation > tolerance:
                errors.append(f'Frame {index}: changed rotation axis')
            if degrees > max_step + tolerance:
                errors.append(f'Frame {index}: angular gap exceeds maximum step')
        steps.append({'index': index, 'degrees': degrees, 'signed_degrees': signed,
                      'axis_deviation_degrees': deviation})
    total = sum(s['signed_degrees'] for s in steps)
    closure = angle(quats[0], quats[-1])
    signs = {1 if s['signed_degrees'] > 0 else -1 for s in steps if s['degrees'] >= 1e-4}
    if len(signs) != 1:
        errors.append('Rotation reverses direction or never progresses')
    if abs(abs(total) - 360) > tolerance:
        errors.append('Recorded path is not exactly one full turn')
    if closure > tolerance:
        errors.append('First and last orientations do not close')
    if asset_root is not None:
        root = Path(asset_root).resolve()
        for index, frame in enumerate(frames):
            name = frame.get('screenshot')
            if not isinstance(name, str) or not name or Path(name).is_absolute():
                errors.append(f'Frame {index}: missing relative screenshot path')
                continue
            path = (root / name).resolve()
            if not path.is_relative_to(root):
                errors.append(f'Frame {index}: screenshot escapes asset root')
                continue
            if not path.is_file() or path.stat().st_size == 0:
                errors.append(f'Frame {index}: screenshot missing or empty')
                continue
            hashes.append(hashlib.sha256(path.read_bytes()).hexdigest())
        if hashes and len(set(hashes)) == 1:
            errors.append('All supplied screenshot bytes are identical')
    return {'pass': not errors, 'frame_count': len(frames), 'axis': axis,
            'signed_total_degrees': total, 'closure_degrees': closure, 'steps': steps,
            'screenshot_files_checked': len(hashes), 'errors': errors,
            'limits': 'Recorded fixed-axis math only; no image decoding, visual acceptance, '
                      'timestamp validation, or proof of desktop-tool provenance.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('frames', type=Path)
    parser.add_argument('--axis', nargs=3, type=float, default=(0, 0, 1), metavar=('X', 'Y', 'Z'))
    parser.add_argument('--tolerance-degrees', type=float, default=1.0)
    parser.add_argument('--max-step-degrees', type=float, default=45.0)
    parser.add_argument('--asset-root', type=Path)
    args = parser.parse_args()
    try:
        report = inspect(json.loads(args.frames.read_text()), args.axis,
                         args.tolerance_degrees, args.max_step_degrees, args.asset_root)
    except (OSError, ValueError, TypeError, OverflowError) as exc:
        report = {'pass': False, 'errors': [str(exc)]}
    print(json.dumps(report, ensure_ascii=False, indent=2, allow_nan=False))
    return 0 if report['pass'] else 1


if __name__ == '__main__':
    sys.exit(main())
