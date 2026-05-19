"""Stage 4B visual and numeric observation intake records."""

from __future__ import annotations

from typing import Any


def build_visual_observations() -> list[dict[str, Any]]:
    """Return conservative Stage 4B visual/numeric observation records."""

    return [
        {
            "record_type": "stage4b_visual_observation_record",
            "observation_id": "stage4b-cuneiform-17-13-55-1",
            "observation_family": "cuneiform_base60",
            "source_id": "stage4b-uncovering-lp-unsolved-pages",
            "page_refs": ["pages-33-39-cuneiform-cluster"],
            "classification": "observation_to_review",
            "evidence_strength": "medium",
            "false_positive_risk": "high",
            "recommended_action": "observation-review now",
            "candidate_readings": [
                {
                    "reading_id": "stage4b-cuneiform-tuple-17-13-55-1",
                    "reading_type": "sexagesimal_digit_sequence",
                    "value": [17, 13, 55, 1],
                    "confidence": "review_required",
                    "notes": "Arithmetic is internally consistent if the visual segmentation is accepted.",
                }
            ],
            "derived_values": {
                "pair_17_13_base60": 1033,
                "pair_55_1_base60": 3301,
                "full_base60": 3722101,
                "full_base60_mod29": 9,
                "1033_mod29": 18,
                "3301_mod29": 24,
            },
            "ambiguity_notes": "Glyph segmentation is not verified; exact page coordinates and alternative readings are required before seed execution.",
            "review_status": "human_review_required",
            "trusted_as_canonical": False,
            "usable_as_experiment_seed": False,
            "solve_claim": False,
            "notes": "Observation-to-review only; not proof that the cuneiform reading is correct.",
        },
        {
            "record_type": "stage4b_visual_observation_record",
            "observation_id": "stage4b-delimiter-three-dot-page5",
            "observation_family": "mirrored_three_dot_delimiter",
            "source_id": "stage4b-uncovering-lp-unsolved-pages",
            "page_refs": ["page-5"],
            "classification": "observation_to_review",
            "evidence_strength": "medium",
            "false_positive_risk": "medium",
            "recommended_action": "observation-review now",
            "candidate_readings": [
                {
                    "reading_id": "stage4b-page5-three-dot-delimiter",
                    "reading_type": "delimiter_punctuation",
                    "value": "mirrored_three_dot_variant",
                    "confidence": "review_required",
                    "notes": "Delimiter/punctuation observation, not a binary seed.",
                }
            ],
            "derived_values": {},
            "ambiguity_notes": "Needs exact coordinates and a complete delimiter inventory across locked page images.",
            "review_status": "human_review_required",
            "trusted_as_canonical": False,
            "usable_as_experiment_seed": False,
            "solve_claim": False,
            "notes": "Stronger than free-form dot symbolism because it is tied to visible punctuation.",
        },
        {
            "record_type": "stage4b_visual_observation_record",
            "observation_id": "stage4b-delimiter-three-dot-page56",
            "observation_family": "mirrored_three_dot_delimiter",
            "source_id": "stage4b-uncovering-lp-unsolved-pages",
            "page_refs": ["page-56"],
            "classification": "observation_to_review",
            "evidence_strength": "medium",
            "false_positive_risk": "medium",
            "recommended_action": "observation-review now",
            "candidate_readings": [
                {
                    "reading_id": "stage4b-page56-three-dot-delimiter",
                    "reading_type": "delimiter_punctuation",
                    "value": "mirrored_three_dot_variant",
                    "confidence": "review_required",
                    "notes": "Delimiter/punctuation observation, not a binary seed.",
                }
            ],
            "derived_values": {},
            "ambiguity_notes": "Needs exact coordinates and review before any handedness/reset hypothesis is tested.",
            "review_status": "human_review_required",
            "trusted_as_canonical": False,
            "usable_as_experiment_seed": False,
            "solve_claim": False,
            "notes": "Preserved for Stage 4C annotation, not experiment execution.",
        },
        {
            "record_type": "stage4b_visual_observation_record",
            "observation_id": "stage4b-dot-binary-13-31-ambiguity",
            "observation_family": "dot_binary_ambiguity",
            "source_id": "stage4b-uncovering-lp-unsolved-pages",
            "page_refs": ["page-39", "five-dot-motif", "three-dot-motif"],
            "classification": "debunk_or_false_positive",
            "evidence_strength": "medium",
            "false_positive_risk": "extreme",
            "recommended_action": "add negative control",
            "candidate_readings": [
                {
                    "reading_id": "stage4b-five-dot-rotations",
                    "reading_type": "five_bit_rotation_values",
                    "value": [13, 26, 21, 11, 22],
                    "confidence": "review_required",
                    "notes": "13 is one possible reading, not a forced reading.",
                },
                {
                    "reading_id": "stage4b-three-dot-31-ambiguity",
                    "reading_type": "three_dot_candidate_values",
                    "value": [7, 11, 13, 14, 19, 21, 22, 25, 26, 28, 31],
                    "confidence": "review_required",
                    "notes": "31 depends on grouping/polarity choices and is not forced.",
                },
            ],
            "derived_values": {"forced_13_or_31": False},
            "ambiguity_notes": "Ambiguous and unforced: bit order, polarity, anchor, grouping, and rotation change the values.",
            "review_status": "negative_control",
            "trusted_as_canonical": False,
            "usable_as_experiment_seed": False,
            "solve_claim": False,
            "notes": "Use as an ambiguity control before any dot-derived candidate pack.",
        },
        {
            "record_type": "stage4b_visual_observation_record",
            "observation_id": "stage4b-onion7-number-square-raw",
            "observation_family": "number_square_raw",
            "source_id": "stage4b-complete-archive-magicsquares",
            "page_refs": ["interconnectedness-magicsquares"],
            "classification": "experiment_candidate",
            "evidence_strength": "high",
            "false_positive_risk": "low",
            "recommended_action": "queue bounded experiment",
            "candidate_readings": [
                {
                    "reading_id": "stage4b-magicsquares-raw-pending",
                    "reading_type": "raw_number_square_values_pending_source_lock",
                    "value": "pending_source_lock",
                    "confidence": "review_required",
                    "notes": "Raw square values must be locked before any no-fudge route test.",
                }
            ],
            "derived_values": {},
            "ambiguity_notes": "No ad-hoc prime-nearby or magic-square arithmetic is allowed before raw values are locked.",
            "review_status": "human_review_required",
            "trusted_as_canonical": False,
            "usable_as_experiment_seed": False,
            "solve_claim": False,
            "notes": "Queue metadata only; Stage 4B does not execute number-square routes.",
        },
        {
            "record_type": "stage4b_visual_observation_record",
            "observation_id": "stage4b-cookie-167-761-exact-artifacts",
            "observation_family": "cookie_hash_artifacts",
            "source_id": "stage4b-uncovering-what-happened-2014",
            "page_refs": ["cookie-2013-167-v0", "cookie-2013-761-v0"],
            "classification": "experiment_candidate",
            "evidence_strength": "medium",
            "false_positive_risk": "medium",
            "recommended_action": "queue bounded experiment",
            "candidate_readings": [
                {
                    "reading_id": "stage4b-cookie-keys-167-761",
                    "reading_type": "exact_cookie_key_ids",
                    "value": ["167", "761"],
                    "confidence": "medium",
                    "notes": "Existing exact artefacts remain source-review targets; no hash pack runs in Stage 4B.",
                }
            ],
            "derived_values": {},
            "ambiguity_notes": "Only explicit source-backed strings may enter a future cookie candidate pack.",
            "review_status": "human_review_required",
            "trusted_as_canonical": False,
            "usable_as_experiment_seed": False,
            "solve_claim": False,
            "notes": "Preserves exact artefact scope without broad hash cracking.",
        },
    ]


def count_by_family(records: list[dict[str, Any]], family: str) -> int:
    return sum(1 for record in records if record.get("observation_family") == family)
