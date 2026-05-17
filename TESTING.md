# Testing

## Test policy

Tests protect reproducibility and prevent false-positive drift.

## Unit tests

Unit tests cover small deterministic functions and placeholder status in Stage 0A.

## Integration tests

Integration tests will later cover manifest execution and result writing.

## Golden tests

Golden tests will later reproduce known solved-page behavior from locked fixtures. None are included in Stage 0A.

Stage 0B adds conditional real-workbook tests that run only when the ignored legacy workbook is locally present.

## Property tests

Property tests will later check transform invariants, inverse behavior, and edge cases.

Synthetic workbook parser tests cover inventory, solved-delta extraction, modulo validation, Prime Sums booleans, formula inventory, deterministic output, and CLI behavior.

## Fuzz tests

Fuzz tests will later target parsers, manifest loading, corpus normalization, and transform composition.

## CPU/GPU parity tests

Every CUDA kernel must match a CPU reference implementation across representative inputs and edge cases.

## Manifest determinism tests

Manifests must replay to the same outputs under pinned inputs and fixed seeds.

## Documentation consistency tests

Documentation checks should verify core policy statements such as raw-data immutability and Stage 0A restrictions.

Legacy workbook tests include p56 prime-minus-one first-delta checks, Welcome `DIVINITY` delta checks, and direct-page zero-delta checks for solved fixture hints.

Legacy Pastebin tests include first-pair prime validation, empty-pair preservation, Parable anchor detection, page-boundary non-finalization, and local-real-file conditional tests.

Stage 0D tests cover rtkd parser preservation, scream314 reference parsing, signature indexing, Pastebin-to-transcript alignment, tentative page-boundary candidates, glyph variant `ᛂ`, CLI commands, and real-source conditional smoke checks.

## Stage 0A smoke tests

Stage 0A includes C++ and Python smoke tests only.

## Stage 0B workbook tests

Stage 0B parser tests are Python-only. CUDA and C++ behavior are unchanged.

## Stage 0C Pastebin tests

Stage 0C parser tests are Python-only. They verify that prime values are converted to decimal indices and that generated records remain non-canonical.

## Stage 0D alignment tests

Stage 0D parser and alignment tests are Python-only. They assert no canonical boundary activation, no canonical trust flag, raw glyph preservation, and timing metadata presence.

## Stage 0D-P documentation and GitHub checks

Stage 0D-P validates tutorial, issue seed, wiki source, and GitHub script existence. GitHub helper scripts support dry runs before mutating labels, issues, or wiki pages.

## Stage 0D-followup parser, alignment, and boundary tests

Stage 0D-followup tests cover transcript physical/logical/stream views, bounded stream-subsequence matching, gap diagnostics, stricter boundary confidence auditing, CLI commands, and real-source conditional smoke checks. Tests assert that empty-pair-only and word-length-only evidence cannot create high-confidence boundaries, all boundaries keep `canonical_page_boundary=false`, and all alignment records remain non-canonical.

## Stage 0E profile and corpus candidate tests

Stage 0E tests validate Gematria profile invariants, glyph variant profile policy, separator grammar rules, corpus tokenization, JSON schemas, synthetic candidate generation, real-source conditional generation, and CLI commands.

## Stage 1A solved fixture tests

Stage 1A tests validate fixture schemas, direct-translation decoding, span selection, provenance validation, synthetic reproduction, real-source conditional reproduction, and solved-fixture CLI commands. They assert that direct fixtures do not use Atbash, Vigenere, prime streams, search, or CUDA.
## Stage 1B Tests

Stage 1B adds tests for reverse Gematria and rotated reverse Gematria formulas, explicit rotation validation, fixture schema compatibility, synthetic Atbash-family reproduction, direct-fixture regression, CLI smoke behavior, and real-source conditional reproduction.

Run:

```powershell
.\.venv\Scripts\python.exe -m pytest -q tests/python
.\.venv\Scripts\python.exe -m ruff check python/libreprimus tests/python
```

C++ tests are not required for Stage 1B unless C++ files change.
## Stage 1C Tests

Stage 1C tests cover reference mirroring metadata, reference-method extraction, explicit-key Vigenere key conversion, subtract decryption, key-advance rules, fixture-declared cleartext-F pass-through, fixture schema validation, synthetic reproduction, CLI commands, and real-source conditional reproduction.

