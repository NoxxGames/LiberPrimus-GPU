"""Build disabled Stage 3R post-Discord experiment manifests."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.discord_lead_promotion.export import write_yaml
from libreprimus.paths import repo_root

MANIFEST_FILENAMES = {
    "EXP-3R-001": "EXP-3R-001-cookie-sha256-signed-variants-a.yaml",
    "EXP-3R-003": "EXP-3R-003-onion7-raw-prime-order-seed-pack-a.yaml",
    "EXP-3R-004": "EXP-3R-004-gp-rune-claim-verifier-a.yaml",
}


def build_post_discord_manifests(
    *,
    out_dir: Path,
    audit_summary: Path | None = None,
    allow_warnings: bool = False,
) -> dict[str, Any]:
    """Write the first three disabled post-Discord manifests."""
    del audit_summary, allow_warnings
    resolved_out = _resolve(out_dir)
    resolved_out.mkdir(parents=True, exist_ok=True)
    manifests = [_cookie_manifest(), _onion7_manifest(), _gp_rune_manifest()]
    for manifest in manifests:
        filename = MANIFEST_FILENAMES[str(manifest["experiment_id"])]
        write_yaml(resolved_out / filename, manifest)
    summary = {
        "record_type": "post_discord_manifest_build_summary",
        "manifest_count": len(manifests),
        "experiments": {
            str(manifest["experiment_id"]): {
                "candidate_count_cap": manifest["candidate_count_cap"],
                "execution_enabled": manifest["execution_enabled"],
                "cuda_enabled": manifest["cuda_enabled"],
                "no_solve_claim": manifest["no_solve_claim"],
            }
            for manifest in manifests
        },
        "output_dir": _display(resolved_out),
    }
    return summary


def post_discord_manifests() -> list[dict[str, Any]]:
    """Return manifests without writing them."""
    return [_cookie_manifest(), _onion7_manifest(), _gp_rune_manifest()]


def _base_manifest(experiment_id: str, description: str, hypothesis: str, cap: int) -> dict[str, Any]:
    return {
        "record_type": "post_discord_experiment_manifest",
        "experiment_id": experiment_id,
        "description": description,
        "hypothesis": hypothesis,
        "candidate_count_cap": cap,
        "execution_enabled": False,
        "cpu_only": True,
        "cuda_enabled": False,
        "cloud_execution": False,
        "paid_services": False,
        "generated_outputs_committed": False,
        "no_solve_claim": True,
        "canonical_corpus_active": False,
        "page_boundaries_final": False,
        "notes": "Stage 3R queues this manifest only; execution is explicitly disabled.",
    }


def _cookie_manifest() -> dict[str, Any]:
    manifest = _base_manifest(
        "EXP-3R-001",
        "cookie_sha256_signed_variants_a",
        "Exact SHA-256 preimage test over historically authenticated strings and artefact names.",
        576,
    )
    base_strings = [
        "ForEveryThingThatLivesIsHoly",
        "For Every Thing That Lives Is Holy",
        "THEPATHLIESEMPTY",
        "LiberPrimusIsTheWay",
        "Liber Primus is the way",
        "7A35090F",
        "1033.jpg",
        "761.mp3",
        "3301",
        "1033",
        "761",
        "167",
        "p7amjopgric7dfdi.onion",
    ]
    byte_variants = [
        "raw",
        "lower",
        "upper",
        "trailing_lf",
        "trailing_crlf",
        "leading_space",
        "trailing_space",
        "wrapped_space",
        "compact_no_spaces",
        "compact_upper",
        "compact_lower",
        "quoted",
    ]
    manifest.update(
        {
            "source_basis": [
                "cookie-2013-167-v0",
                "cookie-2013-761-v0",
                "stage3r-promoted-source-records",
            ],
            "required_inputs": [
                {"input_id": "cookie-2013-167-v0", "kind": "archived_cookie_hash"},
                {"input_id": "cookie-2013-761-v0", "kind": "archived_cookie_hash"},
                {"input_id": "stage3r-public-source-strings", "kind": "authenticated_public_string_review"},
            ],
            "candidate_generation": {
                "algorithm": "sha256",
                "base_strings": base_strings,
                "byte_variants": byte_variants,
                "candidate_count_estimate": len(base_strings) * len(byte_variants),
                "fuzzy_matching": False,
                "gpu_hashcat": False,
            },
            "controls": [
                "Exact hex digest comparison only.",
                "No fuzzy or near-match interpretation.",
                "No external dictionary or brute-force expansion.",
            ],
            "stop_conditions": [
                "candidate_count_exceeds_576",
                "input_string_lacks_public_source",
                "any_non_sha256_algorithm_requested",
            ],
        }
    )
    return manifest


def _onion7_manifest() -> dict[str, Any]:
    manifest = _base_manifest(
        "EXP-3R-003",
        "onion7_raw_prime_order_seed_pack_a",
        "Use explicit Onion 7 table values and documented derived tables as bounded numeric seed streams.",
        144,
    )
    value_spaces = ["raw_table", "prime_delta_table", "prime_order_table"]
    routes = [
        "row_major",
        "column_major",
        "reverse_row_major",
        "reverse_column_major",
        "clockwise_spiral",
        "counterclockwise_spiral",
    ]
    directions = ["forward", "reverse"]
    reset_modes = ["none", "line"]
    manifest.update(
        {
            "source_basis": [
                "stage3r-observation-onion7-page15-raw-table",
                "stage3r-source-onion7-page15",
            ],
            "required_inputs": [
                {"input_id": "onion7_raw_table", "kind": "public_source_table_review_required"},
                {"input_id": "onion7_prime_delta_table", "kind": "derived_table_review_required"},
                {"input_id": "onion7_prime_order_table", "kind": "derived_table_review_required"},
            ],
            "candidate_generation": {
                "value_spaces": value_spaces,
                "routes": routes,
                "directions": directions,
                "reset_modes": reset_modes,
                "candidate_count_estimate": len(value_spaces) * len(routes) * len(directions) * len(reset_modes),
            },
            "controls": [
                "Only exact public Onion 7 table values may be used.",
                "No page-boundary finalization.",
                "No image-derived seed promotion.",
            ],
            "stop_conditions": [
                "candidate_count_exceeds_144",
                "raw_or_derived_table_missing_public_review_source",
                "execution_requested_in_stage3r",
            ],
        }
    )
    return manifest


def _gp_rune_manifest() -> dict[str, Any]:
    manifest = _base_manifest(
        "EXP-3R-004",
        "gp_rune_claim_verifier_a",
        "Verify exact GP-sum and rune-count claims by recomputation on locked transcript inputs.",
        64,
    )
    manifest.update(
        {
            "source_basis": [
                "stage3r-promoted-observation-records",
                "stage3o-promoted-numeric-observation-candidates",
            ],
            "required_inputs": [
                {"input_id": "promoted_numeric_claims", "kind": "exact_claim_review_required"},
                {"input_id": "locked_transcript_candidates", "kind": "future_locked_transcript_input"},
                {"input_id": "gematria_profile_v0", "kind": "committed_profile"},
            ],
            "candidate_generation": {
                "claim_cap": 64,
                "claim_types": ["gp_sum", "rune_count"],
                "classification_results": [
                    "verified",
                    "unverified",
                    "boundary_sensitive",
                    "missing_source_span",
                ],
            },
            "controls": [
                "No vague spans.",
                "No Discord-only claim promoted as fact.",
                "Boundary-sensitive claims must remain non-canonical.",
            ],
            "stop_conditions": [
                "claim_count_exceeds_64",
                "claim_missing_exact_span",
                "execution_requested_in_stage3r",
            ],
        }
    )
    return manifest


def _resolve(path: Path) -> Path:
    return path if path.is_absolute() else repo_root() / path


def _display(path: Path) -> str:
    try:
        return path.resolve().relative_to(repo_root()).as_posix()
    except ValueError:
        return path.as_posix()
