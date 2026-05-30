"""Stage 5CA inactive sidecar review-contract hardening metadata."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from libreprimus.token_block.models import repo_relative, sha256_file, write_json, write_yaml
from libreprimus.token_block.stage5bm import _read

STAGE_ID = "stage-5ca"
STAGE_TITLE = (
    "Stage 5CA - Inactive-sidecar manifest review contract and "
    "activation-precondition hardening, without execution"
)
PROMPT_TYPE = "codex_metadata_implementation"
SOURCE_PREVIOUS_STAGE = "stage-5by"
SOURCE_PREVIOUS_COMMIT = "2554812801d42de888ec4d2561bfa20dc4efee92"
SOURCE_DEEP_RESEARCH_STAGE = "stage-5bz"
SOURCE_DEEP_RESEARCH_REPORT = "15_Stage-5BY-Deep-Research-Review.md"

RESULTS_DIR = Path("experiments/results/token-block/stage5ca")
CODEX_COMPLETION_PATH = Path("codex-output/stage5ca-codex-completion.md")
DEPRECATED_CODEX_OUTPUT = Path("codex_output")
STAGE5BZ_REPORT_PATH = Path(
    "deep-research-reports/reviews-of-ideas-and-concepts-and-data/md/"
    "15_Stage-5BY-Deep-Research-Review.md"
)

CORRECT_STAGE5AW_PATH = "data/token-block/stage5aw-repaired-token-variant-branch-manifest.yaml"
INCORRECT_STAGE5AW_PATH = "data/token-block/stage5aw-repaired-branch-manifest.yaml"

ACTIVE_LINEAGE_PATHS = [
    "data/token-block/stage5ap-token-block-canonical-transcription.yaml",
    CORRECT_STAGE5AW_PATH,
    "data/token-block/stage5ay-branch-eligibility-policy.yaml",
    "data/token-block/stage5az-repaired-bounded-variant-family-manifest.yaml",
    "data/token-block/stage5bb-active-manifest-registry.yaml",
    "data/token-block/stage5bd-active-manifest-lock.yaml",
    "data/token-block/stage5bd-dry-run-plan-manifest.yaml",
    "data/token-block/stage5bd-run-plan-id-registry.yaml",
]

STAGE5BD_PRESERVATION_PATHS = [
    "data/project-state/stage5bd-summary.yaml",
    "data/token-block/stage5bd-active-manifest-lock.yaml",
    "data/token-block/stage5bd-dry-run-plan-manifest.yaml",
    "data/token-block/stage5bd-run-plan-id-registry.yaml",
    "data/token-block/stage5bd-run-plan-id-policy.yaml",
    "data/token-block/stage5bd-dry-run-policy.yaml",
    "data/token-block/stage5bd-future-result-path-validation.yaml",
    "data/token-block/stage5bd-execution-gate-dry-run-validation.yaml",
    "data/token-block/stage5bd-no-byte-stream-proof.yaml",
    "data/token-block/stage5bd-guardrail.yaml",
]

REQUIRED_CITATION_PATHS = [
    "data/token-block/stage5bo-string4-branch-membership-after-errata.yaml",
    "data/token-block/stage5bo-errata-aware-token-option-universe.yaml",
    "data/token-block/stage5bo-string4-source-gap-closure-after-errata.yaml",
    "data/token-block/stage5bq-string4-inactive-branch-planning-context.yaml",
    "data/token-block/stage5bq-errata-aware-dry-run-constraint-update.yaml",
    "data/token-block/stage5bq-string4-no-active-ingestion-proof.yaml",
    "data/token-block/stage5bs-string4-planning-ingestion-gate.yaml",
    "data/token-block/stage5bs-future-runner-citation-policy.yaml",
    "data/token-block/stage5bs-inactive-sidecar-consumption-policy.yaml",
    "data/token-block/stage5bs-active-ingestion-blocker.yaml",
    "data/token-block/stage5bu-lineage-path-resolution-validation.yaml",
    "data/token-block/stage5bu-preserved-active-lineage-digest-index.yaml",
    "data/token-block/stage5bu-active-manifest-preservation-repair.yaml",
    "data/token-block/stage5bw-inactive-sidecar-planning-ingestion-proposal.yaml",
    "data/token-block/stage5bw-manifest-supersession-preflight.yaml",
    "data/token-block/stage5bw-stage5bd-plan-preservation.yaml",
    "data/token-block/stage5bw-future-runner-citation-requirements.yaml",
    "data/token-block/stage5by-inactive-sidecar-planning-manifest-scaffold.yaml",
    "data/token-block/stage5by-no-execution-planning-ingestion-sidecar.yaml",
    "data/token-block/stage5by-future-runner-citation-requirements.yaml",
    "data/token-block/stage5by-sidecar-activation-blocker.yaml",
    "data/token-block/stage5by-stage5bd-plan-preservation.yaml",
    "data/token-block/stage5by-active-lineage-preservation.yaml",
    "data/token-block/stage5ca-inactive-sidecar-review-contract.yaml",
    "data/token-block/stage5ca-future-runner-exact-citation-contract.yaml",
    "data/token-block/stage5ca-fail-closed-trigger-contract.yaml",
    "data/token-block/stage5ca-activation-precondition-contract.yaml",
    "data/token-block/stage5ca-manifest-supersession-preflight-contract.yaml",
    "data/token-block/stage5ca-sidecar-to-active-transition-policy.yaml",
    "data/token-block/stage5ca-no-active-ingestion-proof.yaml",
    "data/token-block/stage5ca-no-byte-stream-proof.yaml",
    "data/token-block/stage5ca-stage5bd-plan-preservation.yaml",
    "data/token-block/stage5ca-active-lineage-preservation.yaml",
]

REQUIRED_FAIL_CLOSED_TRIGGERS = [
    "citation_missing",
    "citation_path_unresolved",
    "citation_set_not_exact",
    "sidecar_status_not_inactive",
    "active_ingestion_flag_true",
    "dry_run_ingestion_flag_true",
    "byte_stream_generation_flag_true",
    "execution_input_flag_true",
    "manifest_supersession_performed",
    "stage5bd_run_plan_ids_changed",
    "stage5bd_run_plan_count_changed",
    "active_lineage_path_missing",
    "deprecated_stage5aw_path_present",
    "no_byte_stream_proof_missing",
    "no_execution_guardrail_missing",
    "dwh_quarantine_not_active",
    "codex_output_used",
]

REQUIRED_ACTIVATION_PRECONDITIONS = [
    "explicit_future_stage_authorization",
    "deep_research_or_operator_review_if_selected",
    "exact_future_runner_citation_contract_validation",
    "fail_closed_trigger_validation",
    "activation_precondition_validation",
    "manifest_validation",
    "no_byte_stream_gate_validation",
    "no_execution_guardrail_validation",
    "stage5bd_preservation_or_explicit_supersession",
    "active_manifest_registry_update_only_in_future_stage",
    "before_after_digest_review_if_supersession_selected",
    "current_stage_authorizes_activation_false",
]

REQUIRED_SUPERSESSION_REQUIREMENTS = [
    "explicit_target_manifest_list",
    "before_after_digest_comparison",
    "active_manifest_registry_update_only_in_future_stage",
    "stage5bd_dry_run_run_plan_policy_review",
    "no_byte_stream_proof",
    "no_execution_proof",
    "future_runner_citation_update",
    "deep_research_or_operator_review_if_selected",
    "explicit_stage5bd_plan_preservation_or_supersession_record",
]

DATA_PATHS: dict[str, Path] = {
    "summary": Path("data/project-state/stage5ca-summary.yaml"),
    "next_stage": Path("data/project-state/stage5ca-next-stage-decision.yaml"),
    "findings": Path("data/project-state/stage5ca-stage5bz-findings-integration.yaml"),
    "stage_marker": Path("data/project-state/stage5ca-reviewable-stage-marker.yaml"),
    "validation_evidence": Path("data/project-state/stage5ca-reviewable-validation-evidence.yaml"),
    "source_digest_index": Path("data/project-state/stage5ca-reviewable-source-digest-index.yaml"),
    "gap_register": Path("data/project-state/stage5ca-reviewability-gap-register.yaml"),
    "equivalence_map": Path("data/project-state/stage5ca-record-family-name-equivalence-map.yaml"),
    "review_contract": Path("data/token-block/stage5ca-inactive-sidecar-review-contract.yaml"),
    "citation_contract": Path("data/token-block/stage5ca-future-runner-exact-citation-contract.yaml"),
    "citation_validation": Path(
        "data/token-block/stage5ca-future-runner-citation-validation-requirements.yaml"
    ),
    "fail_closed_contract": Path("data/token-block/stage5ca-fail-closed-trigger-contract.yaml"),
    "fail_closed_validation": Path(
        "data/token-block/stage5ca-fail-closed-trigger-validation-requirements.yaml"
    ),
    "activation_contract": Path("data/token-block/stage5ca-activation-precondition-contract.yaml"),
    "activation_validation": Path(
        "data/token-block/stage5ca-activation-precondition-validation-requirements.yaml"
    ),
    "supersession_contract": Path(
        "data/token-block/stage5ca-manifest-supersession-preflight-contract.yaml"
    ),
    "supersession_determinism": Path(
        "data/token-block/stage5ca-manifest-supersession-review-determinism.yaml"
    ),
    "transition_policy": Path("data/token-block/stage5ca-sidecar-to-active-transition-policy.yaml"),
    "activation_blocker": Path("data/token-block/stage5ca-sidecar-activation-blocker.yaml"),
    "stage5by_preservation": Path(
        "data/token-block/stage5ca-stage5by-sidecar-scaffold-preservation.yaml"
    ),
    "stage5bd_preservation": Path("data/token-block/stage5ca-stage5bd-plan-preservation.yaml"),
    "active_lineage": Path("data/token-block/stage5ca-active-lineage-preservation.yaml"),
    "no_active_ingestion": Path("data/token-block/stage5ca-no-active-ingestion-proof.yaml"),
    "no_byte_stream": Path("data/token-block/stage5ca-no-byte-stream-proof.yaml"),
    "future_impact": Path("data/token-block/stage5ca-future-dry-run-planning-impact.yaml"),
    "source_gap": Path("data/historical-route/stage5ca-source-gap-severity-update.yaml"),
    "dwh": Path("data/historical-route/stage5ca-dwh-quarantine-reaffirmation.yaml"),
    "guardrail": Path("data/historical-route/stage5ca-guardrail.yaml"),
    "handoff": Path("data/source-harvester/stage5ca-codex-handoff-policy.yaml"),
    "review_packaging_warning": Path(
        "data/source-harvester/stage5ca-review-packaging-warning.yaml"
    ),
}

SCHEMA_PATHS: dict[str, str] = {
    key: path.as_posix().replace("data/", "schemas/", 1).replace(".yaml", "-v0.schema.json")
    for key, path in DATA_PATHS.items()
}
RECORD_TYPES = {key: f"stage5ca_{key}" for key in DATA_PATHS}

FALSE_FLAGS = {
    "active_ingestion_performed": False,
    "active_token_block_manifest_changed": False,
    "ai_ml_interpretation_performed": False,
    "benchmark_performed": False,
    "branch_enumeration_performed": False,
    "canonical_corpus_active": False,
    "canonical_transcription_changed": False,
    "codex_completion_summary_committed": False,
    "codex_output_used": False,
    "cuda_execution_performed": False,
    "decode_attempt_performed": False,
    "dwh_hash_search_performed": False,
    "execution_allowed": False,
    "full_cartesian_product_enumerated": False,
    "generated_outputs_committed": False,
    "hash_preimage_search_performed": False,
    "image_forensics_performed": False,
    "llm_vision_token_reading_performed": False,
    "manifest_supersession_performed": False,
    "method_status_upgraded": False,
    "ocr_performed": False,
    "page_boundaries_final": False,
    "pgp_network_verification_performed": False,
    "raw_archive_files_committed": False,
    "raw_fandom_files_committed": False,
    "raw_human_review_pack_committed": False,
    "real_byte_stream_generated": False,
    "scoring_performed": False,
    "solve_claim": False,
    "spreadsheet_file_committed": False,
    "stage5bd_dry_run_plan_manifest_changed": False,
    "stage5bd_run_plan_ids_changed": False,
    "stego_tool_execution_performed": False,
    "string4_active_input_allowed": False,
    "string4_byte_stream_generation_allowed": False,
    "string4_dry_run_ingestion_allowed_now": False,
    "string4_execution_input_allowed": False,
    "string4_sidecar_planning_ingestion_activated": False,
    "template_bodies_committed": False,
    "token_block_experiment_executed": False,
    "variant_byte_streams_generated": False,
    "variant_materialisation_performed": False,
    "website_expansion_performed": False,
}


def _base(record_type: str, schema_key: str) -> dict[str, Any]:
    return {
        "record_type": record_type,
        "schema": SCHEMA_PATHS[schema_key],
        "stage_id": STAGE_ID,
        "stage_title": STAGE_TITLE,
        "prompt_type": PROMPT_TYPE,
        "source_previous_stage": SOURCE_PREVIOUS_STAGE,
        "source_previous_stage_commit": SOURCE_PREVIOUS_COMMIT,
        "source_deep_research_stage": SOURCE_DEEP_RESEARCH_STAGE,
        "source_deep_research_report": SOURCE_DEEP_RESEARCH_REPORT,
        "metadata_only": True,
        "solve_claim": False,
        "execution_allowed": False,
    }


def _schema(record_type: str) -> dict[str, Any]:
    properties: dict[str, Any] = {
        "record_type": {"const": record_type},
        "stage_id": {"const": STAGE_ID},
        "metadata_only": {"const": True},
    }
    for key in FALSE_FLAGS:
        properties[key] = {"const": False}
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "type": "object",
        "required": [
            "record_type",
            "schema",
            "stage_id",
            "metadata_only",
            "solve_claim",
            "execution_allowed",
        ],
        "properties": properties,
        "additionalProperties": True,
    }


def _write_schemas() -> None:
    for key, schema_path in SCHEMA_PATHS.items():
        path = Path(schema_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        write_json(path, _schema(RECORD_TYPES[key]))


def _write_generated(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.suffix == ".jsonl":
        path.write_text(
            "".join(json.dumps(row, sort_keys=True) + "\n" for row in payload),
            encoding="utf-8",
        )
    else:
        write_json(path, payload)


def _record(key: str, body: dict[str, Any], *, include_false_flags: bool = True) -> dict[str, Any]:
    payload = _base(RECORD_TYPES[key], key)
    payload.update(body)
    if include_false_flags:
        payload.update(FALSE_FLAGS)
    return payload


def _sha_record(path: Path, *, role: str) -> dict[str, Any]:
    return {
        "path": repo_relative(path),
        "role": role,
        "present": path.is_file(),
        "sha256": sha256_file(path) if path.is_file() else None,
        "size_bytes": path.stat().st_size if path.is_file() else None,
        "raw_or_generated_body_committed": False,
    }


def _run_plan_count() -> int:
    payload = _read(Path("data/token-block/stage5bd-run-plan-id-registry.yaml"))
    return int(payload.get("run_plan_id_count") or len(payload.get("plan_ids", [])))


def _source_paths() -> list[str]:
    paths = [
        str(STAGE5BZ_REPORT_PATH),
        "data/project-state/stage5by-summary.yaml",
        "data/project-state/stage5by-next-stage-decision.yaml",
        "data/project-state/stage5by-stage5bx-findings-integration.yaml",
        "data/project-state/stage5by-stage5bw-source-digest-duplicate-review.yaml",
        "data/project-state/stage5by-record-family-name-equivalence-map.yaml",
        "data/project-state/stage5by-reviewable-source-digest-index.yaml",
        "data/project-state/stage5by-reviewable-validation-evidence.yaml",
        "data/project-state/stage5by-reviewability-gap-register.yaml",
        "data/project-state/stage5by-reviewable-stage-marker.yaml",
        "data/historical-route/stage5by-guardrail.yaml",
        *REQUIRED_CITATION_PATHS,
        *ACTIVE_LINEAGE_PATHS,
        *STAGE5BD_PRESERVATION_PATHS,
    ]
    return list(dict.fromkeys(paths))


def _source_digest_records() -> list[dict[str, Any]]:
    return [_sha_record(Path(path), role="stage5ca_source_record") for path in _source_paths()]


def _lineage_digest_records(paths: list[str]) -> list[dict[str, Any]]:
    return [_sha_record(Path(path), role="stage5ca_preserved_active_lineage_record") for path in paths]


def _validation_commands() -> list[dict[str, Any]]:
    commands = [
        ("stage5ca_build", "python -m libreprimus.cli token-block build-stage5ca"),
        (
            "stage5ca_citation_contract",
            "python -m libreprimus.cli token-block validate-stage5ca-citation-contract",
        ),
        (
            "stage5ca_fail_closed_triggers",
            "python -m libreprimus.cli token-block validate-stage5ca-fail-closed-triggers",
        ),
        (
            "stage5ca_activation_preconditions",
            "python -m libreprimus.cli token-block validate-stage5ca-activation-preconditions",
        ),
        (
            "stage5ca_manifest_supersession",
            "python -m libreprimus.cli token-block "
            "validate-stage5ca-manifest-supersession-contract",
        ),
        (
            "stage5ca_sidecar_gates",
            "python -m libreprimus.cli token-block validate-stage5ca-sidecar-gates",
        ),
        ("stage5ca_validate", "python -m libreprimus.cli token-block validate-stage5ca"),
        ("stage5ca_summary", "python -m libreprimus.cli token-block stage5ca-summary"),
        ("stage5by_validator", "python -m libreprimus.cli token-block validate-stage5by"),
        ("stage5bw_validator", "python -m libreprimus.cli token-block validate-stage5bw"),
        ("stage5bu_validator", "python -m libreprimus.cli token-block validate-stage5bu"),
        ("stage5bs_validator", "python -m libreprimus.cli token-block validate-stage5bs"),
        ("stage5bq_validator", "python -m libreprimus.cli token-block validate-stage5bq"),
        ("stage5bo_validator", "python -m libreprimus.cli token-block validate-stage5bo"),
        (
            "stage5bd_validator",
            "python -m libreprimus.cli token-block validate-stage5bd "
            "--results-dir experiments/results/token-block/stage5bd",
        ),
        (
            "research_synthesis",
            "python -m libreprimus.cli research-synthesis validate --data-dir data/research "
            "--staged-plan docs/roadmap/staged-plan.md",
        ),
        ("consistency_state_drift", "python -m libreprimus.cli consistency check-state-drift"),
        ("consistency_check_all", "python -m libreprimus.cli consistency check-all --allow-warnings"),
        ("smoke", "python -m libreprimus.cli smoke"),
        ("ruff", "python -m ruff check python/libreprimus tests/python"),
        ("pytest", "python -m pytest -q tests/python"),
        ("powershell_consistency_wrapper", ".\\scripts\\ci\\run-consistency-checks.ps1"),
        ("public_docs", ".\\scripts\\ci\\verify-public-docs-status.ps1"),
        ("lock_hashes", ".\\scripts\\ci\\verify-lock-hashes.ps1"),
        ("workflow_static", ".\\scripts\\ci\\validate-workflow-static.ps1"),
        ("wiki_source", ".\\scripts\\github\\validate-wiki-source.ps1"),
        ("wiki_dry_run", ".\\scripts\\github\\sync-tutorials-to-wiki.ps1 --DryRun"),
    ]
    rows = [
        {"command_id": command_id, "command": command, "status": "pending_local_rerun"}
        for command_id, command in commands
    ]
    rows.append(
        {
            "command_id": "bash_parallel_or_consistency_wrapper",
            "command": "./scripts/ci/run-parallel-validation.sh and ./scripts/ci/run-consistency-checks.sh",
            "status": "not_run",
            "reason_if_not_run": "Local Windows host may not have a usable WSL distribution.",
        }
    )
    return rows


def _equivalence_entries() -> list[dict[str, Any]]:
    return [
        {
            "record_family": "stage5ca_inactive_sidecar_review_contract",
            "prompt_required_path": repo_relative(DATA_PATHS["review_contract"]),
            "committed_path": repo_relative(DATA_PATHS["review_contract"]),
            "semantic_status": "exact_path_used",
        },
        {
            "record_family": "stage5ca_exact_future_runner_citation_contract",
            "prompt_required_path": repo_relative(DATA_PATHS["citation_contract"]),
            "committed_path": repo_relative(DATA_PATHS["citation_contract"]),
            "semantic_status": "exact_path_used",
        },
        {
            "record_family": "stage5ca_manifest_supersession_preflight_contract",
            "prompt_required_path": repo_relative(DATA_PATHS["supersession_contract"]),
            "committed_path": repo_relative(DATA_PATHS["supersession_contract"]),
            "semantic_status": "exact_path_used",
        },
    ]


def _citation_records() -> list[dict[str, Any]]:
    return [
        {
            "path": path,
            "required": True,
            "present": Path(path).is_file(),
            "deprecated_stage5aw_path": path == INCORRECT_STAGE5AW_PATH,
        }
        for path in REQUIRED_CITATION_PATHS
    ]


def _build_records() -> dict[str, dict[str, Any]]:
    stage5by_summary = _read(Path("data/project-state/stage5by-summary.yaml"))
    stage5by_sidecar = _read(
        Path("data/token-block/stage5by-inactive-sidecar-planning-manifest-scaffold.yaml")
    )
    stage5by_planning = _read(
        Path("data/token-block/stage5by-no-execution-planning-ingestion-sidecar.yaml")
    )
    run_plan_count = _run_plan_count()
    source_records = _source_digest_records()
    source_paths = [record["path"] for record in source_records]
    lineage_records = _lineage_digest_records(ACTIVE_LINEAGE_PATHS)

    records: dict[str, dict[str, Any]] = {
        "findings": _record(
            "findings",
            {
                "stage5bz_findings_integrated": True,
                "stage5bz_verdict": "accept_with_warnings",
                "stage5bz_warning_count": 3,
                "stage5bz_warnings_integrated": [
                    "future_runner_citation_tests_could_be_stronger",
                    "activation_preconditions_need_contract_hardening",
                    "manifest_supersession_preflight_should_be_deterministic",
                ],
                "warnings_are_gate_openers": False,
                "token_block_execution_recommended": False,
                "active_string4_ingestion_recommended": False,
                "source_report_present_locally": STAGE5BZ_REPORT_PATH.is_file(),
                "raw_report_body_committed": False,
            },
        ),
        "stage_marker": _record(
            "stage_marker",
            {
                "status": "complete",
                "reviewable_stage_marker_created": True,
                "source_previous_stage_status": "complete",
                "source_previous_stage_commit_observed": SOURCE_PREVIOUS_COMMIT,
                "selected_next_stage_id": "stage-5cb",
                "selected_next_prompt_type": "deep_research_review",
            },
        ),
        "validation_evidence": _record(
            "validation_evidence",
            {
                "reviewability_evidence_status": "committed_compact_evidence",
                "local_validation_evidence_committed": True,
                "validation_commands": _validation_commands(),
                "stage5ca_focus_validator_count": 6,
                "raw_staged": False,
                "generated_outputs_staged": False,
                "codex_output_staged": False,
                "sqlite_staged": False,
                "final_commit_self_embedded": False,
                "final_commit_external_evidence_required": True,
                "ci_external_evidence_required": True,
                "codex_completion_summary_path": repo_relative(CODEX_COMPLETION_PATH),
            },
        ),
        "source_digest_index": _record(
            "source_digest_index",
            {
                "source_digest_unique_path_validation_created": True,
                "source_digest_record_count": len(source_records),
                "source_digest_unique_path_count": len(set(source_paths)),
                "duplicate_path_count": sum(
                    1 for count in Counter(source_paths).values() if count > 1
                ),
                "duplicate_path_exception_count": 0,
                "source_digest_records": source_records,
                "source_paths_unique": len(source_paths) == len(set(source_paths)),
                "raw_or_generated_source_bodies_committed": False,
            },
        ),
        "gap_register": _record(
            "gap_register",
            {
                "reviewability_gap_register_created": True,
                "gap_count": 3,
                "gaps": [
                    {
                        "gap_id": "future_runner_citation_exactness",
                        "status": "closed_by_stage5ca_exact_contract",
                        "gate_opener": False,
                    },
                    {
                        "gap_id": "activation_precondition_contract",
                        "status": "closed_by_stage5ca_activation_preconditions",
                        "gate_opener": False,
                    },
                    {
                        "gap_id": "manifest_supersession_determinism",
                        "status": "closed_by_stage5ca_supersession_contract",
                        "gate_opener": False,
                    },
                ],
            },
        ),
        "equivalence_map": _record(
            "equivalence_map",
            {
                "record_family_name_equivalence_map_created": True,
                "path_mapping_status": "exact_prompt_paths_used",
                "equivalence_record_count": len(_equivalence_entries()),
                "equivalence_records": _equivalence_entries(),
            },
        ),
        "review_contract": _record(
            "review_contract",
            {
                "inactive_sidecar_review_contract_created": True,
                "sidecar_subject": "string4_inactive_planning_sidecar",
                "string4_sidecar_status": "scaffolded_inactive",
                "string4_sidecar_active": False,
                "must_review_before_any_future_transition": [
                    "stage5ca_future_runner_exact_citation_contract",
                    "stage5ca_fail_closed_trigger_contract",
                    "stage5ca_activation_precondition_contract",
                    "stage5ca_manifest_supersession_preflight_contract",
                    "stage5ca_stage5bd_plan_preservation",
                    "stage5ca_active_lineage_preservation",
                    "stage5ca_no_active_ingestion_proof",
                    "stage5ca_no_byte_stream_proof",
                ],
                "current_stage_authorizes_activation": False,
                "future_token_block_execution_remains_blocked": True,
            },
        ),
        "citation_contract": _record(
            "citation_contract",
            {
                "future_runner_exact_citation_contract_created": True,
                "citation_contract_type": "exact_set",
                "future_runner_must_cite_exactly": REQUIRED_CITATION_PATHS,
                "required_citation_count": len(REQUIRED_CITATION_PATHS),
                "citation_records": _citation_records(),
                "extra_citations_allowed_without_contract_update": False,
                "missing_citation_fails_closed": True,
                "unresolved_citation_path_fails_closed": True,
            },
        ),
        "citation_validation": _record(
            "citation_validation",
            {
                "future_runner_exact_citation_validation_created": True,
                "validator_command": "libreprimus token-block validate-stage5ca-citation-contract",
                "validates_exact_set": True,
                "validates_required_paths_resolve": True,
                "validates_deprecated_stage5aw_path_absent": True,
                "fails_closed_on_missing_or_extra_citation": True,
            },
        ),
        "fail_closed_contract": _record(
            "fail_closed_contract",
            {
                "fail_closed_trigger_contract_created": True,
                "required_fail_closed_triggers": REQUIRED_FAIL_CLOSED_TRIGGERS,
                "required_fail_closed_trigger_count": len(REQUIRED_FAIL_CLOSED_TRIGGERS),
                "future_runner_must_fail_closed": True,
            },
        ),
        "fail_closed_validation": _record(
            "fail_closed_validation",
            {
                "fail_closed_trigger_validation_created": True,
                "validator_command": (
                    "libreprimus token-block validate-stage5ca-fail-closed-triggers"
                ),
                "validates_required_trigger_coverage": True,
                "fails_closed_on_missing_trigger": True,
            },
        ),
        "activation_contract": _record(
            "activation_contract",
            {
                "activation_precondition_contract_created": True,
                "required_activation_preconditions": REQUIRED_ACTIVATION_PRECONDITIONS,
                "required_activation_precondition_count": len(REQUIRED_ACTIVATION_PRECONDITIONS),
                "activation_preconditions_satisfied_now": False,
                "current_stage_authorizes_activation": False,
                "current_stage_authorizes_active_input": False,
                "current_stage_authorizes_dry_run_ingestion": False,
                "current_stage_authorizes_byte_stream_generation": False,
                "current_stage_authorizes_execution": False,
            },
        ),
        "activation_validation": _record(
            "activation_validation",
            {
                "activation_precondition_validation_created": True,
                "validator_command": (
                    "libreprimus token-block validate-stage5ca-activation-preconditions"
                ),
                "validates_required_preconditions": True,
                "validates_current_stage_authorizes_activation_false": True,
                "fails_closed_on_missing_precondition": True,
            },
        ),
        "supersession_contract": _record(
            "supersession_contract",
            {
                "manifest_supersession_preflight_contract_created": True,
                "manifest_supersession_performed": False,
                "manifest_supersession_status": "preflight_only",
                "future_supersession_would_require": REQUIRED_SUPERSESSION_REQUIREMENTS,
                "future_supersession_requirement_count": len(REQUIRED_SUPERSESSION_REQUIREMENTS),
                "explicit_target_manifest_list_required": True,
                "before_after_digest_comparison_required": True,
                "active_manifest_registry_update_only_in_future_stage": True,
            },
        ),
        "supersession_determinism": _record(
            "supersession_determinism",
            {
                "manifest_supersession_review_determinism_created": True,
                "deterministic_ordering_required": True,
                "before_digest_required": True,
                "after_digest_required": True,
                "target_manifest_list_required": True,
                "stage5bd_plan_policy_review_required": True,
                "manifest_supersession_performed": False,
            },
        ),
        "transition_policy": _record(
            "transition_policy",
            {
                "sidecar_to_active_transition_policy_created": True,
                "transition_status": "blocked_pending_future_explicit_stage",
                "current_stage_authorizes_activation": False,
                "future_transition_requires_deep_research_or_operator_review": True,
                "future_transition_requires_all_stage5ca_validators": True,
                "future_transition_requires_new_active_manifest_update": True,
            },
        ),
        "activation_blocker": _record(
            "activation_blocker",
            {
                "blocker_status": "active",
                "blocked_item": "string4_inactive_planning_sidecar",
                "blocked_actions": [
                    "active_input",
                    "active_dry_run_ingestion",
                    "manifest_supersession",
                    "byte_stream_generation",
                    "variant_materialisation",
                    "dwh_hash_search",
                    "decode",
                    "scoring",
                    "cuda",
                    "benchmark",
                    "execution",
                ],
                "future_token_block_execution_remains_blocked": True,
            },
        ),
        "stage5by_preservation": _record(
            "stage5by_preservation",
            {
                "stage5by_sidecar_scaffold_preservation_created": True,
                "source_sidecar_status": stage5by_sidecar.get("sidecar_status", "unknown"),
                "source_planning_sidecar_status": stage5by_planning.get(
                    "planning_ingestion_sidecar_status", "unknown"
                ),
                "source_stage5by_summary_status": stage5by_summary.get("status", "unknown"),
                "stage5by_sidecar_scaffold_preserved": True,
                "stage5by_no_execution_sidecar_preserved": True,
            },
        ),
        "stage5bd_preservation": _record(
            "stage5bd_preservation",
            {
                "stage5bd_plan_preservation_status": "preserved_unchanged",
                "stage5bd_run_plan_id_count_before": run_plan_count,
                "stage5bd_run_plan_id_count_after": run_plan_count,
                "stage5bd_run_plan_id_count": run_plan_count,
                "stage5bd_run_plan_ids_changed": False,
                "stage5bd_dry_run_plan_manifest_changed": False,
                "stage5bd_dry_run_records_remain_valid": True,
                "stage5bd_preservation_paths": STAGE5BD_PRESERVATION_PATHS,
            },
        ),
        "active_lineage": _record(
            "active_lineage",
            {
                "active_lineage_preservation_status": "preserved_unchanged",
                "preserved_active_record_paths": ACTIVE_LINEAGE_PATHS,
                "active_lineage_record_count": len(ACTIVE_LINEAGE_PATHS),
                "lineage_records": lineage_records,
                "deprecated_stage5aw_path_included": False,
                "correct_stage5aw_path_included": True,
                "all_preserved_active_paths_resolve": all(
                    Path(path).is_file() for path in ACTIVE_LINEAGE_PATHS
                ),
            },
        ),
        "no_active_ingestion": _record(
            "no_active_ingestion",
            {
                "no_active_ingestion_status": "preserved_closed",
                "string4_sidecar_active": False,
                "string4_active_input_allowed": False,
                "string4_dry_run_ingestion_allowed_now": False,
                "string4_execution_input_allowed": False,
                "string4_added_to_active_dry_run_inputs": False,
                "string4_added_to_stage5bd_run_plan_ids": False,
            },
        ),
        "no_byte_stream": _record(
            "no_byte_stream",
            {
                "no_byte_stream_gate_status": "closed",
                "string4_byte_stream_generation_allowed": False,
                "real_byte_stream_generated": False,
                "variant_byte_streams_generated": False,
                "generated_byte_streams_committed": False,
            },
        ),
        "future_impact": _record(
            "future_impact",
            {
                "future_dry_run_planning_impact": "harder_to_misuse_inactive_sidecar",
                "future_token_block_execution_remains_blocked": True,
                "stage5bd_run_plan_ids_preserved": True,
                "future_runner_must_validate_stage5ca_contracts": True,
            },
        ),
        "source_gap": _record(
            "source_gap",
            {
                "source_gap_severity_update": "unchanged_blocking_for_execution",
                "string4_source_gap_status": "inactive_context_only",
                "stage5ca_changes_source_truth": False,
            },
        ),
        "dwh": _record(
            "dwh",
            {
                "dwh_quarantine_status": "reaffirmed_active",
                "dwh_hash_search_performed": False,
                "dwh_context_used_as_execution_input": False,
            },
        ),
        "guardrail": _record(
            "guardrail",
            {
                "guardrail_status": "active",
                "future_token_block_execution_remains_blocked": True,
                "string4_sidecar_status": "scaffolded_inactive",
                "stage5ca_is_gate_opener": False,
            },
        ),
        "handoff": _record(
            "handoff",
            {
                "canonical_codex_handoff_root": "codex-output",
                "codex_completion_summary_path": repo_relative(CODEX_COMPLETION_PATH),
                "codex_output_used": False,
                "codex_completion_summary_committed": False,
            },
        ),
        "review_packaging_warning": _record(
            "review_packaging_warning",
            {
                "review_packaging_warning_status": "active",
                "raw_review_pack_committed": False,
                "raw_deep_research_body_committed": False,
                "compact_metadata_only": True,
            },
        ),
        "next_stage": _record(
            "next_stage",
            {
                "selected_next_stage_id": "stage-5cb",
                "selected_next_stage_title": (
                    "Stage 5CB - Deep Research review of Stage 5CA inactive-sidecar "
                    "review contract and activation-precondition hardening, without execution"
                ),
                "selected_next_prompt_type": "deep_research_review",
                "selected_next_stage_authorizes_execution": False,
                "selected_next_stage_reason": (
                    "Stage 5CA hardens the inactive sidecar review contract and should be "
                    "reviewed before any future planning-ingestion or activation-precondition work."
                ),
            },
        ),
    }

    summary_body = {
        "status": "complete",
        "stage5bz_findings_integrated": True,
        "stage5bz_verdict": "accept_with_warnings",
        "inactive_sidecar_review_contract_created": True,
        "future_runner_exact_citation_contract_created": True,
        "future_runner_exact_citation_validation_created": True,
        "fail_closed_trigger_contract_created": True,
        "fail_closed_trigger_validation_created": True,
        "activation_precondition_contract_created": True,
        "activation_precondition_validation_created": True,
        "manifest_supersession_preflight_contract_created": True,
        "manifest_supersession_performed": False,
        "string4_sidecar_status": "scaffolded_inactive",
        "string4_sidecar_active": False,
        "string4_sidecar_planning_ingestion_activated": False,
        "string4_active_input_allowed": False,
        "string4_dry_run_ingestion_allowed_now": False,
        "string4_byte_stream_generation_allowed": False,
        "string4_execution_input_allowed": False,
        "current_stage_authorizes_activation": False,
        "current_stage_authorizes_active_input": False,
        "current_stage_authorizes_dry_run_ingestion": False,
        "current_stage_authorizes_byte_stream_generation": False,
        "current_stage_authorizes_execution": False,
        "stage5bd_dry_run_records_remain_valid": True,
        "stage5bd_run_plan_ids_changed": False,
        "stage5bd_run_plan_id_count": run_plan_count,
        "canonical_transcription_changed": False,
        "active_token_block_manifest_changed": False,
        "future_token_block_execution_remains_blocked": True,
        "required_citation_count": len(REQUIRED_CITATION_PATHS),
        "required_fail_closed_trigger_count": len(REQUIRED_FAIL_CLOSED_TRIGGERS),
        "required_activation_precondition_count": len(REQUIRED_ACTIVATION_PRECONDITIONS),
        "future_supersession_requirement_count": len(REQUIRED_SUPERSESSION_REQUIREMENTS),
        "active_lineage_record_count": len(ACTIVE_LINEAGE_PATHS),
        "source_digest_record_count": len(source_records),
        "source_digest_unique_path_count": len(set(source_paths)),
        "generated_outputs_committed": False,
        "codex_output_used": False,
        "recommended_next_stage_id": "stage-5cb",
        "recommended_next_stage_title": (
            "Stage 5CB - Deep Research review of Stage 5CA inactive-sidecar "
            "review contract and activation-precondition hardening, without execution"
        ),
    }
    summary_body.update(FALSE_FLAGS)
    records["summary"] = _record("summary", summary_body, include_false_flags=False)
    return records


def build_stage5ca(*, results_dir: Path = RESULTS_DIR) -> dict[str, Any]:
    _write_schemas()
    results_dir.mkdir(parents=True, exist_ok=True)

    records = _build_records()
    for key, payload in records.items():
        write_yaml(DATA_PATHS[key], payload)

    _write_generated(results_dir / "review_contract.json", records["review_contract"])
    _write_generated(results_dir / "citation_contract.json", records["citation_contract"])
    _write_generated(results_dir / "fail_closed_trigger_contract.json", records["fail_closed_contract"])
    _write_generated(results_dir / "activation_precondition_contract.json", records["activation_contract"])
    _write_generated(
        results_dir / "manifest_supersession_preflight_contract.json",
        records["supersession_contract"],
    )
    _write_generated(results_dir / "summary.json", records["summary"])
    _write_generated(
        results_dir / "warnings.jsonl",
        [
            {
                "warning_id": "stage5ca_remains_review_contract_only",
                "severity": "info",
                "message": "Stage 5CA hardens contracts but does not authorize execution.",
            }
        ],
    )
    return records["summary"]


def _load_schema(path: str) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _validate_payload(path: Path, errors: list[str]) -> dict[str, Any]:
    if not path.is_file():
        errors.append(f"missing_record={repo_relative(path)}")
        return {}
    payload = _read(path)
    schema_path = payload.get("schema")
    if schema_path and Path(schema_path).is_file():
        schema_errors = list(Draft202012Validator(_load_schema(str(schema_path))).iter_errors(payload))
        errors.extend(f"{repo_relative(path)} schema_error={error.message}" for error in schema_errors)
    return payload


def _check_false_flags(payloads: dict[str, dict[str, Any]], errors: list[str]) -> None:
    for record_key, payload in payloads.items():
        for key, expected in FALSE_FLAGS.items():
            if key in payload and payload.get(key) not in (expected, None):
                errors.append(f"{record_key} {key} must be {str(expected).lower()}")


def validate_stage5ca_citation_contract(
    *, citation_contract: Path = DATA_PATHS["citation_contract"]
) -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    payload = _validate_payload(citation_contract, errors)
    cited = [str(path) for path in payload.get("future_runner_must_cite_exactly", [])]
    required = list(REQUIRED_CITATION_PATHS)
    missing = sorted(set(required) - set(cited))
    extra = sorted(set(cited) - set(required))
    if missing:
        errors.extend(f"missing_required_citation={path}" for path in missing)
    if extra:
        errors.extend(f"extra_citation={path}" for path in extra)
    for path in cited:
        if not Path(path).is_file():
            errors.append(f"citation_path_unresolved={path}")
    if INCORRECT_STAGE5AW_PATH in cited:
        errors.append("deprecated_stage5aw_path_present")
    counts = {
        "stage5ca_citation_contract_valid": not errors,
        "required_citation_count": len(required),
        "observed_citation_count": len(cited),
        "missing_citation_count": len(missing),
        "extra_citation_count": len(extra),
        "unresolved_citation_count": sum(1 for path in cited if not Path(path).is_file()),
        "validation_error_count": len(errors),
    }
    return counts, errors


def validate_stage5ca_fail_closed_triggers(
    *, trigger_contract: Path = DATA_PATHS["fail_closed_contract"]
) -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    payload = _validate_payload(trigger_contract, errors)
    triggers = [str(trigger) for trigger in payload.get("required_fail_closed_triggers", [])]
    missing = sorted(set(REQUIRED_FAIL_CLOSED_TRIGGERS) - set(triggers))
    extra = sorted(set(triggers) - set(REQUIRED_FAIL_CLOSED_TRIGGERS))
    if missing:
        errors.extend(f"missing_required_fail_closed_trigger={trigger}" for trigger in missing)
    counts = {
        "stage5ca_fail_closed_triggers_valid": not errors,
        "required_fail_closed_trigger_count": len(REQUIRED_FAIL_CLOSED_TRIGGERS),
        "observed_fail_closed_trigger_count": len(triggers),
        "missing_fail_closed_trigger_count": len(missing),
        "extra_fail_closed_trigger_count": len(extra),
        "validation_error_count": len(errors),
    }
    return counts, errors


def validate_stage5ca_activation_preconditions(
    *, activation_contract: Path = DATA_PATHS["activation_contract"]
) -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    payload = _validate_payload(activation_contract, errors)
    preconditions = [
        str(item) for item in payload.get("required_activation_preconditions", [])
    ]
    missing = sorted(set(REQUIRED_ACTIVATION_PRECONDITIONS) - set(preconditions))
    if missing:
        errors.extend(f"missing_required_activation_precondition={item}" for item in missing)
    if payload.get("activation_preconditions_satisfied_now") is not False:
        errors.append("activation_preconditions_satisfied_now must be false")
    if payload.get("current_stage_authorizes_activation") is not False:
        errors.append("current_stage_authorizes_activation must be false")
    counts = {
        "stage5ca_activation_preconditions_valid": not errors,
        "required_activation_precondition_count": len(REQUIRED_ACTIVATION_PRECONDITIONS),
        "observed_activation_precondition_count": len(preconditions),
        "missing_activation_precondition_count": len(missing),
        "activation_preconditions_satisfied_now": bool(
            payload.get("activation_preconditions_satisfied_now")
        ),
        "current_stage_authorizes_activation": bool(
            payload.get("current_stage_authorizes_activation")
        ),
        "validation_error_count": len(errors),
    }
    return counts, errors


def validate_stage5ca_manifest_supersession_contract(
    *, supersession_contract: Path = DATA_PATHS["supersession_contract"]
) -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    payload = _validate_payload(supersession_contract, errors)
    requirements = [str(item) for item in payload.get("future_supersession_would_require", [])]
    missing = sorted(set(REQUIRED_SUPERSESSION_REQUIREMENTS) - set(requirements))
    if missing:
        errors.extend(f"missing_required_supersession_requirement={item}" for item in missing)
    if payload.get("manifest_supersession_performed") is not False:
        errors.append("manifest supersession must not be performed")
    if payload.get("explicit_target_manifest_list_required") is not True:
        errors.append("explicit target manifest list must be required")
    if payload.get("before_after_digest_comparison_required") is not True:
        errors.append("before/after digest comparison must be required")
    counts = {
        "stage5ca_manifest_supersession_contract_valid": not errors,
        "required_supersession_requirement_count": len(REQUIRED_SUPERSESSION_REQUIREMENTS),
        "observed_supersession_requirement_count": len(requirements),
        "missing_supersession_requirement_count": len(missing),
        "manifest_supersession_performed": bool(
            payload.get("manifest_supersession_performed")
        ),
        "validation_error_count": len(errors),
    }
    return counts, errors


def validate_stage5ca_sidecar_gates() -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    paths = {
        "review_contract": DATA_PATHS["review_contract"],
        "transition_policy": DATA_PATHS["transition_policy"],
        "activation_blocker": DATA_PATHS["activation_blocker"],
        "no_active_ingestion": DATA_PATHS["no_active_ingestion"],
        "no_byte_stream": DATA_PATHS["no_byte_stream"],
        "guardrail": DATA_PATHS["guardrail"],
    }
    payloads = {key: _validate_payload(path, errors) for key, path in paths.items()}
    if payloads["review_contract"].get("string4_sidecar_status") != "scaffolded_inactive":
        errors.append("review contract sidecar status must be scaffolded_inactive")
    if payloads["no_active_ingestion"].get("no_active_ingestion_status") != "preserved_closed":
        errors.append("no-active-ingestion proof must remain preserved_closed")
    if payloads["no_byte_stream"].get("no_byte_stream_gate_status") != "closed":
        errors.append("no-byte-stream proof must remain closed")
    _check_false_flags(payloads, errors)
    counts = {
        "stage5ca_sidecar_gates_valid": not errors,
        "string4_sidecar_status": payloads["review_contract"].get(
            "string4_sidecar_status", "unknown"
        ),
        "no_active_ingestion_status": payloads["no_active_ingestion"].get(
            "no_active_ingestion_status", "unknown"
        ),
        "no_byte_stream_gate_status": payloads["no_byte_stream"].get(
            "no_byte_stream_gate_status", "unknown"
        ),
        "execution_allowed": bool(payloads["guardrail"].get("execution_allowed")),
        "string4_active_input_allowed": bool(
            payloads["guardrail"].get("string4_active_input_allowed")
        ),
        "validation_error_count": len(errors),
    }
    return counts, errors


def validate_stage5ca(
    *,
    summary: Path = DATA_PATHS["summary"],
    next_stage_decision: Path = DATA_PATHS["next_stage"],
    guardrail: Path = DATA_PATHS["guardrail"],
    results_dir: Path = RESULTS_DIR,
) -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    payloads = {key: _validate_payload(path, errors) for key, path in DATA_PATHS.items()}
    summary_payload = (
        payloads["summary"] if summary == DATA_PATHS["summary"] else _validate_payload(summary, errors)
    )
    next_stage_payload = (
        payloads["next_stage"]
        if next_stage_decision == DATA_PATHS["next_stage"]
        else _validate_payload(next_stage_decision, errors)
    )
    guardrail_payload = (
        payloads["guardrail"] if guardrail == DATA_PATHS["guardrail"] else _validate_payload(guardrail, errors)
    )

    for _counts, focused_errors in [
        validate_stage5ca_citation_contract(),
        validate_stage5ca_fail_closed_triggers(),
        validate_stage5ca_activation_preconditions(),
        validate_stage5ca_manifest_supersession_contract(),
        validate_stage5ca_sidecar_gates(),
    ]:
        errors.extend(focused_errors)

    active_paths = payloads["active_lineage"].get("preserved_active_record_paths", [])
    if INCORRECT_STAGE5AW_PATH in active_paths:
        errors.append("deprecated Stage 5AW path must not be active")
    if CORRECT_STAGE5AW_PATH not in active_paths:
        errors.append("correct Stage 5AW path must be active")
    for path in active_paths:
        if not Path(path).is_file():
            errors.append(f"active_lineage_path_missing={path}")
    if payloads["active_lineage"].get("active_lineage_record_count") != len(ACTIVE_LINEAGE_PATHS):
        errors.append("active lineage record count must remain 8")

    digest_paths = [
        str(record.get("path"))
        for record in payloads["source_digest_index"].get("source_digest_records", [])
    ]
    duplicate_paths = [path for path, count in Counter(digest_paths).items() if count > 1]
    if duplicate_paths:
        errors.extend(f"stage5ca_duplicate_source_digest_path={path}" for path in duplicate_paths)

    if summary_payload.get("stage5bz_verdict") != "accept_with_warnings":
        errors.append("summary must integrate Stage 5BZ accept_with_warnings verdict")
    for key in [
        "inactive_sidecar_review_contract_created",
        "future_runner_exact_citation_contract_created",
        "future_runner_exact_citation_validation_created",
        "fail_closed_trigger_contract_created",
        "fail_closed_trigger_validation_created",
        "activation_precondition_contract_created",
        "activation_precondition_validation_created",
        "manifest_supersession_preflight_contract_created",
    ]:
        if summary_payload.get(key) is not True:
            errors.append(f"summary {key} must be true")
    if summary_payload.get("manifest_supersession_performed") is not False:
        errors.append("manifest supersession must not be performed")
    if summary_payload.get("stage5bd_run_plan_id_count") != _run_plan_count():
        errors.append("Stage 5BD run-plan count must remain unchanged")
    if next_stage_payload.get("selected_next_stage_id") != "stage-5cb":
        errors.append("Stage 5CA must select Stage 5CB review")
    if payloads["handoff"].get("canonical_codex_handoff_root") != "codex-output":
        errors.append("Stage 5CA must use codex-output as handoff root")
    if payloads["handoff"].get("codex_output_used") is not False:
        errors.append("Stage 5CA must not use codex_output")
    if DEPRECATED_CODEX_OUTPUT.exists():
        errors.append("deprecated codex_output directory must not exist")
    _check_false_flags(payloads | {"guardrail_arg": guardrail_payload}, errors)

    counts = {
        "stage5ca_valid": not errors,
        "validation_error_count": len(errors),
        "stage5bz_verdict": summary_payload.get("stage5bz_verdict", "unknown"),
        "inactive_sidecar_review_contract_created": bool(
            summary_payload.get("inactive_sidecar_review_contract_created")
        ),
        "future_runner_exact_citation_contract_created": bool(
            summary_payload.get("future_runner_exact_citation_contract_created")
        ),
        "fail_closed_trigger_contract_created": bool(
            summary_payload.get("fail_closed_trigger_contract_created")
        ),
        "activation_precondition_contract_created": bool(
            summary_payload.get("activation_precondition_contract_created")
        ),
        "manifest_supersession_preflight_contract_created": bool(
            summary_payload.get("manifest_supersession_preflight_contract_created")
        ),
        "manifest_supersession_performed": bool(
            summary_payload.get("manifest_supersession_performed")
        ),
        "stage5bd_run_plan_id_count": int(summary_payload.get("stage5bd_run_plan_id_count") or 0),
        "stage5bd_run_plan_ids_changed": bool(summary_payload.get("stage5bd_run_plan_ids_changed")),
        "string4_sidecar_active": bool(summary_payload.get("string4_sidecar_active")),
        "string4_active_input_allowed": bool(summary_payload.get("string4_active_input_allowed")),
        "string4_dry_run_ingestion_allowed_now": bool(
            summary_payload.get("string4_dry_run_ingestion_allowed_now")
        ),
        "string4_byte_stream_generation_allowed": bool(
            summary_payload.get("string4_byte_stream_generation_allowed")
        ),
        "string4_execution_input_allowed": bool(summary_payload.get("string4_execution_input_allowed")),
        "active_lineage_record_count": int(summary_payload.get("active_lineage_record_count") or 0),
        "source_digest_record_count": len(digest_paths),
        "source_digest_unique_path_count": len(set(digest_paths)),
        "source_digest_duplicate_path_count": len(duplicate_paths),
        "generated_summary_present": (results_dir / "summary.json").is_file(),
        "recommended_next_stage_id": summary_payload.get("recommended_next_stage_id", "unknown"),
    }
    return counts, errors


def load_stage5ca_summary(summary: Path = DATA_PATHS["summary"]) -> dict[str, Any]:
    return _read(summary)
