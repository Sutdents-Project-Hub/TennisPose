# Repository Working Rules

## Product Context

TennisPose is a competition-stage Flutter mobile app. It analyzes one gallery photo of a tennis serve Trophy Pose, visualizes a shoulder-elbow-wrist angle, and presents transparent red or green feedback.

The MVP is an Android-first native app in `app/`. iOS is a follow-up target after Android physical-device verification. The project has no backend, database, cloud model, account system, or video pipeline.

## Technology Boundary

- Use Flutter and Dart for the UI, state, geometry, and overlay rendering.
- Use the official native ML Kit Pose Detection SDK through a Flutter adapter for on-device landmarks.
- Keep gallery access, pose detection, angle calculation, and rendering inside `app/`.
- Do not add Streamlit, Python, React Native, a web frontend, a backend API, cloud storage, or external AI without explicit approval.
- Keep the selected Flutter bridge behind the data-layer adapter and do not treat native pose behavior as accepted until it passes the physical Android photo cases and license review.

## Scope Guardrails

- Analyze one still image, one Trophy Pose, and one user-selected arm side.
- Do not add live video, continuous tracking, full-swing scoring, injury claims, accounts, sharing, payments, or social features.
- The angle range is a configurable demonstration range until its source and viewpoint are confirmed.
- Required landmarks missing, unreliable, or degenerate means `cannot analyze`; never generate a score from incomplete data.

## Documentation Sources of Truth

- `README.md`: product, stack, scope, and status.
- `docs/project-overview.md`: user needs, acceptance, and exclusions.
- `docs/architecture.md`: Flutter modules, native boundary, geometry, and result states.
- `docs/mvp-plan.md`: milestones, device proof, tests, and delivery evidence.
- `docs/competition.md`: demo, assets, and submission checklist.
- `docs/integrations.md`: ML Kit and Flutter bridge decision record.
- `docs/data-and-storage.md` and `docs/security-and-privacy.md`: photo handling and permissions.
- `app/README.md`: Flutter-root contract.

Documentation synchronization is part of done. Update the document that owns any changed product, architecture, dependency, command, test, privacy, or competition fact in the same task.

## Device and Privacy Rules

- Test a physical Android device before claiming the app works; emulator-only evidence is insufficient for gallery permissions and native pose detection.
- Use only team-owned or authorized photos. Do not persist photo bytes, landmarks, or results.
- Do not commit test photos, personal information, API keys, `.env` files, certificates, contracts, or confidential material.
- Keep SDK versions, platform requirements, permissions, and bridge details synchronized with verified manifests, builds, and device evidence.

## Verification Rules

- Treat the repository as an executable Flutter MVP, while keeping emulator/build evidence separate from physical-device pose acceptance.
- Run `flutter analyze`, `flutter test`, builds, and device checks only when they exist, and report skipped checks truthfully.
- Unit-test angle geometry, feedback rules, invalid landmarks, and result-state transitions.
- Manually test no selection, cancelled/denied selection, invalid image, reliable analysis, and cannot-analyze paths.

## Git Rules

Before every branch, commit, merge, push, or pull-request operation, run:

```bash
git status --short --branch
git branch --show-current
git remote -v
```

- Use Conventional Commits: `<type>(<scope>): <English summary>`.
- Stage exact paths; never use `git add .`.
- Inspect staged, unstaged, and untracked content for secrets, private images, personal data, contracts, and legal documents before committing.
- Do not commit, push, merge, open a pull request, release, deploy, or create external services without explicit user authorization.
