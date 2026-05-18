# Discord Lead Promotion Audit

Stage 3R audits redacted Stage 3Q Discord review leads and promotes only safe, public, reviewable records.

Discord remains a lead-discovery layer. A lead becomes a committed record only when it maps to a public URL, an existing source record, or an exact artefact/observation that can be reviewed independently. Discord-only claims, private links, identity-bearing context, and speculative theories are quarantined or preserved as negative controls.

## Outputs

Committed records:

- `data/observations/discord/stage3r-promoted-source-records.yaml`
- `data/observations/discord/stage3r-promoted-observation-records.yaml`
- `data/observations/discord/stage3r-negative-control-records.yaml`
- `data/observations/discord/stage3r-promotion-audit-summary.yaml`

Generated audit details remain ignored under `experiments/results/discord-lead-promotion/stage3r/`.

## Policy

- No raw Discord messages are committed.
- No usernames, user IDs, message IDs, or private attachment URLs are committed.
- Promoted records keep `trusted_as_canonical=false`.
- Observation records keep `usable_as_experiment_seed=false`.
- Negative controls preserve false-positive classes for future review.
- Stage 3R creates disabled experiment manifests but does not execute them.
