# Flutter Mobile Application

`app/` is the complete Flutter project root for TennisPose. It contains the shared Dart application, Android and iOS platform projects, tests, gallery selection, on-device pose integration, angle logic, and result overlay.

## Module Boundaries

```text
lib/
  main.dart
  features/pose_analysis/
    data/
      ml_kit_pose_analyzer.dart
    domain/
      pose_analysis.dart
    presentation/
      pose_analysis_page.dart
      result_overlay_painter.dart
```

- `presentation/` owns UI state, gallery interaction, error messages, and painting.
- `domain/` owns plugin-free points, angle geometry, result types, and the feedback rule.
- `data/` maps native ML Kit poses into validated domain landmarks.

## Commands

```bash
flutter pub get
flutter run
flutter analyze
flutter test
flutter build apk --debug
```

The primary acceptance target is an Android physical device. An iOS simulator debug build is available through:

```bash
flutter build ios --simulator --debug --no-codesign
```

## Platform Configuration

- Android application ID: `com.studentsprojecthub.tennispose`
- Android minSdk: 23
- iOS deployment target: 15.5
- iOS photo-library usage description: configured in `ios/Runner/Info.plist`
- Release signing: intentionally not configured
- Environment variables: none

## Verified State

On August 23, 2026, static analysis passed with no issues, all 8 tests passed, the Android debug APK built, the app launched on an Android 36 emulator, and the system picker cancellation flow returned safely. The iOS simulator debug target also compiled, with native ML Kit architecture warnings.

Physical Android pose detection with authorized photos remains the final device acceptance gate. Do not describe the app as medically validated or professionally calibrated.
