# Competition Demo and Submission Plan

## Target

The expected target is the Congressional App Challenge or another confirmed student-app competition. This repository does not verify current eligibility, deadline, submission fields, video duration, repository visibility, or platform requirements. Confirm them from the organizer's official source before submitting.

## Demo Narrative

Tennis learners may not have instant coaching feedback. TennisPose gives a transparent first look at one Trophy Pose photo: it shows the relevant arm landmarks, calculates an elbow angle locally on the phone, and explains the displayed result.

The claim is limited to visualizing a photo-based demonstration range. The app does not diagnose injury, certify a serve, or replace a coach.

## Two-Minute Mobile Demo

| Time | Content |
|---:|---|
| 0:00-0:20 | Learner problem, Android-first decision, and single-photo boundary. |
| 0:20-0:50 | Select an authorized adjustment-case photo and show overlay, angle, and red feedback. |
| 0:50-1:20 | Select an authorized in-range photo and show the same local calculation with green feedback. |
| 1:20-1:40 | Explain shoulder-elbow-wrist geometry and on-device processing. |
| 1:40-2:00 | State privacy handling, limits, and the role of a coach for meaningful advice. |

## Desktop Prototype Recording

Before mobile-device acceptance, the team may record `tools/desktop_demo/` as an algorithm prototype: open one authorized still image, show the annotated arm and reported angle, then show a cannot-analyze case. Label this honestly as a local MediaPipe desktop prototype. It does not demonstrate the delivered Flutter/ML Kit path and must not be presented as a mobile app run.

## Evidence and Asset Rules

- Use only team-created photos or assets with documented permission for competition and public demonstration.
- Record package, native SDK, bridge, image, icon, font, and code attribution before submission.
- Do not include private images, personal data, secrets, contracts, or unlicensed media in the repository or recording.
- A recorded fallback is allowed only when clearly labelled as recorded evidence, not represented as a live run.
- Commons test photos are local prototype inputs only. The final public recording should use team-owned or separately authorized images with source and attribution records.

## Submission Checklist

- [ ] Official rules, deadline, format, repository visibility, and platform expectations have been verified.
- [ ] The real-device recording matches the current code and documented scope.
- [ ] Green, red, cancellation/permission, and cannot-analyze paths are demonstrated.
- [ ] Flutter, ML Kit, bridge packages, and assets have complete attribution and license review.
- [ ] Documentation contains no unsupported accuracy, injury, medical, or competition-compliance claim.
- [ ] No secrets, private photos, personal data, contracts, or confidential documents are included.
