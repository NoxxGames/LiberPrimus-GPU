# Experiments

## Stage 3Y Method Retirement And Result Synthesis

Stage 3Y does not add or execute an experiment. It records method-family status and retirement/deprioritisation guardrails in `data/research/` and documents them in `docs/roadmap/staged-plan.md` and `docs/experiments/method-retirement-ledger.md`.

Noisy, negative, or inconclusive families must not be widened unless their recorded reopen conditions are met and a new manifest explains the evidence. Cookie SHA-256 packs, broad Vigenere/dictionary expansion, Caesar/affine widening, Mersenne/perfect-number expansion, and CUDA acceleration all have explicit stop or defer conditions in the ledger.

## Stage 3Z Onboarding And Stage 4A Direction

Stage 3Z does not add or execute an experiment. It adds onboarding/source-of-truth maps and updates the staged plan so Stage 4A is full Discord research-bundle extraction for Deep Research. Stage 4A must create redacted, scoped, generated bundles only; raw Discord logs and private attachments remain local/ignored and uncommitted.

## Experiment philosophy

Experiments are reproducible tests of hypotheses, not evidence of solves by themselves.

## Manifest-driven runs

Every real run must start from a YAML manifest that pins inputs, transforms, scorers, controls, and output policy.

Legacy workbook-derived records may support hypothesis generation, but they cannot be direct evidence of a solve.

Local-Pastebin-derived records may be used for parser validation and alignment hints only. They may not be direct evidence of a solve or direct GPU campaign input until canonical alignment is complete.

Stage 0D alignment outputs may inform future corpus selection and transcript-version policy. They cannot be used as direct solve evidence, and tentative boundary candidates require later review.

Public tutorial examples must use smoke commands and summaries, not solve claims or generated candidate plaintext.

## Required manifest fields

Future manifests must include experiment ID, stage, hypothesis, corpus slice, transform chain, scorers, hardware requirements, success criteria, false-positive controls, output policy, and notes.

A future manifest may reference `legacy_source_id` for provenance hints, but canonical corpus locks must still be separate.

## Required run metadata

Runs must record git commit, manifest hash, corpus locks, tool versions, hardware metadata, timestamps, random seeds, and reviewer status.

## Result review process

Generated candidates require manual review, null-control comparison, score breakdown inspection, and reproducible reruns before escalation.

## Negative results

Negative results are useful and should be recorded with enough metadata to avoid repeating failed paths.

## Null controls

Null controls should include shuffled text, randomized keys, known non-solutions, and corpus slices that should not score well.

## Manual review

Manual review notes must distinguish promising output from solved evidence.

## Stage 3O Discord source promotion

Stage 3O promotion records are reviewable source-discovery leads, not experiment seeds. They may point reviewers toward public GitHub, archive, wiki, Reddit, Pastebin, Google, image, audio, or PDF sources, but Discord context itself is not source truth.

Generated promotion candidates and rejection lists remain ignored under `experiments/results/discord-promotion/stage3o/`. Any future experiment based on a promoted source must first promote the public source through a source-lock or observation registry step with independent provenance.

## Stage 3Q Discord review bundles

Stage 3Q topic shards are redacted AI-review aids, not experiment records or evidence. They may help reviewers find public sources, method claims, numeric observations, visual observations, and debunk notes. They must not be used as transform seeds until a later stage promotes selected leads through source/observation review with controls.

Generated review bundles remain ignored under `experiments/results/discord-review-bundles/stage3q/`. The committed aggregate contains counts and privacy flags only.

## Stage 3R Post-Discord Manifest Queue

Stage 3R promotes selected public-source and exact-observation leads, preserves negative controls, and creates disabled experiment manifests only. It does not execute the manifests.

Queued manifests:

- `EXP-3R-001 cookie_sha256_signed_variants_a`, candidate cap `576`.
- `EXP-3R-003 onion7_raw_prime_order_seed_pack_a`, candidate cap `144`.
- `EXP-3R-004 gp_rune_claim_verifier_a`, claim cap `64`.

All three keep `execution_enabled=false`, `cpu_only=true`, `cuda_enabled=false`, `cloud_execution=false`, `paid_services=false`, `generated_outputs_committed=false`, `no_solve_claim=true`, `canonical_corpus_active=false`, and `page_boundaries_final=false`.

