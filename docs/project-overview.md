# Product Requirements and Acceptance

## User Problem

A learner may have a serve photo but no immediate way to inspect one key Trophy Pose arm angle. TennisPose turns one authorized local photo into a transparent visual result rather than a black-box score.

## Target User

The primary user is a tennis learner or student with a desktop browser and a clear side-view Trophy Pose photo. The local web application supports practice reflection and a competition demonstration; it is not for clinical, rehabilitation, or professional biomechanical assessment.

## Primary User Story

As a learner, I can upload an authorized Trophy Pose photo in the local web app and see the shoulder-elbow-wrist overlay and angle for my racket arm, so I understand the feedback rather than receiving a score.

## Functional Requirements

| ID | Requirement | MVP acceptance condition |
|---|---|---|
| FR-01 | Upload a photo | The local page accepts JPEG or PNG content only, limits input to 10 MB and 20 megapixels, and handles no upload, unsupported, oversized, or unreadable input safely. |
| FR-02 | Identify the racket arm | The app detects the racket arm automatically and works for a left-handed or right-handed server. The user can override the choice with an explicit left or right selection. |
| FR-03 | Detect pose | The local MediaPipe adapter returns selected-side landmarks or a typed cannot-analyze state. |
| FR-04 | Measure angle | The app calculates the elbow angle from shoulder-elbow and wrist-elbow vectors in 3D world space, so a foreshortened arm is not understated. |
| FR-05 | Render evidence | The image shows relevant points, arm segments, and numeric angle. |
| FR-06 | Explain result | The app labels a demonstration range and shows neutral in-range or adjustment feedback. |
| FR-07 | Fail safely | Missing image, invalid input, missing landmarks, and invalid geometry never create a score. |
| FR-08 | Refuse the wrong moment | In auto-detect mode, a photo that is not a serve trophy position returns cannot-analyze with the reason, rather than scoring a different moment of the serve against the trophy checkpoint. A visible manual arm override is measured with a caution. |
| FR-09 | Report confidence | The app measures the photo more than once and reports how much the readings disagreed, refusing when no majority agrees. |

## Non-Functional Requirements

- Analysis runs locally without an account, database, API key, cloud service, or analysis-time internet dependency after model setup.
- The complete flow is understandable in a two-minute competition video.
- Raw photos, landmarks, and results are not persisted after the current analysis session.
- All visible product copy, source comments, documentation, and repository artifacts use English.
- The application uses CPU inference and does not require camera input or GPU acceleration.

## Out of Scope

- Live camera, video, tracking, ball detection, full-swing scoring, or history.
- Native mobile applications, APK distribution, mobile-device permissions, or iOS/Android delivery.
- Sharing, social features, subscriptions, dashboards, public deployment, or server-side features.
- Injury or medical claims.

## Acceptance Evidence

1. **Required unit tests:** Python tests cover 2D and 3D angle geometry, body scale, the trophy-position gate, racket-arm selection, pooling and confidence, entry-point guards, and inclusive feedback boundaries.
2. **Required accuracy regression:** `tests/test_reference_photos.py` replays the authorized reference photos and asserts the chosen arm, the verdict, and the angle against recorded expectations.
3. **Required manual local check:** A clear authorized photo reaches the configured in-range result.
4. **Required manual local check:** A clear authorized photo reaches the configured adjustment result.
5. **Required manual local check:** In auto-detect mode, a non-trophy photo refuses instead of scoring.
6. **Required manual local check:** An unreliable input reaches a clear cannot-analyze state.
7. **Required manual local check:** Empty, unsupported, or unreadable input returns safe recovery guidance.
8. **Required submission review:** Overlay, limitations, demo script, attribution, and behavior agree.