The Stage 1C smoke keeps Stage 1A direct and Stage 1B Atbash-family fixtures as regressions.

## Stage 1D Tests

Stage 1D tests cover deterministic prime generation, prime-minus-one / phi-prime equivalence, stream advancement rules, cleartext-F skip handling, payload hash checks, fixture schema validation, synthetic reproduction, CLI commands, and real-source conditional reproduction.

The Stage 1D smoke keeps Stage 1A direct, Stage 1B Atbash-family, and Stage 1C Vigenere fixtures as regressions. C++ tests are not required for Stage 1D unless C++ files change.

## Stage 2A Tests

Stage 2A tests cover transform registry metadata, SHA-256 locks, alias resolution, CPU dispatch, manifest schema validation, synthetic solved-baseline runner outputs, CLI commands, and real-source conditional smoke checks.

The Stage 2A smoke reproduces 10 known solved fixtures through registry dispatch. C++ tests are not required for Stage 2A unless C++ files change.

## Stage 2B Tests

Stage 2B tests cover result-store JSON schemas, JSONL sink determinism, SQLite table creation and duplicate handling, provenance capture, solved-baseline import, CLI commands, and real-source conditional smoke checks.

The Stage 2B smoke imports the Stage 2A all-known solved-baseline run into generated JSONL and SQLite result stores. C++ tests are not required for Stage 2B unless C++ files change.

## Stage 2C Tests

Stage 2C adds static workflow tests and CI script tests. They verify `.github/workflows/ci.yml` runs on push and pull requests, uses Python 3.12, runs Ruff and pytest, validates the transform registry and committed manifests, avoids secrets and artifact uploads, and keeps scripts raw-data-free.

Local CI reproduction:

```powershell
.\scripts\ci\run-python-ci.ps1
.\scripts\ci\run-schema-manifest-checks.ps1
.\scripts\ci\validate-workflow-static.ps1
```

The GitHub Actions workflow also includes a CPU-only CMake smoke job with CUDA disabled.

Stage 2C-followup extends workflow tests to parse YAML with PyYAML, validate trigger and job structure, and reject flattened/minified workflow files.

Stage 2C-followup-2 adds post-push remote workflow verification scripts and strengthens static tests with an explicit minified workflow rejection sample.

Stage 2C-followup-3 adds `.gitattributes` static tests and canonical lock-hash line-ending tests. CI now verifies lock hashes before Python tests.

Stage 2C-followup-4 adds public documentation status tests for README, STATUS, and ROADMAP. These tests allow historical stage mentions but reject stale top-level current-status and next-milestone language.

Stage 2C-followup-5 adds remote Git blob verifier tests that require post-push workflow and `.gitattributes` checks to use `git show` as the authoritative remote source and treat raw URL mismatches as warnings.

## Stage 2D Consistency Tests

Stage 2D adds tests for consistency models, registry checks, manifest checks, schema checks, documentation checks, ignored-output checks, result-store checks, and CLI behavior.

## Stage 2E Dry-Run Planner Tests

Stage 2E adds tests for exploratory schemas, candidate-count estimators, safety gates, dry-run planner records, committed exploratory manifests, and `libreprimus experiment` CLI commands.

The tests assert that dry-run plans preserve disabled execution/search/candidate-generation/scoring/CUDA flags and do not include candidate plaintext fields.

## Stage 2F Bounded CPU Execution Tests

Stage 2F adds tests for CPU execution schemas, safety gates, synthetic execution, solved-fixture replay, blocked unsolved execution, CLI behavior, and committed manifest files.

The tests assert that synthetic direct, reverse, rotated reverse, Vigenere, and prime-stream examples pass; the blocked unsolved manifest fails; and search, candidate generation, scoring, and CUDA remain disabled.

## Stage 2G Proposal Approval Tests

Stage 2G adds tests for proposal schemas, approval records, approval gates, review packet generation, CLI behavior, and committed proposal files.

The tests assert that pending, denied, missing, invalid, expired, and mismatched approvals block execution; committed Stage 2G proposals are unapproved and non-executable; and review packets contain no candidate plaintext outputs.

## Stage 2H Approval-Gated Execution Tests

