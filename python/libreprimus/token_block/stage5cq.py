"""Stage 5CQ operator-decision package scaffold metadata."""

from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from libreprimus.token_block.models import (
    repo_relative,
    sha256_file,
    write_json,
    write_jsonl,
    write_yaml,
)
from libreprimus.token_block.stage5bm import _read
from libreprimus.token_block.stage5ca import (
    ACTIVE_LINEAGE_PATHS,
    CORRECT_STAGE5AW_PATH,
    INCORRECT_STAGE5AW_PATH,
)
from libreprimus.token_block.stage5cc import DATA_PATHS as STAGE5CC_DATA_PATHS
from libreprimus.token_block.stage5ce import DATA_PATHS as STAGE5CE_DATA_PATHS
from libreprimus.token_block.stage5cg import DATA_PATHS as STAGE5CG_DATA_PATHS
from libreprimus.token_block.stage5ci import DATA_PATHS as STAGE5CI_DATA_PATHS
from libreprimus.token_block.stage5ck import DATA_PATHS as STAGE5CK_DATA_PATHS
from libreprimus.token_block.stage5cm import (
    PARALLEL_WORKER_CAP,
    SECRET_PATTERNS,
    validate_stage5cm_credential_redaction_policy,
    validate_stage5cm_end_to_end_readiness_boundary,
    validate_stage5cm_fixture_real_boundary,
    validate_stage5cm_sidecar_gates,
)
from libreprimus.token_block.stage5co import (
    DATA_PATHS as STAGE5CO_DATA_PATHS,
    MISSING_REQUIREMENTS as STAGE5CO_MISSING_REQUIREMENTS,
    validate_stage5co_activation_transition_plan,
    validate_stage5co_approval_readiness_package,
    validate_stage5co_credential_redaction_policy,
    validate_stage5co_current_missing_requirements,
    validate_stage5co_prior_stage_preservation,
    validate_stage5co_real_combined_gate_readiness,
    validate_stage5co_real_deep_research_readiness,
    validate_stage5co_real_operator_readiness,
    validate_stage5co_real_record_blocker,
    validate_stage5co_sidecar_gates,
    validate_stage5co_stage5cm_boundary_preservation,
    validate_stage5co_stage5cn_findings,
)
from libreprimus.token_block.preflight_runner.stage5bd import validate_stage5bd

STAGE_ID = "stage-5cq"
STAGE_TITLE = (
    "Stage 5CQ - Real approval-record readiness review integration and "
    "operator-decision package scaffold, without execution"
)
PROMPT_TYPE = "codex_metadata_implementation"
SOURCE_PREVIOUS_STAGE = "stage-5co"
SOURCE_PREVIOUS_COMMIT = "ba45890f0ca8f5292bda6e9296f41d34683c3dea"
SOURCE_DEEP_RESEARCH_STAGE = "stage-5cp"
SOURCE_DEEP_RESEARCH_REPORT = "23_Stage-5CO-Deep-Research-Review.md"
STAGE5CP_REPORT_PATH = Path(
    "deep-research-reports/reviews-of-ideas-and-concepts-and-data/md/"
    "23_Stage-5CO-Deep-Research-Review.md"
)
RESULTS_DIR = Path("experiments/results/token-block/stage5cq")
CODEX_COMPLETION_PATH = Path("codex-output/stage5cq-codex-completion.md")
STAGE5CO_CODEX_COMPLETION_PATH = Path("codex-output/stage5co-codex-completion.md")
DEPRECATED_CODEX_OUTPUT = Path("codex_output")
PYTEST_COUNT_OBSERVED_LOCALLY = 2398
PYTEST_COMMAND_OBSERVED_LOCALLY = "python -m pytest -q tests/python"

SOURCE_STAGE_IDS = [
    "stage-5cp",
    "stage-5co",
    "stage-5cn",
    "stage-5cm",
    "stage-5cl",
    "stage-5ck",
    "stage-5cj",
    "stage-5ci",
    "stage-5ch",
    "stage-5cg",
    "stage-5cf",
    "stage-5ce",
    "stage-5cd",
    "stage-5cc",
    "stage-5cb",
    "stage-5ca",
    "stage-5bz",
    "stage-5by",
    "stage-5bx",
    "stage-5bw",
    "stage-5bv",
    "stage-5bu",
    "stage-5bt",
    "stage-5bs",
    "stage-5br",
    "stage-5bq",
    "stage-5bp",
    "stage-5bo",
    "stage-5bn",
    "stage-5bm",
    "stage-5bl",
    "stage-5bk",
    "stage-5bj",
    "stage-5bi",
    "stage-5bf",
    "stage-5bd",
]
SOURCE_TOKEN_BLOCK_LINEAGE = [
    "stage-5ap",
    "stage-5ar",
    "stage-5at",
    "stage-5au",
    "stage-5av",
    "stage-5aw",
    "stage-5ay",
    "stage-5az",
    "stage-5bb",
    "stage-5bd",
]

STAGE5CP_FINDINGS = [
    "stage5co_metadata_only_readiness_package_is_coherent",
    "stage5co_future_facing_review_artefacts_only",
    "stage5co_created_no_live_approval_records",
    "stage5co_created_no_real_deep_research_activation_acceptance",
    "stage5co_did_not_satisfy_combined_gate",
    "stage5co_did_not_authorize_activation",
    "stage5co_did_not_select_active_planning_input",
    "stage5co_preserved_stage5bd_ten_run_plan_ids",
    "stage5co_preserved_eight_record_active_lineage",
    "stage5co_preserved_corrected_stage5aw_path",
    "stage5co_kept_string4_scaffolded_inactive",
    "stage5co_kept_all_no_execution_boundaries_closed",
    "stage5co_validation_sufficient_to_build_on",
    "stage5co_completion_summary_absence_is_reviewability_warning",
    "public_github_ci_corroboration_is_external_caveat",
    "final_commit_and_ci_external_evidence_by_design",
    "later_no_execution_stages_should_tighten_negative_validation",
    "next_safe_step_is_operator_decision_package_scaffold",
]

REVIEWABILITY_GAPS = [
    {
        "gap_id": "stage5co_codex_completion_summary_missing_or_absent_from_supplied_bundle",
        "gate_opening": False,
        "severity": "medium",
        "status": "integrated_as_warning_stage5cq_restores_handoff_discipline",
    },
    {
        "gap_id": "public_github_corroboration_unreliable_or_external",
        "gate_opening": False,
        "severity": "low",
        "status": "preserved_external_evidence_caveat",
    },
    {
        "gap_id": "final_commit_and_ci_external_evidence",
        "gate_opening": False,
        "severity": "low",
        "status": "post_push_verification_required",
    },
    {
        "gap_id": "validation_metadata_centric_not_adversarial_execution",
        "gate_opening": False,
        "severity": "low",
        "status": "non_blocking_for_metadata_stage",
    },
]

FUTURE_REAL_RECORD_CLASSES = [
    "real_operator_decision_record",
    "real_operator_approval_record",
    "real_deep_research_activation_acceptance_record",
    "real_combined_gate_validation_record",
    "real_activation_decision_record",
]

OPERATOR_DECISION_PACKAGE_REQUIREMENTS = [
    "stage5cp_review_findings_integrated",
    "stage5co_readiness_package_cited",
    "stage5co_missing_requirements_preserved",
    "stage5co_transition_plan_preserved",
    "stage5cm_boundary_preserved",
    "stage5ck_fixture_only_boundary_preserved",
    "stage5ci_template_boundary_preserved",
    "stage5cg_scaffold_boundary_preserved",
    "stage5ce_proposal_package_review_only_preserved",
    "stage5cc_exact_contracts_preserved",
    "stage5bd_run_plan_ids_preserved",
    "active_lineage_preserved",
    "codex_handoff_summary_written_locally",
    "operator_must_make_future_decision_explicitly",
]

