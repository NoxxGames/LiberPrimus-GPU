from libreprimus.token_block.stage5cu import (
    FUTURE_REAL_RECORD_CLASSES,
    NEGATIVE_FIXTURE_IDS,
    OPTION_SELECTION_MISUSE_TRANSITIONS,
)

from test_stage5cw_common import ensure_stage5cw_built, load_yaml


def test_stage5cw_preserves_stage5cu_negative_fixture_layer() -> None:
    ensure_stage5cw_built()
    summary = load_yaml("data/project-state/stage5cw-summary.yaml")

    assert summary["stage5cu_negative_fixture_pack_preserved"] is True
    assert summary["stage5cu_negative_fixture_count_preserved"] == len(NEGATIVE_FIXTURE_IDS)
    assert summary["stage5cu_real_decision_negative_fixture_pack_preserved"] is True
    assert summary["stage5cu_real_decision_negative_fixture_count_preserved"] == len(
        FUTURE_REAL_RECORD_CLASSES
    )
    assert summary["stage5cu_option_selection_misuse_matrix_preserved"] is True
    assert summary["stage5cu_option_selection_misuse_case_count_preserved"] == len(
        OPTION_SELECTION_MISUSE_TRANSITIONS
    )
    assert summary["stage5cu_fixture_isolation_policy_preserved"] is True
    assert summary["stage5cu_real_record_blocker_preserved"] is True
