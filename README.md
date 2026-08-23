# TennisPose - AI Tennis Trophy Pose Coach

> Stage: competition MVP | Product: native mobile app | Primary platform: Android | Deployment: none

TennisPose analyzes one tennis serve Trophy Pose photo on-device. The user selects a side-view image, chooses the left or right arm, and receives an annotated elbow angle with explainable green or red feedback.

It is deliberately a single-photo learning aid. It is not a live-video coach, full-swing tracker, injury-prevention system, or medical product.

## Implemented MVP

- Android and iOS Flutter project generated directly in `app/` with no nested repository.
- Android system photo picker with cancellation and readable failure handling.
- Left/right arm selection.
- Static-image pose detection through Google ML Kit's native SDK and a Flutter platform-channel adapter.
- Shoulder, elbow, and wrist confidence validation before any score is shown.
- Pure Dart elbow-angle geometry and a configurable 90-105 degree demonstration rule.
- `CustomPainter` overlay with landmarks, arm segments, angle label, and green/red status.
- Focused idle, selected, analyzing, analyzed, and cannot-analyze states.
- No account, backend, database, cloud upload, remote AI, API key, or saved history.

## Technology

| Responsibility | Implementation |
|---|---|
| App framework | Flutter 3.41.9 and Dart 3.11.5 |
| Gallery selection | `image_picker` 1.2.3 |
| Pose landmarks | `google_mlkit_pose_detection` 0.15.0 in accurate, single-image mode |
| Angle math | Pure Dart vectors, dot product, and trigonometry |
| Overlay | Flutter `CustomPainter` |
| Android baseline | minSdk 23; app ID `com.studentsprojecthub.tennispose` |
| iOS baseline | iOS 15.5; photo-library purpose string configured |

The Flutter package is a community bridge to the native Google ML Kit SDK, not an official Google Flutter plugin. The native pose API is processed locally and remains subject to the SDK and bridge limitations documented in [integrations](docs/integrations.md).

## Run Locally

Prerequisites: Flutter 3.41.9 or a compatible stable release, Dart 3.11.5 or compatible, and an Android SDK/toolchain.

```bash
cd app
flutter pub get
flutter run
```

Choose an Android device for the primary MVP flow. Use only a photo you own or are authorized to analyze.

## Verify

```bash
cd app
flutter analyze
flutter test
flutter build apk --debug
flutter build ios --simulator --debug --no-codesign
```

Verified on August 23, 2026:

- `flutter analyze`: no issues.
- `flutter test`: 8 tests passed.
- Android debug APK: built at `app/build/app/outputs/flutter-apk/app-debug.apk`.
- Android 36 emulator: app launched, layout inspected, system photo picker opened, and cancellation returned a safe message.
- iOS simulator debug build: compiled successfully. ML Kit reported simulator architecture warnings, so iOS runtime behavior is not accepted yet.

Still required for competition acceptance: run pose detection with authorized in-range, adjustment, and unsuitable photos on a physical Android device and record the results. An emulator-only run is not treated as physical-device evidence.

## Repository Layout

```text
app/
  android/
  ios/
  lib/
    main.dart
    features/pose_analysis/
      data/
      domain/
      presentation/
  test/
  pubspec.yaml
  pubspec.lock
docs/
```

## Documentation

- [Project profile](docs/project-profile.md)
- [Product requirements](docs/project-overview.md)
- [Solution architecture](docs/architecture.md)
- [MVP roadmap and test evidence](docs/mvp-plan.md)
- [Competition plan](docs/competition.md)
- [Data and storage boundary](docs/data-and-storage.md)
- [Native bridge and dependency notes](docs/integrations.md)
- [Security and privacy](docs/security-and-privacy.md)
- [Mobile app component guide](app/README.md)
- [Repository working rules](AGENTS.md)

## License and Attribution

No project license has been selected. Confirm source-code ownership, dependency licenses, demo-photo consent, asset attribution, and competition rules before public submission or release.
