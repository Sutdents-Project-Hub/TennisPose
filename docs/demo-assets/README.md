# Licensed Reference Photos and Streamlit Results

This directory is the repository's explicit public-documentation asset set. It
contains ten licensed tennis-serve reference photos and the corresponding
full-page screenshots from the local Streamlit application. These files are
static repository documentation; the application itself does not save uploaded
photos, landmarks, or results.

## Directory Layout

```text
reference-photos/   # metadata-free JPEG inputs used by the regression suite
streamlit-results/  # 1280x1400 local-browser screenshots for the same inputs
```

Run the reference-photo regression suite with:

```bash
TENNISPOSE_SAMPLE_DIR=docs/demo-assets/reference-photos \
  .venv/bin/python -m unittest discover -s tests -v
```

## Asset Manifest

The visual source photos were downloaded from Wikimedia Commons on August 28,
2026. The repository copies have their JPEG metadata removed; their visual
pixels, filenames, source links, authors, and licenses are preserved. The
Streamlit result files are annotated derivatives of their matching input photos.
Preserve the upstream attribution and applicable Creative Commons terms when
copying, publishing, or showing either reference image or its result image.

| Input and source | Credit and license | Result screenshot | Verified result |
|---|---|---|---|
| [01 Dominic Pagon](reference-photos/01_dominic_pagon.jpg) — [source](https://commons.wikimedia.org/wiki/File:Dominic_Pagon,_Jamaica_Tennis_Serve_,_Oct_2016.jpg) | Tennisp; CC BY-SA 4.0 | [Cannot analyze](streamlit-results/01_dominic_pagon-auto-cannot-analyze.png) | Ready stance; no trophy-position score |
| [02 John McEnroe](reference-photos/02_mcenroe_serve.jpg) — [source](https://commons.wikimedia.org/wiki/File:McEnroe_Serving.jpg) | Levg; Commons page lists CC BY-SA and GFDL terms | [Green](streamlit-results/02_mcenroe_serve-auto-green.png) | Left arm, 101 degrees |
| [03 Jelena Ostapenko](reference-photos/03_jelena_ostapenko.jpg) — [source](https://commons.wikimedia.org/wiki/File:Jelena_Ostapenko_serving.jpg) | MasterMind5991; CC BY-SA 4.0 | [Cannot analyze](streamlit-results/03_jelena_ostapenko-auto-cannot-analyze.png) | Racket arm hidden; ambiguous arm |
| [04 Carlos Alcaraz](reference-photos/04_carlos_alcaraz.jpg) — [source](https://commons.wikimedia.org/wiki/File:Carlos_Alcaraz_-_Roland_Garros_2025_-_serving_(cropped).jpg) | Attribution as listed on source page; CC BY-SA 4.0 | [Green](streamlit-results/04_carlos_alcaraz-auto-green.png) | Right arm, 101 degrees |
| [05 Gökberk Ergeneman](reference-photos/05_gokberk_ergeneman.jpg) — [source](https://commons.wikimedia.org/wiki/File:G%C3%B6kberk_Ergeneman_Tennis_Serve.jpg) | Newinfoeveryminute; CC BY-SA 4.0 | [Red](streamlit-results/05_gokberk_ergeneman-auto-red.png) | Right arm, 166 degrees |
| [06 Nicolas Mahut](reference-photos/06_nicolas_mahut.jpg) — [source](https://commons.wikimedia.org/wiki/File:Nicolas_Mahut,_serving.jpg) | Bruno Girin; CC BY-SA 2.0 | [Red](streamlit-results/06_nicolas_mahut-auto-red.png) | Right arm, 168 degrees |
| [07 Tommy Haas](reference-photos/07_tommy_haas.jpg) — [source](https://commons.wikimedia.org/wiki/File:Tommy_Haas_serves.jpg) | Diane Krauss; CC BY-SA 2.5 and GFDL | [Cannot analyze](streamlit-results/07_tommy_haas-auto-cannot-analyze.png) | Racket hand below the checkpoint |
| [08 Roger Federer](reference-photos/08_federer_trophy_pose.jpg) — [source](https://commons.wikimedia.org/wiki/File:Fed_Trophy_Pose_(3)_(27009790086).jpg) | JC / Tennis-Bargains.com; CC BY-SA 2.0 | [Green](streamlit-results/08_federer_trophy_pose-auto-green.png) | Right arm, 83 degrees |
| [09 Novak Djokovic](reference-photos/09_djokovic_trophy_pose.jpg) — [source](https://commons.wikimedia.org/wiki/File:Djokovic_trophy_pose_on_serve_(2)_(7861310456).jpg) | JC / JCTennis.com; CC BY-SA 2.0 | [Green](streamlit-results/09_djokovic_trophy_pose-auto-green.png) | Right arm, 111 degrees |
| [10 Maria Sharapova](reference-photos/10_sharapova_serve.jpg) — [source](https://commons.wikimedia.org/wiki/File:Sharapova_tennis_service_0826.jpg) | terence; CC BY 2.0 | [Red](streamlit-results/10_sharapova_serve-auto-red.png) | Right arm, 144 degrees |

The 80–120 degree range remains configurable demonstration logic. These assets
show the current MVP behavior; they do not prove coaching, injury-prevention,
medical, competition-compliance, or biomechanical validity.

## Public-Use Conditions

- Keep the input filename, source link, author credit, and license notice with
  every asset reused outside this repository.
- Treat the annotated screenshots as derivatives of the original photographs;
  the applicable source license continues to apply, including ShareAlike terms
  where present.
- Do not add private user uploads, new photographs, or model files to this
  directory without an attribution and permission review.
