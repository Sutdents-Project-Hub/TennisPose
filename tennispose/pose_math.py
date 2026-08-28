"""Pure, testable geometry, gating rules, and feedback thresholds.

This module deliberately imports nothing from MediaPipe or OpenCV so that every
decision the product makes can be unit tested without a model file or an image.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import acos, degrees, isfinite, sqrt
from statistics import median
from typing import Literal, Sequence


Arm = Literal["left", "right"]

# --- Trophy-position feedback thresholds -------------------------------------
# Coaching references describe the serve trophy position as a hitting elbow bent
# to roughly a right angle. Measured across the elite reference photos in
# tests/reference_expectations.json the observed spread is about 83-112 degrees, and
# monocular 3D estimation adds roughly +/- 10 degrees, so the inclusive default
# band is widened accordingly. It is demonstration logic, not a clinical rule.
DEFAULT_TROPHY_MINIMUM = 80.0
DEFAULT_TROPHY_MAXIMUM = 120.0

# MediaPipe visibility below this is treated as "the model is guessing".
# 0.55 was previously used and rejected usable dim photos; 0.35 still rejects
# a fully hidden arm, which reports visibility near 0.01.
DEFAULT_MINIMUM_VISIBILITY = 0.35

# Agreement between the test-time-augmentation passes, in degrees.
# The reported value is the median of the passes, so the useful question is not
# "did every pass agree" but "did a majority agree". CONSENSUS_* therefore grades
# the typical deviation from the median, while NO_CONSENSUS_SPREAD_DEGREES is the
# separate guard for a photo where every pass disagreed and the model is lost.
STABLE_SPREAD_DEGREES = 8.0
MAX_SPREAD_DEGREES = 20.0
NO_CONSENSUS_SPREAD_DEGREES = 60.0

# Trophy-position gate, expressed in body-scale units where 1.0 is the distance
# from the shoulder line to the hip line. Positive means "above the shoulder".
MIN_WRIST_RISE = -0.25
MIN_ELBOW_RISE = -0.45

Confidence = Literal["high", "moderate", "low"]


@dataclass(frozen=True)
class Point:
    """One normalized image-space point with detector visibility.

    ``y`` grows downward, matching image coordinates.
    """

    x: float
    y: float
    visibility: float = 1.0


@dataclass(frozen=True)
class Point3:
    """One metric world-space point in meters, relative to the hip midpoint."""

    x: float
    y: float
    z: float


@dataclass(frozen=True)
class ArmGeometry:
    """Scale-normalized position of one arm relative to its own shoulder."""

    wrist_rise: float
    elbow_rise: float


@dataclass(frozen=True)
class AngleResult:
    """A pooled elbow-angle measurement and its demonstration feedback.

    ``spread_degrees`` is the full range across passes and is what the interface
    discloses as uncertainty. ``consensus_degrees`` is the median deviation from
    the median, which is what actually grades ``confidence``.
    """

    degrees: float
    spread_degrees: float
    consensus_degrees: float
    confidence: Confidence
    in_demo_range: bool
    sample_count: int


def has_reliable_point(point: Point, minimum_visibility: float) -> bool:
    """Return whether a point is finite and meets the visibility threshold."""

    return (
        isfinite(point.x)
        and isfinite(point.y)
        and isfinite(point.visibility)
        and point.visibility >= minimum_visibility
    )


def calculate_elbow_angle(shoulder: Point, elbow: Point, wrist: Point) -> float | None:
    """Return the projected shoulder-elbow-wrist angle, or ``None`` if degenerate.

    This is the flat image-plane angle. It is kept for transparency and testing
    only: an arm pointing toward or away from the camera is foreshortened, so
    this value can understate a real bend by 50 degrees or more. Product
    decisions use :func:`calculate_elbow_angle_3d` instead.
    """

    if not all(
        isfinite(value)
        for value in (shoulder.x, shoulder.y, elbow.x, elbow.y, wrist.x, wrist.y)
    ):
        return None

    return _angle_between(
        (shoulder.x - elbow.x, shoulder.y - elbow.y),
        (wrist.x - elbow.x, wrist.y - elbow.y),
    )


def calculate_elbow_angle_3d(
    shoulder: Point3,
    elbow: Point3,
    wrist: Point3,
) -> float | None:
    """Return the true shoulder-elbow-wrist angle from metric world landmarks.

    World landmarks carry a depth estimate, so this stays correct when the arm
    is foreshortened by the camera angle. Returns ``None`` for degenerate or
    non-finite geometry.
    """

    values = (
        shoulder.x, shoulder.y, shoulder.z,
        elbow.x, elbow.y, elbow.z,
        wrist.x, wrist.y, wrist.z,
    )
    if not all(isfinite(value) for value in values):
        return None

    return _angle_between(
        (shoulder.x - elbow.x, shoulder.y - elbow.y, shoulder.z - elbow.z),
        (wrist.x - elbow.x, wrist.y - elbow.y, wrist.z - elbow.z),
    )


def _angle_between(first: Sequence[float], second: Sequence[float]) -> float | None:
    """Return the angle in degrees between two vectors of equal dimension."""

    first_length = sqrt(sum(value * value for value in first))
    second_length = sqrt(sum(value * value for value in second))
    if first_length < 1e-9 or second_length < 1e-9:
        return None

    dot = sum(a * b for a, b in zip(first, second))
    cosine = max(-1.0, min(1.0, dot / (first_length * second_length)))
    angle = degrees(acos(cosine))
    return angle if isfinite(angle) else None


def body_scale(
    left_shoulder: Point,
    right_shoulder: Point,
    left_hip: Point,
    right_hip: Point,
    width: int,
    height: int,
) -> float | None:
    """Return a pixel length that one torso spans, used to normalize positions.

    Falls back to shoulder width when the hips are missing or implausible, so a
    cropped upper-body photo still yields a usable scale. Returns ``None`` when
    the person is too small to measure.
    """

    def pixel(point: Point) -> tuple[float, float]:
        return (point.x * width, point.y * height)

    def distance(first: tuple[float, float], second: tuple[float, float]) -> float:
        return sqrt((first[0] - second[0]) ** 2 + (first[1] - second[1]) ** 2)

    shoulder_mid = _midpoint(pixel(left_shoulder), pixel(right_shoulder))
    hip_mid = _midpoint(pixel(left_hip), pixel(right_hip))
    torso = distance(shoulder_mid, hip_mid)
    shoulders = distance(pixel(left_shoulder), pixel(right_shoulder))

    hips_usable = (
        has_reliable_point(left_hip, 0.2)
        and has_reliable_point(right_hip, 0.2)
        and isfinite(torso)
    )
    scale = max(torso if hips_usable else 0.0, shoulders)
    return scale if isfinite(scale) and scale >= 20.0 else None


def _midpoint(first: tuple[float, float], second: tuple[float, float]) -> tuple[float, float]:
    return ((first[0] + second[0]) / 2, (first[1] + second[1]) / 2)


def arm_geometry(
    shoulder: Point,
    elbow: Point,
    wrist: Point,
    scale: float,
    height: int,
) -> ArmGeometry:
    """Return how far the elbow and wrist sit above the shoulder, in body scales.

    Positive values mean "above the shoulder" because image ``y`` grows downward.
    """

    return ArmGeometry(
        wrist_rise=(shoulder.y - wrist.y) * height / scale,
        elbow_rise=(shoulder.y - elbow.y) * height / scale,
    )


def is_in_preparation_position(geometry: ArmGeometry) -> bool:
    """Return whether one arm is raised into a serve preparation position.

    At the trophy position the hitting wrist sits near or just above shoulder
    height and the elbow is at most a little below it. A hand resting at the
    waist, or an arm that has already swung down after contact, fails this test.
    """

    return (
        isfinite(geometry.wrist_rise)
        and isfinite(geometry.elbow_rise)
        and geometry.wrist_rise >= MIN_WRIST_RISE
        and geometry.elbow_rise >= MIN_ELBOW_RISE
    )


def classify_confidence(
    consensus_degrees: float,
    *,
    stable_spread: float = STABLE_SPREAD_DEGREES,
    maximum_spread: float = MAX_SPREAD_DEGREES,
) -> Confidence:
    """Grade a measurement by how far the passes sat from their own median."""

    if consensus_degrees <= stable_spread:
        return "high"
    if consensus_degrees <= maximum_spread:
        return "moderate"
    return "low"


def pool_angles(
    angles: Sequence[float],
    demo_minimum: float,
    demo_maximum: float,
    *,
    stable_spread: float = STABLE_SPREAD_DEGREES,
    maximum_spread: float = MAX_SPREAD_DEGREES,
) -> AngleResult | None:
    """Combine repeated measurements of one elbow into a single graded result.

    The median resists a single bad pass, and the spread between passes becomes
    the reported confidence. Returns ``None`` when nothing measurable was given.
    """

    usable = [angle for angle in angles if isfinite(angle)]
    if not usable:
        return None

    pooled = float(median(usable))
    spread = max(usable) - min(usable)
    consensus = float(median([abs(angle - pooled) for angle in usable]))

    confidence = classify_confidence(
        consensus, stable_spread=stable_spread, maximum_spread=maximum_spread
    )
    # Every pass landing somewhere different means there is no majority to trust,
    # however tight the median happens to look.
    if spread > NO_CONSENSUS_SPREAD_DEGREES:
        confidence = "low"

    return AngleResult(
        degrees=pooled,
        spread_degrees=spread,
        consensus_degrees=consensus,
        confidence=confidence,
        in_demo_range=demo_minimum <= pooled <= demo_maximum,
        sample_count=len(usable),
    )


def make_angle_result(
    angle: float,
    demo_minimum: float,
    demo_maximum: float,
) -> AngleResult:
    """Apply the inclusive demonstration range to one already valid angle."""

    return AngleResult(
        degrees=angle,
        spread_degrees=0.0,
        consensus_degrees=0.0,
        confidence="high",
        in_demo_range=demo_minimum <= angle <= demo_maximum,
        sample_count=1,
    )
