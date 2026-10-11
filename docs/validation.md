# Research and Validation — October 11, 2026

The current local MVP screens for preparation-like dual-arm geometry, then
compares a supported elbow estimate against the user's target interval. It now
refuses wrong-phase examples, invalid repeats, insufficient support and boundary
conflicts. This validates those safeguards; it does not establish universal
serve correctness or absolute monocular angle accuracy.

## Evidence Behind the Design

- [Jacquier-Bret and Gorce, Sensors 2024](https://pmc.ncbi.nlm.nih.gov/articles/PMC11175047/)
  measured four players with ten cameras. Trophy position, racket low point and
  ball impact are distinct sequence events. A single still can only support
  preparation-like appearance; it cannot establish a temporal maximum. Their
  segment-rotation/flexion conventions are not this application's three-point
  interior angle, so published values cannot directly become its angle labels.
- [Google's official pose classification guide](https://github.com/google-ai-edge/mediapipe/blob/master/docs/solutions/pose_classification.md)
  and [pose embedding source](https://github.com/googlesamples/mlkit/blob/master/android/vision-quickstart/app/src/main/java/com/google/mlkit/vision/demo/java/posedetector/classification/PoseEmbedding.java)
  informed torso normalization and relative-joint features. The examples are
  not validated tennis classifiers. A small collection of stills does not
  justify training and claiming a general classifier. No source code was copied
  and no ML Kit/Android dependency was added.
- [BlazePose GHUM's primary paper](https://arxiv.org/abs/2206.11678) describes
  monocular 3D estimation. Hip-relative metric coordinates and repeated image
  transforms do not provide measured 3D ground truth.

The numerical position, limb-plausibility, association and repeat thresholds
are conservative engineering heuristics documented in
[architecture.md](architecture.md). They are not thresholds supplied or validated
by these publications. The 80–120 target remains a configurable demonstration.

## Changes and Regression Evidence

| Prior failure | Current safeguard and evidence |
|---|---|
| A raised contact/follow-through arm could be graded, even green after widening the target | Torso-relative racket-arm geometry plus elevated opposite-hand cues; target-independent; automatic and manual modes both gate. Twelve real-photo checks across four unsuitable images and three arm modes refuse at 40–180. |
| Low-visibility repeats could overwrite a reliable primary angle | Every repeat checks image/world visibility, presence, bounds, finite coordinates, segment geometry and preparation. Mock regression preserves refusal instead of inventing a green result. |
| One surviving pass or a conflicting majority could be called high confidence | At least three valid readings; full spread <=20 degrees; no interval-category crossing. All accepted readings count, including reliable outliers. |
| Repeat detection could change person or arm | Inverse affine/mirror restoration and spatial association with the primary arm. Person-shift, arm-drift and actual affine round-trip tests pass. This is not identity recognition. |
| NaN/short landmarks crashed annotation/indexing | Complete-array check before indexing and reliable-point checks before drawing; regression returns no score. |
| 2D comparison ignored rectangular image aspect | Compute it in pixels; keep it out of verdict decisions. |
| Displayed symmetric uncertainty and implied accuracy | Show actual observed min/max, valid/attempted passes and repeat agreement; no accuracy probability or calibrated confidence interval. |

Numeric reference expectations are model-output snapshots. The default unittest
command now uses the repository's licensed photos, avoiding an accidental skip
caused by an unrelated personal Desktop path.

## Real-Photo Results

The original ten licensed images were previously used for development. They are
regression inputs, not heldout accuracy data. Current default results:

| Input | Result |
|---|---|
| McEnroe | Left, 100.8 degrees; 98.2–105.3 observed; high repeat agreement |
| Federer | Right, 85.3 degrees; 81.4–90.7; moderate agreement |
| Djokovic | Right, 111.6 degrees; 100.9–113.2; moderate agreement |
| Alcaraz | Genuine preparation view, but conflicting inferred angles; `unstable`, no score |
| Pagon, Ergeneman, Mahut, Sharapova | Unsupported preparation cues; no score |
| Ostapenko, Haas | Unreliable/ambiguous arm; no score |

Six additional licensed images were collected and visually labelled for phase
and racket arm **before their first inference**. Thresholds were not tuned on
them. Labels are visual inspection, not coach or motion-capture ground truth:

| Heldout input and credit | Pre-inference label | Result |
|---|---|---|
| [Murray part 1](https://commons.wikimedia.org/wiki/File:Andy_Murray_Serve_Part_1.jpg), Nick Hewson, CC BY 2.0 | Preparation-like, right | Ambiguous arm; refused |
| [Murray part 2](https://commons.wikimedia.org/wiki/File:Andy_Murray_serve_part_2.jpg), Nick Hewson, CC BY 2.0 | Near/after contact | Not preparation; refused |
| [Murray part 3](https://commons.wikimedia.org/wiki/File:Andy_Murray_serve_part_3.jpg), Nick Hewson, CC BY 2.0 | Follow-through | Ambiguous arm; refused |
| [Nadal Serving](https://commons.wikimedia.org/wiki/File:Nadal_Serving.jpg), Donna and Keith, CC BY 2.0 | Preparation-like, left | Left, 102.0 degrees; 100.9–102.7; high agreement |
| [Nadal lefty serve](https://commons.wikimedia.org/wiki/File:Nadal_lefty_serve_(4944616391).jpg), JC, CC BY-SA 2.0 | Foreground receiver/multiple distant players; unsuitable | No reliable arm; refused |
| [Stephens serve](https://commons.wikimedia.org/wiki/File:Sloane_Stephens_serves_at_the_US_Open_(9662688451)_(cropped).jpg), Boss Tweed, CC BY 2.0 | Late cocking/acceleration, not clear TP | Not preparation; refused |

All four unsuitable/other-phase heldout examples refused. One of two preparation
examples was usable; the distant Murray example refused. This is an explicit
coverage cost, not a perfect accuracy claim. Murray's three images share a
player/event/photographer. Six images are too few to estimate population accuracy.
Nadal/Stephens use the uncropped licensed Flickr upstream images; the local
manifest records the actual URLs, sizes, hashes and terms. Additional photos
and annotations remain in ignored local `archive/optimization-2026-10-11/`.

## Verification and Reproduction

```bash
.venv/bin/python -m unittest discover -s tests -v
bash start.command
```

The full suite passed **80 tests, zero skips** on Apple Silicon macOS/Python
3.11.14 with the pinned dependencies and official version-1 heavy model.
Geometry tests include 72 analytically known angle/rotation/scale combinations;
these validate the formula, not MediaPipe's image accuracy. The model checksum
and startup procedure are unchanged from the verified launcher.

Local browser checks cover no upload, unreadable JPEG, unsupported text, green
Nadal, a deliberately configured red interval, wrong-phase refusal at 40–180
including manual selection, conflicting estimates and target-boundary refusal.
The red interval demo does not supply a poor-technique ground-truth photo.
The application remains available only at `http://127.0.0.1:8501` while running.

Local evidence: `archive/optimization-2026-10-11/unittest.log`,
`photo-results-final.json`, `wide-band-guards.json`, `heldout/blind-labels.json`,
`heldout/manifest.json`, and `output/playwright/`. Historical August screenshots
remain attributed in `demo-assets/`; they are not current result screenshots.

The additional licensed local assets can be replayed, when present, with:

```bash
.venv/bin/python archive/optimization-2026-10-11/evaluate.py
```

This ignored evaluation script checks the pre-labelled negative cases and arm
identity of accepted heldout cases. It writes reports for these explicitly
licensed evaluation inputs only; it is separate from the in-memory application
upload path and is not a general private-photo export feature.

## Remaining Accuracy Acceptance

Candidate datasets were also inspected, rather than assuming an open repository
provides independently measured angle labels:

| Source | Current suitability |
|---|---|
| [SportsPose](https://christianingwersen.github.io/SportsPose/download.html) | Multi-view sports benchmark, but access requires a request with academic identity and intended use. No external request or account change was made. |
| [University of Bath serve motion capture](https://researchdata.bath.ac.uk/1454/) | CC BY 4.0 marker trajectories are available. The released file list does not include paired RGB frames for running this photo model against the measurements. |
| [UVA tennis serve dataset](https://github.com/jasnwag/tennis_serve_dataset) | Its documented RTMPose/MotionBERT pipeline estimates 3D from broadcast video; these are model-derived labels, not measured 3D ground truth. |
| [THETIS](https://github.com/THETIS-dataset/dataset) | Kinect action sequences include beginner/expert players, but the inspected README lists rendered skeleton videos and supplies no dataset reuse license or numerical joint table. Further data/terms review is needed before local photo evaluation. |

The photo sets contain no independently measured 3D elbow angles and no
coach-labelled incorrect Trophy technique. Before a stronger correct/incorrect
claim, obtain authorized, independent coach labels and synchronized calibrated
3D reference measurements across players, views, lighting and occlusion. Freeze
development and heldout splits by player/session; report angle error, accepted
coverage, wrong-phase false acceptance, interval errors and refusals separately.
The acceptable errors/coverage must be set with the intended evaluator before
testing. More heuristics or the same model's repeated outputs cannot supply that
missing ground truth. No full-serve, injury, deployment or competition acceptance
claim is made by this local verification.
