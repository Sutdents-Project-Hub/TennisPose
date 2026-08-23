# Security and Privacy Plan

## Risk Context

The Android-first MVP has no login, payment, database, cloud API, or remote storage. Its main risk is a selected photo that may contain an identifiable person.

## Required Protections

- Before selection, tell the user to choose only photos they own or are authorized to use.
- Request only the image-access permission needed for the platform picker flow.
- Keep image bytes, landmarks, and results in memory for current analysis only.
- Do not transmit or persist photos, landmarks, or results.
- Do not commit real test photos, device identifiers, screenshots containing personal data, or private evaluator notes.
- Do not create an API key or `.env` requirement for the MVP.

## Responsible Product Language

- Use "demonstration range", "in range", "adjustment suggested", and "cannot analyze" rather than medical or safety claims.
- Explain that image quality, viewpoint, occlusion, clothing, orientation, and landmark confidence can affect the result.
- Keep feedback wording aligned with the actual angle rule and evidence source.

## Scope-Change Trigger

Cloud upload, result history, sharing, sign-in, telemetry, or public deployment moves the project into a higher-risk state. Before such work, define consent, access control, retention, deletion, incident response, and deployment ownership.