Generated audit outputs remain ignored under `experiments/results/discord-lead-promotion/stage3r/`. Promoted records are review leads, not facts or solve evidence.

## Stage 3S Onion 7 Seed Pack

Stage 3S executes only `EXP-3R-003`, the Onion 7 explicit seed-pack manifest created in Stage 3R.

Run:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli post-discord validate-manifest `
  --manifest experiments/manifests/post-discord/EXP-3R-003-onion7-raw-prime-order-seed-pack-a.yaml
.\.venv\Scripts\python.exe -m libreprimus.cli post-discord run-onion7-seed-pack `
  --manifest experiments/manifests/post-discord/EXP-3R-003-onion7-raw-prime-order-seed-pack-a.yaml `
  --out-dir experiments/results/post-discord/stage3s `
  --top-k 25 `
  --allow-warnings
.\.venv\Scripts\python.exe -m libreprimus.cli post-discord summary `
  --results-dir experiments/results/post-discord/stage3s
```

The run enumerates `72` candidates from three value spaces, six routes, two directions, and two reset modes under a cap of `144`. Candidate streams reduce the selected Onion 7 sequence mod 29 and apply decrypt-subtract over transformable tokens only.

Generated candidate records, top-candidate JSONL, summary JSON, warnings, and calibrated score details remain ignored under `experiments/results/post-discord/stage3s/`. The top result is `inconclusive`, not solve evidence.

## Stage 3T GP/Rune Claim Verifier

Stage 3T executes only `EXP-3R-004`, the GP/rune claim verifier manifest created in Stage 3R.

Run:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli post-discord validate-gp-rune-manifest `
  --manifest experiments/manifests/post-discord/EXP-3R-004-gp-rune-claim-verifier-a.yaml
.\.venv\Scripts\python.exe -m libreprimus.cli post-discord run-gp-rune-verifier `
  --manifest experiments/manifests/post-discord/EXP-3R-004-gp-rune-claim-verifier-a.yaml `
  --promoted-observations data/observations/discord/stage3r-promoted-observation-records.yaml `
  --visual-observations data/observations/visual/visual-numeric-observations-v0.yaml `
  --out-dir experiments/results/post-discord/stage3t `
  --allow-warnings
.\.venv\Scripts\python.exe -m libreprimus.cli post-discord gp-rune-summary `
  --results-dir experiments/results/post-discord/stage3t
```

The run verifies exact promoted claims only. It does not search neighbouring spans, infer missing boundaries, process raw Discord logs, process raw page images, use CUDA, or claim a solve.

Generated verification records, per-status JSONL files, summary JSON, and warnings remain ignored under `experiments/results/post-discord/stage3t/`.

## Stage 3U Cookie Signed-Variant Pack

Stage 3U executes only `EXP-3R-001`, the cookie SHA-256 signed-variant manifest created in Stage 3R.

Run:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli post-discord validate-cookie-manifest `
  --manifest experiments/manifests/post-discord/EXP-3R-001-cookie-sha256-signed-variants-a.yaml
.\.venv\Scripts\python.exe -m libreprimus.cli post-discord run-cookie-signed-variants `
  --manifest experiments/manifests/post-discord/EXP-3R-001-cookie-sha256-signed-variants-a.yaml `
  --cookies data/observations/web/cookie-hash-records-v0.yaml `
  --out-dir experiments/results/post-discord/stage3u `
  --allow-warnings
.\.venv\Scripts\python.exe -m libreprimus.cli post-discord cookie-signed-summary `
  --results-dir experiments/results/post-discord/stage3u
```

The run generated `156` candidates before deduplication, tested `105` deduplicated byte strings against two target cookies for `210` exact SHA-256 comparisons, and found `0` exact matches.

Generated hash candidate records, exact-match JSONL, summary JSON, and warnings remain ignored under `experiments/results/post-discord/stage3u/`.

## Stage 3V OutGuess Regression Harness

Stage 3V runs only the explicit `outguess-regression-v1` manifest.

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli stego outguess-run `
  --manifest experiments/manifests/stego/outguess-regression-v1.yaml `
  --artifacts data/observations/stego/outguess-artifacts-v0.yaml `
  --out-dir experiments/results/stego/outguess/stage3v `
  --allow-missing-tool `
  --allow-missing-assets `
  --allow-warnings
