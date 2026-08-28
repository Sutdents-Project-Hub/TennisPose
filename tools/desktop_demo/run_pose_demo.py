#!/usr/bin/env python3
"""OpenCV desktop runner for a single tennis Trophy Pose image.

This is a local developer/demo tool. It uses MediaPipe for a fast visual
prototype and does not replace the Flutter app's Android/iOS ML Kit path.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

LOCAL_CACHE_DIRECTORY = Path(__file__).with_name(".cache")
LOCAL_CACHE_DIRECTORY.mkdir(parents=True, exist_ok=True)
os.environ.setdefault("MPLCONFIGDIR", str(LOCAL_CACHE_DIRECTORY / "matplotlib"))
os.environ.setdefault("XDG_CACHE_HOME", str(LOCAL_CACHE_DIRECTORY))
os.environ.setdefault("GLOG_minloglevel", "2")

import cv2
import mediapipe as mp

from pose_math import Point, calculate_elbow_angle, has_reliable_point, make_angle_result


GREEN = (39, 174, 96)
RED = (55, 76, 232)
AMBER = (0, 165, 255)
NAVY = (31, 41, 55)
WHITE = (255, 255, 255)
POSE_CONNECTIONS = (
    (0, 1), (0, 4), (1, 2), (2, 3), (3, 7), (0, 5), (5, 6), (6, 8),
    (9, 10), (11, 12), (11, 13), (13, 15), (15, 17), (15, 19), (15, 21),
    (17, 19), (12, 14), (14, 16), (16, 18), (16, 20), (16, 22), (18, 20),
    (11, 23), (12, 24), (23, 24), (23, 25), (24, 26), (25, 27), (26, 28),
    (27, 29), (28, 30), (29, 31), (30, 32), (27, 31), (28, 32),
)
DEFAULT_MODEL_PATH = Path(__file__).with_name("models") / "pose_landmarker_heavy.task"


@dataclass(frozen=True)
class AnalysisReport:
    status: str
    arm: str
    angle_degrees: float | None
    in_demo_range: bool | None
    message: str
    output_path: str | None


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Analyze one tennis Trophy Pose photo with a local OpenCV window."
    )
    parser.add_argument("--image", required=True, type=Path, help="Path to a JPEG or PNG image.")
    parser.add_argument(
        "--arm",
        choices=("left", "right"),
        default="right",
        help="Arm to evaluate in the photo (default: right).",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Optional path for the annotated JPEG or PNG result.",
    )
    parser.add_argument(
        "--model",
        type=Path,
        default=DEFAULT_MODEL_PATH,
        help="Path to the local MediaPipe pose-landmarker task model.",
    )
    parser.add_argument(
        "--no-display",
        action="store_true",
        help="Save or print the result without opening an OpenCV window.",
    )
    parser.add_argument(
        "--minimum-visibility",
        type=float,
        default=0.55,
        help="Landmark visibility required before an angle is shown (default: 0.55).",
    )
    parser.add_argument(
        "--demo-minimum",
        type=float,
        default=90.0,
        help="Inclusive lower angle bound for green feedback (default: 90).",
    )
    parser.add_argument(
        "--demo-maximum",
        type=float,
        default=105.0,
        help="Inclusive upper angle bound for green feedback (default: 105).",
    )
    parser.add_argument(
        "--print-json",
        action="store_true",
        help="Print one machine-readable result line after processing.",
    )
    return parser.parse_args()


def normalized_point(landmark: object) -> Point:
    return Point(
        x=float(landmark.x),
        y=float(landmark.y),
        visibility=float(getattr(landmark, "visibility", 0.0)),
    )


def pixel_point(point: Point, width: int, height: int) -> tuple[int, int]:
    return (round(point.x * width), round(point.y * height))


def draw_text_banner(image: object, lines: list[str], color: tuple[int, int, int]) -> None:
    line_height = 32
    padding = 16
    banner_height = padding * 2 + line_height * len(lines)
    cv2.rectangle(image, (0, 0), (image.shape[1], banner_height), NAVY, -1)
    for index, line in enumerate(lines):
        origin = (padding, padding + 22 + index * line_height)
        cv2.putText(image, line, origin, cv2.FONT_HERSHEY_DUPLEX, 0.72, WHITE, 1, cv2.LINE_AA)
    cv2.rectangle(image, (0, banner_height - 6), (image.shape[1], banner_height), color, -1)


def draw_selected_arm(
    image: object,
    shoulder: Point,
    elbow: Point,
    wrist: Point,
    color: tuple[int, int, int],
) -> None:
    height, width = image.shape[:2]
    points = [
        pixel_point(shoulder, width, height),
        pixel_point(elbow, width, height),
        pixel_point(wrist, width, height),
    ]
    cv2.line(image, points[0], points[1], color, 6, cv2.LINE_AA)
    cv2.line(image, points[1], points[2], color, 6, cv2.LINE_AA)
    for point in points:
        cv2.circle(image, point, 9, WHITE, -1, cv2.LINE_AA)
        cv2.circle(image, point, 11, color, 3, cv2.LINE_AA)


def landmark_indices(arm: str) -> tuple[int, int, int]:
    if arm == "left":
        return (11, 13, 15)
    return (12, 14, 16)


def draw_pose_skeleton(image: object, landmarks: list[object]) -> None:
    """Draw a lightweight full-body guide from the current Tasks API output."""

    height, width = image.shape[:2]
    for start, end in POSE_CONNECTIONS:
        start_landmark = normalized_point(landmarks[start])
        end_landmark = normalized_point(landmarks[end])
        if has_reliable_point(start_landmark, 0.2) and has_reliable_point(end_landmark, 0.2):
            cv2.line(
                image,
                pixel_point(start_landmark, width, height),
                pixel_point(end_landmark, width, height),
                (178, 178, 178),
                2,
                cv2.LINE_AA,
            )
    for landmark in landmarks:
        point = normalized_point(landmark)
        if has_reliable_point(point, 0.2):
            cv2.circle(image, pixel_point(point, width, height), 3, WHITE, -1, cv2.LINE_AA)


def analyze_image(
    image: object,
    arm: str,
    minimum_visibility: float,
    demo_minimum: float,
    demo_maximum: float,
    model_path: Path,
) -> tuple[object, AnalysisReport]:
    annotated = image.copy()
    vision = mp.tasks.vision
    options = vision.PoseLandmarkerOptions(
        base_options=mp.tasks.BaseOptions(
            model_asset_path=str(model_path),
            delegate=mp.tasks.BaseOptions.Delegate.CPU,
        ),
        running_mode=vision.RunningMode.IMAGE,
        num_poses=1,
        min_pose_detection_confidence=0.5,
        min_pose_presence_confidence=0.5,
        min_tracking_confidence=0.5,
    )
    input_image = mp.Image(
        image_format=mp.ImageFormat.SRGB,
        data=cv2.cvtColor(image, cv2.COLOR_BGR2RGB),
    )

    with vision.PoseLandmarker.create_from_options(options) as detector:
        result = detector.detect(input_image)

    if not result.pose_landmarks:
        draw_text_banner(
            annotated,
            ["TennisPose Desktop Demo", "Cannot analyze: no pose was detected."],
            AMBER,
        )
        return annotated, AnalysisReport(
            status="cannot_analyze",
            arm=arm,
            angle_degrees=None,
            in_demo_range=None,
            message="No pose was detected in this image.",
            output_path=None,
        )

    landmark_values = result.pose_landmarks[0]
    draw_pose_skeleton(annotated, landmark_values)
    selected = tuple(
        normalized_point(landmark_values[index])
        for index in landmark_indices(arm)
    )

    if not all(has_reliable_point(point, minimum_visibility) for point in selected):
        draw_text_banner(
            annotated,
            [
                "TennisPose Desktop Demo",
                f"Cannot analyze: selected {arm} arm landmarks are unreliable.",
            ],
            AMBER,
        )
        return annotated, AnalysisReport(
            status="cannot_analyze",
            arm=arm,
            angle_degrees=None,
            in_demo_range=None,
            message="Selected arm landmarks did not meet the visibility threshold.",
            output_path=None,
        )

    angle = calculate_elbow_angle(*selected)
    if angle is None:
        draw_text_banner(
            annotated,
            ["TennisPose Desktop Demo", "Cannot analyze: elbow geometry is degenerate."],
            AMBER,
        )
        return annotated, AnalysisReport(
            status="cannot_analyze",
            arm=arm,
            angle_degrees=None,
            in_demo_range=None,
            message="The selected elbow geometry was invalid.",
            output_path=None,
        )

    angle_result = make_angle_result(angle, demo_minimum, demo_maximum)
    color = GREEN if angle_result.in_demo_range else RED
    feedback = "IN DEMO RANGE" if angle_result.in_demo_range else "ADJUSTMENT SUGGESTED"
    draw_selected_arm(annotated, *selected, color)
    draw_text_banner(
        annotated,
        [
            "TennisPose Desktop Demo",
            f"{arm.upper()} elbow: {angle_result.degrees:.1f} deg | {feedback}",
            f"Demo range: {demo_minimum:.0f}-{demo_maximum:.0f} deg",
        ],
        color,
    )
    return annotated, AnalysisReport(
        status="analyzed",
        arm=arm,
        angle_degrees=round(angle_result.degrees, 1),
        in_demo_range=angle_result.in_demo_range,
        message=feedback.lower().replace("_", " "),
        output_path=None,
    )


def display_image(image: object) -> None:
    max_height = 900
    height, width = image.shape[:2]
    if height > max_height:
        ratio = max_height / height
        image = cv2.resize(image, (round(width * ratio), max_height))
    cv2.imshow("TennisPose Desktop Demo", image)
    print("OpenCV preview shown. Press any key, Escape, or q to close it.")
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def main() -> int:
    arguments = parse_arguments()
    if not 0 <= arguments.minimum_visibility <= 1:
        print("--minimum-visibility must be between 0 and 1.", file=sys.stderr)
        return 2
    if arguments.demo_minimum > arguments.demo_maximum:
        print("--demo-minimum cannot be greater than --demo-maximum.", file=sys.stderr)
        return 2
    if not arguments.model.is_file():
        print(
            f"Cannot find MediaPipe model: {arguments.model}. "
            "See tools/desktop_demo/README.md for the download command.",
            file=sys.stderr,
        )
        return 2

    image = cv2.imread(str(arguments.image))
    if image is None:
        print(f"Cannot read image: {arguments.image}", file=sys.stderr)
        return 2

    annotated, report = analyze_image(
        image,
        arguments.arm,
        arguments.minimum_visibility,
        arguments.demo_minimum,
        arguments.demo_maximum,
        arguments.model,
    )
    output_path: str | None = None
    if arguments.output:
        arguments.output.parent.mkdir(parents=True, exist_ok=True)
        if not cv2.imwrite(str(arguments.output), annotated):
            print(f"Could not write annotated image: {arguments.output}", file=sys.stderr)
            return 2
        output_path = str(arguments.output.resolve())

    report = AnalysisReport(**{**asdict(report), "output_path": output_path})
    status_line = report.message if report.angle_degrees is None else (
        f"{report.angle_degrees:.1f} deg — {report.message}"
    )
    print(f"{report.status}: {status_line}")
    if arguments.print_json:
        print(json.dumps(asdict(report), ensure_ascii=False))
    if not arguments.no_display:
        display_image(annotated)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
