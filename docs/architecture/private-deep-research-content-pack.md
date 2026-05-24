# Private Deep Research Content Pack

Stage 5AN adds a private content layer after the Stage 5AM metadata-only static index.

Stage 5AM produced `website-export/stage5am/research-index/`, which is a navigation and metadata site only. Stage 5AN produces the content library that a later Deep Research prompt can cite:

- `deep-research-content-packs/stage5an/deep-research-content-pack-stage5an.zip`
- `website-export/stage5an/private-content/`
- `website-export/stage5an/webserver-root/`

The combined webroot contains the Stage 5AM metadata index plus `private-content/`. Copy the contents of `website-export/stage5an/webserver-root/` to the private webserver root when preparing the hosted handoff.

## Boundaries

The Stage 5AN outputs are private/review-gated generated outputs. They are not public publication, source truth, Deep Research output, experiment results, or solve evidence.

Stage 5AN does not run network fetches, online cloning, Google Drive storage, OCR, AI/ML interpretation, image forensics, stego/audio tooling, CUDA, benchmarks, scored experiments, hypothesis execution, or public website expansion.

Noindex and `robots.txt` are discoverability hints, not security controls. If the private content library is uploaded, use server-side access control appropriate for private generated extracts.

## Committed Records

Committed Stage 5AN records live under `data/deep-research-export/`. Generated content-pack files, hosted content, combined webroot files, ZIP archives, and safe extracts remain ignored.
