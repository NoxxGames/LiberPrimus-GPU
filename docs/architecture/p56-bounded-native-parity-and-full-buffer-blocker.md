# P56 Bounded Native Parity And Full Buffer Blocker

Stage 5X separates the bounded p56 parity check from full p56 execution.

The bounded check uses the committed Stage 4O/5L p56 mapping and Stage 5W expected hash. It produces a compact parity record only. The full p56 mapping remains blocked because no complete source-backed p56 cipher token buffer is committed.

Full p56 execution requires a future explicit stage that supplies:

- a committed source-backed full cipher token buffer;
- declared stream schedule and skip policy;
- expected-output policy;
- no-generated-body publication guardrails;
- result-store and score-summary preflight records.

Until then, full p56 parity is `blocked_full_p56_token_buffer_missing`.
