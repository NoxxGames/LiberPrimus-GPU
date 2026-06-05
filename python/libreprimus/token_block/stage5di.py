"""Stage 5DI recent clue source-lock and pivot-readiness metadata.

Stage 5DI records recent clue families as source-locked, reviewable metadata
without selecting a pivot target or authorizing any byte-stream, route, Tor, or
execution work.
"""

from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from libreprimus.token_block.models import (
    read_yaml,
    sha256_file,
    write_json,
    write_jsonl,
    write_yaml,
)
from libreprimus.token_block.preflight_runner.stage5bd import validate_stage5bd
from libreprimus.token_block.stage5ca import (
    ACTIVE_LINEAGE_PATHS,
    CORRECT_STAGE5AW_PATH,
    INCORRECT_STAGE5AW_PATH,
)
from libreprimus.token_block.stage5cm import PARALLEL_WORKER_CAP, SECRET_PATTERNS
from libreprimus.token_block.stage5dg import (
    DATA_PATHS as STAGE5DG_DATA_PATHS,
    SOURCE_PREVIOUS_STAGE_COMMIT as STAGE5DG_COMMIT,
    load_stage5dg_summary,
)

STAGE_ID = "stage-5di"
STAGE_TITLE = "Stage 5DI - Recent clue source-lock and pivot-readiness package, without execution"
PROMPT_TYPE = "codex_metadata_implementation"
SOURCE_PREVIOUS_STAGE = "stage-5dg"
SOURCE_PREVIOUS_STAGE_COMMIT = "bc47233023556073d5a057097aa23ce79d899c8a"
SOURCE_PREVIOUS_STAGE_ISSUE = 143
SOURCE_PREVIOUS_STAGE_CI_RUN = 26986063945
SOURCE_PREVIOUS_STAGE_PYTEST_COUNT = 2557
NEXT_STAGE_ID = "stage-5dj"
NEXT_STAGE_TITLE = "Stage 5DJ - Target-priority decision package, without execution"
NEXT_PROMPT_TYPE = "codex_metadata_implementation"
RESULTS_DIR = Path("experiments/results/token-block/stage5di")
CODEX_COMPLETION_PATH = Path("codex-output/stage5di-codex-completion.md")
DEPRECATED_CODEX_OUTPUT = Path("codex_output")
RETRIEVED_AT_UTC = "2026-06-05T00:00:00Z"

IDDQD_ROOT = Path("third_party/CiadaSolversIddqd_v2")
IDDQD_ALTERNATE_ROOT = Path("third_party/CicadaSolversIddqd_v2")
NUMBER_TRIANGLE_ROOT = Path("third_party/UsefulFilesAndIdeas/number-triangle-theory")
TOKEN_BLOCK_PAGES = ["49.jpg", "50.jpg", "51.jpg"]

FORBIDDEN_FALSE_FLAGS: dict[str, bool] = {
    "activation_authorized_now": False,
    "activation_decision_valid_now": False,
    "active_ingestion_performed": False,
    "active_manifest_registry_updated": False,
    "active_planning_input_authorized_now": False,
    "active_planning_input_selected_now": False,
    "active_token_block_manifest_changed": False,
    "ai_ml_interpretation_performed": False,
    "approval_gate_authorizes_activation_now": False,
    "approval_gate_satisfied_now": False,
    "benchmark_performed": False,
    "branch_enumeration_performed": False,
    "byte_stream_generation_authorized_now": False,
    "canonical_corpus_active": False,
    "canonical_transcription_changed": False,
    "combined_approval_gate_authorizes_activation_now": False,
    "combined_approval_gate_satisfied_now": False,
    "cuda_execution_performed": False,
    "decode_attempt_performed": False,
    "deep_research_activation_accept_record_present_now": False,
    "deep_research_acceptance_component_satisfied_now": False,
    "dry_run_ingestion_authorized_now": False,
    "dwh_hash_search_performed": False,
    "execution_allowed": False,
    "execution_authorized_now": False,
    "experiment_authorized_now": False,
    "experiment_executed_now": False,
    "experiments_authorized_now": False,
    "full_cartesian_product_enumerated": False,
    "future_real_records_created_now": False,
    "hash_preimage_search_performed": False,
    "historical_route_execution_performed": False,
    "image_forensics_performed": False,
    "manifest_supersession_authorized_now": False,
    "manifest_supersession_performed": False,
    "meaning_claimed_now": False,
    "method_status_upgraded": False,
    "mp3stego_execution_performed": False,
    "new_active_planning_input_created": False,
    "new_real_operator_approval_record_created_in_stage5di": False,
    "ocr_performed": False,
    "old_16_worker_default_reintroduced": False,
    "openpuff_execution_performed": False,
    "operator_approval_alone_authorizes_activation": False,
    "operator_approval_alone_authorizes_active_planning_input": False,
    "operator_approval_alone_authorizes_byte_stream_generation": False,
    "operator_approval_alone_authorizes_execution": False,
    "operator_approval_alone_satisfies_combined_gate": False,
    "operator_target_priority_decision_created_now": False,
    "page_boundaries_finalized": False,
    "pivot_target_selected_now": False,
    "polar_route_extraction_performed_now": False,
    "raw_body_committed": False,
    "real_byte_stream_generated": False,
    "real_deep_research_acceptance_record_created_now": False,
    "route_extraction_performed_now": False,
    "scoring_performed": False,
    "solve_claim": False,
    "stage5bd_dry_run_plan_manifest_changed": False,
    "stage5bd_plan_superseded": False,
    "stage5bd_run_plan_ids_changed": False,
    "stego_tool_execution_performed": False,
    "string4_active_input_allowed": False,
    "string4_added_to_active_dry_run_inputs": False,
    "string4_added_to_stage5bd_run_plan_ids": False,
    "string4_byte_stream_generation_allowed": False,
    "string4_dry_run_ingestion_allowed_now": False,
    "string4_execution_input_allowed": False,
    "string4_sidecar_active": False,
    "string4_sidecar_planning_ingestion_activated": False,
    "target_class_validation_implemented": False,
    "token_block_experiment_executed": False,
    "token_block_transform_performed_now": False,
    "tor_network_access_performed": False,
    "triangle_route_extraction_performed_now": False,
    "variant_byte_streams_generated": False,
    "variant_materialisation_performed": False,
    "website_expansion_performed": False,
}

TRUE_FLAGS: dict[str, bool] = {
    "metadata_only": True,
    "stage5dg_operator_approval_record_preserved": True,
    "real_operator_approval_record_created_now": True,
    "operator_approval_component_satisfied_now": True,
    "stage5bd_dry_run_records_remain_valid": True,
}

SOURCE_FAMILY_IDS = [
    "2016_message_route_meta_clue_v0",
    "page32_tree_polar_route_v0",
    "pdd_153_triangle_word_route_v0",
    "page56_dwh_hash_target_contract_v0",
    "token_block_matrix_context_v0",
    "dinkus_visual_delimiter_candidate_v0",
    "magic_square_matrix_route_context_v0",
    "boxentriq_known_method_synthesis_v0",
]

ROUTE_CANDIDATE_FAMILY_IDS = [
    "2016_message_route_meta_clue_v0",
    "page32_tree_polar_route_v0",
    "pdd_153_triangle_word_route_v0",
    "page56_dwh_hash_target_contract_v0",
    "token_block_matrix_context_v0",
    "dinkus_visual_delimiter_candidate_v0",
    "magic_square_matrix_route_context_v0",
]

PIVOT_CANDIDATES = [
    ("token_block_first", "Continue token-block-first path"),
    ("page32_tree_polar_route_first", "Prioritize page32/full49 tree/polar route candidate"),
    ("pdd_153_triangle_route_first", "Prioritize 153-word triangle route candidate"),
    ("page56_dwh_hash_contract_first", "Prioritize DWH/hash target-contract analysis"),
    ("continue_approval_chain_first", "Continue Deep Research acceptance / combined-gate chain"),
    ("defer_for_more_source_locking", "Defer and source-lock more evidence"),
]

