from libreprimus.token_block.preflight_runner.stage5bd import make_run_plan_id


def test_stage5bd_run_plan_id_is_deterministic() -> None:
    left = make_run_plan_id({"b": 2, "a": 1})
    right = make_run_plan_id({"a": 1, "b": 2})

    assert left == right
    assert left.startswith("stage5bd-")
    assert len(left) == len("stage5bd-") + 16
