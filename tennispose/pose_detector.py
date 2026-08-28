"""Local MediaPipe pose inference, arm selection, and annotation for one photo.

The pipeline is deliberately explicit so every number shown to a user can be
traced back to a landmark:

1. run the pose model over a few cheap variants of the same photo;
2. reject arms the model could not actually see;
3. reject photos that are not a serve preparation at all;
4. pool the surviving 3D elbow angles into one median with a spread; and
5. only then apply the configurable green/red demonstration range.
"""

from __future__ import annotations

import threading
from dataclasses import dataclass
from pathlib import Path
from typing import Literal, Sequence

import cv2
import mediapipe as mp
import numpy as np

from tennispose.annotate import (
    AMBER,
    GREEN,
    RED,
    draw_banner,
    draw_measured_arm,
    draw_skeleton,
)
from tennispose.pose_math import (
    DEFAULT_MINIMUM_VISIBILITY,
    DEFAULT_TROPHY_MAXIMUM,
    DEFAULT_TROPHY_MINIMUM,
    AngleResult,
    Arm,
    ArmGeometry,
    Point,
    Point3,
    arm_geometry,
    body_scale,
    calculate_elbow_angle,
    calculate_elbow_angle_3d,
    has_reliable_point,
    is_in_preparation_position,
    pool_angles,
)


DEFAULT_MODEL_PATH = (
    Path(__file__).resolve().parent.parent / "models" / "pose_landmarker_heavy.task"
)

# Kept as aliases so existing callers and docs that referenced the demo range
# continue to work after the trophy-position rename.
DEFAULT_DEMO_MINIMUM = DEFAULT_TROPHY_MINIMUM
DEFAULT_DEMO_MAXIMUM = DEFAULT_TROPHY_MAXIMUM

LEFT_ARM_INDICES = (11, 13, 15)
RIGHT_ARM_INDICES = (12, 14, 16)
LEFT_SHOULDER, RIGHT_SHOULDER = 11, 12
LEFT_HIP, RIGHT_HIP = 23, 24

# Landmark indices swap sides when the photo is mirrored for an extra pass.
_MIRRORED_INDEX = {11: 12, 12: 11, 13: 14, 14: 13, 15: 16, 16: 15, 23: 24, 24: 23}

ArmChoice = Literal["auto", "left", "right"]
Status = Literal["analyzed", "cannot_analyze"]


class ModelFileMissingError(FileNotFoundError):
    """Raised when the local MediaPipe model has not been downloaded."""


@dataclass(frozen=True)
class ArmObservation:
    """Everything measured about one arm in the primary detection pass."""

    arm: Arm
    shoulder: Point
    elbow: Point
    wrist: Point
    geometry: ArmGeometry
    angle_3d: float | None
    angle_2d: float | None
    minimum_visibility: float
    reliable: bool
    in_preparation: bool


@dataclass(frozen=True)
class AnalysisReport:
    """The explainable result shown by the Streamlit interface."""

    status: Status
    arm: Arm | None
    angle_degrees: float | None
    in_demo_range: bool | None
    message: str
    confidence: str | None = None
    spread_degrees: float | None = None
    sample_count: int = 0
    projected_angle_degrees: float | None = None
    arm_was_detected: bool = False
    reason_code: str = ""


_detector_lock = threading.Lock()
_detector_cache: dict[str, object] = {}


def get_detector(model_path: Path = DEFAULT_MODEL_PATH) -> object:
    """Return a process-wide PoseLandmarker, loading the model at most once.

    Building the landmarker costs roughly half a second while a detection costs
    about thirty milliseconds, so caching it dominates perceived speed.
    """

    if not model_path.is_file():
        raise ModelFileMissingError(
            f"Local MediaPipe model not found at {model_path}. "
            "Follow the README download step before analyzing a photo."
        )

    key = str(model_path)
    with _detector_lock:
        detector = _detector_cache.get(key)
        if detector is None:
            vision = mp.tasks.vision
            options = vision.PoseLandmarkerOptions(
                base_options=mp.tasks.BaseOptions(
                    model_asset_path=key,
                    delegate=mp.tasks.BaseOptions.Delegate.CPU,
                ),
                running_mode=vision.RunningMode.IMAGE,
                num_poses=1,
                min_pose_detection_confidence=0.5,
                min_pose_presence_confidence=0.5,
                min_tracking_confidence=0.5,
            )
            detector = vision.PoseLandmarker.create_from_options(options)
            _detector_cache[key] = detector
        return detector


