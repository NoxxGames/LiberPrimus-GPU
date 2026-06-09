from __future__ import annotations

from libreprimus.token_block.stage5dw import (
    validate_stage5dw_active_lineage_preservation,
    validate_stage5dw_governance_scope,
    validate_stage5dw_stage5bd_preservation,
    validate_stage5dw_stage5dg_preservation,
    validate_stage5dw_stage5dv_preservation,
)
from test_stage5dw_common import ensure_stage5dw_built


def test_stage5dw_preserves_prior_governance_layers() -> None:
    ensure_stage5dw_built()
    validators = [
        validate_stage5dw_stage5dv_preservation,
        validate_stage5dw_stage5dg_preservation,
        validate_stage5dw_stage5bd_preservation,
        validate_stage5dw_active_lineage_preservation,
        validate_stage5dw_governance_scope,
    ]

    for validator in validators:
        assert validator().validation_error_count == 0
