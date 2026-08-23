# AI, Native Bridge, and Dependency Plan

## Native Pose Strategy

The selected direction is Flutter plus the official Google ML Kit Pose Detection SDK on Android and iOS. The product only needs a still photo, so the adapter must expose ML Kit static-image mode rather than a video-tracking flow.

The official native SDK is documented as beta. The project must prove the final SDK version, Flutter bridge, permissions, image conversion, and result mapping on a real Android device before treating the integration as ready.

## Planned Dependency Categories

| Category | Intended role | Current status |
|---|---|---|
| Flutter SDK | Native app framework and Dart runtime | Not verified in this repository |
| Gallery picker package | Local image selection | Candidate not selected |
| ML Kit bridge | Flutter-to-native pose detector adapter | Candidate not selected; device spike required |
| Flutter rendering | `CustomPainter` image overlay | Framework capability planned |
| Test and lint tooling | `flutter test` and `flutter analyze` | Planned; commands not verified |

## Bridge Selection Rule

Prefer a maintained Flutter bridge that exposes static-image landmarks, confidence data, Android/iOS configuration, and a compatible license. Validate it with the Android device spike before product UI work. If no bridge satisfies that contract, use a minimal, documented platform channel to the official ML Kit SDK rather than changing the product to a cloud service.

## Official References to Verify During Bootstrap

- Flutter mobile application setup: https://docs.flutter.dev/
- ML Kit Pose Detection for Android: https://developers.google.com/ml-kit/vision/pose-detection/android
- ML Kit Pose Detection for iOS: https://developers.google.com/ml-kit/vision/pose-detection/ios

No LLM, remote computer-vision API, analytics SDK, identity provider, payment service, or API key is in scope. Adding any of these changes privacy, cost, reliability, and competition disclosure requirements.
