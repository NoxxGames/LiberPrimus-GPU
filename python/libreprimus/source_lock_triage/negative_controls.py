"""Stage 4B false-positive and negative-control records."""

from __future__ import annotations

from typing import Any


NEGATIVE_CONTROL_SPECS: tuple[tuple[str, str, str, str], ...] = (
    (
        "braille_dot_readings",
        "Braille dot readings",
        "Too many plausible readings can be imposed on sparse dot motifs.",
        "Use as visual pareidolia negative controls before any dot scoring.",
    ),
    (
        "constellation_dot_readings",
        "Constellation dot readings",
        "Resemblance-only star matching is unstable and contradictory.",
        "Use as resemblance-only controls.",
    ),
    (
        "forced_13_31_dot_values",
        "Forced 13/31 dot readings",
        "13 and 31 depend on anchor, rotation, grouping, and polarity choices.",
        "Require ambiguity tables before treating dot values as seeds.",
    ),
    (
        "cuneiform_reading_as_fact",
        "Cuneiform reading treated as fact",
        "The arithmetic is clean only if the visual segmentation is accepted.",
        "Require coordinate annotation and alternate readings first.",
    ),
    (
        "incorrect_base60_conversion",
        "Incorrect or ambiguous base-60 conversion",
        "Sexagesimal arithmetic can be correct while the glyph readout is wrong.",
        "Separate arithmetic checks from visual evidence.",
    ),
    (
        "ad_hoc_prime_magic_square_arithmetic",
        "Ad-hoc prime/magic-square arithmetic",
        "Prime-nearby and no-rule arithmetic can make coincidences look intentional.",
        "Use only fixed no-fudge routes on locked raw values.",
    ),
    (
        "broad_outguess_bruteforce_garbage",
        "Broad OutGuess brute-force garbage outputs",
        "OutGuess-like tools can emit fake file types or garbage under arbitrary passwords.",
        "Require known positives, negatives, and expected hash checks before new extraction claims.",
    ),
    (
        "mp3stego_without_exact_positive",
        "MP3Stego enthusiasm without exact source-positive",
        "Audio stego claims need reproducible positive controls, not plausible filenames.",
        "Source-lock historical positives before broad audio work.",
    ),
    (
        "spectrogram_pareidolia",
        "Spectrogram pareidolia",
        "Spectrogram shapes are easy to over-read without exact expected payloads.",
        "Treat as negative control unless a source-locked positive exists.",
    ),
    (
        "ai_generated_page_solves",
        "AI-generated page solves",
        "AI-generated plaintext can hallucinate even solved-page context.",
        "Do not admit AI text as evidence or seed source.",
    ),
    (
        "sixteen_page_authenticity_myth",
        "LP only has 16 authentic pages myth",
        "Unverified authenticity shortcuts can erase reviewable corpus material.",
        "Keep as myth-control until backed by signed provenance.",
    ),
    (
        "unsigned_new_cicada_claims",
        "Unsigned or unverifiable new-Cicada claims",
        "Claims without PGP/signature provenance are cheap false paths.",
        "Quarantine unless public signing evidence exists.",
    ),
    (
        "dictionary_looking_prime_hits",
        "Dictionary-looking prime/totient hits",
        "Small transforms can produce English-looking coincidences by chance.",
        "Require controls and source-anchored hypotheses.",
    ),
    (
        "broad_literature_key_fishing",
        "Broad literature-key fishing",
        "Literature references are abundant and low-yield without exact keys.",
        "Do not broaden Vigenere/book-key packs without explicit source keys.",
    ),
    (
        "geometry_mirror_overlay_dumps",
        "Geometry/mirror overlay dumps without source lineage",
        "Overlays can manufacture structure from arbitrary alignments.",
        "Require exact source lineage and negative overlays.",
    ),
    (
        "mayfly_dot_skip_index_theory",
        "Mayfly-dot skip-index theory",
        "Large claims from weak visual evidence are high-risk false positives.",
        "Quarantine until public exact evidence exists.",
    ),
    (
        "attachment_reference_privacy_risk",
        "Attachment-reference indexing as privacy risk",
        "Attachment identifiers are not evidence and increase public exposure.",
        "Keep generated attachment indexes private/redacted.",
    ),
)


def build_negative_controls() -> list[dict[str, Any]]:
    """Return Stage 4B negative-control records."""

    return [
        {
            "record_type": "stage4b_negative_control_record",
            "negative_control_id": f"stage4b-negative-{slug}",
            "false_positive_class": slug,
            "description": description,
            "why_dangerous": why,
            "recommended_use": use,
            "evidence_strength": "medium"
            if slug
            in {
                "forced_13_31_dot_values",
                "cuneiform_reading_as_fact",
                "attachment_reference_privacy_risk",
            }
            else "low",
            "false_positive_risk": "extreme"
            if slug not in {"attachment_reference_privacy_risk", "sixteen_page_authenticity_myth"}
            else "high",
            "trusted_as_canonical": False,
            "solve_claim": False,
            "notes": "Preserved from Stage 4A/Deep Research review as a false-positive class, not evidence.",
        }
        for slug, description, why, use in NEGATIVE_CONTROL_SPECS
    ]
