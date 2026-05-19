# Source-Lock Snapshot CLI

Stage 4K adds:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli source-lock-snapshots build `
  --out-dir experiments/results/source-lock-snapshots/stage4k `
  --cache-dir third_party/SourceSnapshots `
  --snapshot-records-out data/locks/third-party/source-snapshots/stage4k-source-lock-snapshot-records.yaml `
  --fetch-records-out data/locks/third-party/source-snapshots/stage4k-source-fetch-records.yaml `
  --copyright-records-out data/locks/third-party/source-snapshots/stage4k-source-copyright-policy-records.yaml `
  --summary-out data/locks/third-party/source-snapshots/stage4k-source-lock-summary.yaml `
  --allow-network `
  --allow-warnings
```

Offline validation:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli source-lock-snapshots validate `
  --snapshot-records data/locks/third-party/source-snapshots/stage4k-source-lock-snapshot-records.yaml `
  --fetch-records data/locks/third-party/source-snapshots/stage4k-source-fetch-records.yaml `
  --copyright-records data/locks/third-party/source-snapshots/stage4k-source-copyright-policy-records.yaml `
  --summary data/locks/third-party/source-snapshots/stage4k-source-lock-summary.yaml
```

Summary and allowlist inspection:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli source-lock-snapshots summary `
  --summary data/locks/third-party/source-snapshots/stage4k-source-lock-summary.yaml
.\.venv\Scripts\python.exe -m libreprimus.cli source-lock-snapshots list-allowlist
```

`build` reads committed records only. Network use is explicit; validation is raw-data-free and
network-free.
