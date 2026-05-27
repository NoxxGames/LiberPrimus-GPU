# Historical Route Source-Lock CLI

Use `libreprimus historical-route` for Stage 5BF metadata-only source locking.

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
