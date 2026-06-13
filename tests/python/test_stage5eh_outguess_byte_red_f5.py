from __future__ import annotations

from test_stage5eh_common import stage5eh_data


def test_outguess03_operator_transcription_facts_preserved() -> None:
    record = stage5eh_data("outguess_pgp_xor_records")
    transcription = record["outguess03_jpeg_transcription"]

    assert transcription["outguess03_jpeg_transcription_source"] == "operator_supplied_human_transcription"
    assert transcription["outguess03_ocr_performed_now"] is False
    assert transcription["outguess03_image_forensics_performed_now"] is False
    assert transcription["outguess03_literal_digit_markers"] == [5, 3]
    assert transcription["outguess03_rune_token_count"] == 18
    assert transcription["outguess03_visible_item_count_including_digits"] == 20
    assert transcription["outguess03_segment_lengths_between_literal_digits"] == [8, 5, 5]
    assert transcription["outguess03_rune_zero_based_index_sum"] == 261
    assert transcription["outguess03_index_sum_factorization"] == "9 * 29"
    assert transcription["outguess03_index_sum_mod29"] == 0
    assert transcription["outguess03_segment_index_sums"] == [103, 72, 86]
    assert transcription["outguess03_segment_prime_sums"] == [387, 273, 330]
    assert transcription["outguess03_used_to_decode_now"] is False


def test_byte_string_crosslinks_do_not_generate_bytes() -> None:
    record = stage5eh_data("byte_string_context_records")

    assert record["byte_string_count"] == 4
    assert record["exact_512_hex_string_count"] == 4
    assert record["decoded_byte_length_each"] == 256
    assert record["stage5bk_source_lock_record"] == "data/historical-route/stage5bk-iddqd-v2-byte-strings-source-lock.yaml"
    assert record["byte_strings_real_byte_stream_generated_now"] is False
    assert record["byte_strings_used_as_execution_seed_now"] is False


def test_page54_55_red_numbers_are_separate_from_postlude() -> None:
    record = stage5eh_data("red_number_control_records")
    candidate = record["page54_55_red_numbered_line_blocks_candidate_v0"]

    assert candidate["page54_red_numbers_observed_by_assistant_or_operator"] == [2, 3, 4]
    assert candidate["page55_red_numbers_observed_by_operator"] == [5]
    assert candidate["not_same_as_a_postlude_red_heading_theory"] is True
    assert candidate["route_control_not_accepted_now"] is True


def test_page13_detector_context_is_not_execution() -> None:
    record = stage5eh_data("stegdetect_f5_signal_records")
    candidate = record["page13_stegdetect_f5_beta_signal_candidate_v0"]

    assert candidate["page13_stegdetect_result_source"] == "operator_supplied_external_run"
    assert candidate["page13_stegdetect_raw_log_fragment"] == "f5[1.368187]"
    assert candidate["page13_stegdetect_detail_beta"] == 1.368
    assert candidate["stegdetect_execution_performed_now"] is False
    assert candidate["f5_extraction_performed_now"] is False
    assert candidate["known_outguess_payload_confound"] is True
    assert candidate["no_solve_claim"] is True
