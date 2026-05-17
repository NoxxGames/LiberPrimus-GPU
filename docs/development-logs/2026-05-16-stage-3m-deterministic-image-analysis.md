# Stage 3M Deterministic Image Analysis

Stage 3M adds deterministic local image-analysis tooling over ignored Liber Primus page images.

Initial state:

- Branch: `main`
- Local HEAD: `579c029e5b927c89d09f7c65c2dcea90dec2622a`
- Origin remote: `https://github.com/NoxxGames/LiberPrimus-GPU.git`
- Local equals `origin/main`: true
- Latest known CI: success, run `26002495564`
- Stage 3K image locks: present
- Local image files: `58`
- Generated outputs staged: `0`
- Raw images staged: `0`
- Root research reports staged: `0`

Scope:

- Deterministic local image features only.
- No OCR, AI/ML image interpretation, OutGuess, audio/spectrogram work, live Tor/web acquisition, image-derived cipher execution, CUDA, or solve claim.
- Raw page images and generated JSON/JSONL analysis outputs remain ignored.

Implementation status:

- Output directory and ignore policy: complete.
- Schemas: seven Stage 3M visual/image-analysis schemas added.
- Dependency: Pillow added as the only image-decoding dependency.
- Implementation: grayscale statistics, channel statistics, fixed-threshold summaries, 4-connected connected components, symmetry metrics, border features, bit-plane summaries, deterministic average hash, feature candidate flags, export, summary, and validation modules added.
- CLI: `libreprimus image-analysis analyze-local-pages`, `validate-results`, and `summary` added.
- Consistency integration: raw-image-free validation added.

Local run:

- Images analysed: `58`
- Threshold values: `32, 64, 96, 128, 160, 192, 224`
- Component records: `406`
- Symmetry records: `58`
- Bitplane records: `464`
- Visual feature candidates: `71`
- High-symmetry candidates: `7`
- Sparse-dot-like candidates: `2`
- High-noise candidates: `0`
- Generated outputs: ignored under `experiments/results/image-analysis/stage3m/`
- Solve claim: false
