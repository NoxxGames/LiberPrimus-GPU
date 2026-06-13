from __future__ import annotations

from libreprimus.token_block import stage5eh
from test_stage5eh_common import stage5eh_data


def test_lag5_inventory_and_claims_are_locked() -> None:
    inventory = stage5eh_data("lag5_file_inventory")
    lag5 = stage5eh_data("lag5_candidate_records")

    assert inventory["expected_file_count_present"] == 5
    assert inventory["event_list_observed_row_count"] == 57
    assert lag5["lag5_marker_definition"] == "M[i] = 1 iff C[i] = C[i+5]"
    assert lag5["lag_value"] == 5
    assert lag5["lag5_d_counts"] == {"d1": 29, "d2": 15, "d3": 14, "d4": 28, "d5": 19, "d6": 15}
    assert lag5["lag5_m_sum_claimed_or_reproduced"] == 479
    assert lag5["unsolved_corpus_rune_count_claimed_or_reproduced"] == 12956
    assert lag5["not_solve_evidence"] is True


def test_lp_outguessed_inventory_checks_xor_presence_before_records() -> None:
    record = stage5eh_data("lp_outguessed_source_lock_register")

    assert record["lp_outguessed_inventory_performed_before_records"] is True
    assert record["lp_outguessed_xor_txt_local_presence_checked"] is True
    assert record["expected_pgp_signed_output_present_count"] == 8
    assert record["pgp_verification_performed_now"] is False
    assert record["outguess_xor_reconstruction_performed_now"] is False


def test_absent_canonical_xor_txt_is_gap_not_reconstruction() -> None:
    record = stage5eh_data("lp_outguessed_source_lock_register")
    gaps = stage5eh_data("reviewability_gap_register")

    assert record["xor_txt_local_file_present"] is False
    assert record["lp_outguessed_xor_txt_reviewability_gap"] is True
    assert record["xor_txt_reconstructed_now"] is False
    assert record["xor_txt_synthesized_now"] is False
    assert gaps["canonical_xor_txt_reviewability_gap"] is True
    assert len(record["duplicate_or_old_xor_txt_candidate_paths"]) >= 1


def test_stage5eh_focused_inventory_validators_pass() -> None:
    assert stage5eh.validate_lag5_inventory().ok
    assert stage5eh.validate_lp_outguessed_inventory().ok
