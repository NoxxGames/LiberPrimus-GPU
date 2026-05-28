from libreprimus.historical_route.stage5bk import locate_stage5bk_iddqd_v2

from test_stage5bk_common import load_yaml


def test_stage5bk_records_selected_typo_path() -> None:
    payload = load_yaml("data/historical-route/stage5bk-iddqd-v2-local-source-root.yaml")
    assert payload["source_root_found"] is True
    assert payload["selected_path"] == "third_party/CiadaSolversIddqd_v2"
    assert payload["codex_output_used"] is False


def test_stage5bk_missing_root_is_blocked_metadata(tmp_path) -> None:
    payload = locate_stage5bk_iddqd_v2(
        preferred_relative_path=tmp_path / "missing-a",
        fallback_relative_path=tmp_path / "missing-b",
        results_dir=tmp_path / "results",
        out=tmp_path / "source-root.yaml",
    )
    assert payload["source_root_found"] is False
    assert payload["source_root_status"] == "blocked_missing_local_root"
    assert payload["execution_allowed"] is False
