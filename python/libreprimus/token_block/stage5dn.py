"""Stage 5DN DiskCipher v1 source-lock and bridge records.

This stage is metadata-only. It source-locks updated local DiskCipher material,
records candidate-level triangle/circumference crosslinks, and preserves the
closed governance gates. It does not execute HTML tools, OCR images, run disk
cipher branches, select targets, generate byte streams, score, use CUDA, or make
solve claims.
"""

from __future__ import annotations

import hashlib
import json
import mimetypes
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from libreprimus.token_block.models import read_yaml, sha256_file, write_json, write_jsonl, write_yaml
from libreprimus.token_block.preflight_runner.stage5bd import validate_stage5bd
from libreprimus.token_block.stage5ca import ACTIVE_LINEAGE_PATHS
from libreprimus.token_block.stage5cm import PARALLEL_WORKER_CAP
from libreprimus.token_block.stage5dm import DATA_PATHS as STAGE5DM_DATA_PATHS
from libreprimus.token_block.stage5dm import validate_stage5dm

STAGE_ID = "stage-5dn"
STAGE_TITLE = (
    "Stage 5DN - DiskCipher v1 source-lock and triangle/circumference bridge update, "
    "without execution"
)
PROMPT_TYPE = "codex_metadata_implementation"
SOURCE_PREVIOUS_STAGE_ID = "stage-5dm"
SOURCE_PREVIOUS_STAGE_COMMIT = "bd6fc6ad6cdf770cada3503c19995f389bf64b0a"
NEXT_STAGE_ID = "stage-5do"
NEXT_STAGE_TITLE = (
    "Stage 5DO - Source/evidence review and target-priority decision readiness review, "
    "without execution"
)

RESULTS_DIR = Path("experiments/results/token-block/stage5dn")
CODEX_COMPLETION_PATH = Path("codex-output/stage5dn-codex-completion.md")
DEPRECATED_CODEX_OUTPUT = Path("codex_output")

DISK_SOURCE_ROOT = Path("third_party/DiskCipherStuff")
DISK_EFFECTIVE_ROOT = Path("third_party/DiskCipherStuff/DiskCipherStuff")
TRANSLATION_CANDIDATES = [
    Path("third_party/NumberTriangleStuff/v2-number-triangles/liber-primus__translation/liber-primus__translation.txt"),
    Path("third_party/CiadaSolversIddqd_v2/liber-primus__translation/liber-primus__translation.txt"),
    Path("third_party/CicadaSolversIddqd/liber-primus__translation/liber-primus__translation.txt"),
]

SOURCE_LOCK_FAMILIES = [
    "disk_alberti_branch_cipher_candidate_v1",
    "disk_p39_row1_math_semantic_cluster_v1",
    "disk_56311_wynn_way_bridge_v1",
    "disk_rule4_mobius_trip_rotation_bridge_v0",
    "disk_doublet_suppression_candidate_v1",
    "disk_ruth_root_route_way_wordplay_candidate_v0",
    "disk_2015_eclipse_167_temporal_candidate_v0",
    "pdd_153_triangle_56311_wynn_way_route_v1",
    "solved_i_voice_of_circumference_precedent_v0",
    "circumference_single_i_spiral_anchor_crosslink_v0",
    "disk_probability_claim_quarantine_v1",
]

CLAIM_GROUPS = [
    (
        "p39_row_branching_claim",
        "p.39 first compressed row produces branching plaintext fragments under Alberti/disk rules and dot branching.",
    ),
    (
        "seq_56311_claim",
        "sequence 5-6-3-11 is used horizontally/vertically and underlies branch results.",
    ),
    (
        "wynn_claim",
        "WYNN is name of rune \\u16b9 and is structurally highlighted in branch results.",
    ),
    (
        "row1_math_semantic_cluster_claim",
        "row 1 produces EULER/LEONHARD/NAPIER/JOHN/TOTIENT/CIRCUMFERENCE/PRIME NUMBER/FISH/WYNN/PHI fragments.",
    ),
    (
        "doublet_suppression_claim",
        "disk/branching model may explain low doublet count or suppress repeated-rune structures.",
    ),
    (
        "ruth_route_way_wordplay_claim",
        "WAY/RUTH/root/route/road/path/direction semantic bridge is proposed.",
    ),
    (
        "rule4_mobius_trip_claim",
        "rotation/flip/loop sequence is compared to Moebius trip/step behavior.",
    ),
    (
        "eclipse_167_candidate_claim",
        "March 20 2015 eclipse/equinox/167-second timing candidate is proposed.",
    ),
    (
        "blake_urizen_circumference_claim",
        "disk/circumference metaphor is linked to Blake/Urizen/reason/self loop.",
    ),
]

EXPECTED_DISK_FILES = [
    "results.png",
    "message_bodies.txt",
    "alberti_v26_branchfix.html",
    "Claudes_Alberti_LP_summary.md.pdf",
    "Ivis_Alberti_LP summary.pdf",
    "Alberti_statisticsGr.rtf",
    "Alberti_LP.pdf",
    "test1.pdf",
    "Bookcover_inv.pdf",
    "Rule changes from base M.pdf",
    "39_1_clear.webp",
    "P39_1row_ext.webp",
    "p.39_new.webp",
    "Branching2.webp",
    "Branching3.webp",
    "image.webp",
    "image1231234.webp",
    "image1352.webp",
    "image234151.webp",
    "image2361234.webp",
    "image3423651.webp",
    "image456234346.webp",
    "image663333333323.webp",
    "image782634.png",
]

FORBIDDEN_FALSE_FLAGS = {
    "activation_authorized_now",
    "activation_decision_valid_now",
    "active_ingestion_performed",
    "active_manifest_registry_updated",
    "active_planning_input_authorized_now",
    "active_planning_input_selected_now",
    "active_token_block_manifest_changed",
    "alberti_cipher_execution_performed_now",
    "alberti_html_executed_now",
    "ai_ml_interpretation_performed",
    "audio_stego_performed",
    "benchmark_performed",
    "branch_enumeration_performed",
    "byte_stream_generation_authorized_now",
    "canonical_corpus_active",
    "combined_approval_gate_satisfied_now",
    "cuda_execution_performed",
    "decode_attempt_performed",
    "decryption_attempt_performed_now",
    "disk_cipher_execution_performed_now",
    "dwh_hash_search_performed",
    "execution_authorized_now",
    "execution_performed",
    "full_cartesian_product_enumerated",
    "generated_outputs_committed",
    "hash_preimage_search_performed",
    "html_tool_executed_now",
    "image_forensics_performed",
    "known_plaintext_attack_performed_now",
    "mp3stego_execution_performed",
    "network_target_validation_performed_now",
    "ocr_performed",
    "openpuff_execution_performed",
    "page32_route_extraction_performed_now",
    "page56_hash_preimage_tested_now",
    "pivot_target_selected_now",
    "probability_claim_accepted_as_validated",
    "real_byte_stream_generated",
    "route_extraction_performed_now",
    "scoring_performed",
    "solve_claim",
    "spectrogram_stego_performed",
    "target_class_validation_implemented",
    "target_priority_decision_created_now",
    "token_block_experiment_executed",
    "tor_network_access_performed",
    "triangle_route_extraction_performed_now",
    "variant_materialisation_performed",
    "website_expansion_performed",
}

