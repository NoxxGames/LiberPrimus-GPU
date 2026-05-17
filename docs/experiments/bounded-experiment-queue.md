# Bounded Experiment Queue

The Stage 2J queue is committed at `experiments/queues/stage2j-bounded-cpu-queue.yaml`.

## Queue Items

The queue contains:

- `stage2j-caesar-affine-first-reviewable-slice`: policy conversion of the Stage 2I Caesar plus affine reviewable-slice proposal, upper bound `841`.
- `stage2j-solved-baseline-regression-control`: solved-baseline control item, upper bound `10`.
- `stage2j-blocked-overbudget-example`: deliberate over-budget negative control, upper bound `100001`.

## Execution Behavior

Policy-passing items do not require per-experiment approval. Items above policy limits are blocked and must not run.

The first reviewable Caesar plus affine item is policy-eligible. It was deferred in Stage 2J, and Stage 3A adds the minimal safe real executor for the `841` candidate run when generated selector metadata exists locally. Generated outputs must remain ignored and must not be treated as solve evidence.

## Generated Outputs

Generated bounded auto-run outputs are ignored under `experiments/results/bounded-auto-runs/stage2j/`. Commit queue manifests and research summaries, not generated result bulk files.
