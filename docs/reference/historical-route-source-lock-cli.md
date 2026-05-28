# Historical Route Source-Lock CLI

Use `libreprimus historical-route` for Stage 5BF, Stage 5BI, and Stage 5BJ metadata-only source locking.

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

## Stage 5BJ Commands

- `stage5bj-build`
- `stage5bj-validate`
- `stage5bj-summary`

Stage 5BJ commands close or explicitly carry forward the high-priority Stage 5BI original/archive crosswalk gaps. The builder reads ignored local archive and spreadsheet metadata from `third_party/CicadaSolversIddqd`, `third_party/3N_3p_Bases_49-51.jpg.xlsx`, and `third_party/SourceSnapshots` as provenance material only, then writes compact metadata records for 12 crosswalk closures, 3 exact 2014 512-hex surface source locks, Fandom page-body crosswalk status, boards-thread archive-equivalent context, media-equivalence closure, source-gap updates, token-block lineage preservation, guardrails, and Stage 5BK next-stage routing.

The Stage 5BJ CLI does not execute token-block experiments, generate byte streams, combine 2014 surfaces with page 49-51, run DWH/hash/preimage search, decode, score, run stego/audio/image/OCR/AI/CUDA tooling, publish website content, or make solve claims. Full extracted surface bodies and reports are generated under ignored paths, and the local Codex completion summary under `codex_output/` or `codex-output/` must remain unstaged.
