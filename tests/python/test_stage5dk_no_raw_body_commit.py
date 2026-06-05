from __future__ import annotations

from libreprimus.token_block import stage5dk
from test_stage5dk_common import ensure_stage5dk_built, git_check_ignore, load_yaml, write_temp_yaml


def test_stage5dk_records_do_not_commit_raw_fandom_bodies() -> None:
    ensure_stage5dk_built()

    for path in stage5dk.DATA_PATHS.values():
        record = load_yaml(path)
        assert record.get("raw_body_committed") is False
        assert record.get("raw_fandom_body_committed") is False
        assert record.get("raw_webpage_bodies_committed") is False
        assert record.get("source_bodies_committed") is False
        assert record.get("generated_outputs_committed") is False


def test_stage5dk_validator_rejects_raw_body_flag(monkeypatch: object, tmp_path) -> None:
    ensure_stage5dk_built()
    record = load_yaml("data/source-harvester/stage5dk-fandom-source-lock-register.yaml")
    record["sources"][0]["raw_body_committed"] = True
    path = write_temp_yaml(tmp_path / "register.yaml", record)
    monkeypatch.setitem(stage5dk.DATA_PATHS, "fandom_source_lock_register", path)

    result = stage5dk.validate_stage5dk_fandom_source_locks()
    assert result.validation_error_count > 0
    assert any("raw_body_committed_true" in error for error in result.errors)


def test_stage5dk_generated_outputs_are_ignored() -> None:
    assert git_check_ignore("experiments/results/token-block/stage5dk/summary.json")
    assert git_check_ignore("experiments/results/token-block/stage5dk/warnings.jsonl")
