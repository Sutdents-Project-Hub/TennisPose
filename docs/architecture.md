# Solution Architecture

## Delivery Model

TennisPose is a local Streamlit web application. A browser connects to a Streamlit process on the same machine; the process decodes one uploaded image, runs local MediaPipe PoseLandmarker CPU inference over a few variants of that image, selects and validates the racket arm, pools the elbow angle, and returns an annotated result. No server, cloud API, database, or remote model is required.

```text
Local browser
  -> Streamlit upload, arm mode, and target range
  -> in-memory image bytes
  -> local MediaPipe PoseLandmarker (CPU, loaded once per process)
  -> per-arm reliability, body scale, and trophy-position gate
  -> racket-arm selection (auto or explicit)
  -> 3D elbow angle over original + downscaled + mirrored passes
  -> median angle, spread, and confidence
  -> annotated image and typed report
  -> Streamlit feedback UI
```

`streamlit_app.py` is the application entry point. `tennispose/` contains reusable local analysis code; it does not expose an HTTP API or run as a separate service.

## Module Boundaries

| Path | Responsibility | Must not do |
|---|---|---|
| `streamlit_app.py` | Streamlit page, upload control, arm mode, target range, and presentation of results | Contain geometry rules or persist user data |
| `tennispose/image_input.py` | Enforce JPEG/PNG content, 10 MB upload, and 20 megapixel decode limits before RGB conversion | Persist source bytes or accept another format |
| `tennispose/pose_math.py` | Point validation, 2D and 3D angle calculation, body scale, trophy-position gate, pooling, confidence, and feedback rule | Import Streamlit, OpenCV, MediaPipe, files, or network services |
| `tennispose/pose_detector.py` | Cache the local model, run the inference passes, select the racket arm, and build the typed report | Create a backend, persist images, draw, or make medical claims |
| `tennispose/annotate.py` | Draw the skeleton, measured arm, angle arc, and result banner onto one BGR canvas | Decide a verdict or run inference |
| `tests/` | Deterministic coverage of geometry, gating, selection, entry-point guards, and reference-photo accuracy | Depend on a browser or on photos that cannot be skipped |
| `models/` | Ignored local MediaPipe model dependency | Store user images or tracked project assets |

## Geometry Contract

For shoulder `S`, elbow `E`, and wrist `W`, calculate the interior elbow angle between `S - E` and `W - E`.

```text
cos(theta) = dot(S - E, W - E) / (norm(S - E) * norm(W - E))
angle = degrees(arccos(clamp(cos(theta), -1, 1)))
```

The vectors come from MediaPipe's **`pose_world_landmarks`**, which are metric 3D
coordinates relative to the hip midpoint. This is a correctness requirement, not
an optimization: a serve points the racket arm toward or away from the camera, so
the same formula over the flat normalized landmarks reports a foreshortened angle.
On the reference photos the projection understated the bend by up to 60 degrees.
The 2D value is still computed and surfaced in the interface for comparison, but
never decides a verdict.

## Selection and Gating Contract

Positions are normalized by a body scale — the shoulder-line to hip-line distance
in pixels, falling back to shoulder width when the hips are hidden — so the same
thresholds hold at any photo size. `rise` is measured upward from the arm's own
shoulder, so a positive value means "above the shoulder".

| Rule | Threshold | Purpose |
|---|---|---|
| Landmark reliability | visibility >= 0.35 | Reject an arm the model is guessing at rather than seeing |
| Wrist raised | `wrist_rise` >= -0.25 | Reject an arm that has swung down past the trophy position |
| Elbow raised | `elbow_rise` >= -0.45 | Reject a hand resting at the waist with the forearm folded up |
| Racket arm (auto) | most bent surviving arm | The tossing arm is straight and high; the racket arm is folded |
| Ambiguity | one arm usable, other hidden | Refuse: either hand could hold the racket |
| Confidence | median deviation across passes | Grade the reading; refuse when no majority agrees |

An explicit left/right selection overrides auto-detection. Reliability still
blocks an unmeasurable arm, but the trophy-position gate becomes a caution
carried in the report rather than a refusal, so a deliberate choice is honored.

Every rejection returns `cannot analyze` with a reason code, never a score. Valid
angles are mapped to an adjustable inclusive demonstration range that defaults to
80–120 degrees: green when in range and red when adjustment is suggested.

## Result States

| State | Trigger | Browser behavior |
|---|---|---|
| Idle | No image uploaded | Explain the one-photo requirement and local-processing boundary. |
| Image ready | A readable JPEG or PNG is uploaded | Keep the current arm selector visible; after inference, show only the annotated result rather than a duplicate original-photo preview. |
| Analyzing | The current upload or any setting changes | Run the local inference passes and show Streamlit's progress indicator. |
| Analyzed | An arm was selected, gated, and pooled successfully | Show annotated image, angle, configured range, confidence, green/red feedback, and the measurement detail panel. |
| Cannot analyze | Any reason code below | Explain the issue and allow another image without a score. |

### Cannot-analyze reason codes

| Code | Meaning |
|---|---|
| `no_pose` | No person was detected in the photo. |
| `no_scale` | The player is too small or too cropped to normalize positions against. |
| `no_reliable_arm` | Neither arm was visible enough to measure. |
| `arm_not_visible` | The explicitly selected arm was not visible enough to measure. |
| `not_trophy_pose` | Neither arm is raised into a serve preparation position. |
| `ambiguous_arm` | Only one arm is usable and the other is hidden, so the racket hand is unknown. |
| `invalid_geometry` | Zero-length or non-finite shoulder-elbow-wrist geometry. |
| `unstable` | The inference passes disagreed with no majority to trust. |

## Local Processing Boundary

- Image bytes, landmarks, angle, and feedback stay in memory for the active local Streamlit session. JPEG/PNG content is rechecked after upload; the app rejects files above 10 MB or 20 megapixels before RGB conversion.
- The MediaPipe model is downloaded once to an ignored `models/` path. Loading it is local; inference does not upload a photo or call a remote service.
- The application does not intentionally write uploaded photos, landmark coordinates, or results to disk, logs, databases, or history.
- Public deployment, result storage, sharing, telemetry, camera input, or video support are separate architecture and privacy changes requiring explicit approval.
