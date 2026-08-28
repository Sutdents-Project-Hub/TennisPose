# AI, Native Bridge, and Dependencies

## Native Pose Strategy

The implementation uses Flutter plus the native Google ML Kit Pose Detection SDK on Android and iOS. The Flutter package is a community-maintained platform-channel bridge; it is not an official Google Flutter plugin.

`MlKitPoseAnalyzer` selects the accurate model and single-image mode. It chooses the detected pose with the strongest minimum confidence across the selected shoulder, elbow, and wrist, requires a confidence of at least 0.55 for all three, and returns a typed failure otherwise.

## Resolved Dependencies

| Category | Version | Role and verification |
|---|---|---|
| Flutter / Dart | 3.41.9 / 3.11.5 | Framework and runtime; analyze, test, Android build, and iOS simulator debug build verified. |
| `image_picker` | 1.2.3 | Local image selection; Android system picker launch and cancellation verified on emulator. |
| `google_mlkit_pose_detection` | 0.15.0 | Platform-channel bridge to native static-image pose detection; compilation verified, physical-photo result pending. |
| `google_mlkit_commons` | 0.12.0 transitive | Native input-image bridge used by the pose package. |
| Flutter rendering | SDK | `CustomPainter` overlay implemented and compiled. |
| `flutter_lints` | 6.0.0 | `flutter analyze` passed with no issues. |
| MediaPipe Tasks desktop prototype | 0.10.35 | Local single-image PoseLandmarker used only by `tools/desktop_demo/`; a ten-photo run returned eight annotated results and two safe cannot-analyze responses. |
| OpenCV Contrib desktop prototype | 5.0.0.93 | Local preview window and annotated-file rendering for the desktop tool. |
| NumPy desktop prototype | 2.4.6 | Desktop tool dependency. |

## Platform Notes

- Android minSdk is 23. The Android debug APK builds and launches on an Android 36 emulator.
- iOS minimum deployment target is 15.5 and the required photo-library purpose string is configured.
- The iOS simulator debug build succeeds, but native ML Kit dependencies report Apple Silicon simulator architecture warnings. Treat iOS runtime as unaccepted until device testing.
- ML Kit pose detection remains subject to native SDK accuracy, viewpoint, occlusion, and beta/API limitations.
- If the bridge becomes unmaintained or fails the physical-device gate, replace it with a documented minimal platform channel rather than introducing cloud processing.
- The desktop tool downloads the official MediaPipe heavy pose-landmarker model to an ignored local path and explicitly uses the CPU delegate for its single-image workflow. It makes no automatic network request at analysis time. MediaPipe is an independent prototype engine, not a replacement for the Flutter ML Kit bridge; inspect model terms before redistributing it.

## Primary References

- Flutter mobile application setup: https://docs.flutter.dev/
- ML Kit Pose Detection for Android: https://developers.google.com/ml-kit/vision/pose-detection/android
- ML Kit Pose Detection for iOS: https://developers.google.com/ml-kit/vision/pose-detection/ios

No LLM, remote computer-vision API, analytics SDK, identity provider, payment service, or API key is present. Adding any of these changes privacy, cost, reliability, and competition disclosure requirements.
