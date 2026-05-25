# Token-Block Alphabet Registry

Stage 5AP creates a candidate alphabet registry for the page 49-51 token block. The primary registry records a 60-character suffix alphabet and a primary-60 byte-mapping preflight over two-character tokens.

Important boundaries:

- The primary-60 mapping is a candidate value mapping, not decoded plaintext.
- `00 -> 0` and `4F -> 255` are mapping checks only.
- Lowercase `f` is recorded as absent from the observed suffix set.
- Mapping values remain preflight metadata until exact source and review requirements are closed.
- The registry must not be treated as canonical rune semantics or page-boundary evidence.

Committed records:

- `data/token-block/stage5ap-token-block-alphabet-registry.yaml`
- `data/token-block/stage5ap-token-block-mapping-preflight.yaml`
- `data/token-block/stage5ap-token-block-null-control-plan.yaml`

Future reviews should compare any claimed token-value source against these records and record alternate alphabet orders explicitly instead of silently changing the mapping.
