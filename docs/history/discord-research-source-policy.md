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