Stage 2H adds tests for approval-gated request schemas, approval gate behavior, approved synthetic and solved-control execution, blocked no-op real proposals, CLI behavior, and committed Stage 2H files.

The tests assert that proposal SHA, scope, expiry, approver, and constraints are checked; approved synthetic and solved-control requests pass; no approval, pending approval, denied approval, expired approval, wrong scope, mismatched SHA, and future-unsolved proposals block; and search, candidate generation, scoring, and CUDA remain disabled.

## Stage 2I Approval-Readiness Tests

Stage 2I adds tests for approval-readiness packet schemas, readiness analysis, packet generation, committed proposal files, CLI behavior, and no-execution guarantees.

The tests assert that the first real proposal remains pending and unapproved, candidate-count estimate and upper bound are `841`, generated packets contain no raw unsolved text or candidate plaintext, no approved Stage 2I approval records are committed, and approval-readiness commands do not invoke the execution runner.

## Stage 2J Bounded Auto-Run Tests

Stage 2J adds tests for operator policies, bounded queues, policy checking, bounded runner behavior, and `libreprimus bounded-experiment` CLI commands.

The tests assert that the `841` candidate Caesar plus affine item passes policy, the solved-baseline control passes policy, over-budget/CUDA/cloud/solve-claim/generated-output-commit items fail policy, blocked items do not run, generated outputs are ignored, and per-experiment approval is not required for policy-passing bounded local CPU items.

## Stage 3A Minimal Executor Tests

## Stage 3J Mersenne Probe Tests

Stage 3J adds tests for finite exponent-sequence loading, modular stream values, forward/reverse indexing, reset handling, cyclic exponent behavior, duplicate stream-signature detection, output record fields, CLI execution on synthetic input, generated-output ignore policy, and policy blocking when offsets expand without a matching candidate-count update.

Run:

```powershell
.\.venv\Scripts\python.exe -m pytest -q tests/python/test_stage3j_mersenne_stream_values.py tests/python/test_stage3j_mersenne_executor.py tests/python/test_stage3j_mersenne_cli.py tests/python/test_stage3j_mersenne_output.py tests/python/test_stage3j_queue.py
```

## Stage 3K Archive And Visual Registry Tests

Stage 3K adds tests for source/archive records, source-class vocabulary, noncanonical flags, synthetic image scanning, prime dimension helpers, missing-image handling, committed image lock validation, visual numeric observations, cookie/hash records, CLI commands, ignored raw images, ignored generated scan outputs, and trackable registry JSONL files.

Run:

```powershell
.\.venv\Scripts\python.exe -m pytest -q tests/python -k stage3k
```

Stage 3A adds tests for minimal triage scoring, Caesar and affine enumeration counts, candidate output schemas, generated-output ignore policy, policy blocking, and `libreprimus bounded-run` CLI behavior.

The tests assert that scoring is deterministic, Caesar generates `29` candidates, affine generates `812` candidates, total candidate count is `841`, output indices stay in `0..28`, candidate records and run summaries validate, top-k output is bounded, CUDA stays false, solve claims stay false, and synthetic CLI runs work without raw corpus data.

## Stage 3B Inspection And Scoring Tests

Stage 3B adds tests for candidate inspection, refined triage scoring, Stage 3A reranking, reverse-direction Caesar/affine transforms, and the Stage 3B bounded queue.

The tests assert that candidate records load from JSONL, inspection summaries group by transform and score distribution, noisy candidates stay noisy, readable synthetic controls score better, tiny impossible-bigram and repeated-symbol penalties work, reranking can change top order, reverse Caesar and affine inverse formulas are correct, reverse affine produces `812` candidates, total reverse candidates remain `841`, generated outputs are ignored, and no solve claims are made.

## Stage 3C Scoring Calibration Tests

Stage 3C adds tests for positive-control loading, deterministic null controls, crib checks, calibration summaries, scoring CLI commands, and the Stage 3C bounded queue.

The tests assert that solved fixture controls load, null controls are deterministic and length-matched, negative controls remain noisy or garbage, crib hits do not imply solve claims, calibration summaries validate, confidence labels are assigned, noisy synthetic candidates stay noisy or garbage, readable synthetic controls classify as positive/plausible, generated outputs are ignored, and the next queue item stays under policy.

