# Page Boundary Confidence Policy

## Status

Proposed Stage 0D-followup policy. Boundary records are non-canonical diagnostics.

## Why Boundary Confidence Matters

Boundary labels can shape future corpus records and solved-page fixtures. Overconfident boundaries are dangerous when line-pair alignment is incomplete or based on legacy sources.

## Boundary Evidence Classes

Evidence may include explicit transcript markers, local alignment continuity, known solved-page anchors, empty structural rows, source-reference context, and marker conflicts.

## Confidence Labels

- `high`: strong evidence with explicit markers or anchors and nearby aligned records.
- `medium`: plausible boundary with useful alignment context but missing explicit confirmation.
- `low`: weak structural evidence or ambiguous placement.
- `none`: insufficient evidence.

## High-Confidence Requirements

High confidence requires at least one strong evidence class:

- explicit source page marker plus nearby strong alignment coverage;
- known anchor plus consecutive alignment support;
- contiguous aligned pair chain around the boundary.

## Medium-Confidence Requirements

Medium confidence is appropriate when alignment evidence is useful but not locally strong enough for high confidence, or when an explicit marker lacks enough nearby aligned records.

## Low-Confidence Requirements

Low confidence is used for structural evidence alone, weak alignment, missing local continuity, or multiple plausible boundary placements.

## Empty-Pair Rule

Empty `{}` pairs are preserved as structural evidence. Empty pairs alone must never create high-confidence boundaries.

## Word-Length-Only Rule

Word-length-only evidence may break ties but must never create high-confidence boundaries.

## Anchor Rule

Known anchors, including the Parable final-page hint, remain non-authoritative. An anchor can support high confidence only when paired with strong consecutive alignment evidence.

## Explicit-Marker Rule

Explicit transcript markers are strong source evidence, but they are not automatically canonical. Stage 0D-followup downgrades markers without nearby alignment support.

## Overgeneration Warning

If boundary candidates exceed the expected LP2 page count or plausible start/end count, the summary must flag overgeneration instead of pretending the boundary list is final.

## Non-Canonical Status

Every boundary record must include `canonical_page_boundary=false`. Stage 0D-followup does not activate canonical page boundaries.

## Tests

Tests assert that empty-pair-only and word-length-only evidence cannot be high confidence, explicit markers can be high only with evidence, overgeneration is flagged, and every boundary remains non-canonical.
