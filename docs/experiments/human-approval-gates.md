# Human Approval Gates

## Human Approval Requirement

Any proposal touching future unsolved or reviewable page candidates requires `human_approval_required=true`.

## Approved, Pending, And Denied

Only a valid `approved` record with `approved_for_execution=true` can pass the approval gate. Missing, pending, denied, expired, superseded, or invalid records block execution.

## Expiry

Future approved records must include an expiry timestamp. Expired records fail validation.

## Constraints

Approved records must carry explicit constraints so the execution scope cannot silently expand.

## Automatic Approval Is Forbidden

Stage 2G never approves proposals automatically. The CLI can record and check approval records, but committed examples remain pending or denied.

## Future Execution Stages

Future execution code must validate the approval record against the proposal SHA-256 before any real run.
