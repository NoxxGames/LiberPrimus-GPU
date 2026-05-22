"""Build the Stage 5T solved-family inventory."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any

from libreprimus.cuda_solved_family_readiness.export import write_record_set, write_report
from libreprimus.cuda_solved_family_readiness.models import (
    COMMON_FLAGS,
    FIXTURE_ROOT,
    INVENTORY_PATH,
    INVENTORY_REPORT_JSON,
    OUTPUT_DIR,
)


def build_solved_family_inventory(
    *,
    fixture_root: Path = FIXTURE_ROOT,
    inventory_out: Path = INVENTORY_PATH,
    out_dir: Path = OUTPUT_DIR,
) -> list[dict[str, Any]]:
    """Inventory committed solved families without reading raw corpus inputs."""

    counts = _fixture_counts(fixture_root)
    records = [
        _record(
            "direct_translation",
            "direct_translation_solved_fixture",
            counts["direct_translation"],
            "cuda_parity_ready_existing_kernel",
            "Direct fixtures have verified shift-score token-buffer parity, but direct translation itself is not a CUDA transform.",
            cpu_reference=True,
            native_reference=True,
            current_kernel_verified=False,
            original_verified=False,
        ),
        _record(
            "reverse_gematria",
            "atbash_reverse_solved_fixture",
            counts["reverse_gematria"],
            "needs_cuda_kernel_contract",
            "Reverse Gematria has CPU solved fixtures and one consumed shift-score token buffer, but original semantics need a separate contract.",
            cpu_reference=True,
            native_reference=True,
        ),
        _record(
            "rotated_reverse_gematria",
            "atbash_rotated_reverse_solved_fixture",
            counts["rotated_reverse_gematria"],
            "blocked_original_transform_contract",
            "Rotated reverse Gematria is solved-fixture-safe but requires explicit rotation ABI and a separate original-family contract.",
            cpu_reference=True,
            native_reference=True,
        ),
        _record(
            "vigenere_explicit_key",
            "vigenere_explicit_key_solved_fixture",
            counts["vigenere_explicit_key"],
            "needs_batch_abi",
            "Explicit-key Vigenere has solved fixtures and CPU references, but needs key-schedule ABI before CUDA contracts.",
            cpu_reference=True,
            native_reference=True,
        ),
        _record(
            "prime_minus_one_stream",
            "prime_minus_one_solved_fixture",
            counts["prime_minus_one_stream"],
            "needs_batch_abi",
            "Prime-minus-one has a solved fixture and CPU reference, but needs stream-schedule ABI before CUDA contracts.",
            cpu_reference=True,
            native_reference=True,
        ),
        _record(
            "gematria_shift_score_only",
            "solved_fixture_shift_score_token_buffer",
            8,
            "cuda_parity_verified_existing_kernel",
            "Stage 5M and Stage 5R verified the existing Gematria shift-score kernel over eight solved-fixture-safe token buffers.",
            cpu_reference=True,
            native_reference=True,
            cuda_kernel=True,
            current_kernel_verified=True,
        ),
        _record(
            "synthetic_shift_score",
            "stage5f_uppercase_latin_synthetic",
            1,
            "cuda_parity_verified_existing_kernel",
            "Stage 5F verified the earlier uppercase-Latin synthetic shift_score kernel; it is separate from Gematria mod-29.",
            cpu_reference=True,
            native_reference=True,
            cuda_kernel=True,
            current_kernel_verified=True,
        ),
        _record(
            "synthetic_gematria_mod29",
            "stage5j_numeric_gematria_synthetic",
            1,
            "cuda_parity_verified_existing_kernel",
            "Stage 5J verified the synthetic numeric Gematria mod-29 kernel before solved-fixture parity was attempted.",
            cpu_reference=True,
            native_reference=True,
            cuda_kernel=True,
            current_kernel_verified=True,
        ),
    ]
    write_record_set(inventory_out, records)
    write_report(out_dir, INVENTORY_REPORT_JSON, {"records": records})
    return records


def _fixture_counts(fixture_root: Path) -> Counter[str]:
    counts: Counter[str] = Counter()
    for path in fixture_root.rglob("*.fixture.json"):
        payload = json.loads(path.read_text(encoding="utf-8"))
        family = str(payload.get("method_family", "unknown"))
        counts[family] += 1
    return counts


def _record(
    family_id: str,
    fixture_class: str,
    fixture_count: int,
    readiness_status: str,
    rationale: str,
    *,
    cpu_reference: bool,
    native_reference: bool,
    cuda_kernel: bool = False,
    current_kernel_verified: bool = False,
    original_verified: bool = False,
) -> dict[str, Any]:
    return {
        "record_type": "solved_family_cuda_inventory_record",
        "solved_family_inventory_id": f"stage5t-inventory-{family_id}",
        "solved_family_id": family_id,
        "fixture_class": fixture_class,
        "fixture_count": fixture_count,
        "cpu_reference_ready": cpu_reference,
        "native_reference_ready": native_reference,
        "cuda_kernel_available": cuda_kernel,
        "verified_current_kernel_parity": current_kernel_verified,
        "original_transform_semantics_cuda_verified": original_verified,
        "readiness_status": readiness_status,
        "rationale": rationale,
        **COMMON_FLAGS,
    }
