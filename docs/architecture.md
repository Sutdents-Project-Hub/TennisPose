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
| Data | Gallery picker and native pose bridge adapters | Persist images or make medical claims |
| Platform | Android/iOS ML Kit and permission configuration | Hold product feedback logic |

## Geometry Contract

For shoulder `S`, elbow `E`, and wrist `W`, calculate the interior elbow angle between `S - E` and `W - E`.

```text
cos(theta) = dot(S - E, W - E) / (norm(S - E) * norm(W - E))
angle = degrees(arccos(clamp(cos(theta), -1, 1)))
```

The domain layer rejects missing, non-finite, low-confidence, or zero-length landmarks. It returns a typed failure rather than an angle when the calculation is not trustworthy.

## Result States

| State | Trigger | App behavior |
|---|---|---|
| Idle | No photo selected | Explain the required photo and permission boundary. |
| Image selected | Valid local image selected | Show preview and side selection. |
| Analyzing | Native bridge running | Disable duplicate actions and show progress. |
| Analyzed | Required landmarks and valid geometry | Show annotated image, angle, range, and feedback. |
| Cannot analyze | Denial, cancellation, unsupported input, missing landmarks, or invalid geometry | Explain the issue and allow a new selection without a score. |

## Android-First Boundary

- The first executable proof is an Android debug build on a physical device.
- iOS is not promised until Android gallery access, native pose detection, and rendering pass the same acceptance cases.
- The bridge must expose the official ML Kit static-image mode. If a package cannot meet that contract, replace it with a maintained adapter or documented platform channel before feature expansion.

## Data Boundary

- Photo bytes, landmarks, and results stay in memory for the active analysis.
- No image, result, account, analytics event, database record, or remote API is part of this design.
- Cloud upload, history, sharing, or remote AI is an architecture and privacy scope change requiring explicit approval.
