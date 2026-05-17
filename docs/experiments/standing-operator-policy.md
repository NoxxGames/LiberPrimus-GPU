# Standing Operator Policy

The Stage 2J standing operator policy lets Codex run worthwhile bounded local CPU experiments without asking for a separate YAML approval record every time.

The policy is committed at `experiments/policies/operator-policy-v0.yaml`.

## Allowed Automatically

An experiment can run automatically only when all policy checks pass:

- `cpu_only=true`
- `cuda_enabled=false`
- `cloud_execution=false`
- `external_paid_services=false`
- candidate upper bound at or below `100000`
- runtime estimate at or below `600` seconds
- generated output budget at or below `250` MB
- generated outputs remain ignored
- no canonical corpus activation
- no page-boundary finalization
- no solve claim

## Still Requires Explicit Instruction

Explicit user instruction is still required for CUDA or GPU work, over-budget experiments, cloud or paid services, committing generated outputs, solve claims, canonical corpus activation, and page-boundary finalization.

## Approval Tooling

The Stage 2G through Stage 2I approval tooling remains available as optional audit tooling for high-risk or out-of-policy work. It is no longer the default path for normal bounded local CPU experiments.
