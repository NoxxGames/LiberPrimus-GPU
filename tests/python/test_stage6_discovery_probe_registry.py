from __future__ import annotations

from libreprimus.token_block import stage6
from test_stage6_common import stage6_data


def test_stage6_registry_preserves_stage5eh_probe_ids() -> None:
    payload = stage6_data("discovery_probe_manifest_registry")
    ids = {entry["diagnostic_id"] for entry in payload["diagnostics"]}
    assert set(stage6.STAGE5EH_PROBE_IDS).issubset(ids)
    assert payload["stage5eh_probe_count_preserved"] == 23


def test_stage6_registry_includes_exact_observation_future_probe_ids() -> None:
    payload = stage6_data("discovery_probe_manifest_registry")
    ids = {entry["diagnostic_id"] for entry in payload["diagnostics"]}
    assert set(stage6.OBSERVATION_PROBE_IDS).issubset(ids)
    assert payload["observation_on_rune_frequency_probe_count"] == 11


def test_stage6_all_probe_registry_entries_are_future_only() -> None:
    payload = stage6_data("discovery_probe_manifest_registry")
    for entry in payload["diagnostics"]:
        assert entry["stage6_run_now"] is False
        assert entry["execution_enabled_now"] is False
        assert entry["finite_input_set_required"] is True
        assert entry["full_output_archive_required_when_run"] is True
        assert entry["not_solve_evidence"] is True
