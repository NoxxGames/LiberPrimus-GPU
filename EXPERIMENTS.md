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