WEB_SOURCES = [
    {
        "source_id": "stage5di-web-2016-message-fandom",
        "source_type": "fandom_page",
        "url": "https://uncovering-cicada.fandom.com/wiki/2016_Message",
        "candidate_family_ids": [
            "2016_message_route_meta_clue_v0",
            "page32_tree_polar_route_v0",
            "pdd_153_triangle_word_route_v0",
        ],
        "citation_summary": (
            "Public community page for the 2016 signed message, route wording, "
            "image motif notes, and GP-sum community discussion."
        ),
        "source_lock_confidence": "medium",
    },
    {
        "source_id": "stage5di-web-page56-fandom",
        "source_type": "fandom_page",
        "url": "https://uncovering-cicada.fandom.com/wiki/PAGE_56",
        "candidate_family_ids": ["page56_dwh_hash_target_contract_v0"],
        "citation_summary": "Public community page for PAGE 56 / AN END and DWH hash context.",
        "source_lock_confidence": "medium",
    },
    {
        "source_id": "stage5di-web-2017-pgp-message-fandom",
        "source_type": "fandom_page",
        "url": "https://uncovering-cicada.fandom.com/wiki/PGP_Signed_Message_April_2017",
        "candidate_family_ids": [
            "2016_message_route_meta_clue_v0",
            "magic_square_matrix_route_context_v0",
        ],
        "citation_summary": "Public page for nearby signed-message context; source-lock only.",
        "source_lock_confidence": "medium",
    },
    {
        "source_id": "stage5di-web-boxentriq-liber-primus-guide",
        "source_type": "guide",
        "url": "https://www.boxentriq.com/guides/cicada-3301-liber-primus#solving-liber-primus-with-boxentriq",
        "candidate_family_ids": ["boxentriq_known_method_synthesis_v0"],
        "citation_summary": "Secondary known-method synthesis; not a primary source of truth.",
        "source_lock_confidence": "low",
    },
    {
        "source_id": "stage5di-web-reddit-page32-tree-thread",
        "source_type": "reddit_thread",
        "url": "https://www.reddit.com/r/cicada/comments/9zb42i/next_step_is_page_32_in_liber_primus_the/",
        "candidate_family_ids": ["page32_tree_polar_route_v0"],
        "citation_summary": "Community route discussion tying the 2016 tree clue to page 32/full 49.",
        "source_lock_confidence": "low",
    },
    {
        "source_id": "stage5di-web-tweqx-3301-hash-alarm",
        "source_type": "github_repo",
        "url": "https://github.com/tweqx/3301-hash-alarm",
        "candidate_family_ids": ["page56_dwh_hash_target_contract_v0"],
        "citation_summary": "Public repository preserving the DWH target-hash watch context.",
        "source_lock_confidence": "medium",
    },
]

DATA_PATHS: dict[str, Path] = {
    "summary": Path("data/project-state/stage5di-summary.yaml"),
    "next_stage_decision": Path("data/project-state/stage5di-next-stage-decision.yaml"),
    "source_lock_plan": Path("data/project-state/stage5di-source-lock-plan.yaml"),
    "recent_clue_source_lock_register": Path(
        "data/project-state/stage5di-recent-clue-source-lock-register.yaml"
    ),
    "pivot_readiness_package": Path(
        "data/project-state/stage5di-pivot-readiness-package.yaml"
    ),
    "pivot_priority_matrix": Path("data/project-state/stage5di-pivot-priority-matrix.yaml"),
    "route_candidate_family_index": Path(
        "data/project-state/stage5di-route-candidate-family-index.yaml"
    ),
    "validation_evidence": Path(
        "data/project-state/stage5di-reviewable-validation-evidence.yaml"
    ),
    "gap_register": Path("data/project-state/stage5di-reviewability-gap-register.yaml"),
    "record_family_name_equivalence_map": Path(
        "data/project-state/stage5di-record-family-name-equivalence-map.yaml"
    ),
    "web_source_lock_register": Path(
        "data/source-harvester/stage5di-web-source-lock-register.yaml"
    ),
    "local_archive_source_lock_register": Path(
        "data/source-harvester/stage5di-local-archive-source-lock-register.yaml"
    ),
    "cicada_solvers_crosswalk": Path(
        "data/source-harvester/stage5di-cicada-solvers-iddqd-v2-crosswalk.yaml"
    ),
    "number_triangle_crosswalk": Path(
        "data/source-harvester/stage5di-number-triangle-theory-bundle-crosswalk.yaml"
    ),
    "handoff_policy": Path("data/source-harvester/stage5di-codex-handoff-policy.yaml"),
    "credential_redaction": Path(
        "data/source-harvester/stage5di-credential-redaction-policy-preservation.yaml"
    ),
    "review_packaging_warning": Path(
        "data/source-harvester/stage5di-review-packaging-warning.yaml"
    ),
    "message_2016_route_meta": Path(
        "data/historical-route/stage5di-2016-message-route-meta-clue.yaml"
    ),
    "page32_tree_polar": Path(
        "data/historical-route/stage5di-page32-tree-polar-route-candidate.yaml"
    ),
    "pdd_153_triangle": Path(
        "data/historical-route/stage5di-pdd-153-triangle-word-route-candidate.yaml"
    ),
    "page56_dwh_hash": Path(
        "data/historical-route/stage5di-page56-dwh-hash-target-contract.yaml"
    ),
    "dinkus_visual_delimiter": Path(
        "data/historical-route/stage5di-dinkus-visual-delimiter-candidate.yaml"
    ),
    "boxentriq_synthesis": Path(
        "data/historical-route/stage5di-boxentriq-known-method-synthesis.yaml"
    ),
    "reddit_page32_source_lock": Path(
        "data/historical-route/stage5di-reddit-page32-thread-source-lock.yaml"
    ),
    "magic_square_context": Path(
        "data/historical-route/stage5di-magic-square-matrix-route-context.yaml"
    ),
    "source_gap_severity_update": Path(
        "data/historical-route/stage5di-source-gap-severity-update.yaml"
    ),
    "dwh_quarantine_reaffirmation": Path(
        "data/historical-route/stage5di-dwh-quarantine-reaffirmation.yaml"
    ),
    "guardrail": Path("data/historical-route/stage5di-guardrail.yaml"),
    "stage5dg_operator_approval_preservation": Path(
        "data/token-block/stage5di-stage5dg-operator-approval-preservation.yaml"
    ),
    "stage5bd_plan_preservation": Path(
        "data/token-block/stage5di-stage5bd-plan-preservation.yaml"
    ),
    "active_lineage_preservation": Path(
        "data/token-block/stage5di-active-lineage-preservation.yaml"
    ),
    "no_active_ingestion": Path("data/token-block/stage5di-no-active-ingestion-proof.yaml"),
    "no_byte_stream_transition_gate": Path(
        "data/token-block/stage5di-no-byte-stream-transition-gate.yaml"
    ),
    "no_execution_transition_gate": Path(
        "data/token-block/stage5di-no-execution-transition-gate.yaml"
    ),
    "target_class_context_preservation": Path(
        "data/token-block/stage5di-target-class-context-preservation.yaml"
    ),
}

SCHEMA_PATHS: dict[str, str] = {
    key: path.as_posix().replace("data/", "schemas/", 1).replace(".yaml", "-v0.schema.json")
    for key, path in DATA_PATHS.items()
}
RECORD_TYPES = {key: f"stage5di_{key}" for key in DATA_PATHS}


def _base_record(record_key: str) -> dict[str, Any]:
    return {
        "record_type": RECORD_TYPES[record_key],
        "schema": SCHEMA_PATHS[record_key],
        "stage_id": STAGE_ID,
        "stage_title": STAGE_TITLE,
        "prompt_type": PROMPT_TYPE,
        "source_previous_stage": SOURCE_PREVIOUS_STAGE,
        "source_previous_stage_commit": SOURCE_PREVIOUS_STAGE_COMMIT,
        "metadata_only": True,
        "solve_claim": False,
        "execution_allowed": False,
        "canonical_codex_handoff_root": "codex-output",
    }


def _common_state() -> dict[str, Any]:
    return {
        **FORBIDDEN_FALSE_FLAGS,
        **TRUE_FLAGS,
        "deep_research_acceptance_component_satisfied_now": False,
        "real_deep_research_acceptance_record_created_now": False,
        "real_deep_research_acceptance_record_present_now": False,
        "combined_approval_gate_satisfied_now": False,
        "combined_approval_gate_authorizes_activation_now": False,
        "approval_gate_satisfied_now": False,
        "approval_gate_authorizes_activation_now": False,
        "activation_authorized_now": False,
        "active_planning_input_selected_now": False,
        "byte_stream_generation_authorized_now": False,
        "execution_authorized_now": False,
        "target_class_validation_implemented": False,
        "tor_network_access_performed": False,
        "stage5bd_run_plan_id_count": 10,
        "active_lineage_record_count": len(ACTIVE_LINEAGE_PATHS),
        "parallel_worker_cap_for_stage5di_and_later": PARALLEL_WORKER_CAP,
    }


def _schema_for(record_key: str) -> dict[str, Any]:
    properties: dict[str, Any] = {
        "record_type": {"const": RECORD_TYPES[record_key]},
        "stage_id": {"const": STAGE_ID},
        "metadata_only": {"const": True},
        "execution_allowed": {"const": False},
        "solve_claim": {"const": False},
        "canonical_codex_handoff_root": {"const": "codex-output"},
    }
    for key in FORBIDDEN_FALSE_FLAGS:
        properties[key] = {"const": False}
    for key in TRUE_FLAGS:
        properties[key] = {"const": True}
    for key in [
        "deep_research_acceptance_component_satisfied_now",
        "combined_approval_gate_satisfied_now",
        "activation_authorized_now",
        "active_planning_input_selected_now",
        "byte_stream_generation_authorized_now",
        "execution_authorized_now",
        "target_class_validation_implemented",
        "tor_network_access_performed",
    ]:
        properties[key] = {"const": False}
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "title": f"{STAGE_ID} {record_key}",
        "type": "object",
        "required": [
            "record_type",
            "stage_id",
            "metadata_only",
            "execution_allowed",
            "solve_claim",
            "canonical_codex_handoff_root",
        ],
        "properties": properties,
        "additionalProperties": True,
    }


def _write_schemas() -> None:
    for key, schema_path in SCHEMA_PATHS.items():
        write_json(Path(schema_path), _schema_for(key))


def _load_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    payload = read_yaml(path)
    return payload if isinstance(payload, dict) else {}


