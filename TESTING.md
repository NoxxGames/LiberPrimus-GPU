# Testing

## Test policy

Tests protect reproducibility and prevent false-positive drift.

## Unit tests

Unit tests cover deterministic parsing, schema validation, manifest safety, bounded executor behavior, fake-tool wrappers, scoring helpers, and consistency policies.

## Integration tests

Integration tests cover raw-data-free CLI paths, manifest validation, synthetic execution paths, generated-output ignore rules, and local CI reproduction scripts.

## Golden tests

Golden solved-baseline tests reproduce the committed known solved fixtures through the CPU transform registry and manifest path. They are regression evidence, not new solve claims.

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

Documentation and anti-drift checks verify core policy statements such as raw-data immutability, generated-output ignore rules, current completed stage, canonical corpus inactive status, page-boundary review status, CUDA deferral, Discord privacy, and no-solve-claim policy.

## Stage 3W State-Drift Tests

Stage 3W tests cover the state-drift checker, stale current-stage phrase detection, historical-reference allowances, required CUDA/corpus/page-boundary/raw-output/Discord privacy facts, pyproject metadata, persistent doc current-state coverage, and CLI integration through `libreprimus consistency check-state-drift`.

## Stage 3X CLI Command-Surface Tests

Stage 3X tests cover the modular CLI package layout, the thin public `python -m libreprimus.cli` entrypoint, preserved root command groups, selected high-risk subcommands, help output, and the rule that no `python/libreprimus/cli/` package may exist while `cli.py` remains the public module.

## Stage 3Y Research Synthesis Tests

Stage 3Y tests cover the durable staged plan, research synthesis schemas, method-family status records, method-retirement references, Deep Research influence records, direction-change records, `libreprimus research-synthesis` CLI commands, and state-drift integration for `docs/roadmap/staged-plan.md`.

The local validation stack now includes:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli research-synthesis validate --data-dir data/research --staged-plan docs/roadmap/staged-plan.md
```

## Stage 3Z Onboarding And Source-Of-Truth Tests

Stage 3Z tests cover onboarding docs, Stage 4A direction in the staged plan, direction-change records, AGENTS doc freshness policy, private/generated data maps, and state-drift integration for the new onboarding maps.

## Stage 4A Discord Full Review Bundle Tests

Stage 4A tests cover full-review schemas, synthetic Discord-like HTML parsing, redaction of
usernames/IDs/message IDs/private Discord URLs, public-link preservation, low-signal message
retention, huge-channel shard splitting, multi-topic classification, image and attachment reference
indexes, synthetic LP page-gallery thumbnails, static-site generation, Deep Research manifests, SFTP
instructions, aggregate privacy checks, Wiki publish diagnostics, generated-output ignore rules, and
CLI build/validate/summary paths using synthetic fixtures.

Stage 4A follow-up tests cover static review-site privacy hardening: noindex metadata, all-disallow
`robots.txt`, site privacy notice, SFTP upload checklist, optional `.htaccess` guidance, deterministic
site manifests, validation failures when noindex metadata is missing, and Wiki publish blocker
reporting.

Local validation includes:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli discord-full-review validate --results-dir experiments/results/discord-full-review/stage4a
```

## Stage 3O Promotion And Wiki Tests

Stage 3O tests cover Discord promotion redaction, public-safe URL filtering, review-only promotion records, README/tutorial coverage, Wiki source generation, Wiki validation scripts, and ignored raw/generated paths.

Local validation includes:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli discord-promote validate-promoted --links data/observations/discord/promoted-public-source-links-stage3o.yaml --methods data/observations/discord/promoted-method-claim-candidates-stage3o.yaml --numerics data/observations/discord/promoted-numeric-observation-candidates-stage3o.yaml --allow-empty
.\scripts\github\validate-wiki-source.ps1
.\scripts\github\sync-tutorials-to-wiki.ps1 --DryRun
```

## Stage 3Q Discord Review Bundle Tests

Stage 3Q tests cover schema parsing, redaction of usernames/IDs/private URLs, preservation of public external URLs, topic classification, review lead construction, shard privacy headers, shard splitting, local review-index generation, CLI missing-input mode, aggregate privacy flags, and ignored generated shard paths.

Local validation includes:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli discord-review validate-bundles `
  --results-dir experiments/results/discord-review-bundles/stage3q `
  --aggregate data/observations/discord/discord-review-bundle-aggregate-stage3q.yaml `
  --allow-missing
```

## Stage 3R Discord Lead Promotion Tests

Stage 3R tests cover schema validation, public/private URL corroboration, Discord-only claim rejection, promoted source and observation records, negative-control classes, disabled manifest caps, CLI promote/build/validate behavior, privacy policy checks, and ignored generated outputs.

Local validation includes:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli discord-leads validate `
  --promoted-sources data/observations/discord/stage3r-promoted-source-records.yaml `
  --promoted-observations data/observations/discord/stage3r-promoted-observation-records.yaml `
  --negative-controls data/observations/discord/stage3r-negative-control-records.yaml `
  --manifest-dir experiments/manifests/post-discord `
  --allow-empty
