# Solution Architecture

## Delivery Model

TennisPose is a single Flutter mobile application. It reads a gallery image, runs pose inference on-device through a native ML Kit bridge, calculates an elbow angle in pure Dart, and renders the result with Flutter. No server call is required.

```text
Android device
  -> Flutter page and gallery picker
  -> local image bytes
  -> Flutter native adapter
  -> official ML Kit Pose Detection SDK
  -> shoulder, elbow, wrist validation
  -> pure Dart angle calculation
  -> Flutter CustomPainter overlay
  -> result state and feedback UI
```

## Module Boundaries

| Layer | Responsibility | Must not do |
|---|---|---|
| Presentation | Page layout, side choice, loading/error state, image display, `CustomPainter` | Call ML Kit directly or decide geometry |
| Domain | Point validation, angle calculation, result state, feedback rule | Access plugins or device permissions |
| Data | Native pose bridge adapter and landmark mapping | Persist images or make medical claims |
| Platform | Android/iOS ML Kit and permission configuration | Hold product feedback logic |

## Geometry Contract

For shoulder `S`, elbow `E`, and wrist `W`, calculate the interior elbow angle between `S - E` and `W - E`.

```text
cos(theta) = dot(S - E, W - E) / (norm(S - E) * norm(W - E))
angle = degrees(arccos(clamp(cos(theta), -1, 1)))
```

The data layer rejects missing or below-threshold landmarks at a minimum confidence of 0.55. The domain layer rejects non-finite or zero-length geometry. Both paths return a typed failure rather than an angle when the calculation is not trustworthy.

## Result States

| State | Trigger | App behavior |
|---|---|---|
| Idle | No photo selected | Explain the required photo and permission boundary. |
| Image selected | Valid local image selected | Show preview and side selection. |
| Analyzing | Native bridge running | Disable duplicate actions and show progress. |
| Analyzed | Required landmarks and valid geometry | Show annotated image, angle, range, and feedback. |
| Cannot analyze | Denial, cancellation, unsupported input, missing landmarks, or invalid geometry | Explain the issue and allow a new selection without a score. |

## Implemented Modules

| Path | Responsibility |
|---|---|
| `presentation/pose_analysis_page.dart` | Gallery selection, arm choice, app states, and user-facing recovery. |
| `presentation/result_overlay_painter.dart` | Image rendering, coordinate scaling, arm segments, points, and angle label. |
| `domain/pose_analysis.dart` | Pure Dart models, confidence contract, angle calculation, and feedback rule. |
| `data/ml_kit_pose_analyzer.dart` | Accurate single-image ML Kit detector and landmark mapping. |

## Android-First Boundary

- The Android debug build and Android 36 emulator launch are verified.
- The emulator verified layout, system picker launch, and safe picker cancellation.
- A physical Android device with authorized in-range, adjustment, and unsuitable photos is still required to accept native pose behavior and overlay alignment.
- iOS simulator debug compilation is verified, but ML Kit emitted simulator architecture warnings; iOS runtime acceptance remains a follow-up.

## Data Boundary

- Photo bytes, landmarks, and results stay in memory for the active analysis.
- No image, result, account, analytics event, database record, or remote API is part of this design.
- Cloud upload, history, sharing, or remote AI is an architecture and privacy scope change requiring explicit approval.
