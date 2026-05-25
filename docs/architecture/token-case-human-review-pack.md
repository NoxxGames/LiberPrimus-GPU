# Token Case Human Review Pack

Stage 5AT turns the Stage 5AR token-case ambiguity records into a deterministic local human-review pack. It is packaging infrastructure, not token reading, OCR, AI/ML interpretation, decoding, hash search, CUDA, or experiment execution.

The active ambiguity classes are fixed to:

- `I/l`
- `O/0`
- `1/I/l`
- `S/5`
- `Z/2`
- `B/8`
- `G/6`
- `o/0`
- `q/g/p`

Stale examples such as `f/F`, `A/4`, and `C/G` are non-active examples only. They must not appear as Stage 5AT active challenge classes.

Committed metadata lives under `data/token-block/` and `data/project-state/`. Generated review material lives under `human-review-packs/stage5at/token-case-review/` and remains ignored. The pack contains crops, context crops, review sheets, an HTML index, and decision templates for manual review.

Stage 5AT deliberately keeps `canonical_transcription_changed=false`. Stage 5AU later records the Stage 5AT generated pack as count-valid but not usable for reliable manual decisions and rebuilds a v2 pack under `human-review-packs/stage5au/token-case-review-v2/`. Manual review decisions are expected in Stage 5AV before any later Codex integration stage can consider transcription updates.