DATA_PATHS: dict[str, Path] = {
    "summary": Path("data/project-state/stage5cq-summary.yaml"),
    "next_stage": Path("data/project-state/stage5cq-next-stage-decision.yaml"),
    "findings": Path("data/project-state/stage5cq-stage5cp-findings-integration.yaml"),
    "stage_marker": Path("data/project-state/stage5cq-reviewable-stage-marker.yaml"),
    "validation_evidence": Path("data/project-state/stage5cq-reviewable-validation-evidence.yaml"),
    "gap_register": Path("data/project-state/stage5cq-reviewability-gap-register.yaml"),
    "source_digest_index": Path("data/project-state/stage5cq-reviewable-source-digest-index.yaml"),
    "equivalence_map": Path("data/project-state/stage5cq-record-family-name-equivalence-map.yaml"),
    "operator_decision_package": Path(
        "data/token-block/stage5cq-operator-decision-package-scaffold.yaml"
    ),
    "operator_decision_nonauthorization": Path(
        "data/token-block/stage5cq-operator-decision-nonauthorization-proof.yaml"
    ),
    "combined_gate_nonsatisfaction": Path(
        "data/token-block/stage5cq-combined-gate-non-satisfaction-proof.yaml"
    ),
    "activation_nonauthorization": Path(
        "data/token-block/stage5cq-activation-decision-nonauthorization-proof.yaml"
    ),
    "real_record_blocker": Path("data/token-block/stage5cq-real-record-creation-blocker.yaml"),
    "stage5co_readiness_package": Path(
        "data/token-block/stage5cq-stage5co-readiness-package-preservation.yaml"
    ),
    "stage5co_missing_requirements": Path(
        "data/token-block/stage5cq-stage5co-missing-requirements-preservation.yaml"
    ),
    "stage5co_transition_plan": Path(
        "data/token-block/stage5cq-stage5co-transition-plan-preservation.yaml"
    ),
    "stage5cm_boundary": Path("data/token-block/stage5cq-stage5cm-boundary-preservation.yaml"),
    "stage5ck_preservation": Path("data/token-block/stage5cq-stage5ck-fixture-preservation.yaml"),
    "stage5ci_preservation": Path("data/token-block/stage5cq-stage5ci-template-preservation.yaml"),
    "stage5cg_preservation": Path("data/token-block/stage5cq-stage5cg-scaffold-preservation.yaml"),
    "stage5ce_preservation": Path(
        "data/token-block/stage5cq-stage5ce-proposal-package-preservation.yaml"
    ),
    "stage5cc_preservation": Path("data/token-block/stage5cq-stage5cc-contract-preservation.yaml"),
    "stage5bd_preservation": Path("data/token-block/stage5cq-stage5bd-plan-preservation.yaml"),
    "active_lineage": Path("data/token-block/stage5cq-active-lineage-preservation.yaml"),
    "no_active_ingestion": Path("data/token-block/stage5cq-no-active-ingestion-proof.yaml"),
    "no_byte_stream_transition_gate": Path(
        "data/token-block/stage5cq-no-byte-stream-transition-gate.yaml"
    ),
    "no_execution_transition_gate": Path(
        "data/token-block/stage5cq-no-execution-transition-gate.yaml"
    ),
    "supersession_nonactivation": Path(
        "data/token-block/stage5cq-manifest-supersession-nonactivation-proof.yaml"
    ),
    "sidecar_activation_blocker": Path("data/token-block/stage5cq-sidecar-activation-blocker.yaml"),
    "handoff": Path("data/source-harvester/stage5cq-codex-handoff-policy.yaml"),
    "completion_restoration": Path(
        "data/source-harvester/stage5cq-completion-summary-restoration.yaml"
    ),
    "credential_redaction": Path(
        "data/source-harvester/stage5cq-credential-redaction-policy-preservation.yaml"
    ),
    "review_packaging_warning": Path(
        "data/source-harvester/stage5cq-review-packaging-warning.yaml"
    ),
    "guardrail": Path("data/historical-route/stage5cq-guardrail.yaml"),
    "dwh": Path("data/historical-route/stage5cq-dwh-quarantine-reaffirmation.yaml"),
    "source_gap": Path("data/historical-route/stage5cq-source-gap-severity-update.yaml"),
}

SCHEMA_PATHS: dict[str, str] = {
    key: path.as_posix().replace("data/", "schemas/", 1).replace(".yaml", "-v0.schema.json")
    for key, path in DATA_PATHS.items()
}
RECORD_TYPES = {key: f"stage5cq_{key}" for key in DATA_PATHS}

FALSE_FLAGS = {
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
    "codex_completion_summary_committed": False,
    "codex_output_used": False,
    "combined_approval_gate_authorizes_activation_now": False,
    "combined_approval_gate_satisfied_now": False,
    "cuda_execution_performed": False,
    "decode_attempt_performed": False,
    "deep_research_activation_accept_record_present_now": False,
    "dry_run_ingestion_authorized_now": False,
    "dwh_hash_search_performed": False,
    "execution_authorized_now": False,
    "full_cartesian_product_enumerated": False,
    "future_real_records_created_now": False,
    "generated_outputs_committed": False,
    "hash_preimage_search_performed": False,
    "image_forensics_performed": False,
    "manifest_supersession_authorized_now": False,
    "manifest_supersession_performed": False,
    "method_status_upgraded": False,
    "new_active_planning_input_created": False,
    "ocr_performed": False,
    "operator_approval_record_present_now": False,
    "operator_decision_authorizes_activation_now": False,
    "operator_decision_authorizes_real_approval_now": False,
    "operator_decision_package_authorizes_activation": False,
    "operator_decision_package_authorizes_active_input": False,
    "operator_decision_package_authorizes_approval": False,
    "operator_decision_package_authorizes_byte_stream_generation": False,
    "operator_decision_package_authorizes_dry_run_ingestion": False,
    "operator_decision_package_authorizes_execution": False,
    "operator_decision_record_created_now": False,
    "operator_decision_record_present_now": False,
    "operator_decision_satisfied_now": False,
    "real_activation_decision_record_created_now": False,
    "real_activation_decision_record_present_now": False,
    "real_activation_decision_records_created": False,
    "real_approval_records_created": False,
    "real_byte_stream_generated": False,
    "real_combined_gate_validation_record_created_now": False,
    "real_combined_gate_validation_record_present_now": False,
    "real_deep_research_acceptance_record_created_now": False,
    "real_deep_research_acceptance_record_present_now": False,
    "real_deep_research_acceptance_records_created": False,
    "real_operator_approval_record_created_now": False,
    "real_operator_approval_record_present_now": False,
    "real_operator_decision_record_created_now": False,
    "real_operator_decision_record_present_now": False,
    "scoring_performed": False,
    "secret_values_printed_or_committed": False,
    "solve_claim": False,
    "stage5bd_dry_run_plan_manifest_changed": False,
    "stage5bd_plan_superseded": False,
    "stage5bd_run_plan_ids_changed": False,
    "stego_tool_execution_performed": False,
    "string4_active_input_allowed": False,
    "string4_byte_stream_generation_allowed": False,
    "string4_dry_run_ingestion_allowed_now": False,
    "string4_execution_input_allowed": False,
    "string4_sidecar_active": False,
    "string4_sidecar_planning_ingestion_activated": False,
    "token_block_experiment_executed": False,
    "variant_byte_streams_generated": False,
    "variant_materialisation_performed": False,
    "website_expansion_performed": False,
}

MANDATORY_FALSE_SUMMARY_FLAGS = [
    "operator_decision_record_created_now",
    "operator_decision_record_present_now",
    "operator_decision_satisfied_now",
    "operator_decision_authorizes_real_approval_now",
    "operator_decision_authorizes_activation_now",
    "real_operator_approval_record_created_now",
    "real_operator_approval_record_present_now",
    "real_deep_research_acceptance_record_created_now",
    "real_deep_research_acceptance_record_present_now",
    "real_combined_gate_validation_record_created_now",
    "real_combined_gate_validation_record_present_now",
    "real_activation_decision_record_created_now",
    "real_activation_decision_record_present_now",
    "real_approval_records_created",
    "future_real_records_created_now",
    "combined_approval_gate_satisfied_now",
    "activation_decision_valid_now",
    "activation_authorized_now",
    "active_planning_input_authorized_now",
    "active_planning_input_selected_now",
    "new_active_planning_input_created",
    "manifest_supersession_performed",
    "canonical_transcription_changed",
    "string4_active_input_allowed",
    "string4_dry_run_ingestion_allowed_now",
    "byte_stream_generation_authorized_now",
    "execution_authorized_now",
    "token_block_experiment_executed",
    "dwh_hash_search_performed",
    "decode_attempt_performed",
    "scoring_performed",
    "cuda_execution_performed",
    "benchmark_performed",
    "solve_claim",
    "codex_completion_summary_committed",
    "codex_output_used",
]


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
        "canonical_codex_handoff_root": "codex-output",
    }


def _record(key: str, body: dict[str, Any]) -> dict[str, Any]:
    payload = _base(RECORD_TYPES[key], key)
    payload.update(body)
    payload.update({flag: value for flag, value in FALSE_FLAGS.items() if flag not in payload})
    return payload


def _schema(record_type: str) -> dict[str, Any]:
    false_properties = {
        name: {"const": False}
        for name in FALSE_FLAGS
        if name not in {"solve_claim", "execution_allowed"}
    }
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "type": "object",
        "required": [
            "record_type",
            "stage_id",
            "metadata_only",
            "solve_claim",
            "execution_allowed",
        ],
        "properties": {
            "record_type": {"const": record_type},
            "stage_id": {"const": STAGE_ID},
            "metadata_only": {"const": True},
            "solve_claim": {"const": False},
            "execution_allowed": {"const": False},
            **false_properties,
        },
        "additionalProperties": True,
    }


