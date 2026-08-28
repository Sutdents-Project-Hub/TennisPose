# Project Profile

| Field | Value |
|---|---|
| Project | TennisPose - AI Tennis Trophy Pose Coach |
| Repository | `TennisPose` |
| Project slug | `tennispose` |
| Stage | Competition MVP |
| Product type | Native mobile application with a local desktop algorithm-validation tool |
| Primary platform | Android physical device |
| Follow-up platform | iOS after Android validation |
| Framework | Flutter and Dart |
| Bootstrap status | Executable Flutter MVP |
| Deployment | Not planned |

## Product Statement

TennisPose lets a learner inspect one Trophy Pose photo on a mobile device. The app finds local pose landmarks, measures the chosen arm's elbow angle, and makes its red or green feedback visible and explainable.

## Explicit Technology Exception

Flutter is selected instead of the default React Native with Expo because the project needs a genuine installed app, a custom image overlay, Android-first device testing, and an on-device pose boundary without a Python or cloud backend.

The app uses Google ML Kit's native pose SDK through `google_mlkit_pose_detection` 0.15.0. The bridge runs accurate single-image detection through platform channels and returns landmarks to pure Dart domain logic.

The user-approved `tools/desktop_demo/` exception uses Python 3.11, MediaPipe Tasks, and OpenCV as a local-only still-image prototype. It exists to validate and record the geometry concept without a mobile frontend. It is not a backend, web service, or replacement for Flutter/ML Kit device evidence.

## Constraints

- One JPEG or PNG still image, one Trophy Pose, and one user-selected arm side.
- No video, backend, account, database, cloud storage, or remote AI. The desktop tool remains a one-image local runner with no camera stream.
- Local in-memory processing only.
- No medical, injury-prevention, rehabilitation, or professional coaching claim.
- Native Android-first MVP target: 16 to 20 hours.

## Verified Technical Baseline

- Flutter 3.41.9 and Dart 3.11.5.
- Android minSdk 23 and a successful Android debug APK build.
- Android 36 emulator launch, layout inspection, system picker launch, and cancellation handling.
- iOS 15.5 configuration and a successful iOS simulator debug build, with ML Kit simulator architecture warnings.
- Python 3.11 desktop tool geometry tests and a ten-photo local Commons run: eight analyzed adjustments and two safe cannot-analyze results.

## Open Decisions

- Coach validation or replacement of the configurable 90-105 degree demonstration range.
- Physical Android verification with authorized in-range, adjustment, and unsuitable photos.
- Current competition requirements, asset policy, attribution, and project license.