```

The local run detected no OutGuess binary, so it recorded missing-tool skips. This is a valid harness result. Generated extraction records, tool records, summaries, synthetic inputs, and extracted payload directories remain ignored under `experiments/results/stego/outguess/stage3v/`.

Stage 3V does not scan all Liber Primus images, run non-OutGuess stego tools, process raw Discord logs, use CUDA, or claim a solve.

## Stage 3W State Consolidation

Stage 3W is not an experiment stage. It updates persistent project context and anti-drift checks only.

Stage 3W does not create experiment manifests, execute candidate generation, process raw data, run OutGuess, process Discord logs, process page images, use CUDA, activate the canonical corpus, finalize page boundaries, or claim a solve.

## Stage 0A smoke manifest

The Stage 0A smoke manifest validates project bootstrap only. No candidate plaintext is generated in Stage 0A.

## Stage 0D-followup diagnostic outputs

Stage 0D-followup alignment outputs may inform future corpus selection and separator policy. They cannot be used as direct solve evidence, direct GPU campaign input, or canonical page-boundary metadata. Future manifests may reference reviewed alignment summaries as provenance, but generated diagnostics must remain ignored unless explicitly promoted later.

## Stage 0E profile references

Future experiment manifests may reference `gematria-primus-v0`, `glyph-variants-v0`, and `rtkd-separator-grammar-v0` once Stage 0E validates. They must not treat `rtkd-master-v0-candidate` as active canonical corpus until a later activation stage.

## Stage 1A solved baseline gate

Solved-baseline reproduction should run before any future search campaign. Direct-translation fixtures are pre-experiment validation controls; they are not generated candidate evidence and do not justify search results by themselves.
## Stage 1B Baseline Gate

Atbash-family solved fixture reproduction is a pre-experiment validation step. Future search campaigns must preserve these known-solved baselines and direct-translation regressions before claiming experimental results.

Stage 1B does not authorize rotation search, Vigenere search, prime-stream search, scoring, or CUDA runs.
## Stage 1C Pre-Experiment Validation

Explicit-key Vigenere solved fixtures are now part of pre-experiment validation. Future Vigenere or running-key experiments must keep Stage 1A direct, Stage 1B Atbash-family, and Stage 1C Vigenere fixtures passing before search work begins.

Stage 1C does not permit key search or scoring. Any future search campaign must use separate manifests, null controls, and review criteria.

## Stage 1D Prime-Stream Gate

The p56 prime-minus-one fixture is now part of pre-experiment validation. Future prime-stream experiments must keep Stage 1A direct, Stage 1B Atbash-family, Stage 1C Vigenere, and Stage 1D p56 baselines passing before search work begins.

Stage 1D does not authorize offset sweeps, direction sweeps, prime-gap streams, scoring, CUDA kernels, or generic search campaigns.

## Stage 2A Solved-Baseline Manifest Gate

Stage 2A adds manifest-addressable solved-baseline runs. The all-known manifest reproduces 10 current solved fixtures through the CPU reference transform registry.

This is still pre-experiment validation, not an unsolved-page search campaign. Future experiment manifests should import or compare against these solved-baseline results before adding scorers, result stores, or search controls.

## Stage 2B Result-Store Foundation

Stage 2B adds a result-store manifest and generated JSONL/SQLite sinks for importing the Stage 2A solved-baseline regression run.

The result store records manifest SHA-256, registry SHA-256, git commit, host metadata, profile/source provenance, fixture counts, artifact records, and explicit false flags for canonical corpus activation, search, scoring, CUDA, and canonical trust.

Generated result-store files under `experiments/results/result-store/` remain ignored. The import is regression evidence for known solved fixtures only; it is not an unsolved-page experiment and does not authorize search campaigns.

## Stage 2D Consistency Gate

Stage 2D adds a consistency suite that checks schemas, manifests, registry metadata, result-store records, documentation status, and ignored-output rules before any new experiment scaffold is added.

Future experiment manifests should pass this consistency gate before they are used for dry runs or real runs. The gate does not run search, scoring, CUDA, or unsolved-page campaigns.

## Stage 2E Exploratory Dry-Run Planner

Stage 2E adds exploratory experiment manifests and a dry-run planner. The planner validates manifest safety gates, estimates candidate-count bounds, previews generated output paths, and writes ignored dry-run plan records.

Run:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli experiment stage2e-dry-run-all --manifest-dir experiments/manifests/exploratory --out-dir experiments/results/exploratory-dry-runs/stage2e --allow-warnings
```

