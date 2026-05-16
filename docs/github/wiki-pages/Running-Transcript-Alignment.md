# Running Transcript Alignment

Stage 0D aligns Pastebin line pairs against the rtkd transcript candidate.

```powershell
libreprimus corpus-alignment stage0d-smoke --pastebin <path-to-local-txt> --transcript <path-to-rtkd-transcript> --out-dir data/normalized/alignment --allow-warnings
```

Boundary candidates are tentative and non-canonical.