def analyze_rgb_image(
    image_rgb: np.ndarray,
    arm: ArmChoice = "auto",
    *,
    minimum_visibility: float = DEFAULT_MINIMUM_VISIBILITY,
    demo_minimum: float = DEFAULT_TROPHY_MINIMUM,
    demo_maximum: float = DEFAULT_TROPHY_MAXIMUM,
    model_path: Path = DEFAULT_MODEL_PATH,
    stability_passes: bool = True,
) -> tuple[np.ndarray, AnalysisReport]:
    """Analyze one RGB photo locally and return an RGB annotation and report.

    ``arm`` may be ``"auto"`` to infer the racket arm, or an explicit side. An
    explicit side is honored even when the pose gate is unhappy, in which case
    the caution travels back in the report rather than blocking the reading.

    Photo bytes, landmarks, and the result stay in process memory for this call.
    """

    if not 0 <= minimum_visibility <= 1:
        raise ValueError("minimum_visibility must be between 0 and 1")
    if demo_minimum > demo_maximum:
        raise ValueError("demo_minimum cannot be greater than demo_maximum")
    if arm not in ("auto", "left", "right"):
        raise ValueError("arm must be 'auto', 'left', or 'right'")
    if image_rgb.ndim != 3 or image_rgb.shape[2] != 3:
        raise ValueError("image_rgb must be a three-channel RGB image")

    image_rgb = np.ascontiguousarray(image_rgb)
    canvas = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)
    detector = get_detector(model_path)

    primary = _detect(detector, image_rgb)
    if primary is None:
        return _cannot_analyze(
            canvas,
            None,
            "No person was detected in this photo.",
            "no_pose",
            hint="Use a photo where one whole player is clearly visible.",
        )

    landmarks, world_landmarks = primary
    draw_skeleton(canvas, landmarks)

    height, width = image_rgb.shape[:2]
    scale = body_scale(
        landmarks[LEFT_SHOULDER],
        landmarks[RIGHT_SHOULDER],
        landmarks[LEFT_HIP],
        landmarks[RIGHT_HIP],
        width,
        height,
    )
    if scale is None:
        return _cannot_analyze(
            canvas,
            None,
            "The player is too small or too cropped to measure.",
            "no_scale",
            hint="Fill more of the frame with the player, from head to hips.",
        )

    observations = {
        side: _observe_arm(
            side, landmarks, world_landmarks, scale, width, height, minimum_visibility
        )
        for side in ("left", "right")
    }

    selection = _select_arm(arm, observations)
    if selection.report is not None:
        return _cannot_analyze(
            canvas,
            selection.report.arm,
            selection.report.message,
            selection.report.reason_code,
            hint=selection.hint,
        )

    chosen = observations[selection.arm]
    angles = _collect_angles(
        detector, image_rgb, selection.arm, chosen.angle_3d, stability_passes
    )
    pooled = pool_angles(angles, demo_minimum, demo_maximum)
    if pooled is None:
        return _cannot_analyze(
            canvas,
            selection.arm,
            "The selected elbow geometry was invalid, so no angle was shown.",
            "invalid_geometry",
            hint="Try a photo where the shoulder, elbow, and wrist are all visible.",
        )

    if pooled.confidence == "low":
        return _cannot_analyze(
            canvas,
            selection.arm,
            "The measurement was not stable enough to report a result.",
            "unstable",
            hint=(
                f"Repeat readings disagreed by {pooled.spread_degrees:.0f} degrees "
                "with no majority. A sharper, brighter, side-on photo gives a "
                "steadier estimate."
            ),
        )

    return _analyzed(
        canvas,
        chosen,
        pooled,
        demo_minimum,
        demo_maximum,
        caution=selection.caution,
        arm_was_detected=selection.arm_was_detected,
    )


# --- arm selection -----------------------------------------------------------


@dataclass(frozen=True)
class _Selection:
    """Which arm to measure, or the reason no arm could be chosen."""

    arm: Arm = "right"
    arm_was_detected: bool = False
    report: AnalysisReport | None = None
    caution: str = ""
    hint: str = ""