DATA_PATHS = {
    "summary": Path("data/project-state/stage5dn-summary.yaml"),
    "next_stage_decision": Path("data/project-state/stage5dn-next-stage-decision.yaml"),
    "stage5dm_preservation": Path("data/project-state/stage5dn-stage5dm-preservation.yaml"),
    "reviewable_validation_evidence": Path(
        "data/project-state/stage5dn-reviewable-validation-evidence.yaml"
    ),
    "reviewability_gap_register": Path("data/project-state/stage5dn-reviewability-gap-register.yaml"),
    "drive_folder_policy_update": Path(
        "data/project-state/stage5dn-drive-folder-policy-update.yaml"
    ),
    "governance_scope_control": Path("data/project-state/stage5dn-governance-scope-control.yaml"),
    "disk_cipher_v1_source_lock_register": Path(
        "data/source-harvester/stage5dn-disk-cipher-v1-source-lock-register.yaml"
    ),
    "disk_cipher_v1_file_inventory": Path(
        "data/source-harvester/stage5dn-disk-cipher-v1-file-inventory.yaml"
    ),
    "disk_message_bodies_source_lock": Path(
        "data/source-harvester/stage5dn-disk-message-bodies-source-lock.yaml"
    ),
    "disk_results_png_source_lock": Path(
        "data/source-harvester/stage5dn-disk-results-png-source-lock.yaml"
    ),
    "raw_source_noncommit_proof": Path(
        "data/source-harvester/stage5dn-raw-source-noncommit-proof.yaml"
    ),
    "codex_handoff_policy": Path("data/source-harvester/stage5dn-codex-handoff-policy.yaml"),
    "credential_redaction_policy_preservation": Path(
        "data/source-harvester/stage5dn-credential-redaction-policy-preservation.yaml"
    ),
    "disk_alberti_branch_cipher_candidate": Path(
        "data/historical-route/stage5dn-disk-alberti-branch-cipher-candidate-v1.yaml"
    ),
    "disk_p39_row1_math_semantic_cluster": Path(
        "data/historical-route/stage5dn-disk-p39-row1-math-semantic-cluster-v1.yaml"
    ),
    "disk_56311_wynn_way_bridge": Path(
        "data/historical-route/stage5dn-disk-56311-wynn-way-bridge-v1.yaml"
    ),
    "disk_rule4_mobius_trip_rotation_bridge": Path(
        "data/historical-route/stage5dn-disk-rule4-mobius-trip-rotation-bridge-v0.yaml"
    ),
    "disk_doublet_suppression_candidate": Path(
        "data/historical-route/stage5dn-disk-doublet-suppression-candidate-v1.yaml"
    ),
    "disk_ruth_root_route_way_wordplay_candidate": Path(
        "data/historical-route/stage5dn-disk-ruth-root-route-way-wordplay-candidate-v0.yaml"
    ),
    "disk_2015_eclipse_167_temporal_candidate": Path(
        "data/historical-route/stage5dn-disk-2015-eclipse-167-temporal-candidate-v0.yaml"
    ),
    "pdd_153_triangle_56311_wynn_way_route": Path(
        "data/historical-route/stage5dn-pdd-153-triangle-56311-wynn-way-route-v1.yaml"
    ),
    "solved_i_voice_of_circumference_precedent": Path(
        "data/historical-route/stage5dn-solved-i-voice-of-circumference-precedent-v0.yaml"
    ),
    "circumference_single_i_spiral_anchor_crosslink": Path(
        "data/historical-route/stage5dn-circumference-single-i-spiral-anchor-crosslink-v0.yaml"
    ),
    "disk_probability_claim_quarantine": Path(
        "data/historical-route/stage5dn-disk-probability-claim-quarantine-v1.yaml"
    ),
    "stage5dg_preservation": Path("data/token-block/stage5dn-stage5dg-preservation.yaml"),
    "stage5bd_preservation": Path("data/token-block/stage5dn-stage5bd-preservation.yaml"),
    "active_lineage_preservation": Path("data/token-block/stage5dn-active-lineage-preservation.yaml"),
    "no_active_ingestion_proof": Path("data/token-block/stage5dn-no-active-ingestion-proof.yaml"),
    "no_byte_stream_transition_gate": Path(
        "data/token-block/stage5dn-no-byte-stream-transition-gate.yaml"
    ),
    "no_execution_transition_gate": Path("data/token-block/stage5dn-no-execution-transition-gate.yaml"),
}

SCHEMA_PATHS = {
    key: Path("schemas") / path.parent.relative_to("data") / f"{path.stem}-v0.schema.json"
    for key, path in DATA_PATHS.items()
}

CANDIDATE_KEYS = {
    "disk_alberti_branch_cipher_candidate",
    "disk_p39_row1_math_semantic_cluster",
    "disk_56311_wynn_way_bridge",
    "disk_rule4_mobius_trip_rotation_bridge",
    "disk_doublet_suppression_candidate",
    "disk_ruth_root_route_way_wordplay_candidate",
    "disk_2015_eclipse_167_temporal_candidate",
    "pdd_153_triangle_56311_wynn_way_route",
    "solved_i_voice_of_circumference_precedent",
    "circumference_single_i_spiral_anchor_crosslink",
    "disk_probability_claim_quarantine",
}


@dataclass(frozen=True)
class ValidationResult:
    command: str
    validation_error_count: int
    errors: list[str]

    def to_cli_text(self) -> str:
        lines = [
            f"command={self.command}",
            f"validation_error_count={self.validation_error_count}",
        ]
        lines.extend(f"error={error}" for error in self.errors)
        return "\n".join(lines)


def _posix_path(path: Path) -> str:
    return path.as_posix()


def _record_type(key: str) -> str:
    return f"stage5dn_{key}"


def _base_record(key: str, source_previous_commit: str) -> dict[str, Any]:
    record = {
        "record_type": _record_type(key),
        "schema": _posix_path(SCHEMA_PATHS[key]),
        "stage_id": STAGE_ID,
        "stage_title": STAGE_TITLE,
        "prompt_type": PROMPT_TYPE,
        "source_previous_stage": SOURCE_PREVIOUS_STAGE_ID,
        "source_previous_stage_id": SOURCE_PREVIOUS_STAGE_ID,
        "source_previous_stage_commit": source_previous_commit,
        "metadata_only": True,
        "execution_allowed": False,
        "canonical_codex_handoff_root": "codex-output",
        "stage5dm_records_assumed_present_for_stage5dn_addendum": True,
        "stage5dm_rerun_performed": False,
        "stage5dg_operator_approval_record_preserved": True,
        "operator_approval_component_satisfied_now": True,
        "deep_research_activation_accept_record_present_now": False,
        "deep_research_acceptance_component_satisfied_now": False,
        "combined_approval_gate_satisfied_now": False,
        "stage5bd_run_plan_id_count": 10,
        "active_lineage_record_count": len(ACTIVE_LINEAGE_PATHS),
        "parallel_worker_cap_for_stage5dn_and_later": PARALLEL_WORKER_CAP,
        "recommended_next_stage_id": NEXT_STAGE_ID,
        "recommended_next_stage_title": NEXT_STAGE_TITLE,
        "recommended_next_prompt_type": PROMPT_TYPE,
    }
    record.update({flag: False for flag in sorted(FORBIDDEN_FALSE_FLAGS)})
    return record


def _schema_for(key: str) -> dict[str, Any]:
    required = [
        "record_type",
        "stage_id",
        "metadata_only",
        "solve_claim",
        "execution_allowed",
    ]

    def add_required(*names: str) -> None:
        for name in names:
            if name not in required:
                required.append(name)

    properties: dict[str, Any] = {
        "record_type": {"const": _record_type(key)},
        "stage_id": {"const": STAGE_ID},
        "metadata_only": {"const": True},
        "solve_claim": {"const": False},
        "execution_allowed": {"const": False},
    }
    for flag in sorted(FORBIDDEN_FALSE_FLAGS):
        add_required(flag)
        properties[flag] = {"const": False}
    if key in CANDIDATE_KEYS:
        add_required("source_lock_only", "accepted_as_route", "execution_authorized_now")
        properties.update(
            {
                "source_lock_only": {"const": True},
                "accepted_as_route": {"const": False},
                "execution_authorized_now": {"const": False},
            }
        )
    if key == "disk_probability_claim_quarantine":
        add_required("probability_claim_accepted_as_validated")
        properties["probability_claim_accepted_as_validated"] = {"const": False}
    if key == "disk_results_png_source_lock":
        add_required("ocr_performed", "image_forensics_performed", "accepted_as_proof")
        properties.update(
            {
                "ocr_performed": {"const": False},
                "image_forensics_performed": {"const": False},
                "accepted_as_proof": {"const": False},
            }
        )
    if key == "disk_message_bodies_source_lock":
        add_required("claim_groups", "full_raw_body_committed")
        properties.update(
            {
                "claim_groups": {"type": "array", "minItems": len(CLAIM_GROUPS)},
                "full_raw_body_committed": {"const": False},
            }
        )
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": _posix_path(SCHEMA_PATHS[key]),
        "type": "object",
        "required": required,
        "properties": properties,
        "additionalProperties": True,
    }


