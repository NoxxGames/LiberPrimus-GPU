> This Wiki page mirrors $sourceRel. The repository tutorial file is the source of truth.

# Repo Tour

## Purpose

Map the repository structure before running experiments.

## Key Paths

- `python/libreprimus/`: Python CLIs, experiment runners, registries, and validation.
- `schemas/`: JSON schemas for committed and generated records.
- `experiments/`: manifests, queues, policies, and ignored generated results.
- `data/`: committed profiles, fixtures, locks, and reviewable observations.
- `third_party/`: local ignored raw material placeholders.
- `docs/`: architecture, research, reference, and Wiki source docs.
- `tutorials/`: public source-of-truth tutorials.

## Expected Outputs

Repo tour commands should be read-only:

```powershell
git status --short
.\.venv\Scripts\python.exe -m libreprimus.cli paths
```

## What Not To Commit

Generated outputs under `experiments/results/`, raw material under `third_party/`, and root research
reports unless copied into docs intentionally.

## Troubleshooting

If a command expects generated results that are missing, rerun the bounded stage locally or use the
CLI `--allow-missing` option when the command supports raw-data-free validation.
