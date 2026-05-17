# First Real Exploratory Proposal

## Purpose

Stage 2I creates the first review packet for a real bounded CPU exploratory proposal. It touches reviewable unsolved-material metadata only and does not execute transforms, generate outputs, score candidates, or approve a run.

## Proposal ID

The first proposal is `stage2i-first-bounded-caesar-affine-review`.

It lives at `experiments/proposals/stage2i/stage2i-first-bounded-caesar-affine-review.yaml` and remains `ready_for_review`, `approved_for_execution=false`, and `execution_enabled=false`.

## Corpus Slice

The proposal references a `future_unsolved_page_candidate` slice with `review_required=true`. It records selector and source metadata only. It must not include raw unsolved text, transcript dumps, or candidate plaintext.

## Transform-Space Preview

The proposed transform space is a bounded preview:

- Caesar shift preview: `29` candidate-count estimate.
- Affine mod-29 preview: `812` candidate-count estimate.

Both are proposal counts only. Stage 2I does not run either transform.

## Candidate Count

The combined preview count is `841`, with `candidate_count_upper_bound: 841`.

## Review Checklist

The proposal checklist asks reviewers to confirm corpus-slice acceptability, page-boundary handling, transform bounds, output policy, result-store policy, solve-claim restrictions, and stop conditions.

## Approval Status

The committed approval record is pending:

`experiments/proposals/stage2i/approval-records/stage2i-first-bounded-caesar-affine-pending-approval.yaml`

No approved Stage 2I approval record is committed.

## Why It Is Not Executable Yet

The proposal has `approved_for_execution=false`, `execution_enabled=false`, `search_execution_enabled=false`, `candidate_generation_enabled=false`, `scoring_enabled=false`, and `cuda_enabled=false`.

Approval-readiness packets are not approvals. A later human decision must explicitly approve, deny, or revise the proposal before any execution path can be considered.

## Human Decision

A future reviewer must decide whether the corpus slice, transform bounds, output policy, result-store policy, and stop conditions are acceptable. Approval must be recorded in a separate approval record with scope, constraints, approver, timestamp, expiry, and matching proposal SHA-256.

Stage 2I-followup generates a self-contained Markdown review packet named `stage2i-first-bounded-caesar-affine-review.review.md`. The packet includes machine checks and exact paths so the reviewer can decide approve, revise, or deny without manually auditing scattered YAML.

## Stop Conditions

Stop before execution if any approval is missing, expired, mismatched, out of scope, or tries to enable search, candidate generation, scoring, CUDA, canonical corpus activation, or page-boundary finalization.
