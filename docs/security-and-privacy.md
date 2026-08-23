# Security and Privacy Boundary

## Risk Context

The Android-first MVP has no login, payment, database, cloud API, or remote storage. Its main risk is a selected photo that may contain an identifiable person.

## Required Protections

- The app explains local processing before selection; competition operators must use only photos they own or are authorized to use.
- The implementation uses the platform gallery picker and configures the iOS photo-library purpose string. Android uses the current system picker flow without a broad storage permission.
- Keep decoded image data, landmarks, and results in memory for the current analysis only. The selected source image remains under the platform picker and device file lifecycle.
- Do not transmit photos, landmarks, or results, and do not create app-controlled analysis history.
- Do not commit real test photos, device identifiers, screenshots containing personal data, or private evaluator notes.
- Do not create an API key or `.env` requirement for the MVP.

## Responsible Product Language

- Use "demonstration range", "in range", "adjustment suggested", and "cannot analyze" rather than medical or safety claims.
- Explain that image quality, viewpoint, occlusion, clothing, orientation, and landmark confidence can affect the result.
- Keep feedback wording aligned with the actual angle rule and evidence source.

## Scope-Change Trigger

Cloud upload, result history, sharing, sign-in, telemetry, or public deployment moves the project into a higher-risk state. Before such work, define consent, access control, retention, deletion, incident response, and deployment ownership.
