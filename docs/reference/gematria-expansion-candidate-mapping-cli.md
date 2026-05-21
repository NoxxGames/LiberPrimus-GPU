# Gematria Expansion Candidate Mapping CLI

Stage 5Q adds:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli gematria-expansion-candidate-mapping build-candidate-inventory --allow-warnings
.\.venv\Scripts\python.exe -m libreprimus.cli gematria-expansion-candidate-mapping build-token-mapping --allow-warnings
.\.venv\Scripts\python.exe -m libreprimus.cli gematria-expansion-candidate-mapping build-native-parity --allow-warnings
.\.venv\Scripts\python.exe -m libreprimus.cli gematria-expansion-candidate-mapping build-result-store-preflight --allow-warnings
.\.venv\Scripts\python.exe -m libreprimus.cli gematria-expansion-candidate-mapping build-expansion-gate --allow-warnings
.\.venv\Scripts\python.exe -m libreprimus.cli gematria-expansion-candidate-mapping build-summary --allow-warnings
.\.venv\Scripts\python.exe -m libreprimus.cli gematria-expansion-candidate-mapping validate-stage5q
.\.venv\Scripts\python.exe -m libreprimus.cli gematria-expansion-candidate-mapping summary
```

The commands are no-GPU-safe and do not execute CUDA. They read committed solved-fixture-safe records and write compact YAML metadata plus ignored generated reports.

The validation command rejects guardrail drift such as CUDA execution, CUDA source modification, new kernels, generated-output commits, raw-data processing, method-status upgrades, benchmark claims, and solve claims.