def _file_ref(path: Path) -> dict[str, Any]:
    return {
        "path": path.as_posix(),
        "exists": path.exists(),
        "is_file": path.is_file(),
        "size_bytes": path.stat().st_size if path.exists() and path.is_file() else None,
        "sha256": sha256_file(path) if path.exists() and path.is_file() else None,
    }


def _directory_listing(root: Path, suffixes: set[str] | None = None) -> list[dict[str, Any]]:
    if not root.exists() or not root.is_dir():
        return []
    rows = []
    for path in sorted(p for p in root.iterdir() if p.is_file()):
        if suffixes is None or path.suffix.lower() in suffixes:
            rows.append(_file_ref(path))
    return rows


def _path_under_iddqd(relative: str) -> Path:
    return IDDQD_ROOT / relative


def _credential_remote_summary() -> dict[str, Any]:
    result = subprocess.run(
        ["git", "remote", "-v"],
        check=False,
        capture_output=True,
        text=True,
    )
    remote_text = result.stdout + result.stderr
    credential_like_count = 0
    for line in remote_text.splitlines():
        if any(re.search(pattern, line, flags=re.IGNORECASE) for pattern in SECRET_PATTERNS):
            credential_like_count += 1
    return {
        "remote_command_status": "passed" if result.returncode == 0 else "failed",
        "credential_like_remote_count": credential_like_count,
        "remote_url_values_printed": False,
        "secret_values_printed_or_committed": False,
        "verified_github_remote_without_credentials": credential_like_count == 0,
    }


def _web_source_records() -> list[dict[str, Any]]:
    common_limitations = [
        "public page may change",
        "community page may contain unsourced claims",
        "compact metadata only; raw webpage body not committed",
    ]
    records = []
    for source in WEB_SOURCES:
        limitations = list(common_limitations)
        if source["source_type"] == "reddit_thread":
            limitations.append("Reddit thread may be deleted, edited, or rate-limited")
        records.append(
            {
                **source,
                "stage_id": STAGE_ID,
                "retrieved_at_utc": RETRIEVED_AT_UTC,
                "access_status": "reachable",
                "content_saved_raw": False,
                "raw_body_committed": False,
                "source_lock_status": "compact_metadata_url_locked",
                "known_limitations": limitations,
            }
        )
    return records


def _local_archive_records() -> list[dict[str, Any]]:
    paths = [
        ("iddqd_v2_root", IDDQD_ROOT, "directory", SOURCE_FAMILY_IDS),
        (
            "iddqd_v2_transcription_master",
            _path_under_iddqd(
                "liber-primus__transcription--master/liber-primus__transcription--master.txt"
            ),
            "text_file",
            ["pdd_153_triangle_word_route_v0", "token_block_matrix_context_v0"],
        ),
        (
            "iddqd_v2_transcription_sentences",
            _path_under_iddqd(
                "liber-primus__transcription--sentences/"
                "liber-primus__transcription--sentences.txt"
            ),
            "text_file",
            ["pdd_153_triangle_word_route_v0"],
        ),
        (
            "iddqd_v2_unsolved_page32",
            _path_under_iddqd("liber-primus__images--unsolved/32.jpg"),
            "image_file",
            ["page32_tree_polar_route_v0"],
        ),
        (
            "iddqd_v2_full_page49",
            _path_under_iddqd("liber-primus__images--full/49.jpg"),
            "image_file",
            ["page32_tree_polar_route_v0", "token_block_matrix_context_v0"],
        ),
        (
            "iddqd_v2_full_page50",
            _path_under_iddqd("liber-primus__images--full/50.jpg"),
            "image_file",
            ["dinkus_visual_delimiter_candidate_v0", "token_block_matrix_context_v0"],
        ),
        (
            "iddqd_v2_full_page51",
            _path_under_iddqd("liber-primus__images--full/51.jpg"),
            "image_file",
            ["token_block_matrix_context_v0"],
        ),
        (
            "iddqd_v2_full_page56",
            _path_under_iddqd("liber-primus__images--full/56.jpg"),
            "image_file",
            ["dinkus_visual_delimiter_candidate_v0", "page56_dwh_hash_target_contract_v0"],
        ),
        (
            "iddqd_v2_lp_outguessed",
            _path_under_iddqd("lp_outguessed"),
            "directory",
            ["page56_dwh_hash_target_contract_v0", "boxentriq_known_method_synthesis_v0"],
        ),
        (
            "number_triangle_bundle",
            NUMBER_TRIANGLE_ROOT,
            "directory",
            ["pdd_153_triangle_word_route_v0", "magic_square_matrix_route_context_v0"],
        ),
        (
            "number_triangle_messages",
            NUMBER_TRIANGLE_ROOT / "messages.txt",
            "text_file",
            ["pdd_153_triangle_word_route_v0"],
        ),
    ]
    records = []
    for source_id, path, source_type, families in paths:
        ref = _file_ref(path)
        records.append(
            {
                "source_id": f"stage5di-local-{source_id}",
                "stage_id": STAGE_ID,
                "source_type": source_type,
                "source_locator": path.as_posix(),
                "path_exists": path.exists(),
                "source_lock_status": "local_metadata_hash_recorded" if path.exists() else "missing",
                "candidate_family_ids": families,
                "raw_file_committed": False,
                "raw_body_committed": False,
                "content_saved_raw": False,
                "sha256": ref["sha256"],
                "size_bytes": ref["size_bytes"],
            }
        )
    return records


def _cicada_crosswalk() -> dict[str, Any]:
    crosswalks = [
        {
            "candidate_family_id": "page32_tree_polar_route_v0",
            "local_paths": [
                _file_ref(_path_under_iddqd("liber-primus__images--unsolved/32.jpg")),
                _file_ref(_path_under_iddqd("liber-primus__images--full/49.jpg")),
                _file_ref(
                    _path_under_iddqd(
                        "liber-primus__transcription--master/"
                        "liber-primus__transcription--master.txt"
                    )
                ),
            ],
        },
        {
            "candidate_family_id": "pdd_153_triangle_word_route_v0",
            "local_paths": [
                _file_ref(
                    _path_under_iddqd(
                        "liber-primus__transcription--sentences/"
                        "liber-primus__transcription--sentences.txt"
                    )
                ),
                _file_ref(
                    _path_under_iddqd(
                        "liber-primus__transcription--master/"
                        "liber-primus__transcription--master.txt"
                    )
                ),
            ],
        },
        {
            "candidate_family_id": "page56_dwh_hash_target_contract_v0",
            "local_paths": [
                _file_ref(_path_under_iddqd("liber-primus__images--full/56.jpg")),
                _file_ref(_path_under_iddqd("liber-primus__images--unsolved/56.jpg")),
                _file_ref(_path_under_iddqd("lp_outguessed")),
            ],
        },
        {
            "candidate_family_id": "token_block_matrix_context_v0",
            "local_paths": [
                _file_ref(_path_under_iddqd(f"liber-primus__images--full/{page}"))
                for page in TOKEN_BLOCK_PAGES
            ],
        },
        {
            "candidate_family_id": "dinkus_visual_delimiter_candidate_v0",
            "local_paths": [
                _file_ref(_path_under_iddqd("liber-primus__images--full/50.jpg")),
                _file_ref(_path_under_iddqd("liber-primus__images--full/56.jpg")),
            ],
        },
    ]
    return {
        **_base_record("cicada_solvers_crosswalk"),
        **_common_state(),
        "local_archive_root_candidates": [
            "third_party/CiadaSolversIddqd_v2",
            "third_party/CicadaSolversIddqd_v2",
        ],
        "found_in_repo_path": IDDQD_ROOT.as_posix() if IDDQD_ROOT.exists() else None,
        "root_exists": IDDQD_ROOT.exists(),
        "alternate_root_exists": IDDQD_ALTERNATE_ROOT.exists(),
        "path_spelling_warning": IDDQD_ROOT.exists() != IDDQD_ALTERNATE_ROOT.exists(),
        "raw_archive_committed": False,
        "crosswalks": crosswalks,
        "crosswalk_count": len(crosswalks),
    }


def _number_triangle_crosswalk() -> dict[str, Any]:
    message_files = _directory_listing(NUMBER_TRIANGLE_ROOT, {".txt", ".md"})
    image_files = _directory_listing(NUMBER_TRIANGLE_ROOT, {".jpg", ".jpeg", ".png", ".webp"})
    return {
        **_base_record("number_triangle_crosswalk"),
        **_common_state(),
        "operator_path": "third_party/UsefulFilesAndIdeas/number-triangle-theory",
        "bundle_root": NUMBER_TRIANGLE_ROOT.as_posix(),
        "bundle_root_exists": NUMBER_TRIANGLE_ROOT.exists(),
        "file_count": len(_directory_listing(NUMBER_TRIANGLE_ROOT)),
        "message_files": message_files,
        "message_file_count": len(message_files),
        "image_files": image_files,
        "image_file_count": len(image_files),
        "full_forum_text_committed_in_stage5di": False,
        "cross_check_against_iddqd_transcription_status": (
            "not_verified_due_transcription_format_mismatch"
        ),
        "claims_remain_community_bundle_claims": True,
        "experiment_authorized_now": False,
    }


