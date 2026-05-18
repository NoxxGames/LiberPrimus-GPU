"""Negative-control records for known Stage 3R false-positive classes."""

from __future__ import annotations

from typing import Any


def build_negative_control_records() -> list[dict[str, Any]]:
    """Return redacted negative-control records for future falsification checks."""
    rows = [
        (
            "stage3r-negative-2016-qr-background-blocks",
            "2016_qr_background_blocks",
            "Treat QR-background block readings as negative controls unless exact public artefact geometry is locked.",
            "https://uncovering-cicada.fandom.com/wiki/2016_Message",
        ),
        (
            "stage3r-negative-2016-dendrite-interpretation",
            "2016_dendrite_interpretation",
            "Treat dendrite-style visual interpretations as review-only until independently sourced.",
            "https://uncovering-cicada.fandom.com/wiki/2016_Message",
        ),
        (
            "stage3r-negative-2014-imgur-filename-clue",
            "2014_imgur_filename_clue",
            "Do not treat image-hosting filename patterns as clues without authenticated source locking.",
            "https://uncovering-cicada.fandom.com/wiki/CICADA_3301_2014_PUZZLE",
        ),
        (
            "stage3r-negative-2014-brightness-hidden-cicada",
            "2014_brightness_only_hidden_silhouette",
            "Brightness-only hidden-silhouette readings are negative controls without stronger artefact evidence.",
            "https://uncovering-cicada.fandom.com/wiki/CICADA_3301_2014_PUZZLE",
        ),
        (
            "stage3r-negative-onion7-related-snippets",
            "onion7_unverified_related_snippets",
            "Quarantine Onion 7 related-snippet and Mobius/spiral extrapolations not tied to exact tables.",
            "https://uncovering-cicada.fandom.com/wiki/Onion_7:_numbers_on_page_15",
        ),
        (
            "stage3r-negative-dots-unique-code",
            "dots_unique_binary_braille_constellation",
            "Dot motifs are not unique binary, braille, or constellation encodings without exact geometry controls.",
            "https://uncovering-cicada.fandom.com/wiki/Liber_Primus_Unsolved_Pages",
        ),
        (
            "stage3r-negative-roots-branches-fibonacci",
            "roots_branches_fibonacci_instruction",
            "Roots/branches-as-Fibonacci instructions remain negative controls until exact source evidence exists.",
            "https://uncovering-cicada.fandom.com/wiki/Possible_hints_never_used",
        ),
        (
            "stage3r-negative-2016-gp-fibonacci-prime",
            "2016_gp_sum_fibonacci_prime_coincidence",
            "GP-sum/Fibonacci-prime coincidences require transcript-locked recomputation before use.",
            "https://uncovering-cicada.fandom.com/wiki/2016_Message",
        ),
        (
            "stage3r-negative-unsigned-post-2017-claims",
            "unsigned_post_2017_cicada_claims",
            "Unsigned post-2017 claims are negative-control material unless signed/public provenance is shown.",
            "https://uncovering-cicada.fandom.com/wiki/PGP_Signed_Message_April_2017",
        ),
        (
            "stage3r-negative-broad-cookie-gpu-cracking",
            "broad_cookie_bruteforce_gpu_hash_attack",
            "Broad cookie brute force and GPU hash attacks are out of scope for bounded archive tests.",
            "https://uncovering-cicada.fandom.com/wiki/What_Happened_Part_1_(2013)",
        ),
        (
            "stage3r-negative-ai-harmonic-key-proposal",
            "ai_generated_harmonic_key_proposal",
            "AI-generated harmonic-key proposals are review notes only, not evidence or experiment seeds.",
            "https://uncovering-cicada.fandom.com/wiki/Possible_hints_never_used",
        ),
    ]
    return [
        {
            "record_type": "negative_control_record",
            "negative_control_id": control_id,
            "false_positive_class": false_positive_class,
            "description": description,
            "source_url": source_url,
            "basis": "Stage 3R Discord lead-triage policy and public-reference corroboration requirement.",
            "recommended_use": "Use as a negative control when future review or experiments encounter this claim class.",
            "raw_message_committed": False,
            "username_committed": False,
            "private_url_committed": False,
            "trusted_as_canonical": False,
            "solve_claim": False,
            "notes": "Preserved as a false-positive class; not evidence of a solve.",
        }
        for control_id, false_positive_class, description, source_url in rows
    ]
