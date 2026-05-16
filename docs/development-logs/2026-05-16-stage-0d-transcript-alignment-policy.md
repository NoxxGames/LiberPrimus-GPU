# 2026-05-16 Stage 0D Transcript Alignment Policy

## Task Summary

Added Stage 0D transcript alignment, tentative page-boundary inference, glyph-variant policy, and canonical transcript versioning policy scaffolding.

## Starting Branch And Commit

- Branch: `main`
- Starting commit: `7636b7a43233757230bac30297f048848785e43f`
- Starting status: `LiberPrimus-Research-Report.md` was untracked and was not staged.

## Existing Stage 0C Pastebin Status

Stage 0C raw Pastebin TXT existed at `data/raw/legacy-pastebins/58-Pages-In-Runes-With-Prime-Values-Pastebin.txt`.

Stage 0C lock metadata existed under `data/locks/legacy-pastebins/`.

## Source Files Discovered Or Downloaded

The rtkd transcript and scream314 markdown were absent locally and were downloaded from the two allowed raw GitHub URLs.

- rtkd local path: `data/raw/transcripts/rtkd/liber-primus__transcription--master.txt`
- scream314 local path: `data/raw/transcripts/scream314/liber_primus.md`

## Raw-Source Ignore Status

Raw transcript files are ignored through `data/raw/**` with README and `.gitkeep` exceptions. Raw Pastebin TXT remains ignored.

## SHA-256 Lock Status

rtkd lock:

- SHA-256: `e21743ccd9a07f3845d52a329c61b9fa69e9ca6a44ee3ba0db8f28a0d7065004`
- File size: `54478`
- `canonical_corpus_active`: false

scream314 lock:

- SHA-256: `0f7545d470f2056b45b5de2c8c116ecdea66969fdca6be57ccbd8e591e40ee92`
- File size: `137957`
- `canonical_corpus_active`: false

## Transcript Parser Design

The rtkd parser preserves physical line numbers, raw text, stripped text, rune glyphs, separator counts, raw separator characters, source page markers, section markers, parse warnings, and `trusted_as_canonical=false`.

The scream314 parser extracts page labels, LP page-count statements, solved-section titles, and method keywords only. It does not parse markdown as canonical corpus.

## Alignment Algorithm Design

Alignment reuses the Stage 0C Pastebin parser and builds hash/signature indexes for raw rune sequences, documented variant-normalized sequences, decimal-index sequences, and bounded subsequence candidates. The real-source run emits one record for every Pastebin line pair.

## Glyph `ᛂ` Investigation

Stage 0D emits a `glyph_variant_observation` for `ᛂ`:

- Occurrence count: `453`
- Observed prime value: `37`
- Inferred decimal index: `11`
- Inferred canonical candidate: `ᛄ`
- Policy: preserve raw glyphs and allow only a documented normalized view.

No canonical Gematria mapping was changed.

## Tentative Page-Boundary Inference Summary

The rtkd `%` source markers and the final Parable anchor produce tentative boundary candidates. Every boundary record sets `canonical_page_boundary=false`.

## Performance And Timing Notes

Real-source smoke elapsed milliseconds:

- Pastebin parse: about `52`
- Transcript parse: about `25`
- Signature build: about `51`
- Matching: about `230`
- Boundary inference: about `1`
- Glyph variant summary: about `2`

These timings are metadata only, not benchmark claims.

## Tests Run

`python -m pytest -q tests/python`

Result: `55 passed`.

## Validation Result

Stage 0D synthetic parser, alignment, boundary, glyph variant, CLI, and real-source conditional tests passed.

## Git Safety Result

Raw transcript files, raw Pastebin TXT, generated alignment outputs, `.venv`, build outputs, caches, and `LiberPrimus-Research-Report.md` were not staged.

## Files Created Or Updated

Added transcript source parsers, alignment modules, CLI commands, tests, README/.gitkeep placeholders, transcript lock metadata, research docs, corpus policy docs, this developer log, and the Stage 0D research log.

## Known Limitations

The rtkd transcript is only a proposed candidate. The real-source alignment leaves many Pastebin line pairs unmatched. Page boundaries are tentative. The `ᛂ` mapping is a normalized-view policy only.

## Next Recommended Stage

Stage 0D-followup should resolve transcript-alignment gaps and boundary ambiguities before corpus freeze, unless the project accepts the documented gaps and moves to Stage 0E.
