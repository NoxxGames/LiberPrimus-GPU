"""Synthetic Stage 5D parity helpers for the Stage 5F CUDA kernel."""

from __future__ import annotations

from libreprimus.native_cpu.runner import python_reference_run

EXPECTED_NATIVE_HASH = "76a7d57c1da4d1ea39fc1d34f0e29ef4f732dab2f489b26d31758169ccd21a66"
FIXTURE_TEXT = "LIBER PRIMUS STAGE FIVE D"
SHIFTS = (0, 1, 3, 7, 13, 28)


def python_reference_hash() -> str:
    """Return the Stage 5D limited synthetic reference hash."""

    return str(python_reference_run(threads=1)["output_hash"])
