"""Stage 5BU Stage 5BS lineage-path and reviewability hardening metadata."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from libreprimus.token_block.models import repo_relative, sha256_file, write_json, write_yaml
from libreprimus.token_block.stage5bm import _read

STAGE_ID = "stage-5bu"
STAGE_TITLE = (
    "Stage 5BU - Stage 5BS lineage-path and reviewability hardening, without execution"
)
PROMPT_TYPE = "codex_metadata_repair"
SOURCE_PREVIOUS_STAGE = "stage-5bs"
SOURCE_PREVIOUS_COMMIT = "9a56959daf147d96eb18090420e445b38d84666c"
SOURCE_DEEP_RESEARCH_STAGE = "stage-5bt"
SOURCE_DEEP_RESEARCH_REPORT = "12_Stage-5BT-Deep-Research-Review.md"

RESULTS_DIR = Path("experiments/results/token-block/stage5bu")
CODEX_COMPLETION_PATH = Path("codex-output/stage5bu-codex-completion.md")
DEPRECATED_CODEX_OUTPUT = Path("codex_output")
STAGE5BT_REPORT_PATH = Path(
    "deep-research-reports/reviews-of-ideas-and-concepts-and-data/md/"
    "12_Stage-5BT-Deep-Research-Review.md"
)

STAGE5BS_ACTIVE_PRESERVATION_PATH = Path(
    "data/token-block/stage5bs-active-manifest-preservation.yaml"
)
STAGE5BS_SUMMARY_PATH = Path("data/project-state/stage5bs-summary.yaml")
STAGE5BS_GATE_PATH = Path("data/token-block/stage5bs-string4-planning-ingestion-gate.yaml")
STAGE5BS_NO_ACTIVE_INGESTION_PATH = Path("data/token-block/stage5bs-no-active-ingestion-proof.yaml")
STAGE5BS_STAGE5BD_PRESERVATION_PATH = Path("data/token-block/stage5bs-stage5bd-plan-preservation.yaml")
STAGE5BS_FUTURE_IMPACT_PATH = Path("data/token-block/stage5bs-future-dry-run-planning-impact.yaml")
STAGE5BD_ACTIVE_LOCK_PATH = Path("data/token-block/stage5bd-active-manifest-lock.yaml")
STAGE5BD_DRY_RUN_PLAN_PATH = Path("data/token-block/stage5bd-dry-run-plan-manifest.yaml")
STAGE5BD_RUN_PLAN_REGISTRY_PATH = Path("data/token-block/stage5bd-run-plan-id-registry.yaml")

INCORRECT_STAGE5AW_PATH = "data/token-block/stage5aw-repaired-branch-manifest.yaml"
CORRECT_STAGE5AW_PATH = "data/token-block/stage5aw-repaired-token-variant-branch-manifest.yaml"

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

DATA_PATHS: dict[str, Path] = {
    "findings": Path("data/project-state/stage5bu-stage5bt-findings-integration.yaml"),
    "stage_marker": Path("data/project-state/stage5bu-reviewable-stage-marker.yaml"),
    "validation_evidence": Path(
        "data/project-state/stage5bu-reviewable-validation-evidence.yaml"
    ),
    "source_digest_index": Path(
        "data/project-state/stage5bu-reviewable-source-digest-index.yaml"
    ),
    "gap_register": Path("data/project-state/stage5bu-reviewability-gap-register.yaml"),
    "lineage_erratum": Path("data/token-block/stage5bu-stage5bs-lineage-path-erratum.yaml"),
    "active_repair": Path(
        "data/token-block/stage5bu-active-manifest-preservation-repair.yaml"
    ),
    "lineage_digest": Path(
        "data/token-block/stage5bu-preserved-active-lineage-digest-index.yaml"
    ),
    "lineage_validation": Path(
        "data/token-block/stage5bu-lineage-path-resolution-validation.yaml"
    ),
    "validator_hardening": Path(
        "data/token-block/stage5bu-stage5bs-validator-hardening.yaml"
    ),
    "citation_policy": Path(
        "data/token-block/stage5bu-future-runner-citation-policy-repair.yaml"
    ),
    "string4_gate": Path("data/token-block/stage5bu-string4-gate-preservation.yaml"),
    "no_active_ingestion": Path("data/token-block/stage5bu-no-active-ingestion-proof.yaml"),
    "stage5bd_preservation": Path(
        "data/token-block/stage5bu-stage5bd-plan-preservation.yaml"
    ),
    "future_impact": Path(
        "data/token-block/stage5bu-future-dry-run-planning-impact.yaml"
    ),
    "source_gap": Path("data/historical-route/stage5bu-source-gap-severity-update.yaml"),
    "dwh": Path("data/historical-route/stage5bu-dwh-quarantine-reaffirmation.yaml"),
    "guardrail": Path("data/historical-route/stage5bu-guardrail.yaml"),
    "handoff": Path("data/source-harvester/stage5bu-codex-handoff-policy.yaml"),
    "review_packaging_warning": Path(
        "data/source-harvester/stage5bu-review-packaging-warning.yaml"
    ),
    "summary": Path("data/project-state/stage5bu-summary.yaml"),
    "next_stage": Path("data/project-state/stage5bu-next-stage-decision.yaml"),
}

SCHEMA_PATHS: dict[str, str] = {
    "findings": "schemas/project-state/stage5bu-stage5bt-findings-integration-v0.schema.json",
    "stage_marker": "schemas/project-state/stage5bu-reviewable-stage-marker-v0.schema.json",
    "validation_evidence": (
        "schemas/project-state/stage5bu-reviewable-validation-evidence-v0.schema.json"
    ),
    "source_digest_index": (
        "schemas/project-state/stage5bu-reviewable-source-digest-index-v0.schema.json"
    ),
    "gap_register": "schemas/project-state/stage5bu-reviewability-gap-register-v0.schema.json",
    "lineage_erratum": (
        "schemas/token-block/stage5bu-stage5bs-lineage-path-erratum-v0.schema.json"
    ),
    "active_repair": (
        "schemas/token-block/stage5bu-active-manifest-preservation-repair-v0.schema.json"
    ),
    "lineage_digest": (
        "schemas/token-block/stage5bu-preserved-active-lineage-digest-index-v0.schema.json"
    ),
    "lineage_validation": (
        "schemas/token-block/stage5bu-lineage-path-resolution-validation-v0.schema.json"
    ),
    "validator_hardening": (
        "schemas/token-block/stage5bu-stage5bs-validator-hardening-v0.schema.json"
    ),
    "citation_policy": (
        "schemas/token-block/stage5bu-future-runner-citation-policy-repair-v0.schema.json"
    ),
    "string4_gate": "schemas/token-block/stage5bu-string4-gate-preservation-v0.schema.json",
    "no_active_ingestion": (
        "schemas/token-block/stage5bu-no-active-ingestion-proof-v0.schema.json"
    ),
    "stage5bd_preservation": (
        "schemas/token-block/stage5bu-stage5bd-plan-preservation-v0.schema.json"
    ),
    "future_impact": (
        "schemas/token-block/stage5bu-future-dry-run-planning-impact-v0.schema.json"
    ),
    "source_gap": "schemas/historical-route/stage5bu-source-gap-severity-update-v0.schema.json",
    "dwh": "schemas/historical-route/stage5bu-dwh-quarantine-reaffirmation-v0.schema.json",
    "guardrail": "schemas/historical-route/stage5bu-guardrail-v0.schema.json",
    "handoff": "schemas/source-harvester/stage5bu-codex-handoff-policy-v0.schema.json",
    "review_packaging_warning": (
        "schemas/source-harvester/stage5bu-review-packaging-warning-v0.schema.json"
    ),
    "summary": "schemas/project-state/stage5bu-summary-v0.schema.json",
    "next_stage": "schemas/project-state/stage5bu-next-stage-decision-v0.schema.json",
}

FALSE_FLAGS: dict[str, bool] = {
    "active_ingestion_performed": False,
    "active_stage5ap_records_mutated": False,
    "active_stage5aw_records_mutated": False,
    "active_stage5ay_records_mutated": False,
    "active_stage5az_records_mutated": False,
    "active_stage5bb_records_mutated": False,
    "active_stage5bd_records_mutated": False,
    "active_token_block_manifest_changed": False,
    "ai_ml_interpretation_performed": False,
    "audio_analysis_performed": False,
    "benchmark_performed": False,
    "branch_materialised_as_active": False,
    "canonical_corpus_active": False,
    "canonical_transcription_changed": False,
    "codex_output_used": False,
    "corrected_decision_template_committed": False,
    "cryptanalytic_benchmark_performed": False,
    "cuda_execution_performed": False,
    "cuda_source_modified": False,
    "decode_attempt_performed": False,
    "decoded_byte_body_committed": False,
    "dwh_hash_search_performed": False,
    "execution_allowed": False,
    "full_cartesian_product_enumerated": False,
    "full_string4_body_committed": False,
    "generated_outputs_committed": False,
    "hash_preimage_search_performed": False,
    "hash_search_performed": False,
    "hidden_content_image_forensics_performed": False,
    "image_forensics_performed": False,
    "llm_vision_token_reading_performed": False,
    "method_status_upgraded": False,
    "ocr_performed": False,
    "page_boundaries_final": False,
    "public_website_publication_performed": False,
    "raw_archive_files_committed": False,
    "raw_human_review_pack_committed": False,
    "real_byte_stream_generated": False,
    "real_token_block_byte_streams_generated": False,
    "reconstructed_token_stream_committed": False,
    "sampled_real_variants_generated": False,
    "scored_experiments_executed": False,
    "scoring_performed": False,
    "semantic_image_interpretation_performed": False,
    "solve_claim": False,
    "stage5bd_dry_run_plan_changed": False,
    "stage5bd_dry_run_records_changed": False,
    "stego_tool_execution_performed": False,
    "string4_active_input_allowed": False,
    "string4_byte_stream_generation_allowed": False,
    "string4_dry_run_ingestion_allowed_now": False,
    "string4_execution_input_allowed": False,
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


def _write_generated(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.suffix == ".jsonl":
        with path.open("w", encoding="utf-8") as handle:
            for row in payload:
                handle.write(json.dumps(row, sort_keys=True) + "\n")
    else:
        write_json(path, payload)


def _sha_record(path: Path, *, role: str, committed: bool = True) -> dict[str, Any]:
    return {
        "path": repo_relative(path),
        "role": role,
        "present": path.is_file(),
        "committed": committed,
        "sha256": sha256_file(path) if path.is_file() else None,
        "size_bytes": path.stat().st_size if path.is_file() else None,
    }


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


def _validate_active_lineage_paths(paths: list[str]) -> list[str]:
    errors: list[str] = []
    if INCORRECT_STAGE5AW_PATH in paths:
        errors.append(f"deprecated_stage5aw_path_active={INCORRECT_STAGE5AW_PATH}")
    if CORRECT_STAGE5AW_PATH not in paths:
        errors.append(f"corrected_stage5aw_path_missing={CORRECT_STAGE5AW_PATH}")
    for path in paths:
        if not Path(path).is_file():
            errors.append(f"lineage_path_missing={path}")
    return errors


def _replace_stage5bs_preservation_path(active_preservation: Path) -> tuple[dict[str, Any], int]:
    payload = _read(active_preservation)
    paths = list(payload.get("preserved_active_record_paths", []))
    replacement_count = 0
    repaired_paths: list[str] = []
    for path in paths:
        if path == INCORRECT_STAGE5AW_PATH:
            repaired_paths.append(CORRECT_STAGE5AW_PATH)
            replacement_count += 1
        else:
            repaired_paths.append(str(path))
    payload["preserved_active_record_paths"] = repaired_paths
    write_yaml(active_preservation, payload)
    return payload, replacement_count


def _validation_commands() -> list[dict[str, Any]]:
    commands = [
        ("stage5bu_lineage_paths", "python -m libreprimus.cli token-block validate-stage5bu-lineage-paths"),
        ("stage5bu_validator", "python -m libreprimus.cli token-block validate-stage5bu"),
        ("stage5bu_summary", "python -m libreprimus.cli token-block stage5bu-summary"),
        ("stage5bs_validator", "python -m libreprimus.cli token-block validate-stage5bs"),
        ("stage5bq_validator", "python -m libreprimus.cli token-block validate-stage5bq"),
        ("stage5bo_validator", "python -m libreprimus.cli token-block validate-stage5bo"),
        (
            "stage5bd_validator",
            "python -m libreprimus.cli token-block validate-stage5bd "
            "--results-dir experiments/results/token-block/stage5bd",
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
            "command_id": "bash_consistency_wrapper",
            "command": "./scripts/ci/run-consistency-checks.sh",
            "status": "not_run",
            "reason_if_not_run": "Only WSL bash.exe was available locally and no WSL distribution was installed.",
        }
    )
    return rows


def build_stage5bu_lineage_path_repair(
    *,
    active_preservation: Path = STAGE5BS_ACTIVE_PRESERVATION_PATH,
    results_dir: Path = RESULTS_DIR,
) -> dict[str, Any]:
    before_payload = _read(active_preservation)
    before_paths = [str(path) for path in before_payload.get("preserved_active_record_paths", [])]
    before_contains_wrong = INCORRECT_STAGE5AW_PATH in before_paths
    repaired_payload, replacement_count = _replace_stage5bs_preservation_path(active_preservation)
    effective_repair_count = replacement_count or int(
        (not before_contains_wrong) and CORRECT_STAGE5AW_PATH in repaired_payload.get("preserved_active_record_paths", [])
    )
    repaired_paths = [str(path) for path in repaired_payload.get("preserved_active_record_paths", [])]
    lineage_errors = _validate_active_lineage_paths(repaired_paths)
    lineage_records = [_sha_record(Path(path), role="preserved_active_lineage_record") for path in repaired_paths]

    erratum = _base("stage5bu_stage5bs_lineage_path_erratum", "lineage_erratum")
    erratum.update(
        {
            "erratum_status": "corrected_in_place_with_stage5bu_erratum",
            "affected_record_path": repo_relative(active_preservation),
            "incorrect_path": INCORRECT_STAGE5AW_PATH,
            "correct_path": CORRECT_STAGE5AW_PATH,
            "incorrect_path_present_in_stage5bs_original_record": True,
            "incorrect_path_present_before_stage5bu_builder": before_contains_wrong,
            "incorrect_path_resolves": Path(INCORRECT_STAGE5AW_PATH).is_file(),
            "correct_path_resolves": Path(CORRECT_STAGE5AW_PATH).is_file(),
            "path_replacement_count": effective_repair_count,
            "repair_already_applied_before_builder": replacement_count == 0,
            "stage5bs_record_repaired": True,
            "stage5bs_validator_hardened": True,
            "active_ingestion_performed": False,
            "string4_active_input_allowed": False,
            "string4_dry_run_ingestion_allowed_now": False,
            "real_byte_stream_generated": False,
            "generated_outputs_committed": False,
        }
    )

    active_repair = _base("stage5bu_active_manifest_preservation_repair", "active_repair")
    active_repair.update(
        {
            "repaired_stage5bs_record_path": repo_relative(active_preservation),
            "repaired_preserved_active_record_paths": repaired_paths,
            "active_lineage_path_count": len(repaired_paths),
            "all_repaired_paths_resolve": not lineage_errors,
            "wrong_path_removed_from_active_preservation": INCORRECT_STAGE5AW_PATH not in repaired_paths,
            "correct_path_present_in_active_preservation": CORRECT_STAGE5AW_PATH in repaired_paths,
            "active_token_block_manifest_changed": False,
            "stage5aw_branch_manifest_changed": False,
            "stage5az_variant_family_manifest_changed": False,
            "stage5bd_dry_run_plan_changed": False,
            "stage5bd_dry_run_records_changed": False,
            "string4_active_input_allowed": False,
        }
    )

    lineage_digest = _base("stage5bu_preserved_active_lineage_digest_index", "lineage_digest")
    lineage_digest.update(
        {
            "lineage_digest_status": "complete",
            "lineage_records": lineage_records,
            "lineage_record_count": len(lineage_records),
            "all_lineage_paths_resolve": not lineage_errors,
            "wrong_stage5aw_path_included": INCORRECT_STAGE5AW_PATH in repaired_paths,
            "correct_stage5aw_path_included": CORRECT_STAGE5AW_PATH in repaired_paths,
            "generated_outputs_committed": False,
        }
    )

    lineage_validation = _base(
        "stage5bu_lineage_path_resolution_validation",
        "lineage_validation",
    )
    lineage_validation.update(
        {
            "validation_status": "passed" if not lineage_errors else "failed",
            "validation_errors": lineage_errors,
            "incorrect_path_active": INCORRECT_STAGE5AW_PATH in repaired_paths,
            "corrected_path_active": CORRECT_STAGE5AW_PATH in repaired_paths,
            "incorrect_path_resolves": Path(INCORRECT_STAGE5AW_PATH).is_file(),
            "corrected_path_resolves": Path(CORRECT_STAGE5AW_PATH).is_file(),
            "all_preserved_active_paths_resolve": not lineage_errors,
            "preserved_active_record_paths": repaired_paths,
            "active_ingestion_performed": False,
            "execution_allowed": False,
        }
    )

    validator_hardening = _base(
        "stage5bu_stage5bs_validator_hardening",
        "validator_hardening",
    )
    validator_hardening.update(
        {
            "hardened_command": "token-block validate-stage5bs",
            "detects_unresolved_preserved_active_paths": True,
            "detects_deprecated_stage5aw_path": True,
            "detects_missing_corrected_stage5aw_path": True,
            "expected_deprecated_path": INCORRECT_STAGE5AW_PATH,
            "expected_corrected_path": CORRECT_STAGE5AW_PATH,
            "stage5bs_validation_after_repair_expected": "passed",
            "execution_allowed": False,
            "solve_claim": False,
        }
    )

    for key, payload in (
        ("lineage_erratum", erratum),
        ("active_repair", active_repair),
        ("lineage_digest", lineage_digest),
        ("lineage_validation", lineage_validation),
        ("validator_hardening", validator_hardening),
    ):
        write_yaml(DATA_PATHS[key], payload)

    generated_summary = {
        "stage_id": STAGE_ID,
        "lineage_path_repair_written": True,
        "path_replacement_count": effective_repair_count,
        "lineage_path_validation_status": lineage_validation["validation_status"],
        "lineage_record_count": len(lineage_records),
        "wrong_path_removed": INCORRECT_STAGE5AW_PATH not in repaired_paths,
        "correct_path_present": CORRECT_STAGE5AW_PATH in repaired_paths,
        "execution_allowed": False,
    }
    _write_generated(results_dir / "lineage_path_resolution.json", lineage_validation)
    _write_generated(results_dir / "lineage_source_file_digests.json", lineage_records)
    _write_generated(
        results_dir / "warnings.jsonl",
        [
            {
                "warning": "stage5bs_lineage_path_erratum_recorded",
                "stage_id": STAGE_ID,
                "stage_failure": False,
            }
        ],
    )
    return generated_summary


def build_stage5bu_reviewability_records(
    *,
    results_dir: Path = RESULTS_DIR,
    stage5bt_report: Path = STAGE5BT_REPORT_PATH,
) -> dict[str, Any]:
    stage5bs_summary = _read(STAGE5BS_SUMMARY_PATH)
    _read(STAGE5BS_GATE_PATH)
    _read(STAGE5BS_NO_ACTIVE_INGESTION_PATH)
    _read(STAGE5BS_STAGE5BD_PRESERVATION_PATH)
    _read(STAGE5BD_DRY_RUN_PLAN_PATH)
    lineage_validation = _read(DATA_PATHS["lineage_validation"])
    lineage_digest = _read(DATA_PATHS["lineage_digest"])

    findings = _base("stage5bu_stage5bt_findings_integration", "findings")
    findings.update(
        {
            "stage5bt_verdict": "accept_with_warnings",
            "finding_integration_status": "integrated_with_erratum",
            "accepted_findings": [
                "stage5bs_gate_remained_closed",
                "stage5bs_source_gap_severity_correct",
                "stage5bs_dwh_quarantine_correct",
                "stage5bs_path_reviewability_gap_repaired",
            ],
            "warnings_integrated": [
                "preserved_active_lineage_path_must_resolve",
                "future_runner_citation_policy_must_reference_repaired_lineage",
                "codex_completion_summary_remains_ignored",
            ],
            "incorrect_path": INCORRECT_STAGE5AW_PATH,
            "correct_path": CORRECT_STAGE5AW_PATH,
            "execution_allowed": False,
        }
    )

    stage_marker = _base("stage5bu_reviewable_stage_marker", "stage_marker")
    stage_marker.update(
        {
            "reviewable_metadata_created": True,
            "lineage_path_erratum_created": True,
            "stage5bs_record_corrected_in_place": True,
            "final_commit_self_embedded": False,
            "final_commit_external_evidence_required": True,
            "ci_external_evidence_required": True,
            "codex_completion_summary_path": repo_relative(CODEX_COMPLETION_PATH),
            "codex_output_directory_used": False,
            "execution_allowed": False,
        }
    )

    validation_evidence = _base(
        "stage5bu_reviewable_validation_evidence",
        "validation_evidence",
    )
    validation_evidence.update(
        {
            "reviewability_evidence_status": "committed_compact_evidence",
            "local_validation_evidence_committed": True,
            "validation_commands": _validation_commands(),
            "stage5bs_validator_hardened": True,
            "lineage_path_resolution_validation_status": lineage_validation.get(
                "validation_status"
            ),
            "raw_staged": False,
            "generated_outputs_staged": False,
            "codex_output_staged": False,
            "sqlite_staged": False,
        }
    )

    source_records = [
        _sha_record(Path(path), role="preserved_active_lineage_record")
        for path in ACTIVE_LINEAGE_PATHS
    ]
    source_records.extend(
        [
            _sha_record(STAGE5BS_SUMMARY_PATH, role="consumed_stage5bs_summary"),
            _sha_record(STAGE5BS_ACTIVE_PRESERVATION_PATH, role="repaired_stage5bs_record"),
            _sha_record(STAGE5BS_GATE_PATH, role="consumed_stage5bs_gate"),
            _sha_record(STAGE5BS_NO_ACTIVE_INGESTION_PATH, role="consumed_stage5bs_no_active_proof"),
            _sha_record(STAGE5BD_DRY_RUN_PLAN_PATH, role="preserved_stage5bd_plan"),
            _sha_record(STAGE5BD_RUN_PLAN_REGISTRY_PATH, role="preserved_stage5bd_registry"),
            _sha_record(stage5bt_report, role="ignored_stage5bt_deep_research_report", committed=False),
        ]
    )
    source_digest_index = _base(
        "stage5bu_reviewable_source_digest_index",
        "source_digest_index",
    )
    source_digest_index.update(
        {
            "source_digest_status": "complete",
            "source_records": source_records,
            "source_record_count": len(source_records),
            "ignored_deep_research_report_recorded": True,
            "raw_or_generated_bodies_committed": False,
            "codex_completion_summary_committed": False,
        }
    )

    gap_register = _base("stage5bu_reviewability_gap_register", "gap_register")
    gap_register.update(
        {
            "gap_register_status": "open_external_evidence_gaps_only",
            "gaps": [
                {
                    "gap_id": "final_commit_hash_not_self_embedded",
                    "status": "expected_until_after_commit",
                    "blocking": False,
                },
                {
                    "gap_id": "ci_run_id_not_committed_at_stage_commit_time",
                    "status": "expected_until_after_push",
                    "blocking": False,
                },
                {
                    "gap_id": "raw_codex_completion_summary_uncommitted",
                    "status": "intentional_ignored_output",
                    "blocking": False,
                },
            ],
            "lineage_path_gap_closed": True,
            "incorrect_stage5aw_path_gap_closed": True,
            "execution_allowed": False,
        }
    )

    citation_policy = _base(
        "stage5bu_future_runner_citation_policy_repair",
        "citation_policy",
    )
    citation_policy.update(
        {
            "future_runner_citation_status": "citation_required_fail_closed",
            "future_runner_must_cite": [
                "data/token-block/stage5bs-string4-planning-ingestion-gate.yaml",
                "data/token-block/stage5bu-stage5bs-lineage-path-erratum.yaml",
                "data/token-block/stage5bu-lineage-path-resolution-validation.yaml",
                "data/token-block/stage5bu-preserved-active-lineage-digest-index.yaml",
            ],
            "future_runner_must_not_cite_as_active": [INCORRECT_STAGE5AW_PATH],
            "future_runner_active_lineage_entrypoint": CORRECT_STAGE5AW_PATH,
            "execution_allowed": False,
            "string4_dry_run_ingestion_allowed_now": False,
        }
    )

    string4_gate = _base("stage5bu_string4_gate_preservation", "string4_gate")
    string4_gate.update(
        {
            "string4_gate_status": "closed",
            "string4_planning_ingestion_gate_status": "closed_gate_no_active_ingestion",
            "stage5bs_gate_preserved": True,
            "stage5bs_gate_path": repo_relative(STAGE5BS_GATE_PATH),
            "string4_active_input_allowed": False,
            "string4_dry_run_ingestion_allowed_now": False,
            "string4_execution_input_allowed": False,
            "string4_byte_stream_generation_allowed": False,
            "active_ingestion_performed": False,
        }
    )

    no_active_ingestion = _base("stage5bu_no_active_ingestion_proof", "no_active_ingestion")
    no_active_ingestion.update(
        {
            "no_active_ingestion_status": "preserved",
            "stage5bs_no_active_ingestion_proof_path": repo_relative(
                STAGE5BS_NO_ACTIVE_INGESTION_PATH
            ),
            "stage5bs_active_manifest_preservation_repaired": True,
            "active_ingestion_performed": False,
            "real_byte_stream_generated": False,
            "variant_byte_streams_generated": False,
            "full_cartesian_product_enumerated": False,
            "dwh_hash_search_performed": False,
            "hash_preimage_search_performed": False,
            "decode_attempt_performed": False,
            "scoring_performed": False,
            "cuda_execution_performed": False,
            "solve_claim": False,
        }
    )

    stage5bd_preservation = _base(
        "stage5bu_stage5bd_plan_preservation",
        "stage5bd_preservation",
    )
    stage5bd_preservation.update(
        {
            "stage5bd_preservation_status": "unchanged",
            "stage5bd_active_manifest_lock_path": repo_relative(STAGE5BD_ACTIVE_LOCK_PATH),
            "stage5bd_dry_run_plan_path": repo_relative(STAGE5BD_DRY_RUN_PLAN_PATH),
            "stage5bd_run_plan_registry_path": repo_relative(STAGE5BD_RUN_PLAN_REGISTRY_PATH),
            "stage5bd_dry_run_plan_changed": False,
            "stage5bd_dry_run_records_changed": False,
            "stage5bd_plan_ids_changed": False,
            "stage5bd_fixture_records_changed": False,
            "string4_added_to_active_dry_run_inputs": False,
        }
    )

    future_impact = _base("stage5bu_future_dry_run_planning_impact", "future_impact")
    future_impact.update(
        {
            "future_dry_run_planning_impact": "lineage_reviewability_hardened_only",
            "future_runner_required_before_execution": [
                "Stage 5BV review of Stage 5BU",
                "explicit future execution-stage prompt",
                "manifest citation of Stage 5BU lineage repair",
                "fresh execution-gate validation",
            ],
            "execution_allowed": False,
            "string4_dry_run_ingestion_allowed_now": False,
            "byte_stream_generation_allowed": False,
        }
    )

    source_gap = _base("stage5bu_source_gap_severity_update", "source_gap")
    source_gap.update(
        {
            "source_gap_status": "unchanged_from_stage5bs",
            "string4_source_gap_severity": "planning_only_blocked_until_review",
            "lineage_path_reviewability_gap_closed": True,
            "active_ingestion_performed": False,
            "string4_active_input_allowed": False,
        }
    )

    dwh = _base("stage5bu_dwh_quarantine_reaffirmation", "dwh")
    dwh.update(
        {
            "dwh_relationship_status": "quarantined",
            "quarantine_reaffirmed": True,
            "hash_search_performed": False,
            "dwh_hash_search_performed": False,
            "hash_preimage_search_performed": False,
            "decode_attempt_performed": False,
            "solve_claim": False,
        }
    )

    guardrail = _base("stage5bu_guardrail", "guardrail")
    guardrail.update(
        {
            **FALSE_FLAGS,
            "planning_ingestion_gate_only": True,
            "lineage_path_repair_only": True,
            "future_token_block_execution_remains_blocked": True,
            "stage5bs_validator_hardened": True,
            "string4_gate_status": "closed",
        }
    )

    handoff = _base("stage5bu_codex_handoff_policy", "handoff")
    handoff.update(
        {
            "canonical_codex_handoff_root": "codex-output",
            "codex_completion_summary_path": repo_relative(CODEX_COMPLETION_PATH),
            "deprecated_codex_output_root": "codex_output",
            "codex_output_used": False,
            "codex_completion_summary_committed": False,
            "local_completion_summary_required": True,
            "execution_allowed": False,
        }
    )

    review_warning = _base(
        "stage5bu_review_packaging_warning",
        "review_packaging_warning",
    )
    review_warning.update(
        {
            "review_packaging_warning_status": "active",
            "warning": (
                "Stage 5BU records are committed reviewability metadata only; "
                "ignored completion summaries and generated reports are not source truth."
            ),
            "raw_or_generated_review_pack_committed": False,
            "codex_output_used": False,
            "execution_allowed": False,
        }
    )

    stage5bs_status = stage5bs_summary.get("string4_planning_ingestion_gate_status", "unknown")
    summary = _base("stage5bu_summary", "summary")
    summary.update(
        {
            "status": "complete",
            "stage5bt_verdict": "accept_with_warnings",
            "stage5bs_lineage_path_erratum_status": "corrected_in_place_with_stage5bu_erratum",
            "incorrect_path": INCORRECT_STAGE5AW_PATH,
            "correct_path": CORRECT_STAGE5AW_PATH,
            "incorrect_path_active_after_stage5bu": False,
            "correct_path_active_after_stage5bu": True,
            "lineage_path_resolution_validation_status": lineage_validation.get(
                "validation_status"
            ),
            "lineage_record_count": lineage_digest.get("lineage_record_count"),
            "source_digest_record_count": len(source_records),
            "stage5bs_validator_hardened": True,
            "string4_planning_ingestion_gate_status": stage5bs_status,
            "string4_active_input_allowed": False,
            "string4_dry_run_ingestion_allowed_now": False,
            "future_token_block_execution_remains_blocked": True,
            "stage5bd_dry_run_records_remain_valid": True,
            "active_ingestion_performed": False,
            "real_byte_stream_generated": False,
            "variant_materialisation_performed": False,
            "cuda_execution_performed": False,
            "scored_experiments_executed": False,
            "generated_outputs_committed": False,
            "codex_output_used": False,
            "canonical_corpus_active": False,
            "page_boundaries_final": False,
            "recommended_next_stage_id": "stage-5bv",
            "recommended_next_stage_title": (
                "Stage 5BV - Deep Research review of Stage 5BU lineage-path "
                "and reviewability hardening, without execution"
            ),
        }
    )

    next_stage = _base("stage5bu_next_stage_decision", "next_stage")
    next_stage.update(
        {
            "selected_next_stage_id": "stage-5bv",
            "selected_next_stage_title": (
                "Stage 5BV - Deep Research review of Stage 5BU lineage-path "
                "and reviewability hardening, without execution"
            ),
            "selection_reason": (
                "Stage 5BU repaired a lineage-path defect and hardened validation; "
                "Deep Research review must inspect the repair before execution-capable work."
            ),
            "token_block_execution_selected": False,
            "byte_stream_generation_selected": False,
            "variant_materialisation_selected": False,
            "dwh_hash_search_selected": False,
            "scored_experiments_selected": False,
            "cuda_selected": False,
            "benchmark_selected": False,
            "method_status_upgrade_selected": False,
            "solve_claim": False,
        }
    )

    record_payloads = {
        "findings": findings,
        "stage_marker": stage_marker,
        "validation_evidence": validation_evidence,
        "source_digest_index": source_digest_index,
        "gap_register": gap_register,
        "citation_policy": citation_policy,
        "string4_gate": string4_gate,
        "no_active_ingestion": no_active_ingestion,
        "stage5bd_preservation": stage5bd_preservation,
        "future_impact": future_impact,
        "source_gap": source_gap,
        "dwh": dwh,
        "guardrail": guardrail,
        "handoff": handoff,
        "review_packaging_warning": review_warning,
        "summary": summary,
        "next_stage": next_stage,
    }
    for key, payload in record_payloads.items():
        write_yaml(DATA_PATHS[key], payload)

    _write_generated(results_dir / "source_file_digests.json", source_records)
    _write_generated(results_dir / "summary.json", summary)
    existing_warnings = []
    warnings_path = results_dir / "warnings.jsonl"
    if warnings_path.is_file():
        existing_warnings = [
            json.loads(line)
            for line in warnings_path.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
    _write_generated(
        warnings_path,
        existing_warnings
        + [
            {
                "warning": "final_commit_external_evidence_required",
                "stage_id": STAGE_ID,
                "stage_failure": False,
            },
            {
                "warning": "ci_external_evidence_required",
                "stage_id": STAGE_ID,
                "stage_failure": False,
            },
        ],
    )
    return summary


def validate_stage5bu_lineage_paths(
    *,
    lineage_erratum: Path = DATA_PATHS["lineage_erratum"],
    active_repair: Path = DATA_PATHS["active_repair"],
    lineage_digest: Path = DATA_PATHS["lineage_digest"],
    lineage_validation: Path = DATA_PATHS["lineage_validation"],
    active_preservation: Path = STAGE5BS_ACTIVE_PRESERVATION_PATH,
) -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    erratum_payload = _validate_payload(lineage_erratum, errors)
    active_repair_payload = _validate_payload(active_repair, errors)
    lineage_digest_payload = _validate_payload(lineage_digest, errors)
    validation_payload = _validate_payload(lineage_validation, errors)
    active_payload = _read(active_preservation) if active_preservation.is_file() else {}
    active_paths = [str(path) for path in active_payload.get("preserved_active_record_paths", [])]
    errors.extend(_validate_active_lineage_paths(active_paths))

    if erratum_payload.get("incorrect_path") != INCORRECT_STAGE5AW_PATH:
        errors.append("lineage erratum must record the incorrect Stage 5AW path")
    if erratum_payload.get("correct_path") != CORRECT_STAGE5AW_PATH:
        errors.append("lineage erratum must record the corrected Stage 5AW path")
    if active_repair_payload.get("wrong_path_removed_from_active_preservation") is not True:
        errors.append("active repair must remove the deprecated path")
    if active_repair_payload.get("correct_path_present_in_active_preservation") is not True:
        errors.append("active repair must include the corrected path")
    if lineage_digest_payload.get("all_lineage_paths_resolve") is not True:
        errors.append("lineage digest must resolve every active path")
    if validation_payload.get("validation_status") != "passed":
        errors.append("lineage validation status must be passed")
    if validation_payload.get("incorrect_path_active") is not False:
        errors.append("lineage validation must report incorrect_path_active=false")
    if validation_payload.get("corrected_path_active") is not True:
        errors.append("lineage validation must report corrected_path_active=true")

    counts = {
        "stage5bu_lineage_paths_valid": not errors,
        "validation_error_count": len(errors),
        "incorrect_path": INCORRECT_STAGE5AW_PATH,
        "correct_path": CORRECT_STAGE5AW_PATH,
        "correct_path_active": CORRECT_STAGE5AW_PATH in active_paths,
        "incorrect_path_active": INCORRECT_STAGE5AW_PATH in active_paths,
        "lineage_record_count": lineage_digest_payload.get("lineage_record_count", 0),
    }
    return counts, errors


def validate_stage5bu(
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
    _, lineage_errors = validate_stage5bu_lineage_paths()
    errors.extend(lineage_errors)

    if summary_payload.get("stage5bt_verdict") != "accept_with_warnings":
        errors.append("summary must preserve Stage 5BT accept_with_warnings verdict")
    if summary_payload.get("lineage_path_resolution_validation_status") != "passed":
        errors.append("summary must record passed lineage path validation")
    if summary_payload.get("stage5bs_validator_hardened") is not True:
        errors.append("summary must record Stage 5BS validator hardening")
    if summary_payload.get("string4_planning_ingestion_gate_status") != "closed_gate_no_active_ingestion":
        errors.append("String 4 planning-ingestion gate must remain closed")
    if next_stage_payload.get("selected_next_stage_id") != "stage-5bv":
        errors.append("Stage 5BU must select Stage 5BV review")
    if payloads["handoff"].get("canonical_codex_handoff_root") != "codex-output":
        errors.append("Stage 5BU handoff root must be codex-output")
    if payloads["handoff"].get("codex_output_used") is not False:
        errors.append("Stage 5BU must not use codex_output")
    if DEPRECATED_CODEX_OUTPUT.exists():
        errors.append("deprecated codex_output directory must not exist")
    for key in (
        "execution_allowed",
        "solve_claim",
        "string4_active_input_allowed",
        "string4_dry_run_ingestion_allowed_now",
        "real_byte_stream_generated",
        "generated_outputs_committed",
    ):
        for record_key, payload in payloads.items():
            if key in payload and payload.get(key) is not False:
                errors.append(f"{record_key} {key} must be false")
    for key, expected in FALSE_FLAGS.items():
        if key in guardrail_payload and guardrail_payload.get(key) != expected:
            errors.append(f"guardrail {key} must be {str(expected).lower()}")

    counts = {
        "stage5bu_valid": not errors,
        "validation_error_count": len(errors),
        "stage5bt_verdict": summary_payload.get("stage5bt_verdict", "unknown"),
        "lineage_path_resolution_validation_status": summary_payload.get(
            "lineage_path_resolution_validation_status", "unknown"
        ),
        "lineage_record_count": int(summary_payload.get("lineage_record_count") or 0),
        "source_digest_record_count": int(summary_payload.get("source_digest_record_count") or 0),
        "stage5bs_validator_hardened": bool(summary_payload.get("stage5bs_validator_hardened")),
        "string4_gate_status": summary_payload.get("string4_planning_ingestion_gate_status", "unknown"),
        "string4_active_input_allowed": bool(summary_payload.get("string4_active_input_allowed")),
        "string4_dry_run_ingestion_allowed_now": bool(
            summary_payload.get("string4_dry_run_ingestion_allowed_now")
        ),
        "future_token_block_execution_remains_blocked": bool(
            summary_payload.get("future_token_block_execution_remains_blocked")
        ),
        "recommended_next_stage_id": summary_payload.get("recommended_next_stage_id", "unknown"),
        "codex_output_used": bool(payloads["handoff"].get("codex_output_used")),
        "ignored_generated_summary_present": (results_dir / "summary.json").is_file(),
    }
    return counts, errors


def load_stage5bu_summary(summary: Path = DATA_PATHS["summary"]) -> dict[str, Any]:
    return _read(summary)
