from __future__ import annotations

from libreprimus.bounded_execution.models import BoundedCandidateRecord
from libreprimus.bounded_execution.negative_controls import generate_family_negative_controls


def _record(index: int) -> BoundedCandidateRecord:
    return BoundedCandidateRecord(
        record_type="bounded_candidate_record",
        run_id="stage3h-test-run",
        queue_item_id="stage3h_reset_advance_ablation_v1",
        transform_family="reset_advance_ablation",
        transform_id="vigenere:DIVINITY",
        transform_parameters={},
        candidate_index=index,
        input_slice_id="synthetic",
        output_normalized_text="THE PATH IS SHADOW AND LIGHT",
        output_preview="THE PATH IS SHADOW AND LIGHT",
        output_sha256="0" * 64,
        score_summary={"total_score": 1.0},
        ranking_features={},
        search_performed=True,
        scoring_used=True,
        cuda_used=False,
        canonical_corpus_active=False,
        page_boundaries_final=False,
        solve_claim=False,
        trusted_as_canonical=False,
        base_transform_id="vigenere:DIVINITY",
        base_transform_family="vigenere",
        reset_mode="none",
        advance_mode="runes_only",
    )


def test_family_negative_controls_are_deterministic() -> None:
    records = [_record(index) for index in range(3)]

    first = generate_family_negative_controls(records, thresholds={}, representative_transform_subset_size=3, seed=3301)
    second = generate_family_negative_controls(records, thresholds={}, representative_transform_subset_size=3, seed=3301)

    assert first == second
    assert len(first) == 12
    assert {record["control_kind"] for record in first} == {
        "rune_shuffle_same_length",
        "rune_freq_preserving_shuffle",
        "separator_randomised_variant",
        "wrong_mapping_variant",
    }
    assert all(record["solve_claim"] is False for record in first)
    assert all(record["cuda_used"] is False for record in first)
