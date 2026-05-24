"""Stage 5AK community-facts claim and policy records."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .community_facts import COMMUNITY_SOURCE_ID
from .export import write_jsonl, write_records, write_yaml
from .models import (
    STAGE5AK_CLAIM_POLICY_PATH,
    STAGE5AK_CLAIM_RECORDS_PATH,
    STAGE5AK_CLUE_CATEGORIES_PATH,
    STAGE5AK_CORRECTION_LOG_PATH,
    STAGE5AK_ID,
    STAGE5AK_OUTPUT_DIR,
    STAGE5AK_REPORTS,
    STAGE5AK_SOURCE_ROOT,
    STAGE5AK_SOURCE_STAGE_ID,
)


CLUE_CATEGORIES = [
    "community_number_fact_thread",
    "no_fehu_section_count_graph",
    "p54_55_p56_p57_hash_length_equivalence",
    "p15_red_text_progressive_sum_square",
    "red_3299_fehu_count_prime_index",
    "p56_p57_fehu_boundary_prime_observations",
    "final_jpg_gp_runs_road_phrase",
    "artwork_red_header_gp_match",
    "pixel_measurement_prime_dimension_claims",
    "whitespace_prime_sequence_claim",
    "cicada_prime_index_number_network",
    "transcript_word_count_conflict",
    "count_policy_correction_log",
    "base60_emirp_index_observations",
    "doublet_route_index_observations",
]


def build_community_claim_records(
    *,
    source_root: Path = STAGE5AK_SOURCE_ROOT,
    attachment_index_path: Path | None = None,
    claim_policy_out: Path = STAGE5AK_CLAIM_POLICY_PATH,
    claim_records_out: Path = STAGE5AK_CLAIM_RECORDS_PATH,
    correction_log_out: Path = STAGE5AK_CORRECTION_LOG_PATH,
    clue_categories_out: Path = STAGE5AK_CLUE_CATEGORIES_PATH,
    results_dir: Path = STAGE5AK_OUTPUT_DIR,
) -> dict[str, Any]:
    """Write policy, claim, correction, and clue-category records."""

    del attachment_index_path
    policy = _claim_policy(source_root)
    claims = _claim_records(source_root)
    corrections = _correction_records(source_root)
    categories = _clue_categories()
    claim_header = {
        "record_type": "stage5ak_community_facts_claim_records",
        "schema": "schemas/source-harvester/community-facts-claim-record-v0.schema.json",
        "stage_id": STAGE5AK_ID,
        "source_stage_id": STAGE5AK_SOURCE_STAGE_ID,
        "source_id": COMMUNITY_SOURCE_ID,
        "claim_record_count": len(claims),
        "execution_ready_count": 0,
        "source_lock_required_count": sum("source_lock_required" in record["verification_status"] for record in claims),
        "requires_null_controls_count": sum(1 for record in claims if record["requires_null_controls"]),
        "website_publication_allowed_count": 0,
        "solve_claim": False,
    }
    correction_header = {
        "record_type": "stage5ak_community_facts_correction_log",
        "schema": "schemas/source-harvester/community-facts-correction-log-v0.schema.json",
        "stage_id": STAGE5AK_ID,
        "source_stage_id": STAGE5AK_SOURCE_STAGE_ID,
        "source_id": COMMUNITY_SOURCE_ID,
        "correction_record_count": len(corrections),
        "arithmetic_error_count": sum(1 for record in corrections if record["correction_type"] == "arithmetic_error"),
        "solve_claim": False,
    }
    category_header = {
        "record_type": "stage5ak_community_facts_clue_categories",
        "schema": "schemas/source-harvester/community-facts-clue-category-v0.schema.json",
        "stage_id": STAGE5AK_ID,
        "source_stage_id": STAGE5AK_SOURCE_STAGE_ID,
        "new_clue_category_records": len(categories),
        "execution_ready_count": 0,
        "solve_claim": False,
    }
    write_yaml(claim_policy_out, policy)
    write_records(claim_records_out, claims, **claim_header)
    write_records(correction_log_out, corrections, **correction_header)
    write_records(clue_categories_out, categories, **category_header)
    write_jsonl(results_dir / STAGE5AK_REPORTS["claim_records"], claims)
    write_jsonl(results_dir / STAGE5AK_REPORTS["correction_log"], corrections)
    return {
        "policy": policy,
        "claims": {**claim_header, "records": claims},
        "corrections": {**correction_header, "records": corrections},
        "categories": {**category_header, "records": categories},
    }


def _claim_policy(source_root: Path) -> dict[str, Any]:
    return {
        "record_type": "stage5ak_community_claim_policy",
        "schema": "schemas/source-harvester/community-claim-policy-v0.schema.json",
        "stage_id": STAGE5AK_ID,
        "source_stage_id": STAGE5AK_SOURCE_STAGE_ID,
        "source_id": COMMUNITY_SOURCE_ID,
        "source_log_path": f"{source_root.as_posix()}/community-facts-collection.txt",
        "required_fields": [
            "claim_id",
            "claim_family",
            "source_id",
            "source_log_path",
            "source_message_locator",
            "source_image_refs",
            "image_order",
            "claim_text",
            "claim_formula",
            "input_entities",
            "claimed_values",
            "verification_status",
            "verification_method",
            "correction_status",
            "risk_level",
            "requires_exact_transcript",
            "requires_exact_image_source",
            "requires_null_controls",
            "execution_ready",
            "solve_claim",
            "publication_status",
            "deep_research_private_allowed",
            "website_publication_allowed",
        ],
        "verification_statuses": [
            "unverified",
            "arithmetic_verified_only",
            "arithmetic_error",
            "source_lock_required",
            "requires_transcript_policy",
            "requires_image_coordinate_policy",
            "requires_null_controls",
            "corrected_by_thread",
            "ambiguous",
            "deferred",
        ],
        "risk_levels": ["low", "medium", "medium_high", "high", "very_high"],
        "execution_ready": False,
        "solve_claim": False,
        "website_publication_allowed": False,
        "deep_research_private_allowed": True,
    }


def _claim_records(source_root: Path) -> list[dict[str, Any]]:
    specs: list[dict[str, Any]] = [
        {
            "claim_family": "no_fehu_section_count_graph",
            "source_image_refs": ["7.webp", "8.webp", "9.webp", "10.webp"],
            "image_order": [7, 8, 9, 10],
            "claim_text": "No-Fehu section-count graph reports several cross-section equalities after removing Fehu.",
            "claim_formula": "2883, 1894, 1433, 1814, 695, and 91 section-count identities",
            "input_entities": ["section rune counts", "Fehu removal policy", "Liber Primus section labels"],
            "claimed_values": {
                "2883": "Spirals + Branches + Pre-Mobius table = NO Fehu Spiral Branches",
                "1894": "NO Fehu Koan 1 + NO Fehu Loss of Divinity + NO Fehu Koan 2 + NO Fehu Instruction = Mobius",
                "1433": "Wing Tree = NO Fehu Cuneiform = NO Fehu Koan 2 + NO Fehu Spirals",
                "1814": "NO Fehu Koan 1 + NO Fehu Loss of Divinity + NO Fehu Koan 2 = NO Fehu Sign Post + NO Fehu Spirals",
                "695": "Koan 1 - KT1 = NO Fehu Sign Post",
                "91": "NO Fehu Warning - Parable = WT 3 dots",
            },
            "verification_status": "source_lock_required",
            "verification_method": "manual_review_summary_only",
            "risk_level": "medium_high",
            "requires_exact_transcript": True,
            "requires_exact_image_source": False,
            "requires_null_controls": True,
            "recommended_future_test": "deterministic section-count reconstruction plus null controls",
        },
        {
            "claim_family": "p54_55_p56_p57_hash_length_equivalence",
            "source_image_refs": ["3.webp"],
            "image_order": [3],
            "claim_text": "p54-55 total runes are claimed to equal p56 and p57 runes plus 128 hash characters.",
            "claim_formula": "54-55 runes = 308; p56 + p57 runes + 128 hash chars = 308; hash decimal digits = 154 = 308/2",
            "input_entities": ["p54", "p55", "p56", "p57", "512-bit hash text"],
            "claimed_values": {"p54_55_total_runes": 308, "hash_chars": 128, "hash_decimal_digits": 154},
            "verification_status": "source_lock_required",
            "verification_method": "manual_review_summary_only",
            "risk_level": "medium",
            "requires_exact_transcript": True,
            "requires_exact_image_source": False,
            "requires_null_controls": True,
            "recommended_future_test": "source-locked transcript/profile count reconstruction",
        },
        {
            "claim_family": "p15_red_text_progressive_sum_square",
            "source_image_refs": ["2.webp"],
            "image_order": [2],
            "claim_text": "Progressive GP sums of page-15 red words reportedly sum to 2472, which appears in the page-15 number square.",
            "claim_formula": "2 + 5 + 78 + 149 + 246 + 355 + 458 + 541 + 638 = 2472",
            "input_entities": ["page 15 red words", "Gematria Primus sums", "page 15 number square"],
            "claimed_values": {"progressive_sums": [2, 5, 78, 149, 246, 355, 458, 541, 638], "sum": 2472},
            "verification_status": "source_lock_required",
            "verification_method": "manual_review_summary_only",
            "risk_level": "high",
            "requires_exact_transcript": True,
            "requires_exact_image_source": True,
            "requires_null_controls": True,
            "recommended_future_test": "red-marker source lock plus null square membership controls",
        },
        {
            "claim_family": "red_3299_fehu_count_prime_index",
            "source_image_refs": ["4.webp"],
            "image_order": [4],
            "claim_text": "Reported Fehu count links 463, its prime index, the 463rd prime, and red 3299.",
            "claim_formula": "Fehu count = 463; prime_index(463)=90; nth_prime(463)=3299",
            "input_entities": ["pages 0-57", "An End decrypted policy", "page 15 red number square"],
            "claimed_values": {"fehu_count": 463, "prime_index_463": 90, "prime_463": 3299},
            "verification_status": "arithmetic_verified_only",
            "verification_method": "arithmetic_preflight_for_prime_index_facts",
            "risk_level": "medium_high",
            "requires_exact_transcript": True,
            "requires_exact_image_source": True,
            "requires_null_controls": True,
            "recommended_future_test": "source-locked Fehu count plus red-square source validation",
        },
        {
            "claim_family": "p56_p57_fehu_boundary_prime_observations",
            "source_image_refs": ["3.webp", "4.webp"],
            "image_order": [3, 4],
            "claim_text": "p56/p57 boundary claims connect page/rune positions and GP sums to prime indices.",
            "claim_formula": "p56 is 57th page; skipped F is 57th rune; GP(SEEK OUT)=269=57th prime; initials TH D W A E sum to 277=59th prime",
            "input_entities": ["p56", "p57", "boundary phrase", "SEEK OUT"],
            "claimed_values": {"seek_out_gp": 269, "prime_57": 269, "initials_sum": 277, "prime_59": 277},
            "verification_status": "source_lock_required",
            "verification_method": "manual_review_summary_only",
            "risk_level": "medium_high",
            "requires_exact_transcript": True,
            "requires_exact_image_source": False,
            "requires_null_controls": True,
            "recommended_future_test": "transcript policy and boundary-position reconstruction",
        },
        {
            "claim_family": "artwork_red_header_gp_match",
            "source_image_refs": ["3.webp", "4.webp"],
            "image_order": [3, 4],
            "claim_text": "Artwork/red-header labels are claimed to have paired GP sums and phi(761) relation.",
            "claim_formula": "GP(PARABLE)=GP(MAYFLY)=449; GP(AN END)=GP(FIVE DOTS)=311; 449+311=760=phi(761)",
            "input_entities": ["PARABLE", "MAYFLY", "AN END", "FIVE DOTS", "761"],
            "claimed_values": {"parable_mayfly": 449, "an_end_five_dots": 311, "sum": 760, "phi_761": 760},
            "verification_status": "arithmetic_verified_only",
            "verification_method": "arithmetic_preflight_for_449_plus_311_and_phi_761_only",
            "risk_level": "high",
            "requires_exact_transcript": False,
            "requires_exact_image_source": True,
            "requires_null_controls": True,
            "recommended_future_test": "label policy source lock plus GP helper verification",
        },
        {
            "claim_family": "final_jpg_gp_runs_road_phrase",
            "source_image_refs": [],
            "image_order": [],
            "claim_text": "Candidate GP windows in Final.jpg message reportedly sum to 3301, 991, and 1229 and are linked to road wording.",
            "claim_formula": "Final.jpg GP windows -> 3301, 991, 1229; road wording linked to 2016 phrase",
            "input_entities": ["Final.jpg", "early puzzle message", "2016 road wording"],
            "claimed_values": {"gp_windows": [3301, 991, 1229]},
            "verification_status": "source_lock_required",
            "verification_method": "manual_review_summary_only",
            "risk_level": "medium_high",
            "requires_exact_transcript": True,
            "requires_exact_image_source": True,
            "requires_null_controls": True,
            "recommended_future_test": "exact source text/image lock plus predefined GP windows",
        },
        {
            "claim_family": "pixel_measurement_prime_dimension_claims",
            "source_image_refs": ["6.webp"],
            "image_order": [6],
            "claim_text": "Image dimensions and pixel shifts are claimed to involve consecutive primes and 1033-like distances.",
            "claim_formula": "2014/2016 image dimensions and 1033/p56/p57 pixel-shift or dot-distance claims",
            "input_entities": ["2014 image", "2016 image", "p56/p57 overlays", "pixel coordinates"],
            "claimed_values": {"distance_hint": 1033},
            "verification_status": "requires_image_coordinate_policy",
            "verification_method": "manual_review_summary_only",
            "risk_level": "very_high",
            "requires_exact_transcript": False,
            "requires_exact_image_source": True,
            "requires_null_controls": True,
            "recommended_future_test": "source-locked image variants and coordinate-system declaration",
        },
        {
            "claim_family": "whitespace_prime_sequence_claim",
            "source_image_refs": [],
            "image_order": [],
            "claim_text": "Concatenated primes reportedly appear in whitespace of post-2014 messages.",
            "claim_formula": "23571113172329313753257 is claimed from whitespace extraction and is prime",
            "input_entities": ["post-2014 messages", "whitespace extraction policy"],
            "claimed_values": {"candidate_number": 23571113172329313753257},
            "verification_status": "source_lock_required",
            "verification_method": "arithmetic_preflight_can_verify_primality_only",
            "risk_level": "high",
            "requires_exact_transcript": True,
            "requires_exact_image_source": False,
            "requires_null_controls": True,
            "recommended_future_test": "source-locked whitespace extraction method plus null controls",
        },
        {
            "claim_family": "cicada_prime_index_number_network",
            "source_image_refs": ["5.webp"],
            "image_order": [5],
            "claim_text": "Cicada constants are connected through prime-index arithmetic and a 9901/3301-squared visual context.",
            "claim_formula": "761+167=928; 928/2=464; prime_index(3301)=464; prime_index(761)+prime_index(167)=174; nth_prime(174)=1033",
            "input_entities": ["761", "167", "3301", "1033", "9901"],
            "claimed_values": {"761_plus_167": 928, "half": 464, "prime_index_3301": 464, "prime_index_sum": 174, "prime_174": 1033},
            "verification_status": "arithmetic_verified_only",
            "verification_method": "arithmetic_preflight_only",
            "risk_level": "high",
            "requires_exact_transcript": False,
            "requires_exact_image_source": True,
            "requires_null_controls": True,
            "recommended_future_test": "number-network null controls and source context separation",
        },
        {
            "claim_family": "base60_emirp_index_observations",
            "source_image_refs": [],
            "image_order": [],
            "claim_text": "3301 base-60 and reversed base-60 observations are connected to emirp-index context.",
            "claim_formula": "3301 base60 = [55,1]; 1*60+55 = 115",
            "input_entities": ["3301", "base60", "emirp index"],
            "claimed_values": {"base60_digits": [55, 1], "reversed_value": 115},
            "verification_status": "arithmetic_verified_only",
            "verification_method": "base_conversion_only",
            "risk_level": "medium_high",
            "requires_exact_transcript": False,
            "requires_exact_image_source": False,
            "requires_null_controls": True,
            "recommended_future_test": "base-convention policy plus cuneiform/base60 source review",
        },
        {
            "claim_family": "doublet_route_index_observations",
            "source_image_refs": ["1.webp"],
            "image_order": [1],
            "claim_text": "First doublet-pair route claim reports indexed route values summing to 174, prime index of 1033.",
            "claim_formula": "indices 122,117,88,83,78,61,44,1; GP values 5,29,5,5,17,17,43,53; sum=174",
            "input_entities": ["doublet pair route", "GP values", "indexing convention"],
            "claimed_values": {"indices": [122, 117, 88, 83, 78, 61, 44, 1], "gp_values": [5, 29, 5, 5, 17, 17, 43, 53], "sum": 174, "prime_174": 1033},
            "verification_status": "source_lock_required",
            "verification_method": "manual_review_summary_only",
            "risk_level": "high",
            "requires_exact_transcript": True,
            "requires_exact_image_source": True,
            "requires_null_controls": True,
            "recommended_future_test": "declared indexing convention plus route null controls",
        },
    ]
    return [_claim_record(index, spec, source_root) for index, spec in enumerate(specs, start=1)]


def _claim_record(index: int, spec: dict[str, Any], source_root: Path) -> dict[str, Any]:
    family = spec["claim_family"]
    return {
        "record_type": "stage5ak_community_facts_claim_record",
        "schema": "schemas/source-harvester/community-facts-claim-record-v0.schema.json",
        "stage_id": STAGE5AK_ID,
        "source_stage_id": STAGE5AK_SOURCE_STAGE_ID,
        "claim_id": f"stage5ak-{family}",
        "claim_family": family,
        "source_id": COMMUNITY_SOURCE_ID,
        "source_log_path": f"{source_root.as_posix()}/community-facts-collection.txt",
        "source_message_locator": f"community-facts-collection.txt:manual-review:{index:02d}",
        "source_image_refs": spec["source_image_refs"],
        "image_order": spec["image_order"],
        "claim_text": spec["claim_text"],
        "claim_formula": spec["claim_formula"],
        "input_entities": spec["input_entities"],
        "claimed_values": spec["claimed_values"],
        "verification_status": spec["verification_status"],
        "verification_method": spec["verification_method"],
        "correction_status": "not_corrected",
        "risk_level": spec["risk_level"],
        "requires_exact_transcript": spec["requires_exact_transcript"],
        "requires_exact_image_source": spec["requires_exact_image_source"],
        "requires_null_controls": spec["requires_null_controls"],
        "execution_ready": False,
        "solve_claim": False,
        "publication_status": "blocked_private_or_sensitive_until_review",
        "deep_research_private_allowed": True,
        "website_publication_allowed": False,
        "recommended_future_test": spec["recommended_future_test"],
    }


def _correction_records(source_root: Path) -> list[dict[str, Any]]:
    specs = [
        {
            "correction_id": "stage5ak-correction-13136-plus-256",
            "claim_family": "count_policy_correction_log",
            "correction_type": "arithmetic_error",
            "original_claim": "13136 + 256 = 13397",
            "corrected_value": "13136 + 256 = 13392",
            "verification_status": "arithmetic_error",
        },
        {
            "correction_id": "stage5ak-correction-goya-rasputin",
            "claim_family": "count_policy_correction_log",
            "correction_type": "thread_correction",
            "original_claim": "GOYA + RASPUTIN = 560",
            "corrected_value": "GOYA + RASPUTIN = 550",
            "verification_status": "corrected_by_thread",
        },
        {
            "correction_id": "stage5ak-correction-word-count-conflict",
            "claim_family": "transcript_word_count_conflict",
            "correction_type": "count_policy_conflict",
            "original_claim": "word count 2941/2942 conflict",
            "corrected_value": "requires transcript/count-policy reconciliation",
            "verification_status": "requires_transcript_policy",
        },
        {
            "correction_id": "stage5ak-correction-wing-tree-three-dots",
            "claim_family": "count_policy_correction_log",
            "correction_type": "thread_correction",
            "original_claim": "older Wing Tree / WT 3 dots counts",
            "corrected_value": "corrected by later thread values; needs exact source lock",
            "verification_status": "corrected_by_thread",
        },
    ]
    return [
        {
            "record_type": "stage5ak_community_facts_correction_record",
            "schema": "schemas/source-harvester/community-facts-correction-log-v0.schema.json",
            "stage_id": STAGE5AK_ID,
            "source_stage_id": STAGE5AK_SOURCE_STAGE_ID,
            "source_id": COMMUNITY_SOURCE_ID,
            "source_log_path": f"{source_root.as_posix()}/community-facts-collection.txt",
            "source_message_locator": f"community-facts-collection.txt:manual-review:correction:{index:02d}",
            "execution_ready": False,
            "solve_claim": False,
            "website_publication_allowed": False,
            "deep_research_private_allowed": True,
            **spec,
        }
        for index, spec in enumerate(specs, start=1)
    ]


def _clue_categories() -> list[dict[str, Any]]:
    records = []
    for category in CLUE_CATEGORIES:
        risk = "very_high" if category in {"pixel_measurement_prime_dimension_claims"} else "high"
        if category in {"community_number_fact_thread", "transcript_word_count_conflict", "count_policy_correction_log"}:
            risk = "medium_high"
        records.append(
            {
                "record_type": "stage5ak_community_facts_clue_category",
                "schema": "schemas/source-harvester/community-facts-clue-category-v0.schema.json",
                "stage_id": STAGE5AK_ID,
                "source_stage_id": STAGE5AK_SOURCE_STAGE_ID,
                "category_id": category,
                "description": category.replace("_", " "),
                "source_lock_priority": "A1" if category in {"no_fehu_section_count_graph", "count_policy_correction_log"} else "A2",
                "execution_ready": False,
                "requires_null_controls": category
                not in {"transcript_word_count_conflict", "count_policy_correction_log", "community_number_fact_thread"},
                "risk_level": risk,
                "recommended_sources": [COMMUNITY_SOURCE_ID],
                "what_not_to_assume": "Do not treat community number facts as intentional, canonical, execution-ready, or solve evidence.",
                "recommended_future_test": "source-lock inputs, declare policies, then run bounded null-controlled verifier if later approved.",
                "solve_claim": False,
            }
        )
    return records
