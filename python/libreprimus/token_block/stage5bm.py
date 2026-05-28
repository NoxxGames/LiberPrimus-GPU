"""Stage 5BM String 4 branch-crosswalk repair metadata."""

from __future__ import annotations

import hashlib
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any

from libreprimus.token_block.models import (
    MAPPING_PATH,
    PRIMARY_ALPHABET,
    STAGE5AW_REPAIRED_BRANCH_MANIFEST_PATH,
    STAGE5AW_REPAIRED_PRIMARY60_IMPACT_PATH,
    STAGE5AW_REPAIRED_REVIEWER_EXTRA_TOKENS_PATH,
    STAGE5AW_REPAIRED_UNRESOLVED_VARIANTS_PATH,
    STAGE5AY_BRANCH_ELIGIBILITY_POLICY_PATH,
    STAGE5BD_SUMMARY_PATH,
    TRANSCRIPTION_PATH,
    read_yaml,
    repo_relative,
    sha256_file,
    token_rows,
    write_json,
    write_yaml,
)

STAGE_ID = "stage-5bm"
STAGE_TITLE = "Stage 5BM - Deep Research findings integration and String 4 branch-crosswalk repair, without execution"
SOURCE_PREVIOUS_STAGE = "stage-5bk"
SOURCE_PREVIOUS_COMMIT = "607c30c83491d74f8f6f6ee46519b0a01ecccf8c"
SOURCE_DEEP_RESEARCH_STAGE = "stage-5bl"
SOURCE_DEEP_RESEARCH_REPORT = "09_LiberPrimus-GPU-Stage-5BL-Deep-Research-Review.md"
LOCAL_IDDQD_V2_SOURCE_ROOT = Path("third_party/CiadaSolversIddqd_v2")
BYTE_STRINGS_SOURCE_PATH = LOCAL_IDDQD_V2_SOURCE_ROOT / "byte-strings/byte-strings"
RESULTS_DIR = Path("experiments/results/token-block/stage5bm")
HISTORICAL_RESULTS_DIR = Path("experiments/results/historical-route/stage5bm")
CODEX_COMPLETION_PATH = Path("codex-output/stage5bm-codex-completion.md")
DEPRECATED_CODEX_OUTPUT = Path("codex_output")

STAGE5BK_BYTE_STRINGS_PATH = Path("data/historical-route/stage5bk-iddqd-v2-byte-strings-source-lock.yaml")
STAGE5BK_STRING4_CROSSWALK_PATH = Path("data/token-block/stage5bk-page49-51-string4-crosswalk.yaml")
STAGE5BK_GAP_REGISTER_PATH = Path("data/historical-route/stage5bk-source-gap-severity-register.yaml")
STAGE5BK_FAMILY_STATUS_PATH = Path("data/historical-route/stage5bk-historical-family-planning-status.yaml")
STAGE5BK_DWH_PATH = Path("data/historical-route/stage5bk-dwh-quarantine-reaffirmation.yaml")
STAGE5BF_DWH_PATH = Path("data/historical-route/stage5bf-dwh-historical-context.yaml")
STAGE5BK_ERRATA_PATH = Path("data/historical-route/stage5bk-stage5bj-crosswalk-review-and-errata.yaml")

DATA_PATHS: dict[str, Path] = {
    "findings": Path("data/project-state/stage5bm-stage5bl-findings-integration.yaml"),
    "review_warning": Path("data/source-harvester/stage5bm-review-packaging-warning.yaml"),
    "source_restatement": Path("data/token-block/stage5bm-string4-source-restatement.yaml"),
    "inverse_policy": Path("data/token-block/stage5bm-string4-primary60-inverse-policy.yaml"),
    "mismatch_analysis": Path("data/token-block/stage5bm-string4-stage5ap-mismatch-analysis.yaml"),
    "branch_membership": Path("data/token-block/stage5bm-string4-stage5aw-branch-membership.yaml"),
    "ambiguity_coverage": Path("data/token-block/stage5bm-string4-ambiguity-class-coverage.yaml"),
    "planning_constraint": Path("data/token-block/stage5bm-string4-planning-constraint.yaml"),
    "lineage": Path("data/token-block/stage5bm-token-block-lineage-preservation.yaml"),
    "dry_run_impact": Path("data/token-block/stage5bm-future-dry-run-planning-impact.yaml"),
    "gap_update": Path("data/historical-route/stage5bm-source-gap-severity-update.yaml"),
    "family_update": Path("data/historical-route/stage5bm-historical-family-granularity-update.yaml"),
    "dwh": Path("data/historical-route/stage5bm-dwh-quarantine-reaffirmation.yaml"),
    "errata": Path("data/historical-route/stage5bm-stage5bj-errata-supersession.yaml"),
    "guardrail": Path("data/historical-route/stage5bm-guardrail.yaml"),
    "handoff": Path("data/source-harvester/stage5bm-codex-handoff-policy.yaml"),
    "summary": Path("data/project-state/stage5bm-summary.yaml"),
    "next_stage": Path("data/project-state/stage5bm-next-stage-decision.yaml"),
}

SCHEMA_PATHS: dict[str, str] = {
    "findings": "schemas/project-state/stage5bm-stage5bl-findings-integration-v0.schema.json",
    "review_warning": "schemas/source-harvester/stage5bm-review-packaging-warning-v0.schema.json",
    "source_restatement": "schemas/token-block/stage5bm-string4-source-restatement-v0.schema.json",
    "inverse_policy": "schemas/token-block/stage5bm-string4-primary60-inverse-policy-v0.schema.json",
    "mismatch_analysis": "schemas/token-block/stage5bm-string4-stage5ap-mismatch-analysis-v0.schema.json",
    "branch_membership": "schemas/token-block/stage5bm-string4-stage5aw-branch-membership-v0.schema.json",
    "ambiguity_coverage": "schemas/token-block/stage5bm-string4-ambiguity-class-coverage-v0.schema.json",
    "planning_constraint": "schemas/token-block/stage5bm-string4-planning-constraint-v0.schema.json",
    "lineage": "schemas/token-block/stage5bm-token-block-lineage-preservation-v0.schema.json",
    "dry_run_impact": "schemas/token-block/stage5bm-future-dry-run-planning-impact-v0.schema.json",
    "gap_update": "schemas/historical-route/stage5bm-source-gap-severity-update-v0.schema.json",
    "family_update": "schemas/historical-route/stage5bm-historical-family-granularity-update-v0.schema.json",
    "dwh": "schemas/historical-route/stage5bm-dwh-quarantine-reaffirmation-v0.schema.json",
    "errata": "schemas/historical-route/stage5bm-stage5bj-errata-supersession-v0.schema.json",
    "guardrail": "schemas/historical-route/stage5bm-guardrail-v0.schema.json",
    "handoff": "schemas/source-harvester/stage5bm-codex-handoff-policy-v0.schema.json",
    "summary": "schemas/project-state/stage5bm-summary-v0.schema.json",
    "next_stage": "schemas/project-state/stage5bm-next-stage-decision-v0.schema.json",
}

