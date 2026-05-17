# How To Review An Experiment Proposal

## Purpose

The reviewer should not need to audit scattered YAML or internal code before making a decision. The approval-readiness packet is the self-contained review object.

## What The Packet Does

The packet performs mechanical checks automatically:

- proposal and approval file paths;
- proposal and approval SHA-256 values;
- corpus slice ID, kind, source, selector, and metadata paths;
- raw unsolved text inclusion check;
- candidate-count bounds;
- disabled execution, search, candidate generation, scoring, and CUDA flags;
- inactive canonical corpus and non-final page boundaries;
- ignored generated-output paths.

## What The Human Decides

The human decision is limited to:

- approve later execution in a separate stage;
- revise the proposal;
- deny or defer the proposal.

Approval-readiness packets are not approvals. Approval also does not execute anything by itself; a later stage must still perform any run explicitly.

## Regenerate The Packet

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli approval-readiness packet `
  --proposal experiments/proposals/stage2i/stage2i-first-bounded-caesar-affine-review.yaml `
  --approval experiments/proposals/stage2i/approval-records/stage2i-first-bounded-caesar-affine-pending-approval.yaml `
  --out-dir experiments/results/approval-readiness/stage2i `
  --allow-warnings
```

## Inspect Review Paths

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli approval-readiness inspect-paths `
  --proposal experiments/proposals/stage2i/stage2i-first-bounded-caesar-affine-review.yaml
```

## Corpus Metadata Paths

The packet lists each known metadata path and whether it exists. If no standalone corpus metadata file is referenced by the proposal, the packet says so directly and recommends revision or explicit acceptance of the embedded selector metadata.

## Missing Metadata Path

Do not guess. Ask for a revised proposal that names a standalone metadata file, or explicitly decide that the embedded selector metadata is enough for the next stage.

## Why Approval Exists

Approval separates human review from execution. It prevents a proposal from becoming a run by accident and keeps unsolved-material work behind explicit scope, constraints, expiry, and stop conditions.
