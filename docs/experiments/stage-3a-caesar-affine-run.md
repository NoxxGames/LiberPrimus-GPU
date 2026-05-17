# Stage 3A Caesar Affine Run

Stage 3A executes the first standing-policy bounded CPU item from the queue:

- item: `stage2j-caesar-affine-first-reviewable-slice`
- input slice: `stage3a-page-candidate-018-reviewable-slice`
- candidate count: `841`
- Caesar candidates: `29`
- affine mod-29 candidates: `812`
- CUDA: disabled
- solve claim: false

## Corpus Selector

The queue item uses generated corpus-candidate metadata from `rtkd-master-v0-candidate` and selects `page-candidate-018` by token range. The committed queue does not embed raw unsolved text.

If the generated corpus-candidate files are missing locally, rerun the existing safe corpus-candidate generation command before running this experiment. Do not commit those generated files.

## Outputs

Generated outputs are ignored:

- `experiments/results/bounded-auto-runs/stage3a/candidate_records.jsonl`
- `experiments/results/bounded-auto-runs/stage3a/top_candidates.jsonl`
- `experiments/results/bounded-auto-runs/stage3a/summary.json`
- `experiments/results/bounded-auto-runs/stage3a/result_store_preview.json`

The research log may summarize run ID, counts, top score, and transform parameters. It must not include full candidate dumps or claim a solution.

## Interpretation

Top candidates are leads for later review. Minimal triage scores are not solve evidence and must not be published as a solution claim.
