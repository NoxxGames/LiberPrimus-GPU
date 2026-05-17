# Deterministic Image Analysis

Stage 3M adds local deterministic image-analysis tooling for the ignored Liber Primus page images under `third_party/LiberPrimusPages/`.

The analysis is intentionally mechanical. It records file identity, dimensions, color mode, grayscale statistics, channel statistics, fixed threshold summaries, 4-connected component counts, border darkness ratios, simple symmetry metrics, bit-plane density, a deterministic 8x8 average hash, and review-only visual feature candidates.

It does not run OCR, AI/ML image labelling, steganography extraction, OutGuess, audio/spectrogram work, live web acquisition, or image-derived cipher experiments.

Generated records are written under `experiments/results/image-analysis/stage3m/` and remain ignored. Summary-only research logs may cite counts and image IDs, but not raw images or large generated tables.

Connected components use deterministic 4-connected foreground labelling on a bounded analysis image. The component records are summaries only; no masks or extracted regions are committed.

Feature candidates are review aids. They stay `usable_as_experiment_seed=false`, `trusted_as_canonical=false`, and `solve_claim=false`.
