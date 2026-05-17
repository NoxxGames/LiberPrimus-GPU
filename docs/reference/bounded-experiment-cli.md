# Bounded Experiment CLI

The `libreprimus bounded-experiment` command group manages Stage 2J operator-policy checks and bounded queue runs.

## validate-policy

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli bounded-experiment validate-policy --policy experiments/policies/operator-policy-v0.yaml
```

Validates the standing operator policy.

## validate-queue

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli bounded-experiment validate-queue --queue experiments/queues/stage2j-bounded-cpu-queue.yaml
```

Validates the bounded experiment queue schema and item shape.

## check-queue

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli bounded-experiment check-queue --policy experiments/policies/operator-policy-v0.yaml --queue experiments/queues/stage2j-bounded-cpu-queue.yaml
```

Prints policy pass, warning, and block status for each item.

## run-next

Runs the next policy-passing item and writes generated ignored output records.

## run-all

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli bounded-experiment run-all --policy experiments/policies/operator-policy-v0.yaml --queue experiments/queues/stage2j-bounded-cpu-queue.yaml --out-dir experiments/results/bounded-auto-runs/stage2j --allow-warnings
```

Runs policy-passing items, records deferred items explicitly when a safe executor is missing, and blocks over-budget items. After Stage 3A, the Caesar plus affine queue item can call the minimal CPU executor when generated selector metadata exists locally.

For the direct Stage 3A candidate run, use:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli bounded-run run-caesar-affine --policy experiments/policies/operator-policy-v0.yaml --queue experiments/queues/stage2j-bounded-cpu-queue.yaml --item-id stage2j-caesar-affine-first-reviewable-slice --out-dir experiments/results/bounded-auto-runs/stage3a --top-k 25 --allow-warnings
```

## summary

Prints generated bounded auto-run summary counts from a results directory.
