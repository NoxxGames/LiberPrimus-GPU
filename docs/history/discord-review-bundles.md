# Discord Review Bundles

Stage 3Q turns admin-provided local Discord HTML exports into redacted, topic-specific review bundles for local AI/deep-research workflows.

The bundles are a source-discovery aid only. They are not canonical evidence, not experiment seeds, and not solve claims.

## Inputs

- Local raw exports under `third_party/LiberPrimusDiscordChats/`.
- Stage 3N generated extraction records under `experiments/results/discord-ingestion/stage3n/`.
- Stage 3O promoted public-source and observation records under `data/observations/discord/`.

Raw Discord HTML stays ignored. Stage 3Q does not call Discord APIs, scrape Discord, upload logs, or run AI/ML.

## Generated Outputs

Generated bundle outputs are written under:

```text
experiments/results/discord-review-bundles/stage3q/
```

Expected generated files include:

- `redacted_message_stream.jsonl`
- `topic_shards/*.md`
- `source_links_index.jsonl`
- `method_claims_index.jsonl`
- `numeric_observations_index.jsonl`
- `visual_observations_index.jsonl`
- `debunks_and_false_positives_index.jsonl`
- `attachment_reference_index.jsonl`
- `review_bundle_summary.json`
- `review_index.html`

These files are ignored and must not be committed by default.

## Committed Aggregate

The committed aggregate is:

```text
data/observations/discord/discord-review-bundle-aggregate-stage3q.yaml
```

It contains counts, topic names, generated output paths, and privacy flags only. It must not contain raw message bodies, usernames, user IDs, message IDs, avatar URLs, or private Discord attachment URLs.

## Review Rules

- Topic shards are review aids, not evidence.
- Deep Research should receive selected redacted shards, not raw HTML exports.
- Extracted leads remain hypotheses until promoted through source or observation review.
- No extracted method is executed in Stage 3Q.
