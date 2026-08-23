# Flutter Mobile Application

## Responsibility

`app/` will be the complete Flutter project root. It will contain the manifest, Dart source, tests, generated Android and iOS directories, gallery-selection integration, on-device pose bridge, geometry, and overlay UI.

There is no backend or server component. Android is the first acceptance target; iOS is evaluated only after the shared Flutter code works on Android.

## Required Bootstrap Evidence

The future executable skeleton must be created directly in `app/` with Flutter's official initializer. It must contain:

- `app/pubspec.yaml` and `app/pubspec.lock`
- `app/lib/main.dart`
- `app/test/`
- generated `app/android/` and `app/ios/`
- no nested `.git/`

None of this evidence exists yet. Do not create `app/TennisPose/` or `app/flutter/` wrappers.

Flutter's official application template also generates `app/README.md`. During bootstrap, reconcile that generated file with this component contract in the same task; do not discard the documented architecture, safety, or verification boundary just to retain template text.

## Planned Module Boundaries

```text
lib/
  main.dart
  features/pose_analysis/
    presentation/
      pose_analysis_page.dart
      result_overlay_painter.dart
    domain/
      angle_calculator.dart
      analysis_result.dart
      feedback_rule.dart
    data/
      gallery_image_source.dart
      native_pose_detector_adapter.dart
```

- `presentation/` owns widgets, loading/error states, and `CustomPainter`.
- `domain/` is pure Dart and owns no permissions, images, or platform channels.
- `data/` owns gallery and native ML Kit adapter boundaries; it returns typed data or recoverable failures.

## Android Device Spike

Before building product screens, verify on a real Android phone that a Flutter development build installs, gallery selection safely handles cancellation, the chosen bridge returns landmarks for one clear photo, invalid landmarks yield a controlled failure, and package licenses and permissions are recorded.

## Planned Quality Gates

- `flutter analyze`
- `flutter test`
- Android debug build
- Manual Android test for in-range, adjustment, and cannot-analyze results

Record a command and result only after it has actually run. See [the roadmap](../docs/mvp-plan.md).