This does not execute search, enumerate candidate plaintexts, score outputs, use CUDA, activate a canonical corpus, or finalize page boundaries.

## Stage 2F Bounded CPU Execution

Stage 2F adds CPU execution manifests and a bounded execution harness for synthetic and solved-fixture-only inputs.

Run:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli execution stage2f-run-all --manifest-dir experiments/manifests/cpu-execution --out-dir experiments/results/cpu-execution/stage2f --allow-warnings
```

The harness executes registered CPU reference transforms on synthetic records and records solved-fixture replay status. It rejects the committed blocked unsolved negative manifest and still does not run unsolved-page search, scoring, CUDA, canonical corpus activation, or page-boundary finalization.

## Stage 2G Proposal Workflow

Stage 2G adds proposal-only records under `experiments/proposals/stage2g/`. These describe future bounded exploratory experiments, review checklists, approval requirements, and candidate-count bounds.

Run:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli proposal stage2g-review-all --proposal-dir experiments/proposals/stage2g --out-dir experiments/results/proposal-reviews/stage2g --allow-warnings
```

Generated review packets are ignored under `experiments/results/proposal-reviews/stage2g/`. Stage 2G does not execute proposals, approve proposals automatically, generate candidates, score outputs, use CUDA, activate canonical corpus, or finalize page boundaries.

## Stage 2H Approval-Gated Control Execution

Stage 2H adds approval-gated request records under `experiments/proposals/stage2h/`. Approved examples are limited to synthetic direct translation and solved-fixture replay controls. A no-op real-proposal request remains blocked by a pending approval record and future-unsolved corpus-slice checks.

The `libreprimus approval-execution` CLI validates requests, builds plans, runs approved safe controls, and writes generated ignored results under `experiments/results/approval-gated-execution/stage2h/`. Stage 2H does not approve real unsolved-page execution, generate candidate plaintexts for unsolved pages, score outputs, use CUDA, activate canonical corpus, or finalize page boundaries.

## Stage 2I First Real Approval Packet

Stage 2I adds the first real bounded CPU exploratory proposal under `experiments/proposals/stage2i/`. The proposal references reviewable unsolved metadata only, keeps approval pending, and records Caesar plus affine mod-29 candidate-count bounds of `841`.

Run:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli approval-readiness stage2i-review --proposal-dir experiments/proposals/stage2i --out-dir experiments/results/approval-readiness/stage2i --allow-warnings
```

Generated readiness packets are ignored under `experiments/results/approval-readiness/stage2i/`. Stage 2I does not execute the proposal, approve it, generate candidates, score outputs, use CUDA, activate canonical corpus, or finalize page boundaries.

## Stage 2J Bounded Auto-Run Queue

Stage 2J adds the standing operator policy at `experiments/policies/operator-policy-v0.yaml` and the bounded queue at `experiments/queues/stage2j-bounded-cpu-queue.yaml`.

Policy-passing bounded local CPU queue items no longer require per-experiment approval. The policy still blocks over-budget work, CUDA/GPU campaigns, cloud or paid services, committing generated outputs, canonical corpus activation, page-boundary finalization, and solve claims.

The first queue contains:

- `stage2j-caesar-affine-first-reviewable-slice`, candidate upper bound `841`, policy-eligible and executable after Stage 3A when generated selector metadata exists locally.
- `stage2j-solved-baseline-regression-control`, solved-control upper bound `10`.
- `stage2j-blocked-overbudget-example`, deliberate policy-fail item with upper bound `100001`.

Generated bounded auto-run records are ignored under `experiments/results/bounded-auto-runs/stage2j/`.

## Stage 3A Bounded Caesar Affine Run

Stage 3A adds `libreprimus bounded-run run-caesar-affine` for the first bounded queue item. It enumerates Caesar shift mod 29 and affine mod 29 candidates over a generated reviewable index-29 slice, producing `29 + 812 = 841` candidates.

Run:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli bounded-run run-caesar-affine --policy experiments/policies/operator-policy-v0.yaml --queue experiments/queues/stage2j-bounded-cpu-queue.yaml --item-id stage2j-caesar-affine-first-reviewable-slice --out-dir experiments/results/bounded-auto-runs/stage3a --top-k 25 --allow-warnings
```

Generated `candidate_records.jsonl`, `top_candidates.jsonl`, `summary.json`, warnings, and result-store previews are ignored under `experiments/results/bounded-auto-runs/stage3a/`. Minimal triage scores are not solve evidence and must not be used to claim a page is solved.

