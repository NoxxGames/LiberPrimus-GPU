# Stage 5BW Inactive-Sidecar Planning-Ingestion Workflow

Stage 5BW is a metadata-only preflight stage. It consumes the Stage 5BV `accept_with_warnings` review outcome, proposes a future inactive String 4 sidecar planning-ingestion model, and defines manifest-supersession preflight requirements without activating String 4 or changing active manifests.

Run the local Stage 5BW checks:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli token-block build-stage5bw
.\.venv\Scripts\python.exe -m libreprimus.cli token-block validate-stage5bw
.\.venv\Scripts\python.exe -m libreprimus.cli token-block stage5bw-summary
```

The review starting points are:

- `data/project-state/stage5bw-summary.yaml`
- `data/token-block/stage5bw-inactive-sidecar-planning-ingestion-proposal.yaml`
- `data/token-block/stage5bw-manifest-supersession-preflight.yaml`
- `data/token-block/stage5bw-stage5bd-plan-preservation.yaml`
- `data/token-block/stage5bw-no-active-ingestion-proof.yaml`
- `data/token-block/stage5bw-no-byte-stream-gate.yaml`

Stage 5BW preserves Stage 5AP/5AW/5AY/5AZ/5BB/5BD active lineage and the Stage 5BD run-plan ID count. It must not be used as active runner input, byte-stream generation permission, DWH/hash search permission, decoding evidence, score evidence, CUDA input, benchmark scope, website publication approval, or a solve claim.
