# Native MVP Roadmap and Test Plan

## Definition of Done

The MVP is complete when a reviewer can run a Flutter Android debug build on a physical phone, select an authorized Trophy Pose photo, see an annotated elbow-angle result for two distinct examples, and receive a safe cannot-analyze response for unreliable input.

The software MVP is implemented and buildable. Competition acceptance remains open until the physical-device photo cases and submission evidence are completed; an emulator-only screen is not treated as that evidence.

## Delivery Plan

| Phase | Status | Exit evidence |
|---|---|---|
| 0. Flutter bootstrap | Complete | Official Flutter project exists directly in `app/`; Android and iOS targets compile. |
| 1. Emulator device spike | Complete | Android 36 launch, UI inspection, photo-picker launch, and safe cancellation verified. |
| 2. Domain and tests | Complete | 8 tests cover geometry, invalid inputs, confidence, feedback boundaries, and the idle screen. |
| 2.5. Desktop algorithm check | Complete | Python geometry tests passed; a local ten-photo still-image MediaPipe run produced eight annotated adjustment results and two safe cannot-analyze results. |
| 3. Mobile UI and overlay | Implemented | Focused page, arm selector, progress/failure states, `CustomPainter`, and result card compile and pass analysis. |
| 4. Physical Android acceptance | Pending | Authorized in-range, adjustment, and unsuitable photos must verify ML Kit results and overlay alignment. |
| 5. Competition evidence | Pending | Prepare authorized photos, record the two-minute device demo, and record limitations. |
| 6. Submission check | Pending | Reconcile official rules, attribution, license, repository visibility, and final materials. |

The coding baseline is complete. Remaining time depends on physical-device photo preparation, result tuning, recording, and the competition submission review. iOS runtime acceptance remains a follow-up.

## Test Matrix

| Case | Expected result | Evidence |
|---|---|---|
| Right and straight point sets | Correct angles within tolerance | Passed in `flutter test` |
| Duplicate, zero-length, or non-finite points | Typed invalid result; no crash | Passed in `flutter test` |
| Confidence threshold and feedback boundaries | Deterministic validation and inclusive range | Passed in `flutter test` |
| No image | Clear instruction and one primary action | Verified on Android 36 emulator |
| Picker launch and cancellation | System picker opens; safe inline return message | Verified on Android 36 emulator |
| Clear one-person side-view photo | Overlay, angle, and configured result | Pending physical Android device |
| Blurry, occluded, or unsuitable photo | Cannot-analyze state; no score | Pending physical Android device |
| In-range and adjustment examples | Separate green and red flows | Pending real-device recording |
| Ten local usable-scale tennis-serve images, selected right arm | Annotation/angle or cannot-analyze with no network call | Verified on August 28, 2026: eight adjustment results and two cannot-analyze results; does not substitute for ML Kit device evidence |

## Competition Demo Script

1. State the learner problem and the deliberate single-photo scope.
2. Select the adjustment-case image and explain its overlay, angle, and red result.
3. Select the in-range image and show the same transparent calculation path.
4. Explain that the elbow angle comes from three visible landmarks, not an unexplained score.
5. State limits: still image, viewpoint sensitivity, one pose, local processing, and no medical claim.

## Verification Record

- `flutter analyze`: passed with no issues on August 23, 2026.
- `flutter test`: all 8 tests passed on August 23, 2026.
- `flutter build apk --debug`: succeeded; the ignored APK is under `app/build/`.
- Android 36 emulator: app foreground launch, visual layout, system picker handoff, and cancellation state verified.
- `flutter build ios --simulator --debug --no-codesign`: succeeded with native ML Kit simulator architecture warnings.
- `python -m unittest tools/desktop_demo/test_pose_math.py`: 5 tests passed on August 28, 2026.
- Desktop MediaPipe prototype: a new ten-photo Commons run chose photos with one tennis player at a usable scale. It returned eight annotated adjustment results and two safe cannot-analyze results. Results and source records are local test artifacts only.
