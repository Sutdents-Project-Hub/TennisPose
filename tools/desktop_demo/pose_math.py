"""Pure geometry and feedback rules for the desktop pose-analysis demo."""

from __future__ import annotations

from dataclasses import dataclass
from math import acos, degrees, hypot, isfinite


@dataclass(frozen=True)
class Point:
    """One normalized image-space point with an optional detector confidence."""

    x: float
    y: float
    visibility: float = 1.0


@dataclass(frozen=True)
class AngleResult:
    """A valid elbow-angle measurement and its demonstration feedback."""

    degrees: float
    in_demo_range: bool


def has_reliable_point(point: Point, minimum_visibility: float) -> bool:
    """Return whether a point is finite and meets the configured confidence gate."""

    return (
        isfinite(point.x)
        and isfinite(point.y)
        and isfinite(point.visibility)
        and point.visibility >= minimum_visibility
    )


def calculate_elbow_angle(
    shoulder: Point,
    elbow: Point,
    wrist: Point,
) -> float | None:
    """Return the interior shoulder-elbow-wrist angle, or None for bad geometry."""

    shoulder_vector = (shoulder.x - elbow.x, shoulder.y - elbow.y)
    wrist_vector = (wrist.x - elbow.x, wrist.y - elbow.y)
    shoulder_length = hypot(*shoulder_vector)
    wrist_length = hypot(*wrist_vector)

    if shoulder_length == 0 or wrist_length == 0:
        return None

    cosine = (
        shoulder_vector[0] * wrist_vector[0]
        + shoulder_vector[1] * wrist_vector[1]
    ) / (shoulder_length * wrist_length)
    angle = degrees(acos(max(-1.0, min(1.0, cosine))))
    return angle if isfinite(angle) else None


def make_angle_result(
    angle: float,
    demo_minimum: float,
    demo_maximum: float,
) -> AngleResult:
    """Apply the inclusive demonstration range to an already valid angle."""

    return AngleResult(
        degrees=angle,
        in_demo_range=demo_minimum <= angle <= demo_maximum,
    )