## Stage 3B Lead Inspection And Reverse-Direction Queue

Stage 3B adds candidate-inspection tooling for the Stage 3A generated outputs, refines minimal triage scoring, reranks the original `841` candidates, and adds `experiments/queues/stage3b-bounded-cpu-queue.yaml`.

Run the inspection summary without committing full candidates:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli candidate-inspect inspect-stage3a --results-dir experiments/results/bounded-auto-runs/stage3a --top-n 25 --out-markdown research-log/2026-05-16-stage-3b-stage3a-lead-inspection.md
```

Run the bounded reverse-direction comparison:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli bounded-run run-caesar-affine --policy experiments/policies/operator-policy-v0.yaml --queue experiments/queues/stage3b-bounded-cpu-queue.yaml --item-id stage3b-caesar-affine-reverse-direction --out-dir experiments/results/bounded-auto-runs/stage3b/reverse_direction --top-k 25 --allow-warnings
```

Generated rerank and reverse-direction outputs remain ignored under `experiments/results/bounded-auto-runs/stage3b/`. Research logs may summarize top transform parameters, scores, and qualitative labels only. Stage 3B top candidates are leads, not solve evidence.

## Stage 3C Scoring Calibration

Stage 3C calibrates minimal triage scoring with solved-fixture positive controls, deterministic local null controls, synthetic negative controls, tiny crib checks, and Stage 3A/3B candidate leads.

Run:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli scoring calibrate --stage3-results-dir experiments/results/bounded-auto-runs/stage3a --stage3b-results-dir experiments/results/bounded-auto-runs/stage3b --out-dir experiments/results/scoring-calibration/stage3c --allow-warnings
```

Generated calibration records remain ignored under `experiments/results/scoring-calibration/stage3c/`. Stage 3C queued `stage3c-small-vigenere-known-motif-key-list` for Stage 3D because Stage 3A/3B leads remained `noisy` under calibrated controls.

## Stage 3D Small Vigenere Key-List Preview

Stage 3D runs the Stage 3C-selected queue item `stage3c-small-vigenere-known-motif-key-list`.

Run:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli bounded-run run-vigenere-key-list --policy experiments/policies/operator-policy-v0.yaml --queue experiments/queues/stage3c-bounded-cpu-queue.yaml --item-id stage3c-small-vigenere-known-motif-key-list --out-dir experiments/results/bounded-auto-runs/stage3d --top-k 4 --allow-warnings
```

The command tests exactly four declared keys: `LIBER`, `PRIMUS`, `DIVINITY`, and `CICADA`. It does not mutate keys, infer keys, search key lengths, use CUDA, or claim a solve.

Generated candidate records and summaries remain ignored under `experiments/results/bounded-auto-runs/stage3d/`. The committed research log records only top-key score metadata and the calibrated confidence label.

## Stage 3E Method Backlog And Bounded Queue

Stage 3E records the Deep Research method backlog and converts the top bounded methods into `experiments/queues/stage3e-bounded-cpu-queue.yaml`.

Run the dry-run count and support check:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli bounded-experiment dry-run-queue --policy experiments/policies/operator-policy-v0.yaml --queue experiments/queues/stage3e-bounded-cpu-queue.yaml --out-dir experiments/results/bounded-auto-runs/stage3e --allow-warnings
```

The queue currently contains seven items with total deterministic candidate estimate `972`: LP evidence Vigenere `48`, p56 local prime-minus-one offsets `256`, historical Vigenere `56`, family-specific negative controls `100`, reset/advance ablation `64`, prime mod/gap `256`, and Mersenne/perfect-number probe `192`.

Stage 3E is an ingestion and dry-run stage. It does not execute items whose family-specific negative-control or prime-neighbour stream executors are missing. Generated dry-run summaries remain ignored under `experiments/results/bounded-auto-runs/stage3e/`, and no candidate dumps, CUDA work, canonical corpus activation, page-boundary finalization, or solve claims are produced.

## Stage 3F Evidence-Key Vigenere Pack

Stage 3F runs the first Stage 3E item whose missing executor was implemented:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli bounded-run run-vigenere-key-pack `
  --policy experiments/policies/operator-policy-v0.yaml `
  --queue experiments/queues/stage3e-bounded-cpu-queue.yaml `
  --item-id stage3e_vig_lp_evidence_pack_v1 `
  --out-dir experiments/results/bounded-auto-runs/stage3f `
  --top-k 25 `
  --allow-warnings
```

