"""Read-only source loaders for Stage 5Z prime-minus-one CUDA contract preparation."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.prime_minus_one_cuda_contract.export import read_records, read_yaml
from libreprimus.prime_minus_one_cuda_contract.models import (
    STAGE5U_ABI_PATH,
    STAGE5W_CONTRACT_PATH,
    STAGE5W_MAPPING_PATH,
    STAGE5X_PARITY_PATH,
    STAGE5Y_GATE_PATH,
    STAGE5Y_SCORED_PATH,
    STAGE5Y_SUMMARY_PATH,
)


def load_stage5z_sources(
    *,
    stage5y_summary: Path = STAGE5Y_SUMMARY_PATH,
    stage5y_gate: Path = STAGE5Y_GATE_PATH,
    stage5y_scored: Path = STAGE5Y_SCORED_PATH,
    stage5x_parity: Path = STAGE5X_PARITY_PATH,
    stage5w_mapping: Path = STAGE5W_MAPPING_PATH,
    stage5w_contract: Path = STAGE5W_CONTRACT_PATH,
    stage5u_abi: Path = STAGE5U_ABI_PATH,
) -> dict[str, Any]:
    """Load committed Stage 5U/5W/5X/5Y metadata without executing anything."""

    return {
        "stage5y_summary": read_yaml(stage5y_summary),
        "stage5y_gate": read_records(stage5y_gate),
        "stage5y_scored": read_records(stage5y_scored),
        "stage5x_parity": read_records(stage5x_parity),
        "stage5w_mapping": read_records(stage5w_mapping),
        "stage5w_contract": read_records(stage5w_contract),
        "stage5u_abi": read_yaml(stage5u_abi),
    }


__all__ = ["load_stage5z_sources"]
