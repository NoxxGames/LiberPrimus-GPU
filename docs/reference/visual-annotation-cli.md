# Visual Annotation CLI

Stage 4C adds:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli visual-annotation build `
  --visual-observations data/observations/visual/stage4b-visual-observation-records.yaml `
  --negative-controls data/observations/research/stage4b-negative-control-records.yaml `
  --image-artifacts data/observations/visual/liber-primus-page-image-artifacts-v0.jsonl `
  --image-locks data/locks/third-party/liber-primus-pages/liber-primus-page-image-locks-v0.jsonl `
  --image-dir third_party/LiberPrimusPages `
  --out-dir experiments/results/visual-annotation/stage4c `
  --task-out data/observations/visual/stage4c-visual-annotation-tasks.yaml `
  --cuneiform-out data/observations/visual/stage4c-cuneiform-reading-candidates.yaml `
  --dot-out data/observations/visual/stage4c-dot-pattern-annotation-tasks.yaml `
  --delimiter-out data/observations/visual/stage4c-delimiter-annotation-tasks.yaml `
  --negative-out data/observations/visual/stage4c-visual-negative-control-annotation-tasks.yaml `
  --summary-out data/observations/visual/stage4c-annotation-pack-summary.yaml `
  --allow-warnings
```

Validation:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli visual-annotation validate `
  --task data/observations/visual/stage4c-visual-annotation-tasks.yaml `
  --cuneiform data/observations/visual/stage4c-cuneiform-reading-candidates.yaml `
  --dot data/observations/visual/stage4c-dot-pattern-annotation-tasks.yaml `
  --delimiter data/observations/visual/stage4c-delimiter-annotation-tasks.yaml `
  --negative data/observations/visual/stage4c-visual-negative-control-annotation-tasks.yaml `
  --summary data/observations/visual/stage4c-annotation-pack-summary.yaml
```

Summary:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli visual-annotation summary `
  --summary data/observations/visual/stage4c-annotation-pack-summary.yaml
```

`build` may read local ignored LP page images to create a generated local site. `validate` works from committed records and does not require raw images.