The run is limited to the 12 declared LP evidence keys, reset modes `none` and `line`, and advance modes `runes_only` and `token_break_preserving`. Candidate count is `48`. Generated outputs remain ignored under `experiments/results/bounded-auto-runs/stage3f/`. The Stage 3F top candidate is classified `noisy`; no solve claim is made.

## Stage 3G p56-local prime offset sweep

Stage 3G runs the bounded p56-local prime-minus-one offset sweep:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli bounded-run run-prime-offset-sweep `
  --policy experiments/policies/operator-policy-v0.yaml `
  --queue experiments/queues/stage3e-bounded-cpu-queue.yaml `
  --item-id stage3e_prime_minus_one_offsets_v1 `
  --out-dir experiments/results/bounded-auto-runs/stage3g `
  --top-k 25 `
  --allow-warnings
```

The run is limited to offsets `0..63`, directions `forward` and `reverse`, and reset modes `none` and `line`, for `256` candidates. Generated outputs remain ignored under `experiments/results/bounded-auto-runs/stage3g/`. The Stage 3G top candidate is classified `inconclusive`; no solve claim is made.

Stage 3G also adds `stage3i_mersenne_prime_stream_tiny_v1` as a future `192` candidate probe. Stage 3J later promotes it to runnable through a dedicated bounded executor.

## Stage 3H reset/advance ablation

Stage 3H runs the bounded reset/advance ablation:

- Queue: `experiments/queues/stage3h-bounded-cpu-queue.yaml`
- Item: `stage3h_reset_advance_ablation_v1`
- Base transforms: four explicit Vigenere keys plus `prime_minus_one` offsets `0` and `1`, `prime_mod29` offset `0`, and `prime_gap` offset `0`
- Reset modes: `none`, `word`, `clause`, `line`
- Advance modes: `runes_only`, `token_break_preserving`
- Candidate count: `64`

The run executes all `64` candidates on the existing reviewable slice because word, clause, line, and token-break metadata are available. It also writes `100` family-specific negative controls. Generated outputs remain ignored under `experiments/results/bounded-auto-runs/stage3h/`. The top candidate is classified `noisy`; no solve claim is made.

## Stage 3I Historical Motif Vigenere Pack

Stage 3I runs the bounded historical motif Vigenere pack from the Stage 3E queue:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli bounded-run run-vigenere-key-pack `
  --policy experiments/policies/operator-policy-v0.yaml `
  --queue experiments/queues/stage3e-bounded-cpu-queue.yaml `
  --item-id stage3e_vig_history_key_pack_v1 `
  --out-dir experiments/results/bounded-auto-runs/stage3i `
  --top-k 25 `
  --allow-warnings
```

The run is limited to 14 declared historical motif keys, reset modes `none` and `line`, and advance modes `runes_only` and `token_break_preserving`, for `56` candidates. It does not mutate keys, infer keys, run a dictionary search, use CUDA, activate the canonical corpus, finalize page boundaries, or claim a solve.

Generated outputs remain ignored under `experiments/results/bounded-auto-runs/stage3i/`. The top candidate is classified `noisy`; no solve claim is made.

## Stage 3J Mersenne / Perfect-Number Probe

Stage 3J runs the bounded Mersenne/perfect-number stream probe:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli bounded-run run-mersenne-stream-probe `
  --policy experiments/policies/operator-policy-v0.yaml `
  --queue experiments/queues/stage3j-bounded-cpu-queue.yaml `
  --item-id stage3j_mersenne_prime_stream_tiny_v1 `
  --out-dir experiments/results/bounded-auto-runs/stage3j `
  --top-k 25 `
  --allow-warnings
```

The run is limited to the finite declared exponent sequence `2, 3, 5, 7, 13, 17, 19, 31`, three stream variants, offsets `0..15`, directions `forward` and `reverse`, and reset modes `none` and `line`, for `192` candidates.

Generated outputs remain ignored under `experiments/results/bounded-auto-runs/stage3j/`. Duplicate stream signatures are reported in the summary. The top candidate is classified `inconclusive`; no solve claim is made.

## Stage 3K Archive And Visual Observation Registry

Stage 3K creates a registry rather than an execution stage.

Run validation:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli archive validate-sources --records data/observations/archive/source-archive-records-v0.yaml
.\.venv\Scripts\python.exe -m libreprimus.cli observation validate-visual --records data/observations/visual/visual-numeric-observations-v0.yaml
.\.venv\Scripts\python.exe -m libreprimus.cli observation validate-cookies --records data/observations/web/cookie-hash-records-v0.yaml
```