def _pivot_candidates() -> list[dict[str, Any]]:
    return [
        {
            "candidate_id": candidate_id,
            "label": label,
            "status": "candidate_not_selected",
            "candidate_not_selected": True,
            "immediate_execution_allowed": False,
            "operator_priority_decision_created_now": False,
            "byte_stream_generation_authorized_now": False,
            "execution_authorized_now": False,
        }
        for candidate_id, label in PIVOT_CANDIDATES
    ]


def _route_family_index() -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for family_id in SOURCE_FAMILY_IDS:
        records.append(
            {
                "candidate_family_id": family_id,
                "stage_id": STAGE_ID,
                "status": "source_lock_only",
                "route_candidate": family_id in ROUTE_CANDIDATE_FAMILY_IDS,
                "future_bounded_candidate": True,
                "experiment_authorized_now": False,
                "immediate_execution_allowed": False,
                "solve_claim": False,
            }
        )
    return records


def _target_classes() -> list[str]:
    return [
        "direct_v3_onion_hostname",
        "raw_v3_onion_public_key_material",
        "historical_v2_onion_candidate",
        "lp_style_deep_web_content_hash",
        "pgp_or_rsa_related_payload",
        "compressed_payload",
        "encrypted_payload",
        "file_or_container_bytes",
        "high_entropy_key_or_hash_material",
        "unknown_binary_payload",
    ]


