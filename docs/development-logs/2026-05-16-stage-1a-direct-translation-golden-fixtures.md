# Stage 1A Direct-Translation Golden Fixtures Developer Log

## Task Summary

Added solved-page golden fixture infrastructure and direct-translation reproduction for selected known solved direct-transliteration sections.

## Starting State

- branch: `main`
- starting commit: `7e98f15ebd37aee11b3bec0542be1311ef4d076a`
- target repository: `NoxxGames/LiberPrimus-GPU`
- raw rtkd, scream314, and Pastebin sources were present and ignored.
- Stage 0E profile hashes matched expected values.
- `LiberPrimus-Research-Report.md` remained unstaged.

## Fixture Directories

Created committed fixture docs and manifests under `data/fixtures/solved-pages/direct-translation-v0/`. Generated reproduction output is ignored under `data/normalized/solved-baselines/direct-translation-v0/`.

## Schemas

Added schemas for solved-page fixtures, reproduction records, and reproduction summaries. Schemas require non-canonical flags to remain false.

## Decoder Design

The direct decoder maps rune tokens to Gematria profile preferred Latin labels, converts word separators to spaces, converts clause separators to `. `, joins visual line separators, preserves numeric literals, and emits warnings for unknown symbols. It does not implement Atbash, Vigenere, prime streams, or search.

## Fixtures

Created four passing-intended direct fixtures: `the-loss-of-divinity`, `some-wisdom`, `an-instruction-direct`, and `p57-parable`.

## Real Smoke Result

Stage 1A smoke produced four passes, zero failures, zero pending, and zero skipped records. Generated outputs remain ignored.

## Validation Result

- fixture validation: passed
- real-source smoke: `4` pass, `0` fail, `0` pending, `0` skipped
- pytest: `108 passed`
- ruff: passed
- C++/CUDA tests: skipped because this is a Python/docs/fixture stage only

## GitHub Issue Status

Issue `Add solved-page golden fixture framework` should be updated with fixture counts, pass status, generated output path, and test result.

Issue `#4` was found, labeled with `solved-fixtures`, updated with the Stage 1A result, and closed after the framework, four passing direct fixtures, docs, tests, and generated-output ignore policy were verified.

## Git Safety

Raw sources, generated corpus candidates, generated solved-baseline outputs, `.venv`, caches, and `LiberPrimus-Research-Report.md` must not be staged.

Final pre-commit checks confirmed raw files, generated corpus-candidate outputs, generated solved-baseline outputs, and the local research report were ignored or unstaged.

## Known Limitations

The canonical corpus is inactive. Page boundaries remain reviewable. Only direct translation is implemented. Non-direct solved pages remain future work.

## Next Recommended Stage

Stage 1B: implement reverse Gematria / Atbash-family solved-page reproduction for clearly documented fixtures.