FALSE_FLAGS = {
    "active_token_block_manifest_changed": False,
    "ai_ml_interpretation_performed": False,
    "audio_analysis_performed": False,
    "benchmark_performed": False,
    "canonical_corpus_active": False,
    "canonical_transcription_changed": False,
    "codex_output_committed": False,
    "codex_output_directory_created": False,
    "codex_output_used": False,
    "cuda_execution_performed": False,
    "cuda_source_modified": False,
    "decode_attempt_performed": False,
    "decoded_byte_body_committed": False,
    "decoded_byte_bodies_committed": False,
    "decoded_bytes_committed": False,
    "dwh_hash_search_performed": False,
    "execution_allowed": False,
    "fandom_images_committed": False,
    "fandom_page_bodies_committed": False,
    "full_cartesian_product_enumerated": False,
    "full_hex_body_committed": False,
    "full_mismatch_table_committed": False,
    "full_position_table_committed": False,
    "generated_outputs_committed": False,
    "hash_preimage_search_performed": False,
    "hash_search_performed": False,
    "image_forensics_performed": False,
    "llm_vision_token_reading_performed": False,
    "method_status_upgraded": False,
    "ocr_performed": False,
    "page_boundaries_final": False,
    "public_website_publication_performed": False,
    "real_byte_stream_generated": False,
    "real_token_block_byte_streams_generated": False,
    "reconstructed_token_stream_committed": False,
    "scored_experiments_executed": False,
    "scoring_performed": False,
    "solve_claim": False,
    "source_string_body_committed": False,
    "stage5aw_branch_manifest_changed": False,
    "stage5az_variant_family_manifest_changed": False,
    "stego_tool_execution_performed": False,
    "string4_branch_materialised_as_active": False,
    "token_experiment_executed": False,
    "token_experiments_executed": False,
    "variant_byte_streams_generated": False,
    "variant_materialisation_performed": False,
    "website_expansion_performed": False,
}

FALSE_NEXT_STAGE_FLAGS = {
    "token_block_execution_selected": False,
    "byte_stream_generation_selected": False,
    "variant_materialisation_selected": False,
    "dwh_hash_search_selected": False,
    "hash_preimage_search_selected": False,
    "decode_selected": False,
    "scored_experiments_selected": False,
    "benchmark_selected": False,
    "cuda_selected": False,
    "public_website_expansion_selected": False,
    "stego_execution_selected": False,
    "pgp_verification_selected": False,
    "audio_analysis_selected": False,
    "image_forensics_selected": False,
    "ocr_selected": False,
    "ai_ml_selected": False,
    "canonical_corpus_activation_selected": False,
    "page_boundary_finalisation_selected": False,
    "method_status_upgrade_selected": False,
    "solve_claim": False,
}


def _read(path: Path) -> dict[str, Any]:
    return read_yaml(path)


