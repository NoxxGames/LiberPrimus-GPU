# Stage 4B Source-Lock Triage

Stage 4B triages Stage 4A public-link output and the Stage 4A Discord Research-Bundle Review into durable source records. It does not crawl broadly, mirror large archives, process raw Discord logs, or promote private links.

## Inputs

- Generated Stage 4A indexes under `experiments/results/discord-full-review/stage4a/`.
- The curated Stage 4A Deep Research review copy under `docs/research/`.
- Existing archive, visual, cookie, and research-synthesis records.

## Output Records

- `data/observations/archive/stage4b-promoted-source-records.yaml`
- `data/locks/third-party/stage4b-source-health-records.yaml`
- Generated triage diagnostics under ignored `experiments/results/source-lock-triage/stage4b/`.

The promoted records are metadata and source-lock targets only. They are not canonical transcript activation, not page-boundary finalization, and not solve evidence.

## Promotion Rules

Public links are promoted only when they match an allowlisted high-value source class, such as strong community technical repositories, public Cicada history pages, reference-only tooling pages, or selected secondary archives. Discord CDN links, avatar URLs, generic utility noise, opaque attachments, and unsafe/private links are rejected or quarantined.

Stage 4B records selected sources rather than mirroring whole repositories. Later source-lock work may fetch or pin selected files with explicit scope.

Stage 4E follows that policy for the public `cicada-solvers/iddqd` repository. It records tree/path metadata and source-health records, but it does not blind-mirror the repository or commit raw images, audio, fonts, archives, OutGuess payloads, or extracted artefacts.

## Stage 4B Counts

- Stage 4A public links loaded: 57,969.
- Promoted source records: 20.
- Source-health records: 19.
- Duplicate normalized links skipped: 47,755.
- Unsafe or noisy links rejected: 40,716.

No experiments were executed and no raw/generated output was committed.
