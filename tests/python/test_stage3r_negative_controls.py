from __future__ import annotations

from libreprimus.discord_lead_promotion.negative_controls import build_negative_control_records


def test_negative_controls_include_required_false_positive_classes() -> None:
    controls = build_negative_control_records()
    classes = {record["false_positive_class"] for record in controls}
    assert "2016_qr_background_blocks" in classes
    assert "2016_dendrite_interpretation" in classes
    assert "2014_imgur_filename_clue" in classes
    assert "2014_brightness_only_hidden_silhouette" in classes
    assert "broad_cookie_bruteforce_gpu_hash_attack" in classes
    for record in controls:
        assert record["raw_message_committed"] is False
        assert record["username_committed"] is False
        assert record["private_url_committed"] is False
        assert record["solve_claim"] is False
