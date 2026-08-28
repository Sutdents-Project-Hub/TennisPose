# TennisPose Desktop Algorithm Demo

This small local tool verifies the photo-analysis concept before or alongside the Flutter mobile UI. It opens an OpenCV window for one still image, draws MediaPipe landmarks, measures the selected shoulder-elbow-wrist angle, and renders green, red, or cannot-analyze feedback.

It is a developer and presentation tool, not a web service or product backend. It does not replace the Flutter app's native Google ML Kit implementation, so a successful MediaPipe run is concept validation rather than mobile-device acceptance.

The runner explicitly uses the CPU delegate because this single-image workflow does not need GPU acceleration and the MediaPipe Python GPU delegate is not the supported macOS path.

## Scope

- One local JPEG or PNG image.
- One selected arm: `left` or `right`.
- One local MediaPipe inference pass.
- A 90–105 degree configurable demonstration range.
- No camera stream, live video, storage, cloud request, account, or medical claim.

## Setup

Use Python 3.11. The local virtual environment belongs at the repository root and is ignored by Git.

```bash
/opt/homebrew/bin/python3.11 -m venv .venv
.venv/bin/python -m pip install -r tools/desktop_demo/requirements.txt
```

The current MediaPipe Tasks API also needs a local model file. Download it once;
the model and a harmless local runtime cache are ignored by Git and are not project assets.

```bash
mkdir -p tools/desktop_demo/models
curl -L --fail \
  --output tools/desktop_demo/models/pose_landmarker_heavy.task \
  https://storage.googleapis.com/mediapipe-models/pose_landmarker/pose_landmarker_heavy/float16/latest/pose_landmarker_heavy.task
```

## Run

This opens an OpenCV preview window. Press any key to close it.

```bash
.venv/bin/python tools/desktop_demo/run_pose_demo.py \
  --image /Users/felix/Desktop/TennisPose_Test_Images/djokovic_trophy_pose.jpg \
  --arm right
```

For a repeatable recording artifact without opening a window, add `--no-display` and an output path.

```bash
.venv/bin/python tools/desktop_demo/run_pose_demo.py \
  --image /Users/felix/Desktop/TennisPose_Test_Images/djokovic_trophy_pose.jpg \
  --arm right \
  --output /Users/felix/Desktop/TennisPose_Test_Images/results/djokovic_result.jpg \
  --no-display \
  --print-json
```

If the selected landmarks are missing, below the visibility threshold, or geometrically invalid, the tool writes an annotated `cannot_analyze` image and never invents a score.

## Test

```bash
.venv/bin/python -m unittest tools/desktop_demo/test_pose_math.py
```

## Test Photo Attribution

The locally downloaded test photos are intentionally excluded from Git. Their source records are in [sample-sources.md](sample-sources.md). Recheck the MediaPipe model terms, every source page, license, and attribution requirement before a public competition demo.
