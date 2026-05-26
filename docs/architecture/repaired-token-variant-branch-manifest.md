# Repaired Token Variant Branch Manifest

Stage 5AW creates `data/token-block/stage5aw-repaired-token-variant-branch-manifest.yaml` as the compact superseding branch manifest for future bounded preflight planning.

The manifest supersedes the Stage 5AV branch metadata because Stage 5AV accidentally treated three prose fragments as reviewer-extra possible tokens. Stage 5AW keeps the 77 unresolved cases, preserves valid reviewer extras, preserves visual placeholders as unmappable review-only options, and recalculates the branch upper bound without enumerating the Cartesian product.

Current Stage 5AW branch counts:

- Repaired reviewer-extra tokens: `10`.
- Malformed fragments audited: `3`.
- Visual placeholders: `2`.
- Primary-60 mappable/unmappable options: `99 / 65`.
- Branch upper-bound product: `2720083094132915643088896`.
- Branch upper-bound log10: `24.434582`.
- Primary-60 mappable branch product: `4194304`.

The manifest is planning metadata only. It must be cited by Stage 5AX bounded preflight design, but it does not enable execution, decoding, hash/preimage work, CUDA, benchmarks, scored experiments, or solve claims.
