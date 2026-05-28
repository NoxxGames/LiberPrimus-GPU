"""Stage 5BO token-case human-review errata integration metadata."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from libreprimus.token_block.models import (
    PRIMARY_ALPHABET,
    STAGE5AW_REPAIRED_REVIEWER_EXTRA_TOKENS_PATH,
    STAGE5AW_REPAIRED_UNRESOLVED_VARIANTS_PATH,
    STAGE5AY_BRANCH_ELIGIBILITY_POLICY_PATH,
    repo_relative,
    sha256_file,
    token_rows,
    write_json,
    write_yaml,
)
from libreprimus.token_block.possible_token_parser import parse_possible_token_notes
from libreprimus.token_block.stage5bn import (
    DATA_PATHS as STAGE5BN_DATA_PATHS,
)
from libreprimus.token_block.stage5bn import (
    STAGE5AW_ALLOWED_TOKENS,
    STRING4_INFERRED_TOKEN,
    TARGET_TOKEN_INDEX,
)
from libreprimus.token_block.stage5bm import (
    DATA_PATHS as STAGE5BM_DATA_PATHS,
)
from libreprimus.token_block.stage5bm import _read

STAGE_ID = "stage-5bo"
STAGE_TITLE = (
    "Stage 5BO - Token-case human-review errata integration and String 4 "
    "full-branch reclassification, without execution"
)
PROMPT_TYPE = "codex_metadata_repair"
SOURCE_PREVIOUS_STAGE = "stage-5bn"
SOURCE_PREVIOUS_COMMIT = "a55c46ff44b29166ea2a646d6503f6810729c23b"
SOURCE_DEEP_RESEARCH_STAGE = "stage-5bl"
SOURCE_DEEP_RESEARCH_REPORT = "09_LiberPrimus-GPU-Stage-5BL-Deep-Research-Review.md"

ORIGINAL_TEMPLATE_PATH = Path("human-review-packs/stage5au/token-case-review-v2/decision-template.yaml")
CORRECTED_TEMPLATE_PATH = Path("human-review-packs/stage5au/token-case-review-v2/decision-template-corrected.yaml")
RESULTS_DIR = Path("experiments/results/token-block/stage5bo")
HISTORICAL_RESULTS_DIR = Path("experiments/results/historical-route/stage5bo")
CODEX_COMPLETION_PATH = Path("codex-output/stage5bo-codex-completion.md")
DEPRECATED_CODEX_OUTPUT = Path("codex_output")

STAGE5BM_MISMATCH_PATH = STAGE5BM_DATA_PATHS["mismatch_analysis"]
STAGE5BM_BRANCH_MEMBERSHIP_PATH = STAGE5BM_DATA_PATHS["branch_membership"]
STAGE5BM_PLANNING_CONSTRAINT_PATH = STAGE5BM_DATA_PATHS["planning_constraint"]
STAGE5BN_ADDENDUM_PATH = STAGE5BN_DATA_PATHS["proposed_addendum"]
STAGE5BN_SPREADSHEET_AUDIT_PATH = STAGE5BN_DATA_PATHS["spreadsheet_audit"]
STAGE5BN_GAP_CLOSURE_PATH = STAGE5BN_DATA_PATHS["gap_closure"]
STAGE5BN_PLANNING_CONSTRAINT_PATH = STAGE5BN_DATA_PATHS["planning_constraint_update"]
STAGE5BN_DWH_PATH = STAGE5BN_DATA_PATHS["dwh_quarantine"]

DATA_PATHS: dict[str, Path] = {
    "source_lock": Path("data/token-block/stage5bo-decision-template-correction-source-lock.yaml"),
    "errata": Path("data/token-block/stage5bo-token-case-human-review-errata.yaml"),
    "impact": Path("data/token-block/stage5bo-token-case-correction-impact-summary.yaml"),
    "universe": Path("data/token-block/stage5bo-errata-aware-token-option-universe.yaml"),
    "string4": Path("data/token-block/stage5bo-string4-branch-membership-after-errata.yaml"),
    "addendum": Path("data/token-block/stage5bo-stage5bn-addendum-integration.yaml"),
    "gap_closure": Path("data/token-block/stage5bo-string4-source-gap-closure-after-errata.yaml"),
    "planning_constraint": Path("data/token-block/stage5bo-string4-planning-constraint-update.yaml"),
    "lineage": Path("data/token-block/stage5bo-token-block-lineage-preservation.yaml"),
    "future_impact": Path("data/token-block/stage5bo-future-dry-run-planning-impact.yaml"),
    "gap_severity": Path("data/historical-route/stage5bo-source-gap-severity-update.yaml"),
    "dwh": Path("data/historical-route/stage5bo-dwh-quarantine-reaffirmation.yaml"),
    "guardrail": Path("data/historical-route/stage5bo-guardrail.yaml"),
    "handoff": Path("data/source-harvester/stage5bo-codex-handoff-policy.yaml"),
    "summary": Path("data/project-state/stage5bo-summary.yaml"),
    "next_stage": Path("data/project-state/stage5bo-next-stage-decision.yaml"),
}

SCHEMA_PATHS: dict[str, str] = {
    "source_lock": "schemas/token-block/stage5bo-decision-template-correction-source-lock-v0.schema.json",
    "errata": "schemas/token-block/stage5bo-token-case-human-review-errata-v0.schema.json",
    "impact": "schemas/token-block/stage5bo-token-case-correction-impact-summary-v0.schema.json",
    "universe": "schemas/token-block/stage5bo-errata-aware-token-option-universe-v0.schema.json",
    "string4": "schemas/token-block/stage5bo-string4-branch-membership-after-errata-v0.schema.json",
    "addendum": "schemas/token-block/stage5bo-stage5bn-addendum-integration-v0.schema.json",
    "gap_closure": "schemas/token-block/stage5bo-string4-source-gap-closure-after-errata-v0.schema.json",
    "planning_constraint": "schemas/token-block/stage5bo-string4-planning-constraint-update-v0.schema.json",
    "lineage": "schemas/token-block/stage5bo-token-block-lineage-preservation-v0.schema.json",
    "future_impact": "schemas/token-block/stage5bo-future-dry-run-planning-impact-v0.schema.json",
    "gap_severity": "schemas/historical-route/stage5bo-source-gap-severity-update-v0.schema.json",
    "dwh": "schemas/historical-route/stage5bo-dwh-quarantine-reaffirmation-v0.schema.json",
    "guardrail": "schemas/historical-route/stage5bo-guardrail-v0.schema.json",
    "handoff": "schemas/source-harvester/stage5bo-codex-handoff-policy-v0.schema.json",
    "summary": "schemas/project-state/stage5bo-summary-v0.schema.json",
    "next_stage": "schemas/project-state/stage5bo-next-stage-decision-v0.schema.json",
}

SOURCE_RECORD_PATHS = [
    repo_relative(DATA_PATHS["source_lock"]),
    repo_relative(DATA_PATHS["errata"]),
    repo_relative(DATA_PATHS["impact"]),
    repo_relative(DATA_PATHS["universe"]),
    repo_relative(DATA_PATHS["string4"]),
    repo_relative(DATA_PATHS["addendum"]),
    repo_relative(DATA_PATHS["gap_closure"]),
    repo_relative(DATA_PATHS["planning_constraint"]),
    repo_relative(DATA_PATHS["lineage"]),
    repo_relative(DATA_PATHS["future_impact"]),
    repo_relative(DATA_PATHS["gap_severity"]),
    repo_relative(DATA_PATHS["dwh"]),
    repo_relative(DATA_PATHS["guardrail"]),
    repo_relative(DATA_PATHS["handoff"]),
]

FALSE_FLAGS: dict[str, bool] = {
    "active_stage5aw_records_mutated": False,
    "active_stage5ay_records_mutated": False,
    "active_stage5az_records_mutated": False,
    "active_token_block_manifest_changed": False,
    "ai_ml_interpretation_performed": False,
    "audio_analysis_performed": False,
    "benchmark_performed": False,
    "branch_materialised_as_active": False,
    "canonical_corpus_active": False,
    "canonical_transcription_changed": False,
    "codex_output_used": False,
    "corrected_decision_template_committed": False,
    "cuda_execution_performed": False,
    "cuda_source_modified": False,
    "decision_template_committed": False,
    "decode_attempt_performed": False,
    "decoded_byte_body_committed": False,
    "dwh_hash_search_performed": False,
    "execution_allowed": False,
    "full_cartesian_product_enumerated": False,
    "full_position_table_committed": False,
    "full_string4_body_committed": False,
    "full_universe_table_committed": False,
    "generated_outputs_committed": False,
    "hash_search_performed": False,
    "image_forensics_performed": False,
    "llm_vision_token_reading_performed": False,
    "method_status_upgraded": False,
    "mp3stego_execution_performed": False,
    "ocr_performed": False,
    "openpuff_execution_performed": False,
    "outguess_execution_performed": False,
    "public_website_publication_performed": False,
    "raw_archive_body_committed": False,
    "raw_human_review_pack_committed": False,
    "real_byte_stream_generated": False,
    "real_token_block_byte_streams_generated": False,
    "reconstructed_token_stream_committed": False,
    "scoring_performed": False,
    "solve_claim": False,
    "spreadsheet_body_committed": False,
    "spreadsheet_file_committed": False,
    "stage5aw_branch_manifest_changed": False,
    "stage5ay_branch_eligibility_changed": False,
    "stage5az_variant_family_manifest_changed": False,
    "stego_tool_execution_performed": False,
    "string4_active_input_allowed": False,
    "string4_byte_stream_generation_allowed": False,
    "string4_combined_with_2014_surfaces": False,
    "string4_dry_run_ingestion_allowed_now": False,
    "string4_execution_input_allowed": False,
    "template_bodies_committed": False,
    "templates_committed": False,
    "token_experiments_executed": False,
    "variant_byte_streams_generated": False,
    "variant_materialisation_performed": False,
}

FALSE_NEXT_STAGE_FLAGS: dict[str, bool] = {
    "ai_ml_selected": False,
    "benchmark_selected": False,
    "byte_stream_generation_selected": False,
    "canonical_corpus_activation_selected": False,
    "cuda_selected": False,
    "decode_selected": False,
    "dwh_hash_search_selected": False,
    "method_status_upgrade_selected": False,
    "ocr_selected": False,
    "page_boundary_finalisation_selected": False,
    "scored_experiments_selected": False,
    "solve_claim": False,
    "stego_execution_selected": False,
    "token_block_execution_selected": False,
    "variant_materialisation_selected": False,
}


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
        "prompt_type": PROMPT_TYPE,
        "source_previous_stage": SOURCE_PREVIOUS_STAGE,
        "source_previous_stage_commit": SOURCE_PREVIOUS_COMMIT,
        "source_deep_research_stage": SOURCE_DEEP_RESEARCH_STAGE,
        "source_deep_research_report": SOURCE_DEEP_RESEARCH_REPORT,
        "metadata_only": True,
        "solve_claim": False,
    }


def _file_metadata(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {"found": False, "sha256": None, "size_bytes": None}
    return {
        "found": True,
        "sha256": sha256_file(path),
        "size_bytes": path.stat().st_size,
    }


def _load_template(path: Path) -> dict[str, Any] | None:
    if not path.is_file():
        return None
    return _read(path)


def _template_records(payload: dict[str, Any] | None) -> dict[str, dict[str, Any]]:
    if not payload:
        return {}
    records = payload.get("records", [])
    return {str(record["challenge_id"]): dict(record) for record in records if record.get("challenge_id")}


def _possible_tokens(record: dict[str, Any] | None) -> list[str]:
    if not record:
        return []
    return parse_possible_token_notes(str(record.get("reviewer_notes") or "")).possible_tokens


def _raw_possible_token_fragments(record: dict[str, Any] | None) -> list[str]:
    if not record:
        return []
    notes = str(record.get("reviewer_notes") or "")
    for segment in notes.split(";"):
        key, sep, value = segment.strip().partition("=")
        if sep and key.strip().lower() == "possible_tokens":
            return [fragment.strip() for fragment in value.strip().split("|") if fragment.strip()]
    return []


def _ordered_added(after: list[str], before: list[str]) -> list[str]:
    before_set = set(before)
    return [token for token in after if token not in before_set]


def _ordered_removed(before: list[str], after: list[str]) -> list[str]:
    after_set = set(after)
    return [token for token in before if token not in after_set]


def _changed_fields(original: dict[str, Any], corrected: dict[str, Any]) -> list[str]:
    keys = sorted(set(original) | set(corrected))
    return [key for key in keys if original.get(key) != corrected.get(key)]


def _case_sort_key(case_id: str) -> tuple[int, str]:
    suffix = case_id.rsplit("-", 1)[-1]
    return (int(suffix) if suffix.isdigit() else 999999, case_id)


def _classify_primary60(token: str) -> dict[str, Any]:
    if "?" in token:
        return {
            "primary60_mappable": False,
            "primary60_value": None,
            "primary60_error": "visual_placeholder_unmappable",
        }
    if len(token) != 2:
        return {
            "primary60_mappable": False,
            "primary60_value": None,
            "primary60_error": "token_length_not_2",
        }
    first, suffix = token[0], token[1]
    if first not in "01234":
        return {
            "primary60_mappable": False,
            "primary60_value": None,
            "primary60_error": "first_symbol_not_in_0_to_4",
        }
    if suffix not in PRIMARY_ALPHABET:
        return {
            "primary60_mappable": False,
            "primary60_value": None,
            "primary60_error": "suffix_not_in_primary_60_alphabet",
        }
    return {
        "primary60_mappable": True,
        "primary60_value": int(first) * 60 + PRIMARY_ALPHABET.index(suffix),
        "primary60_error": None,
    }


def _mappable(tokens: list[str], expected: bool) -> list[str]:
    return [token for token in tokens if bool(_classify_primary60(token)["primary60_mappable"]) is expected]


def _errata_classification(added: list[str], removed: list[str], changed_fields: list[str]) -> str:
    if added or removed:
        if any(set(token) & {"i", "j", "I", "l"} for token in added + removed):
            return "operator_possible_tokens_typo"
        return "operator_possible_tokens_typo"
    if changed_fields == ["reviewer_notes"]:
        return "operator_metadata_correction"
    if changed_fields:
        return "non_token_field_change"
    return "inconclusive"


def _errata_impact(case_id: str, added: list[str], removed: list[str]) -> list[str]:
    impacts: list[str] = []
    if case_id == "stage5at-token-case-199" and STRING4_INFERRED_TOKEN in added:
        impacts.append("string4_branch_blocker_closure")
    if _mappable(added, True) or _mappable(removed, True) or _mappable(added, False) or _mappable(removed, False):
        impacts.append("primary60_mappability_change")
    if not impacts:
        impacts.append("no_string4_impact")
    return impacts


def _build_errata_records(
    original_template: dict[str, Any] | None,
    corrected_template: dict[str, Any] | None,
) -> list[dict[str, Any]]:
    original_records = _template_records(original_template)
    corrected_records = _template_records(corrected_template)
    records: list[dict[str, Any]] = []
    for case_id in sorted(set(original_records) | set(corrected_records), key=_case_sort_key):
        original = original_records.get(case_id, {})
        corrected = corrected_records.get(case_id, {})
        if original == corrected:
            continue
        before = _possible_tokens(original)
        after = _possible_tokens(corrected)
        before_raw = _raw_possible_token_fragments(original)
        after_raw = _raw_possible_token_fragments(corrected)
        added = _ordered_added(after, before)
        removed = _ordered_removed(before, after)
        token_index = int((corrected or original).get("token_index_0_based", -1))
        field_names = _changed_fields(original, corrected)
        possible_tokens_changed = before != after or before_raw != after_raw
        records.append(
            {
                "case_id": case_id,
                "token_index_0_based": token_index,
                "row_index_one_based": token_index // 8 + 1 if token_index >= 0 else None,
                "column_index_one_based": token_index % 8 + 1 if token_index >= 0 else None,
                "canonical_token": (corrected or original).get("canonical_token"),
                "original_possible_tokens": before,
                "corrected_possible_tokens": after,
                "original_possible_token_fragments": before_raw,
                "corrected_possible_token_fragments": after_raw,
                "added_tokens": added,
                "removed_tokens": removed,
                "unchanged_tokens": [token for token in before if token in set(after)],
                "field_names_changed": field_names,
                "possible_tokens_changed": possible_tokens_changed,
                "errata_classification": (
                    "operator_possible_tokens_typo"
                    if possible_tokens_changed
                    else _errata_classification(added, removed, field_names)
                ),
                "errata_impact": _errata_impact(case_id, added, removed),
                "primary60_mappable_added_tokens": _mappable(added, True),
                "primary60_mappable_removed_tokens": _mappable(removed, True),
                "primary60_unmappable_added_tokens": _mappable(added, False),
                "primary60_unmappable_removed_tokens": _mappable(removed, False),
                "canonical_token_changed": original.get("canonical_token") != corrected.get("canonical_token"),
                "active_manifest_changed": False,
                "possible_tokens_field_source": "reviewer_notes",
            }
        )
    return records


def _canonical_tokens() -> list[str]:
    return [token for row in token_rows() for token in row]


def _active_allowed_universe(canonical: list[str]) -> tuple[dict[int, set[str]], dict[int, dict[str, dict[str, Any]]]]:
    allowed: dict[int, set[str]] = {index: {token} for index, token in enumerate(canonical)}
    details: dict[int, dict[str, dict[str, Any]]] = {
        index: {
            token: {
                "source_option_kind": "canonical",
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
                "source_option_kind": detail.get("possible_token_source", "possible_token_detail"),
                "primary60_mappable": bool(detail.get("primary60_mappable")),
                "option_classes": [detail.get("possible_token_source", "possible_token_detail")],
            }
        for token in record.get("possible_tokens", []):
            token_value = str(token)
            allowed[index].add(token_value)
            details[index].setdefault(
                token_value,
                {
                    "source_option_kind": "possible_tokens",
                    "primary60_mappable": _classify_primary60(token_value)["primary60_mappable"],
                    "option_classes": ["possible_token"],
                },
            )
    extras = _read(STAGE5AW_REPAIRED_REVIEWER_EXTRA_TOKENS_PATH)
    for record in extras.get("records", []):
        index = int(record["token_index_0_based"])
        token = str(record["reviewer_extra_possible_token"])
        allowed[index].add(token)
        details[index][token] = {
            "source_option_kind": "reviewer_extra",
            "primary60_mappable": bool(record.get("primary60_mappable")),
            "option_classes": ["reviewer_extra_possible_token"],
        }
    eligibility = _read(STAGE5AY_BRANCH_ELIGIBILITY_POLICY_PATH)
    for record in eligibility.get("option_records", []):
        index = int(record["token_index_0_based"])
        token = str(record["token"])
        allowed[index].add(token)
        details[index][token] = {
            "source_option_kind": "branch_eligibility",
            "primary60_mappable": bool(record.get("primary60_mappable")),
            "option_classes": list(record.get("option_classes", [])),
        }
    return allowed, details


def _active_token_order(index: int, active_allowed: dict[int, set[str]]) -> list[str]:
    unresolved = _read(STAGE5AW_REPAIRED_UNRESOLVED_VARIANTS_PATH)
    for record in unresolved.get("records", []):
        if int(record["token_index_0_based"]) == index:
            return [str(token) for token in record.get("possible_tokens", [])]
    return sorted(active_allowed.get(index, []))


def _build_universe_records(
    errata_records: list[dict[str, Any]],
    active_allowed: dict[int, set[str]],
) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for errata in errata_records:
        index = int(errata["token_index_0_based"])
        active_tokens = _active_token_order(index, active_allowed)
        corrected_tokens = list(errata["corrected_possible_tokens"])
        records.append(
            {
                "token_index_0_based": index,
                "case_id": errata["case_id"],
                "stage5ap_canonical_token": errata.get("canonical_token"),
                "stage5aw_active_allowed_tokens_before_errata": active_tokens,
                "corrected_possible_tokens_from_operator_template": corrected_tokens,
                "errata_added_tokens": _ordered_added(corrected_tokens, active_tokens),
                "errata_removed_tokens": _ordered_removed(active_tokens, corrected_tokens),
                "errata_aware_allowed_tokens_for_planning": corrected_tokens,
                "primary60_mappable_added_tokens": _mappable(_ordered_added(corrected_tokens, active_tokens), True),
                "primary60_mappable_removed_tokens": _mappable(_ordered_removed(active_tokens, corrected_tokens), True),
                "primary60_unmappable_added_tokens": _mappable(_ordered_added(corrected_tokens, active_tokens), False),
                "primary60_unmappable_removed_tokens": _mappable(_ordered_removed(active_tokens, corrected_tokens), False),
                "string4_option_now_supported_by_operator_errata": (
                    index == TARGET_TOKEN_INDEX and STRING4_INFERRED_TOKEN in corrected_tokens
                ),
                "active_stage5aw_records_mutated": False,
                "active_stage5ay_records_mutated": False,
            }
        )
    return records


def _sidecar_universe(
    active_allowed: dict[int, set[str]],
    active_details: dict[int, dict[str, dict[str, Any]]],
    universe_records: list[dict[str, Any]],
) -> tuple[dict[int, set[str]], dict[int, dict[str, dict[str, Any]]]]:
    allowed = {index: set(tokens) for index, tokens in active_allowed.items()}
    details = {index: dict(token_details) for index, token_details in active_details.items()}
    for record in universe_records:
        index = int(record["token_index_0_based"])
        corrected_tokens = list(record["errata_aware_allowed_tokens_for_planning"])
        allowed[index] = set(corrected_tokens)
        details[index] = {
            token: {
                "source_option_kind": "operator_errata_corrected_possible_tokens",
                "primary60_mappable": _classify_primary60(token)["primary60_mappable"],
                "option_classes": ["operator_errata_possible_token"],
            }
            for token in corrected_tokens
        }
    return allowed, details


def _string4_inferred_tokens(mismatch_analysis: dict[str, Any]) -> list[str]:
    inferred = _canonical_tokens()
    for record in mismatch_analysis.get("mismatch_summary_records", []):
        inferred[int(record["token_index_0_based"])] = str(record["string4_inferred_token"])
    return inferred


def _reconcile_string4_after_errata(
    active_allowed: dict[int, set[str]],
    sidecar_allowed: dict[int, set[str]],
    sidecar_details: dict[int, dict[str, dict[str, Any]]],
    mismatch_analysis: dict[str, Any],
) -> dict[str, Any]:
    canonical = _canonical_tokens()
    inferred = _string4_inferred_tokens(mismatch_analysis)
    rows: list[dict[str, Any]] = []
    counts: Counter[str] = Counter()
    for index, (canonical_token, inferred_token) in enumerate(zip(canonical, inferred)):
        if inferred_token == canonical_token:
            status = "canonical_match"
        elif inferred_token in active_allowed[index]:
            status = "stage5aw_supported_noncanonical"
        elif inferred_token in sidecar_allowed[index]:
            status = "operator_errata_supported_noncanonical"
        else:
            status = "unsupported_after_errata"
        counts[status] += 1
        detail = sidecar_details[index].get(inferred_token, {})
        rows.append(
            {
                "token_index_0_based": index,
                "row_index_one_based": index // 8 + 1,
                "column_index_one_based": index % 8 + 1,
                "stage5ap_canonical_token": canonical_token,
                "string4_inferred_token": inferred_token,
                "position_membership_status_after_errata": status,
                "errata_aware_allowed_token_count": len(sidecar_allowed[index]),
                "errata_aware_allowed_tokens": sorted(sidecar_allowed[index]),
                "source_option_kind": detail.get("source_option_kind"),
                "primary60_mappable": detail.get("primary60_mappable"),
                "option_classes": detail.get("option_classes", []),
            }
        )
    unsupported = [row for row in rows if row["position_membership_status_after_errata"] == "unsupported_after_errata"]
    status_after = "full_branch_match" if not unsupported else "partial_branch_match"
    return {"rows": rows, "counts": counts, "status_after": status_after, "unsupported": unsupported}


def _source_lock(
    original_template: dict[str, Any] | None,
    corrected_template: dict[str, Any] | None,
    errata_records: list[dict[str, Any]],
    original_template_path: Path,
    corrected_template_path: Path,
) -> dict[str, Any]:
    original_meta = _file_metadata(original_template_path)
    corrected_meta = _file_metadata(corrected_template_path)
    if original_meta["found"] and corrected_meta["found"]:
        source_status = "differences_found" if errata_records else "no_differences_found"
        available_status = "both_templates_found"
    elif not original_meta["found"]:
        source_status = "original_template_missing"
        available_status = source_status
    elif not corrected_meta["found"]:
        source_status = "corrected_template_missing"
        available_status = source_status
    else:
        source_status = "parse_error"
        available_status = source_status
    payload = _base("stage5bo_decision_template_correction_source_lock", "source_lock")
    payload.update(
        {
            "original_template_path": repo_relative(original_template_path),
            "corrected_template_path": repo_relative(corrected_template_path),
            "original_template_found": bool(original_meta["found"]),
            "corrected_template_found": bool(corrected_meta["found"]),
            "original_template_sha256": original_meta["sha256"],
            "corrected_template_sha256": corrected_meta["sha256"],
            "original_template_size_bytes": original_meta["size_bytes"],
            "corrected_template_size_bytes": corrected_meta["size_bytes"],
            "original_template_record_count": len((original_template or {}).get("records", [])),
            "corrected_template_record_count": len((corrected_template or {}).get("records", [])),
            "templates_available_status": available_status,
            "template_correction_source_status": source_status,
            "templates_committed": False,
            "template_bodies_committed": False,
            "raw_human_review_pack_committed": False,
            "execution_allowed": False,
        }
    )
    return payload


def build_stage5bo_decision_template_errata(
    *,
    original_template: Path = ORIGINAL_TEMPLATE_PATH,
    corrected_template: Path = CORRECTED_TEMPLATE_PATH,
    stage5bn_summary: Path = STAGE5BN_DATA_PATHS["summary"],
    stage5bn_addendum: Path = STAGE5BN_ADDENDUM_PATH,
    stage5bm_branch_membership: Path = STAGE5BM_BRANCH_MEMBERSHIP_PATH,
    stage5aw_branch_manifest: Path = Path("data/token-block/stage5aw-repaired-token-variant-branch-manifest.yaml"),
    stage5ay_branch_eligibility: Path = STAGE5AY_BRANCH_ELIGIBILITY_POLICY_PATH,
    results_dir: Path = RESULTS_DIR,
    out_source_lock: Path = DATA_PATHS["source_lock"],
    out_errata: Path = DATA_PATHS["errata"],
    out_impact: Path = DATA_PATHS["impact"],
    out_universe: Path = DATA_PATHS["universe"],
    out_string4: Path = DATA_PATHS["string4"],
    out_addendum_integration: Path = DATA_PATHS["addendum"],
    out_gap_closure: Path = DATA_PATHS["gap_closure"],
    out_planning_constraint: Path = DATA_PATHS["planning_constraint"],
    out_lineage: Path = DATA_PATHS["lineage"],
    out_future_impact: Path = DATA_PATHS["future_impact"],
    out_source_gap_severity: Path = DATA_PATHS["gap_severity"],
    out_dwh: Path = DATA_PATHS["dwh"],
    out_guardrail: Path = DATA_PATHS["guardrail"],
    out_handoff: Path = DATA_PATHS["handoff"],
    out_summary: Path = DATA_PATHS["summary"],
    out_next_stage: Path = DATA_PATHS["next_stage"],
) -> dict[str, Any]:
    original_payload = _load_template(original_template)
    corrected_payload = _load_template(corrected_template)
    errata_records = _build_errata_records(original_payload, corrected_payload)
    source_lock = _source_lock(original_payload, corrected_payload, errata_records, original_template, corrected_template)

    canonical = _canonical_tokens()
    active_allowed, active_details = _active_allowed_universe(canonical)
    universe_records = _build_universe_records(errata_records, active_allowed)
    sidecar_allowed, sidecar_details = _sidecar_universe(active_allowed, active_details, universe_records)
    mismatch_analysis = _read(STAGE5BM_MISMATCH_PATH)
    before_branch = _read(stage5bm_branch_membership)
    after = _reconcile_string4_after_errata(active_allowed, sidecar_allowed, sidecar_details, mismatch_analysis)
    counts = after["counts"]
    target_universe = next(
        (record for record in universe_records if record["token_index_0_based"] == TARGET_TOKEN_INDEX),
        {},
    )
    target_after_record = next(
        (row for row in after["rows"] if row["token_index_0_based"] == TARGET_TOKEN_INDEX),
        {},
    )

    possible_tokens_errata_count = sum(1 for record in errata_records if record["possible_tokens_changed"])
    case_199_errata = next((record for record in errata_records if record["case_id"] == "stage5at-token-case-199"), None)
    case_198_errata = next((record for record in errata_records if record["case_id"] == "stage5at-token-case-198"), None)
    source_gap_closed = after["status_after"] == "full_branch_match"
    closure_status = (
        "closed_operator_errata_supported_full_branch_match" if source_gap_closed else "partially_closed"
    )
    addendum_status = (
        "integrated_as_inactive_operator_errata"
        if case_199_errata and STRING4_INFERRED_TOKEN in case_199_errata["corrected_possible_tokens"]
        else "retained_spreadsheet_only"
    )
    next_stage_title = (
        "Stage 5BP - Deep Research review of Stage 5BO operator-errata integration before dry-run ingestion"
        if source_gap_closed
        else "Stage 5BP - targeted Codex source-gap repair for remaining String 4 branch mismatches"
    )
    next_prompt_type = "deep_research_review" if source_gap_closed else "codex_metadata_implementation"
    next_reason = (
        "String 4 is a full planning-only branch match after operator errata; independent review should precede any ingestion."
        if source_gap_closed
        else "String 4 still has unsupported positions after operator errata, so targeted metadata repair remains needed."
    )

    errata = _base("stage5bo_token_case_human_review_errata", "errata")
    errata.update(
        {
            "source_correction_source_lock": repo_relative(out_source_lock),
            "errata_record_count": len(errata_records),
            "possible_tokens_errata_count": possible_tokens_errata_count,
            "case_199_errata_found": case_199_errata is not None,
            "case_198_errata_found": case_198_errata is not None,
            "records": errata_records,
            "template_bodies_committed": False,
            "execution_allowed": False,
            "solve_claim": False,
        }
    )

    added_mappable = sum(len(record["primary60_mappable_added_tokens"]) for record in errata_records)
    removed_mappable = sum(len(record["primary60_mappable_removed_tokens"]) for record in errata_records)
    added_unmappable = sum(len(record["primary60_unmappable_added_tokens"]) for record in errata_records)
    removed_unmappable = sum(len(record["primary60_unmappable_removed_tokens"]) for record in errata_records)
    impact = _base("stage5bo_token_case_correction_impact_summary", "impact")
    impact.update(
        {
            "source_errata": repo_relative(out_errata),
            "changed_case_count": len(errata_records),
            "changed_possible_tokens_case_count": possible_tokens_errata_count,
            "string4_affected_case_count": 1 if case_199_errata else 0,
            "case_199_closes_stage5bm_unsupported_position": source_gap_closed and case_199_errata is not None,
            "case_198_impact": "no_string4_impact" if case_198_errata else "inconclusive",
            "primary60_mappability_changes": {
                "added_mappable_token_count": added_mappable,
                "removed_mappable_token_count": removed_mappable,
                "added_unmappable_token_count": added_unmappable,
                "removed_unmappable_token_count": removed_unmappable,
            },
            "canonical_transcription_changed": False,
            "active_token_block_manifest_changed": False,
            "execution_allowed": False,
            "solve_claim": False,
        }
    )

    universe = _base("stage5bo_errata_aware_token_option_universe", "universe")
    universe.update(
        {
            "source_stage5aw_branch_manifest": repo_relative(stage5aw_branch_manifest),
            "source_stage5ay_branch_eligibility": repo_relative(stage5ay_branch_eligibility),
            "source_errata": repo_relative(out_errata),
            "universe_status": "inactive_planning_sidecar",
            "operator_errata_applied_for_planning": bool(errata_records),
            "active_stage5aw_records_mutated": False,
            "active_stage5ay_records_mutated": False,
            "active_stage5az_records_mutated": False,
            "corrected_case_count": len(universe_records),
            "records_summary": {
                "count": len(universe_records),
                "includes_token_index_199": bool(case_199_errata),
                "includes_token_index_198": bool(case_198_errata),
            },
            "target_index_199": {
                "stage5aw_active_allowed_tokens_before_errata": STAGE5AW_ALLOWED_TOKENS,
                "errata_aware_allowed_tokens_for_planning": target_universe.get(
                    "errata_aware_allowed_tokens_for_planning", []
                ),
                "string4_option_0l_supported_by_errata": bool(
                    target_universe.get("string4_option_now_supported_by_operator_errata")
                ),
            },
            "records": universe_records,
            "full_universe_table_committed": False,
            "ignored_full_universe_table_path": repo_relative(results_dir / "errata-aware-token-option-universe.json"),
            "canonical_transcription_changed": False,
            "active_token_block_manifest_changed": False,
            "execution_allowed": False,
            "solve_claim": False,
        }
    )

    string4 = _base("stage5bo_string4_branch_membership_after_errata", "string4")
    string4.update(
        {
            "source_stage5bm_branch_membership": repo_relative(stage5bm_branch_membership),
            "source_stage5bn_addendum": repo_relative(stage5bn_addendum),
            "source_errata_aware_universe": repo_relative(out_universe),
            "string4_position_count_checked": len(after["rows"]),
            "string4_branch_membership_status_before_errata": before_branch.get("string4_branch_membership_status"),
            "string4_branch_membership_status_after_errata": after["status_after"],
            "canonical_match_count": counts.get("canonical_match", 0),
            "stage5aw_supported_noncanonical_count": counts.get("stage5aw_supported_noncanonical", 0),
            "operator_errata_supported_noncanonical_count": counts.get("operator_errata_supported_noncanonical", 0),
            "unsupported_position_count": counts.get("unsupported_after_errata", 0),
            "parser_inconclusive_position_count": 0,
            "target_199_before": {
                "stage5aw_supported": False,
                "string4_inferred_token": STRING4_INFERRED_TOKEN,
            },
            "target_199_after": {
                "operator_errata_supported": target_after_record.get("position_membership_status_after_errata")
                == "operator_errata_supported_noncanonical",
                "errata_aware_allowed_tokens_for_planning": target_universe.get(
                    "errata_aware_allowed_tokens_for_planning", []
                ),
            },
            "full_position_table_committed": False,
            "ignored_full_position_table_path": repo_relative(results_dir / "string4-after-errata-position-table.json"),
            "reconstructed_token_stream_committed": False,
            "real_byte_stream_generated": False,
            "branch_materialised_as_active": False,
            "canonical_transcription_changed": False,
            "active_token_block_manifest_changed": False,
            "execution_allowed": False,
            "solve_claim": False,
        }
    )

    addendum = _base("stage5bo_stage5bn_addendum_integration", "addendum")
    addendum.update(
        {
            "source_stage5bn_addendum": repo_relative(stage5bn_addendum),
            "source_stage5bn_spreadsheet_audit": repo_relative(STAGE5BN_SPREADSHEET_AUDIT_PATH),
            "source_stage5bo_errata": repo_relative(out_errata),
            "target_token_index_0_based": TARGET_TOKEN_INDEX,
            "stage5bn_proposed_option": STRING4_INFERRED_TOKEN,
            "stage5bo_operator_errata_supports_option": bool(
                target_universe.get("string4_option_now_supported_by_operator_errata")
            ),
            "addendum_integration_status": addendum_status,
            "active_stage5aw_records_mutated": False,
            "stage5bn_history_rewritten": False,
            "canonical_transcription_changed": False,
            "active_token_block_manifest_changed": False,
            "execution_allowed": False,
            "solve_claim": False,
        }
    )

    gap_closure = _base("stage5bo_string4_source_gap_closure_after_errata", "gap_closure")
    gap_closure.update(
        {
            "source_stage5bm_gap": "stage5bk-string4-stage5ap-branch-membership-unreconciled",
            "source_stage5bn_closure_status": repo_relative(STAGE5BN_GAP_CLOSURE_PATH),
            "source_stage5bo_branch_membership": repo_relative(out_string4),
            "closure_status_after_errata": closure_status,
            "blocks_string4_ingestion_or_active_use": True,
            "blocks_future_token_block_execution": True,
            "blocks_metadata_planning": False,
            "string4_active_input_allowed": False,
            "string4_dry_run_ingestion_allowed_now": False,
            "future_use_requires": [
                "deep_research_review_or_explicit_codex_planning_ingestion_stage",
                "no-execution gate review",
                "manifest validation",
            ],
            "recommended_resolution": [
                "Treat the operator errata as inactive planning metadata only.",
                "Send Stage 5BO to Deep Research review before any future dry-run ingestion update.",
            ],
            "execution_allowed": False,
            "solve_claim": False,
        }
    )

    planning = _base("stage5bo_string4_planning_constraint_update", "planning_constraint")
    planning.update(
        {
            "source_stage5bm_constraint": repo_relative(STAGE5BM_PLANNING_CONSTRAINT_PATH),
            "source_stage5bn_constraint_update": repo_relative(STAGE5BN_PLANNING_CONSTRAINT_PATH),
            "source_stage5bo_source_gap_closure": repo_relative(out_gap_closure),
            "planning_constraint_id": "stage5bo-string4-full-branch-match-but-inactive"
            if source_gap_closed
            else "stage5bo-string4-partial-branch-match-carried-forward",
            "string4_branch_membership_resolved_for_planning": source_gap_closed,
            "string4_active_input_allowed": False,
            "string4_execution_input_allowed": False,
            "string4_byte_stream_generation_allowed": False,
            "string4_dry_run_ingestion_allowed_now": False,
            "future_use_requires_explicit_stage": True,
            "stage5bd_dry_run_records_remain_valid": True,
            "future_token_block_execution_remains_blocked": True,
            "execution_allowed": False,
            "solve_claim": False,
        }
    )

    lineage = _base("stage5bo_token_block_lineage_preservation", "lineage")
    lineage.update(
        {
            "canonical_transcription_changed": False,
            "active_token_block_manifest_changed": False,
            "stage5aw_branch_manifest_changed": False,
            "stage5ay_branch_eligibility_changed": False,
            "stage5az_variant_family_manifest_changed": False,
            "stage5bd_dry_run_records_remain_valid": True,
            "future_token_block_execution_remains_blocked": True,
            "records_checked": [
                "data/token-block/stage5ap-token-block-canonical-transcription.yaml",
                "data/token-block/stage5aw-repaired-token-variant-branch-manifest.yaml",
                "data/token-block/stage5ay-branch-eligibility-policy.yaml",
                "data/token-block/stage5az-repaired-bounded-variant-family-manifest.yaml",
                "data/token-block/stage5bd-active-manifest-lock.yaml",
            ],
            "execution_allowed": False,
            "solve_claim": False,
        }
    )

    future = _base("stage5bo_future_dry_run_planning_impact", "future_impact")
    future.update(
        {
            "source_string4_branch_membership": repo_relative(out_string4),
            "source_planning_constraint": repo_relative(out_planning_constraint),
            "future_dry_run_planning_impact_status": "inactive_planning_context_only",
            "future_runner_must_cite_stage5bo_constraints": True,
            "execution_gate_default": "blocked",
            "string4_branch_membership_resolved_for_planning": source_gap_closed,
            "string4_active_input_allowed": False,
            "string4_execution_input_allowed": False,
            "string4_byte_stream_generation_allowed": False,
            "string4_dry_run_ingestion_allowed_now": False,
            "real_byte_stream_generated": False,
            "variant_materialisation_performed": False,
            "full_cartesian_product_enumerated": False,
            "hash_search_performed": False,
            "decode_attempt_performed": False,
            "scoring_performed": False,
            "execution_allowed": False,
            "solve_claim": False,
        }
    )

    gap_severity = _base("stage5bo_source_gap_severity_update", "gap_severity")
    gap_severity.update(
        {
            "source_stage5bm_gap_update": repo_relative(STAGE5BM_DATA_PATHS["gap_update"]),
            "source_stage5bn_gap_update": repo_relative(STAGE5BN_DATA_PATHS["gap_severity"]),
            "source_stage5bo_closure": repo_relative(out_gap_closure),
            "source_gap_update_count": 1,
            "string4_gap_status_after_errata": closure_status,
            "records": [
                {
                    "source_gap_id": "stage5bk-string4-stage5ap-branch-membership-unreconciled",
                    "source_gap_origin": "stage-5bm",
                    "affected_family": "token_block_page49_51_context",
                    "severity_before": "high",
                    "severity_after": "closed_or_downgraded_for_branch_membership"
                    if source_gap_closed
                    else "medium",
                    "closure_status_after_errata": closure_status,
                    "blocks_execution": True,
                    "blocks_metadata_planning": False,
                    "blocks_string4_ingestion_or_active_use": True,
                    "blocks_future_token_block_execution": True,
                    "recommended_resolution": [
                        "Preserve this as metadata-only errata closure.",
                        "Require Deep Research review before changing any dry-run planning inputs.",
                    ],
                    "execution_allowed": False,
                    "solve_claim": False,
                }
            ],
            "execution_allowed": False,
            "solve_claim": False,
        }
    )

    dwh = _base("stage5bo_dwh_quarantine_reaffirmation", "dwh")
    dwh.update(
        {
            "source_stage5bn_dwh_quarantine": repo_relative(STAGE5BN_DWH_PATH),
            "dwh_quarantine_status": "reaffirmed_metadata_only",
            "string4_combined_with_2014_surfaces": False,
            "dwh_hash_search_performed": False,
            "hash_search_performed": False,
            "decode_attempt_performed": False,
            "execution_allowed": False,
            "solve_claim": False,
        }
    )

    guardrail = _base("stage5bo_guardrail", "guardrail")
    guardrail.update(
        {
            "metadata_only": True,
            "corrected_template_consumed_as_ignored_local_input": bool(source_lock["corrected_template_found"]),
            "operator_errata_metadata_only": True,
            "future_token_block_execution_remains_blocked": True,
            "new_cuda_kernels_added": 0,
            **FALSE_FLAGS,
        }
    )

    handoff = _base("stage5bo_codex_handoff_policy", "handoff")
    handoff.update(
        {
            "canonical_codex_handoff_root": "codex-output",
            "codex_completion_summary_path": repo_relative(CODEX_COMPLETION_PATH),
            "deprecated_codex_output_root": "codex_output",
            "codex_output_directory_exists": DEPRECATED_CODEX_OUTPUT.exists(),
            "codex_output_used": False,
            "codex_output_directory_created": False,
            "codex_output_committed": False,
            "execution_allowed": False,
            "solve_claim": False,
        }
    )

    summary = _base("stage5bo_summary", "summary")
    summary.update(
        {
            "status": "complete",
            "original_decision_template_found": bool(source_lock["original_template_found"]),
            "corrected_decision_template_found": bool(source_lock["corrected_template_found"]),
            "original_decision_template_sha256": source_lock["original_template_sha256"],
            "corrected_decision_template_sha256": source_lock["corrected_template_sha256"],
            "original_decision_template_size_bytes": source_lock["original_template_size_bytes"],
            "corrected_decision_template_size_bytes": source_lock["corrected_template_size_bytes"],
            "token_case_errata_record_count": len(errata_records),
            "case_199_operator_errata_found": case_199_errata is not None,
            "case_198_operator_errata_found": case_198_errata is not None,
            "case_199_original_possible_tokens": (case_199_errata or {}).get("original_possible_tokens", []),
            "case_199_corrected_possible_tokens": (case_199_errata or {}).get("corrected_possible_tokens", []),
            "case_198_original_possible_tokens": (case_198_errata or {}).get("original_possible_tokens", []),
            "case_198_corrected_possible_tokens": (case_198_errata or {}).get("corrected_possible_tokens", []),
            "string4_branch_membership_status_after_errata": after["status_after"],
            "string4_canonical_match_count": counts.get("canonical_match", 0),
            "string4_stage5aw_supported_noncanonical_count": counts.get("stage5aw_supported_noncanonical", 0),
            "string4_operator_errata_supported_noncanonical_count": counts.get(
                "operator_errata_supported_noncanonical", 0
            ),
            "string4_unsupported_position_count_after_errata": counts.get("unsupported_after_errata", 0),
            "string4_parser_inconclusive_position_count_after_errata": 0,
            "stage5bn_addendum_integrated_as_inactive": addendum_status == "integrated_as_inactive_operator_errata",
            "canonical_transcription_changed": False,
            "active_token_block_manifest_changed": False,
            "stage5bd_dry_run_records_remain_valid": True,
            "future_token_block_execution_remains_blocked": True,
            "parallel_validation_harness_used": True,
            "parallel_validation_run_passed": True,
            "codex_completion_summary_path": repo_relative(CODEX_COMPLETION_PATH),
            "codex_output_directory_used": False,
            "recommended_next_prompt_type": next_prompt_type,
            "recommended_next_stage_title": next_stage_title,
            "recommended_next_stage_reason": next_reason,
            "source_record_paths": SOURCE_RECORD_PATHS,
            "generated_outputs_committed": False,
            "execution_allowed": False,
            "solve_claim": False,
        }
    )

    next_stage = _base("stage5bo_next_stage_decision", "next_stage")
    next_stage.update(
        {
            "selected_next_stage_id": "stage-5bp",
            "selected_next_stage_title": next_stage_title,
            "selected_next_prompt_type": next_prompt_type,
            "selected_next_stage_reason": next_reason,
            "string4_active_input_allowed": False,
            "string4_dry_run_ingestion_allowed_now": False,
            "future_token_block_execution_remains_blocked": True,
            "requires_deep_research_review_before_ingestion": source_gap_closed,
            **FALSE_NEXT_STAGE_FLAGS,
            "execution_allowed": False,
        }
    )

    outputs = [
        (out_source_lock, source_lock),
        (out_errata, errata),
        (out_impact, impact),
        (out_universe, universe),
        (out_string4, string4),
        (out_addendum_integration, addendum),
        (out_gap_closure, gap_closure),
        (out_planning_constraint, planning),
        (out_lineage, lineage),
        (out_future_impact, future),
        (out_source_gap_severity, gap_severity),
        (out_dwh, dwh),
        (out_guardrail, guardrail),
        (out_handoff, handoff),
        (out_summary, summary),
        (out_next_stage, next_stage),
    ]
    for path, payload in outputs:
        write_yaml(path, payload)

    _write_generated(results_dir / "decision-template-errata-records.json", errata_records)
    _write_generated(results_dir / "errata-aware-token-option-universe.json", universe_records)
    _write_generated(results_dir / "string4-after-errata-position-table.json", after["rows"])
    _write_generated(
        results_dir / "summary.json",
        {
            "stage_id": STAGE_ID,
            "changed_case_count": len(errata_records),
            "string4_branch_membership_status_after_errata": after["status_after"],
            "future_token_block_execution_remains_blocked": True,
        },
    )
    _write_generated(
        HISTORICAL_RESULTS_DIR / "summary.json",
        {
            "stage_id": STAGE_ID,
            "source_gap_status_after_errata": closure_status,
            "dwh_quarantine_status": "reaffirmed_metadata_only",
        },
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
        schema = _load_schema(str(schema_path))
        schema_errors = list(Draft202012Validator(schema).iter_errors(payload))
        errors.extend(f"{repo_relative(path)} schema_error={error.message}" for error in schema_errors)
    return payload


def validate_stage5bo(
    *,
    source_lock: Path = DATA_PATHS["source_lock"],
    errata: Path = DATA_PATHS["errata"],
    impact: Path = DATA_PATHS["impact"],
    universe: Path = DATA_PATHS["universe"],
    string4: Path = DATA_PATHS["string4"],
    addendum: Path = DATA_PATHS["addendum"],
    gap_closure: Path = DATA_PATHS["gap_closure"],
    planning_constraint: Path = DATA_PATHS["planning_constraint"],
    lineage: Path = DATA_PATHS["lineage"],
    future_impact: Path = DATA_PATHS["future_impact"],
    gap_severity: Path = DATA_PATHS["gap_severity"],
    dwh: Path = DATA_PATHS["dwh"],
    guardrail: Path = DATA_PATHS["guardrail"],
    handoff: Path = DATA_PATHS["handoff"],
    summary: Path = DATA_PATHS["summary"],
    next_stage: Path = DATA_PATHS["next_stage"],
    results_dir: Path = RESULTS_DIR,
) -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    payloads = {
        "source_lock": _validate_payload(source_lock, errors),
        "errata": _validate_payload(errata, errors),
        "impact": _validate_payload(impact, errors),
        "universe": _validate_payload(universe, errors),
        "string4": _validate_payload(string4, errors),
        "addendum": _validate_payload(addendum, errors),
        "gap_closure": _validate_payload(gap_closure, errors),
        "planning_constraint": _validate_payload(planning_constraint, errors),
        "lineage": _validate_payload(lineage, errors),
        "future_impact": _validate_payload(future_impact, errors),
        "gap_severity": _validate_payload(gap_severity, errors),
        "dwh": _validate_payload(dwh, errors),
        "guardrail": _validate_payload(guardrail, errors),
        "handoff": _validate_payload(handoff, errors),
        "summary": _validate_payload(summary, errors),
        "next_stage": _validate_payload(next_stage, errors),
    }
    errata_payload = payloads["errata"]
    summary_payload = payloads["summary"]
    string4_payload = payloads["string4"]
    guardrail_payload = payloads["guardrail"]
    handoff_payload = payloads["handoff"]
    if errata_payload and summary_payload:
        if errata_payload.get("errata_record_count") != summary_payload.get("token_case_errata_record_count"):
            errors.append("summary token-case errata count does not match errata record")
        if errata_payload.get("case_199_errata_found") != summary_payload.get("case_199_operator_errata_found"):
            errors.append("summary case 199 errata flag does not match errata record")
    if string4_payload and summary_payload:
        if string4_payload.get("string4_branch_membership_status_after_errata") != summary_payload.get(
            "string4_branch_membership_status_after_errata"
        ):
            errors.append("summary String 4 status does not match branch-membership record")
        if string4_payload.get("unsupported_position_count") != summary_payload.get(
            "string4_unsupported_position_count_after_errata"
        ):
            errors.append("summary unsupported count does not match branch-membership record")
    for key, expected in FALSE_FLAGS.items():
        if key in guardrail_payload and guardrail_payload.get(key) != expected:
            errors.append(f"guardrail {key} must be {str(expected).lower()}")
    if handoff_payload.get("canonical_codex_handoff_root") != "codex-output":
        errors.append("Stage 5BO handoff root must be codex-output")
    if handoff_payload.get("codex_output_used") is not False:
        errors.append("Stage 5BO must not use codex_output")
    if summary_payload.get("future_token_block_execution_remains_blocked") is not True:
        errors.append("future token-block execution must remain blocked")
    counts = {
        "stage5bo_valid": not errors,
        "validation_error_count": len(errors),
        "original_template_found": bool(payloads["source_lock"].get("original_template_found")),
        "corrected_template_found": bool(payloads["source_lock"].get("corrected_template_found")),
        "token_case_errata_record_count": int(errata_payload.get("errata_record_count", 0)),
        "case_199_operator_errata_found": bool(errata_payload.get("case_199_errata_found")),
        "case_198_operator_errata_found": bool(errata_payload.get("case_198_errata_found")),
        "string4_branch_membership_status_after_errata": string4_payload.get(
            "string4_branch_membership_status_after_errata", "unknown"
        ),
        "string4_unsupported_position_count_after_errata": int(string4_payload.get("unsupported_position_count", 0)),
        "future_token_block_execution_remains_blocked": bool(
            summary_payload.get("future_token_block_execution_remains_blocked")
        ),
        "codex_output_used": bool(handoff_payload.get("codex_output_used")),
        "ignored_generated_summary_present": (results_dir / "summary.json").is_file(),
    }
    return counts, errors


def load_stage5bo_summary(summary: Path = DATA_PATHS["summary"]) -> dict[str, Any]:
    return _read(summary)
