# Approval Decision Guide

## Decision Scope

Stage 2I-followup does not approve or execute a proposal. It makes the review object clearer so the human can decide what should happen next.

## Option A: Approve Later Execution

Choose this only if the proposal summary, corpus selector, metadata paths, transform bounds, output policy, and stop conditions are acceptable.

The next step must create a separate approved approval record with proposal SHA-256, approver, timestamp, scope, constraints, and expiry. Approval still does not run the experiment unless a later execution stage is explicitly requested.

Suggested next prompt:

`Stage 2J - create an explicit approved approval record for stage2i-first-bounded-caesar-affine-review, scope-bound to the reviewed proposal, but do not execute it in the same step.`

## Option B: Revise Proposal

Choose this if metadata paths are missing, selector metadata is unclear, bounds are too broad, or stop conditions need tightening.

Suggested next prompt:

`Stage 2I-followup - revise stage2i-first-bounded-caesar-affine-review with clearer corpus metadata paths, bounds, or stop conditions; regenerate the review packet.`

## Option C: Deny Or Defer

Choose this if the proposal should not proceed as written.

Suggested next prompt:

`Stage 2J - record a denied or deferred decision for stage2i-first-bounded-caesar-affine-review and keep execution blocked.`

## What Approval Does Not Mean

Approval does not authorize CUDA, scoring, broader search, canonical corpus activation, page-boundary finalization, or a solve claim. Those require separate future stages and explicit instructions.