def _write_generated(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.suffix == ".jsonl":
        with path.open("w", encoding="utf-8") as handle:
            for row in payload:
                handle.write(json.dumps(row, sort_keys=True) + "\n")
    else:
        write_json(path, payload)


def _base(record_type: str, schema_key: str) -> dict[str, Any]:
    return {
        "record_type": record_type,
        "schema": SCHEMA_PATHS[schema_key],
        "stage_id": STAGE_ID,
        "stage_title": STAGE_TITLE,
        "source_deep_research_stage": SOURCE_DEEP_RESEARCH_STAGE,
        "source_previous_stage": SOURCE_PREVIOUS_STAGE,
        "source_previous_stage_commit": SOURCE_PREVIOUS_COMMIT,
        "metadata_only": True,
        "solve_claim": False,
    }


def _sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def _extract_string4(source_path: Path) -> dict[str, Any]:
    result: dict[str, Any] = {
        "source_file_found": source_path.is_file(),
        "source_file_sha256": sha256_file(source_path) if source_path.is_file() else None,
        "string4_reparsed_from_local_source": False,
        "hex_length": None,
        "decoded_byte_count": None,
        "normalized_hex_sha256": None,
        "raw_hex_sha256": None,
        "decoded_byte_sha256": None,
        "bytes": None,
    }
    if not source_path.is_file():
        return result
    text = source_path.read_text(encoding="utf-8", errors="replace")
    matches = re.findall(r"(?i)\b[0-9a-f]{512}\b", text)
    if len(matches) < 4:
        result["parse_error"] = "fewer_than_four_exact_512_hex_strings"
        return result
    raw_hex = matches[3]
    normalized_hex = raw_hex.lower()
    decoded = bytes.fromhex(normalized_hex)
    result.update(
        {
            "string4_reparsed_from_local_source": True,
            "hex_length": len(normalized_hex),
            "decoded_byte_count": len(decoded),
            "normalized_hex_sha256": _sha256_text(normalized_hex),
            "raw_hex_sha256": _sha256_text(raw_hex),
            "decoded_byte_sha256": _sha256_bytes(decoded),
            "bytes": decoded,
        }
    )
    return result


def _stage5bk_string4_record(byte_strings: dict[str, Any]) -> dict[str, Any]:
    for record in byte_strings.get("records", []):
        if record.get("string_number") == 4:
            return record
    return {}


def _canonical_tokens() -> list[str]:
    rows = token_rows()
    return [token for row in rows for token in row]


def _stage5ap_byte_hashes(mapping: dict[str, Any]) -> dict[str, str | int]:
    values = [int(row["mapped_value"]) for row in mapping.get("value_records", [])]
    payload = bytes(values)
    return {
        "stage5ap_token_count": len(values),
        "stage5ap_primary60_hex_sha256": _sha256_text(payload.hex()),
        "stage5ap_primary60_decoded_byte_sha256": _sha256_bytes(payload),
    }


def _string4_tokens(decoded: bytes) -> list[str]:
    return [f"{value // 60}{PRIMARY_ALPHABET[value % 60]}" for value in decoded]


def _allowed_universe(canonical: list[str]) -> tuple[dict[int, set[str]], dict[int, dict[str, dict[str, Any]]]]:
    allowed: dict[int, set[str]] = {index: {token} for index, token in enumerate(canonical)}
    details: dict[int, dict[str, dict[str, Any]]] = {
        index: {
            token: {
                "source_stage5aw_option_kind": "canonical",
                "primary60_mappable": True,
                "option_classes": ["canonical_current_token"],
            }
        }
        for index, token in enumerate(canonical)
    }

    unresolved = _read(STAGE5AW_REPAIRED_UNRESOLVED_VARIANTS_PATH)
    for record in unresolved.get("records", []):
        index = int(record["token_index_0_based"])
        for detail in record.get("possible_token_details", []):
            token = str(detail["token"])
            allowed[index].add(token)
            details[index][token] = {
                "source_stage5aw_option_kind": detail.get("possible_token_source", "possible_token_detail"),
                "primary60_mappable": bool(detail.get("primary60_mappable")),
                "option_classes": [detail.get("possible_token_source", "possible_token_detail")],
            }
        for token_value in record.get("possible_tokens", []):
            token = str(token_value)
            allowed[index].add(token)
            details[index].setdefault(
                token,
                {
                    "source_stage5aw_option_kind": "possible_tokens",
                    "primary60_mappable": None,
                    "option_classes": ["possible_token"],
                },
            )

    extras = _read(STAGE5AW_REPAIRED_REVIEWER_EXTRA_TOKENS_PATH)
    for record in extras.get("records", []):
        index = int(record["token_index_0_based"])
        token = str(record["reviewer_extra_possible_token"])
        allowed[index].add(token)
        details[index][token] = {
            "source_stage5aw_option_kind": "reviewer_extra",
            "primary60_mappable": bool(record.get("primary60_mappable")),
            "option_classes": ["reviewer_extra_possible_token"],
        }

    eligibility = _read(STAGE5AY_BRANCH_ELIGIBILITY_POLICY_PATH)
    for record in eligibility.get("option_records", []):
        index = int(record["token_index_0_based"])
        token = str(record["token"])
        allowed[index].add(token)
        details[index][token] = {
            "source_stage5aw_option_kind": "branch_eligibility",
            "primary60_mappable": bool(record.get("primary60_mappable")),
            "option_classes": list(record.get("option_classes", [])),
        }
    return allowed, details


def _ambiguity_class(canonical: str, inferred: str, detail: dict[str, Any] | None, unsupported: bool) -> str:
    if canonical == inferred:
        return "canonical_exact"
    if unsupported:
        return "unsupported_external"
    classes = detail.get("option_classes", []) if detail else []
    source = str((detail or {}).get("source_stage5aw_option_kind", ""))
    if "reviewer_extra_possible_token" in classes or source == "reviewer_extra":
        return "reviewer_extra"
    if "?" in inferred or any("visual_placeholder" in str(value) for value in classes):
        return "visual_placeholder"
    if canonical[0] != inferred[0]:
        return "prefix_digit_change" if canonical[0].isdigit() or inferred[0].isdigit() else "digit_letter_confusion"
    suffixes = {canonical[1], inferred[1]}
    if suffixes <= {"I", "l"}:
        return "I_l"
    if suffixes <= {"O", "0", "o"}:
        return "O_0"
    if canonical[1].lower() == inferred[1].lower() and canonical[1] != inferred[1]:
        return "case_only"
    if canonical[1] != inferred[1]:
        return "primary60_suffix_choice"
    return "other"


def _reconcile_positions(canonical: list[str], inferred: list[str]) -> dict[str, Any]:
    allowed, details = _allowed_universe(canonical)
    rows = []
    counts: Counter[str] = Counter()
    ambiguity_counts: Counter[str] = Counter()
    for index, (canonical_token, inferred_token) in enumerate(zip(canonical, inferred)):
        detail = details[index].get(inferred_token)
        if inferred_token == canonical_token:
            status = "canonical_match"
        elif inferred_token in allowed[index]:
            if detail and detail.get("primary60_mappable") is False:
                status = "option_supported_but_primary60_unmappable_context_only"
            else:
                status = "noncanonical_option_supported_by_stage5aw"
        else:
            status = "unsupported_by_stage5aw"
        ambiguity = _ambiguity_class(canonical_token, inferred_token, detail, status == "unsupported_by_stage5aw")
        counts[status] += 1
        ambiguity_counts[ambiguity] += 1
        rows.append(
            {
                "token_index_0_based": index,
                "row_index_one_based": index // 8 + 1,
                "column_index_one_based": index % 8 + 1,
                "stage5ap_canonical_token": canonical_token,
                "string4_inferred_token": inferred_token,
                "position_membership_status": status,
                "ambiguity_class": ambiguity,
                "stage5aw_allowed_token_count": len(allowed[index]),
                "stage5aw_allowed_tokens": sorted(allowed[index]),
                "source_stage5aw_option_kind": (detail or {}).get("source_stage5aw_option_kind"),
                "primary60_mappable": (detail or {}).get("primary60_mappable"),
                "option_classes": (detail or {}).get("option_classes", []),
            }
        )
    mismatches = [row for row in rows if row["position_membership_status"] != "canonical_match"]
    supported = [
        row
        for row in mismatches
        if row["position_membership_status"]
        in {"noncanonical_option_supported_by_stage5aw", "option_supported_but_primary60_unmappable_context_only"}
    ]
    unsupported = [row for row in mismatches if row["position_membership_status"] == "unsupported_by_stage5aw"]
    if unsupported and supported:
        branch_status = "partial_branch_match"
    elif unsupported:
        branch_status = "external_mismatch_unrepresented"
    else:
        branch_status = "full_branch_match"
    return {
        "rows": rows,
        "mismatches": mismatches,
        "supported": supported,
        "unsupported": unsupported,
        "counts": counts,
        "ambiguity_counts": ambiguity_counts,
        "branch_status": branch_status,
    }


def _summarize_allowed_tokens(tokens: list[str]) -> str:
    if len(tokens) <= 8:
        return ", ".join(tokens)
    return ", ".join(tokens[:8]) + f", ... ({len(tokens)} total)"


def _compact_mismatch(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "token_index_0_based": row["token_index_0_based"],
        "row_index_one_based": row["row_index_one_based"],
        "column_index_one_based": row["column_index_one_based"],
        "stage5ap_canonical_token": row["stage5ap_canonical_token"],
        "string4_inferred_token": row["string4_inferred_token"],
        "mismatch_class_guess": row["ambiguity_class"],
        "stage5aw_membership_status": row["position_membership_status"],
    }


def _guardrail() -> dict[str, Any]:
    record = _base("stage5bm_guardrail", "guardrail")
    record.update(FALSE_FLAGS)
    record.update(
        {
            "string4_branch_crosswalk_metadata_only": True,
            "stage5bd_dry_run_records_remain_valid": True,
            "future_token_block_execution_remains_blocked": True,
            "raw_archive_files_committed": False,
            "raw_iddqd_v2_files_committed": False,
            "spreadsheet_committed": False,
            "full_surface_bodies_committed": False,
            "real_variant_branches_materialised": False,
            "sampled_real_variants_generated": False,
            "string4_combined_with_2014_surfaces": False,
            "fandom_surface_combination_performed": False,
            "iddqd_surface_combination_performed": False,
            "xor_attempt_performed": False,
            "transposition_attempt_performed": False,
            "hash_comparison_performed_as_experiment": False,
            "outguess_execution_performed": False,
            "openpuff_execution_performed": False,
            "mp3stego_execution_performed": False,
            "pgp_network_key_fetch_performed": False,
            "pgp_verification_performed_as_project_truth": False,
            "semantic_image_interpretation_performed": False,
            "hidden_content_image_forensics_performed": False,
            "new_cuda_kernels_added": 0,
            "cryptanalytic_benchmark_performed": False,
        }
    )
    return record


def build_stage5bm_string4_reconciliation(
    results_dir: Path = RESULTS_DIR,
    historical_results_dir: Path = HISTORICAL_RESULTS_DIR,
) -> dict[str, Any]:
    results_dir.mkdir(parents=True, exist_ok=True)
    historical_results_dir.mkdir(parents=True, exist_ok=True)
    (results_dir / ".gitkeep").touch(exist_ok=True)
    (historical_results_dir / ".gitkeep").touch(exist_ok=True)

    byte_strings = _read(STAGE5BK_BYTE_STRINGS_PATH)
    string4_record = _stage5bk_string4_record(byte_strings)
    mapping = _read(MAPPING_PATH)
    canonical = _canonical_tokens()
    local = _extract_string4(BYTE_STRINGS_SOURCE_PATH)
    stage5ap_hashes = _stage5ap_byte_hashes(mapping)

    if local["bytes"] is not None:
        inferred_tokens = _string4_tokens(local["bytes"])
        reconciliation = _reconcile_positions(canonical, inferred_tokens)
    else:
        inferred_tokens = []
        reconciliation = {
            "rows": [],
            "mismatches": [],
            "supported": [],
            "unsupported": [],
            "counts": Counter({"not_checked": 256}),
            "ambiguity_counts": Counter(),
            "branch_status": "not_attempted_due_missing_source",
        }

    branch_status = reconciliation["branch_status"]
    counts: Counter[str] = reconciliation["counts"]
    mismatches: list[dict[str, Any]] = reconciliation["mismatches"]
    supported: list[dict[str, Any]] = reconciliation["supported"]
    unsupported: list[dict[str, Any]] = reconciliation["unsupported"]

    if branch_status == "full_branch_match":
        planning_effect = "valid_existing_branch_context_only"
        source_gap_status = "closed"
        source_gap_closure = "closed_full_branch_match"
        next_prompt_type = "deep_research_review"
        next_title = "Stage 5BN - Deep Research review of String 4 branch-crosswalk reconciliation and historical-route constraint repair, without execution"
        next_reason = "String 4 was reconciled into the existing branch universe; independent review is still required before any dry-run context ingestion."
    elif branch_status == "partial_branch_match":
        planning_effect = "source_gap"
        source_gap_status = "partial"
        source_gap_closure = "partially_closed_branch_match"
        next_prompt_type = "codex_metadata_implementation"
        next_title = "Stage 5BN - String 4 unsupported-position source-gap closure and human-review pack preparation, without execution"
        next_reason = "String 4 has Stage 5AW-supported I/l differences plus one unsupported position, so future work should close that source gap before ingestion."
    elif branch_status == "external_mismatch_unrepresented":
        planning_effect = "source_gap"
        source_gap_status = "open"
        source_gap_closure = "external_mismatch_unrepresented"
        next_prompt_type = "codex_metadata_implementation"
        next_title = "Stage 5BN - String 4 unsupported-position source-gap closure and human-review pack preparation, without execution"
        next_reason = "String 4 is materially outside the current Stage 5AW branch universe and must remain external context."
    else:
        planning_effect = "source_gap"
        source_gap_status = "inconclusive"
        source_gap_closure = "parser_inconclusive"
        next_prompt_type = "codex_metadata_implementation"
        next_title = "Stage 5BN - String 4 parser/source-lock repair, without execution"
        next_reason = "String 4 source parsing was insufficient for reliable branch-membership classification."

    findings = _base("stage5bm_stage5bl_findings_integration", "findings")
    findings.update(
        {
            "source_deep_research_report": SOURCE_DEEP_RESEARCH_REPORT,
            "stage5bl_verdict": "accept_with_warnings",
            "stage5bl_primary_warning": "string4_stage5aw_branch_membership_unreconciled",
            "stage5bl_findings_integrated": [
                "stage5bk_safe_metadata_only",
                "string1_to_3_crosswalk_green",
                "string4_mismatch_yellow",
                "planning_constraints_yellow",
                "family_granularity_yellow",
                "source_gap_severity_missing_string4_row",
                "dwh_quarantine_green",
                "guardrails_green",
            ],
            "stage5bl_recommended_next_stage": STAGE_ID,
            "execution_selected": False,
        }
    )

    review_warning = _base("stage5bm_review_packaging_warning", "review_warning")
    review_warning.update(
        {
            "zip_review_sufficient": True,
            "exact_final_commit_pin_missing_from_review_zip": True,
            "ignored_iddqd_v2_tree_absent_from_review_zip": True,
            "warning_is_stage_failure": False,
            "recommended_future_resolution": [
                "include archive/commit marker in future review ZIPs",
                "include compact local-source-root marker metadata where ignored trees are omitted",
                "do not commit raw third_party bodies",
            ],
            "execution_allowed": False,
        }
    )

    source_restatement = _base("stage5bm_string4_source_restatement", "source_restatement")
    source_restatement.update(
        {
            "source_stage5bk_byte_strings_record": repo_relative(STAGE5BK_BYTE_STRINGS_PATH),
            "source_stage5bk_string4_crosswalk": repo_relative(STAGE5BK_STRING4_CROSSWALK_PATH),
            "source_byte_string_id": string4_record.get("byte_string_id", "stage5bk-iddqd-v2-byte-string-4"),
            "source_label": string4_record.get("source_label", "Matrix from pages 49-51 converted to hexadecimal"),
            "source_root_path": repo_relative(LOCAL_IDDQD_V2_SOURCE_ROOT),
            "source_file_path": repo_relative(BYTE_STRINGS_SOURCE_PATH),
            "source_file_found": bool(local["source_file_found"]),
            "source_file_sha256": local["source_file_sha256"],
            "hex_length": local["hex_length"] or string4_record.get("hex_length"),
            "claimed_byte_length_if_hex": 256,
            "string4_hex_sha256": local["normalized_hex_sha256"] or string4_record.get("hex_sha256"),
            "string4_raw_hex_sha256": local["raw_hex_sha256"],
            "string4_decoded_byte_sha256": local["decoded_byte_sha256"] or string4_record.get("decoded_byte_sha256"),
            "source_string_body_committed": False,
            "full_hex_body_committed": False,
            "decoded_byte_body_committed": False,
            "reconstructed_token_stream_committed": False,
            "execution_allowed": False,
            "hash_search_performed": False,
            "decode_attempt_performed": False,
        }
    )

    inverse_policy = _base("stage5bm_string4_primary60_inverse_policy", "inverse_policy")
    inverse_policy.update(
        {
            "source_stage5ap_mapping": repo_relative(MAPPING_PATH),
            "source_stage5ap_transcription": repo_relative(TRANSCRIPTION_PATH),
            "source_stage5aw_branch_manifest": repo_relative(STAGE5AW_REPAIRED_BRANCH_MANIFEST_PATH),
            "primary60_alphabet": PRIMARY_ALPHABET,
            "inverse_formula": "token = str(value // 60) + alphabet[value % 60]",
            "input_domain": "0_to_255_bytes",
            "output_token_shape": "leading_digit_0_to_4_plus_primary60_suffix",
            "policy_scope": "string4_branch_membership_metadata_only",
            "full_hex_body_committed": False,
            "decoded_bytes_committed": False,
            "reconstructed_token_stream_committed": False,
            "real_byte_stream_generated": False,
            "active_token_block_manifest_changed": False,
            "canonical_transcription_changed": False,
            "execution_allowed": False,
        }
    )

    mismatch_analysis = _base("stage5bm_string4_stage5ap_mismatch_analysis", "mismatch_analysis")
    mismatch_analysis.update(
        {
            "source_string4_restatement": repo_relative(DATA_PATHS["source_restatement"]),
            "source_stage5ap_mapping": repo_relative(MAPPING_PATH),
            "source_stage5ap_transcription": repo_relative(TRANSCRIPTION_PATH),
            "string4_reparsed_from_local_source": bool(local["string4_reparsed_from_local_source"]),
            "stage5ap_token_count": len(canonical),
            "string4_decoded_byte_count": local["decoded_byte_count"] or 0,
            "stage5ap_primary60_decoded_byte_sha256": stage5ap_hashes["stage5ap_primary60_decoded_byte_sha256"],
            "string4_decoded_byte_sha256": local["decoded_byte_sha256"] or string4_record.get("decoded_byte_sha256"),
            "string4_matches_stage5ap_primary60_bytes": bool(
                (local["decoded_byte_sha256"] or string4_record.get("decoded_byte_sha256"))
                == stage5ap_hashes["stage5ap_primary60_decoded_byte_sha256"]
            ),
            "mismatch_count": len(mismatches),
            "canonical_match_count": counts.get("canonical_match", 0),
            "first_mismatch_index_0_based": mismatches[0]["token_index_0_based"] if mismatches else None,
            "last_mismatch_index_0_based": mismatches[-1]["token_index_0_based"] if mismatches else None,
            "mismatch_summary_records": [_compact_mismatch(row) for row in mismatches[:25]],
            "full_mismatch_table_committed": False,
            "ignored_full_mismatch_table_path": repo_relative(results_dir / "string4-stage5ap-mismatch-table.json"),
            "reconstructed_token_stream_committed": False,
            "real_byte_stream_generated": False,
            "execution_allowed": False,
            "hash_search_performed": False,
            "decode_attempt_performed": False,
        }
    )

    unresolved_summary = _read(STAGE5AW_REPAIRED_PRIMARY60_IMPACT_PATH)
    unsupported_records = [
        {
            "token_index_0_based": row["token_index_0_based"],
            "row_index_one_based": row["row_index_one_based"],
            "column_index_one_based": row["column_index_one_based"],
            "stage5ap_canonical_token": row["stage5ap_canonical_token"],
            "string4_inferred_token": row["string4_inferred_token"],
            "stage5aw_allowed_token_count": row["stage5aw_allowed_token_count"],
            "stage5aw_allowed_tokens_summary": _summarize_allowed_tokens(row["stage5aw_allowed_tokens"]),
            "suspected_ambiguity_class": row["ambiguity_class"],
            "reason": "String 4 inferred token is not present in Stage 5AW/5AY allowed options for this index.",
        }
        for row in unsupported
    ]
    branch_membership = _base("stage5bm_string4_stage5aw_branch_membership", "branch_membership")
    branch_membership.update(
        {
            "source_string4_mismatch_analysis": repo_relative(DATA_PATHS["mismatch_analysis"]),
            "source_stage5aw_branch_manifest": repo_relative(STAGE5AW_REPAIRED_BRANCH_MANIFEST_PATH),
            "source_stage5aw_unresolved_records": repo_relative(STAGE5AW_REPAIRED_UNRESOLVED_VARIANTS_PATH),
            "source_stage5aw_reviewer_extras": repo_relative(STAGE5AW_REPAIRED_REVIEWER_EXTRA_TOKENS_PATH),
            "source_stage5ay_branch_eligibility": repo_relative(STAGE5AY_BRANCH_ELIGIBILITY_POLICY_PATH),
            "stage5aw_unresolved_variant_record_count": unresolved_summary.get("unresolved_token_variant_count", 77),
            "stage5aw_primary60_mappable_option_count": unresolved_summary.get("primary60_mappable_option_count", 99),
            "stage5aw_primary60_unmappable_option_count": unresolved_summary.get("primary60_unmappable_option_count", 65),
            "string4_position_count_checked": len(canonical) if local["bytes"] is not None else 0,
            "string4_branch_membership_status": branch_status,
            "canonical_match_count": counts.get("canonical_match", 0),
            "stage5aw_supported_noncanonical_count": len(supported),
            "stage5aw_supported_total_count": counts.get("canonical_match", 0) + len(supported),
            "unsupported_position_count": len(unsupported),
            "parser_inconclusive_position_count": counts.get("source_token_unparseable", 0) + counts.get("not_checked", 0),
            "primary60_mappable_supported_count": sum(1 for row in supported if row.get("primary60_mappable") is not False),
            "primary60_unmappable_supported_context_count": sum(
                1 for row in supported if row.get("primary60_mappable") is False
            ),
            "unsupported_position_records": unsupported_records,
            "supported_noncanonical_records_summary": {
                "count": len(supported),
                "sample_records": [
                    {
                        "token_index_0_based": row["token_index_0_based"],
                        "stage5ap_canonical_token": row["stage5ap_canonical_token"],
                        "string4_inferred_token": row["string4_inferred_token"],
                        "ambiguity_class": row["ambiguity_class"],
                        "source_stage5aw_option_kind": row["source_stage5aw_option_kind"],
                    }
                    for row in supported[:10]
                ],
            },
            "full_position_table_committed": False,
            "ignored_full_position_table_path": repo_relative(results_dir / "string4-stage5aw-branch-membership.json"),
            "full_cartesian_product_enumerated": False,
            "branch_materialised_as_active": False,
            "active_token_block_manifest_changed": False,
            "canonical_transcription_changed": False,
            "real_byte_stream_generated": False,
            "execution_allowed": False,
        }
    )

    ambiguity_keys = [
        "I_l",
        "O_0",
        "case_only",
        "digit_letter_confusion",
        "primary60_suffix_choice",
        "prefix_digit_change",
        "visual_placeholder",
        "reviewer_extra",
        "canonical_exact",
        "unsupported_external",
        "other",
    ]
    difference_counts = Counter(row["ambiguity_class"] for row in mismatches)
    coverage = _base("stage5bm_string4_ambiguity_class_coverage", "ambiguity_coverage")
    coverage.update(
        {
            "source_branch_membership": repo_relative(DATA_PATHS["branch_membership"]),
            "ambiguity_class_counts": {key: difference_counts.get(key, 0) for key in ambiguity_keys},
            "coverage_assessment": "partially_supported" if branch_status == "partial_branch_match" else (
                "all_supported_by_known_ambiguity_classes" if branch_status == "full_branch_match" else "unsupported_or_inconclusive"
            ),
            "majority_difference_class": difference_counts.most_common(1)[0][0] if difference_counts else None,
            "notes": [
                "String 4 may represent external community transcription branch only if supported by Stage 5AW metadata.",
                "Ambiguity-class support is not canonicalisation and does not authorise execution.",
            ],
            "execution_allowed": False,
            "canonical_transcription_changed": False,
            "active_token_block_manifest_changed": False,
        }
    )

    planning_constraint = _base("stage5bm_string4_planning_constraint", "planning_constraint")
    planning_constraint.update(
        {
            "source_branch_membership": repo_relative(DATA_PATHS["branch_membership"]),
            "planning_constraint_id": "stage5bm-string4-not-active-input-until-reviewed",
            "planning_effect": planning_effect,
            "string4_active_input_allowed": False,
            "string4_execution_input_allowed": False,
            "string4_byte_stream_generation_allowed": False,
            "string4_dry_run_ingestion_allowed_now": False,
            "string4_future_use_requires": [
                "stage5bm_branch_membership_record",
                "deep_research_review_of_stage5bm",
                "explicit future Codex planning-ingestion stage",
                "no-execution gate review",
                "source-gap closure if unsupported positions remain",
            ],
            "stage5bd_dry_run_records_remain_valid": True,
            "future_token_block_execution_remains_blocked": True,
            "requires_deep_research_review_before_dry_run_context_ingestion": branch_status == "full_branch_match",
            "requires_gap_closure_before_any_ingestion": branch_status != "full_branch_match",
            "execution_allowed": False,
        }
    )

    gap_update = _base("stage5bm_source_gap_severity_update", "gap_update")
    existing_gap = _read(STAGE5BK_GAP_REGISTER_PATH)
    existing_records = list(existing_gap.get("records", []))
    new_gap = {
        "source_gap_id": "stage5bk-string4-stage5ap-branch-membership-unreconciled",
        "source_gap_origin": STAGE_ID,
        "affected_family": "token_block_page49_51_context",
        "affected_candidate_ids": ["stage5bk-iddqd-v2-byte-string-4"],
        "severity": "high" if branch_status != "full_branch_match" else "medium",
        "closure_status": source_gap_closure,
        "blocks_execution": True,
        "blocks_metadata_planning": False,
        "blocks_string4_ingestion_or_active_use": True,
        "blocks_future_token_block_execution": True,
        "recommended_resolution": [
            "Prepare human-review/source-gap closure for unsupported String 4 position(s)."
            if branch_status != "full_branch_match"
            else "Deep Research review before any dry-run context ingestion."
        ],
        "execution_allowed": False,
        "solve_claim": False,
    }
    gap_update.update(
        {
            "source_stage5bk_gap_register": repo_relative(STAGE5BK_GAP_REGISTER_PATH),
            "source_gap_update_count": len(existing_records) + 1,
            "new_source_gap_count": 1,
            "closed_source_gap_count": 0 if branch_status != "full_branch_match" else 1,
            "carried_forward_source_gap_count": len(existing_records) + (0 if branch_status == "full_branch_match" else 1),
            "records": existing_records + [new_gap],
        }
    )

    family_update = _base("stage5bm_historical_family_granularity_update", "family_update")
    family_update.update(
        {
            "source_stage5bk_family_status": repo_relative(STAGE5BK_FAMILY_STATUS_PATH),
            "granularity_update_status": "targeted_addendum_only",
            "new_or_refined_family_rows": [
                {
                    "family_id": "token_block_page49_51_string4_branch_context",
                    "parent_family_id": "token_block_page49_51_context",
                    "planning_status": "partial_branch_context_only" if branch_status == "partial_branch_match" else planning_effect,
                    "execution_allowed": False,
                },
                {
                    "family_id": "pgp_false_path_warning_and_7a35090f_gate",
                    "parent_family_id": "authenticity_pgp_route",
                    "planning_status": "blocked_authenticity_gate_required",
                    "execution_allowed": False,
                },
                {
                    "family_id": "stego_outguess_openpuff_mp3_positive_controls",
                    "parent_family_id": "stego_audio_positive_controls",
                    "planning_status": "positive_control_only_or_review_before_execution",
                    "execution_allowed": False,
                },
            ],
            "family_status_records_mutated": False,
            "method_status_upgraded": False,
            "execution_allowed": False,
        }
    )

    dwh = _base("stage5bm_dwh_quarantine_reaffirmation", "dwh")
    dwh.update(
        {
            "source_stage5bk_dwh_record": repo_relative(STAGE5BK_DWH_PATH),
            "source_stage5bf_dwh_record": repo_relative(STAGE5BF_DWH_PATH),
            "dwh_expansion": "Deep Web Hash",
            "dwh_operational_status": "not_operational",
            "token_block_dwh_relationship_status": "speculative_source_lock_required",
            "string4_dwh_status": "not_a_dwh_target",
            "hash_search_performed": False,
            "hash_preimage_search_performed": False,
            "hash_comparison_performed_as_experiment": False,
            "decode_attempt_performed": False,
            "execution_allowed": False,
        }
    )

    errata = _base("stage5bm_stage5bj_errata_supersession", "errata")
    errata.update(
        {
            "source_stage5bk_errata": repo_relative(STAGE5BK_ERRATA_PATH),
            "errata_id": "stage5bm-stage5bj-hidden-content-4gq25-planning-supersession",
            "source_stage5bj_record_id": "stage5bj-page-body-hidden-original-image",
            "source_url": "https://uncovering-cicada.fandom.com/wiki/Hidden_content_of_original_image_(January_4th_2013)",
            "problem": "Stage 5BJ linked a 2013 hidden-original-image Fandom page-body row to the 2016 4gq25 media fixture.",
            "corrected_planning_status": "media_source_reference_or_positive_control_only_not_exact_page_body_snapshot",
            "supersedes_for_planning": True,
            "stage5bj_historical_records_mutated": False,
            "route_equivalent_file_is_page_body_snapshot": False,
            "route_equivalent_file_is_media_fixture": True,
            "execution_allowed": False,
            "image_forensics_performed": False,
        }
    )

    lineage = _base("stage5bm_token_block_lineage_preservation", "lineage")
    lineage.update(
        {
            "source_records": [
                repo_relative(TRANSCRIPTION_PATH),
                repo_relative(STAGE5AW_REPAIRED_BRANCH_MANIFEST_PATH),
                "data/token-block/stage5az-repaired-bounded-variant-family-manifest.yaml",
                "data/token-block/stage5bb-active-manifest-registry.yaml",
                "data/token-block/stage5bd-active-manifest-lock.yaml",
                "data/token-block/stage5bd-dry-run-plan-manifest.yaml",
            ],
            "canonical_transcription_changed": False,
            "active_token_block_manifest_changed": False,
            "stage5aw_branch_manifest_changed": False,
            "stage5az_variant_family_manifest_changed": False,
            "stage5bd_dry_run_records_remain_valid": True,
            "future_token_block_execution_remains_blocked": True,
            "string4_branch_materialised_as_active": False,
            "real_token_block_byte_streams_generated": False,
            "variant_byte_streams_generated": False,
            "execution_allowed": False,
        }
    )

    dry_run_impact = _base("stage5bm_future_dry_run_planning_impact", "dry_run_impact")
    dry_run_impact.update(
        {
            "source_string4_branch_membership": repo_relative(DATA_PATHS["branch_membership"]),
            "source_string4_planning_constraint": repo_relative(DATA_PATHS["planning_constraint"]),
            "source_stage5bd_summary": repo_relative(STAGE5BD_SUMMARY_PATH),
            "stage5bd_status": "complete",
            "future_dry_run_planning_impact_status": "metadata_constraints_only",
            "future_dry_run_can_consume": [
                "string4_branch_membership_status",
                "string4_supported_unsupported_counts",
                "source_gap_severity_update",
                "planning_constraint_ids",
            ],
            "future_dry_run_must_not_consume": [
                "raw String 4 hex body",
                "decoded String 4 byte body",
                "reconstructed full token stream",
                "active String 4 bytes",
                "raw iddqd-v2 files",
                "generated diagnostic bodies",
            ],
            "future_runner_must_cite_stage5bm_constraints": True,
            "requires_deep_research_review_before_ingestion": True,
            "execution_gate_default": "blocked",
            "real_byte_stream_generated": False,
            "variant_materialisation_performed": False,
            "full_cartesian_product_enumerated": False,
            "hash_search_performed": False,
            "decode_attempt_performed": False,
            "scoring_performed": False,
            "execution_allowed": False,
        }
    )

    handoff = _base("stage5bm_codex_handoff_policy", "handoff")
    handoff.update(
        {
            "canonical_handoff_root": "codex-output",
            "deprecated_handoff_root": "codex_output",
            "future_stages_must_use_deprecated_root": False,
            "codex_completion_summary_path": repo_relative(CODEX_COMPLETION_PATH),
            "codex_output_used": False,
            "codex_output_committed": False,
            "codex_output_directory_created": False,
            "deprecated_handoff_root_present": DEPRECATED_CODEX_OUTPUT.exists(),
            "completion_summary_committed": False,
        }
    )

    guardrail = _guardrail()

    summary = _base("stage5bm_summary", "summary")
    summary.update(
        {
            "status": "complete",
            "source_stage_ids": [
                SOURCE_DEEP_RESEARCH_STAGE,
                SOURCE_PREVIOUS_STAGE,
                "stage-5bj",
                "stage-5bi",
                "stage-5bf",
                "stage-5bd",
            ],
            "stage5bl_findings_integrated": True,
            "review_packaging_warning_recorded": True,
            "string4_source_restatement_created": True,
            "string4_primary60_inverse_policy_created": True,
            "string4_stage5ap_mismatch_analysis_created": True,
            "string4_stage5aw_branch_membership_created": True,
            "string4_ambiguity_class_coverage_created": True,
            "string4_planning_constraint_created": True,
            "string4_branch_membership_status": branch_status,
            "string4_position_count_checked": len(canonical) if local["bytes"] is not None else 0,
            "string4_canonical_match_count": counts.get("canonical_match", 0),
            "string4_stage5aw_supported_noncanonical_count": len(supported),
            "string4_unsupported_position_count": len(unsupported),
            "string4_parser_inconclusive_position_count": counts.get("source_token_unparseable", 0) + counts.get("not_checked", 0),
            "string4_full_body_committed": False,
            "string4_decoded_bytes_committed": False,
            "string4_reconstructed_token_stream_committed": False,
            "source_gap_severity_update_created": True,
            "string4_source_gap_status": source_gap_status,
            "historical_family_granularity_update_created": True,
            "stage5bj_errata_supersession_created": True,
            "dwh_quarantine_reaffirmed": True,
            "token_block_lineage_preserved": True,
            "future_dry_run_planning_impact_created": True,
            "canonical_transcription_changed": False,
            "active_token_block_manifest_changed": False,
            "stage5bd_dry_run_records_remain_valid": True,
            "future_token_block_execution_remains_blocked": True,
            "raw_archive_files_committed": False,
            "raw_iddqd_v2_files_committed": False,
            "fandom_page_bodies_committed": False,
            "fandom_images_committed": False,
            "full_surface_bodies_committed": False,
            "decoded_byte_bodies_committed": False,
            "generated_outputs_committed": False,
            "token_experiments_executed": False,
            "real_token_block_byte_streams_generated": False,
            "variant_byte_streams_generated": False,
            "hash_search_performed": False,
            "decode_attempt_performed": False,
            "stego_tool_execution_performed": False,
            "cuda_execution_performed": False,
            "benchmark_performed": False,
            "scored_experiments_executed": False,
            "parallel_validation_harness_used": True,
            "parallel_validation_run_passed": False,
            "consistency_checks_passed": False,
            "codex_completion_summary_path": repo_relative(CODEX_COMPLETION_PATH),
            "codex_output_directory_used": False,
            "recommended_next_prompt_type": next_prompt_type,
            "recommended_next_stage_title": next_title,
            "recommended_next_stage_reason": next_reason,
        }
    )

    next_stage = _base("stage5bm_next_stage_decision", "next_stage")
    next_stage.update(FALSE_NEXT_STAGE_FLAGS)
    next_stage.update(
        {
            "selected_next_stage_id": "stage-5bn",
            "selected_next_prompt_type": next_prompt_type,
            "selected_next_stage_title": next_title,
            "selected_next_stage_reason": next_reason,
            "string4_branch_membership_status": branch_status,
            "string4_source_gap_status": source_gap_status,
        }
    )

    records = {
        "findings": findings,
        "review_warning": review_warning,
        "source_restatement": source_restatement,
        "inverse_policy": inverse_policy,
        "mismatch_analysis": mismatch_analysis,
        "branch_membership": branch_membership,
        "ambiguity_coverage": coverage,
        "planning_constraint": planning_constraint,
        "lineage": lineage,
        "dry_run_impact": dry_run_impact,
        "gap_update": gap_update,
        "family_update": family_update,
        "dwh": dwh,
        "errata": errata,
        "guardrail": guardrail,
        "handoff": handoff,
        "summary": summary,
        "next_stage": next_stage,
    }
    for key, payload in records.items():
        write_yaml(DATA_PATHS[key], payload)

    _write_generated(results_dir / "string4-stage5ap-mismatch-table.json", [_compact_mismatch(row) for row in mismatches])
    _write_generated(results_dir / "string4-stage5aw-branch-membership.json", reconciliation["rows"])
    _write_generated(
        results_dir / "summary.json",
        {
            "stage_id": STAGE_ID,
            "string4_branch_membership_status": branch_status,
            "canonical_match_count": counts.get("canonical_match", 0),
            "stage5aw_supported_noncanonical_count": len(supported),
            "unsupported_position_count": len(unsupported),
            "parser_inconclusive_position_count": counts.get("source_token_unparseable", 0) + counts.get("not_checked", 0),
            "generated_outputs_committed": False,
            "solve_claim": False,
        },
    )
    _write_generated(historical_results_dir / "summary.json", {"stage_id": STAGE_ID, "source_gap_status": source_gap_status})

    return summary


def validate_stage5bm(results_dir: Path = RESULTS_DIR, summary: Path = DATA_PATHS["summary"]) -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    for key, path in DATA_PATHS.items():
        if not path.is_file():
            errors.append(f"missing required Stage 5BM record: {path}")
            continue
        payload = _read(path)
        if payload.get("stage_id") != STAGE_ID:
            errors.append(f"{path} has unexpected stage_id={payload.get('stage_id')}")
        if payload.get("solve_claim") is not False:
            errors.append(f"{path} must keep solve_claim=false")
        for flag, expected in FALSE_FLAGS.items():
            if flag in payload and payload.get(flag) is not expected:
                errors.append(f"{path} has {flag}={payload.get(flag)!r}, expected {expected!r}")

    summary_payload = _read(summary)
    branch = _read(DATA_PATHS["branch_membership"])
    guardrail = _read(DATA_PATHS["guardrail"])
    handoff = _read(DATA_PATHS["handoff"])
    next_stage = _read(DATA_PATHS["next_stage"])

    if branch.get("string4_position_count_checked") != 256:
        errors.append("String 4 branch membership must check exactly 256 positions")
    if branch.get("string4_branch_membership_status") not in {
        "full_branch_match",
        "partial_branch_match",
        "external_mismatch_unrepresented",
        "parser_or_source_inconclusive",
        "not_attempted_due_missing_source",
    }:
        errors.append("String 4 branch membership status is invalid")
    if branch.get("full_cartesian_product_enumerated") is not False:
        errors.append("Stage 5BM must not enumerate the full Cartesian product")
    if handoff.get("canonical_handoff_root") != "codex-output" or handoff.get("codex_output_used") is not False:
        errors.append("Stage 5BM must use codex-output and must not use codex_output")
    if DEPRECATED_CODEX_OUTPUT.exists():
        errors.append("deprecated codex_output directory exists unexpectedly")
    for key, expected in FALSE_NEXT_STAGE_FLAGS.items():
        if next_stage.get(key) is not expected:
            errors.append(f"next-stage decision has {key}={next_stage.get(key)!r}, expected {expected!r}")
    if guardrail.get("string4_branch_crosswalk_metadata_only") is not True:
        errors.append("guardrail must mark String 4 crosswalk as metadata-only")
    if not (results_dir / "summary.json").is_file():
        errors.append("ignored Stage 5BM generated summary is missing")

    counts = {
        "stage5bm_valid": not errors,
        "validation_error_count": len(errors),
        "string4_branch_membership_status": branch.get("string4_branch_membership_status"),
        "string4_position_count_checked": branch.get("string4_position_count_checked"),
        "canonical_match_count": branch.get("canonical_match_count"),
        "stage5aw_supported_noncanonical_count": branch.get("stage5aw_supported_noncanonical_count"),
        "unsupported_position_count": branch.get("unsupported_position_count"),
        "parser_inconclusive_position_count": branch.get("parser_inconclusive_position_count"),
        "future_token_block_execution_remains_blocked": summary_payload.get("future_token_block_execution_remains_blocked"),
        "codex_output_used": handoff.get("codex_output_used"),
    }
    return counts, errors


def stage5bm_summary(summary: Path = DATA_PATHS["summary"]) -> dict[str, Any]:
    return _read(summary)
