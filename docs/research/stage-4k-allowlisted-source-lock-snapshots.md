# Stage 4K Research Summary

Stage 4K strengthens public-source reproducibility after Stage 4J made observation review states and
promotion gates explicit.

The stage selected a small allowlisted source subset and recorded source-lock snapshots, fetch records,
copyright-policy records, GitHub commit-address metadata, and an aggregate summary. It did not execute
experiments or process raw private data.

Result summary:

- `43` source candidates considered.
- `15` unique allowlisted source-lock records written.
- `8` GitHub commit-address locks recorded.
- `1` public page fetched to ignored cache and hash-locked.
- `0` committed small text snapshots.
- `22` rejected unsafe/noisy or non-priority sources.
- `6` duplicate sources recorded.
- `6` fetch failures preserved as metadata/failure records.

Interpretation: source-lock snapshots improve provenance and future reproducibility. They do not prove
plaintext, activate the canonical corpus, finalize page boundaries, or justify experiments without a
separate reviewed promotion stage.
