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

Runs policy-passing items, records deferred items explicitly, and blocks over-budget items.

## summary

Prints generated bounded auto-run summary counts from a results directory.
