# Result Synthesis CLI

Stage 3Y adds the `research-synthesis` CLI group for validating and summarising durable research-memory records.

## Validate

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli research-synthesis validate `
  --data-dir data/research `
  --staged-plan docs/roadmap/staged-plan.md
```

This validates schemas, required method-family records, retirement references, no-solve flags, CUDA deferral, cookie hash no-broadening guardrails, raw/generated output flags, and staged-plan policy text.

## Summary

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli research-synthesis summary `
  --data-dir data/research
```

This prints counts by record set and method/retirement status.

## Check One Method Family

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli research-synthesis check-retirement `
  --data-dir data/research `
  --method-family caesar_affine
```

This prints the method-family status, reopen conditions, stop conditions, and retirement/deprioritisation record if present.
