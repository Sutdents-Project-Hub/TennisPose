# Security and Privacy Boundary

## Risk Context

The local Streamlit MVP has no login, payment, database, cloud API, or remote storage. Its main risk is an uploaded photo that may contain an identifiable person.

## Required Protections

- The page explains local processing before upload; competition operators must use only photos they own or are authorized to use.
- Run the application locally. Do not expose it through a public URL, tunnel, or shared server without a separate security and privacy review.
- Keep uploaded image bytes, decoded image data, landmarks, and results in the active local session only.
- Recheck JPEG/PNG content after upload and reject files above 10 MB or 20 megapixels before full image conversion.
- Do not transmit photos, landmarks, or results, and do not create analysis history, logs, or saved result files.
- Do not commit real test photos, screenshots containing personal data, private evaluator notes, downloaded model binaries, device identifiers, or secrets.
- Do not create an API key or `.env` requirement for the MVP.

## Responsible Product Language

- Use "demonstration range", "in range", "adjustment suggested", and "cannot analyze" rather than medical or safety claims.
- Explain that image quality, viewpoint, occlusion, clothing, orientation, framing, and landmark confidence can affect the result.
- Keep feedback wording aligned with the actual angle rule and evidence source.

## Scope-Change Trigger

Public deployment, cloud upload, result history, sharing, sign-in, telemetry, camera input, or video processing moves the project into a higher-risk state. Before such work, define consent, access control, retention, deletion, incident response, and deployment ownership.
