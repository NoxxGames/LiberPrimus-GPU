from test_stage5bu_common import load_yaml


def test_stage5bu_erratum_records_wrong_and_correct_stage5aw_paths() -> None:
    payload = load_yaml("data/token-block/stage5bu-stage5bs-lineage-path-erratum.yaml")

    assert payload["erratum_status"] == "corrected_in_place_with_stage5bu_erratum"
    assert payload["incorrect_path"] == "data/token-block/stage5aw-repaired-branch-manifest.yaml"
    assert payload["correct_path"] == "data/token-block/stage5aw-repaired-token-variant-branch-manifest.yaml"
    assert payload["incorrect_path_resolves"] is False
    assert payload["correct_path_resolves"] is True
    assert payload["stage5bs_record_repaired"] is True
    assert payload["stage5bs_validator_hardened"] is True
