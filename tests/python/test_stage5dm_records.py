from __future__ import annotations

from libreprimus.token_block.stage5dm import (
    PAGE32_PRIME_INDICES,
    PAGE32_SPIRAL,
    verify_page32_relation,
)

from test_stage5dm_common import ensure_stage5dm_built, load_yaml


def test_stage5dm_does_not_rerun_stage5dl_and_keeps_gates_closed() -> None:
    ensure_stage5dm_built()
    summary = load_yaml("data/project-state/stage5dm-summary.yaml")

    assert summary["stage_id"] == "stage-5dm"
    assert summary["stage5dl_rerun_performed"] is False
    assert summary["stage5dl_records_assumed_present_for_stage5dm_addendum"] is True
    assert summary["pivot_target_selected_now"] is False
    assert summary["execution_authorized_now"] is False
    assert summary["target_class_validation_implemented"] is False
    assert summary["tor_network_access_performed"] is False
    assert summary["parallel_worker_cap_for_stage5dm_and_later"] == 8


def test_stage5dm_blake_source_family_is_context_only() -> None:
    ensure_stage5dm_built()
    record = load_yaml("data/historical-route/stage5dm-blake-visual-text-source-family.yaml")

    assert record["candidate_family_id"] == "blake_visual_text_source_family_v0"
    assert record["thematic_links_only"] is True
    assert record["cipher_key_claimed"] is False
    assert record["solve_claim"] is False
    assert record["ocr_performed"] is False
    assert record["visual_matching_performed_now"] is False


def test_stage5dm_sacred_book_overlay_index_is_alignment_aid() -> None:
    ensure_stage5dm_built()
    record = load_yaml("data/historical-route/stage5dm-lp-sacred-book-edition-overlay-index.yaml")

    assert record["overlay_family_id"] == "lp_sacred_book_edition_overlay_v0"
    assert record["overlay_primary_source_status"] is False
    assert record["overlay_human_alignment_aid"] is True
    assert record["raw_overlay_images_committed"] is False
    assert record["ocr_or_ai_interpretation_performed"] is False


def test_stage5dm_magic_square_precedent_records_word_number_interchange() -> None:
    ensure_stage5dm_built()
    record = load_yaml("data/historical-route/stage5dm-solved-magic-square-word-sum-precedent.yaml")

    assert record["candidate_family_id"] == "solved_magic_square_word_sum_precedent_v0"
    assert record["word_number_interchange_precedent"] is True
    assert record["magic_constant"] == 1033
    assert record["worked_row_sum_examples"][0]["sum"] == 1033
    assert record["broad_magic_square_search_performed_now"] is False


def test_stage5dm_page32_prime_relation_and_future_only_projection() -> None:
    ensure_stage5dm_built()
    record = load_yaml(
        "data/historical-route/stage5dm-page32-moebius-fibonacci-prime-index-spiral.yaml"
    )

    assert record["spiral_sequence"] == PAGE32_SPIRAL
    assert record["prime_index_sequence"] == PAGE32_PRIME_INDICES
    assert record["abs_3301_minus_prime_index_relation_verified"] is True
    assert all(row["relation_verified"] for row in verify_page32_relation())
    assert record["mod_153_projection_recorded_future_only"] is True
    assert record["route_extraction_performed_now"] is False
    assert record["page32_route_extraction_performed_now"] is False


def test_stage5dm_visual_motifs_doublet_and_atlas_are_review_only() -> None:
    ensure_stage5dm_built()
    motifs = load_yaml("data/historical-route/stage5dm-full-lp-page-visual-motif-index.yaml")
    doublet = load_yaml("data/historical-route/stage5dm-lp-doublet-scarcity-feature-candidate.yaml")
    atlas = load_yaml("data/project-state/stage5dm-evidence-source-atlas-readiness.yaml")

    assert motifs["visual_motif_index_created"] is True
    assert motifs["image_classification_performed_now"] is False
    assert motifs["ocr_performed"] is False
    assert doublet["metric_definition_created"] is True
    assert doublet["statistics_computed_now"] is False
    assert atlas["design_contract_created"] is True
    assert atlas["atlas_tool_built_now"] is False
    assert atlas["web_app_built_now"] is False


def test_stage5dm_codex_output_policy() -> None:
    ensure_stage5dm_built()
    summary = load_yaml("data/project-state/stage5dm-summary.yaml")

    assert summary["canonical_codex_handoff_root"] == "codex-output"
    assert summary["stage5dm_builds_web_app_now"] is False
