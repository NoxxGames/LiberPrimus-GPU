"""Stage 5AW possible-token parser repair helpers."""

from __future__ import annotations

import math
from pathlib import Path
from typing import Any

import yaml

from .models import (
    ALPHABET_PATH,
    MAPPING_PATH,
    PRIMARY_ALPHABET,
    STAGE5AU_CASE_CHALLENGES_V2_PATH,
    STAGE5AV_BRANCH_MANIFEST_PATH,
    STAGE5AV_ID,
    STAGE5AV_LOCAL_DECISION_TEMPLATE_PATH,
    STAGE5AV_REVIEWER_EXTRA_TOKENS_PATH,
    STAGE5AW_CANONICAL_UPDATE_PATH,
    STAGE5AW_DECISION_PARSER_AUDIT_PATH,
    STAGE5AW_DWH_CONTEXT_PATH,
    STAGE5AW_GUARDRAIL_PATH,
    STAGE5AW_ID,
    STAGE5AW_MALFORMED_FRAGMENTS_PATH,
    STAGE5AW_NEXT_STAGE_DECISION_PATH,
    STAGE5AW_NULL_CONTROL_UPDATE_PATH,
    STAGE5AW_PARSER_POLICY_PATH,
    STAGE5AW_REPAIRED_BRANCH_MANIFEST_PATH,
    STAGE5AW_REPAIRED_HUMAN_REVIEW_DECISIONS_PATH,
    STAGE5AW_REPAIRED_PRIMARY60_IMPACT_PATH,
    STAGE5AW_REPAIRED_REVIEWER_EXTRA_TOKENS_PATH,
    STAGE5AW_REPAIRED_UNRESOLVED_VARIANTS_PATH,
    STAGE5AW_RESULTS_DIR,
    STAGE5AW_SUMMARY_PATH,
    TOKEN_BLOCK_ID,
    TRANSCRIPTION_PATH,
    read_yaml,
    repo_relative,
    sha256_file,
    write_json,
    write_yaml,
)
from .possible_token_parser import parse_possible_token_notes
from .stage5av import (
    COMPACT_MANIFEST_MAX_BRANCHES,
    FULL_ENUMERATION_MAX_BRANCHES,
    PRIMARY60_ALPHABET_ID,
)

AUDIT_TARGET_IDS = [
    "stage5at-token-case-013",
    "stage5at-token-case-025",
    "stage5at-token-case-164",
    "stage5at-token-case-165",
    "stage5at-token-case-175",
    "stage5at-token-case-186",
    "stage5at-token-case-198",
    "stage5at-token-case-199",
]
SOURCE_STAGE5AV_COMMIT = "023e10c2a283c1fc01df215908d6c0744700c515"


def _ensure_results_dir(results_dir: Path) -> None:
    results_dir.mkdir(parents=True, exist_ok=True)
    gitkeep = results_dir / ".gitkeep"
    if not gitkeep.exists():
        gitkeep.write_text("", encoding="utf-8")


def _safe_text(value: Any) -> str | None:
    if value is None:
        return None
    return str(value)


def _safe_token_list(values: Any) -> list[str]:
    if not isinstance(values, list):
        return []
    return [str(value) for value in values]


