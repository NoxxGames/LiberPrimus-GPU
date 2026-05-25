# Token-Block Case Policy

Stage 5AR records case and glyph-shape ambiguity as review metadata. It does not silently alter the Stage 5AP canonical token transcription.

The committed policy at `data/token-block/stage5ar-token-case-policy.yaml` keeps `canonical_transcription_changed=false` and records unresolved ambiguity classes for visually similar forms such as `I/l`, `O/0`, `f/F`, `S/5`, `B/8`, `Z/2`, `G/6`, `A/4`, and `C/G`.

Those ambiguity records are null-control and review inputs. They are not proof of an intended encoding, not a source of alternate plaintext, and not a reason to run a decode or hash/preimage search.

Future bounded planning must keep case-confusion controls distinct from source truth. Any reviewed change to token text requires a later source-lock record, explicit provenance, and an updated transcription policy.

