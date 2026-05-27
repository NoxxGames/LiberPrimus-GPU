from test_stage5bf_local_archive_location import assert_stage5bf_metadata_only, load_yaml


def test_stage5bf_network_byte_channel_artifacts_are_historical_context_only() -> None:
    payload = load_yaml("data/historical-route/stage5bf-network-byte-channel-artifacts.yaml")
    families = {family for artifact in payload["artifacts"] for family in artifact["artifact_families"]}

    assert payload["candidate_count"] == 12
    assert "telnet_instruction" in families
    assert "tcp_server_script" in families
    assert_stage5bf_metadata_only(payload)
