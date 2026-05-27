# Historical Route Source-Lock CLI

Use `libreprimus historical-route` for Stage 5BF and Stage 5BI metadata-only source locking.

Primary commands:

- `locate-stage5bf-archive`
- `inventory-stage5bf-archive`
- `classify-stage5bf-artifacts`
- `build-stage5bf-annual-route-inventory`
- `build-stage5bf-trust-classifications`
- `build-stage5bf-technique-taxonomy`
- `build-stage5bf-specialized-artifact-records`
- `build-stage5bf-token-block-impact`
- `build-stage5bf-deep-research-readiness`
- `build-stage5bf-summary`
- `validate-stage5bf`

The CLI reads the ignored local archive and writes compact committed metadata plus ignored generated JSON/JSONL reports. It never clones online sources or executes route techniques.

## Stage 5BI Commands

- `stage5bi-build`
- `stage5bi-validate`
- `stage5bi-summary`

Stage 5BI commands build and validate Fandom page triage, item source-lock candidates, original/archive crosswalk candidates, Fandom media non-original policy, 2014 surface context, token-block external context, local spreadsheet source-lock/reconciliation metadata, source gaps, negative controls, guardrails, summary, and next-stage decision records.

The Stage 5BI builder may read ignored local metadata from `third_party/CicadaSolversIddqd` and `third_party/3N_3p_Bases_49-51.jpg.xlsx`, but it commits only compact YAML metadata. It does not commit raw archive files, Fandom page bodies or media, spreadsheet cell bodies, generated outputs, token-block byte streams, or decoded results.
