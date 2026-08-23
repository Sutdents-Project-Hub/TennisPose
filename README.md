# TennisPose - AI Tennis Trophy Pose Coach

> Stage: competition MVP | Product: native mobile app | Primary platform: Android | Deployment: not planned

## Product

TennisPose is a Flutter mobile app that analyzes one tennis serve Trophy Pose photo. A user selects a side-view image from a phone, chooses an arm to inspect, and receives an annotated elbow-angle result with explainable red or green feedback.

It is deliberately a single-photo coaching aid, not a live-video coach, full-swing tracker, injury-prevention system, or medical product.

## Technology Decision

The app will use **Flutter and Dart** rather than Streamlit or React Native. Flutter delivers a genuine Android and iOS application from one codebase. The MVP is Android-first: gallery selection, on-device pose detection, overlay rendering, and the real-device demo must work on Android before iOS work begins.

Pose landmarks will come from the official Google ML Kit Pose Detection SDK through a Flutter adapter. Static-image detection is a direct match for this product, but the native SDK is beta. The bridge, device configuration, and final package versions remain unverified until a physical-device spike passes.

## MVP User Flow

1. Read a short privacy and photo-permission notice.
2. Select one authorized JPEG or PNG from the phone gallery.
3. Choose the left or right arm to inspect.
4. Run on-device pose detection and validate shoulder, elbow, and wrist landmarks.
5. Draw arm segments and elbow angle over a copy of the photo.
6. Show an in-range, adjustment-suggested, or cannot-analyze result.

## Scope

### Included

- One still gallery image, one Trophy Pose, and one selected arm side.
- On-device pose landmarks and pure Dart elbow-angle geometry.
- Annotated result image, transparent feedback, and safe failure states.

### Excluded

- Live camera, video, tracking, ball detection, full-swing analysis, or history.
- Accounts, database, cloud storage, sharing, payment, or a custom backend.
- Remote AI, API keys, medical claims, or app-store release in this MVP.

## Planned Technology

| Responsibility | Planned choice | Status |
|---|---|---|
| Native UI | Flutter and Dart | Planned; no Flutter project exists yet |
| Image selection | Flutter gallery picker | Candidate; package and permissions unverified |
| Pose landmarks | Official ML Kit SDK through a Flutter adapter | Planned; bridge unverified |
| Angle math | Pure Dart vectors and trigonometry | Planned |
| Overlay | Flutter `CustomPainter` | Planned |
| Quality checks | `flutter analyze` and `flutter test` | Planned; not yet available |

## Planned Layout

```text
app/
  pubspec.yaml
  lib/
    main.dart
    features/pose_analysis/
      presentation/
      domain/
      data/
  test/
  android/
  ios/
docs/
```

Only `app/README.md` and documentation exist today. No Flutter manifest, Dart code, device build, or dependency has been created.

## Delivery Plan

The Android-first native MVP is planned for **16 to 20 hours**. This is longer than the earlier web plan because it includes Flutter bootstrap, native permissions, the pose bridge, and physical-device verification.

See [the roadmap and test plan](docs/mvp-plan.md), [the architecture](docs/architecture.md), and [the competition plan](docs/competition.md).

## Documentation

- [Project profile](docs/project-profile.md)
- [Product requirements](docs/project-overview.md)
- [Solution architecture](docs/architecture.md)
- [MVP roadmap and test plan](docs/mvp-plan.md)
- [Competition plan](docs/competition.md)
- [Data and storage boundary](docs/data-and-storage.md)
- [AI, native bridge, and dependency plan](docs/integrations.md)
- [Security and privacy plan](docs/security-and-privacy.md)
- [Mobile app component contract](app/README.md)
- [Repository working rules](AGENTS.md)

## License and Attribution

No license has been selected. Confirm ownership and attribution for source code, demo photos, Flutter, ML Kit, bridge packages, icons, and other assets before public release or submission.
