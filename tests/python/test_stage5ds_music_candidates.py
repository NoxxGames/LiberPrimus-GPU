from __future__ import annotations

from test_stage5ds_common import ensure_stage5ds_built, load_yaml


def test_stage5ds_instar_product_candidate() -> None:
    ensure_stage5ds_built()
    record = load_yaml(
        "data/historical-route/stage5ds-instar-parable-id3-gp-product-candidate-v1.yaml"
    )
    assert record["prime_product"] == 1595277641
    assert [row["value"] for row in record["prime_factors"]] == [1031, 1229, 1259]
    assert all(row["is_prime"] for row in record["prime_factors"])
    assert record["execution_authorized_now"] is False


def test_stage5ds_guitar_prime_strings_and_quarantine() -> None:
    ensure_stage5ds_built()
    guitar = load_yaml(
        "data/historical-route/stage5ds-interconnectedness-guitar-tab-prime-fret-strings-v1.yaml"
    )
    assert guitar["nonprime_exception"]["value"] == 32023
    assert guitar["nonprime_exception"]["factorization"] == [31, 1033]

    quarantine = load_yaml(
        "data/historical-route/stage5ds-music-direct-pitch-substitution-quarantine-v0.yaml"
    )
    assert quarantine["candidate_status"] == "quarantined_direct_substitution"
    assert quarantine["direct_music_substitution_executed"] is False
