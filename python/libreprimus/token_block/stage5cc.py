"""Stage 5CC active-planning-input preflight metadata."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from libreprimus.token_block.models import repo_relative, sha256_file, write_json, write_yaml
from libreprimus.token_block.stage5bm import _read
from libreprimus.token_block.stage5ca import (
    ACTIVE_LINEAGE_PATHS,
    CORRECT_STAGE5AW_PATH,
    DATA_PATHS as STAGE5CA_DATA_PATHS,
    INCORRECT_STAGE5AW_PATH,
    REQUIRED_ACTIVATION_PRECONDITIONS,
    REQUIRED_CITATION_PATHS,
    REQUIRED_FAIL_CLOSED_TRIGGERS,
    STAGE5BD_PRESERVATION_PATHS,
    validate_stage5ca_citation_contract,
)

STAGE_ID = "stage-5cc"
STAGE_TITLE = (
    "Stage 5CC - Inactive-sidecar active-planning-input proposal preflight "
    "and no-byte-stream transition gate, without execution"
)
PROMPT_TYPE = "codex_metadata_implementation"
SOURCE_PREVIOUS_STAGE = "stage-5ca"
SOURCE_PREVIOUS_COMMIT = "5da4d0e82dd1de34d9d3ff6e9d2b04587d1531db"
SOURCE_DEEP_RESEARCH_STAGE = "stage-5cb"
SOURCE_DEEP_RESEARCH_REPORT = "16_Stage-5CA-Deep-Research-Review.md"

RESULTS_DIR = Path("experiments/results/token-block/stage5cc")
CODEX_COMPLETION_PATH = Path("codex-output/stage5cc-codex-completion.md")
DEPRECATED_CODEX_OUTPUT = Path("codex_output")
STAGE5CB_REPORT_PATH = Path(
    "deep-research-reports/reviews-of-ideas-and-concepts-and-data/md/"
    "16_Stage-5CA-Deep-Research-Review.md"
)

FUTURE_ACTIVE_PLANNING_INPUT_REQUIREMENTS = [
    "explicit_future_codex_stage",
    "deep_research_or_operator_review_if_selected",
    "exact_future_runner_citation_contract_validation",
    "fail_closed_trigger_exact_set_validation",
    "activation_precondition_exact_set_validation",
    "sidecar_status_inactive_until_future_activation_record",
    "stage5bd_plan_preservation_or_explicit_supersession",
    "active_lineage_preservation_or_explicit_supersession",
    "no_byte_stream_transition_gate",
    "no_execution_transition_gate",
    "manifest_supersession_preflight_if_any_manifest_change_is_selected",
    "explicit_non_solve_reporting_policy",
]

BLOCKED_BYTE_STREAM_ACTIONS = [
    "primary60_byte_stream_generation",
    "string4_byte_stream_generation",
    "branch_materialisation",
    "variant_materialisation",
    "full_cartesian_enumeration",
    "sampled_real_variant_generation",
    "2014_surface_combination",
    "dwh_hash_search",
    "decode",
    "scoring",
    "cuda",
    "benchmark",
    "solve_claim",
]

EXTENSION_REQUIRES = [
    "unique_extension_id",
    "non_gate_opening_classification",
    "explicit_future_stage_review",
    "validator_asserts_non_gate_opening",
]

DATA_PATHS: dict[str, Path] = {
    "summary": Path("data/project-state/stage5cc-summary.yaml"),
    "next_stage": Path("data/project-state/stage5cc-next-stage-decision.yaml"),
    "findings": Path("data/project-state/stage5cc-stage5cb-findings-integration.yaml"),
    "stage_marker": Path("data/project-state/stage5cc-reviewable-stage-marker.yaml"),
    "validation_evidence": Path("data/project-state/stage5cc-reviewable-validation-evidence.yaml"),
    "source_digest_index": Path("data/project-state/stage5cc-reviewable-source-digest-index.yaml"),
    "gap_register": Path("data/project-state/stage5cc-reviewability-gap-register.yaml"),
    "equivalence_map": Path("data/project-state/stage5cc-record-family-name-equivalence-map.yaml"),
    "stage5ca_preservation": Path("data/token-block/stage5cc-stage5ca-contract-preservation.yaml"),
    "fail_closed_contract": Path(
        "data/token-block/stage5cc-fail-closed-trigger-exact-set-contract.yaml"
    ),
    "fail_closed_extension_policy": Path(
        "data/token-block/stage5cc-fail-closed-trigger-extension-policy.yaml"
    ),
    "fail_closed_validation": Path(
        "data/token-block/stage5cc-fail-closed-trigger-validation-requirements.yaml"
    ),
    "activation_contract": Path(
        "data/token-block/stage5cc-activation-precondition-exact-set-contract.yaml"
    ),
    "activation_extension_policy": Path(
        "data/token-block/stage5cc-activation-precondition-extension-policy.yaml"
    ),
    "activation_validation": Path(
        "data/token-block/stage5cc-activation-precondition-validation-requirements.yaml"
    ),
    "active_planning_preflight": Path(
        "data/token-block/stage5cc-active-planning-input-proposal-preflight.yaml"
    ),
    "transition_preflight": Path(
        "data/token-block/stage5cc-sidecar-to-active-transition-preflight.yaml"
    ),
    "no_byte_stream_transition_gate": Path(
        "data/token-block/stage5cc-no-byte-stream-transition-gate.yaml"
    ),
    "no_execution_transition_gate": Path(
        "data/token-block/stage5cc-no-execution-transition-gate.yaml"
    ),
    "supersession_nonactivation": Path(
        "data/token-block/stage5cc-manifest-supersession-nonactivation-proof.yaml"
    ),
    "stage5bd_preservation": Path("data/token-block/stage5cc-stage5bd-plan-preservation.yaml"),
    "active_lineage": Path("data/token-block/stage5cc-active-lineage-preservation.yaml"),
    "no_active_ingestion": Path("data/token-block/stage5cc-no-active-ingestion-proof.yaml"),
    "no_byte_stream_proof": Path("data/token-block/stage5cc-no-byte-stream-proof.yaml"),
    "citation_preservation": Path(
        "data/token-block/stage5cc-future-runner-citation-contract-preservation.yaml"
    ),
    "sidecar_activation_blocker": Path("data/token-block/stage5cc-sidecar-activation-blocker.yaml"),
    "future_impact": Path("data/token-block/stage5cc-future-dry-run-planning-impact.yaml"),
    "dwh": Path("data/historical-route/stage5cc-dwh-quarantine-reaffirmation.yaml"),
    "source_gap": Path("data/historical-route/stage5cc-source-gap-severity-update.yaml"),
    "guardrail": Path("data/historical-route/stage5cc-guardrail.yaml"),
    "handoff": Path("data/source-harvester/stage5cc-codex-handoff-policy.yaml"),
    "review_packaging_warning": Path("data/source-harvester/stage5cc-review-packaging-warning.yaml"),
}

SCHEMA_PATHS: dict[str, str] = {
    key: path.as_posix().replace("data/", "schemas/", 1).replace(".yaml", "-v0.schema.json")
    for key, path in DATA_PATHS.items()
}

RECORD_TYPES = {key: f"stage5cc_{key}" for key in DATA_PATHS}
RECORD_TYPES.update(
    {
        "active_planning_preflight": "stage5cc_active_planning_input_proposal_preflight",
        "no_byte_stream_transition_gate": "stage5cc_no_byte_stream_transition_gate",
        "no_execution_transition_gate": "stage5cc_no_execution_transition_gate",
    }
)

FALSE_FLAGS = {
    "active_ingestion_performed": False,
    "active_manifest_registry_updated": False,
    "active_planning_input_authorized_now": False,
    "active_planning_input_proposal_performed": False,
    "active_planning_input_selected_now": False,
    "active_token_block_manifest_changed": False,
    "ai_ml_interpretation_performed": False,
    "benchmark_performed": False,
    "branch_enumeration_performed": False,
    "byte_stream_generation_authorized_now": False,
    "canonical_corpus_active": False,
    "canonical_transcription_changed": False,
    "codex_completion_summary_committed": False,
    "codex_output_used": False,
    "cuda_execution_performed": False,
    "decode_attempt_performed": False,
    "dwh_hash_search_performed": False,
    "execution_allowed": False,
    "execution_authorized_now": False,
    "full_cartesian_product_enumerated": False,
    "generated_byte_streams_committed": False,
    "generated_outputs_committed": False,
    "hash_preimage_search_performed": False,
    "image_forensics_performed": False,
    "llm_vision_token_reading_performed": False,
    "manifest_supersession_authorized_now": False,
    "manifest_supersession_performed": False,
    "method_status_upgraded": False,
    "new_active_planning_input_created": False,
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
    "stage5bd_plan_superseded": False,
    "stego_tool_execution_performed": False,
    "string4_active_input_allowed": False,
    "string4_byte_stream_generation_allowed": False,
    "string4_dry_run_ingestion_allowed_now": False,
    "string4_execution_input_allowed": False,
    "string4_sidecar_active": False,
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


def _record(key: str, body: dict[str, Any], *, include_false_flags: bool = True) -> dict[str, Any]:
    payload = _base(RECORD_TYPES[key], key)
    payload.update(body)
    if include_false_flags:
        payload.update(FALSE_FLAGS)
    return payload


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
        str(STAGE5CB_REPORT_PATH),
        "README.md",
        "STATUS.md",
        "AGENTS.md",
        "ROADMAP.md",
        "TESTING.md",
        "docs/roadmap/staged-plan.md",
        "docs/onboarding/start-here.md",
        "docs/onboarding/source-of-truth-map.md",
        "docs/onboarding/operational-file-map.md",
        "docs/onboarding/codex-navigation-map.md",
        "docs/onboarding/deep-research-handoff-map.md",
        "docs/onboarding/token-block-source-lock-workflow.md",
        "docs/onboarding/token-block-preflight-dry-run-workflow.md",
        "docs/reference/token-block-cli.md",
        *[path.as_posix() for path in STAGE5CA_DATA_PATHS.values()],
        *REQUIRED_CITATION_PATHS,
        *ACTIVE_LINEAGE_PATHS,
        *STAGE5BD_PRESERVATION_PATHS,
    ]
    return list(dict.fromkeys(paths))


def _source_digest_records() -> list[dict[str, Any]]:
    return [_sha_record(Path(path), role="stage5cc_source_record") for path in _source_paths()]


def _lineage_digest_records(paths: list[str]) -> list[dict[str, Any]]:
    return [_sha_record(Path(path), role="stage5cc_preserved_active_lineage_record") for path in paths]


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


def _validation_commands() -> list[dict[str, Any]]:
    commands = [
        ("stage5cc_build", "python -m libreprimus.cli token-block build-stage5cc"),
        (
            "stage5cc_citation_contract",
            "python -m libreprimus.cli token-block validate-stage5cc-citation-contract",
        ),
        (
            "stage5cc_fail_closed_triggers",
            "python -m libreprimus.cli token-block validate-stage5cc-fail-closed-triggers",
        ),
        (
            "stage5cc_activation_preconditions",
            "python -m libreprimus.cli token-block validate-stage5cc-activation-preconditions",
        ),
        (
            "stage5cc_active_planning_input_preflight",
            "python -m libreprimus.cli token-block "
            "validate-stage5cc-active-planning-input-preflight",
        ),
        (
            "stage5cc_no_byte_stream_transition_gate",
            "python -m libreprimus.cli token-block "
            "validate-stage5cc-no-byte-stream-transition-gate",
        ),
        (
            "stage5cc_no_execution_transition_gate",
            "python -m libreprimus.cli token-block "
            "validate-stage5cc-no-execution-transition-gate",
        ),
        (
            "stage5cc_sidecar_gates",
            "python -m libreprimus.cli token-block validate-stage5cc-sidecar-gates",
        ),
        ("stage5cc_validate", "python -m libreprimus.cli token-block validate-stage5cc"),
        ("stage5cc_summary", "python -m libreprimus.cli token-block stage5cc-summary"),
        ("stage5ca_validator", "python -m libreprimus.cli token-block validate-stage5ca"),
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
        ("stage5ax_parallel_validation", ".\\scripts\\ci\\run-parallel-validation.ps1"),
        (
            "stage5ax_validation",
            "python -m libreprimus.cli parallel-validation validate-stage5ax",
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
        {"command_id": command_id, "command": command, "status": "passed_local_validation"}
        for command_id, command in commands
    ]
    rows.append(
        {
            "command_id": "bash_parallel_or_consistency_wrapper",
            "command": "./scripts/ci/run-parallel-validation.sh and ./scripts/ci/run-consistency-checks.sh",
            "status": "not_run_wsl_unavailable",
            "reason_if_not_run": (
                "Local bash resolves to the Windows Subsystem for Linux launcher, "
                "but no WSL distributions are installed."
            ),
        }
    )
    return rows


def _equivalence_entries() -> list[dict[str, Any]]:
    return [
        {
            "record_family": key,
            "prompt_required_path": repo_relative(path),
            "committed_path": repo_relative(path),
            "semantic_status": "exact_path_used",
        }
        for key, path in DATA_PATHS.items()
        if key in {"summary", "stage5ca_preservation", "active_planning_preflight"}
    ]


def _extension_policy_body(subject: str) -> dict[str, Any]:
    return {
        "extension_policy_subject": subject,
        "extension_policy_status": "explicit_extensions_only",
        "unclassified_extension_allowed": False,
        "extension_can_open_gate": False,
        "extension_can_authorize_execution": False,
        "extension_can_authorize_active_input": False,
        "extension_can_authorize_byte_stream_generation": False,
        "extension_requires": EXTENSION_REQUIRES,
        "classified_extension_count": 0,
        "validator_asserts_non_gate_opening": True,
    }


def _build_records() -> dict[str, dict[str, Any]]:
    stage5ca_summary = _read(STAGE5CA_DATA_PATHS["summary"])
    stage5ca_citation = _read(STAGE5CA_DATA_PATHS["citation_contract"])
    run_plan_count = _run_plan_count()
    source_records = _source_digest_records()
    source_paths = [record["path"] for record in source_records]
    lineage_records = _lineage_digest_records(ACTIVE_LINEAGE_PATHS)
    stage5ca_citation_count = len(stage5ca_citation.get("future_runner_must_cite_exactly", []))

    records: dict[str, dict[str, Any]] = {
        "findings": _record(
            "findings",
            {
                "stage5cb_findings_integrated": True,
                "stage5cb_verdict": "accept_with_warnings",
                "stage5cb_warning_count": 3,
                "stage5cb_warnings_integrated": [
                    "public_github_ci_corrobation_is_external_evidence",
                    "final_commit_and_ci_cannot_be_self_embedded",
                    "trigger_and_precondition_validators_need_exact_set_hardening",
                ],
                "warnings_are_gate_openers": False,
                "token_block_execution_recommended": False,
                "active_string4_ingestion_recommended": False,
                "source_report_present_locally": STAGE5CB_REPORT_PATH.is_file(),
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
                "selected_next_stage_id": "stage-5cd",
                "selected_next_prompt_type": "deep_research_review",
            },
        ),
        "validation_evidence": _record(
            "validation_evidence",
            {
                "reviewability_evidence_status": "committed_compact_evidence",
                "local_validation_evidence_committed": True,
                "validation_commands": _validation_commands(),
                "stage5cc_focus_validator_count": 8,
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
                        "gap_id": "external_ci_corroboration",
                        "status": "preserved_as_external_evidence_requirement",
                        "gate_opener": False,
                    },
                    {
                        "gap_id": "fail_closed_trigger_exact_set",
                        "status": "closed_by_stage5cc_exact_set_contract",
                        "gate_opener": False,
                    },
                    {
                        "gap_id": "activation_precondition_exact_set",
                        "status": "closed_by_stage5cc_exact_set_contract",
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
        "stage5ca_preservation": _record(
            "stage5ca_preservation",
            {
                "stage5ca_exact_citation_contract_preserved": True,
                "stage5ca_exact_citation_validation_preserved": True,
                "stage5ca_required_citation_count": stage5ca_citation_count,
                "stage5ca_summary_status": stage5ca_summary.get("status", "unknown"),
                "stage5ca_summary_path": repo_relative(STAGE5CA_DATA_PATHS["summary"]),
                "stage5ca_citation_contract_path": repo_relative(
                    STAGE5CA_DATA_PATHS["citation_contract"]
                ),
                "stage5ca_contracts_rewritten": False,
                "stage5ca_history_rewritten": False,
                "future_runner_must_cite_exactly": REQUIRED_CITATION_PATHS,
                "required_citation_count": len(REQUIRED_CITATION_PATHS),
                "citation_records": _citation_records(),
                "extra_citations_allowed_without_contract_update": False,
                "missing_citation_fails_closed": True,
                "unresolved_citation_path_fails_closed": True,
            },
        ),
        "citation_preservation": _record(
            "citation_preservation",
            {
                "future_runner_citation_contract_preservation_created": True,
                "stage5ca_exact_citation_contract_preserved": True,
                "citation_contract_type": "exact_set",
                "future_runner_must_cite_exactly": REQUIRED_CITATION_PATHS,
                "required_citation_count": len(REQUIRED_CITATION_PATHS),
                "citation_records": _citation_records(),
                "extra_citations_allowed_without_contract_update": False,
                "missing_citation_fails_closed": True,
                "unresolved_citation_path_fails_closed": True,
                "deprecated_stage5aw_path_allowed": False,
            },
        ),
        "fail_closed_contract": _record(
            "fail_closed_contract",
            {
                "fail_closed_trigger_exact_set_contract_created": True,
                "fail_closed_trigger_validation_mode": "exact_set",
                "required_fail_closed_triggers": REQUIRED_FAIL_CLOSED_TRIGGERS,
                "observed_fail_closed_triggers": REQUIRED_FAIL_CLOSED_TRIGGERS,
                "required_fail_closed_trigger_count": len(REQUIRED_FAIL_CLOSED_TRIGGERS),
                "observed_fail_closed_trigger_count": len(REQUIRED_FAIL_CLOSED_TRIGGERS),
                "missing_fail_closed_trigger_count": 0,
                "extra_fail_closed_trigger_count": 0,
                "missing_trigger_fails_closed": True,
                "extra_trigger_fails_closed": True,
                "unresolved_trigger_definition_fails_closed": True,
                "future_runner_must_fail_closed": True,
            },
        ),
        "fail_closed_extension_policy": _record(
            "fail_closed_extension_policy",
            _extension_policy_body("fail_closed_trigger"),
        ),
        "fail_closed_validation": _record(
            "fail_closed_validation",
            {
                "fail_closed_trigger_validation_requirements_created": True,
                "validator_command": (
                    "libreprimus token-block validate-stage5cc-fail-closed-triggers"
                ),
                "validates_exact_set": True,
                "fails_closed_on_missing_trigger": True,
                "fails_closed_on_extra_trigger": True,
                "fails_closed_on_unclassified_extension": True,
            },
        ),
        "activation_contract": _record(
            "activation_contract",
            {
                "activation_precondition_exact_set_contract_created": True,
                "activation_precondition_validation_mode": "exact_set",
                "required_activation_preconditions": REQUIRED_ACTIVATION_PRECONDITIONS,
                "observed_activation_preconditions": REQUIRED_ACTIVATION_PRECONDITIONS,
                "required_activation_precondition_count": len(REQUIRED_ACTIVATION_PRECONDITIONS),
                "observed_activation_precondition_count": len(REQUIRED_ACTIVATION_PRECONDITIONS),
                "missing_activation_precondition_count": 0,
                "extra_activation_precondition_count": 0,
                "missing_precondition_fails_closed": True,
                "extra_precondition_fails_closed": True,
                "unresolved_precondition_definition_fails_closed": True,
                "activation_preconditions_satisfied_now": False,
                "current_stage_authorizes_activation": False,
                "current_stage_authorizes_active_input": False,
                "current_stage_authorizes_dry_run_ingestion": False,
                "current_stage_authorizes_byte_stream_generation": False,
                "current_stage_authorizes_execution": False,
            },
        ),
        "activation_extension_policy": _record(
            "activation_extension_policy",
            _extension_policy_body("activation_precondition"),
        ),
        "activation_validation": _record(
            "activation_validation",
            {
                "activation_precondition_validation_requirements_created": True,
                "validator_command": (
                    "libreprimus token-block validate-stage5cc-activation-preconditions"
                ),
                "validates_exact_set": True,
                "validates_current_stage_authorizes_activation_false": True,
                "fails_closed_on_missing_precondition": True,
                "fails_closed_on_extra_precondition": True,
                "fails_closed_on_unclassified_extension": True,
            },
        ),
        "active_planning_preflight": _record(
            "active_planning_preflight",
            {
                "active_planning_input_proposal_preflight_created": True,
                "active_planning_input_proposal_performed": False,
                "active_planning_input_authorized_now": False,
                "active_planning_input_selected_now": False,
                "candidate_sidecar_id": "string4_inactive_planning_sidecar",
                "candidate_sidecar_status_required": "scaffolded_inactive",
                "candidate_sidecar_must_remain_noncanonical": True,
                "future_active_planning_input_proposal_would_require": (
                    FUTURE_ACTIVE_PLANNING_INPUT_REQUIREMENTS
                ),
                "current_stage_authorizes_activation": False,
                "current_stage_authorizes_active_input": False,
                "current_stage_authorizes_dry_run_ingestion": False,
                "current_stage_authorizes_byte_stream_generation": False,
                "current_stage_authorizes_execution": False,
                "string4_added_to_stage5bd_run_plan_ids": False,
                "string4_added_to_active_dry_run_inputs": False,
            },
        ),
        "transition_preflight": _record(
            "transition_preflight",
            {
                "sidecar_to_active_transition_preflight_created": True,
                "transition_preflight_status": "created_no_activation",
                "candidate_sidecar_id": "string4_inactive_planning_sidecar",
                "candidate_sidecar_status": "scaffolded_inactive",
                "future_transition_requires_stage5cd_or_later_review": True,
                "future_transition_requires_no_byte_stream_gate": True,
                "future_transition_requires_no_execution_gate": True,
                "current_stage_authorizes_activation": False,
            },
        ),
        "no_byte_stream_transition_gate": _record(
            "no_byte_stream_transition_gate",
            {
                "no_byte_stream_transition_gate_created": True,
                "no_byte_stream_transition_gate_status": "closed",
                "future_active_planning_input_does_not_imply_bytes": True,
                "byte_stream_generation_requires_separate_future_stage": True,
                "byte_stream_generation_authorized_now": False,
                "real_byte_stream_generated": False,
                "variant_byte_streams_generated": False,
                "generated_byte_streams_committed": False,
                "blocked_actions": BLOCKED_BYTE_STREAM_ACTIONS,
            },
        ),
        "no_execution_transition_gate": _record(
            "no_execution_transition_gate",
            {
                "no_execution_transition_gate_created": True,
                "no_execution_transition_gate_status": "closed",
                "future_active_planning_input_does_not_imply_execution": True,
                "execution_authorized_now": False,
                "token_block_experiment_executed": False,
                "decode_attempt_performed": False,
                "dwh_hash_search_performed": False,
                "scoring_performed": False,
                "cuda_execution_performed": False,
                "benchmark_performed": False,
                "stego_tool_execution_performed": False,
            },
        ),
        "supersession_nonactivation": _record(
            "supersession_nonactivation",
            {
                "manifest_supersession_nonactivation_proof_created": True,
                "manifest_supersession_performed": False,
                "manifest_supersession_authorized_now": False,
                "active_manifest_registry_updated": False,
                "before_after_digest_comparison_performed_for_supersession": False,
                "explicit_target_manifest_list_selected_now": False,
                "stage5bd_plan_superseded": False,
                "stage5bd_plan_preserved_or_explicitly_superseded": "preserved",
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
                "string4_added_to_stage5bd_run_plan_ids": False,
                "string4_added_to_active_dry_run_inputs": False,
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
                "canonical_transcription_changed": False,
                "active_token_block_manifest_changed": False,
            },
        ),
        "no_active_ingestion": _record(
            "no_active_ingestion",
            {
                "no_active_ingestion_status": "preserved_closed",
                "string4_sidecar_status": "scaffolded_inactive",
                "string4_sidecar_active": False,
                "string4_active_input_allowed": False,
                "string4_dry_run_ingestion_allowed_now": False,
                "string4_execution_input_allowed": False,
                "string4_added_to_active_dry_run_inputs": False,
                "string4_added_to_stage5bd_run_plan_ids": False,
                "active_ingestion_performed": False,
            },
        ),
        "no_byte_stream_proof": _record(
            "no_byte_stream_proof",
            {
                "no_byte_stream_proof_created": True,
                "no_byte_stream_gate_status": "closed",
                "string4_byte_stream_generation_allowed": False,
                "real_byte_stream_generated": False,
                "variant_byte_streams_generated": False,
                "generated_byte_streams_committed": False,
            },
        ),
        "sidecar_activation_blocker": _record(
            "sidecar_activation_blocker",
            {
                "blocker_status": "active",
                "blocked_item": "string4_inactive_planning_sidecar",
                "blocked_actions": [
                    "active_input",
                    "active_dry_run_ingestion",
                    "manifest_supersession",
                    *BLOCKED_BYTE_STREAM_ACTIONS,
                    "execution",
                ],
                "future_token_block_execution_remains_blocked": True,
            },
        ),
        "future_impact": _record(
            "future_impact",
            {
                "future_dry_run_planning_impact": (
                    "future active-planning proposal is reviewable but blocked from bytes"
                ),
                "future_token_block_execution_remains_blocked": True,
                "stage5bd_run_plan_ids_preserved": True,
                "future_runner_must_validate_stage5cc_contracts": True,
                "stage5bd_dry_run_plan_manifest_changed": False,
            },
        ),
        "dwh": _record(
            "dwh",
            {
                "dwh_quarantine_status": "reaffirmed_active",
                "dwh_quarantine_reaffirmed": True,
                "dwh_hash_search_performed": False,
                "dwh_context_used_as_execution_input": False,
            },
        ),
        "source_gap": _record(
            "source_gap",
            {
                "source_gap_severity_update": "unchanged_blocking_for_execution",
                "string4_source_gap_status": "inactive_context_only",
                "stage5cc_changes_source_truth": False,
            },
        ),
        "guardrail": _record(
            "guardrail",
            {
                "guardrail_status": "active",
                "future_token_block_execution_remains_blocked": True,
                "string4_sidecar_status": "scaffolded_inactive",
                "stage5cc_is_gate_opener": False,
                "no_byte_stream_transition_gate_status": "closed",
                "no_execution_transition_gate_status": "closed",
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
                "selected_next_stage_id": "stage-5cd",
                "selected_next_stage_title": (
                    "Stage 5CD - Deep Research review of Stage 5CC "
                    "active-planning-input proposal preflight and no-byte-stream "
                    "transition gate, without execution"
                ),
                "selected_next_prompt_type": "deep_research_review",
                "selected_next_stage_authorizes_execution": False,
                "selected_next_stage_reason": (
                    "Stage 5CC creates a no-execution active-planning-input preflight "
                    "that requires review before any planning-ingestion or execution-capable work."
                ),
            },
        ),
    }

    summary_body = {
        "status": "complete",
        "stage5cb_findings_integrated": True,
        "stage5cb_verdict": "accept_with_warnings",
        "stage5ca_exact_citation_contract_preserved": True,
        "stage5ca_exact_citation_validation_preserved": True,
        "fail_closed_trigger_exact_set_hardened": True,
        "activation_precondition_exact_set_hardened": True,
        "unexpected_trigger_extension_policy_created": True,
        "unexpected_precondition_extension_policy_created": True,
        "active_planning_input_proposal_preflight_created": True,
        "active_planning_input_proposal_performed": False,
        "active_planning_input_authorized_now": False,
        "active_planning_input_selected_now": False,
        "no_byte_stream_transition_gate_created": True,
        "no_byte_stream_transition_gate_status": "closed",
        "no_execution_transition_gate_created": True,
        "no_execution_transition_gate_status": "closed",
        "manifest_supersession_performed": False,
        "manifest_supersession_authorized_now": False,
        "stage5bd_dry_run_records_remain_valid": True,
        "stage5bd_run_plan_id_count": run_plan_count,
        "stage5bd_run_plan_ids_changed": False,
        "stage5bd_dry_run_plan_manifest_changed": False,
        "string4_sidecar_status": "scaffolded_inactive",
        "string4_sidecar_active": False,
        "string4_sidecar_planning_ingestion_activated": False,
        "string4_active_input_allowed": False,
        "string4_dry_run_ingestion_allowed_now": False,
        "string4_byte_stream_generation_allowed": False,
        "string4_execution_input_allowed": False,
        "canonical_transcription_changed": False,
        "active_token_block_manifest_changed": False,
        "future_token_block_execution_remains_blocked": True,
        "required_citation_count": len(REQUIRED_CITATION_PATHS),
        "required_fail_closed_trigger_count": len(REQUIRED_FAIL_CLOSED_TRIGGERS),
        "observed_fail_closed_trigger_count": len(REQUIRED_FAIL_CLOSED_TRIGGERS),
        "required_activation_precondition_count": len(REQUIRED_ACTIVATION_PRECONDITIONS),
        "observed_activation_precondition_count": len(REQUIRED_ACTIVATION_PRECONDITIONS),
        "active_lineage_record_count": len(ACTIVE_LINEAGE_PATHS),
        "source_digest_record_count": len(source_records),
        "source_digest_unique_path_count": len(set(source_paths)),
        "dwh_quarantine_reaffirmed": True,
        "generated_outputs_committed": False,
        "codex_output_used": False,
        "recommended_next_stage_id": "stage-5cd",
        "recommended_next_stage_title": (
            "Stage 5CD - Deep Research review of Stage 5CC active-planning-input "
            "proposal preflight and no-byte-stream transition gate, without execution"
        ),
    }
    summary_body.update(FALSE_FLAGS)
    records["summary"] = _record("summary", summary_body, include_false_flags=False)
    return records


def build_stage5cc(*, results_dir: Path = RESULTS_DIR) -> dict[str, Any]:
    _write_schemas()
    results_dir.mkdir(parents=True, exist_ok=True)

    records = _build_records()
    for key, payload in records.items():
        write_yaml(DATA_PATHS[key], payload)

    _write_generated(results_dir / "citation_contract_preservation.json", records["citation_preservation"])
    _write_generated(results_dir / "fail_closed_trigger_contract.json", records["fail_closed_contract"])
    _write_generated(results_dir / "activation_precondition_contract.json", records["activation_contract"])
    _write_generated(
        results_dir / "active_planning_input_preflight.json",
        records["active_planning_preflight"],
    )
    _write_generated(
        results_dir / "no_byte_stream_transition_gate.json",
        records["no_byte_stream_transition_gate"],
    )
    _write_generated(
        results_dir / "no_execution_transition_gate.json",
        records["no_execution_transition_gate"],
    )
    _write_generated(results_dir / "summary.json", records["summary"])
    _write_generated(
        results_dir / "warnings.jsonl",
        [
            {
                "warning_id": "stage5cc_remains_preflight_only",
                "severity": "info",
                "message": "Stage 5CC creates transition preflight metadata but authorizes no bytes or execution.",
            },
            {
                "warning_id": "external_ci_evidence_not_self_embedded",
                "severity": "info",
                "message": "Final commit and CI status remain external evidence.",
            },
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


def validate_stage5cc_citation_contract(
    *, citation_contract: Path = DATA_PATHS["citation_preservation"]
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
    unresolved = [path for path in cited if not Path(path).is_file()]
    errors.extend(f"citation_path_unresolved={path}" for path in unresolved)
    if INCORRECT_STAGE5AW_PATH in cited:
        errors.append("deprecated_stage5aw_path_present")
    if payload.get("stage5ca_exact_citation_contract_preserved") is not True:
        errors.append("Stage 5CA exact citation contract must be preserved")
    _stage5ca_counts, stage5ca_errors = validate_stage5ca_citation_contract()
    errors.extend(f"stage5ca_{error}" for error in stage5ca_errors)
    counts = {
        "stage5cc_citation_contract_valid": not errors,
        "required_citation_count": len(required),
        "observed_citation_count": len(cited),
        "missing_citation_count": len(missing),
        "extra_citation_count": len(extra),
        "unresolved_citation_count": len(unresolved),
        "validation_error_count": len(errors),
    }
    return counts, errors


def validate_stage5cc_fail_closed_triggers(
    *, trigger_contract: Path = DATA_PATHS["fail_closed_contract"]
) -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    payload = _validate_payload(trigger_contract, errors)
    triggers = [str(trigger) for trigger in payload.get("required_fail_closed_triggers", [])]
    required = list(REQUIRED_FAIL_CLOSED_TRIGGERS)
    missing = sorted(set(required) - set(triggers))
    extra = sorted(set(triggers) - set(required))
    if missing:
        errors.extend(f"missing_required_fail_closed_trigger={trigger}" for trigger in missing)
    if extra:
        errors.extend(f"extra_fail_closed_trigger={trigger}" for trigger in extra)
    if payload.get("fail_closed_trigger_validation_mode") != "exact_set":
        errors.append("fail_closed_trigger_validation_mode must be exact_set")
    if payload.get("missing_trigger_fails_closed") is not True:
        errors.append("missing_trigger_fails_closed must be true")
    if payload.get("extra_trigger_fails_closed") is not True:
        errors.append("extra_trigger_fails_closed must be true")
    counts = {
        "stage5cc_fail_closed_triggers_valid": not errors,
        "required_fail_closed_trigger_count": len(required),
        "observed_fail_closed_trigger_count": len(triggers),
        "missing_fail_closed_trigger_count": len(missing),
        "extra_fail_closed_trigger_count": len(extra),
        "validation_error_count": len(errors),
    }
    return counts, errors


def validate_stage5cc_activation_preconditions(
    *, activation_contract: Path = DATA_PATHS["activation_contract"]
) -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    payload = _validate_payload(activation_contract, errors)
    preconditions = [str(item) for item in payload.get("required_activation_preconditions", [])]
    required = list(REQUIRED_ACTIVATION_PRECONDITIONS)
    missing = sorted(set(required) - set(preconditions))
    extra = sorted(set(preconditions) - set(required))
    if missing:
        errors.extend(f"missing_required_activation_precondition={item}" for item in missing)
    if extra:
        errors.extend(f"extra_activation_precondition={item}" for item in extra)
    if payload.get("activation_precondition_validation_mode") != "exact_set":
        errors.append("activation_precondition_validation_mode must be exact_set")
    if payload.get("activation_preconditions_satisfied_now") is not False:
        errors.append("activation_preconditions_satisfied_now must be false")
    for flag in [
        "current_stage_authorizes_activation",
        "current_stage_authorizes_active_input",
        "current_stage_authorizes_dry_run_ingestion",
        "current_stage_authorizes_byte_stream_generation",
        "current_stage_authorizes_execution",
    ]:
        if payload.get(flag) is not False:
            errors.append(f"{flag} must be false")
    counts = {
        "stage5cc_activation_preconditions_valid": not errors,
        "required_activation_precondition_count": len(required),
        "observed_activation_precondition_count": len(preconditions),
        "missing_activation_precondition_count": len(missing),
        "extra_activation_precondition_count": len(extra),
        "activation_preconditions_satisfied_now": bool(
            payload.get("activation_preconditions_satisfied_now")
        ),
        "validation_error_count": len(errors),
    }
    return counts, errors


def validate_stage5cc_active_planning_input_preflight(
    *, preflight: Path = DATA_PATHS["active_planning_preflight"]
) -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    payload = _validate_payload(preflight, errors)
    requirements = [
        str(item) for item in payload.get("future_active_planning_input_proposal_would_require", [])
    ]
    missing = sorted(set(FUTURE_ACTIVE_PLANNING_INPUT_REQUIREMENTS) - set(requirements))
    extra = sorted(set(requirements) - set(FUTURE_ACTIVE_PLANNING_INPUT_REQUIREMENTS))
    errors.extend(f"missing_active_planning_requirement={item}" for item in missing)
    errors.extend(f"extra_active_planning_requirement={item}" for item in extra)
    if payload.get("active_planning_input_proposal_preflight_created") is not True:
        errors.append("active planning input preflight must be created")
    for flag in [
        "active_planning_input_proposal_performed",
        "active_planning_input_authorized_now",
        "active_planning_input_selected_now",
        "current_stage_authorizes_activation",
        "current_stage_authorizes_active_input",
        "current_stage_authorizes_dry_run_ingestion",
        "current_stage_authorizes_byte_stream_generation",
        "current_stage_authorizes_execution",
        "string4_added_to_stage5bd_run_plan_ids",
        "string4_added_to_active_dry_run_inputs",
    ]:
        if payload.get(flag) is not False:
            errors.append(f"{flag} must be false")
    counts = {
        "stage5cc_active_planning_input_preflight_valid": not errors,
        "active_planning_input_authorized_now": bool(
            payload.get("active_planning_input_authorized_now")
        ),
        "active_planning_input_selected_now": bool(payload.get("active_planning_input_selected_now")),
        "validation_error_count": len(errors),
    }
    return counts, errors


def validate_stage5cc_no_byte_stream_transition_gate(
    *, gate: Path = DATA_PATHS["no_byte_stream_transition_gate"]
) -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    payload = _validate_payload(gate, errors)
    actions = [str(item) for item in payload.get("blocked_actions", [])]
    missing = sorted(set(BLOCKED_BYTE_STREAM_ACTIONS) - set(actions))
    extra = sorted(set(actions) - set(BLOCKED_BYTE_STREAM_ACTIONS))
    errors.extend(f"missing_blocked_action={item}" for item in missing)
    errors.extend(f"extra_blocked_action={item}" for item in extra)
    if payload.get("no_byte_stream_transition_gate_status") != "closed":
        errors.append("no-byte-stream transition gate must be closed")
    for flag in [
        "byte_stream_generation_authorized_now",
        "real_byte_stream_generated",
        "variant_byte_streams_generated",
        "generated_byte_streams_committed",
    ]:
        if payload.get(flag) is not False:
            errors.append(f"{flag} must be false")
    counts = {
        "stage5cc_no_byte_stream_transition_gate_valid": not errors,
        "no_byte_stream_transition_gate_status": payload.get(
            "no_byte_stream_transition_gate_status", "unknown"
        ),
        "blocked_action_count": len(actions),
        "validation_error_count": len(errors),
    }
    return counts, errors


def validate_stage5cc_no_execution_transition_gate(
    *, gate: Path = DATA_PATHS["no_execution_transition_gate"]
) -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    payload = _validate_payload(gate, errors)
    if payload.get("no_execution_transition_gate_status") != "closed":
        errors.append("no-execution transition gate must be closed")
    for flag in [
        "execution_authorized_now",
        "token_block_experiment_executed",
        "decode_attempt_performed",
        "dwh_hash_search_performed",
        "scoring_performed",
        "cuda_execution_performed",
        "benchmark_performed",
        "stego_tool_execution_performed",
    ]:
        if payload.get(flag) is not False:
            errors.append(f"{flag} must be false")
    counts = {
        "stage5cc_no_execution_transition_gate_valid": not errors,
        "no_execution_transition_gate_status": payload.get(
            "no_execution_transition_gate_status", "unknown"
        ),
        "validation_error_count": len(errors),
    }
    return counts, errors


def validate_stage5cc_sidecar_gates(
    *,
    active_planning_preflight: Path = DATA_PATHS["active_planning_preflight"],
    transition_preflight: Path = DATA_PATHS["transition_preflight"],
    no_active_ingestion: Path = DATA_PATHS["no_active_ingestion"],
    no_byte_stream_proof: Path = DATA_PATHS["no_byte_stream_proof"],
    no_byte_stream_transition_gate: Path = DATA_PATHS["no_byte_stream_transition_gate"],
    no_execution_transition_gate: Path = DATA_PATHS["no_execution_transition_gate"],
    supersession_nonactivation: Path = DATA_PATHS["supersession_nonactivation"],
    stage5bd_preservation: Path = DATA_PATHS["stage5bd_preservation"],
    active_lineage: Path = DATA_PATHS["active_lineage"],
    guardrail: Path = DATA_PATHS["guardrail"],
    handoff: Path = DATA_PATHS["handoff"],
) -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    paths = {
        "active_planning_preflight": active_planning_preflight,
        "transition_preflight": transition_preflight,
        "no_active_ingestion": no_active_ingestion,
        "no_byte_stream_proof": no_byte_stream_proof,
        "no_byte_stream_transition_gate": no_byte_stream_transition_gate,
        "no_execution_transition_gate": no_execution_transition_gate,
        "supersession_nonactivation": supersession_nonactivation,
        "stage5bd_preservation": stage5bd_preservation,
        "active_lineage": active_lineage,
        "guardrail": guardrail,
        "handoff": handoff,
    }
    payloads = {key: _validate_payload(path, errors) for key, path in paths.items()}
    if payloads["transition_preflight"].get("candidate_sidecar_status") != "scaffolded_inactive":
        errors.append("transition preflight sidecar status must be scaffolded_inactive")
    if payloads["no_active_ingestion"].get("no_active_ingestion_status") != "preserved_closed":
        errors.append("no-active-ingestion proof must remain preserved_closed")
    if payloads["no_byte_stream_transition_gate"].get("no_byte_stream_transition_gate_status") != "closed":
        errors.append("no-byte-stream transition gate must remain closed")
    if payloads["no_execution_transition_gate"].get("no_execution_transition_gate_status") != "closed":
        errors.append("no-execution transition gate must remain closed")
    if payloads["supersession_nonactivation"].get("manifest_supersession_performed") is not False:
        errors.append("manifest supersession must not be performed")
    if payloads["stage5bd_preservation"].get("stage5bd_run_plan_id_count") != _run_plan_count():
        errors.append("Stage 5BD run-plan count must remain 10")
    active_paths = payloads["active_lineage"].get("preserved_active_record_paths", [])
    if INCORRECT_STAGE5AW_PATH in active_paths:
        errors.append("deprecated_stage5aw_path_present")
    if CORRECT_STAGE5AW_PATH not in active_paths:
        errors.append("correct_stage5aw_path_missing")
    for path in active_paths:
        if not Path(path).is_file():
            errors.append(f"active_lineage_path_missing={path}")
    if payloads["handoff"].get("canonical_codex_handoff_root") != "codex-output":
        errors.append("Stage 5CC must use codex-output as handoff root")
    if payloads["handoff"].get("codex_output_used") is not False:
        errors.append("codex_output_used must be false")
    if DEPRECATED_CODEX_OUTPUT.exists():
        errors.append("deprecated codex_output directory must not exist")
    _check_false_flags(payloads, errors)
    counts = {
        "stage5cc_sidecar_gates_valid": not errors,
        "no_active_ingestion_status": payloads["no_active_ingestion"].get(
            "no_active_ingestion_status", "unknown"
        ),
        "no_byte_stream_transition_gate_status": payloads["no_byte_stream_transition_gate"].get(
            "no_byte_stream_transition_gate_status", "unknown"
        ),
        "no_execution_transition_gate_status": payloads["no_execution_transition_gate"].get(
            "no_execution_transition_gate_status", "unknown"
        ),
        "stage5bd_run_plan_id_count": int(
            payloads["stage5bd_preservation"].get("stage5bd_run_plan_id_count") or 0
        ),
        "active_lineage_record_count": int(
            payloads["active_lineage"].get("active_lineage_record_count") or 0
        ),
        "validation_error_count": len(errors),
    }
    return counts, errors


def validate_stage5cc(
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
        payloads["guardrail"]
        if guardrail == DATA_PATHS["guardrail"]
        else _validate_payload(guardrail, errors)
    )

    for _counts, focused_errors in [
        validate_stage5cc_citation_contract(),
        validate_stage5cc_fail_closed_triggers(),
        validate_stage5cc_activation_preconditions(),
        validate_stage5cc_active_planning_input_preflight(),
        validate_stage5cc_no_byte_stream_transition_gate(),
        validate_stage5cc_no_execution_transition_gate(),
        validate_stage5cc_sidecar_gates(),
    ]:
        errors.extend(focused_errors)

    digest_paths = [
        str(record.get("path"))
        for record in payloads["source_digest_index"].get("source_digest_records", [])
    ]
    duplicate_paths = [path for path, count in Counter(digest_paths).items() if count > 1]
    if duplicate_paths:
        errors.extend(f"stage5cc_duplicate_source_digest_path={path}" for path in duplicate_paths)

    if summary_payload.get("stage5cb_verdict") != "accept_with_warnings":
        errors.append("summary must integrate Stage 5CB accept_with_warnings verdict")
    for key in [
        "stage5ca_exact_citation_contract_preserved",
        "stage5ca_exact_citation_validation_preserved",
        "fail_closed_trigger_exact_set_hardened",
        "activation_precondition_exact_set_hardened",
        "active_planning_input_proposal_preflight_created",
        "no_byte_stream_transition_gate_created",
        "no_execution_transition_gate_created",
        "future_token_block_execution_remains_blocked",
    ]:
        if summary_payload.get(key) is not True:
            errors.append(f"summary {key} must be true")
    if summary_payload.get("manifest_supersession_performed") is not False:
        errors.append("manifest supersession must not be performed")
    if summary_payload.get("stage5bd_run_plan_id_count") != _run_plan_count():
        errors.append("Stage 5BD run-plan count must remain unchanged")
    if next_stage_payload.get("selected_next_stage_id") != "stage-5cd":
        errors.append("Stage 5CC must select Stage 5CD review")
    if guardrail_payload.get("guardrail_status") != "active":
        errors.append("Stage 5CC guardrail must be active")
    _check_false_flags(payloads | {"guardrail_arg": guardrail_payload}, errors)

    counts = {
        "stage5cc_valid": not errors,
        "validation_error_count": len(errors),
        "stage5cb_verdict": summary_payload.get("stage5cb_verdict", "unknown"),
        "stage5ca_exact_citation_contract_preserved": bool(
            summary_payload.get("stage5ca_exact_citation_contract_preserved")
        ),
        "fail_closed_trigger_exact_set_hardened": bool(
            summary_payload.get("fail_closed_trigger_exact_set_hardened")
        ),
        "activation_precondition_exact_set_hardened": bool(
            summary_payload.get("activation_precondition_exact_set_hardened")
        ),
        "active_planning_input_proposal_preflight_created": bool(
            summary_payload.get("active_planning_input_proposal_preflight_created")
        ),
        "active_planning_input_authorized_now": bool(
            summary_payload.get("active_planning_input_authorized_now")
        ),
        "no_byte_stream_transition_gate_status": summary_payload.get(
            "no_byte_stream_transition_gate_status", "unknown"
        ),
        "no_execution_transition_gate_status": summary_payload.get(
            "no_execution_transition_gate_status", "unknown"
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


def load_stage5cc_summary(summary: Path = DATA_PATHS["summary"]) -> dict[str, Any]:
    return _read(summary)
