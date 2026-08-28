# Data and Storage Boundary

## MVP Data Contract

| Data | Source | Processing | Persistence |
|---|---|---|---|
| Selected photo | Authorized phone-gallery image selected through the platform picker | Local file-path handoff, in-memory decode, local pose detection, overlay rendering | No app-controlled record; the OS or picker plugin may manage a temporary local copy |
| Pose landmarks | Native ML Kit result for current image | In-memory validation and angle calculation | None |
| Angle and feedback | Pure Dart domain logic | Visible in current result state | None |
| Demo assets | Team-controlled local photos | Permission review before recording | Do not commit without documented public-use approval |
| Desktop prototype input | Operator-selected local JPEG or PNG | Local MediaPipe analysis and OpenCV annotation | No copied source file; optional annotated result only at the operator's explicit `--output` path |
| Desktop PoseLandmarker model | Official model download | Local model inference | Ignored local dependency; not user data |

## Rules

- The MVP has no database, account, analytics pipeline, upload bucket, app-managed cache, or result history.
- The app does not deliberately copy or retain the selected photo. The platform picker may provide a temporary local file governed by the operating system and plugin lifecycle.
- The mobile app must not write photos, landmark coordinates, or results to logs, test fixtures, screenshots, temporary folders, or Git. The desktop runner may write only its rendered annotation to an explicit operator-selected output path; it does not write raw photo copies or landmark-coordinate files.
- `uploads/` and `data/private/` remain ignored as a defensive rule, not as an approved storage design.
- The local Desktop test folder and `tools/desktop_demo/models/` are excluded from Git. Do not move test photos, annotated examples, or model binaries into tracked paths.
- A feature that saves, shares, uploads, or synchronizes a photo requires new consent, retention, deletion, access-control, and backup design.

## Asset Review

For each demo image, record ownership, subject consent, competition permission, and whether public repository or video use is allowed.
