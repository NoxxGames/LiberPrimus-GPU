"""Stage 4O CPU batch adapter coverage expansion."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from libreprimus.cpu_batch.models import SUPPORTED_LOCAL_TRANSFORMS, SUPPORTED_REGISTRY_TRANSFORMS
from libreprimus.history.source_records import resolve_repo_path
from libreprimus.transforms.registry import load_registry

BOUNDED_FAMILY_RECORDS = (
    {
        "transform_id": "caesar_shift",
        "canonical_transform_id": "caesar_shift",
        "transform_family": "caesar_mod29",
        "adapter_status": "supported",
        "reason": "Local Stage 4H adapter covers bounded Caesar mod-29 shifts.",
    },
    {
        "transform_id": "affine_mod29",
        "canonical_transform_id": "affine_mod29",
        "transform_family": "affine_mod29",
        "adapter_status": "supported",
        "reason": "Local Stage 4H adapter covers bounded Affine mod-29 transforms.",
    },
    {
        "transform_id": "p56_prime_minus_one",
        "canonical_transform_id": "prime_minus_one_stream",
        "transform_family": "p56_prime_minus_one",
        "adapter_status": "supported",
        "reason": "Solved-fixture p56 prime-minus-one semantics are covered by prime_minus_one_stream.",
    },
    {
        "transform_id": "reset_advance_variants",
        "canonical_transform_id": None,
        "transform_family": "reset_advance",
        "adapter_status": "deferred",
        "reason": "Reset/advance state-machine variants exist in bounded execution but need a stable CPU batch manifest contract before adapter support.",
    },
    {
        "transform_id": "historical_motif_vigenere",
        "canonical_transform_id": None,
        "transform_family": "historical_motif_vigenere",
        "adapter_status": "deferred",
        "reason": "Historical motif Vigenere uses explicit-list bounded runners; adapter support is deferred until key-pack manifests expose stable batch parameters.",
    },
    {
        "transform_id": "cookie_hash_family",
        "canonical_transform_id": None,
        "transform_family": "cookie_hash",
        "adapter_status": "unsupported_by_design",
        "reason": "Cookie/hash comparisons are exact digest checks, not text transform adapters.",
    },
    {
        "transform_id": "stego_audio_family",
        "canonical_transform_id": None,
        "transform_family": "stego_audio",
        "adapter_status": "unsupported_by_design",
        "reason": "Stego/audio fixtures are toolchain readiness records, not CPU text transform adapters.",
    },
    {
        "transform_id": "image_compression_bigram_family",
        "canonical_transform_id": None,
        "transform_family": "image_compression_bigram",
        "adapter_status": "unsupported_by_design",
        "reason": "Image, compression, and bigram observations are review/preflight records, not CPU text transform adapters.",
    },
)


def build_adapter_coverage(*, registry_path: Path, out_dir: Path) -> dict[str, Any]:
    """Write expanded Stage 4O adapter coverage records."""

    registry = load_registry(registry_path)
    registry_records = [
        {
            "transform_id": definition.transform_id,
            "canonical_transform_id": definition.alias_of or definition.transform_id,
            "transform_family": definition.method_family,
            "adapter_status": _registry_status(definition.transform_id),
            "supports_cpu_reference": definition.supports_cpu_reference,
            "supports_gpu": False,
            "reason": "Registry transform has a stable CPU batch adapter."
            if definition.transform_id in SUPPORTED_REGISTRY_TRANSFORMS
            else "Registry transform is not covered by the CPU batch adapter set.",
        }
        for definition in sorted(registry.transforms, key=lambda item: item.transform_id)
    ]
    bounded_records = [
        {
            **record,
            "supports_cpu_reference": record["transform_id"] in SUPPORTED_LOCAL_TRANSFORMS
            or record["transform_id"] == "p56_prime_minus_one",
            "supports_gpu": False,
        }
        for record in BOUNDED_FAMILY_RECORDS
    ]
    records = registry_records + bounded_records
    supported = sum(1 for record in records if record["adapter_status"] == "supported")
    missing = sum(1 for record in records if record["adapter_status"] == "missing")
    deferred = sum(1 for record in records if record["adapter_status"] == "deferred")
    unsupported = sum(1 for record in records if record["adapter_status"] == "unsupported_by_design")
    payload = {
        "record_type": "cpu_batch_adapter_coverage",
        "registry_id": registry.registry_id,
        "registry_sha256": registry.sha256,
        "transform_count": len(records),
        "supported_adapter_count": supported,
        "missing_adapter_count": missing,
        "deferred_adapter_count": deferred,
        "unsupported_by_design_count": unsupported,
        "missing_or_deferred_adapter_count": missing + deferred,
        "records": records,
        "cpu_only": True,
        "cuda_used": False,
        "cuda_required": False,
        "no_solve_claim": True,
        "canonical_corpus_active": False,
        "page_boundaries_final": False,
        "generated_outputs_committed": False,
    }
    resolved_out = resolve_repo_path(out_dir)
    resolved_out.mkdir(parents=True, exist_ok=True)
    (resolved_out / "adapter_coverage.json").write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return payload


def _registry_status(transform_id: str) -> str:
    if transform_id in SUPPORTED_REGISTRY_TRANSFORMS:
        return "supported"
    return "missing"