def _dedupe_ordered(values: list[str]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for value in values:
        if value not in seen:
            seen.add(value)
            out.append(value)
    return out


def _load_decision_file(path: Path) -> dict[str, Any]:
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def _challenge_index(path: Path) -> dict[str, dict[str, Any]]:
    payload = read_yaml(path)
    records = payload.get("records", []) if isinstance(payload, dict) else []
    return {str(record.get("challenge_id")): record for record in records}


def _is_prose_token(value: str) -> bool:
    return len(value) != 2 or any(char.isspace() for char in value)


def _classify_primary60(token: str | None) -> dict[str, Any]:
    if token is None:
        return {
            "primary60_status": "missing_token",
            "primary60_mappable": False,
            "primary60_value": None,
            "primary60_error": "missing_token",
            "variant_byte_stream_eligible": False,
        }
    if "?" in token:
        return {
            "primary60_status": "visual_placeholder_unmappable",
            "primary60_mappable": False,
            "primary60_value": None,
            "primary60_error": "visual_placeholder_unmappable",
            "variant_byte_stream_eligible": False,
        }
    if len(token) != 2:
        return {
            "primary60_status": "unmappable_primary_60",
            "primary60_mappable": False,
            "primary60_value": None,
            "primary60_error": "token_length_not_2",
            "variant_byte_stream_eligible": False,
        }
    first, suffix = token[0], token[1]
    if first not in "01234":
        return {
            "primary60_status": "unmappable_primary_60",
            "primary60_mappable": False,
            "primary60_value": None,
            "primary60_error": "first_symbol_not_in_0_to_4",
            "variant_byte_stream_eligible": False,
        }
    if suffix not in PRIMARY_ALPHABET:
        return {
            "primary60_status": "unmappable_primary_60",
            "primary60_mappable": False,
            "primary60_value": None,
            "primary60_error": "suffix_not_in_primary_60_alphabet",
            "variant_byte_stream_eligible": False,
        }
    return {
        "primary60_status": "mapped_primary_60",
        "primary60_mappable": True,
        "primary60_value": int(first) * 60 + PRIMARY_ALPHABET.index(suffix),
        "primary60_error": None,
        "variant_byte_stream_eligible": True,
    }


def _possible_token_details(
    possible_tokens: list[str],
    canonical_token: str,
    candidate_tokens: list[str],
) -> list[dict[str, Any]]:
    candidate_set = set(candidate_tokens)
    details: list[dict[str, Any]] = []
    for token in possible_tokens:
        if "?" in token:
            source = "visual_placeholder_from_reviewer_notes"
        elif token == canonical_token:
            source = "current_canonical_token"
        elif token in candidate_set:
            source = "generated_candidate_token"
        else:
            source = "reviewer_extra_possible_token"
        primary60 = _classify_primary60(token)
        details.append(
            {
                "token": token,
                "possible_token_source": source,
                "primary60_alphabet_id": PRIMARY60_ALPHABET_ID,
                **primary60,
            }
        )
    return details


def _branch_product(records: list[dict[str, Any]], key: str) -> int:
    product = 1
    for record in records:
        product *= max(int(record.get(key, 0)), 1)
    return product


def _log10_int(value: int) -> float:
    return 0.0 if value <= 1 else round(math.log10(value), 6)


def audit_stage5aw_decision_parser(
    decision_file: Path = STAGE5AV_LOCAL_DECISION_TEMPLATE_PATH,
    stage5av_extras: Path = STAGE5AV_REVIEWER_EXTRA_TOKENS_PATH,
    stage5av_branch_manifest: Path = STAGE5AV_BRANCH_MANIFEST_PATH,
    results_dir: Path = STAGE5AW_RESULTS_DIR,
    out_audit: Path = STAGE5AW_DECISION_PARSER_AUDIT_PATH,
    out_policy: Path = STAGE5AW_PARSER_POLICY_PATH,
) -> tuple[dict[str, Any], dict[str, Any]]:
    _ensure_results_dir(results_dir)
    extras_payload = read_yaml(stage5av_extras)
    manifest_payload = read_yaml(stage5av_branch_manifest)
    original_extras = extras_payload.get("records", [])
    malformed_stage5av_records = [
        {
            "challenge_id": record.get("challenge_id"),
            "token_index_0_based": record.get("token_index_0_based"),
            "raw_reviewer_extra_possible_token": record.get("reviewer_extra_possible_token"),
            "malformation_reason": "prose_fragment_or_non_two_character_token",
        }
        for record in original_extras
        if _is_prose_token(str(record.get("reviewer_extra_possible_token", "")))
    ]
    audit = {
        "record_type": "decision_parser_audit",
        "schema": "schemas/token-block/decision-parser-audit-v0.schema.json",
        "stage_id": STAGE5AW_ID,
        "source_stage_id": STAGE5AV_ID,
        "source_stage5av_commit": SOURCE_STAGE5AV_COMMIT,
        "decision_file_path": repo_relative(decision_file),
        "decision_file_sha256": sha256_file(decision_file) if decision_file.exists() else None,
        "stage5av_original_reviewer_extra_possible_token_count": extras_payload.get(
            "reviewer_extra_possible_token_count",
            len(original_extras),
        ),
        "stage5av_malformed_reviewer_extra_count": len(malformed_stage5av_records),
        "malformed_stage5av_reviewer_extra_records": malformed_stage5av_records,
        "audit_target_ids": AUDIT_TARGET_IDS,
        "stage5av_branch_manifest_path": repo_relative(stage5av_branch_manifest),
        "stage5av_branch_count_upper_bound_product": manifest_payload.get(
            "branch_count_upper_bound_product",
        ),
        "parser_repair_required": bool(malformed_stage5av_records),
        "canonical_transcription_changed": False,
        "variant_byte_streams_generated": False,
        "execution_performed": False,
        "solve_claim": False,
    }
    policy = {
        "record_type": "possible_token_parser_policy",
        "schema": "schemas/token-block/possible-token-parser-policy-v0.schema.json",
        "stage_id": STAGE5AW_ID,
        "source_stage_id": STAGE5AV_ID,
        "policy_status": "active_for_stage5aw_repair",
        "notes_are_semicolon_delimited": True,
        "possible_tokens_value_stops_at_next_semicolon": True,
        "pipe_separator": "|",
        "token_like_option_length": 2,
        "preserve_exact_case": True,
        "deduplicate_preserving_order": True,
        "extract_token_prefix_from_prose_segment": True,
        "extract_visual_placeholder_from_prose": True,
        "visual_placeholders_allowed": True,
        "visual_placeholder_variant_byte_stream_eligible": False,
        "prose_fragments_in_reviewer_extra_tokens_allowed": False,
        "malformed_fragments_audited": True,
        "canonical_transcription_changed": False,
        "variant_byte_streams_generated": False,
        "solve_claim": False,
    }
    write_yaml(out_audit, audit)
    write_yaml(out_policy, policy)
    write_json(results_dir / "decision_parser_audit.json", audit)
    return audit, policy


def _build_repaired_records(
    decision_file: Path,
    case_challenges: Path,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    payload = _load_decision_file(decision_file)
    challenge_records = _challenge_index(case_challenges)
    repaired_decisions: list[dict[str, Any]] = []
    unresolved_records: list[dict[str, Any]] = []
    extra_records: list[dict[str, Any]] = []
    malformed_records: list[dict[str, Any]] = []
    for raw_record in payload.get("records", []):
        if not isinstance(raw_record, dict):
            continue
        challenge_id = str(raw_record.get("challenge_id"))
        expected = challenge_records.get(challenge_id, {})
        canonical_token = str(raw_record.get("canonical_token"))
        candidate_tokens = _safe_token_list(raw_record.get("candidate_tokens"))
        reviewer_notes = _safe_text(raw_record.get("reviewer_notes"))
        parsed = parse_possible_token_notes(reviewer_notes)
        possible_tokens = parsed.possible_tokens
        details = _possible_token_details(possible_tokens, canonical_token, candidate_tokens)
        visual_placeholders = [
            item["token"]
            for item in details
            if item.get("possible_token_source") == "visual_placeholder_from_reviewer_notes"
        ]
        for malformed in parsed.malformed_fragments:
            malformed_records.append(
                {
                    "record_type": "malformed_possible_token_fragment",
                    "schema": "schemas/token-block/malformed-possible-token-fragment-v0.schema.json",
                    "stage_id": STAGE5AW_ID,
                    "source_stage_id": STAGE5AV_ID,
                    "challenge_id": challenge_id,
                    "token_index_0_based": raw_record.get("token_index_0_based"),
                    "canonical_token": canonical_token,
                    "raw_fragment": malformed["raw_fragment"],
                    "extracted_tokens": malformed["extracted_tokens"],
                    "cleanup_status": malformed["cleanup_status"],
                    "included_in_reviewer_extra_possible_tokens": False,
                    "variant_byte_stream_eligible": False,
                    "canonical_transcription_changed": False,
                    "solve_claim": False,
                }
            )
        repaired_decisions.append(
            {
                "record_type": "repaired_human_review_decision_record",
                "schema": "schemas/token-block/repaired-human-review-decision-record-v0.schema.json",
                "stage_id": STAGE5AW_ID,
                "source_stage_id": STAGE5AV_ID,
                "challenge_id": challenge_id,
                "token_index_0_based": raw_record.get("token_index_0_based"),
                "canonical_token": canonical_token,
                "candidate_tokens": candidate_tokens,
                "selected_token": raw_record.get("selected_token"),
                "decision": raw_record.get("decision"),
                "confidence": raw_record.get("confidence"),
                "reviewer_notes": reviewer_notes,
                "requires_second_review": raw_record.get("requires_second_review"),
                "possible_tokens": possible_tokens,
                "include_all_possible_tokens_for_variant_controls": (
                    parsed.include_all_possible_tokens_for_variant_controls
                ),
                "parser_cleanup_warnings": parsed.cleanup_warnings,
                "malformed_possible_token_fragment_count": len(parsed.malformed_fragments),
                "visual_placeholder_possible_tokens": visual_placeholders,
                "user_decisions_reinterpreted": False,
                "canonical_transcription_changed": False,
                "variant_byte_streams_generated": False,
                "execution_performed": False,
                "solve_claim": False,
            }
        )
        if raw_record.get("decision") == "unresolved":
            mappable = [item for item in details if item.get("primary60_mappable")]
            unmappable = [item for item in details if not item.get("primary60_mappable")]
            reviewer_extra = [
                item["token"]
                for item in details
                if item.get("possible_token_source") == "reviewer_extra_possible_token"
            ]
            unresolved_records.append(
                {
                    "record_type": "repaired_unresolved_token_variant_record",
                    "schema": "schemas/token-block/repaired-unresolved-token-variant-record-v0.schema.json",
                    "stage_id": STAGE5AW_ID,
                    "source_stage_id": STAGE5AV_ID,
                    "source_decision_record_id": challenge_id,
                    "challenge_id": challenge_id,
                    "token_index_0_based": raw_record.get("token_index_0_based"),
                    "canonical_token": canonical_token,
                    "candidate_tokens": candidate_tokens,
                    "possible_tokens": possible_tokens,
                    "possible_token_details": details,
                    "reviewer_extra_possible_tokens": reviewer_extra,
                    "visual_placeholder_possible_tokens": visual_placeholders,
                    "malformed_possible_token_fragments": [
                        record
                        for record in malformed_records
                        if record["challenge_id"] == challenge_id
                    ],
                    "possible_token_count": len(possible_tokens),
                    "generated_candidate_possible_token_count": sum(
                        1
                        for item in details
                        if item["possible_token_source"] == "generated_candidate_token"
                    ),
                    "reviewer_extra_possible_token_count": len(reviewer_extra),
                    "visual_placeholder_possible_token_count": len(visual_placeholders),
                    "primary60_mappable_possible_token_count": len(mappable),
                    "primary60_unmappable_possible_token_count": len(unmappable),
                    "variant_byte_stream_eligible_possible_token_count": sum(
                        1 for item in details if item.get("variant_byte_stream_eligible")
                    ),
                    "possible_tokens_missing": not possible_tokens,
                    "variant_options_default_to_current_only": not possible_tokens,
                    "requires_review_followup": True,
                    "variant_policy_status": "stage5aw_repaired_compact_branch_manifest_only",
                    "source_stage5au_challenge_record_present": bool(expected),
                    "canonical_transcription_changed": False,
                    "variant_byte_streams_generated": False,
                    "execution_performed": False,
                    "solve_claim": False,
                }
            )
        for item in details:
            if item["possible_token_source"] != "reviewer_extra_possible_token":
                continue
            extra_records.append(
                {
                    "record_type": "repaired_reviewer_extra_possible_token",
                    "schema": "schemas/token-block/repaired-reviewer-extra-possible-token-v0.schema.json",
                    "stage_id": STAGE5AW_ID,
                    "source_stage_id": STAGE5AV_ID,
                    "source_decision_record_id": challenge_id,
                    "challenge_id": challenge_id,
                    "token_index_0_based": raw_record.get("token_index_0_based"),
                    "canonical_token": canonical_token,
                    "reviewer_extra_possible_token": item["token"],
                    "reviewer_extra_token_status": "preserved_valid_token_for_variant_controls",
                    "in_generated_candidate_tokens": False,
                    "primary60_alphabet_id": PRIMARY60_ALPHABET_ID,
                    "primary60_mappable": item["primary60_mappable"],
                    "primary60_value": item["primary60_value"],
                    "primary60_error": item["primary60_error"],
                    "variant_byte_stream_eligible": item["variant_byte_stream_eligible"],
                    "canonical_transcription_changed": False,
                    "solve_claim": False,
                }
            )
    return repaired_decisions, unresolved_records, extra_records, malformed_records


def repair_stage5aw_decision_variants(
    decision_file: Path = STAGE5AV_LOCAL_DECISION_TEMPLATE_PATH,
    stage5au_case_challenges: Path = STAGE5AU_CASE_CHALLENGES_V2_PATH,
    stage5ap_alphabet_registry: Path = ALPHABET_PATH,
    parser_policy: Path = STAGE5AW_PARSER_POLICY_PATH,
    results_dir: Path = STAGE5AW_RESULTS_DIR,
    out_decisions: Path = STAGE5AW_REPAIRED_HUMAN_REVIEW_DECISIONS_PATH,
    out_unresolved: Path = STAGE5AW_REPAIRED_UNRESOLVED_VARIANTS_PATH,
    out_extras: Path = STAGE5AW_REPAIRED_REVIEWER_EXTRA_TOKENS_PATH,
    out_malformed: Path = STAGE5AW_MALFORMED_FRAGMENTS_PATH,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    _ = (stage5ap_alphabet_registry, parser_policy)
    _ensure_results_dir(results_dir)
    decisions, unresolved, extras, malformed = _build_repaired_records(
        decision_file,
        stage5au_case_challenges,
    )
    payloads = (
        (
            out_decisions,
            None,
            {
                "record_type": "repaired_human_review_decision_record_set",
                "schema": "schemas/token-block/repaired-human-review-decision-record-v0.schema.json",
                "stage_id": STAGE5AW_ID,
                "source_stage_id": STAGE5AV_ID,
                "decision_file_path": repo_relative(decision_file),
                "decision_file_sha256": sha256_file(decision_file),
                "decision_record_count": len(decisions),
                "records": decisions,
                "user_decisions_reinterpreted": False,
                "canonical_transcription_changed": False,
                "variant_byte_streams_generated": False,
                "solve_claim": False,
            },
        ),
        (
            out_unresolved,
            results_dir / "repaired_unresolved_variants.json",
            {
                "record_type": "repaired_unresolved_token_variant_record_set",
                "schema": "schemas/token-block/repaired-unresolved-token-variant-record-v0.schema.json",
                "stage_id": STAGE5AW_ID,
                "source_stage_id": STAGE5AV_ID,
                "unresolved_token_variant_count": len(unresolved),
                "records": unresolved,
                "canonical_transcription_changed": False,
                "variant_byte_streams_generated": False,
                "execution_performed": False,
                "solve_claim": False,
            },
        ),
        (
            out_extras,
            results_dir / "repaired_reviewer_extra_possible_tokens.json",
            {
                "record_type": "repaired_reviewer_extra_possible_token_set",
                "schema": "schemas/token-block/repaired-reviewer-extra-possible-token-v0.schema.json",
                "stage_id": STAGE5AW_ID,
                "source_stage_id": STAGE5AV_ID,
                "repaired_reviewer_extra_possible_token_count": len(extras),
                "records": extras,
                "prose_fragments_excluded": True,
                "canonical_transcription_changed": False,
                "solve_claim": False,
            },
        ),
        (
            out_malformed,
            results_dir / "malformed_possible_token_fragments.json",
            {
                "record_type": "malformed_possible_token_fragment_set",
                "schema": "schemas/token-block/malformed-possible-token-fragment-v0.schema.json",
                "stage_id": STAGE5AW_ID,
                "source_stage_id": STAGE5AV_ID,
                "malformed_possible_token_fragment_count": len(malformed),
                "records": malformed,
                "fragments_excluded_from_reviewer_extra_tokens": True,
                "variant_byte_streams_generated": False,
                "solve_claim": False,
            },
        ),
    )
    built: list[dict[str, Any]] = []
    for yaml_path, json_path, payload in payloads:
        write_yaml(yaml_path, payload)
        if json_path is not None:
            write_json(json_path, payload)
        built.append(payload)
    return built[0], built[1], built[2], built[3]


def build_stage5aw_repaired_branch_manifest(
    repaired_decisions: Path = STAGE5AW_REPAIRED_HUMAN_REVIEW_DECISIONS_PATH,
    repaired_unresolved: Path = STAGE5AW_REPAIRED_UNRESOLVED_VARIANTS_PATH,
    repaired_extras: Path = STAGE5AW_REPAIRED_REVIEWER_EXTRA_TOKENS_PATH,
    malformed_fragments: Path = STAGE5AW_MALFORMED_FRAGMENTS_PATH,
    stage5ap_transcription: Path = TRANSCRIPTION_PATH,
    stage5ap_mapping_preflight: Path = MAPPING_PATH,
    results_dir: Path = STAGE5AW_RESULTS_DIR,
    out_impact: Path = STAGE5AW_REPAIRED_PRIMARY60_IMPACT_PATH,
    out_branch_manifest: Path = STAGE5AW_REPAIRED_BRANCH_MANIFEST_PATH,
) -> tuple[dict[str, Any], dict[str, Any]]:
    _ = (repaired_decisions, repaired_extras, stage5ap_transcription)
    _ensure_results_dir(results_dir)
    unresolved_payload = read_yaml(repaired_unresolved)
    malformed_payload = read_yaml(malformed_fragments)
    mapping_payload = read_yaml(stage5ap_mapping_preflight)
    unresolved_records = unresolved_payload.get("records", [])
    current_values = {
        record["token"]: record.get("mapped_value")
        for record in mapping_payload.get("value_records", [])
        if isinstance(record, dict)
    }
    possible_values_by_token: list[dict[str, Any]] = []
    delta_rows: list[dict[str, Any]] = []
    for record in unresolved_records:
        current_value = current_values.get(record["canonical_token"])
        mappable_options = [
            item
            for item in record.get("possible_token_details", [])
            if item.get("primary60_mappable")
        ]
        possible_values_by_token.append(
            {
                "challenge_id": record["challenge_id"],
                "token_index_0_based": record["token_index_0_based"],
                "canonical_token": record["canonical_token"],
                "current_primary60_value": current_value,
                "possible_primary60_values": [
                    {
                        "token": item["token"],
                        "primary60_value": item["primary60_value"],
                        "delta_from_current": (
                            item["primary60_value"] - current_value
                            if current_value is not None
                            else None
                        ),
                    }
                    for item in mappable_options
                ],
            }
        )
        deltas = [
            item["primary60_value"] - current_value
            for item in mappable_options
            if current_value is not None
        ]
        delta_rows.append(
            {
                "challenge_id": record["challenge_id"],
                "token_index_0_based": record["token_index_0_based"],
                "canonical_token": record["canonical_token"],
                "delta_values": deltas,
                "delta_min": min(deltas) if deltas else None,
                "delta_max": max(deltas) if deltas else None,
                "delta_count": len(deltas),
            }
        )
    branch_product = _branch_product(unresolved_records, "possible_token_count")
    mappable_branch_product = _branch_product(
        unresolved_records,
        "primary60_mappable_possible_token_count",
    )
    visual_count = sum(
        record.get("visual_placeholder_possible_token_count", 0)
        for record in unresolved_records
    )
    impact = {
        "record_type": "repaired_primary60_variant_impact_summary",
        "schema": "schemas/token-block/repaired-primary60-variant-impact-summary-v0.schema.json",
        "stage_id": STAGE5AW_ID,
        "source_stage_id": STAGE5AV_ID,
        "token_block_id": TOKEN_BLOCK_ID,
        "primary_alphabet_id": PRIMARY60_ALPHABET_ID,
        "primary_alphabet": PRIMARY_ALPHABET,
        "unresolved_token_variant_count": len(unresolved_records),
        "affected_token_indices": [
            record["token_index_0_based"] for record in unresolved_records
        ],
        "total_possible_token_options": sum(
            record.get("possible_token_count", 0) for record in unresolved_records
        ),
        "primary60_mappable_option_count": sum(
            record.get("primary60_mappable_possible_token_count", 0)
            for record in unresolved_records
        ),
        "primary60_unmappable_option_count": sum(
            record.get("primary60_unmappable_possible_token_count", 0)
            for record in unresolved_records
        ),
        "visual_placeholder_possible_token_count": visual_count,
        "malformed_fragment_count": malformed_payload.get(
            "malformed_possible_token_fragment_count",
            0,
        ),
        "branch_count_upper_bound_product": branch_product,
        "branch_count_upper_bound_log10": _log10_int(branch_product),
        "primary60_mappable_branch_upper_bound_product": mappable_branch_product,
        "primary60_mappable_branch_upper_bound_log10": _log10_int(mappable_branch_product),
        "possible_primary60_values_by_token": possible_values_by_token,
        "value_delta_summary_by_token": delta_rows,
        "variant_byte_streams_generated": False,
        "execution_performed": False,
        "solve_claim": False,
    }
    manifest = {
        "record_type": "repaired_token_variant_branch_manifest",
        "schema": "schemas/token-block/repaired-token-variant-branch-manifest-v0.schema.json",
        "stage_id": STAGE5AW_ID,
        "source_stage_id": STAGE5AV_ID,
        "token_block_id": TOKEN_BLOCK_ID,
        "branch_manifest_type": "stage5aw_repaired_compact_unresolved_case_variant_manifest",
        "baseline_source": "stage5ap_canonical_token_block_with_stage5aw_parser_repair",
        "supersedes_stage5av_branch_manifest": STAGE5AV_BRANCH_MANIFEST_PATH.as_posix(),
        "unresolved_token_variant_count": len(unresolved_records),
        "branch_count_upper_bound_product": branch_product,
        "branch_count_upper_bound_log10": _log10_int(branch_product),
        "primary60_mappable_branch_upper_bound_product": mappable_branch_product,
        "primary60_mappable_branch_upper_bound_log10": _log10_int(mappable_branch_product),
        "full_enumeration_max_branches": FULL_ENUMERATION_MAX_BRANCHES,
        "compact_manifest_max_branches": COMPACT_MANIFEST_MAX_BRANCHES,
        "full_enumeration_allowed": branch_product <= FULL_ENUMERATION_MAX_BRANCHES,
        "use_compact_branch_manifest": True,
        "full_cartesian_product_enumerated": False,
        "variant_byte_streams_generated": False,
        "execution_performed": False,
        "unresolved_cases": unresolved_records,
        "malformed_possible_token_fragments": malformed_payload.get("records", []),
        "controls": [
            {
                "control_id": "stage5aw-baseline-confirmed-current-control",
                "control_type": "baseline_current_tokens",
            },
            {
                "control_id": "stage5aw-visual-placeholder-excluded-control",
                "control_type": "visual_placeholders_review_only_not_primary60_variants",
            },
            {
                "control_id": "stage5aw-malformed-fragment-exclusion-control",
                "control_type": "malformed_prose_fragments_excluded",
            },
            {
                "control_id": "stage5aw-single-change-per-case-controls",
                "control_type": "single_unresolved_case_option_controls",
            },
        ],
        "automatic_case_resolution_performed": False,
        "canonical_transcription_changed": False,
        "solve_claim": False,
    }
    write_yaml(out_impact, impact)
    write_yaml(out_branch_manifest, manifest)
    write_json(results_dir / "repaired_primary60_variant_impact_summary.json", impact)
    write_json(results_dir / "repaired_token_variant_branch_manifest.json", manifest)
    return impact, manifest


def build_stage5aw_updates(
    repaired_unresolved: Path = STAGE5AW_REPAIRED_UNRESOLVED_VARIANTS_PATH,
    impact_summary: Path = STAGE5AW_REPAIRED_PRIMARY60_IMPACT_PATH,
    branch_manifest: Path = STAGE5AW_REPAIRED_BRANCH_MANIFEST_PATH,
    out_canonical_update: Path = STAGE5AW_CANONICAL_UPDATE_PATH,
    out_null_control: Path = STAGE5AW_NULL_CONTROL_UPDATE_PATH,
    out_dwh_context: Path = STAGE5AW_DWH_CONTEXT_PATH,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    unresolved = read_yaml(repaired_unresolved)
    impact = read_yaml(impact_summary)
    manifest = read_yaml(branch_manifest)
    canonical_update = {
        "record_type": "stage5aw_canonical_transcription_update",
        "schema": "schemas/token-block/canonical-transcription-update-v0.schema.json",
        "stage_id": STAGE5AW_ID,
        "source_stage_id": STAGE5AV_ID,
        "token_block_id": TOKEN_BLOCK_ID,
        "canonical_transcription_update_status": "unchanged_parser_repair_only",
        "canonical_transcription_changed": False,
        "canonical_transcription_change_count": 0,
        "explicit_change_token_count": 0,
        "parser_repair_only": True,
        "solve_claim": False,
    }
    null_control = {
        "record_type": "stage5aw_null_control_decision_update",
        "schema": "schemas/token-block/null-control-decision-update-v0.schema.json",
        "stage_id": STAGE5AW_ID,
        "source_stage_id": STAGE5AV_ID,
        "token_block_id": TOKEN_BLOCK_ID,
        "supersedes_stage5av_branch_metadata": True,
        "future_preflight_must_use_stage5aw_repaired_manifest": True,
        "visual_placeholders_preserved_for_review": True,
        "visual_placeholders_excluded_from_primary60_byte_variants": True,
        "malformed_prose_fragments_preserved_in_audit": True,
        "malformed_prose_fragments_excluded_from_variant_options": True,
        "unresolved_variant_control_count": unresolved.get("unresolved_token_variant_count", 0),
        "branch_count_upper_bound_product": impact.get("branch_count_upper_bound_product"),
        "control_families": manifest.get("controls", []),
        "execution_performed": False,
        "solve_claim": False,
    }
    dwh_context = {
        "record_type": "stage5aw_dwh_decision_context",
        "schema": "schemas/token-block/dwh-decision-context-v0.schema.json",
        "stage_id": STAGE5AW_ID,
        "source_stage_id": STAGE5AV_ID,
        "token_block_id": TOKEN_BLOCK_ID,
        "dwh_defined": True,
        "dwh_expansion": "Deep Web Hash",
        "decision_parser_repair_relevance": "repaired token variants affect future token-to-value planning",
        "token_block_dwh_relationship_status": "speculative_source_lock_required",
        "dwh_operational_status": "not_operational",
        "hash_search_performed": False,
        "hash_preimage_claim": False,
        "decode_claim": False,
        "solve_claim": False,
    }
    write_yaml(out_canonical_update, canonical_update)
    write_yaml(out_null_control, null_control)
    write_yaml(out_dwh_context, dwh_context)
    return canonical_update, null_control, dwh_context


def build_stage5aw_summary(
    audit: Path = STAGE5AW_DECISION_PARSER_AUDIT_PATH,
    policy: Path = STAGE5AW_PARSER_POLICY_PATH,
    repaired_decisions: Path = STAGE5AW_REPAIRED_HUMAN_REVIEW_DECISIONS_PATH,
    repaired_unresolved: Path = STAGE5AW_REPAIRED_UNRESOLVED_VARIANTS_PATH,
    repaired_extras: Path = STAGE5AW_REPAIRED_REVIEWER_EXTRA_TOKENS_PATH,
    malformed_fragments: Path = STAGE5AW_MALFORMED_FRAGMENTS_PATH,
    impact_summary: Path = STAGE5AW_REPAIRED_PRIMARY60_IMPACT_PATH,
    branch_manifest: Path = STAGE5AW_REPAIRED_BRANCH_MANIFEST_PATH,
    canonical_update: Path = STAGE5AW_CANONICAL_UPDATE_PATH,
    null_control: Path = STAGE5AW_NULL_CONTROL_UPDATE_PATH,
    dwh_context: Path = STAGE5AW_DWH_CONTEXT_PATH,
    out_guardrail: Path = STAGE5AW_GUARDRAIL_PATH,
    out_next_stage: Path = STAGE5AW_NEXT_STAGE_DECISION_PATH,
    out_summary: Path = STAGE5AW_SUMMARY_PATH,
    results_dir: Path = STAGE5AW_RESULTS_DIR,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    _ensure_results_dir(results_dir)
    audit_payload = read_yaml(audit)
    _ = read_yaml(policy)
    decisions_payload = read_yaml(repaired_decisions)
    unresolved_payload = read_yaml(repaired_unresolved)
    extras_payload = read_yaml(repaired_extras)
    malformed_payload = read_yaml(malformed_fragments)
    impact = read_yaml(impact_summary)
    manifest = read_yaml(branch_manifest)
    canonical = read_yaml(canonical_update)
    _ = read_yaml(null_control)
    _ = read_yaml(dwh_context)
    parser_followup_required = any(
        _is_prose_token(str(record.get("reviewer_extra_possible_token", "")))
        for record in extras_payload.get("records", [])
    )
    next_stage_title = (
        "Stage 5AX - decision parser repair followup"
        if parser_followup_required
        else "Stage 5AX - bounded token-block preflight manifest design without execution"
    )
    guardrail = {
        "record_type": "stage5aw_guardrail",
        "schema": "schemas/token-block/stage5aw-guardrail-v0.schema.json",
        "stage_id": STAGE5AW_ID,
        "parser_repair_only": True,
        "user_decisions_reinterpreted": False,
        "automatic_case_resolution_performed": False,
        "canonical_transcription_changed": False,
        "variant_byte_streams_generated": False,
        "variant_experiments_executed": False,
        "ocr_performed": False,
        "ai_ml_interpretation_performed": False,
        "llm_vision_token_reading_performed": False,
        "semantic_image_interpretation_performed": False,
        "hidden_content_image_forensics_performed": False,
        "stego_tool_execution_performed": False,
        "decode_attempt_performed": False,
        "hash_preimage_search_performed": False,
        "cuda_execution_performed": False,
        "cuda_source_modified": False,
        "new_cuda_kernel_added": False,
        "new_cuda_kernels_added": 0,
        "benchmark_performed": False,
        "scored_experiments_executed": False,
        "solve_claim": False,
    }
    next_stage = {
        "record_type": "stage5aw_next_stage_decision",
        "schema": "schemas/project-state/stage5aw-summary-v0.schema.json",
        "stage_id": STAGE5AW_ID,
        "source_stage_id": STAGE5AV_ID,
        "selected_option_id": (
            "stage5ax_decision_parser_repair_followup"
            if parser_followup_required
            else "stage5ax_bounded_token_block_preflight_manifest_design_without_execution"
        ),
        "selected_next_stage_title": next_stage_title,
        "selected_next_stage_reason": (
            "Repaired records still contain malformed reviewer extras."
            if parser_followup_required
            else "Parser repair validated; bounded preflight design can use Stage 5AW repaired branch metadata."
        ),
        "bounded_preflight_manifest_design_ready": not parser_followup_required,
        "decision_parser_followup_required": parser_followup_required,
        "execution_enabled": False,
        "solve_claim": False,
    }
    warning_count = sum(
        len(record.get("parser_cleanup_warnings", []))
        for record in decisions_payload.get("records", [])
    )
    summary = {
        "record_type": "stage5aw_decision_possible_token_parser_repair_summary",
        "schema": "schemas/project-state/stage5aw-summary-v0.schema.json",
        "stage_id": STAGE5AW_ID,
        "status": "complete",
        "source_stage_id": STAGE5AV_ID,
        "source_stage5av_commit": SOURCE_STAGE5AV_COMMIT,
        "decision_file_path": audit_payload.get("decision_file_path"),
        "decision_file_sha256": audit_payload.get("decision_file_sha256"),
        "stage5av_original_reviewer_extra_possible_token_count": audit_payload.get(
            "stage5av_original_reviewer_extra_possible_token_count",
        ),
        "stage5aw_repaired_reviewer_extra_possible_token_count": extras_payload.get(
            "repaired_reviewer_extra_possible_token_count",
        ),
        "malformed_possible_token_fragment_count": malformed_payload.get(
            "malformed_possible_token_fragment_count",
        ),
        "visual_placeholder_possible_token_count": impact.get(
            "visual_placeholder_possible_token_count",
        ),
        "parser_cleanup_warning_count": warning_count,
        "unresolved_variant_record_count": unresolved_payload.get(
            "unresolved_token_variant_count",
        ),
        "primary60_mappable_option_count": impact.get("primary60_mappable_option_count"),
        "primary60_unmappable_option_count": impact.get("primary60_unmappable_option_count"),
        "branch_count_upper_bound_product": impact.get("branch_count_upper_bound_product"),
        "branch_count_upper_bound_log10": impact.get("branch_count_upper_bound_log10"),
        "primary60_mappable_branch_upper_bound_product": impact.get(
            "primary60_mappable_branch_upper_bound_product",
        ),
        "primary60_mappable_branch_upper_bound_log10": impact.get(
            "primary60_mappable_branch_upper_bound_log10",
        ),
        "full_cartesian_product_enumerated": False,
        "variant_byte_streams_generated": False,
        "compact_branch_manifest_created": manifest.get("use_compact_branch_manifest"),
        "canonical_transcription_changed": canonical.get("canonical_transcription_changed"),
        "canonical_transcription_change_count": canonical.get("canonical_transcription_change_count"),
        "canonical_transcription_update_status": canonical.get("canonical_transcription_update_status"),
        "stage5aw_repaired_branch_manifest_created": True,
        "stage5aw_supersedes_stage5av_branch_manifest": True,
        "next_bounded_preflight_manifest_design_ready": not parser_followup_required,
        "decision_parser_followup_required": parser_followup_required,
        "network_fetch_performed": False,
        "live_web_scrape_performed": False,
        "online_repo_clone_performed": False,
        "google_drive_storage_used": False,
        "raw_images_committed": False,
        "generated_crops_committed": False,
        "generated_review_pack_committed": False,
        "generated_variant_outputs_committed": False,
        "generated_outputs_committed": False,
        "codex_output_committed": False,
        "third_party_raw_staged": False,
        "third_party_raw_tracked_new": False,
        "deep_research_performed": False,
        "public_website_publication_performed": False,
        "ocr_performed": False,
        "ai_ml_interpretation_performed": False,
        "llm_vision_token_reading_performed": False,
        "semantic_image_interpretation_performed": False,
        "hidden_content_image_forensics_performed": False,
        "stego_tool_execution_performed": False,
        "lp_page_outguess_run_performed": False,
        "hash_preimage_search_performed": False,
        "decode_attempt_performed": False,
        "hypothesis_generation_performed": False,
        "hypothesis_execution_performed": False,
        "variant_experiments_executed": False,
        "cuda_execution_performed": False,
        "cuda_source_modified": False,
        "new_cuda_kernel_added": False,
        "new_cuda_kernels_added": 0,
        "benchmark_performed": False,
        "scored_experiments_executed": False,
        "canonical_corpus_active": False,
        "page_boundaries_final": False,
        "method_status_upgraded": False,
        "solve_claim": False,
    }
    write_yaml(out_guardrail, guardrail)
    write_yaml(out_next_stage, next_stage)
    write_yaml(out_summary, summary)
    write_json(results_dir / "summary.json", summary)
    (results_dir / "warnings.jsonl").write_text("", encoding="utf-8")
    return guardrail, next_stage, summary


def validate_stage5aw(
    audit: Path = STAGE5AW_DECISION_PARSER_AUDIT_PATH,
    policy: Path = STAGE5AW_PARSER_POLICY_PATH,
    repaired_decisions: Path = STAGE5AW_REPAIRED_HUMAN_REVIEW_DECISIONS_PATH,
    repaired_unresolved: Path = STAGE5AW_REPAIRED_UNRESOLVED_VARIANTS_PATH,
    repaired_extras: Path = STAGE5AW_REPAIRED_REVIEWER_EXTRA_TOKENS_PATH,
    malformed_fragments: Path = STAGE5AW_MALFORMED_FRAGMENTS_PATH,
    impact_summary: Path = STAGE5AW_REPAIRED_PRIMARY60_IMPACT_PATH,
    branch_manifest: Path = STAGE5AW_REPAIRED_BRANCH_MANIFEST_PATH,
    canonical_update: Path = STAGE5AW_CANONICAL_UPDATE_PATH,
    null_control: Path = STAGE5AW_NULL_CONTROL_UPDATE_PATH,
    dwh_context: Path = STAGE5AW_DWH_CONTEXT_PATH,
    guardrail: Path = STAGE5AW_GUARDRAIL_PATH,
    next_stage: Path = STAGE5AW_NEXT_STAGE_DECISION_PATH,
    summary: Path = STAGE5AW_SUMMARY_PATH,
    results_dir: Path | None = STAGE5AW_RESULTS_DIR,
) -> tuple[dict[str, Any], list[str]]:
    payloads = [
        read_yaml(path)
        for path in (
            audit,
            policy,
            repaired_decisions,
            repaired_unresolved,
            repaired_extras,
            malformed_fragments,
            impact_summary,
            branch_manifest,
            canonical_update,
            null_control,
            dwh_context,
            guardrail,
            next_stage,
            summary,
        )
    ]
    (
        audit_payload,
        policy_payload,
        decisions_payload,
        unresolved_payload,
        extras_payload,
        malformed_payload,
        impact,
        manifest,
        canonical,
        null_payload,
        dwh,
        guard,
        next_payload,
        summary_payload,
    ) = payloads
    errors: list[str] = []
    if audit_payload.get("stage5av_malformed_reviewer_extra_count", 0) <= 0:
        errors.append("Stage 5AV malformed reviewer extras were not detected")
    if policy_payload.get("prose_fragments_in_reviewer_extra_tokens_allowed") is not False:
        errors.append("parser policy must disallow prose fragments in extras")
    if decisions_payload.get("decision_record_count") != 203:
        errors.append("repaired decision record count must be 203")
    if unresolved_payload.get("unresolved_token_variant_count") != 77:
        errors.append("repaired unresolved variant count must be 77")
    if any(
        _is_prose_token(str(record.get("reviewer_extra_possible_token", "")))
        for record in extras_payload.get("records", [])
    ):
        errors.append("repaired reviewer extra records still contain prose fragments")
    if malformed_payload.get("malformed_possible_token_fragment_count", 0) <= 0:
        errors.append("malformed possible token fragments must be audited")
    if impact.get("visual_placeholder_possible_token_count", 0) <= 0:
        errors.append("visual placeholders must be preserved")
    if manifest.get("supersedes_stage5av_branch_manifest") != STAGE5AV_BRANCH_MANIFEST_PATH.as_posix():
        errors.append("Stage 5AW manifest must supersede Stage 5AV branch manifest")
    if manifest.get("variant_byte_streams_generated") is not False:
        errors.append("variant byte streams must not be generated")
    if canonical.get("canonical_transcription_changed") is not False:
        errors.append("canonical transcription must remain unchanged")
    if not null_payload.get("future_preflight_must_use_stage5aw_repaired_manifest"):
        errors.append("null-control update must route future preflight to Stage 5AW")
    if dwh.get("hash_search_performed") is not False:
        errors.append("DWH context must block hash search")
    if any(value is not False for key, value in guard.items() if key.endswith("_performed")):
        errors.append("guardrail performed flags must remain false")
    if guard.get("cuda_execution_performed") is not False:
        errors.append("CUDA execution must remain false")
    if guard.get("new_cuda_kernels_added") != 0:
        errors.append("new CUDA kernel count must be 0")
    if guard.get("solve_claim") is not False:
        errors.append("solve claim must remain false")
    if next_payload.get("selected_option_id") != "stage5ax_bounded_token_block_preflight_manifest_design_without_execution":
        errors.append("next stage must be bounded token-block preflight manifest design")
    if summary_payload.get("decision_parser_followup_required") is not False:
        errors.append("decision parser followup should not be required after repair")
    generated_reports_local_present = False
    if results_dir is not None:
        generated_reports_local_present = (results_dir / "summary.json").exists()
    counts = {
        "stage5av_malformed_extras_found": audit_payload.get("stage5av_malformed_reviewer_extra_count", 0),
        "repaired_reviewer_extra_possible_token_count": extras_payload.get(
            "repaired_reviewer_extra_possible_token_count",
            0,
        ),
        "visual_placeholder_possible_token_count": impact.get("visual_placeholder_possible_token_count", 0),
        "malformed_possible_token_fragment_count": malformed_payload.get(
            "malformed_possible_token_fragment_count",
            0,
        ),
        "primary60_mappable_option_count": impact.get("primary60_mappable_option_count", 0),
        "primary60_unmappable_option_count": impact.get("primary60_unmappable_option_count", 0),
        "branch_count_upper_bound_product": impact.get("branch_count_upper_bound_product"),
        "branch_count_upper_bound_log10": impact.get("branch_count_upper_bound_log10"),
        "compact_branch_manifest_created": manifest.get("use_compact_branch_manifest"),
        "canonical_transcription_changed": canonical.get("canonical_transcription_changed"),
        "next_stage": next_payload.get("selected_next_stage_title"),
        "generated_reports_local_present": generated_reports_local_present,
        "validation_error_count": len(errors),
    }
    return counts, errors
