# Stage 5DC Operator Choice Record

Stage 5DC is metadata-only. It records the explicit operator choice `prepare_real_operator_approval_record` after the Stage 5DB `accept_with_warnings` review of Stage 5DA.

The stage creates a valid operator choice/pause decision record and selected-option record. It preserves the other five Stage 5CS options unselected, leaves explicit pause unselected, preserves the Stage 5DA scaffold and Stage 5CY preflight, preserves exactly `10` Stage 5BD run-plan IDs, preserves `8` active-lineage records, and keeps the Stage 5CM-and-later worker cap at `8`.

It does not create a real operator approval record, Deep Research acceptance record, combined-gate validation record, activation decision, active planning input, byte stream, token-block execution, CUDA execution, benchmark, website expansion, method-status upgrade, canonical corpus activation, page-boundary finalisation, or solve claim.

Generated diagnostics remain ignored under `experiments/results/token-block/stage5dc/`. The local completion handoff remains ignored at `codex-output/stage5dc-codex-completion.md`; `codex_output` remains deprecated and must stay absent.
