"""Invoke and mirror the Stage 5D native CPU backend."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any

from libreprimus.native_cpu.models import BACKEND_ID, FIXTURE_ID


_FNV_PRIME = 1099511628211
_MASK64 = (1 << 64) - 1
_SEEDS = (
    14695981039346656037,
    1099511628211,
    7809847782465536322,
    1609587929392839161,
)
_CANDIDATES = (
    ("native-shift-00", 0),
    ("native-shift-01", 1),
    ("native-shift-03", 3),
    ("native-shift-07", 7),
    ("native-shift-13", 13),
    ("native-shift-28", 28),
)
_FIXTURE_TEXT = "LIBER PRIMUS STAGE FIVE D"


def run_native_backend(executable: Path, *, threads: int) -> dict[str, Any]:
    """Run the native executable and return its JSON payload."""

    command = [str(executable), "--threads", str(max(1, threads))]
    if executable.suffix == ".py":
        command = [sys.executable, *command]
    completed = subprocess.run(
        command,
        check=True,
        capture_output=True,
        text=True,
    )
    payload = json.loads(completed.stdout)
    if not isinstance(payload, dict):
        raise ValueError("native backend output must be a JSON object")
    return payload


def python_reference_run(*, threads: int = 1) -> dict[str, Any]:
    """Return the limited synthetic Python semantic mirror for Stage 5D."""

    records: list[dict[str, Any]] = []
    for index, (candidate_id, shift) in enumerate(_CANDIDATES):
        output_text = _apply_shift(_FIXTURE_TEXT, shift)
        output_hash = stable_hash_hex(output_text)
        record = {
            "candidate_index": index,
            "candidate_id": candidate_id,
            "shift": shift,
            "output_text": output_text,
            "output_hash": output_hash,
        }
        material = f"{index}|{candidate_id}|{shift}|{output_text}|{output_hash}"
        record["record_hash"] = stable_hash_hex(material)
        records.append(record)
    output_hash = stable_hash_hex(f"{BACKEND_ID}|{FIXTURE_ID}|" + "".join(f"{record['record_hash']}|" for record in records))
    return {
        "backend_id": BACKEND_ID,
        "fixture_id": FIXTURE_ID,
        "thread_count": max(1, threads),
        "candidate_count": len(records),
        "result_count": len(records),
        "output_hash": output_hash,
        "record_hash": stable_hash_hex(f"{BACKEND_ID}|{FIXTURE_ID}|{output_hash}"),
        "deterministic_ordering": True,
        "native_cpu_only": True,
        "cuda_used": False,
        "gpu_benchmark_performed": False,
        "solve_claim": False,
        "records": records,
    }


def stable_hash_hex(value: str) -> str:
    """Mirror the C++ deterministic hash used for Stage 5D record comparison."""

    encoded = value.encode("utf-8")
    chunks: list[str] = []
    for seed in _SEEDS:
        hash_value = seed
        for byte in encoded:
            hash_value ^= byte
            hash_value = (hash_value * _FNV_PRIME) & _MASK64
        chunks.append(f"{hash_value:016x}")
    return "".join(chunks)


def _apply_shift(value: str, shift: int) -> str:
    parts: list[str] = []
    for char in value:
        if char.isalpha():
            parts.append(chr(ord("A") + ((ord(char.upper()) - ord("A") + shift) % 26)))
        else:
            parts.append(char)
    return "".join(parts)
