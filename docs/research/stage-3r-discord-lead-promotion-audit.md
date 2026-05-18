# Stage 3R Discord Lead Promotion Audit

Stage 3R converts selected redacted Discord review leads into public-source and observation review records. The stage treats Discord as discovery context only, not evidence.

Local run summary:

- Promoted source records: `13`
- Promoted observation records: `11`
- Negative controls: `11`
- Duplicate existing source references counted: `3`
- Unsafe/private or quarantined records counted: `25`
- Post-Discord manifests created: `3`

No new experiments were executed. No raw Discord logs, generated topic shards, message bodies, usernames, private URLs, or generated audit JSONL records are committed. No solve claim is made.

## Promotion Rules

Promote public sources and exact artefact observations only. Quarantine Discord-only, speculative, identity-bearing, private, or uncited material. Preserve known false-positive classes as negative controls.

## Generated Outputs

Generated audit files remain ignored under `experiments/results/discord-lead-promotion/stage3r/`.