## Stage 3D Small Vigenere Key-List Tests

Stage 3D adds tests for exact key-list loading, key expansion rejection, Gematria key mapping, explicit-key Vigenere execution, CLI execution, output schema validation, ignored generated outputs, queue candidate counts, and policy blocking when declared keys exceed the candidate bound.

The tests assert that the Stage 3D key list remains exactly `LIBER`, `PRIMUS`, `DIVINITY`, and `CICADA`; the run produces exactly four candidates; candidate records include `key_text`, `key_indices`, calibrated confidence labels, `cuda_used=false`, and `solve_claim=false`; and generated Stage 3D outputs remain ignored.

## Stage 3E Method Backlog Tests

Stage 3E adds tests for method backlog schemas, bounded queue candidate counts, executor-support classification, dry-run CLI behavior, and no-scope-creep rules.

The tests assert that the Stage 3E/3G/3J backlog items validate, LP evidence Vigenere count is `48`, p56 local prime-minus-one offset count is `256`, historical Vigenere count is `56`, negative-control count is `100`, reset/advance ablation count is `64`, prime mod/gap count is `256`, Mersenne probe count is `192`, every item fits operator-policy limits, CUDA stays disabled, solve claims stay false, broad dictionary search and unconstrained skip masks are absent, dry-run output is ignored, and missing executors are reported instead of faked.

## Stage 3F Vigenere Key-Pack Tests

Stage 3F adds tests for the evidence-key Vigenere pack executor, CLI, generated output shape, and queue integration.

The tests assert that the LP evidence pack loads exactly 12 keys, rejects key expansion without a count update, computes `12 * 2 * 2 = 48` candidates, maps all keys through the Gematria profile, executes `none` reset, executes or explicitly defers `line` reset based on line metadata, executes or warns for `token_break_preserving` based on token-break metadata, writes key/reset/advance metadata in candidate records, keeps `cuda_used=false` and `solve_claim=false`, blocks candidate-count drift, and leaves generated outputs ignored.

## Stage 3G Prime Offset Sweep Tests

Stage 3G adds tests for deterministic prime generation, prime-minus-one stream values, offset/direction/reset candidate counts, forward and reverse stream indexing, reset-mode handling, CLI execution, generated output shape, Mersenne backlog metadata, and queue-runner integration.

The tests assert that the first ten primes are stable, the p56-local sweep computes `64 * 2 * 2 = 256` candidates, line reset executes with line metadata or defers with an explicit warning, candidate records include offset/direction/reset metadata, `cuda_used=false`, `solve_claim=false`, calibrated confidence labels are present, generated Stage 3G outputs are ignored, the Mersenne probe is promoted to Stage 3J runnable status, and offset expansion without a count update is blocked.

## Stage 3H Reset/Advance Ablation Tests

Stage 3H adds tests for the reset/advance state machine, transform adapters, family-specific negative controls, CLI execution, generated output shape, and queue policy.

The tests assert that reset `none` uses the whole sequence, reset `line` segments by line metadata, reset `word` and `clause` require metadata, missing metadata emits explicit warnings instead of fake segmentation, `runes_only` advances only transformable tokens, `token_break_preserving` preserves separators, Vigenere and prime-stream adapters work on synthetic tokens, the ablation count is `64`, executed plus deferred counts match, negative controls are deterministic, generated outputs are ignored, `cuda_used=false`, and `solve_claim=false`.

## Stage 3I Historical Vigenere Pack Tests

Stage 3I adds tests for the historical motif Vigenere key pack, generic key-pack CLI execution, generated output shape, evidence-family metadata, and queue support classification.

The tests assert that the historical pack loads exactly 14 declared keys, computes `14 * 2 * 2 = 56` candidates, maps all keys through the Gematria profile, rejects key expansion without a candidate-count update, executes reset `none`, executes or explicitly defers reset `line` based on line metadata, executes `runes_only`, executes or warns for `token_break_preserving`, writes `evidence_family=historical_motif_key_pack`, keeps `cuda_used=false`, keeps `solve_claim=false`, includes calibrated confidence labels, and leaves generated outputs ignored.

The consistency suite is raw-data-free. It validates generated result-store outputs only when they are present locally; missing generated outputs are warnings, not CI failures.
