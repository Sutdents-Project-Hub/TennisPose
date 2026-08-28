# Local Dependencies and Model Integration

## Local Pose Strategy

The delivered application uses Streamlit for a locally served browser interface and MediaPipe Tasks PoseLandmarker for a single-image local inference pass. The PoseLandmarker uses the CPU delegate so the MVP does not require a GPU or any cloud computer-vision service.

`tennispose.pose_detector` owns model loading, the inference passes, and racket-arm selection. It must require reliable shoulder, elbow, and wrist points before passing values to `tennispose.pose_math`, and it must read the angle from `pose_world_landmarks` rather than the normalized image landmarks. The model is cached for the process lifetime and guarded by a lock, because building a PoseLandmarker costs about half a second while a detection costs about thirty milliseconds, and the MediaPipe detector is not safe to call concurrently. The geometry, gating, and feedback rules remain pure Python and independent of Streamlit widgets or MediaPipe objects.

## Resolved Dependencies

| Category | Role |
|---|---|
| Python | Local runtime; Python 3.11 is the documented setup baseline. |
| Streamlit | Local web interface, upload control, selection, and result presentation. |
| MediaPipe Tasks | Local PoseLandmarker model invocation for one image. |
| NumPy and image-rendering dependency | Image conversion and local annotation support as pinned in `requirements.txt`. |
| Python `unittest` | Standard-library unit tests for geometry and feedback behavior. |

Exact dependency versions are pinned in `requirements.txt`; update this document when dependency roles, model format, or runtime requirements change.

## Model Handling

- The heavy PoseLandmarker task file is a local dependency at `models/pose_landmarker_heavy.task`, an ignored path.
- Download the model manually during setup. Analysis must not download the model automatically or send uploaded images to the internet.
- Review MediaPipe and model terms before redistribution, public hosting, or packaging.
- Local landmarks are sensitive to image quality, orientation, occlusion, framing, and model limitations. The application must return cannot-analyze when required points cannot be trusted.

## Primary References

- Streamlit documentation: https://docs.streamlit.io/
- MediaPipe Pose Landmarker for Python: https://ai.google.dev/edge/mediapipe/solutions/vision/pose_landmarker/python
- Pose Landmarker model catalog: https://ai.google.dev/edge/mediapipe/solutions/vision/pose_landmarker

No LLM, remote computer-vision API, analytics SDK, identity provider, payment service, backend service, or API key is part of this MVP. Adding any of these changes privacy, cost, reliability, and competition disclosure requirements.
