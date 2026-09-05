# TennisPose - AI Tennis Trophy Pose Coach

> Stage: competition MVP | Product: local Streamlit web application | Deployment: none

TennisPose analyzes one authorized tennis serve Trophy Pose photo in a local browser session. The user uploads a JPEG or PNG; the app locates the racket arm, measures the shoulder-elbow-wrist angle from MediaPipe's 3D world landmarks, and returns an annotated green, red, or cannot-analyze result.

It is deliberately a single-photo learning aid. It is not a live-video coach, full-swing tracker, injury-prevention system, or medical product. The 80–120 degree inclusive interval is configurable demonstration logic, not a validated coaching or clinical standard.

## How the Measurement Works

The accuracy of this app rests on three decisions, each of which is testable:

1. **The angle is measured in 3D, not on the flat image.** MediaPipe returns both
   normalized image landmarks and metric `pose_world_landmarks`. A serve puts the
   racket arm at a steep angle to the camera, so the flat 2D projection
   understates the bend badly — on the reference photos it read 33° where the arm
   was actually near 83°, and 43° where it was near 101°. Every verdict uses the
   3D landmarks; the 2D value is shown only for comparison.
2. **The racket arm is detected, not guessed.** At the trophy position the tossing
   arm is nearly straight and high while the racket arm is folded to roughly a
   right angle near shoulder height. Auto-detect measures the more bent of the
   arms that are both visible and already raised, which finds a left-handed
   server's arm as readily as a right-handed one. The choice can be overridden.
3. **The same photo is measured three times.** The original, a downscaled copy,
   and a mirrored copy each produce an angle; the reported value is their median
   and the disagreement between them is reported as confidence. A single
   inference pass can be confidently wrong on a dark or unusual photo — pooling
   turns that silent failure into either a corrected value or a visible caution.

The app refuses rather than guesses in auto-detect mode. A ready stance, a
contact frame, a follow-through, a hidden racket arm, a player too small in the
frame, or three passes that cannot agree return cannot-analyze with a specific
reason, never a score. A manual left/right override instead honors a clearly
visible selected arm and labels a non-trophy reading with a caution.

## MVP Scope

- A local Streamlit interface served from `streamlit_app.py`.
- JPEG and PNG content validation for one still image, with a 10 MB upload and 20 megapixel decode limit.
- Automatic racket-arm detection, with a manual left/right override.
- Local CPU inference with MediaPipe PoseLandmarker, loaded once per process.
- Shoulder, elbow, and wrist reliability checks before any angle is shown.
- An auto-detect trophy-position gate that rejects photos showing a different moment of the serve; a manual arm override preserves a visible-arm reading with a caution.
- Three-point elbow-angle geometry from 3D world landmarks, pooled over three passes.
- Inclusive, adjustable 80–120 degree demonstration feedback with a reported confidence.
- Annotated in-range (green), adjustment (red), or cannot-analyze result.
- No account, backend, database, cloud upload, remote AI, API key, saved history, camera, or video.

## Technology

| Responsibility | Implementation |
|---|---|
| Local web UI | Streamlit |
| Runtime | 64-bit Python 3.11 |
| Pose landmarks | MediaPipe Tasks PoseLandmarker, local CPU delegate |
| Geometry, gating, and feedback | `tennispose.pose_math` |
| Landmark extraction and arm selection | `tennispose.pose_detector` |
| Result drawing | `tennispose.annotate` |
| Tests | Python `unittest` |
| Dependencies | Pinned in `requirements.txt` |

