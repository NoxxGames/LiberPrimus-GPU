# Stage 5DY - Validation Performance Repair

Stage 5DY is validation infrastructure, not a cryptanalytic experiment. It records the Stage 5DX validation-tooling pain points and adds a safer staged validation path before Stage 5DZ number-fact review batch 3.

Committed outputs:

- `data/project-state/stage5dy-summary.yaml`
- `data/project-state/stage5dy-validation-profile-registry.yaml`
- `data/project-state/stage5dy-stage-isolation-policy.yaml`
- `data/project-state/stage5dy-nonmutating-validator-policy.yaml`
- `data/project-state/stage5dy-pytest-shard-race-audit.yaml`
- `data/source-harvester/stage5dy-codex-handoff-policy.yaml`
- `data/token-block/stage5dy-no-token-block-execution-proof.yaml`
- `data/ci/stage5dy-validation-profile-baseline.yaml`
- `python/libreprimus/token_block/stage5dy.py`
- `scripts/ci/run-stage-validation.ps1`
- `scripts/ci/run-stage-validation.sh`

Local summary:

- Validation profiles: 6
- Parallel worker cap: 8
- Full serial pytest default: false
- Stage-isolation repair: true
- Shared-schema collision guard: true
- Non-mutating validator guard: true
- Stage 5DX preserved: true
- Stage 5BD run-plan IDs: 10
- Active-lineage records: 8
- Number-fact batch 3 performed: false
- Target selected: false
- Bytes generated: false
- Execution performed: false
- Solve claim: false

Stage 5DY does not run route extraction, byte-stream generation, OCR, image forensics, audio/stego tools, Tor/network checks, scoring, CUDA, benchmarks, or any puzzle execution. The recommended next stage is Stage 5DZ, the operator/assistant source-lock number-fact review batch 3 without execution.