def _write_schemas() -> None:
    for key, path in SCHEMA_PATHS.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(_schema_for(key), indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _classify_file(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix == ".png":
        return "image_png"
    if suffix in {".jpg", ".jpeg"}:
        return "image_jpeg"
    if suffix == ".webp":
        return "image_webp"
    if suffix == ".txt":
        return "text_plain"
    if suffix == ".html":
        return "html_tool_candidate"
    if suffix == ".pdf":
        return "pdf_source_document"
    if suffix == ".rtf":
        return "rtf_source_document"
    return "other_source_file"


def _file_role(path: Path) -> str:
    name = path.name.lower()
    if name == "results.png":
        return "result_summary_image"
    if name == "message_bodies.txt":
        return "updated_forum_or_chat_message_body_export"
    if name == "alberti_v26_branchfix.html":
        return "html_tool_candidate"
    if "rule" in name:
        return "disk_rule_reference_document"
    if path.suffix.lower() in {".webp", ".png"}:
        return "supporting_visual_source"
    if path.suffix.lower() in {".pdf", ".rtf"}:
        return "supporting_source_document"
    return "supporting_source_file"


def _safe_file_record(path: Path, root: Path) -> dict[str, Any]:
    stat = path.stat()
    return {
        "relative_path": _posix_path(path.relative_to(root)),
        "repo_relative_path": _posix_path(path),
        "file_name": path.name,
        "file_size_bytes": stat.st_size,
        "sha256": sha256_file(path),
        "file_kind": _classify_file(path),
        "source_role": _file_role(path),
        "mime_type_guess": mimetypes.guess_type(path.name)[0] or "application/octet-stream",
        "source_lock_status": "present_ignored_local_source",
        "raw_file_committed_now": False,
        "html_executed_now": False if path.suffix.lower() == ".html" else None,
    }


def _disk_root() -> Path:
    if DISK_EFFECTIVE_ROOT.exists():
        return DISK_EFFECTIVE_ROOT
    return DISK_SOURCE_ROOT


def _disk_file_inventory() -> tuple[Path, list[dict[str, Any]], list[dict[str, Any]]]:
    root = _disk_root()
    files = []
    if root.exists():
        files = sorted([path for path in root.rglob("*") if path.is_file()])
    records = [_safe_file_record(path, root) for path in files]
    by_name = {record["relative_path"]: record for record in records}
    gaps = []
    for expected in EXPECTED_DISK_FILES:
        if expected not in by_name:
            gaps.append(
                {
                    "relative_path": expected,
                    "present": False,
                    "source_lock_status": "optional_expected_file_missing",
                    "blocking": False,
                }
            )
    return root, records, gaps


def _read_text_digest(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {
            "source_path": _posix_path(path),
            "present": False,
            "sha256": None,
            "file_size_bytes": 0,
            "line_count": 0,
        }
    text = path.read_text(encoding="utf-8", errors="replace")
    return {
        "source_path": _posix_path(path),
        "present": True,
        "sha256": sha256_file(path),
        "file_size_bytes": path.stat().st_size,
        "line_count": len(text.splitlines()),
        "text_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
    }


def _image_dimensions(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"width": None, "height": None, "image_metadata_recorded": False}
    try:
        from PIL import Image

        with Image.open(path) as image:
            return {
                "width": image.width,
                "height": image.height,
                "image_format": image.format,
                "colour_mode": image.mode,
                "image_metadata_recorded": True,
            }
    except Exception as exc:  # pragma: no cover - Pillow may be unavailable in local variants.
        return {
            "width": None,
            "height": None,
            "image_metadata_recorded": False,
            "image_metadata_error": type(exc).__name__,
        }


def _translation_source_lock() -> dict[str, Any]:
    selected = next((path for path in TRANSLATION_CANDIDATES if path.exists()), TRANSLATION_CANDIDATES[0])
    digest = _read_text_digest(selected)
    return {
        **digest,
        "source_file_candidates": [_posix_path(path) for path in TRANSLATION_CANDIDATES],
        "selected_source_path": _posix_path(selected),
    }


def _claim_group_records() -> list[dict[str, Any]]:
    return [
        {
            "id": claim_id,
            "summary": summary,
            "claim_status": "source_locked_candidate",
            "accepted_as_solved": False,
            "experiment_executed_now": False,
        }
        for claim_id, summary in CLAIM_GROUPS
    ]


def _file_by_name(records: list[dict[str, Any]], name: str) -> dict[str, Any] | None:
    return next((record for record in records if record["relative_path"] == name), None)


def _preservation_record(key: str, source_previous_commit: str, updates: dict[str, Any]) -> dict[str, Any]:
    record = _base_record(key, source_previous_commit)
    record.update(
        {
            "preservation_record": True,
            "source_lock_only": True,
            "selected_now": False,
            "accepted_as_route": False,
            "stage5bd_run_plan_ids_preserved": True,
            "active_lineage_preserved": True,
        }
    )
    record.update(updates)
    return record


def _build_records(source_previous_commit: str | None = None) -> dict[str, dict[str, Any]]:
    source_previous_commit = source_previous_commit or SOURCE_PREVIOUS_STAGE_COMMIT
    disk_root, file_records, file_gaps = _disk_file_inventory()
    results_path = disk_root / "results.png"
    message_path = disk_root / "message_bodies.txt"
    message_digest = _read_text_digest(message_path)
    results_record = _file_by_name(file_records, "results.png")
    message_record = _file_by_name(file_records, "message_bodies.txt")
    html_record = _file_by_name(file_records, "alberti_v26_branchfix.html")
    source_root_exists = DISK_SOURCE_ROOT.exists()

    records: dict[str, dict[str, Any]] = {}

    records["disk_cipher_v1_file_inventory"] = {
        **_base_record("disk_cipher_v1_file_inventory", source_previous_commit),
        "source_lock_only": True,
        "source_root": _posix_path(DISK_SOURCE_ROOT),
        "effective_source_root": _posix_path(disk_root),
        "source_root_exists": source_root_exists,
        "effective_source_root_exists": disk_root.exists(),
        "file_count_observed": len(file_records),
        "files": file_records,
        "expected_file_gaps": file_gaps,
        "html_tool_executed_now": False,
        "raw_files_committed_now": False,
    }

    records["disk_cipher_v1_source_lock_register"] = {
        **_base_record("disk_cipher_v1_source_lock_register", source_previous_commit),
        "source_lock_only": True,
        "source_root": _posix_path(DISK_SOURCE_ROOT),
        "effective_source_root": _posix_path(disk_root),
        "source_root_exists": source_root_exists,
        "updated_disk_cipher_material_detected": bool(file_records),
        "results_png_present": results_record is not None,
        "message_bodies_present": message_record is not None,
        "html_tool_present": html_record is not None,
        "html_tool_executed_now": False,
        "raw_files_committed_now": False,
        "file_count_observed": len(file_records),
        "files": file_records,
        "high_flexibility_warning": True,
        "risk_factors": [
            "multiple_disk_rules",
            "flips_and_rotations",
            "branch_points",
            "manual_or_semimanual_reading",
            "semantic_target_selection",
            "unknown_search_space",
            "probability_claim_not_audited",
        ],
        "why_preserve_anyway": [
            "row1_math_terms_overlap_solved_lp_math_vocabulary",
            "wynn_bridge_to_triangle_center",
            "sequence_56311_hits_word52_from_center",
            "circumference_overlap_solved_koan_and_blake_music_page32_context",
            "doublet_suppression_claim_matches_operator_doublet_observation",
        ],
    }

    records["disk_results_png_source_lock"] = {
        **_base_record("disk_results_png_source_lock", source_previous_commit),
        "source_path": _posix_path(results_path),
        "source_type": "result_summary_image",
        "source_lock_only": True,
        "source_present": results_path.exists(),
        "file_size_bytes": results_path.stat().st_size if results_path.exists() else 0,
        "sha256": sha256_file(results_path) if results_path.exists() else None,
        **_image_dimensions(results_path),
        "ocr_performed": False,
        "image_forensics_performed": False,
        "ai_ml_interpretation_performed": False,
        "accepted_as_proof": False,
        "candidate_context": "disk_p39_row1_math_semantic_cluster_v1",
        "raw_file_committed_now": False,
    }

    records["disk_message_bodies_source_lock"] = {
        **_base_record("disk_message_bodies_source_lock", source_previous_commit),
        **message_digest,
        "source_lock_only": True,
        "compact_excerpts_only": True,
        "full_raw_body_committed": False,
        "raw_file_committed_now": False,
        "claim_groups": _claim_group_records(),
        "late_update_claims": [
            "p39_first_row_branching_results",
            "row1_math_semantic_cluster",
            "sequence_56311_horizontal_and_vertical",
            "dot_branching_plus_one",
            "wynn_duplicate_or_special_rune",
            "rule4_mobius_trip_rotation_loop",
            "doublet_suppression",
            "ruth_root_route_way_wordplay",
            "eclipse_2015_167_second_temporal_candidate",
            "blake_urizen_circumference_loop_metaphor",
        ],
        "html_tool_executed_now": False,
        "disk_cipher_execution_performed_now": False,
    }

    records["disk_alberti_branch_cipher_candidate"] = {
        **_base_record("disk_alberti_branch_cipher_candidate", source_previous_commit),
        "candidate_family_id": "disk_alberti_branch_cipher_candidate_v1",
        "source_root": _posix_path(DISK_SOURCE_ROOT),
        "source_lock_only": True,
        "model_status": "community_candidate_unverified",
        "html_tool_executed_now": False,
        "disk_cipher_execution_performed_now": False,
        "branch_enumeration_performed_now": False,
        "branch_enumeration_performed": False,
        "accepted_as_route": False,
        "execution_authorized_now": False,
        "high_degrees_of_freedom_warning": True,
        "claimed_model_components": [
            "alberti_disk_correspondences",
            "book_cover_finger_rules",
            "four_rule_codebook",
            "flips_and_rotations",
            "sequence_56311",
            "dot_branching_plus_one",
            "multiple_branch_plaintext_fragments",
            "wynn_duplicate_or_special_rune",
        ],
    }

    records["disk_p39_row1_math_semantic_cluster"] = {
        **_base_record("disk_p39_row1_math_semantic_cluster", source_previous_commit),
        "candidate_family_id": "disk_p39_row1_math_semantic_cluster_v1",
        "source_context": "p.39 first compressed row / branch result summary",
        "source_lock_only": True,
        "accepted_as_route": False,
        "execution_authorized_now": False,
        "accepted_as_decryption": False,
        "cluster_accepted_as_plaintext": False,
        "cluster_source": "results_png_and_message_bodies_claims",
        "cluster_interpretation_status": "semantic_candidate_only",
        "terms_are_claimed_by_source_author": True,
        "assistant_review_found_terms_relevant": True,
        "requires_future_independent_reimplementation": True,
        "requires_future_negative_controls": True,
        "terms_claimed": [
            "EULER",
            "LEONHARD",
            "NAPIER",
            "JOHN",
            "TOTIENT",
            "CIRCUMFERENCE",
            "PRIME_NUMBER",
            "FISH",
            "WYNN",
            "PHI",
        ],
        "math_terms": ["EULER", "LEONHARD", "NAPIER", "JOHN", "TOTIENT", "PHI", "PRIME_NUMBER"],
        "geometry_or_lp_terms": ["CIRCUMFERENCE", "FISH", "WYNN"],
        "lp_relevance": [
            "prime_totient_solved_wisdom_precedent",
            "circumference_solved_koan_precedent",
            "fish_153_triangle_symbolic_context",
            "wynn_center_41_triangle_context",
            "phi_geometry_context",
        ],
    }

    records["disk_56311_wynn_way_bridge"] = {
        **_base_record("disk_56311_wynn_way_bridge", source_previous_commit),
        "candidate_family_id": "disk_56311_wynn_way_bridge_v1",
        "source_sequence": [5, 6, 3, 11],
        "source_sequence_status": "disk_cipher_candidate_sequence",
        "source_lock_only": True,
        "triangle_center_index": 41,
        "triangle_center_word": "\\u16b9",
        "triangle_center_latin": "W",
        "wynn_rune": "\\u16b9",
        "wynn_bridge_present": True,
        "word52_way_derivation_candidate": True,
        "cumulative_offsets_from_center": [5, 11, 14, 25],
        "positions_from_center": [46, 52, 55, 66],
        "position_52_reached_from_center": True,
        "position_52_role": "word52_derives_WAY_when_reversed_against_heading",
        "accepted_as_route": False,
        "route_extraction_performed_now": False,
        "execution_authorized_now": False,
        "links_to": [
            "pdd_153_triangle_56311_wynn_way_route_v1",
            "pdd_153_triangle_way_anchor_route_v1",
            "pdd_153_triangle_word_prime_route_v1",
        ],
    }

    records["pdd_153_triangle_56311_wynn_way_route"] = {
        **_base_record("pdd_153_triangle_56311_wynn_way_route", source_previous_commit),
        "candidate_subfamily_id": "pdd_153_triangle_56311_wynn_way_route_v1",
        "candidate_family_id": "pdd_153_triangle_56311_wynn_way_route_v1",
        "source_lock_only": True,
        "stage5dl_record_preserved": True,
        "stage5dn_disk_v1_support_added": True,
        "source_bridge_records": [
            "disk_56311_wynn_way_bridge_v1",
            "disk_p39_row1_math_semantic_cluster_v1",
            "solved_i_voice_of_circumference_precedent_v0",
        ],
        "center_word_index": 41,
        "center_word_rune": "\\u16b9",
        "word52_reached_by_56311_from_center": True,
        "word52_way_derivation_candidate_preserved": True,
        "selected_now": False,
        "accepted_as_route": False,
        "execution_authorized_now": False,
    }

    records["solved_i_voice_of_circumference_precedent"] = {
        **_base_record("solved_i_voice_of_circumference_precedent", source_previous_commit),
        **_translation_source_lock(),
        "candidate_context_id": "solved_i_voice_of_circumference_precedent_v0",
        "candidate_family_id": "solved_i_voice_of_circumference_precedent_v0",
        "source_section_id": "0.4.0",
        "source_section_type": "solved_koan",
        "source_status": "solved_translation_precedent",
        "source_lock_only": True,
        "accepted_as_route": False,
        "execution_authorized_now": False,
        "accepted_as_solved_precedent": True,
        "used_for_decryption_now": False,
        "plaintext_quote": "THE I IS THE VOICE OF THE CIRCUMFERENCE",
        "speaker_tag": "HE SAID",
        "plain_i_token_length": 1,
        "circumference_token_present": True,
        "voice_inside_head_context_present": True,
        "source_lines": [
            {"id": "0.4.0.1", "text": "DURING A LESSON, THE MASTER EXPLAINED THE I"},
            {"id": "0.4.0.2", "text": "\"THE I IS THE VOICE OF THE CIRCUMFERENCE,\" HE SAID"},
            {
                "id": "0.4.0.3",
                "text_contains": 'THE MASTER SAID "IT IS A VOICE INSIDE YOUR HEAD"',
            },
            {
                "id": "0.4.0.5",
                "text_contains": '"THE VOICE THAT JUST SAID YOU HAVE NO VOICE IN YOUR HEAD; IS THE I"',
            },
        ],
        "relevance": [
            "circumference_theme",
            "single_letter_I_anchor",
            "quote_dialogue_crib_template",
            "solved_koan_body_self_context",
            "disk_circumference_blake_urizen_claim",
            "triangle_single_rune_anchor_context",
        ],
        "links_to": [
            "disk_p39_row1_math_semantic_cluster_v1",
            "disk_rule4_mobius_trip_rotation_bridge_v0",
            "circumference_single_i_spiral_anchor_crosslink_v0",
            "blake_urizen_los_reason_circumference_v0",
            "music_3301_instar_crab_canon_v0",
            "pdd_153_triangle_word_prime_route_v1",
        ],
        "single_letter_I_relation_to_single_rune_anchors": "candidate_crosslink_only",
        "not_claiming_I_equals_center_W": True,
        "not_claiming_direct_mapping_between_I_and_wynn": True,
    }

    records["circumference_single_i_spiral_anchor_crosslink"] = {
        **_base_record("circumference_single_i_spiral_anchor_crosslink", source_previous_commit),
        "candidate_family_id": "circumference_single_i_spiral_anchor_crosslink_v0",
        "source_lock_only": True,
        "crosslink_only": True,
        "crosslink_status": "thematic_and_structural_candidate",
        "accepted_as_route": False,
        "execution_authorized_now": False,
        "not_a_mapping_claim": True,
        "not_claiming_i_equals_wynn": True,
        "not_claiming_i_equals_triangle_center": True,
        "not_claiming_plain_i_maps_to_single_rune_anchor": True,
        "source_facts": [
            "solved text says THE I IS THE VOICE OF THE CIRCUMFERENCE",
            "triangle has single-rune anchors [25, 41, 53, 91, 106]",
            "triangle center word 41 is single rune \\u16b9",
            "Page32 contains giant Moebius and Fibonacci-prime-index spiral",
            "DiskCipher claims CIRCUMFERENCE and WYNN in row-1 cluster",
            "Music metadata says shed our own circumferences",
            "Blake source family includes Urizen/compass/circumference/selfhood context",
        ],
        "candidate_relationships": [
            "single_letter_I_in_solved_koan",
            "circumference_theme",
            "spiral_and_mobius_route_context",
            "disk_cipher_circular_mechanics",
            "triangle_single_rune_anchors",
            "center_word_41_wynn",
            "music_shed_circumference_context",
        ],
    }

    records["disk_rule4_mobius_trip_rotation_bridge"] = {
        **_base_record("disk_rule4_mobius_trip_rotation_bridge", source_previous_commit),
        "candidate_family_id": "disk_rule4_mobius_trip_rotation_bridge_v0",
        "source_lock_only": True,
        "source_claim_summary": "DiskCipher notes compare rule/rotation/flip behavior to a Moebius trip/step/loop candidate.",
        "claimed_components": ["rotation", "flip", "loop", "step_or_trip", "circumference"],
        "links_to": [
            "page32_mobius_fibonacci_prime_index_spiral_v1",
            "mobius_loop_orientation_marker_v0",
            "disk_alberti_branch_cipher_candidate_v1",
        ],
        "confidence": "low_medium",
        "accepted_as_route": False,
        "execution_authorized_now": False,
        "execution_performed_now": False,
    }

    records["disk_doublet_suppression_candidate"] = {
        **_base_record("disk_doublet_suppression_candidate", source_previous_commit),
        "candidate_family_id": "disk_doublet_suppression_candidate_v1",
        "source_lock_only": True,
        "source_claim_status": "community_or_ai_assisted_candidate",
        "claim_status": "source_locked_unverified",
        "claimed_values_source": "DiskCipherStuff community/assistant-summary material",
        "claimed_expected_doublets": 448,
        "claimed_observed_doublets": 89,
        "claimed_suppression_factor": "approximately_5x",
        "claimed_suppression_factor_approx": 5,
        "accepted_as_validated": False,
        "probability_claim_accepted_as_validated": False,
        "future_validation_required": True,
        "requires_future_independent_metric_definition": True,
        "requires_future_search_space_audit": True,
        "future_validation_requirements": [
            "exact_doublet_metric_definition",
            "canonical_lp_corpus_selection",
            "solved_vs_unsolved_split",
            "random_controls",
            "model_output_controls",
            "trial_count_accounting",
        ],
        "links_to": ["lp_doublet_scarcity_feature_v0", "disk_alberti_branch_cipher_candidate_v1"],
        "accepted_as_route": False,
        "execution_authorized_now": False,
    }

    records["disk_probability_claim_quarantine"] = {
        **_base_record("disk_probability_claim_quarantine", source_previous_commit),
        "candidate_family_id": "disk_probability_claim_quarantine_v1",
        "source_lock_only": True,
        "probability_claims_present": True,
        "probability_claim_accepted_as_validated": False,
        "accepted_as_route": False,
        "execution_authorized_now": False,
        "reason_for_quarantine": [
            "many_degrees_of_freedom",
            "manual_or_semiautomated_branch_selection",
            "unclear_search_space",
            "unclear_dictionary_or_semantic_target_class",
            "possible_selection_bias",
        ],
        "future_requirements": [
            "formal_model_specification",
            "deterministic_reimplementation",
            "trial_count_accounting",
            "negative_controls",
            "blind_test_against_randomized_inputs",
        ],
    }

    records["disk_ruth_root_route_way_wordplay_candidate"] = {
        **_base_record("disk_ruth_root_route_way_wordplay_candidate", source_previous_commit),
        "candidate_family_id": "disk_ruth_root_route_way_wordplay_candidate_v0",
        "source_lock_only": True,
        "source_claim_summary": "DiskCipher notes propose WAY/RUTH/root/route/road/path/direction semantic bridge.",
        "confidence": "low_medium",
        "reason_for_confidence": "semantically relevant_to_2016_way_path_road_direction_but_flexible_wordplay",
        "accepted_as_route": False,
        "execution_authorized_now": False,
        "links_to": [
            "pdd_153_triangle_way_anchor_route_v1",
            "2016_message_route_meta_clue_v0",
            "disk_56311_wynn_way_bridge_v1",
        ],
    }

    records["disk_2015_eclipse_167_temporal_candidate"] = {
        **_base_record("disk_2015_eclipse_167_temporal_candidate", source_previous_commit),
        "candidate_family_id": "disk_2015_eclipse_167_temporal_candidate_v0",
        "source_lock_only": True,
        "source_claim_summary": "DiskCipher notes propose March 20 2015 eclipse/equinox/167-second timing candidate.",
        "external_fact_verification_performed_now": False,
        "external_fact_source_locked_now": False,
        "confidence": "low_medium",
        "reason_for_confidence": "possible_crosslink_to_761_MP3_duration_167_seconds_but_external_symbolic_chain_is_broad",
        "reason_for_low_medium": "externally_symbolic_chain_is_broad_but_167_seconds_crosslink_to_761_mp3_duration_is_notable",
        "links_to": ["music_3301_instar_crab_canon_v0", "disk_alberti_branch_cipher_candidate_v1"],
        "future_verification_required": True,
        "accepted_as_cicada_clue": False,
        "accepted_as_route": False,
        "execution_authorized_now": False,
    }

    reviewability_gaps = [
        {
            "gap_id": "disk_cipher_model_not_independently_reimplemented",
            "severity": "medium_high",
            "blocking": False,
        },
        {"gap_id": "disk_probability_claim_quarantined", "severity": "medium", "blocking": False},
        {
            "gap_id": "results_png_not_ocr_or_machine_interpreted",
            "severity": "low",
            "blocking": False,
        },
        {
            "gap_id": "solved_i_circumference_crosslink_is_thematic_not_decryption",
            "severity": "low",
            "blocking": False,
        },
        {
            "gap_id": "eclipse_167_candidate_external_chain_broad",
            "severity": "medium",
            "blocking": False,
        },
    ]

    records["reviewability_gap_register"] = {
        **_base_record("reviewability_gap_register", source_previous_commit),
        "source_lock_only": True,
        "reviewability_gaps": reviewability_gaps,
        "gap_count": len(reviewability_gaps),
        "gap_authorizes_execution": False,
    }

    records["drive_folder_policy_update"] = {
        **_base_record("drive_folder_policy_update", source_previous_commit),
        "source_lock_only": True,
        "preferred_google_drive_folder_now": "LiberPrimusSolver",
        "previous_temporary_drive_folder": "LiberPrimusSolverDrive",
        "reason_for_reversion": "regular_folder_no_longer_contains_root_git_or_wiki_git_folders",
        "google_drive_storage_used": False,
        "local_storage_only_for_stage5dn": True,
        "visible_drive_git_warning_recorded": False,
        "drive_content_modified": False,
    }

    records["raw_source_noncommit_proof"] = {
        **_base_record("raw_source_noncommit_proof", source_previous_commit),
        "source_lock_only": True,
        "raw_files_committed_now": False,
        "raw_disk_cipher_files_committed_now": False,
        "generated_outputs_committed": False,
        "codex_output_committed": False,
        "sqlite_staged": 0,
    }

    records["codex_handoff_policy"] = {
        **_base_record("codex_handoff_policy", source_previous_commit),
        "source_lock_only": True,
        "canonical_codex_handoff_root": "codex-output",
        "deprecated_codex_output_used": False,
        "codex_completion_summary_path": _posix_path(CODEX_COMPLETION_PATH),
        "codex_completion_summary_committed": False,
    }

    records["credential_redaction_policy_preservation"] = {
        **_base_record("credential_redaction_policy_preservation", source_previous_commit),
        "source_lock_only": True,
        "credential_redaction_policy_preserved": True,
        "secrets_committed": False,
        "raw_message_body_publication_performed": False,
    }

    records["stage5dm_preservation"] = _preservation_record(
        "stage5dm_preservation",
        source_previous_commit,
        {
            "stage5dm_summary_path": _posix_path(STAGE5DM_DATA_PATHS["summary"]),
            "stage5dm_validation_required": True,
            "stage5dm_preserved": True,
        },
    )
    records["stage5dg_preservation"] = _preservation_record(
        "stage5dg_preservation",
        source_previous_commit,
        {
            "stage5dg_operator_approval_record_preserved": True,
            "operator_approval_component_satisfied_now": True,
            "deep_research_activation_accept_record_present_now": False,
        },
    )
    records["stage5bd_preservation"] = _preservation_record(
        "stage5bd_preservation",
        source_previous_commit,
        {
            "stage5bd_validation_passed": validate_stage5bd()[0].get("validation_error_count") == 0,
            "stage5bd_run_plan_id_count": 10,
        },
    )
    records["active_lineage_preservation"] = _preservation_record(
        "active_lineage_preservation",
        source_previous_commit,
        {
            "active_lineage_record_paths": ACTIVE_LINEAGE_PATHS,
            "active_lineage_record_count": len(ACTIVE_LINEAGE_PATHS),
        },
    )
    records["no_active_ingestion_proof"] = _preservation_record(
        "no_active_ingestion_proof",
        source_previous_commit,
        {"active_ingestion_performed": False, "active_planning_input_selected_now": False},
    )
    records["no_byte_stream_transition_gate"] = _preservation_record(
        "no_byte_stream_transition_gate",
        source_previous_commit,
        {"byte_stream_generation_authorized_now": False, "real_byte_stream_generated": False},
    )
    records["no_execution_transition_gate"] = _preservation_record(
        "no_execution_transition_gate",
        source_previous_commit,
        {
            "execution_authorized_now": False,
            "execution_performed": False,
            "token_block_experiment_executed": False,
        },
    )

    records["reviewable_validation_evidence"] = {
        **_base_record("reviewable_validation_evidence", source_previous_commit),
        "source_lock_only": True,
        "validation_commands": [
            "token-block build-stage5dn",
            "token-block validate-stage5dn",
            "token-block stage5dn-summary",
            "focused Stage 5DN validators",
            "ruff check python/libreprimus tests/python",
            "pytest -q tests/python",
            "scripts/ci/run-parallel-validation.ps1 -Workers 8 -PytestWorkers 8 -PytestMode auto",
            "scripts/ci/run-consistency-checks.ps1",
        ],
        "validation_evidence_is_terminal_output_only": False,
        "reviewability_gap_count": len(reviewability_gaps),
    }

    records["governance_scope_control"] = {
        **_base_record("governance_scope_control", source_previous_commit),
        "source_lock_only": True,
        "scope_control_status": "all_stage5dn_operational_gates_closed",
        "target_selected": False,
        "target_selected_now": False,
        "route_extraction_performed_now": False,
        "disk_cipher_execution_performed_now": False,
        "html_tool_executed_now": False,
        "ocr_performed": False,
        "image_forensics_performed": False,
        "solve_claim": False,
    }

    records["next_stage_decision"] = {
        **_base_record("next_stage_decision", source_previous_commit),
        "source_lock_only": True,
        "selected_next_stage_id": NEXT_STAGE_ID,
        "selected_next_stage_title": NEXT_STAGE_TITLE,
        "target_priority_decision_created_now": False,
        "target_selected": False,
        "reason": "Stage 5DN source-locks updated DiskCipher bridges; Stage 5DO must review source/evidence and target-priority readiness without execution.",
    }

    records["summary"] = {
        **_base_record("summary", source_previous_commit),
        "status": "complete",
        "source_lock_only": True,
        "disk_cipher_v1_source_lock_created": True,
        "updated_disk_message_bodies_source_locked": message_path.exists(),
        "disk_results_png_source_locked": results_path.exists(),
        "disk_alberti_branch_cipher_candidate_v1_created": True,
        "disk_p39_row1_math_semantic_cluster_v1_created": True,
        "disk_56311_wynn_way_bridge_v1_created": True,
        "disk_rule4_mobius_trip_rotation_bridge_v0_created": True,
        "disk_doublet_suppression_candidate_v1_created": True,
        "disk_probability_claim_quarantine_v1_created": True,
        "solved_i_voice_of_circumference_precedent_created": True,
        "circumference_single_i_spiral_anchor_crosslink_created": True,
        "pdd_153_triangle_56311_wynn_way_route_v1_updated": True,
        "disk_ruth_root_route_way_wordplay_candidate_v0_created": True,
        "disk_2015_eclipse_167_temporal_candidate_v0_created": True,
        "pivot_target_selected_now": False,
        "route_extraction_performed_now": False,
        "disk_cipher_execution_performed_now": False,
        "html_tool_executed_now": False,
        "ocr_performed": False,
        "image_forensics_performed": False,
        "activation_authorized_now": False,
        "byte_stream_generation_authorized_now": False,
        "execution_authorized_now": False,
        "stage5bd_run_plan_id_count": 10,
        "active_lineage_record_count": len(ACTIVE_LINEAGE_PATHS),
        "parallel_worker_cap_for_stage5dn_and_later": PARALLEL_WORKER_CAP,
        "source_previous_stage": SOURCE_PREVIOUS_STAGE_ID,
        "source_previous_stage_commit": source_previous_commit,
        "recommended_next_stage_id": NEXT_STAGE_ID,
        "recommended_next_stage_title": NEXT_STAGE_TITLE,
        "disk_cipher_stuff_file_count": len(file_records),
        "candidate_records_created": len(CANDIDATE_KEYS),
        "source_lock_addendum_family_count": len(SOURCE_LOCK_FAMILIES),
        "source_lock_addendum_families": SOURCE_LOCK_FAMILIES,
        "results_png_present": results_path.exists(),
        "message_bodies_present": message_path.exists(),
        "raw_third_party_files_committed": False,
        "raw_third_party_files_staged": 0,
        "generated_outputs_staged": 0,
        "codex_output_used": False,
        "sqlite_staged": 0,
    }

    return records


def build_stage5dn() -> dict[str, dict[str, Any]]:
    stage5dm_result = validate_stage5dm()
    if stage5dm_result.validation_error_count:
        joined = "; ".join(stage5dm_result.errors[:5])
        raise RuntimeError(f"Stage 5DM validation failed; refusing Stage 5DN build: {joined}")

    records = _build_records()
    _write_schemas()
    for key, payload in records.items():
        write_yaml(DATA_PATHS[key], payload)

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    write_json(RESULTS_DIR / "summary.json", records["summary"])
    write_json(RESULTS_DIR / "disk_source_lock_report.json", records["disk_cipher_v1_source_lock_register"])
    write_json(RESULTS_DIR / "disk_file_inventory.json", records["disk_cipher_v1_file_inventory"])
    write_json(
        RESULTS_DIR / "candidate_bridge_report.json",
        {
            key: records[key]
            for key in [
                "disk_56311_wynn_way_bridge",
                "pdd_153_triangle_56311_wynn_way_route",
                "solved_i_voice_of_circumference_precedent",
                "circumference_single_i_spiral_anchor_crosslink",
            ]
        },
    )
    write_json(
        RESULTS_DIR / "preservation_report.json",
        {
            key: records[key]
            for key in [
                "stage5dm_preservation",
                "stage5dg_preservation",
                "stage5bd_preservation",
                "active_lineage_preservation",
                "no_active_ingestion_proof",
                "no_byte_stream_transition_gate",
                "no_execution_transition_gate",
            ]
        },
    )
    warnings = records["reviewability_gap_register"]["reviewability_gaps"]
    write_jsonl(RESULTS_DIR / "warnings.jsonl", warnings)
    return records


def _schema_errors(key: str) -> list[str]:
    schema_path = SCHEMA_PATHS[key]
    data_path = DATA_PATHS[key]
    if not schema_path.exists():
        return [f"missing_schema:{schema_path}"]
    if not data_path.exists():
        return [f"missing_data:{data_path}"]
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    data = read_yaml(data_path)
    validator = Draft202012Validator(schema)
    return [
        f"{data_path}:{'/'.join(map(str, error.path))}:{error.message}"
        for error in sorted(validator.iter_errors(data), key=lambda err: list(err.path))
    ]


def _read_record(key: str) -> dict[str, Any]:
    return read_yaml(DATA_PATHS[key]) or {}


def _common_errors(record: dict[str, Any], context: str) -> list[str]:
    errors = []
    if record.get("stage_id") != STAGE_ID:
        errors.append(f"{context}:stage_id_must_be_{STAGE_ID}")
    if record.get("metadata_only") is not True:
        errors.append(f"{context}:metadata_only_must_be_true")
    if record.get("execution_allowed") is not False:
        errors.append(f"{context}:execution_allowed_must_be_false")
    if record.get("canonical_codex_handoff_root") != "codex-output":
        errors.append(f"{context}:canonical_codex_handoff_root_must_be_codex-output")
    if record.get("stage5bd_run_plan_id_count") != 10:
        errors.append(f"{context}:stage5bd_run_plan_id_count_must_be_10")
    if record.get("active_lineage_record_count") != len(ACTIVE_LINEAGE_PATHS):
        errors.append(f"{context}:active_lineage_record_count_must_be_{len(ACTIVE_LINEAGE_PATHS)}")
    if record.get("parallel_worker_cap_for_stage5dn_and_later") != PARALLEL_WORKER_CAP:
        errors.append(f"{context}:parallel_worker_cap_must_be_{PARALLEL_WORKER_CAP}")
    for flag in FORBIDDEN_FALSE_FLAGS:
        if record.get(flag) is not False:
            errors.append(f"{context}:{flag}_must_be_false")
    return errors


def _candidate_common_errors(record: dict[str, Any], context: str) -> list[str]:
    errors = _common_errors(record, context)
    if record.get("source_lock_only") is not True:
        errors.append(f"{context}:source_lock_only_must_be_true")
    if record.get("accepted_as_route") is not False:
        errors.append(f"{context}:accepted_as_route_must_be_false")
    if record.get("execution_authorized_now") is not False:
        errors.append(f"{context}:execution_authorized_now_must_be_false")
    return errors


def _result(command: str, errors: list[str]) -> ValidationResult:
    return ValidationResult(command, len(errors), errors)


def validate_stage5dn_disk_source_lock() -> ValidationResult:
    command = "validate-stage5dn-disk-source-lock"
    register = _read_record("disk_cipher_v1_source_lock_register")
    inventory = _read_record("disk_cipher_v1_file_inventory")
    errors = _common_errors(register, command)
    errors.extend(_common_errors(inventory, f"{command}:inventory"))
    if register.get("updated_disk_cipher_material_detected") is not True:
        errors.append("updated_disk_cipher_material_detected_must_be_true")
    if register.get("results_png_present") is not True:
        errors.append("results_png_present_must_be_true")
    if register.get("message_bodies_present") is not True:
        errors.append("message_bodies_present_must_be_true")
    if register.get("html_tool_present") is not True:
        errors.append("html_tool_present_must_be_true")
    if inventory.get("file_count_observed", 0) < 3:
        errors.append("disk_file_inventory_too_small")
    return _result(command, errors)


def validate_stage5dn_results_png() -> ValidationResult:
    command = "validate-stage5dn-results-png"
    record = _read_record("disk_results_png_source_lock")
    errors = _common_errors(record, command)
    if record.get("source_type") != "result_summary_image":
        errors.append("results_png_source_type_changed")
    if record.get("ocr_performed") is not False:
        errors.append("ocr_performed_must_be_false")
    if record.get("image_forensics_performed") is not False:
        errors.append("image_forensics_performed_must_be_false")
    if record.get("accepted_as_proof") is not False:
        errors.append("accepted_as_proof_must_be_false")
    if record.get("source_present") is not True:
        errors.append("results_png_source_missing")
    return _result(command, errors)


def validate_stage5dn_message_bodies() -> ValidationResult:
    command = "validate-stage5dn-message-bodies"
    record = _read_record("disk_message_bodies_source_lock")
    errors = _common_errors(record, command)
    claim_ids = {claim["id"] for claim in record.get("claim_groups", [])}
    for claim_id, _summary in CLAIM_GROUPS:
        if claim_id not in claim_ids:
            errors.append(f"missing_claim_group:{claim_id}")
    if record.get("full_raw_body_committed") is not False:
        errors.append("full_raw_body_committed_must_be_false")
    return _result(command, errors)


def validate_stage5dn_disk_56311_wynn_way() -> ValidationResult:
    command = "validate-stage5dn-disk-56311-wynn-way"
    record = _read_record("disk_56311_wynn_way_bridge")
    errors = _candidate_common_errors(record, command)
    if record.get("source_sequence") != [5, 6, 3, 11]:
        errors.append("source_sequence_changed")
    if record.get("triangle_center_index") != 41:
        errors.append("triangle_center_index_must_be_41")
    if record.get("positions_from_center") != [46, 52, 55, 66]:
        errors.append("positions_from_center_changed")
    if record.get("position_52_reached_from_center") is not True:
        errors.append("position_52_reached_from_center_must_be_true")
    return _result(command, errors)


def validate_stage5dn_disk_p39_row1_cluster() -> ValidationResult:
    command = "validate-stage5dn-disk-p39-row1-cluster"
    record = _read_record("disk_p39_row1_math_semantic_cluster")
    errors = _candidate_common_errors(record, command)
    expected = {
        "EULER",
        "LEONHARD",
        "NAPIER",
        "JOHN",
        "TOTIENT",
        "CIRCUMFERENCE",
        "PRIME_NUMBER",
        "FISH",
        "WYNN",
        "PHI",
    }
    if set(record.get("terms_claimed", [])) != expected:
        errors.append("terms_claimed_changed")
    if record.get("accepted_as_decryption") is not False:
        errors.append("accepted_as_decryption_must_be_false")
    return _result(command, errors)


def validate_stage5dn_doublet_suppression() -> ValidationResult:
    command = "validate-stage5dn-doublet-suppression"
    record = _read_record("disk_doublet_suppression_candidate")
    errors = _candidate_common_errors(record, command)
    if record.get("claimed_expected_doublets") != 448:
        errors.append("claimed_expected_doublets_changed")
    if record.get("claimed_observed_doublets") != 89:
        errors.append("claimed_observed_doublets_changed")
    if record.get("probability_claim_accepted_as_validated") is not False:
        errors.append("probability_claim_accepted_as_validated_must_be_false")
    return _result(command, errors)


def validate_stage5dn_probability_quarantine() -> ValidationResult:
    command = "validate-stage5dn-probability-quarantine"
    record = _read_record("disk_probability_claim_quarantine")
    errors = _candidate_common_errors(record, command)
    if record.get("probability_claims_present") is not True:
        errors.append("probability_claims_present_must_be_true")
    if record.get("probability_claim_accepted_as_validated") is not False:
        errors.append("probability_claim_accepted_as_validated_must_be_false")
    return _result(command, errors)


def validate_stage5dn_circumference_precedent() -> ValidationResult:
    command = "validate-stage5dn-circumference-precedent"
    precedent = _read_record("solved_i_voice_of_circumference_precedent")
    crosslink = _read_record("circumference_single_i_spiral_anchor_crosslink")
    errors = _candidate_common_errors(precedent, command)
    errors.extend(_candidate_common_errors(crosslink, f"{command}:crosslink"))
    if precedent.get("source_section_id") != "0.4.0":
        errors.append("source_section_id_changed")
    if precedent.get("plaintext_quote") != "THE I IS THE VOICE OF THE CIRCUMFERENCE":
        errors.append("plaintext_quote_changed")
    if precedent.get("used_for_decryption_now") is not False:
        errors.append("used_for_decryption_now_must_be_false")
    for flag in [
        "not_a_mapping_claim",
        "not_claiming_i_equals_wynn",
        "not_claiming_i_equals_triangle_center",
        "not_claiming_plain_i_maps_to_single_rune_anchor",
    ]:
        if crosslink.get(flag) is not True:
            errors.append(f"{flag}_must_be_true")
    return _result(command, errors)


def validate_stage5dn_pdd_triangle_56311_update() -> ValidationResult:
    command = "validate-stage5dn-pdd-triangle-56311-update"
    record = _read_record("pdd_153_triangle_56311_wynn_way_route")
    errors = _candidate_common_errors(record, command)
    if record.get("stage5dl_record_preserved") is not True:
        errors.append("stage5dl_record_preserved_must_be_true")
    if record.get("stage5dn_disk_v1_support_added") is not True:
        errors.append("stage5dn_disk_v1_support_added_must_be_true")
    if record.get("selected_now") is not False:
        errors.append("selected_now_must_be_false")
    return _result(command, errors)


def validate_stage5dn_stage5dm_preservation() -> ValidationResult:
    command = "validate-stage5dn-stage5dm-preservation"
    record = _read_record("stage5dm_preservation")
    errors = _common_errors(record, command)
    if record.get("stage5dm_preserved") is not True:
        errors.append("stage5dm_preserved_must_be_true")
    if validate_stage5dm().validation_error_count:
        errors.append("stage5dm_validation_failed")
    return _result(command, errors)


def validate_stage5dn_stage5bd_preservation() -> ValidationResult:
    command = "validate-stage5dn-stage5bd-preservation"
    record = _read_record("stage5bd_preservation")
    errors = _common_errors(record, command)
    if record.get("stage5bd_run_plan_id_count") != 10:
        errors.append("stage5bd_run_plan_id_count_must_be_10")
    return _result(command, errors)


def validate_stage5dn_active_lineage_preservation() -> ValidationResult:
    command = "validate-stage5dn-active-lineage-preservation"
    record = _read_record("active_lineage_preservation")
    errors = _common_errors(record, command)
    if record.get("active_lineage_record_count") != len(ACTIVE_LINEAGE_PATHS):
        errors.append("active_lineage_record_count_changed")
    return _result(command, errors)


def validate_stage5dn_sidecar_gates() -> ValidationResult:
    command = "validate-stage5dn-sidecar-gates"
    errors: list[str] = []
    for key in [
        "no_active_ingestion_proof",
        "no_byte_stream_transition_gate",
        "no_execution_transition_gate",
    ]:
        errors.extend(_common_errors(_read_record(key), f"{command}:{key}"))
    return _result(command, errors)


def validate_stage5dn_handoff_continuity() -> ValidationResult:
    command = "validate-stage5dn-handoff-continuity"
    record = _read_record("codex_handoff_policy")
    errors = _common_errors(record, command)
    if record.get("canonical_codex_handoff_root") != "codex-output":
        errors.append("canonical_codex_handoff_root_changed")
    if DEPRECATED_CODEX_OUTPUT.exists():
        errors.append("deprecated_codex_output_path_exists")
    return _result(command, errors)


def validate_stage5dn_governance_scope() -> ValidationResult:
    command = "validate-stage5dn-governance-scope"
    record = _read_record("governance_scope_control")
    errors = _common_errors(record, command)
    if record.get("scope_control_status") != "all_stage5dn_operational_gates_closed":
        errors.append("scope_control_status_changed")
    if record.get("target_selected") is not False:
        errors.append("target_selected_must_be_false")
    return _result(command, errors)


def validate_stage5dn() -> ValidationResult:
    command = "validate-stage5dn"
    errors: list[str] = []
    for key in DATA_PATHS:
        errors.extend(_schema_errors(key))
        if DATA_PATHS[key].exists():
            errors.extend(_common_errors(_read_record(key), key))
    for validator in [
        validate_stage5dn_disk_source_lock,
        validate_stage5dn_results_png,
        validate_stage5dn_message_bodies,
        validate_stage5dn_disk_56311_wynn_way,
        validate_stage5dn_disk_p39_row1_cluster,
        validate_stage5dn_doublet_suppression,
        validate_stage5dn_probability_quarantine,
        validate_stage5dn_circumference_precedent,
        validate_stage5dn_pdd_triangle_56311_update,
        validate_stage5dn_stage5dm_preservation,
        validate_stage5dn_stage5bd_preservation,
        validate_stage5dn_active_lineage_preservation,
        validate_stage5dn_sidecar_gates,
        validate_stage5dn_handoff_continuity,
        validate_stage5dn_governance_scope,
    ]:
        result = validator()
        errors.extend(f"{result.command}:{error}" for error in result.errors)
    return _result(command, errors)


def load_stage5dn_summary() -> dict[str, Any]:
    return _read_record("summary")


def stage5dn_summary_text() -> str:
    summary = load_stage5dn_summary()
    lines = [
        f"stage_id={summary.get('stage_id')}",
        f"status={summary.get('status')}",
        f"disk_cipher_v1_source_lock_created={str(summary.get('disk_cipher_v1_source_lock_created')).lower()}",
        f"disk_cipher_stuff_file_count={summary.get('disk_cipher_stuff_file_count')}",
        f"disk_results_png_source_locked={str(summary.get('disk_results_png_source_locked')).lower()}",
        f"updated_disk_message_bodies_source_locked={str(summary.get('updated_disk_message_bodies_source_locked')).lower()}",
        f"disk_p39_row1_math_semantic_cluster_v1_created={str(summary.get('disk_p39_row1_math_semantic_cluster_v1_created')).lower()}",
        f"disk_56311_wynn_way_bridge_v1_created={str(summary.get('disk_56311_wynn_way_bridge_v1_created')).lower()}",
        f"solved_i_voice_of_circumference_precedent_created={str(summary.get('solved_i_voice_of_circumference_precedent_created')).lower()}",
        f"disk_probability_claim_quarantine_v1_created={str(summary.get('disk_probability_claim_quarantine_v1_created')).lower()}",
        f"pdd_153_triangle_56311_wynn_way_route_v1_updated={str(summary.get('pdd_153_triangle_56311_wynn_way_route_v1_updated')).lower()}",
        f"target_selected={str(summary.get('pivot_target_selected_now')).lower()}",
        f"execution_authorized_now={str(summary.get('execution_authorized_now')).lower()}",
        f"html_tool_executed_now={str(summary.get('html_tool_executed_now')).lower()}",
        f"ocr_performed={str(summary.get('ocr_performed')).lower()}",
        f"image_forensics_performed={str(summary.get('image_forensics_performed')).lower()}",
        f"stage5bd_run_plan_id_count={summary.get('stage5bd_run_plan_id_count')}",
        f"active_lineage_record_count={summary.get('active_lineage_record_count')}",
        f"parallel_worker_cap_for_stage5dn_and_later={summary.get('parallel_worker_cap_for_stage5dn_and_later')}",
        f"recommended_next_stage_id={summary.get('recommended_next_stage_id')}",
    ]
    return "\n".join(lines)


__all__ = [
    "CODEX_COMPLETION_PATH",
    "DATA_PATHS",
    "RESULTS_DIR",
    "SCHEMA_PATHS",
    "STAGE_ID",
    "STAGE_TITLE",
    "build_stage5dn",
    "load_stage5dn_summary",
    "stage5dn_summary_text",
    "validate_stage5dn",
    "validate_stage5dn_active_lineage_preservation",
    "validate_stage5dn_circumference_precedent",
    "validate_stage5dn_disk_56311_wynn_way",
    "validate_stage5dn_disk_p39_row1_cluster",
    "validate_stage5dn_disk_source_lock",
    "validate_stage5dn_doublet_suppression",
    "validate_stage5dn_governance_scope",
    "validate_stage5dn_handoff_continuity",
    "validate_stage5dn_message_bodies",
    "validate_stage5dn_pdd_triangle_56311_update",
    "validate_stage5dn_probability_quarantine",
    "validate_stage5dn_results_png",
    "validate_stage5dn_sidecar_gates",
    "validate_stage5dn_stage5bd_preservation",
    "validate_stage5dn_stage5dm_preservation",
]