The browser is a local interface to the Python process, and photo inference runs locally. The application code contains no photo-upload service. However, the installed MediaPipe 0.10.35 binary emitted background Clearcut uploader failure messages during verification; local inference is not a guarantee that every dependency makes zero network attempts. See [the dependency privacy caveat](docs/security-and-privacy.md#dependency-network-caveat).

## Run Locally

Install **64-bit Python 3.11** first, then extract the complete project to a
writable local folder. The launchers do not install Python, change system
settings, or require administrator privileges. Do not copy another computer's
`.venv` folder. See [the Traditional Chinese teaching guide](docs/teaching-guide.zh-TW.md)
for the classroom lesson and exercises.

- **Windows:** double-click `start.bat`. The launcher checks the existing project
  environment, `py -3.11`, then `python`. When installing Python, include the
  Python launcher and enable the PATH option.
- **macOS:** double-click `start.command`. If the extracted ZIP lost executable
  permission, open Terminal in the project folder and run `bash start.command`.
  If macOS blocks a downloaded file, follow your school's software policy; do
  not disable system security. The terminal command is also a fallback when
  Finder opens the script as text.

Python installers are available from [python.org](https://www.python.org/downloads/).
For Windows/macOS installer-based classrooms, the
[Python 3.11.9 release](https://www.python.org/downloads/release/python-3119/)
has platform installers; use the school's approved Python 3.11 distribution
when available. Newer 3.11 patch releases may use a different distribution method.
The current package pins require compatible binary wheels; the launchers stop
instead of attempting a compiler-based installation on an unsupported platform.
Windows and Intel Mac runtime compatibility must be checked on those machines;
a successful Apple Silicon Mac run does not establish it.

On first launch, `scripts/bootstrap.py` creates `.venv`, installs
`requirements.txt`, downloads the versioned official heavy model (~29 MB),
verifies its SHA-256, checks imports and model loading, and starts Streamlit.
Allow several minutes and an internet connection before class. Subsequent runs
reuse the packages when the requirements fingerprint is unchanged and reuse the
verified model without downloading. Keep the terminal open while using the app;
press **Ctrl+C** there to stop it. If no browser opens, visit
**http://127.0.0.1:8501** on the same computer.

The launcher binds only to `127.0.0.1` and disables Streamlit usage statistics.
This is a local app, not a public deployment. A busy port produces a clear error
instead of starting another service on an unexpected address.

Optional terminal commands from the project folder:

```bash
# macOS: install and verify before class, without opening the app
bash start.command --setup-only
# Recheck/install requirements after a package problem (internet required)
bash start.command --repair
```

```bat
rem Windows Command Prompt equivalents
start.bat --setup-only
start.bat --repair
```

If an existing `.venv` is broken or incompatible, the launcher preserves it and
stops. Close the app, rename `.venv` to `.venv-backup`, and retry. `--repair`
reruns normal pip installation; it does not rebuild a broken environment or
force-reinstall damaged files. For a model checksum error, rename the indicated
model file and retry. Interrupted downloads use temporary files and never become
accepted models. For a stale `.tennispose-setup.lock`, first close all setup
terminals, then remove that lock file and retry. Package/network errors remain
visible in the terminal; show the error to the teacher instead of repeatedly
changing Python versions.

Manual equivalent (Python 3.11 must be installed):

```bash
python3.11 -m venv .venv
.venv/bin/python scripts/bootstrap.py
```

```bat
py -3.11 -m venv .venv
.venv\Scripts\python.exe scripts\bootstrap.py
```

Open the local URL shown by Streamlit and upload a photo you own or are authorized to analyze. The racket arm is detected automatically; override it in the sidebar if the photo is unusual. The page runs the local analysis immediately for the current upload and settings. Do not upload photos to a public deployment: public hosting is outside this MVP.

## Verify

```bash
.venv/bin/python -m unittest discover -s tests -v
```

`tests/test_reference_photos.py` replays ten authorized reference serve photos
through the full pipeline and asserts the arm chosen, the verdict, and the angle
against `tests/reference_expectations.json`. It is the regression gate for
accuracy: change a threshold and it tells you what moved. Point it at the photos
with `TENNISPOSE_SAMPLE_DIR`, and it skips cleanly when they or the model are
absent.

```bash
TENNISPOSE_SAMPLE_DIR=docs/demo-assets/reference-photos \
  .venv/bin/python -m unittest discover -s tests -v
```

Before competition submission, manually exercise these local paths in the browser:

- no uploaded image;
- unsupported or unreadable input;
- a trophy-position photo that lands in the configured range (green);
- a trophy-position photo outside that range (red);
- a photo that is not a trophy position at all in auto-detect mode, which must refuse rather than score; and
- an occluded or unreliable-landmark photo that returns cannot-analyze without a score.

## Demo Assets and Results

The repository includes a licensed, documented ten-photo reference set and the
corresponding full-page Streamlit results. The input photos are used by the
accuracy regression suite; the result screenshots are visual evidence for the
green, red, and cannot-analyze states. See
[the asset manifest](docs/demo-assets/README.md) for source links, author
credits, license terms, result summaries, and public-use conditions.

## Repository Layout

```text
start.bat / start.command   # classroom setup and local launch
scripts/bootstrap.py        # shared setup, integrity checks, loopback server
streamlit_app.py             # local Streamlit entry point
requirements.txt             # pinned Python dependencies
tennispose/
  __init__.py
  pose_math.py               # pure geometry, gating rules, and feedback
  image_input.py             # content validation and safe JPEG/PNG decoding
  pose_detector.py           # MediaPipe inference, arm selection, and reporting
  annotate.py                # result drawing
tests/
  test_pose_math.py          # geometry, gating, and pooling
  test_arm_selection.py      # racket-arm detection and refusal reasons
  test_analysis_pipeline.py  # entry-point guards and empty-photo behavior
  test_reference_photos.py   # accuracy regression over authorized photos
  test_image_input.py        # upload validation
  reference_expectations.json
models/                      # ignored local MediaPipe model file
docs/
  demo-assets/
    reference-photos/        # licensed reference inputs used by the regression suite
    streamlit-results/       # full-page local-browser evidence for the ten inputs
    README.md                # attribution and result manifest
```

## Documentation

- [Project profile](docs/project-profile.md)
- [Product requirements](docs/project-overview.md)
- [Solution architecture](docs/architecture.md)
- [MVP roadmap and test plan](docs/mvp-plan.md)
- [Competition plan](docs/competition.md)
- [Data and storage boundary](docs/data-and-storage.md)
- [Dependencies](docs/integrations.md)
- [Security and privacy](docs/security-and-privacy.md)
- [Demo asset attribution and results](docs/demo-assets/README.md)
- [Repository working rules](AGENTS.md)

## License and Attribution

No overall project license has been selected. The versioned demo photos and
derived screenshots retain the upstream Creative Commons terms documented in
[the asset manifest](docs/demo-assets/README.md). Confirm source-code
ownership, dependency licenses, model terms, asset attribution, and current
competition rules before public submission or release.
