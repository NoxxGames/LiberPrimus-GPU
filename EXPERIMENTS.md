# Experiments

## Experiment philosophy

Experiments are reproducible tests of hypotheses, not evidence of solves by themselves.

## Manifest-driven runs

Every real run must start from a YAML manifest that pins inputs, transforms, scorers, controls, and output policy.

Legacy workbook-derived records may support hypothesis generation, but they cannot be direct evidence of a solve.

Local-Pastebin-derived records may be used for parser validation and alignment hints only. They may not be direct evidence of a solve or direct GPU campaign input until canonical alignment is complete.

Stage 0D alignment outputs may inform future corpus selection and transcript-version policy. They cannot be used as direct solve evidence, and tentative boundary candidates require later review.

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