def _select_arm(
    requested: ArmChoice,
    observations: dict[str, ArmObservation],
) -> _Selection:
    """Choose the racket arm, or explain why the photo cannot be scored.

    In ``auto`` mode the racket arm is the more bent of the arms that are both
    visible and already raised into a preparation position: at the trophy
    position the tossing arm is nearly straight and high, while the hitting arm
    is folded to roughly a right angle near shoulder height.
    """

    if requested != "auto":
        chosen = observations[requested]
        if not chosen.reliable:
            return _Selection(
                report=_reason(
                    requested,
                    f"The {requested} arm is not clearly visible in this photo.",
                    "arm_not_visible",
                ),
                hint="Choose a photo where that whole arm is unobstructed.",
            )
        if chosen.angle_3d is None:
            return _Selection(
                report=_reason(
                    requested,
                    "The selected elbow geometry was invalid, so no angle was shown.",
                    "invalid_geometry",
                ),
            )
        caution = (
            ""
            if chosen.in_preparation
            else (
                "This arm is not raised into a trophy position, so the reading "
                "describes a different moment of the serve."
            )
        )
        return _Selection(arm=requested, caution=caution)

    reliable = {side: item for side, item in observations.items() if item.reliable}
    if not reliable:
        return _Selection(
            report=_reason(
                None,
                "Neither arm was clearly enough visible to measure.",
                "no_reliable_arm",
            ),
            hint="Use a brighter, sharper photo with both arms unobstructed.",
        )

    candidates = {
        side: item
        for side, item in reliable.items()
        if item.in_preparation and item.angle_3d is not None
    }
    if not candidates:
        return _Selection(
            report=_reason(
                None,
                "This photo does not show a serve trophy position.",
                "not_trophy_pose",
            ),
            hint=(
                "At the trophy position the racket hand is up near shoulder height "
                "with the elbow bent. A ready stance, a contact frame, or a "
                "follow-through cannot be scored against that checkpoint."
            ),
        )

    # Only one arm is usable while the other was hidden rather than lowered:
    # the racket could be in either hand, so guessing would be dishonest.
    if len(candidates) == 1 and len(reliable) == 1:
        hidden = "left" if "right" in reliable else "right"
        return _Selection(
            report=_reason(
                None,
                "The racket arm could not be identified in this photo.",
                "ambiguous_arm",
            ),
            hint=(
                f"The {hidden} arm is hidden, so it is unclear which hand holds the "
                "racket. Use a photo showing both arms, or pick the arm manually."
            ),
        )

    # The tossing arm is the straighter one, so the most bent candidate is the
    # arm holding the racket.
    chosen = min(candidates.values(), key=lambda item: item.angle_3d)
    return _Selection(arm=chosen.arm, arm_was_detected=True)


def _reason(arm: Arm | None, message: str, reason_code: str) -> AnalysisReport:
    return AnalysisReport(
        status="cannot_analyze",
        arm=arm,
        angle_degrees=None,
        in_demo_range=None,
        message=message,
        reason_code=reason_code,
    )


# --- measurement -------------------------------------------------------------


def _observe_arm(
    arm: Arm,
    landmarks: Sequence[Point],
    world_landmarks: Sequence[Point3],
    scale: float,
    width: int,
    height: int,
    minimum_visibility: float,
) -> ArmObservation:
    """Measure one arm's visibility, raised-ness, and elbow angle in one pass."""

    indices = LEFT_ARM_INDICES if arm == "left" else RIGHT_ARM_INDICES
    shoulder, elbow, wrist = (landmarks[index] for index in indices)
    world = tuple(world_landmarks[index] for index in indices)

    geometry = arm_geometry(shoulder, elbow, wrist, scale, height)
    reliable = all(
        has_reliable_point(point, minimum_visibility) for point in (shoulder, elbow, wrist)
    )
    return ArmObservation(
        arm=arm,
        shoulder=shoulder,
        elbow=elbow,
        wrist=wrist,
        geometry=geometry,
        angle_3d=calculate_elbow_angle_3d(*world),
        angle_2d=calculate_elbow_angle(shoulder, elbow, wrist),
        minimum_visibility=min(
            shoulder.visibility, elbow.visibility, wrist.visibility
        ),
        reliable=reliable,
        in_preparation=is_in_preparation_position(geometry),
    )


