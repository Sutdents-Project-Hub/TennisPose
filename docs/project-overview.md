# Product Requirements and Acceptance

## User Problem

A learner may have a serve photo but no immediate way to understand one key Trophy Pose arm angle. TennisPose turns one authorized photo into a transparent visual result rather than a black-box score.

## Target User

The primary user is a tennis learner or student with an Android phone and a clear side-view Trophy Pose photo. The app supports practice reflection and a competition demonstration; it is not for clinical, rehabilitation, or professional biomechanical assessment.

The project team may also use the local desktop algorithm demo to validate still-image behavior and record a prototype walkthrough before the mobile interface is ready. That tool is not a separate end-user product.

## Primary User Story

As a learner, I can select an authorized Trophy Pose photo from my phone, choose the arm I want to inspect, and see the shoulder-elbow-wrist overlay and angle so I understand the feedback.

## Functional Requirements

| ID | Requirement | MVP acceptance condition |
|---|---|---|
| FR-01 | Select a photo | The app opens the phone picker, accepts a JPEG or PNG, and handles cancel or denial safely. |
| FR-02 | Select arm side | The user can choose left or right before analysis. |
| FR-03 | Detect pose | The on-device adapter returns selected-side landmarks or a typed cannot-analyze state. |
| FR-04 | Measure angle | The app calculates the elbow angle from shoulder-elbow and wrist-elbow vectors. |
| FR-05 | Render evidence | The image shows relevant points, arm segments, and numeric angle. |
| FR-06 | Explain result | The app labels a demonstration range and shows neutral in-range or adjustment feedback. |
| FR-07 | Fail safely | Missing image, cancelled selection, unsupported input, missing landmarks, and invalid geometry never create a score. |
| DV-01 | Desktop concept check | A team member can run one local still image through the independent desktop tool and receive an annotated result or a clear cannot-analyze message. |

## Non-Functional Requirements

- Analysis runs on-device without an account, database, API key, or internet dependency.
- The Android app is demonstrable on a physical device.
- Raw photos, landmarks, and results are not persisted after the current analysis.
- The complete flow is understandable in a two-minute competition video.
- All visible app copy, source comments, documentation, and repository artifacts use English.
- The desktop tool remains local: it makes no server request and only writes an annotated image when the operator explicitly supplies `--output`.

## Out of Scope

- Live camera, video, tracking, ball detection, full-swing scoring, or history, including in the desktop tool.
- Native iOS delivery before Android acceptance.
- Sharing, social features, subscriptions, dashboards, or server-side features.
- Injury or medical claims.

## Acceptance Evidence

1. **Verified on emulator:** Flutter application boots and opens the Android system photo picker.
2. **Verified by tests:** Dart tests cover right, straight, invalid, confidence, and feedback-boundary inputs.
3. **Pending physical device:** One authorized photo reaches the configured in-range result.
4. **Pending physical device:** One authorized photo reaches the configured adjustment result.
5. **Pending physical device:** One unreliable input reaches a clear cannot-analyze state.
6. **Pending submission review:** Overlay, limitations, demo script, attribution, and behavior agree.
7. **Verified desktop prototype:** A fresh ten-photo Commons run with one usable-scale tennis player per image produced eight red adjustment results and two safe cannot-analyze results. This is not evidence that the Flutter/ML Kit path behaves identically.
