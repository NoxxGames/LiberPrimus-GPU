# Discord Source Promotion

Stage 3O promotes a small curated subset of Stage 3N Discord source-discovery output into committed review records.

Discord remains a source-discovery layer, not source truth. Promoted records are redacted leads only. They must not include raw message bodies, usernames, user IDs, message IDs, avatar URLs, private attachment URLs, or private query strings.

Committed records:

- `data/observations/discord/promoted-public-source-links-stage3o.yaml`
- `data/observations/discord/promoted-method-claim-candidates-stage3o.yaml`
- `data/observations/discord/promoted-numeric-observation-candidates-stage3o.yaml`

Generated promotion candidates, rejection lists, and summaries remain ignored under `experiments/results/discord-promotion/stage3o/`.

Promotion limits keep public files reviewable:

- public source links: at most `500`
- method-claim candidates: at most `200`
- numeric-observation candidates: at most `200`

Every promoted item keeps `trusted_as_canonical=false`, `raw_message_committed=false`, `usernames_committed=false`, and `review_status=human_review_required`.

No promoted record is an experiment seed by default, and no promoted record is a solve claim.
