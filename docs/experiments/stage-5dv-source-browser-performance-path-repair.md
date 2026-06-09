# Stage 5DV Source Browser Performance And Path Repair

Stage 5DV repairs the Operator Console Source Browser before the first number-fact review batch.

The stage adds key-aware/source-root-aware path collection, suppresses bare root filename paths, suppresses duplicate present+missing basename pairs, adds canonical local third-party path aliases, caches path resolution, lazily/caches thumbnails and raw-preview strings, precomputes search text, and records Source Browser loadability/performance evidence.

This is GUI/index repair infrastructure only. It does not perform number-fact review batch 1, backfill number facts, rewrite source-lock records, select a target, generate bytes, run OCR/image forensics/audio/stego/CUDA/scoring work, execute source files, or make a solve claim.

Primary records:

- `data/project-state/stage5dv-summary.yaml`
- `data/project-state/stage5dv-source-browser-performance-evidence.yaml`
- `data/project-state/stage5dv-path-canonicalization-repair-summary.yaml`
- `data/operator-console/source-browser/path-canonicalization-policy.yaml`
- `data/operator-console/source-browser/performance-policy.yaml`
- `data/operator-console/source-browser/cache-policy.yaml`

Required validators:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli token-block validate-stage5dv
.\.venv\Scripts\python.exe -m libreprimus.cli source-browser validate-paths
.\.venv\Scripts\python.exe -m libreprimus.cli source-browser performance-smoke
```
