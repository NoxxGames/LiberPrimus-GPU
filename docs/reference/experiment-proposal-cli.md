# Experiment Proposal CLI

## validate

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli proposal validate --proposal experiments/proposals/stage2g/stage2g-caesar-page-candidate-proposal.yaml
```

Validates a proposal schema and Stage 2G safety flags.

## review-packet

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli proposal review-packet --proposal experiments/proposals/stage2g/stage2g-caesar-page-candidate-proposal.yaml --out-dir experiments/results/proposal-reviews/stage2g --allow-warnings
```

Generates ignored JSON and Markdown review packets without execution.

## check-approval

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli proposal check-approval --proposal experiments/proposals/stage2g/stage2g-caesar-page-candidate-proposal.yaml --approval experiments/proposals/stage2g/approval-records/stage2g-example-pending-approval.yaml
```

Reports whether a proposal is blocked or approved.

## stage2g-review-all

Runs validation and review packet generation for all committed Stage 2G proposals.

## review-summary

Summarizes generated review packets in a result directory.

## Troubleshooting

If validation fails, check that execution/search/candidate-generation/scoring/CUDA flags are false and that review checklists are present.