Run the local image scan:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli archive scan-local-images `
  --source-dir third_party/LiberPrimusPages `
  --lock-out data/locks/third-party/liber-primus-pages/liber-primus-page-image-locks-v0.jsonl `
  --artifact-out data/observations/visual/liber-primus-page-image-artifacts-v0.jsonl `
  --summary-out experiments/results/archive-visual-registry/stage3k/local-image-scan-summary.json `
  --allow-missing
```

Raw page images stay ignored under `third_party/LiberPrimusPages/`. Generated scan summaries stay ignored under `experiments/results/archive-visual-registry/stage3k/`. Stage 3K executes no image-derived text experiments and makes no solve claim.

## Stage 3L Cookie Hash Preimage Packs

Stage 3L runs a bounded SHA-256 exact-match preimage check against the two archived 2013 cookie/hash artefacts:

- `cookie-2013-167-v0`
- `cookie-2013-761-v0`

The candidate packs are explicit and committed under `data/observations/web/hash-preimage-candidate-packs/`:

- `hist_cookie_literal_pack_v1`
- `hist_cookie_base29_numeric_pack_v1`

The run tests `1809` deduplicated candidate byte strings against `2` targets for `3618` exact comparisons. It finds `0` exact SHA-256 matches.

Generated outputs remain ignored under `experiments/results/hash-preimage/stage3l/`. Stage 3L does not use external dictionaries, fuzzy matching, partial matching, hashcat, GPU, live Tor, or solve claims.

## Stage 3M Deterministic Image Analysis

Stage 3M analyses local ignored Liber Primus page images with deterministic image features:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli image-analysis analyze-local-pages `
  --source-dir third_party/LiberPrimusPages `
  --image-locks data/locks/third-party/liber-primus-pages/liber-primus-page-image-locks-v0.jsonl `
  --out-dir experiments/results/image-analysis/stage3m `
  --allow-missing `
  --allow-warnings
```

The run analysed `58` local images and generated `406` component records, `58` symmetry records, `464` bitplane records, and `71` visual feature candidates.

Generated outputs remain ignored under `experiments/results/image-analysis/stage3m/`. Stage 3M does not run OCR, AI/ML interpretation, OutGuess extraction, audio analysis, image-derived cipher execution, CUDA, or solve claims.

## Stage 3N Discord HTML Source Discovery

Stage 3N scans admin-provided local Discord HTML exports as source-discovery material only:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli discord-ingest scan `
  --source-dir third_party/LiberPrimusDiscordChats `
  --out-dir experiments/results/discord-ingestion/stage3n `
  --allow-missing `
  --allow-warnings
```

The scanner computes local file locks, extracts redacted link and attachment candidates, emits
keyword-only method-claim and numeric-observation candidates, and creates a local ignored review
index. Generated outputs remain ignored under `experiments/results/discord-ingestion/stage3n/`.

Committed aggregate records contain counts only. Stage 3N does not scrape Discord, call live APIs,
commit message bodies or usernames, fetch attachments, execute extracted methods, activate the
canonical corpus, use CUDA, or claim a solve.

## Stage 3P Deterministic Image Transform Suite

Stage 3P generates deterministic visual review artefacts for local ignored Liber Primus page images:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli image-transform run-local-pages `
  --source-dir third_party/LiberPrimusPages `
  --image-locks data/locks/third-party/liber-primus-pages/liber-primus-page-image-locks-v0.jsonl `
  --out-dir experiments/results/image-transforms/stage3p `
  --allow-missing `
  --allow-warnings
```

The local run processed `58` images, emitted `37` transform names, generated `2077` derived review images, `59` contact sheets, `58` review pages, and `6` review-only visual transform candidates.

Generated images, HTML review pages, JSONL records, and summaries remain ignored under `experiments/results/image-transforms/stage3p/`. Stage 3P does not run OCR, AI/ML interpretation, OpenCV, OutGuess extraction, image-derived cipher execution, Discord processing, CUDA, or solve claims.