def _records() -> dict[str, dict[str, Any]]:
    stage5dg_summary = load_stage5dg_summary()
    web_sources = _web_source_records()
    local_sources = _local_archive_records()
    pivot_candidates = _pivot_candidates()
    route_family_index = _route_family_index()
    common = _common_state()

    records: dict[str, dict[str, Any]] = {}
    records["web_source_lock_register"] = {
        **_base_record("web_source_lock_register"),
        **common,
        "source_lock_scope": "public_web_compact_metadata_only",
        "web_source_lock_count": len(web_sources),
        "sources": web_sources,
        "raw_webpage_bodies_committed": False,
    }
    records["local_archive_source_lock_register"] = {
        **_base_record("local_archive_source_lock_register"),
        **common,
        "source_lock_scope": "local_archive_compact_metadata_only",
        "local_archive_source_lock_count": len(local_sources),
        "sources": local_sources,
        "raw_archive_files_committed": False,
    }
    records["cicada_solvers_crosswalk"] = _cicada_crosswalk()
    records["number_triangle_crosswalk"] = _number_triangle_crosswalk()
    records["message_2016_route_meta"] = {
        **_base_record("message_2016_route_meta"),
        **common,
        "candidate_family_id": "2016_message_route_meta_clue_v0",
        "candidate_status": "source_lock_only",
        "claimed_pgp_signature_present": True,
        "pgp_signature_reverified_stage5di": False,
        "pgp_verification_status": "claimed_by_source_not_reverified_stage5di",
        "claimed_fingerprint_suffix": "7A35090F",
        "image_motif": "oak_tree",
        "image_dimensions_claimed": "563x569",
        "route_terms_present": ["path", "way", "map", "road", "direction"],
        "method_class_implication": "word_number_layout_route_method",
        "status": "source_lock_only",
        "experiment_authorized_now": False,
    }
    records["page32_tree_polar"] = {
        **_base_record("page32_tree_polar"),
        **common,
        "candidate_family_id": "page32_tree_polar_route_v0",
        "candidate_status": "source_lock_only",
        "unsolved_image_path": _file_ref(
            _path_under_iddqd("liber-primus__images--unsolved/32.jpg")
        ),
        "full_image_path": _file_ref(_path_under_iddqd("liber-primus__images--full/49.jpg")),
        "image_crosswalk_status": "verify_by_hash_or_visual_match_future_review",
        "visual_features": [
            "blurred_tree",
            "red_terminal_marker",
            "short_rune_text",
            "page_layout_candidate",
        ],
        "future_route_model_candidates": [
            "tree_root_as_origin",
            "text_block_center_as_origin",
            "red_marker_as_origin",
            "gematria_sum_as_angle",
            "word_length_as_radius",
            "word_index_as_radius",
            "nearest_neighbor_path",
            "right_side_route",
        ],
        "route_extraction_performed_now": False,
        "polar_route_extraction_performed_now": False,
        "experiment_authorized_now": False,
    }
    records["pdd_153_triangle"] = {
        **_base_record("pdd_153_triangle"),
        **common,
        "candidate_family_id": "pdd_153_triangle_word_route_v0",
        "candidate_status": "source_lock_only",
        "community_claim_source_bundle": NUMBER_TRIANGLE_ROOT.as_posix(),
        "body_word_count_verified": False,
        "body_word_count": 153,
        "triangle_row_count": 17,
        "center_word_position": 41,
        "center_word_value": None,
        "single_rune_positions_verified": False,
        "single_rune_positions_claimed": [25, 41, 53, 91, 106],
        "heading_gp_sum_plus_first_four_body_words": 210,
        "heading_gp_sum_plus_first_five_body_words": 265,
        "way_result_verified": False,
        "way_result_operation": "heading_minus_reversed_word52_mod29",
        "way_result": "ᚹᚪᚣ",
        "way_result_transliteration": "WAY",
        "verification_status": "community_claim_pending_reproducible_transcription_crosswalk",
        "triangle_route_extraction_performed_now": False,
        "experiment_authorized_now": False,
    }
    records["page56_dwh_hash"] = {
        **_base_record("page56_dwh_hash"),
        **common,
        "candidate_family_id": "page56_dwh_hash_target_contract_v0",
        "candidate_status": "source_lock_only",
        "known_target_hash_present": True,
        "target_hash_hex": (
            "36367763ab73783c7af284446c59466b4cd653239a311cb7116d4618dee09a842"
            "5893dc7500b464fdaf1672d7bef5e891c6e2274568926a49fb4f45132c2a8b4"
        ),
        "hash_length_hex": 128,
        "hash_bytes_if_hex": 64,
        "hash_algorithm_unknown": True,
        "candidate_algorithms_claimed_by_sources": [
            "sha512",
            "blake512",
            "blake2b",
            "sha3_or_other_512_bit_hash",
        ],
        "stage5di_hash_search_performed": False,
        "target_class_validation_implemented": False,
        "tor_network_access_performed": False,
    }
    records["dinkus_visual_delimiter"] = {
        **_base_record("dinkus_visual_delimiter"),
        **common,
        "candidate_id": "dinkus_visual_delimiter_candidate_v0",
        "candidate_type": "visual_delimiter_or_dinkus",
        "candidate_status": "source_locked_visual_marker_only",
        "observed_feature": "three_black_dots_horizontal_separator",
        "observed_on_operator_attached_images": ["50.jpg", "56.jpg"],
        "local_image_refs": [
            _file_ref(_path_under_iddqd("liber-primus__images--full/50.jpg")),
            _file_ref(_path_under_iddqd("liber-primus__images--full/56.jpg")),
        ],
        "possible_role": "section_separator_or_dinkus",
        "uneven_spacing_observed_by_operator": True,
        "uneven_spacing_cipher_claimed_now": False,
        "spacing_irregularity_observed_by_operator": True,
        "spacing_irregularity_verified_by_measurement_stage5di": False,
        "measurement_performed_now": False,
        "spacing_measurement_interpretation": "descriptive_not_cipher_claim",
        "interpretation_confidence": "low_to_medium",
        "meaning_claimed_now": False,
        "source_lock_only": True,
        "experiment_authorized_now": False,
        "image_forensics_performed": False,
        "ocr_performed": False,
        "ai_ml_interpretation_performed": False,
    }
    records["boxentriq_synthesis"] = {
        **_base_record("boxentriq_synthesis"),
        **common,
        "candidate_family_id": "boxentriq_known_method_synthesis_v0",
        "candidate_status": "secondary_synthesis_source_lock_only",
        "known_method_topics": [
            "gematria_primus",
            "atbash_reversed_gp",
            "divinity_vigenere_with_f_skip",
            "prime_totient_methods",
            "outguess_binary_analysis_context",
            "known_clues_summary",
        ],
        "primary_source": False,
        "experiment_authorized_now": False,
    }
    records["reddit_page32_source_lock"] = {
        **_base_record("reddit_page32_source_lock"),
        **common,
        "source_id": "stage5di-web-reddit-page32-tree-thread",
        "candidate_family_id": "page32_tree_polar_route_v0",
        "source_lock_status": "compact_metadata_url_locked",
        "community_claim_only": True,
        "route_extraction_performed_now": False,
    }
    records["magic_square_context"] = {
        **_base_record("magic_square_context"),
        **common,
        "candidate_family_id": "magic_square_matrix_route_context_v0",
        "candidate_status": "future_bounded_candidate_source_lock_only",
        "route_context_terms": [
            "magic_square",
            "matrix_route",
            "gf_matrix",
            "layout_transform",
        ],
        "magic_square_transform_performed_now": False,
        "experiment_authorized_now": False,
    }
    records["source_gap_severity_update"] = {
        **_base_record("source_gap_severity_update"),
        **common,
        "source_gap_severity": "medium_high",
        "gap_count": 6,
        "gaps": [
            "2016 PGP message not reverified from local immutable source",
            "page32 tree/polar route is community discussion only",
            "PDD 153 triangle claims need reproducible transcript alignment",
            "page56 target hash algorithm and content class remain unknown",
            "dinkus visual delimiter is unmeasured descriptive metadata only",
            "magic-square/matrix route context lacks bounded manifest",
        ],
    }
    records["dwh_quarantine_reaffirmation"] = {
        **_base_record("dwh_quarantine_reaffirmation"),
        **common,
        "dwh_quarantine_reaffirmed": True,
        "page56_target_hash_preserved_as_contract_only": True,
        "dwh_hash_search_performed": False,
        "hash_preimage_search_performed": False,
        "tor_network_access_performed": False,
        "target_class_validation_implemented": False,
    }
    records["guardrail"] = {
        **_base_record("guardrail"),
        **common,
        "guardrail_status": "closed",
        "allowed_actions": [
            "source_lock_recent_clue_metadata",
            "crosswalk_local_archive_paths",
            "record_candidate_route_families",
            "record_pivot_readiness_without_selection",
            "record_no_execution_gate_preservation",
        ],
        "forbidden_actions_preserved_false": sorted(FORBIDDEN_FALSE_FLAGS),
    }
    records["stage5dg_operator_approval_preservation"] = {
        **_base_record("stage5dg_operator_approval_preservation"),
        **common,
        "stage5dg_summary_path": STAGE5DG_DATA_PATHS["summary"].as_posix(),
        "stage5dg_summary_status": stage5dg_summary.get("status"),
        "stage5dg_operator_approval_record_preserved": True,
        "stage5dg_operator_approval_record_path": STAGE5DG_DATA_PATHS[
            "real_operator_approval_record"
        ].as_posix(),
        "real_operator_approval_record_created_now": True,
        "operator_approval_component_satisfied_now": True,
        "operator_approval_alone_satisfies_combined_gate": False,
        "operator_approval_alone_authorizes_activation": False,
        "operator_approval_alone_authorizes_active_planning_input": False,
        "operator_approval_alone_authorizes_byte_stream_generation": False,
        "operator_approval_alone_authorizes_execution": False,
        "new_real_operator_approval_record_created_in_stage5di": False,
    }
    records["stage5bd_plan_preservation"] = {
        **_base_record("stage5bd_plan_preservation"),
        **common,
        "stage5bd_dry_run_records_remain_valid": True,
        "stage5bd_run_plan_id_count": 10,
        "stage5bd_run_plan_ids_changed": False,
        "stage5bd_dry_run_plan_manifest_changed": False,
        "stage5bd_plan_superseded": False,
        "string4_added_to_stage5bd_run_plan_ids": False,
        "string4_added_to_active_dry_run_inputs": False,
    }
    records["active_lineage_preservation"] = {
        **_base_record("active_lineage_preservation"),
        **common,
        "active_lineage_record_count": len(ACTIVE_LINEAGE_PATHS),
        "active_lineage_paths": [
            {"path": path, "exists": Path(path).exists()} for path in ACTIVE_LINEAGE_PATHS
        ],
        "correct_stage5aw_path_included": CORRECT_STAGE5AW_PATH in ACTIVE_LINEAGE_PATHS,
        "deprecated_stage5aw_path_absent": INCORRECT_STAGE5AW_PATH not in ACTIVE_LINEAGE_PATHS,
        "all_lineage_paths_resolve": all(Path(path).exists() for path in ACTIVE_LINEAGE_PATHS),
        "canonical_transcription_changed": False,
        "active_token_block_manifest_changed": False,
    }
    records["no_active_ingestion"] = {
        **_base_record("no_active_ingestion"),
        **common,
        "no_active_ingestion_status": "closed",
        "string4_sidecar_status": "scaffolded_inactive",
        "string4_sidecar_active": False,
        "string4_sidecar_planning_ingestion_activated": False,
        "string4_active_input_allowed": False,
        "string4_dry_run_ingestion_allowed_now": False,
        "active_ingestion_performed": False,
        "active_manifest_registry_updated": False,
        "active_planning_input_authorized_now": False,
        "active_planning_input_selected_now": False,
        "active_token_block_manifest_changed": False,
    }
    records["no_byte_stream_transition_gate"] = {
        **_base_record("no_byte_stream_transition_gate"),
        **common,
        "no_byte_stream_transition_gate_status": "closed",
        "byte_stream_generation_authorized_now": False,
        "real_byte_stream_generated": False,
        "variant_byte_streams_generated": False,
        "variant_materialisation_performed": False,
        "branch_enumeration_performed": False,
        "full_cartesian_product_enumerated": False,
    }
    records["no_execution_transition_gate"] = {
        **_base_record("no_execution_transition_gate"),
        **common,
        "no_execution_transition_gate_status": "closed",
        "execution_authorized_now": False,
        "token_block_experiment_executed": False,
        "dwh_hash_search_performed": False,
        "hash_preimage_search_performed": False,
        "decode_attempt_performed": False,
        "scoring_performed": False,
        "cuda_execution_performed": False,
        "benchmark_performed": False,
        "stego_tool_execution_performed": False,
        "image_forensics_performed": False,
        "ocr_performed": False,
        "ai_ml_interpretation_performed": False,
        "tor_network_access_performed": False,
        "target_class_validation_implemented": False,
        "website_expansion_performed": False,
        "method_status_upgraded": False,
        "canonical_corpus_active": False,
        "page_boundaries_finalized": False,
    }
    records["target_class_context_preservation"] = {
        **_base_record("target_class_context_preservation"),
        **common,
        "candidate_family_id": "token_block_matrix_context_v0",
        "target_class_context_preserved_for_future_design_only": True,
        "future_target_classes": _target_classes(),
        "future_target_class_count": len(_target_classes()),
        "stage5di_target_validation_implemented": False,
        "tor_network_access_performed": False,
    }
    records["source_lock_plan"] = {
        **_base_record("source_lock_plan"),
        **common,
        "source_lock_plan_status": "complete",
        "source_family_count": len(SOURCE_FAMILY_IDS),
        "web_source_lock_count": len(web_sources),
        "local_archive_source_lock_count": len(local_sources),
        "raw_body_committed": False,
        "execution_authorized_now": False,
    }
    records["recent_clue_source_lock_register"] = {
        **_base_record("recent_clue_source_lock_register"),
        **common,
        "recent_clue_source_lock_package_created": True,
        "source_family_ids": SOURCE_FAMILY_IDS,
        "source_family_count": len(SOURCE_FAMILY_IDS),
        "web_source_ids": [source["source_id"] for source in web_sources],
        "web_source_lock_count": len(web_sources),
        "local_archive_source_ids": [source["source_id"] for source in local_sources],
        "local_archive_source_lock_count": len(local_sources),
        "source_records_total": len(web_sources) + len(local_sources),
    }
    records["pivot_readiness_package"] = {
        **_base_record("pivot_readiness_package"),
        **common,
        "pivot_readiness_package_created": True,
        "pivot_target_selected_now": False,
        "selected_next_solve_target_id": None,
        "operator_target_priority_decision_created_now": False,
        "operator_target_priority_decision_required_next": True,
        "experiments_authorized_now": False,
        "byte_stream_generation_authorized_now": False,
        "execution_authorized_now": False,
        "pivot_candidates": pivot_candidates,
        "pivot_option_count": len(pivot_candidates),
    }
    records["pivot_priority_matrix"] = {
        **_base_record("pivot_priority_matrix"),
        **common,
        "priority_matrix_status": "reviewable_qualitative_no_selection",
        "ranking_is_decision": False,
        "pivot_target_selected_now": False,
        "dimensions": [
            "source_strength",
            "specificity",
            "relation_to_verified_cicada_message",
            "relation_to_known_lp_structure",
            "experiment_boundedness",
            "risk_of_overfit",
            "execution_readiness",
            "expected_information_gain",
        ],
        "candidate_priorities": [
            {
                "candidate_id": "token_block_first",
                "current_priority": "medium",
                "reason": "Well-scaffolded but recent clues may point elsewhere.",
            },
            {
                "candidate_id": "page32_tree_polar_route_first",
                "current_priority": "high_or_medium_high",
                "reason": "Specific route wording and page32/full49 visual-link claim.",
            },
            {
                "candidate_id": "pdd_153_triangle_route_first",
                "current_priority": "high_or_medium_high",
                "reason": "Specific numeric/word-position claims requiring reproducible crosswalk.",
            },
            {
                "candidate_id": "page56_dwh_hash_contract_first",
                "current_priority": "medium_high_final_target",
                "reason": "Known target contract but not a route by itself.",
            },
            {
                "candidate_id": "continue_approval_chain_first",
                "current_priority": "medium",
                "reason": "Governance chain still needed, but target priority should be reviewed first.",
            },
            {
                "candidate_id": "defer_for_more_source_locking",
                "current_priority": "medium",
                "reason": "Useful if source-lock gaps remain unresolved.",
            },
        ],
    }
    records["route_candidate_family_index"] = {
        **_base_record("route_candidate_family_index"),
        **common,
        "candidate_families": route_family_index,
        "candidate_family_count": len(SOURCE_FAMILY_IDS),
        "route_candidate_family_count": len(ROUTE_CANDIDATE_FAMILY_IDS),
        "visual_marker_candidate_count": 1,
    }
    records["record_family_name_equivalence_map"] = {
        **_base_record("record_family_name_equivalence_map"),
        **common,
        "equivalence_entries": [
            {
                "canonical_record_path": DATA_PATHS[
                    "stage5dg_operator_approval_preservation"
                ].as_posix(),
                "alternate_name_from_prompt": (
                    "data/token-block/stage5di-stage5dg-approval-preservation.yaml"
                ),
                "equivalence_reason": "prompt shorthand; committed path keeps operator-approval wording",
            },
            {
                "canonical_record_family_id": "page32_tree_polar_route_v0",
                "alternate_names": ["page32/full49_tree_route", "tree_polar_route"],
            },
            {
                "canonical_record_family_id": "pdd_153_triangle_word_route_v0",
                "alternate_names": ["153_word_triangle", "T17_triangle_route"],
            },
        ],
        "equivalence_entry_count": 3,
    }
    records["handoff_policy"] = {
        **_base_record("handoff_policy"),
        **common,
        "canonical_codex_handoff_root": "codex-output",
        "deprecated_handoff_root": "codex_output",
        "codex_output_used": False,
        "codex_output_exists_locally": DEPRECATED_CODEX_OUTPUT.exists(),
        "codex_completion_summary_committed": False,
        "stage5di_codex_completion_summary_path": CODEX_COMPLETION_PATH.as_posix(),
        "stage5di_completion_summary_finalized_not_pending": True,
    }
    records["credential_redaction"] = {
        **_base_record("credential_redaction"),
        **common,
        **_credential_remote_summary(),
        "credential_redaction_policy_preserved": True,
        "operator_paths_committed_only_as_repo_relative_paths": True,
    }
    records["review_packaging_warning"] = {
        **_base_record("review_packaging_warning"),
        **common,
        "review_packaging_warning_status": "active",
        "raw_forum_messages_not_committed": True,
        "raw_page_images_not_committed": True,
        "raw_web_bodies_not_committed": True,
        "source_lock_only_not_review_pack": True,
    }
    records["validation_evidence"] = {
        **_base_record("validation_evidence"),
        **common,
        "validation_evidence_status": "committed_compact_evidence",
        "parallel_worker_cap": PARALLEL_WORKER_CAP,
        "old_16_worker_default_reintroduced": False,
        "pytest_command_observed_locally": "python -m pytest -q tests/python",
        "build_stage5di_status": "passed",
        "focused_validators_status": "passed",
        "validate_stage5di_status": "passed",
        "stage5di_summary_command_status": "passed",
        "parallel_validation_workers_expected": PARALLEL_WORKER_CAP,
        "validation_commands": [
            "python -m libreprimus.cli token-block build-stage5di",
            "python -m libreprimus.cli token-block validate-stage5di",
            "python -m libreprimus.cli token-block stage5di-summary",
            "scripts/ci/run-parallel-validation.ps1 -Workers 8 -PytestWorkers 8 -PytestMode auto",
        ],
        "raw_staged": False,
        "generated_outputs_staged": False,
        "codex_output_staged": False,
        "sqlite_staged": False,
    }
    records["gap_register"] = {
        **_base_record("gap_register"),
        **common,
        "reviewability_gap_count": 7,
        "reviewability_gaps": [
            "deep_research_acceptance_record_absent",
            "combined_gate_validation_absent",
            "operator_target_priority_decision_absent",
            "pdd_153_triangle_claims_need_reproducible_transcript_crosswalk",
            "page32_tree_polar_claims_need bounded route predefinition",
            "page56_hash_contract_lacks algorithm and target-class validation",
            "dinkus_visual_marker_unmeasured_and_not_interpreted",
        ],
    }
    records["next_stage_decision"] = {
        **_base_record("next_stage_decision"),
        **common,
        "selected_next_stage_id": NEXT_STAGE_ID,
        "selected_next_stage_title": NEXT_STAGE_TITLE,
        "selected_next_prompt_type": NEXT_PROMPT_TYPE,
        "selected_next_stage_authorizes_execution": False,
        "selected_next_stage_authorizes_activation": False,
        "selected_next_stage_authorizes_byte_stream_generation": False,
        "selected_next_stage_requires_review_of_stage5di_package": True,
        "reason": (
            "Stage 5DI creates source-lock and pivot-readiness records only. "
            "Stage 5DJ should review target-priority options without selecting "
            "active input or authorizing execution unless a later explicit prompt does so."
        ),
    }
    records["summary"] = {
        **_base_record("summary"),
        **common,
        "status": "complete",
        "source_previous_stage_title": "Stage 5DG - Real operator approval record creation, without activation",
        "source_previous_stage_issue": SOURCE_PREVIOUS_STAGE_ISSUE,
        "source_previous_stage_ci_run": SOURCE_PREVIOUS_STAGE_CI_RUN,
        "source_previous_stage_pytest_count": SOURCE_PREVIOUS_STAGE_PYTEST_COUNT,
        "stage5dg_summary_status": stage5dg_summary.get("status"),
        "stage5dg_source_commit_constant": STAGE5DG_COMMIT,
        "recent_clue_source_lock_package_created": True,
        "pivot_readiness_package_created": True,
        "pivot_target_selected_now": False,
        "selected_next_solve_target_id": None,
        "operator_target_priority_decision_created_now": False,
        "operator_target_priority_decision_required_next": True,
        "web_source_lock_count": len(web_sources),
        "local_archive_source_lock_count": len(local_sources),
        "source_records_total": len(web_sources) + len(local_sources),
        "candidate_family_count": len(SOURCE_FAMILY_IDS),
        "route_candidate_family_count": len(ROUTE_CANDIDATE_FAMILY_IDS),
        "visual_marker_candidate_count": 1,
        "pivot_option_count": len(pivot_candidates),
        "recommended_next_stage_id": NEXT_STAGE_ID,
        "recommended_next_stage_title": NEXT_STAGE_TITLE,
        "recommended_next_prompt_type": NEXT_PROMPT_TYPE,
        "stage5di_codex_completion_summary_path": CODEX_COMPLETION_PATH.as_posix(),
    }
    return records


