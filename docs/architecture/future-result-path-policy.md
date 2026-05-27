# Future Result Path Policy

Stage 5BD validates paths that later token-block execution or review stages may write, but it does not write those future outputs. The policy exists to prevent future stages from accidentally placing generated results under committed data roots.

Allowed future result roots are ignored `experiments/results/token-block/stage*/` paths. Committed data, raw source roots, `third_party/`, human-review packs, `codex-output/`, website exports, and private Deep Research content packs are blocked for result bodies.

Stage 5BD records blocked examples in `data/token-block/stage5bd-future-result-path-validation.yaml`. The record is a path-policy check only; it is not authorization to execute token experiments.
