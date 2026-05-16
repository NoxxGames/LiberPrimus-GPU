# Exploratory Experiment CLI

## `validate-exploratory`

Validates one exploratory manifest and prints its manifest ID, SHA-256, and disabled execution flags.

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli experiment validate-exploratory --manifest experiments/manifests/exploratory/stage2e-caesar-preview-dry-run.yaml
```

## `dry-run`

Builds a generated dry-run plan for one manifest. It does not execute transforms, enumerate plaintexts, score candidates, or use CUDA.

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli experiment dry-run --manifest experiments/manifests/exploratory/stage2e-caesar-preview-dry-run.yaml --out-dir experiments/results/exploratory-dry-runs/stage2e --allow-warnings
```

## `stage2e-dry-run-all`

Builds dry-run plans for all Stage 2E exploratory manifests.

## `dry-run-summary`

Reads generated dry-run summary output and prints plan counts, candidate-count totals, and safety-gate counts.

## Troubleshooting

Safety failures should be fixed in the manifest. Do not bypass disabled execution, search, scoring, CUDA, canonical corpus, or page-boundary gates.
