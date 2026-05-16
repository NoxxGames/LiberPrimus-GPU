# 2026-05-16 Stage 0C Legacy Pastebin Ingestion

## Task summary

Imported the local legacy Pastebin TXT source as a non-canonical LP2 rune/prime-value source.

## Starting branch and commit

- Branch: `main`
- Starting commit: `750e472776ad8f17cdde5f07ed438d2e82e711cc`
- Starting status: root `58-Pages-In-Runes-With-Prime-Values-Pastebin.txt` and `LiberPrimus-Research-Report.md` were untracked.

## Input file path discovered

The source was found at repository root as `58-Pages-In-Runes-With-Prime-Values-Pastebin.txt`.

## Whether the file was moved

Moved: true. Destination: `data/raw/legacy-pastebins/58-Pages-In-Runes-With-Prime-Values-Pastebin.txt`.

## Raw-source ignore status

The root drop and raw legacy Pastebin path are ignored by Git. The raw TXT was not staged.

## SHA-256 lock status

Lock metadata was written under `data/locks/legacy-pastebins/`.

- SHA-256: `88ce49a218421a1e0481e69afcd7ed05380f2edf979bfdd5f3bcc7b4cc8ff98f`
- File size: `88739`
- `canonical_corpus_allowed`: false

## Parser design decisions

The parser reads UTF-8 text, preserves raw source lines, parses alternating rune rows and prime-value rows, preserves literal `{}` empty pairs, and emits one line-pair record per aligned pair. It does not infer page labels as facts.

## Gematria validation profile used

Profile: `legacy_validation_gematria_primus_v0`.

No canonical Gematria module exists yet, so a Python-only validation profile was added. It maps 29 Gematria Primus runes to decimal indices and prime values. Unknown glyphs are not silently mapped; if an observed prime value uniquely maps to a known entry, the parser records an alias warning.

Real-source alias warnings: `453`, all for glyph `ᛂ` with observed prime value `37` mapping to the J entry.

## Extraction summary

- Line pairs: `185`
- Empty pairs: `2`
- Validation warnings: `453`
- Unknown glyph count: `453`
- Unknown prime value count: `0`
- Anchors detected: `1`
- Parable anchor detected: true

## Anchor detection summary

The parser detects the rune word `ᛈᚪᚱᚪᛒᛚᛖ` and emits a non-authoritative `57.jpg` anchor. It sets `canonical_page_boundary=false` and does not finalize page boundaries.

## Tests run

- `python -m pytest -q tests/python/test_legacy_pastebin_parser.py tests/python/test_legacy_pastebin_validation.py tests/python/test_legacy_pastebin_cli.py tests/python/test_legacy_pastebin_real_if_present.py`
- `python -m pytest -q tests/python`

## Validation result

The Stage 0C Pastebin test subset passed. Full Python validation passed with `38 passed`.

## Git safety result

The raw TXT, generated normalized JSON/JSONL outputs, `.venv`, build directories, and caches remain ignored or untracked and are not staged.

## Files created/updated

Added raw-source README/.gitkeep placeholders, lock metadata, parser modules, CLI commands, tests, research documentation, and this development log.

## Known limitations

The source is non-canonical. Page boundaries are not finalized. Anchor detection is non-authoritative. Prime values are validation data, not modulo-29 indices. No cipher solving, corpus freeze, scoring, or CUDA work was added.

## Next recommended stage

Stage 0D - align legacy Pastebin line-pairs with primary transcript/page-image sources, infer tentative page boundaries with confidence labels, create developer logs, and freeze a canonical transcript/versioning policy without attempting unsolved-page cryptanalysis.
