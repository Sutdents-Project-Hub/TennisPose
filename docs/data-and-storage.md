# Data and Storage Boundary

## MVP Data Contract

| Data | Source | Processing | Persistence |
|---|---|---|---|
| Selected photo | Authorized phone-gallery JPEG or PNG | In-memory decode, local pose detection, overlay rendering | None |
| Pose landmarks | Native ML Kit result for current image | In-memory validation and angle calculation | None |
| Angle and feedback | Pure Dart domain logic | Visible in current result state | None |
| Demo assets | Team-controlled local photos | Permission review before recording | Do not commit without documented public-use approval |

## Rules

- The MVP has no database, account, analytics pipeline, upload bucket, cache, or result history.
- Do not write photos, landmark coordinates, or results to logs, test fixtures, screenshots, temporary folders, or Git.
- `uploads/` and `data/private/` remain ignored as a defensive rule, not as an approved storage design.
- A feature that saves, shares, uploads, or synchronizes a photo requires new consent, retention, deletion, access-control, and backup design.

## Asset Review

For each demo image, record ownership, subject consent, competition permission, and whether public repository or video use is allowed.
