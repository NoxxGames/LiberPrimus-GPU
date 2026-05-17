# Approval-Gated Execution CLI

## validate

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli approval-execution validate `
  --request experiments/proposals/stage2h/stage2h-approved-synthetic-direct-request.yaml
```

Validates request schema and false safety flags.

## plan

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli approval-execution plan `
  --request experiments/proposals/stage2h/stage2h-approved-synthetic-direct-request.yaml `
  --out-dir experiments/results/approval-gated-execution/stage2h `
  --allow-warnings
```

Writes a generated plan record.

## run

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli approval-execution run `
  --request experiments/proposals/stage2h/stage2h-approved-synthetic-direct-request.yaml `
  --out-dir experiments/results/approval-gated-execution/stage2h `
  --allow-warnings
```

Runs approved safe controls or writes a blocked result.

## stage2h-run-all

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli approval-execution stage2h-run-all `
  --request-dir experiments/proposals/stage2h `
  --out-dir experiments/results/approval-gated-execution/stage2h `
  --allow-warnings
```

Runs safe approved requests and reports blocked no-op real requests.

## summary

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli approval-execution summary `
  --results-dir experiments/results/approval-gated-execution/stage2h
```

Prints generated result counts.

## Troubleshooting

If a request is blocked, inspect `blocking_reasons` in the plan. Pending, denied, expired, wrong-scope, mismatched SHA, or future-unsolved proposals must not execute.

