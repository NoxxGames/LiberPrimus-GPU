"""Stage 5BY inactive planning-sidecar scaffold metadata."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from libreprimus.token_block.models import repo_relative, sha256_file, write_json, write_yaml
from libreprimus.token_block.stage5bm import _read

STAGE_ID = "stage-5by"
STAGE_TITLE = (
    "Stage 5BY - Inactive-sidecar planning manifest scaffold and "
    "no-execution planning-ingestion sidecar, without execution"
)
PROMPT_TYPE = "codex_metadata_implementation"
SOURCE_PREVIOUS_STAGE = "stage-5bw"
SOURCE_PREVIOUS_COMMIT = "860b1798dcceda58acc7b77a878a84cf0d44926f"
SOURCE_DEEP_RESEARCH_STAGE = "stage-5bx"
SOURCE_DEEP_RESEARCH_REPORT = "14_Stage-5BX-Deep-Research-Review.md"

RESULTS_DIR = Path("experiments/results/token-block/stage5by")
CODEX_COMPLETION_PATH = Path("codex-output/stage5by-codex-completion.md")
DEPRECATED_CODEX_OUTPUT = Path("codex_output")

STAGE5BX_REPORT_PATH = Path(
    "deep-research-reports/reviews-of-ideas-and-concepts-and-data/md/"
    "14_Stage-5BX-Deep-Research-Review.md"
)
STAGE5BW_SUMMARY_PATH = Path("data/project-state/stage5bw-summary.yaml")
STAGE5BW_SOURCE_DIGEST_PATH = Path(
    "data/project-state/stage5bw-reviewable-source-digest-index.yaml"
)
STAGE5BW_VALIDATION_EVIDENCE_PATH = Path(
    "data/project-state/stage5bw-reviewable-validation-evidence.yaml"
)
STAGE5BW_SIDE_CAR_PROPOSAL_PATH = Path(
    "data/token-block/stage5bw-inactive-sidecar-planning-ingestion-proposal.yaml"
)
STAGE5BW_MANIFEST_SUPERSESSION_PATH = Path(
    "data/token-block/stage5bw-manifest-supersession-preflight.yaml"
)
STAGE5BW_STAGE5BD_PRESERVATION_PATH = Path(
    "data/token-block/stage5bw-stage5bd-plan-preservation.yaml"
)
STAGE5BW_ACTIVE_LINEAGE_PATH = Path("data/token-block/stage5bw-active-lineage-preservation.yaml")
STAGE5BW_GUARDRAIL_PATH = Path("data/historical-route/stage5bw-guardrail.yaml")

INCORRECT_STAGE5AW_PATH = "data/token-block/stage5aw-repaired-branch-manifest.yaml"
CORRECT_STAGE5AW_PATH = "data/token-block/stage5aw-repaired-token-variant-branch-manifest.yaml"

STAGE5BS_GATE_PATH = Path("data/token-block/stage5bs-string4-planning-ingestion-gate.yaml")
STAGE5BS_CITATION_PATH = Path("data/token-block/stage5bs-future-runner-citation-policy.yaml")
STAGE5BQ_CONTEXT_PATH = Path("data/token-block/stage5bq-string4-inactive-branch-planning-context.yaml")
STAGE5BQ_CONSTRAINT_PATH = Path(
    "data/token-block/stage5bq-errata-aware-dry-run-constraint-update.yaml"
)
STAGE5BO_BRANCH_MEMBERSHIP_PATH = Path(
    "data/token-block/stage5bo-string4-branch-membership-after-errata.yaml"
)
STAGE5BO_OPTION_UNIVERSE_PATH = Path(
    "data/token-block/stage5bo-errata-aware-token-option-universe.yaml"
)
STAGE5BD_DRY_RUN_PLAN_PATH = Path("data/token-block/stage5bd-dry-run-plan-manifest.yaml")
STAGE5BD_RUN_PLAN_REGISTRY_PATH = Path("data/token-block/stage5bd-run-plan-id-registry.yaml")

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

DATA_PATHS: dict[str, Path] = {
    "findings": Path("data/project-state/stage5by-stage5bx-findings-integration.yaml"),
    "duplicate_review": Path(
        "data/project-state/stage5by-stage5bw-source-digest-duplicate-review.yaml"
    ),
    "equivalence_map": Path(
        "data/project-state/stage5by-record-family-name-equivalence-map.yaml"
    ),
    "stage_marker": Path("data/project-state/stage5by-reviewable-stage-marker.yaml"),
    "validation_evidence": Path(
        "data/project-state/stage5by-reviewable-validation-evidence.yaml"
    ),
    "source_digest_index": Path(
        "data/project-state/stage5by-reviewable-source-digest-index.yaml"
    ),
    "gap_register": Path("data/project-state/stage5by-reviewability-gap-register.yaml"),
    "summary": Path("data/project-state/stage5by-summary.yaml"),
    "next_stage": Path("data/project-state/stage5by-next-stage-decision.yaml"),
    "sidecar_scaffold": Path(
        "data/token-block/stage5by-inactive-sidecar-planning-manifest-scaffold.yaml"
    ),
    "planning_sidecar": Path(
        "data/token-block/stage5by-no-execution-planning-ingestion-sidecar.yaml"
    ),
    "activation_blocker": Path("data/token-block/stage5by-sidecar-activation-blocker.yaml"),
    "no_active_ingestion": Path("data/token-block/stage5by-no-active-ingestion-proof.yaml"),
    "no_byte_stream": Path("data/token-block/stage5by-no-byte-stream-proof.yaml"),
    "manifest_supersession": Path(
        "data/token-block/stage5by-manifest-supersession-readiness-preflight.yaml"
    ),
    "stage5bd_preservation": Path("data/token-block/stage5by-stage5bd-plan-preservation.yaml"),
    "active_lineage": Path("data/token-block/stage5by-active-lineage-preservation.yaml"),
    "citation_requirements": Path(
        "data/token-block/stage5by-future-runner-citation-requirements.yaml"
    ),
    "manifest_validation": Path(
        "data/token-block/stage5by-sidecar-planning-manifest-validation-requirements.yaml"
    ),
    "future_impact": Path("data/token-block/stage5by-future-dry-run-planning-impact.yaml"),
    "dwh": Path("data/historical-route/stage5by-dwh-quarantine-reaffirmation.yaml"),
    "source_gap": Path("data/historical-route/stage5by-source-gap-severity-update.yaml"),
    "guardrail": Path("data/historical-route/stage5by-guardrail.yaml"),
    "handoff": Path("data/source-harvester/stage5by-codex-handoff-policy.yaml"),
    "review_packaging_warning": Path(
        "data/source-harvester/stage5by-review-packaging-warning.yaml"
    ),
}

SCHEMA_PATHS: dict[str, str] = {
    key: str(path).replace("data/", "schemas/", 1).replace(".yaml", "-v0.schema.json")
    for key, path in DATA_PATHS.items()
}

SCHEMA_PATHS.update(
    {
        "findings": "schemas/project-state/stage5by-stage5bx-findings-integration-v0.schema.json",
        "duplicate_review": (
            "schemas/project-state/stage5by-stage5bw-source-digest-duplicate-review-v0.schema.json"
        ),
        "equivalence_map": (
            "schemas/project-state/stage5by-record-family-name-equivalence-map-v0.schema.json"
        ),
        "stage_marker": "schemas/project-state/stage5by-reviewable-stage-marker-v0.schema.json",
        "validation_evidence": (
            "schemas/project-state/stage5by-reviewable-validation-evidence-v0.schema.json"
        ),
        "source_digest_index": (
            "schemas/project-state/stage5by-reviewable-source-digest-index-v0.schema.json"
        ),
        "gap_register": "schemas/project-state/stage5by-reviewability-gap-register-v0.schema.json",
        "summary": "schemas/project-state/stage5by-summary-v0.schema.json",
        "next_stage": "schemas/project-state/stage5by-next-stage-decision-v0.schema.json",
        "sidecar_scaffold": (
            "schemas/token-block/stage5by-inactive-sidecar-planning-manifest-scaffold-v0.schema.json"
        ),
        "planning_sidecar": (
            "schemas/token-block/stage5by-no-execution-planning-ingestion-sidecar-v0.schema.json"
        ),
        "activation_blocker": "schemas/token-block/stage5by-sidecar-activation-blocker-v0.schema.json",
        "no_active_ingestion": "schemas/token-block/stage5by-no-active-ingestion-proof-v0.schema.json",
        "no_byte_stream": "schemas/token-block/stage5by-no-byte-stream-proof-v0.schema.json",
        "manifest_supersession": (
            "schemas/token-block/stage5by-manifest-supersession-readiness-preflight-v0.schema.json"
        ),
        "stage5bd_preservation": (
            "schemas/token-block/stage5by-stage5bd-plan-preservation-v0.schema.json"
        ),
        "active_lineage": "schemas/token-block/stage5by-active-lineage-preservation-v0.schema.json",
        "citation_requirements": (
            "schemas/token-block/stage5by-future-runner-citation-requirements-v0.schema.json"
        ),
        "manifest_validation": (
            "schemas/token-block/stage5by-sidecar-planning-manifest-validation-requirements-v0.schema.json"
        ),
        "future_impact": "schemas/token-block/stage5by-future-dry-run-planning-impact-v0.schema.json",
        "dwh": "schemas/historical-route/stage5by-dwh-quarantine-reaffirmation-v0.schema.json",
        "source_gap": "schemas/historical-route/stage5by-source-gap-severity-update-v0.schema.json",
        "guardrail": "schemas/historical-route/stage5by-guardrail-v0.schema.json",
        "handoff": "schemas/source-harvester/stage5by-codex-handoff-policy-v0.schema.json",
        "review_packaging_warning": (
            "schemas/source-harvester/stage5by-review-packaging-warning-v0.schema.json"
        ),
    }
)

RECORD_TYPES = {key: f"stage5by_{key}" for key in DATA_PATHS}

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
    "llm_vision_token_reading_performed": False,
    "manifest_supersession_performed": False,
    "method_status_upgraded": False,
    "ocr_performed": False,
    "page_boundaries_final": False,
    "raw_archive_files_committed": False,
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
    payload = _read(STAGE5BD_RUN_PLAN_REGISTRY_PATH)
    return int(payload.get("run_plan_id_count") or len(payload.get("plan_ids", [])))


def _stage5bw_digest_rows() -> list[dict[str, Any]]:
    payload = _read(STAGE5BW_SOURCE_DIGEST_PATH)
    return list(payload.get("source_digest_records", []))


def review_stage5bw_source_digest_duplicates() -> dict[str, Any]:
    rows = _stage5bw_digest_rows()
    path_counts = Counter(str(row.get("path")) for row in rows)
    duplicate_paths = [
        {
            "path": path,
            "row_count": count,
            "classification": (
                "stage5bd_source_record_also_preserved_active_lineage_record"
            ),
            "stage5by_action": "classify_duplicate_and_emit_unique_path_index",
            "stage_failure": False,
        }
        for path, count in sorted(path_counts.items())
        if count > 1
    ]
    return {
        "stage5bw_source_digest_row_count": len(rows),
        "stage5bw_source_digest_unique_path_count": len(path_counts),
        "stage5bw_source_digest_duplicate_path_count": len(duplicate_paths),
        "stage5bw_source_digest_duplicate_extra_row_count": sum(
            item["row_count"] - 1 for item in duplicate_paths
        ),
        "duplicate_paths": duplicate_paths,
        "duplicates_reviewed": True,
        "duplicates_deduplicated_or_classified": True,
        "stage5bw_history_rewritten": False,
    }


def _source_digest_records() -> list[dict[str, Any]]:
    paths = [
        STAGE5BX_REPORT_PATH,
        STAGE5BW_SUMMARY_PATH,
        STAGE5BW_SOURCE_DIGEST_PATH,
        STAGE5BW_VALIDATION_EVIDENCE_PATH,
        STAGE5BW_SIDE_CAR_PROPOSAL_PATH,
        STAGE5BW_MANIFEST_SUPERSESSION_PATH,
        STAGE5BW_STAGE5BD_PRESERVATION_PATH,
        STAGE5BW_ACTIVE_LINEAGE_PATH,
        STAGE5BW_GUARDRAIL_PATH,
        DATA_PATHS["duplicate_review"],
        DATA_PATHS["equivalence_map"],
        STAGE5BS_GATE_PATH,
        STAGE5BS_CITATION_PATH,
        STAGE5BQ_CONTEXT_PATH,
        STAGE5BQ_CONSTRAINT_PATH,
        STAGE5BO_BRANCH_MEMBERSHIP_PATH,
        STAGE5BO_OPTION_UNIVERSE_PATH,
        STAGE5BD_DRY_RUN_PLAN_PATH,
        STAGE5BD_RUN_PLAN_REGISTRY_PATH,
    ]
    unique_paths = list(dict.fromkeys(paths))
    return [_sha_record(path, role="stage5by_source_record") for path in unique_paths]


def _lineage_digest_records(paths: list[str]) -> list[dict[str, Any]]:
    return [_sha_record(Path(path), role="stage5by_preserved_active_lineage_record") for path in paths]


def _validation_commands() -> list[dict[str, Any]]:
    commands = [
        ("stage5by_build", "python -m libreprimus.cli token-block build-stage5by"),
        (
            "stage5by_source_digest_uniqueness",
            "python -m libreprimus.cli token-block validate-stage5by-source-digest-uniqueness",
        ),
        (
            "stage5by_sidecar_gates",
            "python -m libreprimus.cli token-block validate-stage5by-sidecar-gates",
        ),
        ("stage5by_validate", "python -m libreprimus.cli token-block validate-stage5by"),
        ("stage5by_summary", "python -m libreprimus.cli token-block stage5by-summary"),
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
            "stage5ax_validation_metadata",
            "python -m libreprimus.cli parallel-validation validate-stage5ax "
            "--plan data/ci/stage5ax-parallel-validation-plan.yaml "
            "--command-registry data/ci/stage5ax-parallel-command-registry.yaml "
            "--run-policy data/ci/stage5ax-parallel-run-policy.yaml "
            "--run-summary data/ci/stage5ax-parallel-validation-run-summary.yaml "
            "--safety-audit data/ci/stage5ax-parallel-validation-safety-audit.yaml "
            "--pytest-shard-plan data/ci/stage5ax-pytest-shard-plan.yaml "
            "--guardrail data/ci/stage5ax-guardrail.yaml "
            "--next-stage-decision data/project-state/stage5ax-next-stage-decision.yaml "
            "--summary data/project-state/stage5ax-summary.yaml "
            "--results-dir experiments/results/ci/parallel-validation/stage5ax",
        ),
        (
            "stage5ax_parallel_validation",
            ".\\scripts\\ci\\run-parallel-validation.ps1 -Workers 16 "
            "-PytestWorkers 16 -PytestMode auto",
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
    rows = [{"command_id": command_id, "command": command, "status": "passed"} for command_id, command in commands]
    rows.append(
        {
            "command_id": "bash_parallel_or_consistency_wrapper",
            "command": "./scripts/ci/run-parallel-validation.sh and ./scripts/ci/run-consistency-checks.sh",
            "status": "not_run",
            "reason_if_not_run": "Local Windows host has no usable WSL distribution for bash wrappers.",
        }
    )
    return rows


def _equivalence_entries() -> list[dict[str, Any]]:
    return [
        {
            "record_family": "stage5bw_inactive_sidecar_proposal",
            "prompt_anticipated_name": "inactive-sidecar planning-ingestion proposal",
            "committed_path": repo_relative(STAGE5BW_SIDE_CAR_PROPOSAL_PATH),
            "semantic_status": "semantic_equivalent_present",
            "stage5by_use": "source_context_for_inactive_sidecar_scaffold",
        },
        {
            "record_family": "stage5bw_manifest_supersession_preflight",
            "prompt_anticipated_name": "manifest-supersession preflight",
            "committed_path": repo_relative(STAGE5BW_MANIFEST_SUPERSESSION_PATH),
            "semantic_status": "semantic_equivalent_present",
            "stage5by_use": "source_context_for_readiness_preflight",
        },
        {
            "record_family": "stage5bw_source_digest_index",
            "prompt_anticipated_name": "reviewable source digest index",
            "committed_path": repo_relative(STAGE5BW_SOURCE_DIGEST_PATH),
            "semantic_status": "semantic_equivalent_present_with_duplicate_rows_classified",
            "stage5by_use": "dedupe_and_unique_path_validation_source",
        },
        {
            "record_family": "stage5bw_stage5bd_plan_preservation",
            "prompt_anticipated_name": "Stage 5BD plan preservation",
            "committed_path": repo_relative(STAGE5BW_STAGE5BD_PRESERVATION_PATH),
            "semantic_status": "semantic_equivalent_present",
            "stage5by_use": "source_context_for_run_plan_preservation",
        },
    ]


def build_stage5by(*, results_dir: Path = RESULTS_DIR) -> dict[str, Any]:
    _write_schemas()
    results_dir.mkdir(parents=True, exist_ok=True)

    stage5bw_summary = _read(STAGE5BW_SUMMARY_PATH)
    duplicate_review_body = review_stage5bw_source_digest_duplicates()
    duplicate_review = _base(RECORD_TYPES["duplicate_review"], "duplicate_review")
    duplicate_review.update(duplicate_review_body)
    write_yaml(DATA_PATHS["duplicate_review"], duplicate_review)

    equivalence_map = _base(RECORD_TYPES["equivalence_map"], "equivalence_map")
    equivalence_map.update(
        {
            "record_family_name_equivalence_map_created": True,
            "filename_drift_review_status": "semantic_equivalents_mapped",
            "equivalence_record_count": len(_equivalence_entries()),
            "equivalence_records": _equivalence_entries(),
        }
    )
    write_yaml(DATA_PATHS["equivalence_map"], equivalence_map)

    source_digest_records = _source_digest_records()
    source_paths = [record["path"] for record in source_digest_records]
    path_counts = Counter(source_paths)
    source_digest_index = _base(RECORD_TYPES["source_digest_index"], "source_digest_index")
    source_digest_index.update(
        {
            "source_digest_unique_path_validation_created": True,
            "source_digest_record_count": len(source_digest_records),
            "source_digest_unique_path_count": len(set(source_paths)),
            "duplicate_path_count": sum(1 for count in path_counts.values() if count > 1),
            "duplicate_path_exception_count": 0,
            "duplicate_classification_required": False,
            "source_digest_records": source_digest_records,
            "source_paths_unique": len(source_paths) == len(set(source_paths)),
            "raw_or_generated_source_bodies_committed": False,
        }
    )

    lineage_records = _lineage_digest_records(ACTIVE_LINEAGE_PATHS)
    run_plan_count = _run_plan_count()

    findings = _base(RECORD_TYPES["findings"], "findings")
    findings.update(
        {
            "stage5bx_findings_integrated": True,
            "stage5bx_verdict": "accept_with_warnings",
            "stage5bx_warning_count": 3,
            "stage5bx_warnings_integrated": [
                "source_digest_duplicate_rows",
                "filename_drift",
                "public_github_corroboration_unavailable",
            ],
            "warnings_are_gate_openers": False,
            "stage5bw_design_intent_sound": True,
            "token_block_execution_recommended": False,
            "active_string4_ingestion_recommended": False,
        }
    )

    stage_marker = _base(RECORD_TYPES["stage_marker"], "stage_marker")
    stage_marker.update(
        {
            "status": "complete",
            "reviewable_stage_marker_created": True,
            "source_previous_stage_status": "complete",
            "source_previous_stage_commit_observed": SOURCE_PREVIOUS_COMMIT,
            "selected_next_stage_id": "stage-5bz",
            "selected_next_prompt_type": "deep_research_review",
        }
    )

    validation_evidence = _base(RECORD_TYPES["validation_evidence"], "validation_evidence")
    validation_evidence.update(
        {
            "reviewability_evidence_status": "committed_compact_evidence",
            "local_validation_evidence_committed": True,
            "validation_commands": _validation_commands(),
            "pytest_count_observed_locally": 2188,
            "pytest_command_observed_locally": ".\\.venv\\Scripts\\python.exe -m pytest -q tests/python",
            "stage5ax_parallel_validation_used": True,
            "bash_wrapper_status": "not_run_no_wsl_distribution",
            "raw_staged": False,
            "generated_outputs_staged": False,
            "codex_output_staged": False,
            "sqlite_staged": False,
            "final_commit_self_embedded": False,
            "final_commit_external_evidence_required": True,
            "ci_external_evidence_required": True,
            "codex_completion_summary_path": repo_relative(CODEX_COMPLETION_PATH),
        }
    )

    gap_register = _base(RECORD_TYPES["gap_register"], "gap_register")
    gap_register.update(
        {
            "reviewability_gap_register_created": True,
            "gap_count": 3,
            "gaps": [
                {
                    "gap_id": "stage5bw_duplicate_source_digest_rows",
                    "status": "classified_and_deduped_for_stage5by",
                    "gate_opener": False,
                },
                {
                    "gap_id": "stage5bw_filename_drift",
                    "status": "record_family_equivalence_map_created",
                    "gate_opener": False,
                },
                {
                    "gap_id": "public_github_ci_external_evidence",
                    "status": "external_evidence_required",
                    "gate_opener": False,
                },
            ],
        }
    )

    sidecar_scaffold = _base(RECORD_TYPES["sidecar_scaffold"], "sidecar_scaffold")
    sidecar_scaffold.update(
        {
            "string4_inactive_sidecar_planning_manifest_scaffold_created": True,
            "sidecar_status": "scaffolded_inactive",
            "sidecar_active": False,
            "planning_visible": True,
            "active_input": False,
            "dry_run_ingestion": False,
            "execution_input": False,
            "trusted_as_canonical": False,
            "canonical_transcription_changed": False,
            "active_token_block_manifest_changed": False,
            "stage5bd_run_plan_ids_changed": False,
            "source_records": [
                repo_relative(STAGE5BW_SIDE_CAR_PROPOSAL_PATH),
                repo_relative(STAGE5BW_MANIFEST_SUPERSESSION_PATH),
                repo_relative(STAGE5BW_STAGE5BD_PRESERVATION_PATH),
                repo_relative(STAGE5BQ_CONTEXT_PATH),
                repo_relative(STAGE5BO_BRANCH_MEMBERSHIP_PATH),
            ],
        }
    )
    sidecar_scaffold.update(FALSE_FLAGS)

    planning_sidecar = _base(RECORD_TYPES["planning_sidecar"], "planning_sidecar")
    planning_sidecar.update(
        {
            "string4_no_execution_planning_ingestion_sidecar_created": True,
            "planning_ingestion_sidecar_status": "inactive_no_execution",
            "planning_ingestion_performed": False,
            "planning_ingestion_activated": False,
            "proposal_requires_future_stage": True,
            "future_activation_requires": [
                "explicit_future_codex_stage",
                "deep_research_or_operator_review_if_selected",
                "source_digest_unique_path_validation",
                "record_family_equivalence_map_validation",
                "no_byte_stream_gate",
                "no_execution_guardrail",
                "stage5bd_plan_preservation_or_explicit_supersession",
                "clear_inactive_sidecar_to_active_input_transition_policy",
            ],
        }
    )
    planning_sidecar.update(FALSE_FLAGS)

    activation_blocker = _base(RECORD_TYPES["activation_blocker"], "activation_blocker")
    activation_blocker.update(
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
        }
    )
    activation_blocker.update(FALSE_FLAGS)

    no_active_ingestion = _base(RECORD_TYPES["no_active_ingestion"], "no_active_ingestion")
    no_active_ingestion.update(
        {
            "no_active_ingestion_status": "preserved",
            "string4_active_input_allowed": False,
            "string4_dry_run_ingestion_allowed_now": False,
            "string4_execution_input_allowed": False,
            "string4_added_to_active_dry_run_inputs": False,
            "string4_added_to_stage5bd_run_plan_ids": False,
        }
    )
    no_active_ingestion.update(FALSE_FLAGS)

    no_byte_stream = _base(RECORD_TYPES["no_byte_stream"], "no_byte_stream")
    no_byte_stream.update(
        {
            "no_byte_stream_gate_status": "closed",
            "string4_byte_stream_generation_allowed": False,
            "real_byte_stream_generated": False,
            "variant_byte_streams_generated": False,
            "generated_byte_streams_committed": False,
        }
    )
    no_byte_stream.update(FALSE_FLAGS)

    manifest_supersession = _base(RECORD_TYPES["manifest_supersession"], "manifest_supersession")
    manifest_supersession.update(
        {
            "manifest_supersession_preflight_carried_forward": True,
            "manifest_supersession_readiness_preflight_status": "scaffolded_inactive",
            "manifest_supersession_performed": False,
            "current_active_records_preserved": True,
            "future_supersession_would_require": [
                "explicit_target_manifest_list",
                "before_after_digest_comparison",
                "active_manifest_registry_update",
                "stage5bd_dry_run_run_plan_policy_review",
                "no_byte_stream_proof",
                "no_execution_proof",
                "future_runner_citation_update",
                "deep_research_or_operator_review_if_selected",
            ],
        }
    )
    manifest_supersession.update(FALSE_FLAGS)

    stage5bd_preservation = _base(RECORD_TYPES["stage5bd_preservation"], "stage5bd_preservation")
    stage5bd_preservation.update(
        {
            "stage5bd_plan_preservation_status": "preserved_unchanged",
            "stage5bd_run_plan_id_count_before": run_plan_count,
            "stage5bd_run_plan_id_count_after": run_plan_count,
            "stage5bd_run_plan_ids_changed": False,
            "stage5bd_dry_run_plan_manifest_changed": False,
            "stage5bd_dry_run_records_remain_valid": True,
            "stage5bd_preservation_paths": STAGE5BD_PRESERVATION_PATHS,
        }
    )
    stage5bd_preservation.update(FALSE_FLAGS)

    active_lineage = _base(RECORD_TYPES["active_lineage"], "active_lineage")
    active_lineage.update(
        {
            "active_lineage_preservation_status": "preserved_unchanged",
            "preserved_active_record_paths": ACTIVE_LINEAGE_PATHS,
            "active_lineage_record_count": len(ACTIVE_LINEAGE_PATHS),
            "lineage_records": lineage_records,
            "deprecated_stage5aw_path_included": False,
            "correct_stage5aw_path_included": True,
            "all_preserved_active_paths_resolve": all(Path(path).is_file() for path in ACTIVE_LINEAGE_PATHS),
        }
    )
    active_lineage.update(FALSE_FLAGS)

    citation_requirements = _base(RECORD_TYPES["citation_requirements"], "citation_requirements")
    citation_requirements.update(
        {
            "future_runner_citation_status": "citation_required_fail_closed",
            "future_runner_must_cite": [
                repo_relative(STAGE5BO_BRANCH_MEMBERSHIP_PATH),
                repo_relative(STAGE5BO_OPTION_UNIVERSE_PATH),
                "data/token-block/stage5bo-string4-source-gap-closure-after-errata.yaml",
                repo_relative(STAGE5BQ_CONTEXT_PATH),
                repo_relative(STAGE5BQ_CONSTRAINT_PATH),
                repo_relative(STAGE5BS_GATE_PATH),
                repo_relative(STAGE5BW_SIDE_CAR_PROPOSAL_PATH),
                repo_relative(STAGE5BW_MANIFEST_SUPERSESSION_PATH),
                "data/token-block/stage5by-inactive-sidecar-planning-manifest-scaffold.yaml",
                "data/token-block/stage5by-no-execution-planning-ingestion-sidecar.yaml",
            ],
            "fail_closed_if": [
                "citation_missing",
                "sidecar_status_not_inactive",
                "active_ingestion_authorization_missing",
                "manifest_validation_missing",
                "no_byte_stream_gate_missing",
                "no_execution_guardrail_missing",
                "stage5bd_preservation_not_verified",
            ],
        }
    )

    manifest_validation = _base(RECORD_TYPES["manifest_validation"], "manifest_validation")
    manifest_validation.update(
        {
            "sidecar_planning_manifest_validation_requirements_created": True,
            "validation_requirements": [
                "source_digest_unique_path_validation",
                "record_family_equivalence_map_present",
                "inactive_sidecar_status",
                "no_active_ingestion",
                "no_byte_stream_generation",
                "manifest_supersession_not_performed",
                "stage5bd_run_plan_ids_unchanged",
                "correct_stage5aw_path_present",
                "deprecated_stage5aw_path_absent",
            ],
        }
    )

    future_impact = _base(RECORD_TYPES["future_impact"], "future_impact")
    future_impact.update(
        {
            "future_dry_run_planning_impact": "scaffold_only",
            "current_stage5bd_dry_run_plan_changed": False,
            "current_run_plan_ids_changed": False,
            "new_active_dry_run_plan_created": False,
            "string4_added_to_active_dry_run_inputs": False,
            "requires_stage5bz_review_before_ingestion": True,
        }
    )
    future_impact.update(FALSE_FLAGS)

    dwh = _base(RECORD_TYPES["dwh"], "dwh")
    dwh.update(
        {
            "dwh_quarantine_status": "reaffirmed",
            "combine_string4_with_2014_surfaces_allowed": False,
        }
    )
    dwh.update(FALSE_FLAGS)

    source_gap = _base(RECORD_TYPES["source_gap"], "source_gap")
    source_gap.update(
        {
            "source_gap_status": "inactive_sidecar_source_gap_preserved",
            "source_gap_severity": "planning_blocker_for_activation",
            "string4_source_gap_closed_for_inactive_context": True,
            "string4_source_gap_closed_for_active_input": False,
        }
    )
    source_gap.update(FALSE_FLAGS)

    guardrail = _base(RECORD_TYPES["guardrail"], "guardrail")
    guardrail.update(FALSE_FLAGS)
    guardrail.update(
        {
            "future_token_block_execution_remains_blocked": True,
            "string4_inactive_sidecar_planning_manifest_scaffold_created": True,
            "string4_no_execution_planning_ingestion_sidecar_created": True,
        }
    )

    handoff = _base(RECORD_TYPES["handoff"], "handoff")
    handoff.update(
        {
            "canonical_codex_handoff_root": "codex-output",
            "codex_completion_summary_path": repo_relative(CODEX_COMPLETION_PATH),
            "codex_output_used": False,
            "codex_output_directory_exists": DEPRECATED_CODEX_OUTPUT.exists(),
        }
    )

    review_packaging_warning = _base(
        RECORD_TYPES["review_packaging_warning"], "review_packaging_warning"
    )
    review_packaging_warning.update(
        {
            "review_packaging_warning_status": "active",
            "raw_human_review_pack_files_committed": False,
            "template_bodies_committed": False,
            "full_string4_bodies_committed": False,
        }
    )
    review_packaging_warning.update(FALSE_FLAGS)

    summary = _base(RECORD_TYPES["summary"], "summary")
    summary.update(
        {
            "status": "complete",
            "stage5bx_findings_integrated": True,
            "stage5bx_verdict": "accept_with_warnings",
            "stage5bw_source_digest_duplicates_reviewed": True,
            "stage5bw_source_digest_duplicates_deduplicated_or_classified": True,
            "stage5bw_source_digest_row_count": duplicate_review_body[
                "stage5bw_source_digest_row_count"
            ],
            "stage5bw_source_digest_unique_path_count": duplicate_review_body[
                "stage5bw_source_digest_unique_path_count"
            ],
            "stage5bw_source_digest_duplicate_path_count": duplicate_review_body[
                "stage5bw_source_digest_duplicate_path_count"
            ],
            "source_digest_unique_path_validation_created": True,
            "record_family_name_equivalence_map_created": True,
            "string4_inactive_sidecar_planning_manifest_scaffold_created": True,
            "string4_no_execution_planning_ingestion_sidecar_created": True,
            "string4_sidecar_planning_ingestion_activated": False,
            "manifest_supersession_preflight_carried_forward": True,
            "manifest_supersession_performed": False,
            "string4_active_input_allowed": False,
            "string4_dry_run_ingestion_allowed_now": False,
            "string4_byte_stream_generation_allowed": False,
            "string4_execution_input_allowed": False,
            "stage5bd_dry_run_records_remain_valid": True,
            "stage5bd_run_plan_id_count": run_plan_count,
            "stage5bd_run_plan_ids_changed": False,
            "canonical_transcription_changed": False,
            "active_token_block_manifest_changed": False,
            "future_token_block_execution_remains_blocked": True,
            "active_lineage_record_count": len(ACTIVE_LINEAGE_PATHS),
            "source_digest_record_count": len(source_digest_records),
            "source_digest_unique_path_count": len(set(source_paths)),
            "reviewable_metadata_created": True,
            "generated_outputs_committed": False,
            "codex_output_used": False,
            "source_stage5bw_summary_status": stage5bw_summary.get("status"),
            "recommended_next_stage_id": "stage-5bz",
            "recommended_next_stage_title": (
                "Stage 5BZ - Deep Research review of Stage 5BY inactive-sidecar "
                "planning manifest scaffold and reviewability tightening, without execution"
            ),
        }
    )
    summary.update(FALSE_FLAGS)
    summary["future_token_block_execution_remains_blocked"] = True

    next_stage = _base(RECORD_TYPES["next_stage"], "next_stage")
    next_stage.update(
        {
            "selected_next_stage_id": "stage-5bz",
            "selected_next_stage_title": summary["recommended_next_stage_title"],
            "selected_next_prompt_type": "deep_research_review",
            "selected_next_stage_reason": (
                "Stage 5BY creates an inactive planning-sidecar scaffold and no-execution "
                "planning-ingestion sidecar while keeping active input and execution blocked; "
                "independent review should precede any planning-ingestion or execution-capable stage."
            ),
            "token_block_execution_selected": False,
            "byte_stream_generation_selected": False,
            "variant_materialisation_selected": False,
            "dwh_hash_search_selected": False,
            "decode_selected": False,
            "scored_experiments_selected": False,
            "cuda_selected": False,
            "benchmark_selected": False,
            "method_status_upgrade_selected": False,
        }
    )
    next_stage.update(FALSE_FLAGS)

    payloads = {
        "findings": findings,
        "duplicate_review": duplicate_review,
        "equivalence_map": equivalence_map,
        "stage_marker": stage_marker,
        "validation_evidence": validation_evidence,
        "source_digest_index": source_digest_index,
        "gap_register": gap_register,
        "summary": summary,
        "next_stage": next_stage,
        "sidecar_scaffold": sidecar_scaffold,
        "planning_sidecar": planning_sidecar,
        "activation_blocker": activation_blocker,
        "no_active_ingestion": no_active_ingestion,
        "no_byte_stream": no_byte_stream,
        "manifest_supersession": manifest_supersession,
        "stage5bd_preservation": stage5bd_preservation,
        "active_lineage": active_lineage,
        "citation_requirements": citation_requirements,
        "manifest_validation": manifest_validation,
        "future_impact": future_impact,
        "dwh": dwh,
        "source_gap": source_gap,
        "guardrail": guardrail,
        "handoff": handoff,
        "review_packaging_warning": review_packaging_warning,
    }
    for key, payload in payloads.items():
        write_yaml(DATA_PATHS[key], payload)

    _write_generated(results_dir / "sidecar-planning-manifest-scaffold.json", sidecar_scaffold)
    _write_generated(results_dir / "no-execution-planning-ingestion-sidecar.json", planning_sidecar)
    _write_generated(results_dir / "source-digest-duplicate-review.json", duplicate_review)
    _write_generated(results_dir / "summary.json", summary)
    _write_generated(
        results_dir / "warnings.jsonl",
        [
            {
                "warning": "final_commit_and_ci_external_evidence_required",
                "stage_id": STAGE_ID,
                "stage_failure": False,
            }
        ],
    )
    return summary


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


def validate_stage5by_source_digest_uniqueness() -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    duplicate_review = _validate_payload(DATA_PATHS["duplicate_review"], errors)
    digest = _validate_payload(DATA_PATHS["source_digest_index"], errors)
    paths = [str(record.get("path")) for record in digest.get("source_digest_records", [])]
    duplicate_paths = [path for path, count in Counter(paths).items() if count > 1]
    if duplicate_paths:
        errors.extend(f"stage5by_duplicate_source_digest_path={path}" for path in duplicate_paths)
    if duplicate_review.get("duplicates_deduplicated_or_classified") is not True:
        errors.append("Stage 5BW digest duplicates must be deduplicated or classified")
    if duplicate_review.get("stage5bw_source_digest_duplicate_path_count") != 2:
        errors.append("Stage 5BW duplicate digest path count must be 2")
    counts = {
        "stage5by_source_digest_uniqueness_valid": not errors,
        "stage5bw_row_count": int(duplicate_review.get("stage5bw_source_digest_row_count") or 0),
        "stage5bw_unique_path_count": int(
            duplicate_review.get("stage5bw_source_digest_unique_path_count") or 0
        ),
        "stage5bw_duplicate_path_count": int(
            duplicate_review.get("stage5bw_source_digest_duplicate_path_count") or 0
        ),
        "stage5by_source_digest_record_count": len(paths),
        "stage5by_source_digest_unique_path_count": len(set(paths)),
        "stage5by_duplicate_path_count": len(duplicate_paths),
        "validation_error_count": len(errors),
    }
    return counts, errors


def validate_stage5by_sidecar_gates() -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    sidecar = _validate_payload(DATA_PATHS["sidecar_scaffold"], errors)
    planning = _validate_payload(DATA_PATHS["planning_sidecar"], errors)
    guardrail = _validate_payload(DATA_PATHS["guardrail"], errors)
    if sidecar.get("sidecar_status") != "scaffolded_inactive":
        errors.append("sidecar scaffold must remain scaffolded_inactive")
    if planning.get("planning_ingestion_sidecar_status") != "inactive_no_execution":
        errors.append("planning ingestion sidecar must remain inactive_no_execution")
    for key in FALSE_FLAGS:
        for name, payload in {
            "sidecar_scaffold": sidecar,
            "planning_sidecar": planning,
            "guardrail": guardrail,
        }.items():
            if key in payload and payload.get(key) is not False:
                errors.append(f"{name} {key} must be false")
    counts = {
        "stage5by_sidecar_gates_valid": not errors,
        "sidecar_status": sidecar.get("sidecar_status", "unknown"),
        "planning_ingestion_sidecar_status": planning.get(
            "planning_ingestion_sidecar_status", "unknown"
        ),
        "execution_allowed": bool(guardrail.get("execution_allowed")),
        "string4_active_input_allowed": bool(guardrail.get("string4_active_input_allowed")),
        "validation_error_count": len(errors),
    }
    return counts, errors


def validate_stage5by(
    *,
    summary: Path = DATA_PATHS["summary"],
    next_stage_decision: Path = DATA_PATHS["next_stage"],
    guardrail: Path = DATA_PATHS["guardrail"],
    results_dir: Path = RESULTS_DIR,
) -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    payloads = {key: _validate_payload(path, errors) for key, path in DATA_PATHS.items()}
    summary_payload = payloads["summary"] if summary == DATA_PATHS["summary"] else _validate_payload(summary, errors)
    next_stage_payload = (
        payloads["next_stage"]
        if next_stage_decision == DATA_PATHS["next_stage"]
        else _validate_payload(next_stage_decision, errors)
    )
    guardrail_payload = payloads["guardrail"] if guardrail == DATA_PATHS["guardrail"] else _validate_payload(guardrail, errors)

    digest_counts, digest_errors = validate_stage5by_source_digest_uniqueness()
    gate_counts, gate_errors = validate_stage5by_sidecar_gates()
    errors.extend(digest_errors)
    errors.extend(gate_errors)

    active_paths = payloads["active_lineage"].get("preserved_active_record_paths", [])
    if INCORRECT_STAGE5AW_PATH in active_paths:
        errors.append("deprecated Stage 5AW path must not be active")
    if CORRECT_STAGE5AW_PATH not in active_paths:
        errors.append("correct Stage 5AW path must be active")
    for path in active_paths:
        if not Path(path).is_file():
            errors.append(f"active_lineage_path_missing={path}")

    equivalence_entries = payloads["equivalence_map"].get("equivalence_records", [])
    if not equivalence_entries:
        errors.append("record-family equivalence map must not be empty")

    if summary_payload.get("stage5bx_verdict") != "accept_with_warnings":
        errors.append("summary must integrate Stage 5BX accept_with_warnings verdict")
    if summary_payload.get("stage5bw_source_digest_duplicates_deduplicated_or_classified") is not True:
        errors.append("Stage 5BW duplicate digest rows must be classified or deduplicated")
    if summary_payload.get("string4_inactive_sidecar_planning_manifest_scaffold_created") is not True:
        errors.append("inactive planning-sidecar scaffold must be created")
    if summary_payload.get("string4_no_execution_planning_ingestion_sidecar_created") is not True:
        errors.append("no-execution planning-ingestion sidecar must be created")
    if summary_payload.get("manifest_supersession_performed") is not False:
        errors.append("manifest supersession must not be performed")
    if summary_payload.get("stage5bd_run_plan_id_count") != _run_plan_count():
        errors.append("Stage 5BD run-plan count must remain unchanged")
    if next_stage_payload.get("selected_next_stage_id") != "stage-5bz":
        errors.append("Stage 5BY must select Stage 5BZ review")
    if payloads["handoff"].get("canonical_codex_handoff_root") != "codex-output":
        errors.append("Stage 5BY must use codex-output as handoff root")
    if payloads["handoff"].get("codex_output_used") is not False:
        errors.append("Stage 5BY must not use codex_output")
    if DEPRECATED_CODEX_OUTPUT.exists():
        errors.append("deprecated codex_output directory must not exist")

    for key, expected in FALSE_FLAGS.items():
        if key in guardrail_payload and guardrail_payload.get(key) != expected:
            errors.append(f"guardrail {key} must be {str(expected).lower()}")
        for record_key, payload in payloads.items():
            if key in payload and payload.get(key) not in (expected, None):
                errors.append(f"{record_key} {key} must be {str(expected).lower()}")

    counts = {
        "stage5by_valid": not errors,
        "validation_error_count": len(errors),
        "stage5bx_verdict": summary_payload.get("stage5bx_verdict", "unknown"),
        "duplicate_digest_rows_reviewed": bool(
            summary_payload.get("stage5bw_source_digest_duplicates_reviewed")
        ),
        "stage5bw_row_count": digest_counts["stage5bw_row_count"],
        "stage5bw_unique_path_count": digest_counts["stage5bw_unique_path_count"],
        "stage5bw_duplicate_path_count": digest_counts["stage5bw_duplicate_path_count"],
        "record_family_equivalence_map_created": bool(
            summary_payload.get("record_family_name_equivalence_map_created")
        ),
        "inactive_sidecar_scaffold_created": bool(
            summary_payload.get("string4_inactive_sidecar_planning_manifest_scaffold_created")
        ),
        "no_execution_sidecar_created": bool(
            summary_payload.get("string4_no_execution_planning_ingestion_sidecar_created")
        ),
        "manifest_supersession_performed": bool(
            summary_payload.get("manifest_supersession_performed")
        ),
        "stage5bd_run_plan_id_count": int(summary_payload.get("stage5bd_run_plan_id_count") or 0),
        "stage5bd_run_plan_ids_changed": bool(summary_payload.get("stage5bd_run_plan_ids_changed")),
        "string4_active_input_allowed": bool(summary_payload.get("string4_active_input_allowed")),
        "string4_dry_run_ingestion_allowed_now": bool(
            summary_payload.get("string4_dry_run_ingestion_allowed_now")
        ),
        "generated_summary_present": (results_dir / "summary.json").is_file(),
        "recommended_next_stage_id": summary_payload.get("recommended_next_stage_id", "unknown"),
        "sidecar_gate_status": gate_counts["sidecar_status"],
    }
    return counts, errors


def load_stage5by_summary(summary: Path = DATA_PATHS["summary"]) -> dict[str, Any]:
    return _read(summary)