def _collect_angles(
    detector: object,
    image_rgb: np.ndarray,
    arm: Arm,
    primary_angle: float | None,
    stability_passes: bool,
) -> list[float]:
    """Measure the same elbow across cheap image variants to expose instability.

    A single inference can be confidently wrong on a dark or unusual photo. A
    downscaled pass and a mirrored pass cost about thirty milliseconds each and
    turn that silent failure into a visible disagreement.
    """

    angles: list[float] = []
    if primary_angle is not None:
        angles.append(primary_angle)
    if not stability_passes:
        return angles

    height, width = image_rgb.shape[:2]
    indices = LEFT_ARM_INDICES if arm == "left" else RIGHT_ARM_INDICES
    variants: list[tuple[np.ndarray, bool]] = [
        (
            cv2.resize(
                image_rgb,
                (max(64, round(width * 0.75)), max(64, round(height * 0.75))),
                interpolation=cv2.INTER_AREA,
            ),
            False,
        ),
        (np.ascontiguousarray(image_rgb[:, ::-1]), True),
    ]

    for variant, mirrored in variants:
        detected = _detect(detector, variant)
        if detected is None:
            continue
        _, world_landmarks = detected
        lookup = tuple(_MIRRORED_INDEX[index] for index in indices) if mirrored else indices
        angle = calculate_elbow_angle_3d(*(world_landmarks[index] for index in lookup))
        if angle is not None:
            angles.append(angle)
    return angles


def _detect(
    detector: object,
    image_rgb: np.ndarray,
) -> tuple[list[Point], list[Point3]] | None:
    """Run one detection and convert the result into plain, testable points."""

    input_image = mp.Image(
        image_format=mp.ImageFormat.SRGB, data=np.ascontiguousarray(image_rgb)
    )
    with _detector_lock:
        result = detector.detect(input_image)

    if not result.pose_landmarks or not result.pose_world_landmarks:
        return None
    return (
        [
            Point(
                x=float(item.x),
                y=float(item.y),
                visibility=float(getattr(item, "visibility", 0.0)),
            )
            for item in result.pose_landmarks[0]
        ],
        [
            Point3(x=float(item.x), y=float(item.y), z=float(item.z))
            for item in result.pose_world_landmarks[0]
        ],
    )


# --- reporting ---------------------------------------------------------------


def _analyzed(
    canvas: np.ndarray,
    observation: ArmObservation,
    pooled: AngleResult,
    demo_minimum: float,
    demo_maximum: float,
    *,
    caution: str,
    arm_was_detected: bool,
) -> tuple[np.ndarray, AnalysisReport]:
    """Draw and describe a completed measurement."""

    color = GREEN if pooled.in_demo_range else RED
    verdict = "GREEN - in range" if pooled.in_demo_range else "RED - adjust"
    if pooled.in_demo_range:
        message = "Elbow bend matches the trophy-position range"
    elif pooled.degrees < demo_minimum:
        message = "Elbow is more bent than the trophy-position range"
    else:
        message = "Elbow is straighter than the trophy-position range"

    draw_measured_arm(
        canvas,
        observation.shoulder,
        observation.elbow,
        observation.wrist,
        color,
        pooled.degrees,
    )
    details = [
        f"{observation.arm.title()} elbow {pooled.degrees:.0f} deg"
        f"  |  target {demo_minimum:.0f}-{demo_maximum:.0f} deg",
        f"{message}  |  confidence {pooled.confidence}",
    ]
    if caution:
        details.append("Note: arm is not in a trophy position")
    draw_banner(canvas, f"TennisPose  {verdict}", details, color)

    return cv2.cvtColor(canvas, cv2.COLOR_BGR2RGB), AnalysisReport(
        status="analyzed",
        arm=observation.arm,
        angle_degrees=round(pooled.degrees, 1),
        in_demo_range=pooled.in_demo_range,
        message=f"{message}. {caution}".strip(),
        confidence=pooled.confidence,
        spread_degrees=round(pooled.spread_degrees, 1),
        sample_count=pooled.sample_count,
        projected_angle_degrees=(
            round(observation.angle_2d, 1) if observation.angle_2d is not None else None
        ),
        arm_was_detected=arm_was_detected,
    )


def _cannot_analyze(
    canvas: np.ndarray,
    arm: Arm | None,
    message: str,
    reason_code: str,
    *,
    hint: str = "",
) -> tuple[np.ndarray, AnalysisReport]:
    """Draw and describe a refusal, always with a reason the user can act on."""

    draw_banner(
        canvas,
        "TennisPose  CANNOT ANALYZE",
        [line for line in (message, hint) if line],
        AMBER,
    )
    return cv2.cvtColor(canvas, cv2.COLOR_BGR2RGB), AnalysisReport(
        status="cannot_analyze",
        arm=arm,
        angle_degrees=None,
        in_demo_range=None,
        message=f"{message} {hint}".strip(),
        reason_code=reason_code,
    )
