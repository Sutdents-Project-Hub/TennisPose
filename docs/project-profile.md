# Project Profile

| Field | Value |
|---|---|
| Project | TennisPose - AI Tennis Trophy Pose Coach |
| Repository | `TennisPose` |
| Project slug | `tennispose` |
| Stage | Competition MVP |
| Product type | Native mobile application |
| Primary platform | Android physical device |
| Follow-up platform | iOS after Android validation |
| Framework | Flutter and Dart |
| Bootstrap status | Documentation scaffold only |
| Deployment | Not planned |

## Product Statement

TennisPose lets a learner inspect one Trophy Pose photo on a mobile device. The app finds local pose landmarks, measures the chosen arm's elbow angle, and makes its red or green feedback visible and explainable.

## Explicit Technology Exception

Flutter is selected instead of the default React Native with Expo because the project needs a genuine installed app, a custom image overlay, Android-first device testing, and an on-device pose boundary without a Python or cloud backend.

The plan uses the official ML Kit native pose SDK behind a Flutter adapter. The adapter implementation and final package versions are not selected or verified yet.

## Constraints

- One JPEG or PNG still image, one Trophy Pose, and one user-selected arm side.
- No video, backend, account, database, cloud storage, or remote AI.
- Local in-memory processing only.
- No medical, injury-prevention, rehabilitation, or professional coaching claim.
- Native Android-first MVP target: 16 to 20 hours.

## Open Decisions

- Flutter and Dart versions, native SDK versions, bridge strategy, and platform permissions.
- Final angle range, source, viewpoint, and feedback wording.
- Current competition requirements, asset policy, attribution, and project license.
