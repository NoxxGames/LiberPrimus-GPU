# Experiments

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

The queue currently contains six items with total deterministic candidate estimate `780`: LP evidence Vigenere `48`, p56 local prime-minus-one offsets `256`, historical Vigenere `56`, family-specific negative controls `100`, reset/advance ablation `64`, and prime mod/gap `256`.

Stage 3E is an ingestion and dry-run stage. It does not execute items whose reset/advance, prime-offset, or family-specific negative-control executors are missing. Generated dry-run summaries remain ignored under `experiments/results/bounded-auto-runs/stage3e/`, and no candidate dumps, CUDA work, canonical corpus activation, page-boundary finalization, or solve claims are produced.

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
