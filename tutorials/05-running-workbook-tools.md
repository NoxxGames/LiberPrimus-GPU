# Running Workbook Tools

## Source

The workbook filename is intentionally `tranlsations.xlsx`. It is a non-canonical legacy analysis workbook, not canonical corpus truth.

## Commands

```powershell
libreprimus legacy-workbook summary --workbook <path-to-local-xlsx>
libreprimus legacy-workbook inventory --workbook <path-to-local-xlsx> --out <repo-root>\data\normalized\legacy-workbook\sheet_inventory.json
libreprimus legacy-workbook extract --workbook <path-to-local-xlsx> --out-dir <repo-root>\data\normalized\legacy-workbook
libreprimus legacy-workbook validate --workbook <path-to-local-xlsx> --allow-warnings
```

## Outputs

Extraction writes generated JSON/JSONL under `data/normalized/legacy-workbook/`. These files are ignored and should not be committed.

## Tests

Synthetic workbook tests always run. Real workbook tests run only when the local ignored workbook is present.
