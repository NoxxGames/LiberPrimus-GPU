# Token-Block Preflight Dry-Run Workflow

Stage 5BD is the current token-block planning layer. It is safe to validate locally because it reads committed metadata, writes compact records, and keeps generated reports ignored.

Start with:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli token-block validate-stage5bd
```

If rebuilding, run the commands in `docs/reference/token-block-preflight-dry-run-cli.md` in order. After rebuilding, verify that `experiments/results/token-block/stage5bd/`, `deep-research-repo-zips/stage5bd/`, and `codex-output/stage5bd-codex-completion.md` remain ignored.

Stage 5BD does not authorize byte-stream generation, variant materialisation, DWH/hash search, decoding, scoring, CUDA, benchmarks, website expansion, canonical corpus activation, page-boundary finalisation, or solve claims. Stage 5BF added historical-route source-lock metadata, Stage 5BI added Fandom/source-lock crosswalk metadata, Stage 5BJ closed or carried forward high-priority original/archive gaps, Stage 5BK integrated those constraints plus iddqd-v2 source-lock metadata without execution, Stage 5BM classified String 4 as a partial branch match without changing active manifests, and Stage 5BN closed the single unsupported-position source gap as spreadsheet-supported inactive-addendum metadata. The next step is Stage 5BO inactive token-option addendum integration, still without token-block execution.
