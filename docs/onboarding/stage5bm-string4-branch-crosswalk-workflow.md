# Stage 5BM String 4 Branch-Crosswalk Workflow

Use Stage 5BM when reviewing how the iddqd-v2 String 4 context relates to the page 49-51 token-block metadata.

## Inputs

- Stage 5BL Deep Research review report.
- Stage 5BK iddqd-v2 source-lock and String 4 crosswalk records.
- Stage 5AP canonical transcription and primary-60 mapping preflight records.
- Stage 5AW repaired unresolved branch metadata and reviewer-extra token records.
- Stage 5AY branch-eligibility policy.
- Stage 5BM source restatement, mismatch analysis, branch-membership, planning-constraint, and next-stage decision records after the build command runs.
- Stage 5BN target-position source-gap closure records for follow-up inactive addendum planning after Stage 5BM is complete.
- Stage 5BO operator-errata records and Stage 5BQ inactive-branch planning constraints for later follow-up context.
- Stage 5BS planning-ingestion gate, future-runner citation policy, no-active-ingestion proof, Stage 5BD preservation, guardrail, and reviewable evidence records for future fail-closed planning-ingestion checks.
- Stage 5BU lineage-path repair records, preserved active-lineage digest index, and validator hardening for future reviewability checks.
- Stage 5BW inactive-sidecar planning-ingestion proposal, manifest-supersession preflight, active-lineage preservation, and Stage 5BD plan preservation records for future review-only planning checks.
- Stage 5BY inactive planning-manifest scaffold, no-execution planning-ingestion sidecar, Stage 5BW duplicate-source-digest classification, filename-equivalence map, active-lineage preservation, and Stage 5BD plan preservation records for Stage 5BZ review-only planning checks.
- Stage 5CA inactive-sidecar review contract, exact citation contract, fail-closed trigger contract, activation-precondition contract, manifest-supersession preflight contract, no-active-ingestion proof, no-byte-stream proof, active-lineage preservation, and Stage 5BD preservation records for Stage 5CB review-only contract checks.
- Stage 5CC active-planning-input proposal preflight, exact fail-closed trigger/precondition hardening, no-byte-stream transition gate, no-execution transition gate, active-lineage preservation, Stage 5BD plan preservation, and DWH quarantine reaffirmation records for Stage 5CD review-only transition-gate checks.
- Stage 5CE active-planning-input proposal package, Stage 5CD findings integration, operator/Deep Research approval-gate design, direct citation negative-test hardening, committed pytest-count capture, active-lineage preservation, Stage 5BD plan preservation, no-byte-stream transition gate, and no-execution transition gate records for Stage 5CF review-only proposal-package checks.
- Stage 5CG Stage 5CF findings integration, unsatisfied operator approval scaffold, unsatisfied Deep Research acceptance scaffold, combined approval-gate scaffold, active-planning-input decision scaffold, Stage 5CE wording review, no-byte-stream transition gate, no-execution transition gate, active-lineage preservation, Stage 5BD plan preservation, sidecar blocker, and guardrail records for Stage 5CH review-only approval-gate checks.
- Stage 5CI Stage 5CH findings integration, future operator approval template, future Deep Research acceptance template, combined approval-gate validation preflight, activation-decision template, negative validation contract, no-byte-stream transition gate, no-execution transition gate, active-lineage preservation, Stage 5BD plan preservation, sidecar blocker, and guardrail records for Stage 5CJ review-only template-hardening checks.

## Commands

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli token-block build-stage5bm-string4-reconciliation
.\.venv\Scripts\python.exe -m libreprimus.cli token-block validate-stage5bm
.\.venv\Scripts\python.exe -m libreprimus.cli token-block stage5bm-summary
```

The build command may read the ignored local iddqd-v2 byte-string file in memory. It writes only compact metadata records plus ignored diagnostics. Validation does not require raw source bytes to be committed.

## Interpretation

Stage 5BM classifies String 4 as `partial_branch_match`: most positions match the Stage 5AP canonical grid, six positions are supported by Stage 5AW ambiguity metadata, and one position remains unsupported. The unsupported position blocks active use until a future review/source-gap closure stage handles it.

## Guardrails

Do not use Stage 5BM as execution permission. String 4 remains external context/review-only. DWH remains quarantined. Future stages must use `codex-output/` for local Codex handoffs and must not create `codex_output/`.
