# Public Source-Locking Policy

Public source locks are the reproducibility layer between review-only observations and later
experiments. A source lock can support provenance, but it cannot promote an observation by itself.

Architecture rules:

- Source-lock candidates must come from committed records or a later explicit source intake stage.
- Allowlist filtering is mandatory before network retrieval.
- GitHub sources should resolve to commit-addressed URLs where possible.
- Non-GitHub web pages default to ignored local snapshots plus committed hash metadata.
- Binary/image/audio/font/archive/PDF sources default to metadata-only records.
- Copyright notes are required for every source-lock snapshot record.
- Validation must fail if raw private data, binaries, images, audio, fonts, archives, or solve claims
  are marked as committed.

Stage 4K writes source-lock metadata under `data/locks/third-party/source-snapshots/` and local
generated reports under ignored `experiments/results/source-lock-snapshots/stage4k/`.
