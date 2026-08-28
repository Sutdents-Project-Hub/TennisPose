# Competition Demo and Submission Plan

## Target

The expected target is the Congressional App Challenge or another confirmed student-app competition. This repository does not verify current eligibility, deadline, submission fields, video duration, repository visibility, or whether a locally served web application is accepted. Confirm those facts from the organizer's official source before submitting.

## Demo Narrative

Tennis learners may have a serve photo but no immediate visual explanation of one key Trophy Pose arm angle. TennisPose accepts one local image, finds the racket arm, draws the relevant landmarks, calculates the elbow angle in 3D, and shows transparent demonstration feedback.

The claim is limited to a photo-based configurable demonstration range. The app does not diagnose injury, certify a serve, or replace a coach.

## Two-Minute Local Web-App Demo

| Time | Content |
|---:|---|
| 0:00-0:20 | Explain the learner problem, single-photo scope, and local Streamlit delivery. |
| 0:20-0:45 | Upload an authorized adjustment-case photo and show overlay, angle, and red feedback. |
| 0:45-1:10 | Upload an authorized in-range photo and show the same local calculation with green feedback. |
| 1:10-1:35 | Open "How this number was measured": the shoulder-elbow-wrist geometry, the 3D reading beside the flat 2D one, the three pooled passes, and local CPU processing. |
| 1:35-1:50 | Upload a photo that is not a trophy position and show the app refusing with a reason instead of inventing a score. |
| 1:50-2:00 | State privacy handling, viewpoint limitations, and the coach/medical boundary. |

The strongest algorithm moment is the 3D-versus-2D comparison. On the reference
trophy photos the flat image-plane angle reads 33 and 43 degrees where the arms
are actually near 83 and 101, because a serve points the racket arm at the
camera. Showing that gap explains why the depth-aware landmarks are used and why
the geometry is not a cosmetic detail.

Record the local browser run as the delivered product. Do not portray it as a mobile application, native app, cloud service, or real-time video coach.

## Evidence and Asset Rules

- Use only team-created photos, separately authorized assets, or the licensed public reference set documented in [`demo-assets/README.md`](demo-assets/README.md) for competition and public demonstration.
- Record Python, Streamlit, MediaPipe, model, image, icon, font, and code attribution before submission.
- Do not include private images, personal data, secrets, contracts, or unlicensed media in the repository or recording.
- A recorded fallback is allowed only when clearly labelled as recorded evidence, not represented as a live run.
- Any sample photo used in a public video must have verified permission, required attribution, and a scope-compatible caption. The versioned reference photos and annotated results retain their upstream Creative Commons terms; include the matching attribution when used outside this repository.

## Submission Checklist

- [ ] Official rules, deadline, format, repository visibility, and web-app expectations have been verified.
- [ ] The local Streamlit recording matches the current code and documented scope.
- [ ] Green, red, invalid-upload, not-a-trophy-position, and cannot-analyze paths are demonstrated.
- [ ] Python dependencies, the MediaPipe model, and assets have complete attribution and license review.
- [ ] The specific reference-photo attribution is shown or linked whenever a versioned demo asset appears in a public recording.
- [ ] Documentation contains no unsupported accuracy, injury, medical, deployment, or competition-compliance claim.
- [ ] No secrets, private photos, personal data, contracts, or confidential documents are included.