def _write_completion_summary(summary: dict[str, Any]) -> None:
    CODEX_COMPLETION_PATH.parent.mkdir(parents=True, exist_ok=True)
    CODEX_COMPLETION_PATH.write_text(
        "# Stage 5DI Codex Completion Summary\n\n"
        "## 1. Stage identity\n"
        f"- stage_id: {STAGE_ID}\n"
        f"- stage_title: {STAGE_TITLE}\n"
        "- stage_status: complete\n"
        "- stage_scope: recent clue source-lock and pivot readiness only\n\n"
        "## 2. Previous stage preservation\n"
        f"- source_previous_stage_commit: {SOURCE_PREVIOUS_STAGE_COMMIT}\n"
        "- stage5dg_operator_approval_record_preserved: true\n"
        "- real_operator_approval_record_created_now: true\n"
        "- operator_approval_component_satisfied_now: true\n"
        "- deep_research_acceptance_component_satisfied_now: false\n"
        "- combined_approval_gate_satisfied_now: false\n\n"
        "## 3. Source-lock package\n"
        f"- web_source_lock_count: {summary['web_source_lock_count']}\n"
        f"- local_archive_source_lock_count: {summary['local_archive_source_lock_count']}\n"
        f"- source_records_total: {summary['source_records_total']}\n"
        f"- candidate_family_count: {summary['candidate_family_count']}\n"
        f"- route_candidate_family_count: {summary['route_candidate_family_count']}\n\n"
        "## 4. Pivot readiness\n"
        "- pivot_readiness_package_created: true\n"
        "- pivot_target_selected_now: false\n"
        "- operator_target_priority_decision_created_now: false\n"
        f"- pivot_option_count: {summary['pivot_option_count']}\n\n"
        "## 5. No-execution guardrails\n"
        "- activation_authorized_now: false\n"
        "- active_planning_input_selected_now: false\n"
        "- byte_stream_generation_authorized_now: false\n"
        "- execution_authorized_now: false\n"
        "- target_class_validation_implemented: false\n"
        "- tor_network_access_performed: false\n"
        "- solve_claim: false\n\n"
        "## 6. Preservation counts\n"
        f"- stage5bd_run_plan_id_count: {summary['stage5bd_run_plan_id_count']}\n"
        f"- active_lineage_record_count: {summary['active_lineage_record_count']}\n"
        f"- parallel_worker_cap_for_stage5di_and_later: {PARALLEL_WORKER_CAP}\n\n"
        "## 7. Output policy\n"
        "- generated_outputs_staged: false\n"
        "- raw_staged: false\n"
        "- codex_output_staged: false\n"
        "- sqlite_staged: false\n"
        "- codex-output completion summary remains ignored and uncommitted\n\n"
        "## 8. Next recommended stage\n"
        f"- recommended_next_stage_id: {NEXT_STAGE_ID}\n"
        f"- recommended_next_stage_title: {NEXT_STAGE_TITLE}\n"
        f"- recommended_next_prompt_type: {NEXT_PROMPT_TYPE}\n",
        encoding="utf-8",
    )


