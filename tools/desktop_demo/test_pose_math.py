"""Unit tests for the desktop demo's plugin-free geometry."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from pose_math import Point, calculate_elbow_angle, has_reliable_point, make_angle_result


class PoseMathTests(unittest.TestCase):
    def test_right_angle_is_calculated(self) -> None:
        angle = calculate_elbow_angle(
            Point(0, 1),
            Point(0, 0),
            Point(1, 0),
        )

        self.assertIsNotNone(angle)
        self.assertAlmostEqual(angle, 90.0)

    def test_straight_angle_is_calculated(self) -> None:
        angle = calculate_elbow_angle(
            Point(-1, 0),
            Point(0, 0),
            Point(1, 0),
        )

        self.assertIsNotNone(angle)
        self.assertAlmostEqual(angle, 180.0)

    def test_degenerate_geometry_is_rejected(self) -> None:
        self.assertIsNone(
            calculate_elbow_angle(Point(0, 0), Point(0, 0), Point(1, 0))
        )

    def test_visibility_gate_is_inclusive(self) -> None:
        self.assertTrue(has_reliable_point(Point(0.5, 0.5, 0.55), 0.55))
        self.assertFalse(has_reliable_point(Point(0.5, 0.5, 0.54), 0.55))

    def test_demo_range_is_inclusive(self) -> None:
        self.assertTrue(make_angle_result(90.0, 90.0, 105.0).in_demo_range)
        self.assertTrue(make_angle_result(105.0, 90.0, 105.0).in_demo_range)
        self.assertFalse(make_angle_result(105.1, 90.0, 105.0).in_demo_range)


if __name__ == "__main__":
    unittest.main()
