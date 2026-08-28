"""Regression suite over the authorized reference serve photos.

The expectations in ``reference_expectations.json`` were established by
inspecting each photo, so this suite is what stops a tuning change from quietly
regressing accuracy. It skips when the photos or the model are unavailable.
"""

from __future__ import annotations

import json
import os
import unittest
from pathlib import Path

import numpy as np
from PIL import Image, ImageOps

from tennispose.pose_detector import DEFAULT_MODEL_PATH, analyze_rgb_image


EXPECTATIONS = json.loads(
    (Path(__file__).parent / "reference_expectations.json").read_text(encoding="utf-8")
)
SAMPLE_DIR = Path(
    os.environ.get(
        "TENNISPOSE_SAMPLE_DIR",
        Path.home() / "Desktop" / "TennisPose_Test_Images" / "normal_use_samples",
    )
)


def load_photo(path: Path) -> np.ndarray:
    with Image.open(path) as image:
        return np.asarray(ImageOps.exif_transpose(image).convert("RGB"))


@unittest.skipUnless(DEFAULT_MODEL_PATH.is_file(), "pose model not downloaded")
@unittest.skipUnless(SAMPLE_DIR.is_dir(), f"reference photos not found at {SAMPLE_DIR}")
class ReferencePhotoTests(unittest.TestCase):
    def test_every_reference_photo_matches_its_verified_expectation(self) -> None:
        tolerance = EXPECTATIONS["tolerance"]
        for case in EXPECTATIONS["cases"]:
            path = SAMPLE_DIR / case["file"]
            with self.subTest(photo=case["file"], shows=case["pose"]):
                if not path.is_file():
                    self.skipTest(f"{path} is not available")

                _, report = analyze_rgb_image(
                    load_photo(path),
                    EXPECTATIONS["arm"],
                    demo_minimum=EXPECTATIONS["trophy_minimum"],
                    demo_maximum=EXPECTATIONS["trophy_maximum"],
                )

                self.assertEqual(report.status, case["status"])
                if case["status"] == "cannot_analyze":
                    self.assertEqual(report.reason_code, case["reason_code"])
                    self.assertIsNone(report.angle_degrees)
                    continue

                self.assertEqual(report.arm, case["arm"])
                self.assertEqual(report.in_demo_range, case["in_demo_range"])
                self.assertAlmostEqual(
                    report.angle_degrees,
                    case["angle_degrees"],
                    delta=tolerance,
                    msg=f"{case['file']} elbow angle drifted beyond {tolerance} degrees",
                )

    def test_every_elite_trophy_photo_passes(self) -> None:
        """The four genuine trophy positions are the demo's green examples."""

        green = [case for case in EXPECTATIONS["cases"] if case.get("in_demo_range")]
        self.assertEqual(len(green), 4)
        for case in green:
            path = SAMPLE_DIR / case["file"]
            with self.subTest(photo=case["file"]):
                if not path.is_file():
                    self.skipTest(f"{path} is not available")
                _, report = analyze_rgb_image(load_photo(path), "auto")
                self.assertTrue(report.in_demo_range)


if __name__ == "__main__":
    unittest.main()
