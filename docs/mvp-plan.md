# Native MVP Roadmap and Test Plan

## Definition of Done

The MVP is complete when a reviewer can run a Flutter Android debug build on a physical phone, select an authorized Trophy Pose photo, see an annotated elbow-angle result for two distinct examples, and receive a safe cannot-analyze response for unreliable input.

Documentation, an emulator-only screen, or a successful Flutter scaffold is not enough.

## Delivery Plan

| Phase | Estimate | Work | Exit evidence |
|---|---:|---|---|
| 0. Flutter bootstrap | 2 hours | Create the official Flutter project directly in `app/`, verify tooling, and record actual commands. | `pubspec.yaml`, `lib/main.dart`, tests, and Android debug launch exist. |
| 1. Android device spike | 3 hours | Verify gallery selection, cancellation, permission behavior, native pose bridge, and one clear photo. | Physical device returns landmarks or a controlled failure. |
| 2. Domain and tests | 3 hours | Implement pure Dart geometry, result states, feedback rules, and unit tests. | `flutter test` covers normal and invalid cases. |
| 3. Mobile UI and overlay | 4 hours | Build one focused page, side selector, error states, image overlay, and feedback copy. | Real-device flow handles green, red, and cannot-analyze paths. |
| 4. Competition evidence | 2 hours | Prepare authorized photos, record a real-device demo, and record limitations. | Reproducible two-minute demo. |
| 5. Submission check | 2 to 6 hours | Reconcile docs, attribution, privacy, app identity, and official rules. | Submission material agrees with the app; no release is implied. |

Estimated total: **16 to 20 hours** for Android-first MVP. iOS support is a separate follow-up.

## Test Matrix

| Case | Expected result | Evidence |
|---|---|---|
| Right, acute, and obtuse point sets | Correct angles within tolerance | `flutter test` |
| Duplicate, zero-length, NaN, or missing points | Typed invalid result; no crash | `flutter test` |
| No image | Clear instruction | Android manual test |
| Picker cancellation or denied permission | Safe state with message | Android manual test |
| Clear one-person side-view photo | Overlay, angle, and configured result | Android manual test |
| Blurry, occluded, or unsuitable photo | Cannot-analyze state; no score | Android manual test |
| In-range and adjustment examples | Separate green and red flows | Real-device recording |

## Competition Demo Script

1. State the learner problem and the deliberate single-photo scope.
2. Select the adjustment-case image and explain its overlay, angle, and red result.
3. Select the in-range image and show the same transparent calculation path.
4. Explain that the elbow angle comes from three visible landmarks, not an unexplained score.
5. State limits: still image, viewpoint sensitivity, one pose, local processing, and no medical claim.

## Documentation Updates Required During Implementation

- Actual Flutter, Dart, SDK, bridge, and command facts: `README.md` and `app/README.md`.
- Module behavior, platform requirements, and error rules: `docs/architecture.md`.
- Test results and device evidence: this document.
- Demo, asset permissions, sources, and competition rules: `docs/competition.md`.
- Photo handling and native dependency attribution: `docs/data-and-storage.md`, `docs/security-and-privacy.md`, and `docs/integrations.md`.
