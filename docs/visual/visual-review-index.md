# Visual Review Index

Stage 3P creates a local review index at:

```text
experiments/results/image-transforms/stage3p/review_index.html
```

The index links to generated contact sheets and per-image review pages. It does not embed raw source image paths. It is an ignored local aid for deciding which deterministic transform views deserve human review.

Candidate flags are review hints only:

- `hidden_low_bitplane_candidate`
- `high_half_mirror_difference_candidate`
- `high_rotational_symmetry_candidate`
- `sparse_dot_like_candidate`
- `dense_rune_text_candidate`
- `border_marker_candidate`
- `large_component_candidate`
- `high_edge_density_candidate`
- `potential_symbol_cluster_candidate`
- `high_noise_candidate`

All candidate records have `usable_as_experiment_seed=false`, `trusted_as_canonical=false`, and `solve_claim=false`.
