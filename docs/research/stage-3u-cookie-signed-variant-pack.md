# Stage 3U Cookie Signed-Variant Pack Research Note

Stage 3U tests whether a small set of historically grounded signed/public strings and exact byte variants are SHA-256 preimages for the two archived 2013 cookie/hash artefacts.

## Method

The verifier loads the Stage 3R manifest and committed cookie/hash records. It expands only the manifest-declared base strings and byte variants, encodes candidates as UTF-8, deduplicates exact byte strings, computes SHA-256, and compares the digest hex exactly to each cookie value.

No web acquisition, Tor access, Discord raw-log processing, page-image processing, external dictionary, fuzzy matching, near-match scoring, hashcat, GPU, or alternate hash algorithm is used.

## Counts

- Cookie targets: `2`
- Base strings: `13`
- Byte variants: `12`
- Generated before deduplication: `156`
- Deduplicated candidates: `105`
- Duplicate byte strings: `51`
- Comparisons: `210`
- Exact matches: `0`

## Interpretation

The Stage 3U candidate pack did not produce an exact SHA-256 preimage for either archived cookie value. This rules out only the manifest-declared string/variant set. It does not prove the cookie values are SHA-256 outputs, does not rule out other preimages or other algorithms, and does not make a solve claim.
