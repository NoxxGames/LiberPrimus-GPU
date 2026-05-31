# Token-Block Preflight Dry-Run Workflow

Stage 5BD is the current token-block planning layer. It is safe to validate locally because it reads committed metadata, writes compact records, and keeps generated reports ignored.

Start with:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli token-block validate-stage5bd
```

Stage 5BW adds an inactive-sidecar planning-ingestion proposal and manifest-supersession preflight on top of the Stage 5BD dry-run layer. It preserves all Stage 5BD run-plan IDs and keeps String 4 out of active dry-run inputs; run `token-block validate-stage5bw` before any future planning-ingestion review.

Stage 5BY turns the Stage 5BX review warnings into concrete metadata: source-digest duplicate classification, record-family filename-equivalence mapping, an inactive planning manifest scaffold, and a no-execution planning-ingestion sidecar. It still preserves all Stage 5BD run-plan IDs and keeps String 4 out of active dry-run inputs; run `token-block validate-stage5by-source-digest-uniqueness`, `token-block validate-stage5by-sidecar-gates`, and `token-block validate-stage5by` before any Stage 5BZ review or future planning-ingestion work.

If rebuilding, run the commands in `docs/reference/token-block-preflight-dry-run-cli.md` in order. After rebuilding, verify that `experiments/results/token-block/stage5bd/`, `deep-research-repo-zips/stage5bd/`, and `codex-output/stage5bd-codex-completion.md` remain ignored.

Stage 5BD does not authorize byte-stream generation, variant materialisation, DWH/hash search, decoding, scoring, CUDA, benchmarks, website expansion, canonical corpus activation, page-boundary finalisation, or solve claims. Stage 5BF added historical-route source-lock metadata, Stage 5BI added Fandom/source-lock crosswalk metadata, Stage 5BJ closed or carried forward high-priority original/archive gaps, Stage 5BK integrated those constraints plus iddqd-v2 source-lock metadata without execution, Stage 5BM classified String 4 as a partial branch match without changing active manifests, Stage 5BN closed the single unsupported-position source gap as spreadsheet-supported inactive-addendum metadata, Stage 5BO reclassifies String 4 as a full branch match only in an inactive operator-errata planning universe, and Stage 5BQ records that status as inactive planning context while keeping active input and dry-run ingestion false. Stage 5BS records the Stage 5BR review outcome as a closed planning-ingestion gate with fail-closed future-runner citation requirements. Stage 5CA hardens inactive-sidecar review contracts, Stage 5CC adds an active-planning-input proposal preflight plus closed no-byte/no-execution transition gates, Stage 5CE packages that proposal for review with operator/Deep Research gate requirements, Stage 5CG creates unsatisfied future decision scaffolds after Stage 5CF review, and Stage 5CI hardens the future approval/acceptance/activation-decision templates after Stage 5CH review. The next step is Stage 5CJ Deep Research review before any approval-record, activation, planning-ingestion, byte-stream generation, or execution-capable token-block stage, still without token-block execution.
