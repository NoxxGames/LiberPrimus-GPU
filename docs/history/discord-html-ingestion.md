# Discord HTML Ingestion

Stage 3N adds local ingestion for admin-provided Discord HTML exports.

The scanner reads local `.html` and `.htm` files, computes file locks, extracts public URL
candidates, redacts Discord attachment query strings, and emits keyword-only method and numeric
observation candidates. It does not fetch links, call Discord APIs, copy attachments, scrape
Discord, or preserve message bodies in committed records.

Generated review outputs are ignored under:

```text
experiments/results/discord-ingestion/stage3n/
```

Committed aggregate records are:

```text
data/locks/third-party/discord-chats/discord-archive-summary-v0.yaml
data/observations/discord/discord-ingestion-aggregate-summary-v0.yaml
```

Those aggregate records contain counts and safety flags only. They are not canonical source locks
for any extracted claim.