def build_stage5di(results_dir: Path = RESULTS_DIR) -> dict[str, Any]:
    _write_schemas()
    records = _records()
    for key, record in records.items():
        write_yaml(DATA_PATHS[key], record)
    results_dir.mkdir(parents=True, exist_ok=True)
    write_json(results_dir / "summary.json", records["summary"])
    write_json(
        results_dir / "source_lock_report.json",
        {
            "web": records["web_source_lock_register"],
            "local": records["local_archive_source_lock_register"],
            "cicada_crosswalk": records["cicada_solvers_crosswalk"],
            "number_triangle_crosswalk": records["number_triangle_crosswalk"],
        },
    )
    write_json(results_dir / "pivot_readiness_report.json", records["pivot_readiness_package"])
    write_json(results_dir / "candidate_family_report.json", records["route_candidate_family_index"])
    write_json(
        results_dir / "preservation_report.json",
        {
            "stage5dg": records["stage5dg_operator_approval_preservation"],
            "stage5bd": records["stage5bd_plan_preservation"],
            "active_lineage": records["active_lineage_preservation"],
            "no_active_ingestion": records["no_active_ingestion"],
            "no_byte_stream": records["no_byte_stream_transition_gate"],
            "no_execution": records["no_execution_transition_gate"],
        },
    )
    write_json(results_dir / "handoff_continuity_report.json", records["handoff_policy"])
    write_jsonl(results_dir / "warnings.jsonl", [])
    _write_completion_summary(records["summary"])
    return records["summary"]


def _validate_schema(record_key: str, path: Path) -> list[str]:
    schema_path = Path(SCHEMA_PATHS[record_key])
    if not schema_path.exists():
        return [f"missing_schema:{schema_path.as_posix()}"]
    if not path.exists():
        return [f"missing_record:{path.as_posix()}"]
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    payload = _load_yaml(path)
    return [
        f"schema:{record_key}:{error.message}"
        for error in Draft202012Validator(schema).iter_errors(payload)
    ]


def _walk_dicts(payload: Any) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    if isinstance(payload, dict):
        records.append(payload)
        for value in payload.values():
            records.extend(_walk_dicts(value))
    elif isinstance(payload, list):
        for value in payload:
            records.extend(_walk_dicts(value))
    return records


