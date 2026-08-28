"""Streamlit entry point for TennisPose's local single-photo MVP."""

from __future__ import annotations

import cv2
import numpy as np
import streamlit as st

from tennispose.image_input import UploadedImageError, decode_uploaded_image
from tennispose.pose_detector import (
    DEFAULT_MINIMUM_VISIBILITY,
    DEFAULT_TROPHY_MAXIMUM,
    DEFAULT_TROPHY_MINIMUM,
    AnalysisReport,
    ModelFileMissingError,
    analyze_rgb_image,
    get_detector,
)

MAX_DISPLAY_WIDTH = 1000

ARM_CHOICES = {
    "Auto-detect racket arm": "auto",
    "Player's right arm": "right",
    "Player's left arm": "left",
}

st.set_page_config(page_title="TennisPose", page_icon="🎾", layout="wide")


@st.cache_resource(show_spinner=False)
def load_detector() -> object:
    """Load the pose model once per server process rather than once per upload."""

    return get_detector()


def fit_result_image(image_rgb: np.ndarray) -> np.ndarray:
    """Downscale only very large photos so the annotation stays sharp on screen."""

    height, width = image_rgb.shape[:2]
    if width <= MAX_DISPLAY_WIDTH:
        return image_rgb
    scale = MAX_DISPLAY_WIDTH / width
    return cv2.resize(
        image_rgb,
        (MAX_DISPLAY_WIDTH, max(1, round(height * scale))),
        interpolation=cv2.INTER_AREA,
    )


def render_verdict(report: AnalysisReport, minimum: float, maximum: float) -> None:
    """Show the headline result: one angle, one colour, one sentence."""

    angle_column, status_column, range_column = st.columns(3)
    angle_column.metric("Elbow angle", f"{report.angle_degrees:.0f}°")
    range_column.metric("Target range", f"{minimum:.0f}°–{maximum:.0f}°")

    if report.in_demo_range:
        status_column.metric("Result", "🟢 Green")
        st.success(f"**Green — in range.** {report.message}")
    else:
        status_column.metric("Result", "🔴 Red")
        st.error(f"**Red — adjust.** {report.message}")

    if report.confidence == "moderate":
        st.warning(
            "Moderate confidence: the repeat measurements of this photo disagreed "
            "more than usual. Treat the angle as approximate."
        )


def render_measurement_detail(report: AnalysisReport) -> None:
    """Expose the working behind the number so the result stays checkable."""

    spread = report.spread_degrees or 0.0
    with st.expander("How this number was measured"):
        st.markdown(
            f"""
- **Arm measured:** player's {report.arm} arm
  ({'auto-detected' if report.arm_was_detected else 'selected'})
- **Angle source:** MediaPipe 3D world landmarks (shoulder → elbow → wrist)
- **Passes combined:** {report.sample_count} (original, downscaled, mirrored) —
  the reported value is their median
- **Disagreement across passes:** ±{spread / 2:.0f}° (full range {spread:.0f}°)
- **Confidence:** {report.confidence}
"""
        )
        if report.projected_angle_degrees is not None:
            st.caption(
                f"For comparison, the flat 2D image-plane angle is "
                f"{report.projected_angle_degrees:.0f}°. It differs whenever the arm "
                "points toward or away from the camera, which is why the 3D "
                "landmarks are used for the verdict."
            )


def main() -> None:
    st.title("🎾 TennisPose")
    st.caption(
        "Upload one serve photo. TennisPose finds the shoulder, elbow, and wrist, "
        "measures the racket-arm elbow angle in 3D, and shows green, red, or "
        "cannot-analyze."
    )

    with st.sidebar:
        st.header("Analysis settings")
        arm_label = st.radio("Arm to inspect", options=tuple(ARM_CHOICES))
        arm = ARM_CHOICES[arm_label]
        if arm == "auto":
            st.caption(
                "At the trophy position the tossing arm is straight and high while "
                "the racket arm is bent near shoulder height. Auto-detect uses that "
                "difference; override it if the photo is unusual."
            )

        minimum, maximum = st.slider(
            "Target elbow range (degrees)",
            min_value=40,
            max_value=180,
            value=(int(DEFAULT_TROPHY_MINIMUM), int(DEFAULT_TROPHY_MAXIMUM)),
            help="Green when the measured angle falls inside this inclusive band.",
        )

        st.divider()
        st.caption(
            "One uploaded photo is processed locally for this request only. It is "
            "not saved, sent to a server, or used to diagnose injury."
        )
        uploaded_file = st.file_uploader(
            "Upload a Trophy Pose photo",
            type=("jpg", "jpeg", "png"),
            help="A clear JPEG or PNG with one person and both arms visible (max 10 MB).",
        )

    if uploaded_file is None:
        st.info(
            "Choose one JPEG or PNG photo from the sidebar to begin. A side-on shot "
            "of the trophy position — racket up, elbow bent, tossing arm extended — "
            "works best."
        )
        with st.expander("What this MVP checks, and what it does not"):
            st.markdown(
                """
**It checks one thing:** the racket-arm elbow angle at the serve trophy
position, measured from a single still photo.

**It refuses rather than guesses** when the arm is hidden, the player is too
small in the frame, the photo is not a trophy position, or repeat measurements
of the same photo do not agree.

**It is not** a full serve analysis, a video tracker, a coach, or a medical or
injury-prevention tool. The target range is configurable demonstration logic,
not a validated coaching or clinical standard.
"""
            )
        return

    try:
        image_rgb = decode_uploaded_image(uploaded_file.getvalue())
    except UploadedImageError as error:
        st.error(str(error))
        st.caption(
            "Choose another JPEG or PNG photo within the 10 MB upload and "
            "20 megapixel decode limits."
        )
        return

    try:
        with st.spinner("Finding pose landmarks locally…"):
            load_detector()
            annotated_image, report = analyze_rgb_image(
                image_rgb,
                arm,
                minimum_visibility=DEFAULT_MINIMUM_VISIBILITY,
                demo_minimum=float(minimum),
                demo_maximum=float(maximum),
            )
    except ModelFileMissingError as error:
        st.error("The local pose model is not installed yet.")
        st.code(str(error), language=None)
        st.caption("Use the model download command in README.md, then rerun Streamlit.")
        return
    except Exception:  # MediaPipe returns platform-specific runtime errors.
        st.error("The local pose analysis could not finish for this photo.")
        st.caption("Choose a clear JPEG or PNG with one visible person, then try again.")
        return

    display_image = fit_result_image(annotated_image)

    if report.status == "cannot_analyze":
        st.warning(f"**Cannot analyze.** {report.message}")
        st.caption(
            "No score was generated. TennisPose reports nothing rather than "
            "reporting a number it cannot stand behind."
        )
        st.image(display_image, use_container_width=True)
        return

    render_verdict(report, float(minimum), float(maximum))
    st.image(display_image, use_container_width=True)
    render_measurement_detail(report)
    st.caption(
        "The target range is configurable demonstration logic, not a medically or "
        "professionally validated standard."
    )


if __name__ == "__main__":
    main()
