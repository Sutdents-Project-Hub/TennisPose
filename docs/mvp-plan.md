# Streamlit MVP Roadmap and Test Plan

## Definition of Done

The MVP is complete when a reviewer can run the local Streamlit application, upload an authorized Trophy Pose JPEG or PNG, see the racket arm detected and a transparent elbow-angle result for both an in-range and an adjustment example, and receive a safe cannot-analyze response for unreliable input and, in auto-detect mode, for a photo that is not a trophy position.

The product is a locally served web application. There is no Android, iOS, APK, device-permission, or native-runtime acceptance gate.

## Delivery Plan

| Phase | Status | Exit evidence |
|---|---|---|
| 0. Repository migration | Complete | Active tracked product paths and documents are Streamlit/Python; the prior mobile sources are removed from the delivered repository. |
| 1. Local app bootstrap | Complete | `streamlit_app.py`, `requirements.txt`, and the ignored local model started on `127.0.0.1:8501` on August 28, 2026. |
| 2. Geometry and feedback tests | Complete | `tests/` covers 2D and 3D geometry, body scale, the trophy-position gate, racket-arm selection, pooling and confidence, entry-point guards, content validation, and size limits; 49 tests passed on August 28, 2026. |
| 3. Upload, inference, and annotation | Complete | Ten authorized reference photos were replayed through the full pipeline on August 28, 2026: four elite trophy positions returned green with the racket arm auto-detected (including a left-handed server), three post-trophy frames returned red, and three unmeasurable photos returned cannot-analyze with distinct reason codes. Locked in by `tests/test_reference_photos.py`. |
| 4. Manual local acceptance | Partially verified | The green and cannot-analyze paths were exercised in the local browser on August 28, 2026. The red path is verified by the reference suite but not yet recorded through the browser, and the invalid-input path still needs a browser pass. |
| 5. Competition evidence | Pending | Prepare authorized photos, record the two-minute local demo, and state limitations. |
| 6. Submission check | Pending | Reconcile official rules, attribution, license, repository visibility, and final materials. |

Do not claim a phase complete until its stated evidence is actually recorded. The configurable angle range still requires coach validation or replacement before any stronger claim is made.

## Test Matrix

| Case | Expected result | Required evidence |
|---|---|---|
| Right and straight point sets | Correct angles within tolerance | `python -m unittest discover -s tests -v` |
| Arm bent toward the camera | The 3D angle reflects the real bend where the 2D projection does not | `python -m unittest discover -s tests -v` |
| Zero-length point geometry | Cannot-analyze outcome; no crash | `python -m unittest discover -s tests -v` |
| Feedback boundaries | 80 and 120 are in range; values outside are adjustment suggested | `python -m unittest discover -s tests -v` |
| Left-handed server | The left arm is auto-detected as the racket arm | `python -m unittest discover -s tests -v` |
| Ready stance, contact, or follow-through | Refused or reported as outside the range; never a green trophy verdict | `python -m unittest discover -s tests -v` |
| Hidden racket arm | Ambiguous-arm refusal, not a measurement of the tossing arm | `python -m unittest discover -s tests -v` |
| Passes that do not agree | Median reported when a majority agrees; refusal when none does | `python -m unittest discover -s tests -v` |
| Ten authorized reference photos | Recorded arm, verdict, and angle within tolerance | `TENNISPOSE_SAMPLE_DIR=... python -m unittest discover -s tests -v` |
| No image | Clear instruction and one primary upload action | Manual local Streamlit check |
| Unsupported, oversized, or unreadable input | Clear recovery guidance; no score | Automated content/size tests and manual local Streamlit check |
| Clear one-person Trophy Pose | Overlay, angle, confidence, and configured result | Manual local Streamlit check with authorized image |
| Blurry, occluded, or unsuitable photo | Cannot-analyze state; no score | Manual local Streamlit check with authorized image |
| In-range and adjustment examples | Separate green and red flows | Manual local recording-ready evidence |

## Competition Demo Script

1. State the learner problem and the deliberate single-photo scope.
2. Upload the adjustment-case image and explain the red result.
3. Upload the in-range image and show the same transparent calculation path.
4. Explain that the elbow angle comes from three visible landmarks, not an unexplained score.
5. Open "How this number was measured" and show the 3D reading beside the flat 2D
   one. This is the strongest algorithm moment in the demo: on the Federer photo
   the projection reads 33 degrees while the arm is actually near 83, which is
   exactly why the depth-aware landmarks are used.
6. Leave auto-detect selected, upload a photo that is not a trophy position, and show the app refusing with a
   reason instead of inventing a score.
7. State limits: still image, viewpoint sensitivity, local processing, an
   adjustable demonstration range, and no medical claim.

## Verification Record

Record only checks run against the Streamlit implementation. Historical Flutter, emulator, APK, iOS, and separate desktop-prototype results are not acceptance evidence for this product and must not be reported as current verification.

Required commands:

```bash
.venv/bin/python -m unittest discover -s tests -v
.venv/bin/streamlit run streamlit_app.py
```

Include the reference photos when checking accuracy, so the suite runs the
regression gate rather than skipping it:

```bash
TENNISPOSE_SAMPLE_DIR=~/Desktop/TennisPose_Test_Images/normal_use_samples \
  .venv/bin/python -m unittest discover -s tests -v
```

### Recorded accuracy run — August 28, 2026

Ten authorized reference photos, auto arm detection, 80-120 degree range:

| Photo shows | Photos | Result |
|---|---|---|
| Trophy position | 4 | Green, racket arm auto-detected, 83-111 degrees |
| Contact or follow-through | 3 | Red, elbow straighter than the range |
| Ready stance, hidden arm, or arm still low | 3 | Cannot analyze, with distinct reason codes |

The previous 2D pipeline scored the same four trophy photos at 33-89 degrees and
reported red for three of them.
