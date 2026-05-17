# Stage 3B Stage 3A Lead Inspection

Run ID: `stage3a-stage2j-caesar-affine-first-reviewable-slice-20260517T025531Z`
Candidate count inspected: `841`
Top-N inspected: `25`

## Original Top Lead

- Candidate index: `726`
- Transform family: `affine_mod29`
- Transform parameters: `{"a": 25, "b": 1}`
- Total score: `33.353307`
- Output SHA-256: `f5a08b7d0a5ac64ea3b1becc4e7d212fe6fe57d59f0377a810a0a9bcd87a9dfd`
- Vowel ratio: `0.424528`
- Common word hits: `AS, BE, FOR, IN, OF, OR, THE, WE`
- Separator-aware word count: `0`
- Negative features: `none recorded in original score`

## Refined Top Lead

- Candidate index: `577`
- Transform family: `affine_mod29`
- Transform parameters: `{"a": 19, "b": 26}`
- Total score: `8.040756`
- Length-normalized score: `6.245247`
- Confidence label: `noisy`

## Score Distribution

- Min: `8.657413`
- Median: `18.298231`
- Mean: `18.116446`
- Max: `33.353307`
- Top1 minus top2: `2.411474`
- Top1 minus top10: `5.71403`

## Transform Family Counts

- All candidates: `{"affine_mod29": 812, "caesar_shift_mod29": 29}`
- Top candidates: `{"affine_mod29": 24, "caesar_shift_mod29": 1}`

## Inspection Result

- Qualitative label: `weak_noisy`
- Recommendation: Queue reverse-direction Caesar plus affine and keep refined scoring.
- Solve claim: false
- CUDA used: false
- Full candidate dump committed: false

## Warnings

- `top_candidate_has_no_separator_or_space_context`