```

## Stage 3S Onion 7 Seed-Pack Tests

Stage 3S tests cover manifest validation, candidate cap checks, raw 4x4 table shape, deterministic route builders, mod-29 reduction, stream repetition, reset behavior, candidate record fields, CLI validation and execution against a synthetic manifest, ignored generated outputs, raw Discord ignore policy, and raw image ignore policy.

Local validation includes:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli post-discord validate-manifest `
  --manifest experiments/manifests/post-discord/EXP-3R-003-onion7-raw-prime-order-seed-pack-a.yaml
.\.venv\Scripts\python.exe -m libreprimus.cli post-discord summary `
  --results-dir experiments/results/post-discord/stage3s
```

## Stage 3T GP/Rune Claim Verifier Tests

Stage 3T tests cover manifest validation, claim-cap checks, claim deduplication, malformed and unsupported claim classification, missing-span handling, synthetic rune counts, transformable-rune counts, GP sums, mod-29 residues, derived cuneiform arithmetic, boundary-sensitive classification, CLI validation/execution against synthetic records, ignored generated outputs, raw Discord ignore policy, raw image ignore policy, and no-solve flags.

Local validation includes:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli post-discord validate-gp-rune-manifest `
  --manifest experiments/manifests/post-discord/EXP-3R-004-gp-rune-claim-verifier-a.yaml
.\.venv\Scripts\python.exe -m libreprimus.cli post-discord gp-rune-summary `
  --results-dir experiments/results/post-discord/stage3t
```

## Stage 3U Cookie Signed-Variant Tests

Stage 3U tests cover manifest validation, candidate-cap checks, SHA-256-only enforcement, cookie-record loading, hex64 validation, deterministic byte variants, compact variants, deduplication, cap-exceeded failure, exact-match output generation, no partial/fuzzy matching, CLI validation/execution against synthetic records, ignored generated outputs, raw Discord ignore policy, raw image ignore policy, and no-solve/CUDA flags.

Local validation includes:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli post-discord validate-cookie-manifest `
  --manifest experiments/manifests/post-discord/EXP-3R-001-cookie-sha256-signed-variants-a.yaml
.\.venv\Scripts\python.exe -m libreprimus.cli post-discord cookie-signed-summary `
  --results-dir experiments/results/post-discord/stage3u
```

## Stage 3V OutGuess Regression Tests

Stage 3V tests cover stego schemas, manifest/artifact validation, missing-tool skips, missing-asset skips, fake OutGuess success and failure, exact expected-payload hash matching, expected-payload hash mismatch, no raw payload commits, no solve claims, CUDA-off flags, CLI detection/validation/run behavior, generated output ignore rules, third-party artefact ignore rules, raw Discord ignore rules, and raw page-image ignore rules.

Local validation includes:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli stego outguess-validate-manifest `
  --manifest experiments/manifests/stego/outguess-regression-v1.yaml `
  --artifacts data/observations/stego/outguess-artifacts-v0.yaml
.\.venv\Scripts\python.exe -m libreprimus.cli stego outguess-summary `
  --results-dir experiments/results/stego/outguess/stage3v
```

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

## Stage 3L Hash Preimage Tests

Stage 3L adds tests for cookie record loading, `hex64` validation, candidate pack validation, SHA-256-only enforcement, no-external-dictionary flags, byte variants, base29 rendering, SHA-256 known vectors, exact match detection, no fuzzy/partial matching, generated output schemas, CLI commands, ignored generated outputs, and `solve_claim=false`.

Run:

```powershell
.\.venv\Scripts\python.exe -m pytest -q tests/python -k stage3l
```

## Stage 3M Image Analysis Tests

Stage 3M adds tests for synthetic grayscale statistics, threshold ratios, deterministic 4-connected component counts, symmetry metrics, bit-plane ratios, visual feature candidate flags, generated output schemas, CLI commands, missing-image raw-data-free mode, ignored generated outputs, ignored raw images, and `solve_claim=false`.

## Stage 3N Discord Ingestion Tests

Stage 3N adds tests for Discord ingestion schemas, synthetic HTML file locks, missing-directory
`--allow-missing` behavior, href/src/plaintext URL extraction, source-domain classification,
Discord attachment URL redaction, keyword-only method-claim extraction, numeric observation
extraction, aggregate privacy policy checks, CLI scan/validate/export commands, ignored generated
outputs, ignored raw Discord logs, and no live API or scrape requirements.

## Stage 3P Image Transform Tests

Stage 3P adds tests for transform schemas, grayscale/invert/threshold previews, RGB channel splits, bitplane previews, edge maps, split/mirror differences, component overlays, contact sheets, review index generation, visual transform candidate safety flags, CLI raw-image-free mode, ignored generated outputs, ignored raw page images, ignored raw Discord logs, and no OCR/AI/OpenCV dependency requirement.

Run:

```powershell
.\.venv\Scripts\python.exe -m pytest -q tests/python -k stage3m
.\.venv\Scripts\python.exe -m pytest -q tests/python -k stage3p
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
