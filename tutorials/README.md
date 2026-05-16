# Tutorials

These tutorials teach practical use of the LiberPrimus GPU Cryptanalysis Workbench on local hardware.

## Recommended Reading Order

1. `00-project-safety-and-provenance.md`
2. `01-windows-setup.md` or `02-linux-setup.md`
3. `03-repository-tour.md`
4. `04-working-with-local-data.md`
5. Tool-specific tutorials as needed.

## Current Project Stage

The project is still in pre-solver corpus-preparation stages. Current tools inventory and validate non-canonical legacy sources, parse transcript candidates, and emit alignment hints.

No unsolved Liber Primus page is claimed solved.

## Quick Command Map

```powershell
libreprimus legacy-workbook summary
libreprimus legacy-pastebin summary
libreprimus transcript-source summary --source rtkd-master --input <repo-root>\data\raw\transcripts\rtkd\liber-primus__transcription--master.txt
libreprimus corpus-alignment stage0d-smoke --pastebin <repo-root>\data\raw\legacy-pastebins\58-Pages-In-Runes-With-Prime-Values-Pastebin.txt --transcript <repo-root>\data\raw\transcripts\rtkd\liber-primus__transcription--master.txt --out-dir <repo-root>\data\normalized\alignment --allow-warnings
```

## Safety Warning

Terminal output, workbook rows, Pastebin rows, and generated alignment records are not solve evidence. Treat all current outputs as provenance-bearing preparation data.
