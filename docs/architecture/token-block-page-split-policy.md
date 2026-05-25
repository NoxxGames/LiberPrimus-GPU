# Token-Block Page-Split Policy

The Stage 5AP token block has 32 rows and 8 columns. Stage 5AR records the source-backed logical page split as:

- page 49: rows 0 through 9, 10 rows;
- page 50: rows 10 through 22, 13 rows;
- page 51: rows 23 through 31, 9 rows.

The 10/13/9 split is accepted only as metadata for the page 49-51 token block. It is not a canonical Liber Primus page-boundary decision and does not activate the canonical corpus.

Future review stages must cite both `data/token-block/stage5ar-page-split-policy.yaml` and `data/token-block/stage5ar-page-split-records.yaml` before using the split. If later source review finds that the split was derived from a screenshot, crop, modified image, or private generated rendering, the split must be downgraded to source-gap status and cannot feed execution planning.

Stage 5AR does not decode the block, execute hypotheses, run hash/preimage search, run OCR, run AI/ML interpretation, run stego tools, run CUDA, benchmark, or perform scored experiments.

