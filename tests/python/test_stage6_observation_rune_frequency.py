from __future__ import annotations

from libreprimus.token_block import stage6
from test_stage6_common import stage6_data


def test_stage6_observation_archive_is_not_canonical_truth() -> None:
    payload = stage6_data("observation_rune_frequency_source_lock_register")
    assert payload["source_status"] == "community_observation_archive"
    assert payload["evidence_status"] == "operator_assistant_observed_hypothesis"
    assert payload["future_probe_required"] is True
    assert payload["usable_for_decision_now"] is False
    assert payload["bigrams_py_executed_now"] is False
    assert payload["community_code_executed_now"] is False
    assert payload["canonical_bigram_matrix_recomputed_now"] is False
    assert payload["canonical_transcript_reproduction_performed_now"] is False
    assert payload["image_ocr_performed_now"] is False
    assert payload["image_forensics_performed_now"] is False
    assert payload["semantic_image_interpretation_performed_now"] is False


def test_stage6_observation_adjacent_doublet_surface_is_exact_archive_candidate() -> None:
    payload = stage6_data("observation_rune_frequency_adjacent_doublet_signature")
    assert payload["observed_diagonal_doublet_vector"] == stage6.OBSERVED_DIAGONAL_VECTOR
    assert payload["observed_compact_string"] == "42442156242421632042324217223"
    assert payload["observed_diagonal_total"] == 86
    assert payload["repeated_delimiter_candidate"] == "421"
    assert payload["delimiter_rune_triples"] == ["ORC", "J/EO/P", "OE/D/A"]
    assert payload["pre_delimiter_segment_lengths"] == [3, 5, 8]
    assert payload["observed_segment_headers"] == [4, 5, 6, 7]
    assert payload["primary_status"] == "future_reproduction_required"


def test_stage6_attachment_filenames_are_context_anchors_not_subject_claims() -> None:
    payload = stage6_data("observation_rune_frequency_attachment_context_map")
    for attachment in payload["attachments"]:
        assert attachment["filename_is_context_anchor"] is True
        assert attachment["filename_is_page_or_subject_claim"] is False
    cover = payload["attachments"][0]
    assert "not_automatically_lp_cover_image" in cover["risk_notes"]
    six_seven = payload["attachments"][1]
    assert "not_automatically_pages_6_and_7" in six_seven["risk_notes"]