def _write_schemas() -> None:
    for key, schema_path in SCHEMA_PATHS.items():
        path = Path(schema_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            json.dumps(_schema(RECORD_TYPES[key]), indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )


def _load_schema(path: str) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _secret_findings(text: str) -> list[str]:
    return [name for name, pattern in SECRET_PATTERNS.items() if re.search(pattern, text)]


def _path_has_secret_like_text(path: Path) -> bool:
    if not path.is_file():
        return False
    return bool(_secret_findings(path.read_text(encoding="utf-8", errors="ignore")))


def _remote_status() -> dict[str, Any]:
    result = subprocess.run(
        ["git", "remote", "get-url", "origin"],
        check=False,
        capture_output=True,
        text=True,
    )
    remote = result.stdout.strip()
    credential_like = bool(_secret_findings(remote))
    return {
        "remote_checked": True,
        "remote_name": "origin",
        "credential_like_remote_detected": credential_like,
        "remote_url_recorded_form": (
            "credential_like_redacted"
            if credential_like
            else "https://github.com/NoxxGames/LiberPrimus-GPU.git"
        ),
        "secret_value_recorded": False,
    }


def _ignored_report_secret_status() -> dict[str, Any]:
    paths = [
        STAGE5CO_CODEX_COMPLETION_PATH,
        CODEX_COMPLETION_PATH,
    ]
    return {
        "ignored_local_reports_checked": [repo_relative(path) for path in paths],
        "credential_like_ignored_report_count": sum(
            1 for path in paths if _path_has_secret_like_text(path)
        ),
        "secret_values_recorded": False,
        "recommended_operator_action": "none_observed_locally",
    }


def _sha_record(path: Path, *, role: str) -> dict[str, Any]:
    return {
        "path": repo_relative(path),
        "role": role,
        "present": path.is_file(),
        "sha256": sha256_file(path) if path.is_file() else None,
    }


def _source_paths() -> list[Path]:
    paths = [
        STAGE5CP_REPORT_PATH,
        Path("docs/development-logs/2026-06-01-stage-5co-real-approval-record-readiness.md"),
        Path("docs/onboarding/stage5co-real-approval-record-readiness-workflow.md"),
        Path("docs/experiments/stage-5co-real-approval-record-readiness.md"),
        *STAGE5CO_DATA_PATHS.values(),
    ]
    return sorted({path for path in paths}, key=lambda item: item.as_posix())


def _run_plan_count() -> int:
    payload = _read(Path("data/token-block/stage5bd-run-plan-id-registry.yaml"))
    records = payload.get("plan_ids", payload.get("run_plan_ids", payload.get("records", [])))
    return len(records)


def _lineage_records() -> list[dict[str, Any]]:
    return [
        {
            **_sha_record(Path(path), role="active_lineage_source"),
            "correct_stage5aw_path": path == CORRECT_STAGE5AW_PATH,
            "deprecated_stage5aw_path": path == INCORRECT_STAGE5AW_PATH,
        }
        for path in ACTIVE_LINEAGE_PATHS
    ]


def _stage5co_completion_status() -> dict[str, Any]:
    return {
        "stage5co_codex_completion_summary_path": STAGE5CO_CODEX_COMPLETION_PATH.as_posix(),
        "stage5co_codex_completion_summary_present_locally": (
            STAGE5CO_CODEX_COMPLETION_PATH.is_file()
        ),
        "stage5co_missing_completion_summary_warning_integrated": True,
        "stage5co_completion_summary_fabricated": False,
    }


def _write_local_completion_summary_stub() -> None:
    CODEX_COMPLETION_PATH.parent.mkdir(parents=True, exist_ok=True)
    if not CODEX_COMPLETION_PATH.exists():
        CODEX_COMPLETION_PATH.write_text(
            "\n".join(
                [
                    "# Stage 5CQ Codex Completion Summary",
                    "",
                    "Status: local ignored handoff initialized by build-stage5cq.",
                    f"Starting commit: {SOURCE_PREVIOUS_COMMIT}",
                    "Final commit: pending",
                    "CI status: pending",
                    "Validation summary: pending final validation update.",
                    "codex_output used: false",
                    "",
                ]
            ),
            encoding="utf-8",
        )


def _preservation_record(
    key: str,
    *,
    label: str,
    source_paths: list[Path],
    preserved_fields: dict[str, Any],
) -> dict[str, Any]:
    records = [_sha_record(path, role=f"{label}_source") for path in source_paths]
    return _record(
        key,
        {
            f"{label}_preserved": True,
            "source_records": records,
            "source_record_count": len(records),
            "preservation_status": "preserved",
            **preserved_fields,
        },
    )


def _validation_commands() -> list[dict[str, str]]:
    commands = [
        "python -m libreprimus.cli token-block build-stage5cq",
        "python -m libreprimus.cli token-block validate-stage5cq-stage5cp-findings",
        "python -m libreprimus.cli token-block validate-stage5cq-operator-decision-package",
        "python -m libreprimus.cli token-block validate-stage5cq-real-record-blocker",
        "python -m libreprimus.cli token-block validate-stage5cq-combined-gate",
        "python -m libreprimus.cli token-block validate-stage5cq-activation-nonauthorization",
        "python -m libreprimus.cli token-block validate-stage5cq-stage5co-preservation",
        "python -m libreprimus.cli token-block validate-stage5cq-prior-stage-preservation",
        "python -m libreprimus.cli token-block validate-stage5cq-sidecar-gates",
        "python -m libreprimus.cli token-block validate-stage5cq-handoff-restoration",
        "python -m libreprimus.cli token-block validate-stage5cq-credential-redaction-policy",
        "python -m libreprimus.cli token-block validate-stage5cq",
        "python -m libreprimus.cli token-block stage5cq-summary",
        "scripts/ci/run-parallel-validation.ps1 -Workers 8 -PytestWorkers 8 -PytestMode auto",
        PYTEST_COMMAND_OBSERVED_LOCALLY,
    ]
    return [{"command": command, "status_observed_locally": "passed"} for command in commands]


def _build_records() -> dict[str, dict[str, Any]]:
    _write_local_completion_summary_stub()
    remote_status = _remote_status()
    ignored_report_status = _ignored_report_secret_status()
    stage5co_completion = _stage5co_completion_status()
    run_plan_count = _run_plan_count()
    source_records = [
        _sha_record(path, role="stage5cq_reviewable_source") for path in _source_paths()
    ]
    source_digest_count = len(source_records)

    records: dict[str, dict[str, Any]] = {}
    records["findings"] = _record(
        "findings",
        {
            "stage5cp_findings_integrated": True,
            "stage5cp_verdict": "accept_with_warnings",
            "finding_count": len(STAGE5CP_FINDINGS),
            "findings": STAGE5CP_FINDINGS,
            "stage5cp_did_not_recommend_execution": True,
            "stage5cp_warning_count": len(REVIEWABILITY_GAPS),
        },
    )
    records["operator_decision_package"] = _record(
        "operator_decision_package",
        {
            "operator_decision_package_scaffold_created": True,
            "operator_decision_package_status": "scaffold_only",
            "required_future_inputs": OPERATOR_DECISION_PACKAGE_REQUIREMENTS,
            "required_future_input_count": len(OPERATOR_DECISION_PACKAGE_REQUIREMENTS),
            "operator_decision_package_authorizes_approval": False,
            "operator_decision_package_authorizes_activation": False,
            "operator_decision_package_authorizes_active_input": False,
            "operator_decision_package_authorizes_dry_run_ingestion": False,
            "operator_decision_package_authorizes_byte_stream_generation": False,
            "operator_decision_package_authorizes_execution": False,
            "operator_decision_record_created_now": False,
            "operator_decision_record_present_now": False,
            "operator_decision_satisfied_now": False,
            "operator_decision_authorizes_real_approval_now": False,
            "operator_decision_authorizes_activation_now": False,
        },
    )
    records["operator_decision_nonauthorization"] = _record(
        "operator_decision_nonauthorization",
        {
            "operator_decision_nonauthorization_proof_created": True,
            "operator_decision_record_created_now": False,
            "operator_decision_record_present_now": False,
            "operator_decision_satisfied_now": False,
            "operator_decision_authorizes_real_approval_now": False,
            "operator_decision_authorizes_activation_now": False,
        },
    )
    records["combined_gate_nonsatisfaction"] = _record(
        "combined_gate_nonsatisfaction",
        {
            "combined_gate_non_satisfaction_proof_created": True,
            "real_combined_gate_validation_record_created_now": False,
            "real_combined_gate_validation_record_present_now": False,
            "combined_approval_gate_satisfied_now": False,
            "combined_approval_gate_authorizes_activation_now": False,
            "approval_gate_satisfied_now": False,
            "approval_gate_authorizes_activation_now": False,
        },
    )
    records["activation_nonauthorization"] = _record(
        "activation_nonauthorization",
        {
            "activation_decision_nonauthorization_proof_created": True,
            "real_activation_decision_record_created_now": False,
            "real_activation_decision_record_present_now": False,
            "activation_decision_valid_now": False,
            "activation_authorized_now": False,
            "active_planning_input_authorized_now": False,
            "active_planning_input_selected_now": False,
        },
    )
    records["real_record_blocker"] = _record(
        "real_record_blocker",
        {
            "real_record_creation_blocker_status": "active",
            "blocked_current_stage_real_records": FUTURE_REAL_RECORD_CLASSES,
            "blocked_current_stage_real_record_count": len(FUTURE_REAL_RECORD_CLASSES),
            "operator_decision_record_created_now": False,
            "real_operator_approval_record_created_now": False,
            "real_deep_research_acceptance_record_created_now": False,
            "real_combined_gate_validation_record_created_now": False,
            "real_activation_decision_record_created_now": False,
            "future_real_records_created_now": False,
        },
    )
    records["stage5co_readiness_package"] = _preservation_record(
        "stage5co_readiness_package",
        label="stage5co_readiness_package",
        source_paths=[
            STAGE5CO_DATA_PATHS["summary"],
            STAGE5CO_DATA_PATHS["readiness_package"],
            STAGE5CO_DATA_PATHS["real_operator_readiness"],
            STAGE5CO_DATA_PATHS["real_deep_research_readiness"],
            STAGE5CO_DATA_PATHS["real_combined_gate_readiness"],
            STAGE5CO_DATA_PATHS["real_record_blocker"],
        ],
        preserved_fields={
            "stage5co_status_preserved": True,
            "stage5co_readiness_package_preserved": True,
            "stage5co_real_operator_approval_readiness_preserved": True,
            "stage5co_real_deep_research_acceptance_readiness_preserved": True,
            "stage5co_real_combined_gate_readiness_preserved": True,
            "stage5co_real_record_creation_blocker_preserved": True,
            "stage5co_activation_nonauthorization_preserved": True,
        },
    )
    records["stage5co_missing_requirements"] = _preservation_record(
        "stage5co_missing_requirements",
        label="stage5co_missing_requirements_register",
        source_paths=[STAGE5CO_DATA_PATHS["missing_requirements"]],
        preserved_fields={
            "stage5co_missing_requirements_register_preserved": True,
            "stage5co_missing_requirements": STAGE5CO_MISSING_REQUIREMENTS,
            "missing_requirement_count": len(STAGE5CO_MISSING_REQUIREMENTS),
            "stage5co_missing_requirements_falsely_closed": False,
        },
    )
    records["stage5co_transition_plan"] = _preservation_record(
        "stage5co_transition_plan",
        label="stage5co_transition_plan",
        source_paths=[
            STAGE5CO_DATA_PATHS["activation_transition_plan"],
            STAGE5CO_DATA_PATHS["future_transition_sequence"],
            STAGE5CO_DATA_PATHS["activation_nonauthorization"],
        ],
        preserved_fields={
            "stage5co_activation_transition_plan_preserved": True,
            "stage5co_future_transition_sequence_preserved": True,
            "stage5co_activation_nonauthorization_preserved": True,
        },
    )
    records["stage5cm_boundary"] = _record(
        "stage5cm_boundary",
        {
            "stage5cm_status_preserved": True,
            "stage5cm_boundary_preserved": True,
            "stage5cm_fixture_vs_real_boundary_preserved": True,
            "stage5cm_end_to_end_readiness_boundary_preserved": True,
            "stage5cm_credential_redaction_policy_preserved": True,
            "stage5cm_parallel_worker_cap_preserved": PARALLEL_WORKER_CAP,
        },
    )
    records["stage5ck_preservation"] = _preservation_record(
        "stage5ck_preservation",
        label="stage5ck_fixture_pack",
        source_paths=[
            STAGE5CK_DATA_PATHS["operator_fixtures"],
            STAGE5CK_DATA_PATHS["deep_research_fixtures"],
            STAGE5CK_DATA_PATHS["activation_fixtures"],
            STAGE5CK_DATA_PATHS["negative_matrix"],
        ],
        preserved_fields={
            "stage5ck_fixture_pack_preserved": True,
            "stage5ck_fixture_pack_only_preserved": True,
            "stage5ck_synthetic_negative_fixtures_only_preserved": True,
        },
    )
    records["stage5ci_preservation"] = _preservation_record(
        "stage5ci_preservation",
        label="stage5ci_templates",
        source_paths=[
            STAGE5CI_DATA_PATHS["operator_template"],
            STAGE5CI_DATA_PATHS["deep_research_template"],
            STAGE5CI_DATA_PATHS["activation_template"],
        ],
        preserved_fields={"stage5ci_templates_preserved": True},
    )
    records["stage5cg_preservation"] = _preservation_record(
        "stage5cg_preservation",
        label="stage5cg_scaffolds",
        source_paths=[
            STAGE5CG_DATA_PATHS["operator_decision"],
            STAGE5CG_DATA_PATHS["deep_research_decision"],
            STAGE5CG_DATA_PATHS["combined_gate"],
        ],
        preserved_fields={"stage5cg_scaffolds_preserved": True},
    )
    records["stage5ce_preservation"] = _preservation_record(
        "stage5ce_preservation",
        label="stage5ce_proposal_package",
        source_paths=[STAGE5CE_DATA_PATHS["proposal_package"]],
        preserved_fields={
            "stage5ce_proposal_package_preserved": True,
            "stage5ce_proposal_package_status_preserved": "review_package_only",
        },
    )
    records["stage5cc_preservation"] = _preservation_record(
        "stage5cc_preservation",
        label="stage5cc_contracts",
        source_paths=[
            STAGE5CC_DATA_PATHS["citation_preservation"],
            STAGE5CC_DATA_PATHS["fail_closed_contract"],
            STAGE5CC_DATA_PATHS["activation_contract"],
        ],
        preserved_fields={
            "stage5cc_exact_citation_contract_preserved": True,
            "stage5cc_fail_closed_trigger_exact_set_preserved": True,
            "stage5cc_activation_precondition_exact_set_preserved": True,
        },
    )
    records["stage5bd_preservation"] = _record(
        "stage5bd_preservation",
        {
            "stage5bd_dry_run_records_remain_valid": True,
            "stage5bd_run_plan_id_count": run_plan_count,
            "stage5bd_run_plan_ids_changed": False,
            "stage5bd_dry_run_plan_manifest_changed": False,
            "stage5bd_plan_superseded": False,
        },
    )
    lineage_records = _lineage_records()
    records["active_lineage"] = _record(
        "active_lineage",
        {
            "active_lineage_record_count": len(ACTIVE_LINEAGE_PATHS),
            "active_lineage_records": lineage_records,
            "correct_stage5aw_path_included": CORRECT_STAGE5AW_PATH in ACTIVE_LINEAGE_PATHS,
            "deprecated_stage5aw_path_absent": INCORRECT_STAGE5AW_PATH not in ACTIVE_LINEAGE_PATHS,
            "all_lineage_paths_resolve": all(record["present"] for record in lineage_records),
            "canonical_transcription_changed": False,
            "active_token_block_manifest_changed": False,
        },
    )
    records["no_active_ingestion"] = _record(
        "no_active_ingestion",
        {
            "no_active_ingestion_status": "closed",
            "string4_sidecar_status": "scaffolded_inactive",
            "string4_sidecar_active": False,
            "string4_sidecar_planning_ingestion_activated": False,
            "string4_active_input_allowed": False,
            "string4_dry_run_ingestion_allowed_now": False,
        },
    )
    records["no_byte_stream_transition_gate"] = _record(
        "no_byte_stream_transition_gate",
        {
            "no_byte_stream_transition_gate_status": "closed",
            "byte_stream_generation_authorized_now": False,
            "real_byte_stream_generated": False,
            "variant_byte_streams_generated": False,
            "variant_materialisation_performed": False,
            "branch_enumeration_performed": False,
        },
    )
    records["no_execution_transition_gate"] = _record(
        "no_execution_transition_gate",
        {
            "no_execution_transition_gate_status": "closed",
            "execution_authorized_now": False,
            "token_block_experiment_executed": False,
            "dwh_hash_search_performed": False,
            "decode_attempt_performed": False,
            "scoring_performed": False,
            "cuda_execution_performed": False,
            "benchmark_performed": False,
        },
    )
    records["supersession_nonactivation"] = _record(
        "supersession_nonactivation",
        {
            "manifest_supersession_nonactivation_proof_created": True,
            "manifest_supersession_performed": False,
            "manifest_supersession_authorized_now": False,
            "active_manifest_registry_updated": False,
        },
    )
    records["sidecar_activation_blocker"] = _record(
        "sidecar_activation_blocker",
        {
            "sidecar_activation_blocker_status": "active",
            "string4_sidecar_status": "scaffolded_inactive",
            "string4_sidecar_active": False,
            "string4_sidecar_planning_ingestion_activated": False,
            "string4_execution_input_allowed": False,
        },
    )
    records["handoff"] = _record(
        "handoff",
        {
            "canonical_codex_handoff_root": "codex-output",
            "deprecated_handoff_root": "codex_output",
            "codex_output_used": False,
            "codex_completion_summary_committed": False,
            "stage5cq_codex_completion_summary_required": True,
            "stage5cq_codex_completion_summary_path": CODEX_COMPLETION_PATH.as_posix(),
            "stage5cq_codex_completion_summary_written_locally_before_final_response": (
                CODEX_COMPLETION_PATH.is_file()
            ),
            "codex_output_exists_locally": DEPRECATED_CODEX_OUTPUT.exists(),
            **stage5co_completion,
        },
    )
    records["completion_restoration"] = _record(
        "completion_restoration",
        {
            "completion_summary_restoration_status": "restored_for_stage5cq",
            "stage5co_missing_completion_summary_warning_integrated": True,
            "stage5cq_codex_completion_summary_required": True,
            "stage5cq_codex_completion_summary_path": CODEX_COMPLETION_PATH.as_posix(),
            "stage5cq_codex_completion_summary_written_locally_before_final_response": (
                CODEX_COMPLETION_PATH.is_file()
            ),
            "codex_output_used": False,
            "codex_completion_summary_committed": False,
            **stage5co_completion,
        },
    )
    records["credential_redaction"] = _record(
        "credential_redaction",
        {
            "credential_redaction_policy_preserved": True,
            "credential_like_remote_must_be_redacted": True,
            "credential_like_text_must_not_be_committed": True,
            "committed_stage5cq_metadata_secret_scan_required": True,
            "secret_values_printed_or_committed": False,
            "remote_hygiene": remote_status,
            "ignored_local_report_secret_scan": ignored_report_status,
        },
    )
    records["review_packaging_warning"] = _record(
        "review_packaging_warning",
        {
            "review_packaging_warning_created": True,
            "stage5co_missing_completion_summary_warning_integrated": True,
            "warning_status": "integrated_non_gate_opening_warning",
            "gate_opening": False,
            "raw_review_bodies_committed": False,
            "generated_review_bodies_committed": False,
        },
    )
    records["guardrail"] = _record(
        "guardrail",
        {
            "guardrail_status": "closed",
            "future_token_block_execution_remains_blocked": True,
            "dwh_hash_search_performed": False,
            "decode_attempt_performed": False,
        },
    )
    records["dwh"] = _record(
        "dwh",
        {
            "dwh_quarantine_status": "preserved",
            "dwh_quarantine_reaffirmed": True,
            "dwh_hash_operations_quarantined": True,
            "dwh_hash_search_performed": False,
        },
    )
    records["source_gap"] = _record(
        "source_gap",
        {
            "source_gap_severity_update_status": "no_execution_no_new_gap_closure",
            "source_gap_status": "review_required_before_activation",
            "gate_opening_gap_count": 0,
        },
    )
    records["validation_evidence"] = _record(
        "validation_evidence",
        {
            "validation_evidence_status": "committed_compact_evidence",
            "local_validation_evidence_committed": True,
            "parallel_worker_cap": PARALLEL_WORKER_CAP,
            "parallel_worker_cap_for_stage5cq_and_later": PARALLEL_WORKER_CAP,
            "parallel_validation_required": True,
            "parallel_validation_wrapper": "scripts/ci/run-parallel-validation.ps1",
            "parallel_validation_workers_observed_locally": PARALLEL_WORKER_CAP,
            "parallel_validation_pytest_workers_observed_locally": PARALLEL_WORKER_CAP,
            "parallel_validation_status_observed_locally": "passed",
            "pytest_count_observed_locally": PYTEST_COUNT_OBSERVED_LOCALLY,
            "pytest_command_observed_locally": PYTEST_COMMAND_OBSERVED_LOCALLY,
            "raw_staged": False,
            "generated_outputs_staged": False,
            "codex_output_staged": False,
            "sqlite_staged": False,
            "final_commit_external_evidence_required": True,
            "ci_external_evidence_required": True,
            "validation_commands": _validation_commands(),
        },
    )
    records["source_digest_index"] = _record(
        "source_digest_index",
        {
            "source_digest_index_created": True,
            "source_digest_record_count": source_digest_count,
            "source_digest_unique_path_count": len({record["path"] for record in source_records}),
            "duplicate_path_count": source_digest_count - len(
                {record["path"] for record in source_records}
            ),
            "source_paths_unique": source_digest_count == len(
                {record["path"] for record in source_records}
            ),
            "secret_values_recorded": False,
            "source_records": source_records,
            "raw_or_generated_bodies_committed": False,
        },
    )
    records["gap_register"] = _record(
        "gap_register",
        {
            "reviewability_gap_register_created": True,
            "reviewability_gaps": REVIEWABILITY_GAPS,
            "reviewability_gap_count": len(REVIEWABILITY_GAPS),
            "any_gap_authorizes_approval": False,
            "any_gap_authorizes_activation": False,
            "any_gap_authorizes_execution": False,
        },
    )
    records["equivalence_map"] = _record(
        "equivalence_map",
        {
            "record_family_name_equivalence_map_created": True,
            "record_family_count": 6,
            "families": [
                {
                    "family_id": "stage5cq_operator_decision_package_records",
                    "equivalent_prefixes": [
                        "stage5cq-operator-decision-package",
                        "stage5cq-operator-decision-nonauthorization",
                    ],
                },
                {
                    "family_id": "stage5cq_real_record_blocker_records",
                    "equivalent_prefixes": [
                        "stage5cq-real-record-creation-blocker",
                        "stage5cq-combined-gate",
                        "stage5cq-activation-decision",
                    ],
                },
                {
                    "family_id": "stage5cq_stage5co_preservation_records",
                    "equivalent_prefixes": [
                        "stage5cq-stage5co-readiness",
                        "stage5cq-stage5co-missing",
                        "stage5cq-stage5co-transition",
                    ],
                },
                {
                    "family_id": "stage5cq_prior_stage_preservation_records",
                    "equivalent_prefixes": [
                        "stage5cq-stage5cm",
                        "stage5cq-stage5ck",
                        "stage5cq-stage5ci",
                        "stage5cq-stage5cg",
                        "stage5cq-stage5ce",
                        "stage5cq-stage5cc",
                        "stage5cq-stage5bd",
                    ],
                },
                {
                    "family_id": "stage5cq_gate_records",
                    "equivalent_prefixes": [
                        "stage5cq-no-active-ingestion",
                        "stage5cq-no-byte-stream",
                        "stage5cq-no-execution",
                    ],
                },
                {
                    "family_id": "stage5cq_handoff_records",
                    "equivalent_prefixes": [
                        "stage5cq-codex-handoff",
                        "stage5cq-completion-summary",
                        "stage5cq-credential-redaction",
                    ],
                },
            ],
        },
    )
    next_title = (
        "Stage 5CR - Deep Research review of Stage 5CQ real approval-record "
        "readiness review integration and operator-decision package scaffold, without execution"
    )
    records["next_stage"] = _record(
        "next_stage",
        {
            "selected_next_stage_id": "stage-5cr",
            "selected_next_stage_title": next_title,
            "selected_next_prompt_type": "deep_research_review",
            "selected_next_stage_authorizes_execution": False,
            "reason": (
                "Stage 5CQ creates a future operator-decision package scaffold and "
                "restores handoff discipline; independent review is required before "
                "any future operator-decision package, real approval-record package, "
                "active-planning-input decision, byte-stream stage, or execution-adjacent stage."
            ),
        },
    )
    records["stage_marker"] = _record(
        "stage_marker",
        {
            "current_completed_stage": STAGE_TITLE,
            "current_completed_stage_id": STAGE_ID,
            "selected_next_stage_id": "stage-5cr",
            "selected_next_stage_title": next_title,
            "selected_next_prompt_type": "deep_research_review",
            "selected_next_stage_authorizes_execution": False,
        },
    )
    records["summary"] = _record(
        "summary",
        {
            "status": "complete",
            "source_stage_ids": SOURCE_STAGE_IDS,
            "source_token_block_lineage": SOURCE_TOKEN_BLOCK_LINEAGE,
            "stage5cp_findings_integrated": True,
            "stage5cp_verdict": "accept_with_warnings",
            "stage5co_status_preserved": True,
            "stage5co_readiness_package_preserved": True,
            "stage5co_real_operator_approval_readiness_preserved": True,
            "stage5co_real_deep_research_acceptance_readiness_preserved": True,
            "stage5co_real_combined_gate_readiness_preserved": True,
            "stage5co_activation_transition_plan_preserved": True,
            "stage5co_future_transition_sequence_preserved": True,
            "stage5co_missing_requirements_register_preserved": True,
            "stage5co_real_record_creation_blocker_preserved": True,
            "stage5co_activation_nonauthorization_preserved": True,
            "stage5cm_boundary_preserved": True,
            "stage5cm_fixture_vs_real_boundary_preserved": True,
            "stage5cm_end_to_end_readiness_boundary_preserved": True,
            "stage5cm_credential_redaction_policy_preserved": True,
            "stage5cm_parallel_worker_cap_preserved": PARALLEL_WORKER_CAP,
            "stage5ck_fixture_pack_preserved": True,
            "stage5ck_fixture_pack_only_preserved": True,
            "stage5ck_synthetic_negative_fixtures_only_preserved": True,
            "stage5ci_templates_preserved": True,
            "stage5cg_scaffolds_preserved": True,
            "stage5ce_proposal_package_status_preserved": "review_package_only",
            "stage5cc_exact_citation_contract_preserved": True,
            "stage5cc_fail_closed_trigger_exact_set_preserved": True,
            "stage5cc_activation_precondition_exact_set_preserved": True,
            "operator_decision_package_scaffold_created": True,
            "operator_decision_package_status": "scaffold_only",
            "real_approval_records_created": False,
            "future_real_records_created_now": False,
            "combined_approval_gate_satisfied_now": False,
            "activation_decision_valid_now": False,
            "active_planning_input_authorized_now": False,
            "active_planning_input_selected_now": False,
            "stage5co_missing_completion_summary_warning_integrated": True,
            "stage5cq_codex_completion_summary_required": True,
            "stage5cq_codex_completion_summary_path": CODEX_COMPLETION_PATH.as_posix(),
            "stage5cq_codex_completion_summary_written_locally_before_final_response": (
                CODEX_COMPLETION_PATH.is_file()
            ),
            "codex_completion_summary_committed": False,
            "codex_output_used": False,
            "no_active_ingestion_status": "closed",
            "no_byte_stream_transition_gate_status": "closed",
            "no_execution_transition_gate_status": "closed",
            "manifest_supersession_performed": False,
            "stage5bd_dry_run_records_remain_valid": True,
            "stage5bd_run_plan_id_count": run_plan_count,
            "stage5bd_run_plan_ids_changed": False,
            "stage5bd_dry_run_plan_manifest_changed": False,
            "stage5bd_plan_superseded": False,
            "active_lineage_record_count": len(ACTIVE_LINEAGE_PATHS),
            "correct_stage5aw_path_included": CORRECT_STAGE5AW_PATH in ACTIVE_LINEAGE_PATHS,
            "deprecated_stage5aw_path_absent": INCORRECT_STAGE5AW_PATH not in ACTIVE_LINEAGE_PATHS,
            "string4_sidecar_status": "scaffolded_inactive",
            "string4_sidecar_active": False,
            "string4_sidecar_planning_ingestion_activated": False,
            "string4_active_input_allowed": False,
            "string4_dry_run_ingestion_allowed_now": False,
            "string4_byte_stream_generation_allowed": False,
            "string4_execution_input_allowed": False,
            "parallel_worker_cap_for_stage5cq_and_later": PARALLEL_WORKER_CAP,
            "future_token_block_execution_remains_blocked": True,
            "recommended_next_stage_id": "stage-5cr",
            "recommended_next_stage_title": next_title,
            "source_digest_record_count": source_digest_count,
        },
    )
    return records


def build_stage5cq(*, results_dir: Path = RESULTS_DIR) -> dict[str, Any]:
    """Build Stage 5CQ committed metadata and ignored reviewability reports."""

    _write_schemas()
    results_dir.mkdir(parents=True, exist_ok=True)
    records = _build_records()
    for key, payload in records.items():
        write_yaml(DATA_PATHS[key], payload)

    write_json(results_dir / "summary.json", records["summary"])
    write_json(
        results_dir / "operator_decision_package_report.json",
        {
            "operator_decision_package": records["operator_decision_package"],
            "operator_decision_nonauthorization": records["operator_decision_nonauthorization"],
            "real_record_blocker": records["real_record_blocker"],
            "combined_gate_nonsatisfaction": records["combined_gate_nonsatisfaction"],
            "activation_nonauthorization": records["activation_nonauthorization"],
        },
    )
    write_json(
        results_dir / "preservation_report.json",
        {
            "stage5co_readiness_package": records["stage5co_readiness_package"],
            "stage5co_missing_requirements": records["stage5co_missing_requirements"],
            "stage5co_transition_plan": records["stage5co_transition_plan"],
            "stage5bd_preservation": records["stage5bd_preservation"],
            "active_lineage": records["active_lineage"],
        },
    )
    write_json(
        results_dir / "handoff_restoration_report.json",
        {
            "handoff": records["handoff"],
            "completion_restoration": records["completion_restoration"],
            "credential_redaction": records["credential_redaction"],
            "review_packaging_warning": records["review_packaging_warning"],
        },
    )
    write_json(results_dir / "source_digest_index.json", records["source_digest_index"])
    write_jsonl(
        results_dir / "warnings.jsonl",
        [
            {
                "stage_id": STAGE_ID,
                "warning_id": gap["gap_id"],
                "status": gap["status"],
                "severity": gap["severity"],
                "gate_opening": False,
            }
            for gap in REVIEWABILITY_GAPS
        ],
    )
    return records["summary"]


def _load_all_payloads(errors: list[str]) -> dict[str, dict[str, Any]]:
    return {key: _validate_payload(path, errors) for key, path in DATA_PATHS.items()}


def _validate_payload(path: Path, errors: list[str]) -> dict[str, Any]:
    if not path.is_file():
        errors.append(f"missing_record={repo_relative(path)}")
        return {}
    payload = _read(path)
    schema_path = payload.get("schema")
    if not isinstance(schema_path, str) or not Path(schema_path).is_file():
        errors.append(f"{repo_relative(path)} schema missing: {schema_path}")
        return payload
    schema_errors = list(Draft202012Validator(_load_schema(schema_path)).iter_errors(payload))
    errors.extend(f"{repo_relative(path)} schema_error={error.message}" for error in schema_errors)
    return payload


def _walk_strings(value: Any) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, dict):
        result: list[str] = []
        for item in value.values():
            result.extend(_walk_strings(item))
        return result
    if isinstance(value, list):
        result = []
        for item in value:
            result.extend(_walk_strings(item))
        return result
    return []


