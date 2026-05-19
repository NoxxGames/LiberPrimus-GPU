"""Disabled future manifest records for Stage 4B."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


MANIFEST_SPECS: tuple[tuple[str, str, int, str, str], ...] = (
    (
        "exp_stage4b_gp_rune_verifier_batch002",
        "Verify new exact-span website-derived GP/rune claims.",
        20,
        "disabled_needs_source_lock",
        "Exact-span website-derived GP/rune claims only.",
    ),
    (
        "exp_stage4b_dot_ambiguity_audit_v1",
        "Measure ambiguity of dot/binary readings after annotation.",
        140,
        "disabled_needs_annotation",
        "Promoted dot motifs and ambiguity tables.",
    ),
    (
        "exp_stage4b_delimiter_handedness_v1",
        "Test delimiter handedness and reset-boundary hypotheses after observation intake.",
        16,
        "disabled_needs_annotation",
        "Mirrored three-dot delimiter observations.",
    ),
    (
        "exp_stage4b_onion7_raw_routes_v1",
        "No-fudge raw number-square route audit.",
        96,
        "disabled_needs_source_lock",
        "Raw Interconnectedness and number-square source locks.",
    ),
    (
        "exp_stage4b_cookie_pack_v2",
        "Exact source-backed cookie string candidates.",
        384,
        "disabled_needs_source_lock",
        "Public-source-backed cookie/hash candidate strings only.",
    ),
    (
        "exp_stage4b_cuneiform_reading_pack_v1",
        "Tiny cuneiform seed test after annotation.",
        32,
        "disabled_needs_annotation",
        "Cuneiform tuple readings after coordinate review.",
    ),
    (
        "exp_stage4b_visual_negative_controls_v1",
        "Pareidolia and ambiguity controls for visual claims.",
        60,
        "disabled_pending_review",
        "Braille, constellation, binary, and visual-overfit negative controls.",
    ),
)


def build_disabled_manifest(
    manifest_id: str, purpose: str, cap: int, status: str, source_basis: str
) -> dict[str, Any]:
    """Create one disabled Stage 4B manifest payload."""

    return {
        "record_type": "stage4b_disabled_experiment_manifest",
        "manifest_id": manifest_id,
        "title": manifest_id.replace("_", " "),
        "purpose": purpose,
        "source_basis": [
            source_basis,
            "Stage 4A Deep Research review",
            "Stage 4B source/observation records",
        ],
        "candidate_count_upper_bound": cap,
        "execution_enabled": False,
        "cuda_enabled": False,
        "no_solve_claim": True,
        "canonical_corpus_active": False,
        "page_boundaries_final": False,
        "generated_outputs_committed": False,
        "status": status,
        "notes": "Queued by Stage 4B only. Do not execute until a later explicit stage enables and validates an executor.",
    }


def build_disabled_manifests() -> list[dict[str, Any]]:
    return [build_disabled_manifest(*spec) for spec in MANIFEST_SPECS]


def write_disabled_manifests(manifest_dir: Path) -> list[Path]:
    """Write disabled manifests and README."""

    manifest_dir.mkdir(parents=True, exist_ok=True)
    (manifest_dir / "README.md").write_text(
        "# Stage 4B Disabled Manifests\n\n"
        "These records queue future bounded work only. `execution_enabled` is false for every manifest.\n",
        encoding="utf-8",
    )
    paths: list[Path] = []
    for payload in build_disabled_manifests():
        path = manifest_dir / f"{payload['manifest_id']}.yaml"
        path.write_text(
            yaml.safe_dump(payload, sort_keys=False, allow_unicode=False), encoding="utf-8"
        )
        paths.append(path)
    return paths
