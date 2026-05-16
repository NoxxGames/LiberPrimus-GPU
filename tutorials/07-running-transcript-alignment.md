# Running Transcript Alignment

## rtkd Transcript Source

Stage 0D uses the rtkd master transcript as a proposed primary transcript candidate. It is hash-locked but not active canonical corpus.

## Current Alignment Status

The real Stage 0D run produced 185 alignment records but many no-match records remain. Stage 0D-followup is needed before corpus freeze.

## Confidence Labels

Labels are `exact`, `high`, `medium`, `low`, and `none`. Boundary candidates remain tentative even when confidence is high.

## Smoke Command

```powershell
libreprimus corpus-alignment stage0d-smoke `
  --pastebin <repo-root>\data\raw\legacy-pastebins\58-Pages-In-Runes-With-Prime-Values-Pastebin.txt `
  --transcript <repo-root>\data\raw\transcripts\rtkd\liber-primus__transcription--master.txt `
  --out-dir <repo-root>\data\normalized\alignment `
  --allow-warnings
```

## Why Boundaries Are Tentative

Source markers, anchors, and alignment neighborhoods need review against canonical transcript policy before becoming corpus metadata.

## Stage 0D-followup Diagnostics

Stage 0D-followup adds:

- transcript logical-line and rune-stream views;
- bounded stream-subsequence matching;
- alignment gap reports;
- stricter page-boundary confidence auditing.

Run:

```powershell
libreprimus corpus-alignment stage0d-followup-smoke `
  --pastebin <repo-root>\data\raw\legacy-pastebins\58-Pages-In-Runes-With-Prime-Values-Pastebin.txt `
  --transcript <repo-root>\data\raw\transcripts\rtkd\liber-primus__transcription--master.txt `
  --out-dir <repo-root>\data\normalized\alignment `
  --allow-warnings
```

The generated files are diagnostic outputs and are ignored by Git. High confidence is stricter after Stage 0D-followup: empty pairs and word-length-only evidence cannot create high-confidence boundaries.

## Stage 0E Corpus Candidate

Stage 0E consumes the rtkd transcript and frozen profiles to generate an inactive corpus candidate:

```powershell
libreprimus corpus-candidate stage0e-smoke `
  --transcript <repo-root>\data\raw\transcripts\rtkd\liber-primus__transcription--master.txt `
  --out-dir <repo-root>\data\normalized\corpus-candidates\rtkd-master-v0-candidate `
  --allow-boundary-warnings `
  --allow-warnings
```

The candidate has `canonical_corpus_active=false`. Generated outputs remain ignored.