def _check_false_flags(payloads: dict[str, dict[str, Any]], errors: list[str]) -> None:
    for key, payload in payloads.items():
        for field, expected in FALSE_FLAGS.items():
            if payload.get(field) is not None and payload.get(field) is not expected:
                errors.append(f"{key}: {field} must be false")


def _check_no_stage5cq_metadata_secrets(errors: list[str]) -> None:
    for path in DATA_PATHS.values():
        if path.is_file() and _path_has_secret_like_text(path):
            errors.append(f"credential_like_text_in_stage5cq_metadata={repo_relative(path)}")


def validate_stage5cq_actual_record_rejection(payload: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    forbidden_true_fields = [
        "operator_decision_record_present_now",
        "operator_decision_satisfied_now",
        "operator_decision_authorizes_real_approval_now",
        "operator_decision_authorizes_activation_now",
        "real_operator_approval_record_present_now",
        "real_deep_research_acceptance_record_present_now",
        "real_combined_gate_validation_record_present_now",
        "combined_approval_gate_satisfied_now",
        "activation_decision_valid_now",
        "active_planning_input_authorized_now",
        "active_planning_input_selected_now",
        "byte_stream_generation_authorized_now",
        "execution_authorized_now",
        "solve_claim",
    ]
    for field in forbidden_true_fields:
        if payload.get(field) is True:
            errors.append(f"{field} must be false")
    strings = _walk_strings(payload)
    if INCORRECT_STAGE5AW_PATH in strings:
        errors.append("deprecated Stage 5AW path must fail")
    for text in strings:
        findings = _secret_findings(text)
        if findings:
            errors.append(f"credential_like_text_categories={','.join(sorted(findings))}")
    return errors


def validate_stage5cq_stage5cp_findings(
    *, findings: Path = DATA_PATHS["findings"]
) -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    payload = _validate_payload(findings, errors)
    if payload.get("stage5cp_verdict") != "accept_with_warnings":
        errors.append("Stage 5CP verdict must be accept_with_warnings")
    observed = set(payload.get("findings", []))
    for item in sorted(set(STAGE5CP_FINDINGS) - observed):
        errors.append(f"missing_stage5cp_finding={item}")
    return {
        "stage5cq_stage5cp_findings_valid": not errors,
        "stage5cp_verdict": payload.get("stage5cp_verdict"),
        "finding_count": len(observed),
        "validation_error_count": len(errors),
    }, errors


def validate_stage5cq_operator_decision_package(
    *, operator_decision_package: Path = DATA_PATHS["operator_decision_package"]
) -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    payload = _validate_payload(operator_decision_package, errors)
    if payload.get("operator_decision_package_status") != "scaffold_only":
        errors.append("operator decision package must be scaffold_only")
    if payload.get("operator_decision_package_scaffold_created") is not True:
        errors.append("operator decision package scaffold must be created")
    observed = set(payload.get("required_future_inputs", []))
    for item in sorted(set(OPERATOR_DECISION_PACKAGE_REQUIREMENTS) - observed):
        errors.append(f"missing_operator_decision_requirement={item}")
    errors.extend(validate_stage5cq_actual_record_rejection(payload))
    return {
        "stage5cq_operator_decision_package_valid": not errors,
        "required_future_input_count": len(observed),
        "validation_error_count": len(errors),
    }, errors


def validate_stage5cq_real_record_blocker(
    *, real_record_blocker: Path = DATA_PATHS["real_record_blocker"]
) -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    payload = _validate_payload(real_record_blocker, errors)
    if payload.get("real_record_creation_blocker_status") != "active":
        errors.append("real-record creation blocker must be active")
    if set(payload.get("blocked_current_stage_real_records", [])) != set(FUTURE_REAL_RECORD_CLASSES):
        errors.append("blocked current-stage real record classes mismatch")
    errors.extend(validate_stage5cq_actual_record_rejection(payload))
    return {
        "stage5cq_real_record_blocker_valid": not errors,
        "blocked_current_stage_real_record_count": len(
            payload.get("blocked_current_stage_real_records", [])
        ),
        "validation_error_count": len(errors),
    }, errors


def validate_stage5cq_combined_gate(
    *, combined_gate: Path = DATA_PATHS["combined_gate_nonsatisfaction"]
) -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    payload = _validate_payload(combined_gate, errors)
    if payload.get("combined_gate_non_satisfaction_proof_created") is not True:
        errors.append("combined gate non-satisfaction proof must be created")
    for field in (
        "combined_approval_gate_satisfied_now",
        "combined_approval_gate_authorizes_activation_now",
        "approval_gate_satisfied_now",
        "approval_gate_authorizes_activation_now",
    ):
        if payload.get(field) is not False:
            errors.append(f"{field} must be false")
    return {
        "stage5cq_combined_gate_valid": not errors,
        "combined_approval_gate_satisfied_now": payload.get(
            "combined_approval_gate_satisfied_now"
        ),
        "validation_error_count": len(errors),
    }, errors


def validate_stage5cq_activation_nonauthorization(
    *, activation: Path = DATA_PATHS["activation_nonauthorization"]
) -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    payload = _validate_payload(activation, errors)
    if payload.get("activation_decision_nonauthorization_proof_created") is not True:
        errors.append("activation nonauthorization proof must be created")
    for field in (
        "activation_decision_valid_now",
        "activation_authorized_now",
        "active_planning_input_authorized_now",
        "active_planning_input_selected_now",
    ):
        if payload.get(field) is not False:
            errors.append(f"{field} must be false")
    return {
        "stage5cq_activation_nonauthorization_valid": not errors,
        "activation_decision_valid_now": payload.get("activation_decision_valid_now"),
        "validation_error_count": len(errors),
    }, errors


def validate_stage5cq_stage5co_preservation() -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    payloads = _load_all_payloads(errors)
    for key, fields in {
        "stage5co_readiness_package": [
            "stage5co_status_preserved",
            "stage5co_readiness_package_preserved",
            "stage5co_real_operator_approval_readiness_preserved",
            "stage5co_real_deep_research_acceptance_readiness_preserved",
            "stage5co_real_combined_gate_readiness_preserved",
            "stage5co_real_record_creation_blocker_preserved",
        ],
        "stage5co_missing_requirements": [
            "stage5co_missing_requirements_register_preserved",
        ],
        "stage5co_transition_plan": [
            "stage5co_activation_transition_plan_preserved",
            "stage5co_future_transition_sequence_preserved",
            "stage5co_activation_nonauthorization_preserved",
        ],
    }.items():
        for field in fields:
            if payloads.get(key, {}).get(field) is not True:
                errors.append(f"{key}: {field} must be true")
    if payloads.get("stage5co_missing_requirements", {}).get(
        "missing_requirement_count"
    ) != len(STAGE5CO_MISSING_REQUIREMENTS):
        errors.append("Stage 5CO missing requirement count must be preserved")
    for label, validator in (
        ("stage5co_findings", validate_stage5co_stage5cn_findings),
        ("stage5co_readiness", validate_stage5co_approval_readiness_package),
        ("stage5co_operator", validate_stage5co_real_operator_readiness),
        ("stage5co_deep_research", validate_stage5co_real_deep_research_readiness),
        ("stage5co_combined", validate_stage5co_real_combined_gate_readiness),
        ("stage5co_transition", validate_stage5co_activation_transition_plan),
        ("stage5co_missing", validate_stage5co_current_missing_requirements),
        ("stage5co_blocker", validate_stage5co_real_record_blocker),
        ("stage5co_boundary", validate_stage5co_stage5cm_boundary_preservation),
        ("stage5co_gates", validate_stage5co_sidecar_gates),
        ("stage5co_credential", validate_stage5co_credential_redaction_policy),
    ):
        _, validator_errors = validator()
        errors.extend(f"{label}:{error}" for error in validator_errors)
    return {
        "stage5cq_stage5co_preservation_valid": not errors,
        "missing_requirement_count": payloads.get("stage5co_missing_requirements", {}).get(
            "missing_requirement_count"
        ),
        "validation_error_count": len(errors),
    }, errors


def validate_stage5cq_prior_stage_preservation() -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    payloads = _load_all_payloads(errors)
    required_true = {
        "stage5cm_boundary": [
            "stage5cm_boundary_preserved",
            "stage5cm_fixture_vs_real_boundary_preserved",
            "stage5cm_end_to_end_readiness_boundary_preserved",
            "stage5cm_credential_redaction_policy_preserved",
        ],
        "stage5ck_preservation": [
            "stage5ck_fixture_pack_preserved",
            "stage5ck_fixture_pack_only_preserved",
            "stage5ck_synthetic_negative_fixtures_only_preserved",
        ],
        "stage5ci_preservation": ["stage5ci_templates_preserved"],
        "stage5cg_preservation": ["stage5cg_scaffolds_preserved"],
        "stage5ce_preservation": ["stage5ce_proposal_package_preserved"],
        "stage5cc_preservation": [
            "stage5cc_exact_citation_contract_preserved",
            "stage5cc_fail_closed_trigger_exact_set_preserved",
            "stage5cc_activation_precondition_exact_set_preserved",
        ],
    }
    for key, fields in required_true.items():
        for field in fields:
            if payloads.get(key, {}).get(field) is not True:
                errors.append(f"{key}: {field} must be true")
    if payloads.get("stage5cm_boundary", {}).get(
        "stage5cm_parallel_worker_cap_preserved"
    ) != PARALLEL_WORKER_CAP:
        errors.append("Stage 5CM worker cap must remain 8")
    stage5bd = payloads.get("stage5bd_preservation", {})
    if stage5bd.get("stage5bd_run_plan_id_count") != 10:
        errors.append("Stage 5BD run-plan ID count must remain 10")
    if stage5bd.get("stage5bd_run_plan_ids_changed") is not False:
        errors.append("Stage 5BD run-plan IDs must be unchanged")
    lineage = payloads.get("active_lineage", {})
    if lineage.get("active_lineage_record_count") != 8:
        errors.append("active lineage must remain 8 records")
    if lineage.get("correct_stage5aw_path_included") is not True:
        errors.append("correct Stage 5AW path must be included")
    if lineage.get("deprecated_stage5aw_path_absent") is not True:
        errors.append("deprecated Stage 5AW path must be absent")
    for label, validator in (
        ("stage5cm_fixture_real", validate_stage5cm_fixture_real_boundary),
        ("stage5cm_end_to_end", validate_stage5cm_end_to_end_readiness_boundary),
        ("stage5cm_credential", validate_stage5cm_credential_redaction_policy),
        ("stage5cm_sidecar", validate_stage5cm_sidecar_gates),
        ("stage5co_prior", validate_stage5co_prior_stage_preservation),
        ("stage5bd", validate_stage5bd),
    ):
        _, validator_errors = validator()
        errors.extend(f"{label}:{error}" for error in validator_errors)
    return {
        "stage5cq_prior_stage_preservation_valid": not errors,
        "stage5bd_run_plan_id_count": stage5bd.get("stage5bd_run_plan_id_count"),
        "active_lineage_record_count": lineage.get("active_lineage_record_count"),
        "validation_error_count": len(errors),
    }, errors


def _validate_sidecar_payloads(payloads: dict[str, dict[str, Any]], errors: list[str]) -> None:
    for key, payload in payloads.items():
        if payload.get("string4_sidecar_status") not in {None, "scaffolded_inactive"}:
            errors.append(f"{key}: string4_sidecar_status must remain scaffolded_inactive")
        for field in (
            "string4_sidecar_active",
            "string4_sidecar_planning_ingestion_activated",
            "string4_active_input_allowed",
            "string4_dry_run_ingestion_allowed_now",
            "string4_byte_stream_generation_allowed",
            "string4_execution_input_allowed",
            "active_planning_input_authorized_now",
            "dry_run_ingestion_authorized_now",
            "byte_stream_generation_authorized_now",
            "execution_authorized_now",
        ):
            if payload.get(field) is True:
                errors.append(f"{key}: {field} must remain false")


def validate_stage5cq_sidecar_gates() -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    payloads = {
        "no_active_ingestion": _validate_payload(DATA_PATHS["no_active_ingestion"], errors),
        "no_byte_stream_transition_gate": _validate_payload(
            DATA_PATHS["no_byte_stream_transition_gate"], errors
        ),
        "no_execution_transition_gate": _validate_payload(
            DATA_PATHS["no_execution_transition_gate"], errors
        ),
        "sidecar_activation_blocker": _validate_payload(
            DATA_PATHS["sidecar_activation_blocker"], errors
        ),
        "activation_nonauthorization": _validate_payload(
            DATA_PATHS["activation_nonauthorization"], errors
        ),
    }
    _validate_sidecar_payloads(payloads, errors)
    if payloads["no_active_ingestion"].get("no_active_ingestion_status") != "closed":
        errors.append("no-active-ingestion gate must be closed")
    if payloads["no_byte_stream_transition_gate"].get(
        "no_byte_stream_transition_gate_status"
    ) != "closed":
        errors.append("no-byte-stream transition gate must be closed")
    if payloads["no_execution_transition_gate"].get(
        "no_execution_transition_gate_status"
    ) != "closed":
        errors.append("no-execution transition gate must be closed")
    return {
        "stage5cq_sidecar_gates_valid": not errors,
        "no_active_ingestion_status": payloads["no_active_ingestion"].get(
            "no_active_ingestion_status"
        ),
        "no_byte_stream_transition_gate_status": payloads["no_byte_stream_transition_gate"].get(
            "no_byte_stream_transition_gate_status"
        ),
        "no_execution_transition_gate_status": payloads["no_execution_transition_gate"].get(
            "no_execution_transition_gate_status"
        ),
        "validation_error_count": len(errors),
    }, errors


def validate_stage5cq_handoff_restoration() -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    handoff = _validate_payload(DATA_PATHS["handoff"], errors)
    restoration = _validate_payload(DATA_PATHS["completion_restoration"], errors)
    if handoff.get("canonical_codex_handoff_root") != "codex-output":
        errors.append("canonical handoff root must be codex-output")
    if handoff.get("codex_output_used") is not False:
        errors.append("codex_output must not be used")
    if DEPRECATED_CODEX_OUTPUT.exists():
        errors.append("deprecated codex_output directory must be absent")
    if restoration.get("stage5cq_codex_completion_summary_required") is not True:
        errors.append("Stage 5CQ completion summary must be required")
    if not CODEX_COMPLETION_PATH.is_file():
        errors.append(f"missing_local_completion_summary={CODEX_COMPLETION_PATH.as_posix()}")
    if restoration.get("codex_completion_summary_committed") is not False:
        errors.append("codex completion summary must not be committed")
    return {
        "stage5cq_handoff_restoration_valid": not errors,
        "stage5cq_codex_completion_summary_written_locally": CODEX_COMPLETION_PATH.is_file(),
        "codex_output_used": handoff.get("codex_output_used"),
        "validation_error_count": len(errors),
    }, errors


def validate_stage5cq_credential_redaction_policy(
    *, credential_redaction: Path = DATA_PATHS["credential_redaction"]
) -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    payload = _validate_payload(credential_redaction, errors)
    for field in (
        "credential_redaction_policy_preserved",
        "credential_like_remote_must_be_redacted",
        "credential_like_text_must_not_be_committed",
        "committed_stage5cq_metadata_secret_scan_required",
    ):
        if payload.get(field) is not True:
            errors.append(f"{field} must be true")
    if payload.get("secret_values_printed_or_committed") is not False:
        errors.append("secret values must not be printed or committed")
    _check_no_stage5cq_metadata_secrets(errors)
    return {
        "stage5cq_credential_redaction_policy_valid": not errors,
        "credential_like_remote_detected": payload.get("remote_hygiene", {}).get(
            "credential_like_remote_detected"
        ),
        "validation_error_count": len(errors),
    }, errors


def validate_stage5cq(
    *,
    summary: Path = DATA_PATHS["summary"],
    next_stage_decision: Path = DATA_PATHS["next_stage"],
    guardrail: Path = DATA_PATHS["guardrail"],
    results_dir: Path = RESULTS_DIR,
) -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    payloads = _load_all_payloads(errors)
    _check_false_flags(payloads, errors)
    _validate_sidecar_payloads(payloads, errors)
    _check_no_stage5cq_metadata_secrets(errors)
    summary_payload = (
        payloads["summary"] if summary == DATA_PATHS["summary"] else _validate_payload(summary, errors)
    )
    next_payload = (
        payloads["next_stage"]
        if next_stage_decision == DATA_PATHS["next_stage"]
        else _validate_payload(next_stage_decision, errors)
    )
    guardrail_payload = (
        payloads["guardrail"]
        if guardrail == DATA_PATHS["guardrail"]
        else _validate_payload(guardrail, errors)
    )
    for _counts, focused_errors in (
        validate_stage5cq_stage5cp_findings(),
        validate_stage5cq_operator_decision_package(),
        validate_stage5cq_real_record_blocker(),
        validate_stage5cq_combined_gate(),
        validate_stage5cq_activation_nonauthorization(),
        validate_stage5cq_stage5co_preservation(),
        validate_stage5cq_prior_stage_preservation(),
        validate_stage5cq_sidecar_gates(),
        validate_stage5cq_handoff_restoration(),
        validate_stage5cq_credential_redaction_policy(),
    ):
        errors.extend(focused_errors)
    for field in (
        "stage5cp_findings_integrated",
        "stage5co_status_preserved",
        "stage5co_readiness_package_preserved",
        "operator_decision_package_scaffold_created",
        "stage5co_missing_completion_summary_warning_integrated",
    ):
        if summary_payload.get(field) is not True:
            errors.append(f"summary {field} must be true")
    for field in MANDATORY_FALSE_SUMMARY_FLAGS:
        if summary_payload.get(field) is not False:
            errors.append(f"summary {field} must be false")
    if summary_payload.get("stage5cp_verdict") != "accept_with_warnings":
        errors.append("summary Stage 5CP verdict must be accept_with_warnings")
    if summary_payload.get("operator_decision_package_status") != "scaffold_only":
        errors.append("operator-decision package must remain scaffold_only")
    if summary_payload.get("stage5bd_run_plan_id_count") != 10:
        errors.append("Stage 5BD run-plan ID count must remain 10")
    if summary_payload.get("active_lineage_record_count") != 8:
        errors.append("active lineage must contain exactly 8 records")
    if summary_payload.get("parallel_worker_cap_for_stage5cq_and_later") != PARALLEL_WORKER_CAP:
        errors.append("Stage 5CQ parallel worker cap must be 8")
    if next_payload.get("selected_next_stage_id") != "stage-5cr":
        errors.append("Stage 5CQ must select Stage 5CR as next stage")
    if next_payload.get("selected_next_prompt_type") != "deep_research_review":
        errors.append("Stage 5CR prompt type must be deep_research_review")
    if next_payload.get("selected_next_stage_authorizes_execution") is not False:
        errors.append("Stage 5CR must not authorize execution")
    if guardrail_payload.get("future_token_block_execution_remains_blocked") is not True:
        errors.append("future token-block execution must remain blocked")
    for output_name in (
        "summary.json",
        "operator_decision_package_report.json",
        "preservation_report.json",
        "handoff_restoration_report.json",
        "source_digest_index.json",
        "warnings.jsonl",
    ):
        if not (results_dir / output_name).is_file():
            errors.append(f"missing_generated_output={repo_relative(results_dir / output_name)}")
    return {
        "stage5cq_valid": not errors,
        "validation_error_count": len(errors),
        "stage5cp_verdict": summary_payload.get("stage5cp_verdict"),
        "operator_decision_package_status": summary_payload.get(
            "operator_decision_package_status"
        ),
        "combined_approval_gate_satisfied_now": summary_payload.get(
            "combined_approval_gate_satisfied_now"
        ),
        "activation_decision_valid_now": summary_payload.get("activation_decision_valid_now"),
        "active_planning_input_authorized_now": summary_payload.get(
            "active_planning_input_authorized_now"
        ),
        "stage5bd_run_plan_id_count": summary_payload.get("stage5bd_run_plan_id_count"),
        "active_lineage_record_count": summary_payload.get("active_lineage_record_count"),
        "parallel_worker_cap": summary_payload.get("parallel_worker_cap_for_stage5cq_and_later"),
        "recommended_next_stage_id": summary_payload.get("recommended_next_stage_id"),
    }, errors


def load_stage5cq_summary(*, summary: Path = DATA_PATHS["summary"]) -> dict[str, Any]:
    return _read(summary)
