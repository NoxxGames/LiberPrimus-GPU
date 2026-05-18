# Discord Research Source Policy

Stage 3N treats admin-provided Discord HTML exports as sensitive local research
material and source-discovery input only.

Rules:

- Raw Discord HTML logs stay under `third_party/LiberPrimusDiscordChats/` and are ignored.
- Do not commit message bodies, usernames, user IDs, avatars, private attachment URLs, or raw logs.
- Do not call Discord APIs, scrape Discord, use user tokens, or implement self-bots.
- Do not upload logs to AI services or run AI/ML summarisation over raw logs.
- Extracted links, attachment references, method claims, and numeric observations are reviewable leads only.
- Committed records must be aggregate and redacted.

Discord evidence is not canonical. Public links discovered through Discord must be reviewed and
promoted through the normal source registry before they are used as evidence or experiment seeds.

Stage 3O may promote selected public links and redacted claim summaries into
`data/observations/discord/`, but those promoted records remain reviewable leads. They must keep
`trusted_as_canonical=false`, must not include raw message bodies or usernames, and must not be
treated as facts until a later public-source review stage validates them independently.

Stage 3Q may generate redacted topic shards for local AI/deep-research review. These shards are
generated outputs and remain ignored by default. Deep Research should receive selected redacted
shards, never raw Discord HTML logs. Committed Stage 3Q records are aggregate-only and must not
contain raw messages, usernames, user IDs, message IDs, avatar URLs, private attachment URLs, or
private Discord CDN query strings.
