"""Future manifest readiness records for Stage 4L."""

from __future__ import annotations

from typing import Any

from libreprimus.observation_promotion.models import FUTURE_MANIFEST_TARGETS


def build_manifest_readiness_records() -> list[dict[str, Any]]:
    """Build disabled future-manifest readiness records."""

    records: list[dict[str, Any]] = []
    for target in FUTURE_MANIFEST_TARGETS:
        spec = _manifest_spec(target)
        records.append(
            {
                "record_type": "manifest_readiness_record",
                "manifest_readiness_id": f"stage4l-manifest-readiness-{target}",
                "future_manifest_id": target,
                "ready_state": spec["ready_state"],
                "blockers": spec["blockers"],
                "source_requirements": spec["source_requirements"],
                "review_requirements": spec["review_requirements"],
                "expected_candidate_cap": spec["expected_candidate_cap"],
                "recommended_next_stage": spec["recommended_next_stage"],
                "execution_enabled": False,
                "solve_claim": False,
                "no_solve_claim": True,
                "canonical_corpus_active": False,
                "page_boundaries_final": False,
                "cuda_used": False,
                "cuda_enabled": False,
            }
        )
    return records


def _manifest_spec(target: str) -> dict[str, Any]:
    specs: dict[str, dict[str, Any]] = {
        "gp_rune_verifier_batch002": {
            "ready_state": "blocked",
            "blockers": ["reviewed_gp_span_records_missing"],
            "source_requirements": ["exact span references", "source locks"],
            "review_requirements": ["accepted GP/rune claims"],
            "expected_candidate_cap": 64,
            "recommended_next_stage": "no_action",
        },
        "dot_ambiguity_audit_v1": {
            "ready_state": "control_only",
            "blockers": [],
            "source_requirements": ["dot observation records"],
            "review_requirements": ["ambiguity preserved"],
            "expected_candidate_cap": 32,
            "recommended_next_stage": "Stage 4M",
        },
        "delimiter_handedness_v1": {
            "ready_state": "blocked",
            "blockers": ["delimiter_meaning_needs_human_review"],
            "source_requirements": ["page/region evidence"],
            "review_requirements": ["accepted delimiter interpretation"],
            "expected_candidate_cap": 32,
            "recommended_next_stage": "no_action",
        },
        "onion7_raw_routes_v1": {
            "ready_state": "deferred",
            "blockers": ["reviewed_route_inputs_not_promoted"],
            "source_requirements": ["source-locked route table"],
            "review_requirements": ["raw/derived value separation"],
            "expected_candidate_cap": 128,
            "recommended_next_stage": "no_action",
        },
        "cookie_pack_v2": {
            "ready_state": "blocked",
            "blockers": ["stage4g_exact_cookie_refresh_zero_matches"],
            "source_requirements": ["new exact source-backed strings"],
            "review_requirements": ["new source-lock review"],
            "expected_candidate_cap": 384,
            "recommended_next_stage": "no_action",
        },
        "cuneiform_reading_pack_v1": {
            "ready_state": "blocked",
            "blockers": ["coordinates_and_accepted_reading_missing"],
            "source_requirements": ["page image reference", "coordinates"],
            "review_requirements": ["accepted reading"],
            "expected_candidate_cap": 32,
            "recommended_next_stage": "no_action",
        },
        "visual_negative_controls_v1": {
            "ready_state": "control_only",
            "blockers": [],
            "source_requirements": ["negative-control descriptions"],
            "review_requirements": ["control-only handling"],
            "expected_candidate_cap": 64,
            "recommended_next_stage": "Stage 4M",
        },
        "outguess_positive_negative_matrix": {
            "ready_state": "blocked",
            "blockers": ["toolchain_unavailable", "expected_output_hash_missing"],
            "source_requirements": ["source-locked fixtures", "expected outputs"],
            "review_requirements": ["positive and negative fixture labels"],
            "expected_candidate_cap": 16,
            "recommended_next_stage": "no_action",
        },
        "mp3_instar_regression_prep": {
            "ready_state": "blocked",
            "blockers": ["toolchain_unavailable", "expected_output_hash_missing"],
            "source_requirements": ["source-locked audio fixtures"],
            "review_requirements": ["expected output policy"],
            "expected_candidate_cap": 16,
            "recommended_next_stage": "no_action",
        },
        "lp_image_variant_hash_dimension_audit": {
            "ready_state": "deferred",
            "blockers": ["raw_image_variants_not_locked"],
            "source_requirements": ["image source variants", "hash/dimension locks"],
            "review_requirements": ["no interpretation"],
            "expected_candidate_cap": 256,
            "recommended_next_stage": "Stage 4M",
        },
        "image_compression_artifact_preflight": {
            "ready_state": "deferred",
            "blockers": ["source_variant_preflight_required"],
            "source_requirements": ["variant hashes", "negative controls"],
            "review_requirements": ["artifact candidates remain non-evidence"],
            "expected_candidate_cap": 128,
            "recommended_next_stage": "Stage 4M",
        },
        "cpu_batch_expansion_future": {
            "ready_state": "deferred",
            "blockers": ["requires_reviewed_ready_manifest_inputs"],
            "source_requirements": ["promotion readiness records"],
            "review_requirements": ["manifest-specific acceptance"],
            "expected_candidate_cap": 512,
            "recommended_next_stage": "no_action",
        },
        "exp_stage4m_bigram_diagonal_fibonacci_421_audit": {
            "ready_state": "blocked",
            "blockers": [
                "needs_reproducible_bigram_matrix",
                "needs_declared_rune_order",
                "needs_null_model",
                "needs_pattern_predefinition",
            ],
            "source_requirements": ["exact transcript/profile source", "reproducible bigram matrix"],
            "review_requirements": ["declared rune order", "predefined pattern and null model"],
            "expected_candidate_cap": 1,
            "recommended_next_stage": "Stage 4M",
        },
    }
    return specs[target]