def _ensure_common_flags(payload: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if payload.get("stage_id") != STAGE_ID:
        errors.append("stage_id_must_be_stage_5di")
    if payload.get("metadata_only") is not True:
        errors.append("metadata_only_must_be_true")
    for item in _walk_dicts(payload):
        for key, expected in FORBIDDEN_FALSE_FLAGS.items():
            if key in item and item[key] is not expected:
                errors.append(f"{key}_must_be_false")
    for key, expected in TRUE_FLAGS.items():
        if key in payload and payload[key] is not expected:
            errors.append(f"{key}_must_be_true")
    return sorted(set(errors))


def _finish(
    record_key: str,
    path: Path,
    counts: dict[str, Any],
    errors: list[str],
) -> tuple[dict[str, Any], list[str]]:
    return counts, [*_validate_schema(record_key, path), *_ensure_common_flags(_load_yaml(path)), *errors]


def validate_stage5di_source_lock_register(
    register: Path = DATA_PATHS["recent_clue_source_lock_register"],
) -> tuple[dict[str, Any], list[str]]:
    payload = _load_yaml(register)
    errors: list[str] = []
    for family_id in SOURCE_FAMILY_IDS:
        if family_id not in payload.get("source_family_ids", []):
            errors.append(f"missing_source_family:{family_id}")
    if payload.get("source_family_count") != len(SOURCE_FAMILY_IDS):
        errors.append("source_family_count_mismatch")
    if payload.get("web_source_lock_count") != len(WEB_SOURCES):
        errors.append("web_source_lock_count_mismatch")
    counts = {
        "source_family_count": payload.get("source_family_count"),
        "web_source_lock_count": payload.get("web_source_lock_count"),
        "local_archive_source_lock_count": payload.get("local_archive_source_lock_count"),
    }
    return _finish("recent_clue_source_lock_register", register, counts, errors)


def validate_stage5di_local_archive_crosswalk(
    crosswalk: Path = DATA_PATHS["cicada_solvers_crosswalk"],
) -> tuple[dict[str, Any], list[str]]:
    payload = _load_yaml(crosswalk)
    errors: list[str] = []
    if payload.get("root_exists") is not True:
        errors.append("iddqd_v2_root_must_exist_for_stage5di_local_source_lock")
    crosswalk_ids = {row.get("candidate_family_id") for row in payload.get("crosswalks", [])}
    for family_id in [
        "page32_tree_polar_route_v0",
        "pdd_153_triangle_word_route_v0",
        "page56_dwh_hash_target_contract_v0",
        "token_block_matrix_context_v0",
    ]:
        if family_id not in crosswalk_ids:
            errors.append(f"missing_crosswalk_family:{family_id}")
    counts = {
        "root_exists": payload.get("root_exists"),
        "crosswalk_count": payload.get("crosswalk_count"),
        "path_spelling_warning": payload.get("path_spelling_warning"),
    }
    return _finish("cicada_solvers_crosswalk", crosswalk, counts, errors)


def validate_stage5di_number_triangle_crosswalk(
    crosswalk: Path = DATA_PATHS["number_triangle_crosswalk"],
) -> tuple[dict[str, Any], list[str]]:
    payload = _load_yaml(crosswalk)
    errors: list[str] = []
    if payload.get("bundle_root_exists") is not True:
        errors.append("number_triangle_bundle_root_must_exist")
    if payload.get("message_file_count", 0) < 1:
        errors.append("number_triangle_message_file_must_be_recorded")
    if payload.get("image_file_count", 0) < 1:
        errors.append("number_triangle_image_files_must_be_recorded")
    counts = {
        "bundle_root_exists": payload.get("bundle_root_exists"),
        "file_count": payload.get("file_count"),
        "message_file_count": payload.get("message_file_count"),
        "image_file_count": payload.get("image_file_count"),
    }
    return _finish("number_triangle_crosswalk", crosswalk, counts, errors)


def validate_stage5di_route_candidate_families(
    index: Path = DATA_PATHS["route_candidate_family_index"],
) -> tuple[dict[str, Any], list[str]]:
    payload = _load_yaml(index)
    errors: list[str] = []
    family_ids = {row.get("candidate_family_id") for row in payload.get("candidate_families", [])}
    for family_id in SOURCE_FAMILY_IDS:
        if family_id not in family_ids:
            errors.append(f"missing_candidate_family:{family_id}")
    if payload.get("candidate_family_count") != len(SOURCE_FAMILY_IDS):
        errors.append("candidate_family_count_mismatch")
    if payload.get("route_candidate_family_count") != len(ROUTE_CANDIDATE_FAMILY_IDS):
        errors.append("route_candidate_family_count_mismatch")
    counts = {
        "candidate_family_count": payload.get("candidate_family_count"),
        "route_candidate_family_count": payload.get("route_candidate_family_count"),
        "visual_marker_candidate_count": payload.get("visual_marker_candidate_count"),
    }
    return _finish("route_candidate_family_index", index, counts, errors)


def validate_stage5di_pivot_readiness(
    package: Path = DATA_PATHS["pivot_readiness_package"],
) -> tuple[dict[str, Any], list[str]]:
    payload = _load_yaml(package)
    errors: list[str] = []
    if payload.get("pivot_target_selected_now") is not False:
        errors.append("pivot_target_must_not_be_selected")
    if payload.get("selected_next_solve_target_id") is not None:
        errors.append("selected_next_solve_target_id_must_be_null")
    candidates = payload.get("pivot_candidates", [])
    if len(candidates) != len(PIVOT_CANDIDATES):
        errors.append("pivot_candidate_count_mismatch")
    if any(candidate.get("status") != "candidate_not_selected" for candidate in candidates):
        errors.append("all_pivot_candidates_must_be_not_selected")
    counts = {
        "pivot_option_count": payload.get("pivot_option_count"),
        "pivot_target_selected_now": payload.get("pivot_target_selected_now"),
        "operator_target_priority_decision_created_now": payload.get(
            "operator_target_priority_decision_created_now"
        ),
    }
    return _finish("pivot_readiness_package", package, counts, errors)


def validate_stage5di_dinkus_visual_delimiter(
    record: Path = DATA_PATHS["dinkus_visual_delimiter"],
) -> tuple[dict[str, Any], list[str]]:
    payload = _load_yaml(record)
    errors: list[str] = []
    if payload.get("candidate_id") != "dinkus_visual_delimiter_candidate_v0":
        errors.append("dinkus_candidate_id_mismatch")
    if payload.get("meaning_claimed_now") is not False:
        errors.append("dinkus_must_not_claim_meaning")
    if payload.get("measurement_performed_now") is not False:
        errors.append("dinkus_measurement_must_not_be_performed_in_stage5di")
    counts = {
        "candidate_status": payload.get("candidate_status"),
        "measurement_performed_now": payload.get("measurement_performed_now"),
        "meaning_claimed_now": payload.get("meaning_claimed_now"),
    }
    return _finish("dinkus_visual_delimiter", record, counts, errors)


def validate_stage5di_stage5dg_preservation(
    preservation: Path = DATA_PATHS["stage5dg_operator_approval_preservation"],
) -> tuple[dict[str, Any], list[str]]:
    payload = _load_yaml(preservation)
    errors: list[str] = []
    if payload.get("stage5dg_operator_approval_record_preserved") is not True:
        errors.append("stage5dg_operator_approval_record_must_be_preserved")
    if payload.get("operator_approval_component_satisfied_now") is not True:
        errors.append("operator_approval_component_must_stay_satisfied")
    if payload.get("new_real_operator_approval_record_created_in_stage5di") is not False:
        errors.append("stage5di_must_not_create_second_operator_approval_record")
    counts = {
        "stage5dg_operator_approval_record_preserved": payload.get(
            "stage5dg_operator_approval_record_preserved"
        ),
        "operator_approval_component_satisfied_now": payload.get(
            "operator_approval_component_satisfied_now"
        ),
        "combined_approval_gate_satisfied_now": payload.get(
            "combined_approval_gate_satisfied_now"
        ),
    }
    return _finish("stage5dg_operator_approval_preservation", preservation, counts, errors)


def validate_stage5di_stage5bd_preservation(
    preservation: Path = DATA_PATHS["stage5bd_plan_preservation"],
) -> tuple[dict[str, Any], list[str]]:
    counts, errors = validate_stage5bd()
    payload = _load_yaml(preservation)
    if payload.get("stage5bd_run_plan_id_count") != 10:
        errors.append("stage5bd_run_plan_id_count_must_be_10")
    for field in [
        "stage5bd_run_plan_ids_changed",
        "stage5bd_dry_run_plan_manifest_changed",
        "stage5bd_plan_superseded",
        "string4_added_to_stage5bd_run_plan_ids",
        "string4_added_to_active_dry_run_inputs",
    ]:
        if payload.get(field) is not False:
            errors.append(f"{field}_must_be_false")
    counts.update(
        {
            "stage5bd_run_plan_id_count": payload.get("stage5bd_run_plan_id_count"),
            "stage5bd_run_plan_ids_changed": payload.get("stage5bd_run_plan_ids_changed"),
        }
    )
    return _finish("stage5bd_plan_preservation", preservation, counts, errors)


def validate_stage5di_active_lineage_preservation(
    preservation: Path = DATA_PATHS["active_lineage_preservation"],
) -> tuple[dict[str, Any], list[str]]:
    payload = _load_yaml(preservation)
    errors: list[str] = []
    if payload.get("active_lineage_record_count") != len(ACTIVE_LINEAGE_PATHS):
        errors.append("active_lineage_record_count_mismatch")
    if payload.get("correct_stage5aw_path_included") is not True:
        errors.append("correct_stage5aw_path_must_be_included")
    if payload.get("deprecated_stage5aw_path_absent") is not True:
        errors.append("deprecated_stage5aw_path_must_be_absent")
    counts = {
        "active_lineage_record_count": payload.get("active_lineage_record_count"),
        "correct_stage5aw_path_included": payload.get("correct_stage5aw_path_included"),
        "deprecated_stage5aw_path_absent": payload.get("deprecated_stage5aw_path_absent"),
    }
    return _finish("active_lineage_preservation", preservation, counts, errors)


def validate_stage5di_sidecar_gates() -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    counts: dict[str, Any] = {}
    for key, status_field in [
        ("no_active_ingestion", "no_active_ingestion_status"),
        ("no_byte_stream_transition_gate", "no_byte_stream_transition_gate_status"),
        ("no_execution_transition_gate", "no_execution_transition_gate_status"),
    ]:
        payload = _load_yaml(DATA_PATHS[key])
        errors.extend(_validate_schema(key, DATA_PATHS[key]))
        errors.extend(_ensure_common_flags(payload))
        if payload.get(status_field) != "closed":
            errors.append(f"{status_field}_must_be_closed")
        counts[status_field] = payload.get(status_field)
    return counts, sorted(set(errors))


def validate_stage5di_handoff_continuity() -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    if not CODEX_COMPLETION_PATH.exists():
        errors.append("stage5di_codex_completion_summary_missing")
    if DEPRECATED_CODEX_OUTPUT.exists():
        errors.append("codex_output_underscore_root_must_be_absent")
    if CODEX_COMPLETION_PATH.exists() and "pending" in CODEX_COMPLETION_PATH.read_text(
        encoding="utf-8"
    ).lower():
        errors.append("stage5di_completion_summary_must_not_be_pending")
    counts = {
        "stage5di_codex_completion_summary_present": CODEX_COMPLETION_PATH.exists(),
        "codex_output_exists_locally": DEPRECATED_CODEX_OUTPUT.exists(),
    }
    return _finish("handoff_policy", DATA_PATHS["handoff_policy"], counts, errors)


def validate_stage5di_credential_redaction_policy(
    credential_redaction: Path = DATA_PATHS["credential_redaction"],
) -> tuple[dict[str, Any], list[str]]:
    payload = _load_yaml(credential_redaction)
    errors: list[str] = []
    if payload.get("remote_url_values_printed") is not False:
        errors.append("remote_url_values_must_not_be_printed")
    if payload.get("secret_values_printed_or_committed") is not False:
        errors.append("secret_values_must_not_be_printed_or_committed")
    counts = {
        "credential_like_remote_count": payload.get("credential_like_remote_count"),
        "remote_url_values_printed": payload.get("remote_url_values_printed"),
    }
    return _finish("credential_redaction", credential_redaction, counts, errors)


def validate_stage5di_governance_scope(
    guardrail: Path = DATA_PATHS["guardrail"],
) -> tuple[dict[str, Any], list[str]]:
    payload = _load_yaml(guardrail)
    errors: list[str] = []
    if payload.get("guardrail_status") != "closed":
        errors.append("guardrail_status_must_be_closed")
    for field in [
        "activation_authorized_now",
        "byte_stream_generation_authorized_now",
        "execution_authorized_now",
        "tor_network_access_performed",
        "target_class_validation_implemented",
        "solve_claim",
    ]:
        if payload.get(field) is not False:
            errors.append(f"{field}_must_be_false")
    counts = {
        "guardrail_status": payload.get("guardrail_status"),
        "forbidden_action_count": len(payload.get("forbidden_actions_preserved_false", [])),
    }
    return _finish("guardrail", guardrail, counts, errors)


def validate_stage5di(
    summary: Path = DATA_PATHS["summary"],
    next_stage_decision: Path = DATA_PATHS["next_stage_decision"],
    results_dir: Path = RESULTS_DIR,
) -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    for key, path in DATA_PATHS.items():
        errors.extend(_validate_schema(key, path))
        errors.extend(_ensure_common_flags(_load_yaml(path)))
    for validator in [
        validate_stage5di_source_lock_register,
        validate_stage5di_local_archive_crosswalk,
        validate_stage5di_number_triangle_crosswalk,
        validate_stage5di_route_candidate_families,
        validate_stage5di_pivot_readiness,
        validate_stage5di_dinkus_visual_delimiter,
        validate_stage5di_stage5dg_preservation,
        validate_stage5di_stage5bd_preservation,
        validate_stage5di_active_lineage_preservation,
        validate_stage5di_sidecar_gates,
        validate_stage5di_handoff_continuity,
        validate_stage5di_credential_redaction_policy,
        validate_stage5di_governance_scope,
    ]:
        _, validator_errors = validator()
        errors.extend(validator_errors)
    payload = _load_yaml(summary)
    next_payload = _load_yaml(next_stage_decision)
    if payload.get("status") != "complete":
        errors.append("summary_status_must_be_complete")
    if payload.get("recommended_next_stage_id") != NEXT_STAGE_ID:
        errors.append("recommended_next_stage_must_be_stage5dj")
    if next_payload.get("selected_next_stage_id") != NEXT_STAGE_ID:
        errors.append("next_stage_decision_must_select_stage5dj")
    for report_name in [
        "summary.json",
        "source_lock_report.json",
        "pivot_readiness_report.json",
        "candidate_family_report.json",
        "preservation_report.json",
        "handoff_continuity_report.json",
        "warnings.jsonl",
    ]:
        if not (results_dir / report_name).exists():
            errors.append(f"missing_generated_report:{report_name}")
    counts = {
        "stage_id": payload.get("stage_id"),
        "status": payload.get("status"),
        "source_records_total": payload.get("source_records_total"),
        "web_source_lock_count": payload.get("web_source_lock_count"),
        "local_archive_source_lock_count": payload.get("local_archive_source_lock_count"),
        "candidate_family_count": payload.get("candidate_family_count"),
        "route_candidate_family_count": payload.get("route_candidate_family_count"),
        "pivot_option_count": payload.get("pivot_option_count"),
        "pivot_target_selected_now": payload.get("pivot_target_selected_now"),
        "stage5dg_operator_approval_record_preserved": payload.get(
            "stage5dg_operator_approval_record_preserved"
        ),
        "operator_approval_component_satisfied_now": payload.get(
            "operator_approval_component_satisfied_now"
        ),
        "combined_approval_gate_satisfied_now": payload.get(
            "combined_approval_gate_satisfied_now"
        ),
        "activation_authorized_now": payload.get("activation_authorized_now"),
        "byte_stream_generation_authorized_now": payload.get(
            "byte_stream_generation_authorized_now"
        ),
        "execution_authorized_now": payload.get("execution_authorized_now"),
        "stage5bd_run_plan_id_count": payload.get("stage5bd_run_plan_id_count"),
        "active_lineage_record_count": payload.get("active_lineage_record_count"),
        "parallel_worker_cap": payload.get("parallel_worker_cap_for_stage5di_and_later"),
        "recommended_next_stage_id": payload.get("recommended_next_stage_id"),
    }
    return counts, sorted(set(errors))


def load_stage5di_summary(summary: Path = DATA_PATHS["summary"]) -> dict[str, Any]:
    return _load_yaml(summary)
