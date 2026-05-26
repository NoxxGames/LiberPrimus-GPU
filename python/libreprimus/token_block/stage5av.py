"""Stage 5AV human token-case decision integration helpers."""

from __future__ import annotations

import math
from collections import Counter
from pathlib import Path
from typing import Any

import yaml

from .models import (
    ALPHABET_PATH,
    FALSE_GUARDRAILS,
    MAPPING_PATH,
    PRIMARY_ALPHABET,
    STAGE5AU_CANONICAL_CHALLENGES_V2_PATH,
    STAGE5AU_CASE_CHALLENGES_V2_PATH,
    STAGE5AU_ID,
    STAGE5AV_BRANCH_MANIFEST_PATH,
    STAGE5AV_CANONICAL_UPDATE_PATH,
    STAGE5AV_CONFIRMED_TOKENS_PATH,
    STAGE5AV_DECISION_FILE_INGEST_PATH,
    STAGE5AV_DECISION_FILE_VALIDATION_PATH,
    STAGE5AV_DWH_CONTEXT_PATH,
    STAGE5AV_GUARDRAIL_PATH,
    STAGE5AV_HUMAN_REVIEW_DECISIONS_PATH,
    STAGE5AV_ID,
    STAGE5AV_LOCAL_DECISION_TEMPLATE_PATH,
    STAGE5AV_NEXT_STAGE_DECISION_PATH,
    STAGE5AV_NULL_CONTROL_UPDATE_PATH,
    STAGE5AV_PRIMARY60_IMPACT_PATH,
    STAGE5AV_RESULTS_DIR,
    STAGE5AV_REVIEWER_EXTRA_TOKENS_PATH,
    STAGE5AV_SUMMARY_PATH,
    STAGE5AV_UNRESOLVED_VARIANTS_PATH,
    TOKEN_BLOCK_ID,
    TRANSCRIPTION_PATH,
    read_yaml,
    repo_relative,
    sha256_file,
    write_json,
    write_jsonl,
    write_yaml,
)
from .possible_token_parser import parse_possible_token_notes

ALLOWED_DECISIONS = {"keep_current", "change_token", "unresolved", "not_reviewable"}
ALLOWED_CONFIDENCE = {"high", "medium", "low", None}
DECISION_FILE_CANDIDATES = [
    STAGE5AV_LOCAL_DECISION_TEMPLATE_PATH,
    Path("decision-template.yaml"),
    Path("review-decisions/stage5av/decision-template.yaml"),
]
PRIMARY60_ALPHABET_ID = "community_60_digit_upper_lower_a_to_x"
FULL_ENUMERATION_MAX_BRANCHES = 10_000
COMPACT_MANIFEST_MAX_BRANCHES = 1_000_000


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


def parse_possible_tokens(notes: str | None) -> tuple[list[str], bool]:
    """Extract reviewer possible token list from a review note."""

    parsed = parse_possible_token_notes(notes)
    return parsed.possible_tokens, parsed.include_all_possible_tokens_for_variant_controls


def classify_primary60_token(token: str | None) -> dict[str, Any]:
    """Classify a token against the Stage 5AP primary-60 byte mapping."""

    if token is None:
        return {
            "token": None,
            "primary60_status": "missing_token",
            "primary60_mappable": False,
            "primary60_value": None,
            "primary60_error": "missing_token",
        }
    if len(token) != 2:
        return {
            "token": token,
            "primary60_status": "unmappable_primary_60",
            "primary60_mappable": False,
            "primary60_value": None,
            "primary60_error": "token_length_not_2",
        }
    first, suffix = token[0], token[1]
    if first not in "01234":
        return {
            "token": token,
            "primary60_status": "unmappable_primary_60",
            "primary60_mappable": False,
            "primary60_value": None,
            "primary60_error": "first_symbol_not_in_0_to_4",
        }
    if suffix not in PRIMARY_ALPHABET:
        return {
            "token": token,
            "primary60_status": "unmappable_primary_60",
            "primary60_mappable": False,
            "primary60_value": None,
            "primary60_error": "suffix_not_in_primary_60_alphabet",
        }
    return {
        "token": token,
        "primary60_status": "mapped_primary_60",
        "primary60_mappable": True,
        "primary60_value": int(first) * 60 + PRIMARY_ALPHABET.index(suffix),
        "primary60_error": None,
    }


def _possible_token_details(
    possible_tokens: list[str],
    canonical_token: str,
    candidate_tokens: list[str],
) -> list[dict[str, Any]]:
    details = []
    candidate_set = set(candidate_tokens)
    for token in possible_tokens:
        if token == canonical_token:
            source = "current_canonical_token"
        elif token in candidate_set:
            source = "generated_candidate_token"
        else:
            source = "reviewer_extra_possible_token"
        primary60 = classify_primary60_token(token)
        details.append(
            {
                "token": token,
                "possible_token_source": source,
                "primary60_alphabet_id": PRIMARY60_ALPHABET_ID,
                **primary60,
            }
        )
    return details


def _load_decision_file(path: Path) -> dict[str, Any]:
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def resolve_stage5av_decision_file(explicit_path: Path | None = None) -> Path | None:
    candidates = []
    if explicit_path is not None:
        candidates.append(explicit_path)
    candidates.extend(path for path in DECISION_FILE_CANDIDATES if path not in candidates)
    for path in candidates:
        if path.exists():
            return path
    return None


def _challenge_index(path: Path) -> dict[str, dict[str, Any]]:
    payload = read_yaml(path)
    records = payload.get("records", []) if isinstance(payload, dict) else []
    return {str(record.get("challenge_id")): record for record in records}


def _record_source_hash(path: Path | None) -> str | None:
    return sha256_file(path) if path is not None and path.exists() else None


def _validate_records(
    decision_payload: dict[str, Any],
    case_challenges: Path,
) -> tuple[dict[str, Any], list[dict[str, Any]], list[dict[str, Any]]]:
    records = decision_payload.get("records", [])
    challenge_records = _challenge_index(case_challenges)
    errors: list[str] = []
    warnings: list[str] = []
    normalized: list[dict[str, Any]] = []
    decision_counter: Counter[str] = Counter()
    confidence_counter: Counter[str] = Counter()
    second_review_counter: Counter[str] = Counter()
    possible_token_note_count = 0
    possible_tokens_missing_count = 0
    selected_token_pipe_error_count = 0
    stale_3l_typo_warning_count = 0
    numeric_token_normalisation_warning_count = 0

    if not isinstance(records, list):
        errors.append("records is not a list")
        records = []

    seen_ids: set[str] = set()
    for index, raw_record in enumerate(records):
        record = raw_record if isinstance(raw_record, dict) else {}
        challenge_id = str(record.get("challenge_id"))
        expected = challenge_records.get(challenge_id)
        if challenge_id in seen_ids:
            errors.append(f"duplicate challenge_id: {challenge_id}")
        seen_ids.add(challenge_id)

        canonical_token = _safe_text(record.get("canonical_token"))
        selected_token = _safe_text(record.get("selected_token"))
        candidate_tokens = _safe_token_list(record.get("candidate_tokens"))
        decision = _safe_text(record.get("decision"))
        confidence = _safe_text(record.get("confidence"))
        if record.get("confidence") is None:
            confidence = None
        reviewer_notes = _safe_text(record.get("reviewer_notes"))
        requires_second_review = record.get("requires_second_review")
        possible_tokens, include_all_possible = parse_possible_tokens(reviewer_notes)
        if possible_tokens:
            possible_token_note_count += 1
        elif decision == "unresolved":
            possible_tokens_missing_count += 1

        if any(not isinstance(record.get(key), (str, type(None))) for key in ("canonical_token", "selected_token")):
            numeric_token_normalisation_warning_count += 1
            warnings.append(f"{challenge_id}: token field normalised to string")

        if decision not in ALLOWED_DECISIONS:
            errors.append(f"{challenge_id}: invalid decision {decision}")
        if confidence not in ALLOWED_CONFIDENCE:
            errors.append(f"{challenge_id}: invalid confidence {confidence}")
        if confidence is None and decision != "not_reviewable":
            errors.append(f"{challenge_id}: null confidence outside not_reviewable")
        if not isinstance(requires_second_review, bool):
            errors.append(f"{challenge_id}: requires_second_review is not boolean")

        if selected_token is not None and "|" in selected_token:
            selected_token_pipe_error_count += 1
            errors.append(f"{challenge_id}: selected_token contains pipe-separated list")
        if reviewer_notes and "3L" in reviewer_notes:
            stale_3l_typo_warning_count += 1
            warnings.append(f"{challenge_id}: reviewer note contains stale 3L text")
        if decision in {"unresolved", "not_reviewable"}:
            if selected_token is not None:
                errors.append(f"{challenge_id}: {decision} must have selected_token null")
            if not reviewer_notes:
                errors.append(f"{challenge_id}: {decision} requires reviewer_notes")
            elif decision == "unresolved" and "reviewed" not in reviewer_notes.lower():
                errors.append(f"{challenge_id}: unresolved note does not mark reviewed")
        if decision == "keep_current" and selected_token != canonical_token:
            errors.append(f"{challenge_id}: keep_current selected token differs from canonical")
        if decision == "change_token":
            if selected_token is None:
                errors.append(f"{challenge_id}: change_token missing selected_token")
            allowed = set(candidate_tokens) | set(possible_tokens)
            if selected_token not in allowed:
                errors.append(f"{challenge_id}: change_token selected token not allowed")

        if expected is None:
            errors.append(f"{challenge_id}: challenge id not found in Stage 5AU v2 set")
        else:
            expected_index = expected.get("token_index_0_based")
            if record.get("token_index_0_based") != expected_index:
                errors.append(f"{challenge_id}: token index does not match Stage 5AU v2")
            if canonical_token != str(expected.get("canonical_token")):
                errors.append(f"{challenge_id}: canonical token does not match Stage 5AU v2")
            expected_candidates = set(_safe_token_list(expected.get("candidate_tokens")))
            if set(candidate_tokens) != expected_candidates:
                errors.append(f"{challenge_id}: candidate token set does not match Stage 5AU v2")

        decision_counter.update([decision or "missing"])
        confidence_counter.update([confidence or "null"])
        second_review_counter.update([str(requires_second_review).lower()])
        normalized.append(
            {
                "challenge_id": challenge_id,
                "record_index": index,
                "token_index_0_based": record.get("token_index_0_based"),
                "canonical_token": canonical_token,
                "selected_token": selected_token,
                "candidate_tokens": candidate_tokens,
                "decision": decision,
                "confidence": confidence,
                "reviewer_notes": reviewer_notes,
                "requires_second_review": requires_second_review,
                "possible_tokens": possible_tokens,
                "include_all_possible_tokens_for_variant_controls": include_all_possible,
                "source_record": record,
                "stage5au_challenge_record": expected,
            }
        )

    missing_challenges = sorted(set(challenge_records) - seen_ids)
    if missing_challenges:
        errors.append(f"missing Stage 5AU v2 challenges: {len(missing_challenges)}")

    stage5at_255 = next(
        (record for record in normalized if record["challenge_id"] == "stage5at-token-case-255"),
        None,
    )
    validation_counts = {
        "decision_counts": dict(sorted(decision_counter.items())),
        "confidence_counts": dict(sorted(confidence_counter.items())),
        "requires_second_review_counts": dict(sorted(second_review_counter.items())),
        "possible_tokens_note_count": possible_token_note_count,
        "possible_tokens_missing_count": possible_tokens_missing_count,
        "selected_token_pipe_error_count": selected_token_pipe_error_count,
        "stale_3l_typo_warning_count": stale_3l_typo_warning_count,
        "numeric_token_normalisation_warning_count": numeric_token_normalisation_warning_count,
        "stage5at_token_case_255_selected_token": stage5at_255.get("selected_token") if stage5at_255 else None,
        "challenge_ids_unique": len(seen_ids) == len(records),
        "stage5au_v2_challenge_count": len(challenge_records),
        "missing_stage5au_v2_challenge_count": len(missing_challenges),
    }
    validation_rows = [{"level": "error", "message": message} for message in errors]
    validation_rows.extend({"level": "warning", "message": message} for message in warnings)
    return validation_counts, normalized, validation_rows


def ingest_stage5av_decisions(
    decision_file: Path | None = None,
    case_challenges_v2: Path = STAGE5AU_CASE_CHALLENGES_V2_PATH,
    canonical_challenges_v2: Path = STAGE5AU_CANONICAL_CHALLENGES_V2_PATH,
    stage5ap_transcription: Path = TRANSCRIPTION_PATH,
    results_dir: Path = STAGE5AV_RESULTS_DIR,
    out_ingest: Path = STAGE5AV_DECISION_FILE_INGEST_PATH,
    out_validation: Path = STAGE5AV_DECISION_FILE_VALIDATION_PATH,
) -> tuple[dict[str, Any], dict[str, Any]]:
    _ = (canonical_challenges_v2, stage5ap_transcription)
    _ensure_results_dir(results_dir)
    selected = resolve_stage5av_decision_file(decision_file)
    parse_error = None
    payload: dict[str, Any] = {}
    if selected is not None:
        try:
            payload = _load_decision_file(selected)
        except yaml.YAMLError as exc:
            parse_error = str(exc)
    records = payload.get("records", []) if isinstance(payload, dict) else []
    validation_counts: dict[str, Any] = {}
    validation_rows: list[dict[str, Any]] = []
    if selected is not None and parse_error is None:
        validation_counts, _, validation_rows = _validate_records(payload, case_challenges_v2)
    errors = [row["message"] for row in validation_rows if row["level"] == "error"]
    warnings = [row["message"] for row in validation_rows if row["level"] == "warning"]
    if selected is None:
        errors.append("decision file not found")
    if parse_error is not None:
        errors.append(f"decision YAML parse failed: {parse_error}")

    ingest = {
        "record_type": "decision_file_ingest",
        "schema": "schemas/token-block/decision-file-ingest-v0.schema.json",
        "stage_id": STAGE5AV_ID,
        "source_stage_id": STAGE5AU_ID,
        "token_block_id": TOKEN_BLOCK_ID,
        "decision_file_priority_order": [repo_relative(path) for path in DECISION_FILE_CANDIDATES],
        "decision_file_found": selected is not None,
        "decision_file_path": repo_relative(selected) if selected else None,
        "decision_file_sha256": _record_source_hash(selected),
        "decision_file_yaml_valid": selected is not None and parse_error is None,
        "decision_file_parse_error": parse_error,
        "decision_record_count": len(records) if isinstance(records, list) else 0,
        "decision_file_not_committed": True,
        "local_human_review_pack_consumed": selected == STAGE5AV_LOCAL_DECISION_TEMPLATE_PATH,
        "canonical_transcription_changed": False,
        "generated_outputs_committed": False,
        "raw_data_committed": False,
        "solve_claim": False,
    }
    validation = {
        "record_type": "decision_file_validation",
        "schema": "schemas/token-block/decision-file-validation-v0.schema.json",
        "stage_id": STAGE5AV_ID,
        "source_stage_id": STAGE5AU_ID,
        "token_block_id": TOKEN_BLOCK_ID,
        "decision_file_path": ingest["decision_file_path"],
        "decision_file_sha256": ingest["decision_file_sha256"],
        "decision_file_found": ingest["decision_file_found"],
        "yaml_parse_status": "valid" if ingest["decision_file_yaml_valid"] else "invalid_or_missing",
        "decision_record_count": ingest["decision_record_count"],
        "expected_decision_count": 203,
        "decision_record_count_matches_expected": ingest["decision_record_count"] == 203,
        **validation_counts,
        "validation_error_count": len(errors),
        "validation_warning_count": len(warnings),
        "validation_errors": errors,
        "validation_warnings": warnings,
        "valid_for_stage5av_integration": not errors,
        "canonical_transcription_changed": False,
        "generated_outputs_committed": False,
        "raw_data_committed": False,
        "solve_claim": False,
    }
    write_yaml(out_ingest, ingest)
    write_yaml(out_validation, validation)
    write_json(results_dir / "decision_file_ingest_report.json", ingest)
    write_json(results_dir / "decision_file_validation_report.json", validation)
    write_jsonl(results_dir / "warnings.jsonl", validation_rows)
    return ingest, validation


def _build_human_review_records(
    decision_file: Path,
    case_challenges_v2: Path,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    payload = _load_decision_file(decision_file)
    _, normalized, _ = _validate_records(payload, case_challenges_v2)
    decision_records: list[dict[str, Any]] = []
    confirmed_records: list[dict[str, Any]] = []
    unresolved_records: list[dict[str, Any]] = []
    extra_records: list[dict[str, Any]] = []
    for record in normalized:
        challenge = record["stage5au_challenge_record"] or {}
        possible_tokens = record["possible_tokens"]
        if record["decision"] == "unresolved" and not possible_tokens:
            possible_tokens = [record["canonical_token"]]
        details = _possible_token_details(
            possible_tokens,
            record["canonical_token"],
            record["candidate_tokens"],
        )
        mappable = [item for item in details if item["primary60_mappable"]]
        unmappable = [item for item in details if not item["primary60_mappable"]]
        reviewer_extra = [
            item["token"]
            for item in details
            if item["possible_token_source"] == "reviewer_extra_possible_token"
        ]
        common = {
            "record_type": "human_review_decision_record",
            "schema": "schemas/token-block/human-review-decision-record-v0.schema.json",
            "stage_id": STAGE5AV_ID,
            "source_stage_id": STAGE5AU_ID,
            "token_block_id": TOKEN_BLOCK_ID,
            "challenge_id": record["challenge_id"],
            "token_index_0_based": record["token_index_0_based"],
            "token_index_1_based": (record["token_index_0_based"] or 0) + 1,
            "canonical_token": record["canonical_token"],
            "selected_token": record["selected_token"],
            "decision": record["decision"],
            "confidence": record["confidence"],
            "requires_second_review": record["requires_second_review"],
            "reviewer_notes": record["reviewer_notes"],
            "candidate_tokens": record["candidate_tokens"],
            "possible_tokens": possible_tokens,
            "possible_tokens_from_review_note": record["possible_tokens"],
            "possible_tokens_missing": record["decision"] == "unresolved" and not record["possible_tokens"],
            "include_all_possible_tokens_for_variant_controls": record[
                "include_all_possible_tokens_for_variant_controls"
            ],
            "reviewer_extra_possible_tokens": reviewer_extra,
            "possible_token_details": details,
            "primary60_mappable_possible_tokens": [item["token"] for item in mappable],
            "primary60_unmappable_possible_tokens": [item["token"] for item in unmappable],
            "primary60_current_value": challenge.get("primary_60_current_value"),
            "canonical_transcription_changed": False,
            "usable_as_experiment_seed": False,
            "solve_claim": False,
        }
        decision_records.append(common)
        if record["decision"] == "keep_current":
            confirmed_records.append(
                {
                    "record_type": "confirmed_token_record",
                    "schema": "schemas/token-block/confirmed-token-record-v0.schema.json",
                    "stage_id": STAGE5AV_ID,
                    "source_decision_record_id": record["challenge_id"],
                    "challenge_id": record["challenge_id"],
                    "token_index_0_based": record["token_index_0_based"],
                    "confirmed_token": record["canonical_token"],
                    "confirmation_decision": "keep_current",
                    "confidence": record["confidence"],
                    "canonical_transcription_changed": False,
                    "solve_claim": False,
                }
            )
        if record["decision"] == "unresolved":
            unresolved_records.append(
                {
                    "record_type": "unresolved_token_variant_record",
                    "schema": "schemas/token-block/unresolved-token-variant-record-v0.schema.json",
                    "stage_id": STAGE5AV_ID,
                    "source_decision_record_id": record["challenge_id"],
                    "challenge_id": record["challenge_id"],
                    "token_index_0_based": record["token_index_0_based"],
                    "canonical_token": record["canonical_token"],
                    "candidate_tokens": record["candidate_tokens"],
                    "possible_tokens": possible_tokens,
                    "possible_token_details": details,
                    "reviewer_extra_possible_tokens": reviewer_extra,
                    "possible_token_count": len(possible_tokens),
                    "generated_candidate_possible_token_count": sum(
                        1
                        for item in details
                        if item["possible_token_source"] == "generated_candidate_token"
                    ),
                    "reviewer_extra_possible_token_count": len(reviewer_extra),
                    "primary60_mappable_possible_token_count": len(mappable),
                    "primary60_unmappable_possible_token_count": len(unmappable),
                    "possible_tokens_missing": not record["possible_tokens"],
                    "variant_options_default_to_current_only": not record["possible_tokens"],
                    "requires_review_followup": True,
                    "variant_policy_status": "compact_branch_manifest_only",
                    "canonical_transcription_changed": False,
                    "variant_byte_streams_generated": False,
                    "execution_performed": False,
                    "solve_claim": False,
                }
            )
        for item in details:
            if item["possible_token_source"] == "reviewer_extra_possible_token":
                extra_records.append(
                    {
                        "record_type": "reviewer_extra_possible_token",
                        "schema": "schemas/token-block/reviewer-extra-possible-token-v0.schema.json",
                        "stage_id": STAGE5AV_ID,
                        "source_decision_record_id": record["challenge_id"],
                        "challenge_id": record["challenge_id"],
                        "token_index_0_based": record["token_index_0_based"],
                        "canonical_token": record["canonical_token"],
                        "reviewer_extra_possible_token": item["token"],
                        "reviewer_extra_token_status": "preserved_for_variant_controls",
                        "in_generated_candidate_tokens": False,
                        "primary60_alphabet_id": PRIMARY60_ALPHABET_ID,
                        "primary60_mappable": item["primary60_mappable"],
                        "primary60_value": item["primary60_value"],
                        "primary60_error": item["primary60_error"],
                        "canonical_transcription_changed": False,
                        "solve_claim": False,
                    }
                )
    return decision_records, confirmed_records, unresolved_records, extra_records


def build_stage5av_decision_records(
    decision_file: Path | None = None,
    validation: Path = STAGE5AV_DECISION_FILE_VALIDATION_PATH,
    case_challenges_v2: Path = STAGE5AU_CASE_CHALLENGES_V2_PATH,
    stage5ap_alphabet_registry: Path = ALPHABET_PATH,
    results_dir: Path = STAGE5AV_RESULTS_DIR,
    out_decisions: Path = STAGE5AV_HUMAN_REVIEW_DECISIONS_PATH,
    out_confirmed: Path = STAGE5AV_CONFIRMED_TOKENS_PATH,
    out_unresolved: Path = STAGE5AV_UNRESOLVED_VARIANTS_PATH,
    out_extras: Path = STAGE5AV_REVIEWER_EXTRA_TOKENS_PATH,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    _ = (validation, stage5ap_alphabet_registry)
    _ensure_results_dir(results_dir)
    selected = resolve_stage5av_decision_file(decision_file)
    if selected is None:
        raise FileNotFoundError("Stage 5AV decision file not found")
    decision_records, confirmed_records, unresolved_records, extra_records = _build_human_review_records(
        selected,
        case_challenges_v2,
    )
    payloads = (
        (
            out_decisions,
            results_dir / "human_review_decision_records.json",
            {
                "record_type": "human_review_decision_record_set",
                "schema": "schemas/token-block/human-review-decision-record-v0.schema.json",
                "stage_id": STAGE5AV_ID,
                "source_stage_id": STAGE5AU_ID,
                "token_block_id": TOKEN_BLOCK_ID,
                "decision_file_path": repo_relative(selected),
                "decision_file_sha256": sha256_file(selected),
                "decision_record_count": len(decision_records),
                "records": decision_records,
                "canonical_transcription_changed": False,
                "solve_claim": False,
            },
        ),
        (
            out_confirmed,
            results_dir / "confirmed_token_records.json",
            {
                "record_type": "confirmed_token_record_set",
                "schema": "schemas/token-block/confirmed-token-record-v0.schema.json",
                "stage_id": STAGE5AV_ID,
                "source_stage_id": STAGE5AU_ID,
                "confirmed_token_count": len(confirmed_records),
                "records": confirmed_records,
                "canonical_transcription_changed": False,
                "solve_claim": False,
            },
        ),
        (
            out_unresolved,
            results_dir / "unresolved_variant_records.json",
            {
                "record_type": "unresolved_token_variant_record_set",
                "schema": "schemas/token-block/unresolved-token-variant-record-v0.schema.json",
                "stage_id": STAGE5AV_ID,
                "source_stage_id": STAGE5AU_ID,
                "unresolved_token_variant_count": len(unresolved_records),
                "records": unresolved_records,
                "canonical_transcription_changed": False,
                "variant_byte_streams_generated": False,
                "execution_performed": False,
                "solve_claim": False,
            },
        ),
        (
            out_extras,
            results_dir / "reviewer_extra_possible_tokens.json",
            {
                "record_type": "reviewer_extra_possible_token_set",
                "schema": "schemas/token-block/reviewer-extra-possible-token-v0.schema.json",
                "stage_id": STAGE5AV_ID,
                "source_stage_id": STAGE5AU_ID,
                "reviewer_extra_possible_token_count": len(extra_records),
                "records": extra_records,
                "canonical_transcription_changed": False,
                "solve_claim": False,
            },
        ),
    )
    built: list[dict[str, Any]] = []
    for yaml_path, json_path, payload in payloads:
        write_yaml(yaml_path, payload)
        write_json(json_path, payload)
        built.append(payload)
    return built[0], built[1], built[2], built[3]


def _branch_product(records: list[dict[str, Any]], key: str) -> int:
    product = 1
    for record in records:
        count = int(record.get(key, 0))
        product *= max(count, 1)
    return product


def _log10_int(value: int) -> float:
    return 0.0 if value <= 1 else round(math.log10(value), 6)


def build_stage5av_variant_branch_manifest(
    decision_records: Path = STAGE5AV_HUMAN_REVIEW_DECISIONS_PATH,
    unresolved_variants: Path = STAGE5AV_UNRESOLVED_VARIANTS_PATH,
    reviewer_extras: Path = STAGE5AV_REVIEWER_EXTRA_TOKENS_PATH,
    stage5ap_transcription: Path = TRANSCRIPTION_PATH,
    stage5ap_mapping_preflight: Path = MAPPING_PATH,
    results_dir: Path = STAGE5AV_RESULTS_DIR,
    out_impact: Path = STAGE5AV_PRIMARY60_IMPACT_PATH,
    out_branch_manifest: Path = STAGE5AV_BRANCH_MANIFEST_PATH,
) -> tuple[dict[str, Any], dict[str, Any]]:
    _ = (decision_records, reviewer_extras, stage5ap_transcription)
    _ensure_results_dir(results_dir)
    unresolved_payload = read_yaml(unresolved_variants)
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
    impact = {
        "record_type": "primary60_variant_impact_summary",
        "schema": "schemas/token-block/primary60-variant-impact-summary-v0.schema.json",
        "stage_id": STAGE5AV_ID,
        "source_stage_id": STAGE5AU_ID,
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
        "primary60_mappable_possible_token_options": sum(
            record.get("primary60_mappable_possible_token_count", 0)
            for record in unresolved_records
        ),
        "primary60_unmappable_possible_token_options": sum(
            record.get("primary60_unmappable_possible_token_count", 0)
            for record in unresolved_records
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
    full_enum_allowed = branch_product <= FULL_ENUMERATION_MAX_BRANCHES
    manifest = {
        "record_type": "token_variant_branch_manifest",
        "schema": "schemas/token-block/token-variant-branch-manifest-v0.schema.json",
        "stage_id": STAGE5AV_ID,
        "source_stage_id": STAGE5AU_ID,
        "token_block_id": TOKEN_BLOCK_ID,
        "branch_manifest_type": "compact_unresolved_case_variant_manifest",
        "baseline_source": "stage5ap_canonical_token_block_with_stage5av_keep_current_confirmations",
        "unresolved_token_variant_count": len(unresolved_records),
        "confirmed_keep_current_token_count": 126,
        "branch_count_upper_bound_product": branch_product,
        "branch_count_upper_bound_log10": _log10_int(branch_product),
        "full_enumeration_max_branches": FULL_ENUMERATION_MAX_BRANCHES,
        "compact_manifest_max_branches": COMPACT_MANIFEST_MAX_BRANCHES,
        "full_enumeration_allowed": full_enum_allowed,
        "use_compact_branch_manifest": True,
        "full_cartesian_product_enumerated": False,
        "variant_byte_streams_generated": False,
        "execution_performed": False,
        "unresolved_cases": unresolved_records,
        "controls": [
            {
                "control_id": "stage5av-baseline-confirmed-current-control",
                "control_type": "baseline_current_tokens",
            },
            {
                "control_id": "stage5av-single-change-per-case-controls",
                "control_type": "single_unresolved_case_option_controls",
            },
            {
                "control_id": "stage5av-randomized-case-assignment-controls",
                "control_type": "randomized_case_assignment_controls",
            },
            {
                "control_id": "stage5av-current-canonical-unchanged-control",
                "control_type": "current_canonical_unchanged_control",
            },
        ],
        "automatic_case_resolution_performed": False,
        "canonical_transcription_changed": False,
        "solve_claim": False,
    }
    write_yaml(out_impact, impact)
    write_yaml(out_branch_manifest, manifest)
    write_json(results_dir / "primary60_variant_impact_summary.json", impact)
    write_json(results_dir / "token_variant_branch_manifest.json", manifest)
    return impact, manifest


def build_stage5av_updates(
    decision_records: Path = STAGE5AV_HUMAN_REVIEW_DECISIONS_PATH,
    unresolved_variants: Path = STAGE5AV_UNRESOLVED_VARIANTS_PATH,
    impact_summary: Path = STAGE5AV_PRIMARY60_IMPACT_PATH,
    branch_manifest: Path = STAGE5AV_BRANCH_MANIFEST_PATH,
    out_canonical_update: Path = STAGE5AV_CANONICAL_UPDATE_PATH,
    out_null_control_update: Path = STAGE5AV_NULL_CONTROL_UPDATE_PATH,
    out_dwh_context: Path = STAGE5AV_DWH_CONTEXT_PATH,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    decisions = read_yaml(decision_records)
    unresolved = read_yaml(unresolved_variants)
    impact = read_yaml(impact_summary)
    manifest = read_yaml(branch_manifest)
    records = decisions.get("records", [])
    decision_counts = Counter(record.get("decision") for record in records)
    canonical_update = {
        "record_type": "canonical_transcription_update",
        "schema": "schemas/token-block/canonical-transcription-update-v0.schema.json",
        "stage_id": STAGE5AV_ID,
        "source_stage_id": STAGE5AU_ID,
        "token_block_id": TOKEN_BLOCK_ID,
        "canonical_transcription_update_status": "unchanged_user_review_confirms_or_leaves_unresolved",
        "canonical_transcription_changed": False,
        "canonical_transcription_change_count": 0,
        "explicit_change_token_count": decision_counts.get("change_token", 0),
        "high_confidence_change_token_count": sum(
            1
            for record in records
            if record.get("decision") == "change_token"
            and record.get("confidence") == "high"
        ),
        "change_token_records": [
            record for record in records if record.get("decision") == "change_token"
        ],
        "no_direct_transcription_file_edit": True,
        "solve_claim": False,
    }
    null_update = {
        "record_type": "null_control_decision_update",
        "schema": "schemas/token-block/null-control-decision-update-v0.schema.json",
        "stage_id": STAGE5AV_ID,
        "source_stage_id": STAGE5AU_ID,
        "token_block_id": TOKEN_BLOCK_ID,
        "baseline_current_control_preserved": True,
        "confirmed_token_control_count": decision_counts.get("keep_current", 0),
        "unresolved_variant_control_count": unresolved.get("unresolved_token_variant_count", 0),
        "control_families": manifest.get("controls", []),
        "variant_branch_upper_bound_product": impact.get("branch_count_upper_bound_product"),
        "execution_performed": False,
        "solve_claim": False,
    }
    dwh_context = {
        "record_type": "dwh_decision_context",
        "schema": "schemas/token-block/dwh-decision-context-v0.schema.json",
        "stage_id": STAGE5AV_ID,
        "source_stage_id": STAGE5AU_ID,
        "token_block_id": TOKEN_BLOCK_ID,
        "dwh_defined": True,
        "dwh_expansion": "Deep Web Hash",
        "dwh_term_status": "context_only",
        "hash_search_performed": False,
        "dwh_hash_candidates_generated": False,
        "dwh_preimage_search_performed": False,
        "dwh_decode_attempt_performed": False,
        "bounded_variant_manifest_may_feed_future_preflight": True,
        "solve_claim": False,
    }
    write_yaml(out_canonical_update, canonical_update)
    write_yaml(out_null_control_update, null_update)
    write_yaml(out_dwh_context, dwh_context)
    return canonical_update, null_update, dwh_context


def build_stage5av_summary(
    ingest: Path = STAGE5AV_DECISION_FILE_INGEST_PATH,
    validation: Path = STAGE5AV_DECISION_FILE_VALIDATION_PATH,
    decision_records: Path = STAGE5AV_HUMAN_REVIEW_DECISIONS_PATH,
    confirmed: Path = STAGE5AV_CONFIRMED_TOKENS_PATH,
    unresolved_variants: Path = STAGE5AV_UNRESOLVED_VARIANTS_PATH,
    reviewer_extras: Path = STAGE5AV_REVIEWER_EXTRA_TOKENS_PATH,
    impact_summary: Path = STAGE5AV_PRIMARY60_IMPACT_PATH,
    branch_manifest: Path = STAGE5AV_BRANCH_MANIFEST_PATH,
    canonical_update: Path = STAGE5AV_CANONICAL_UPDATE_PATH,
    null_control_update: Path = STAGE5AV_NULL_CONTROL_UPDATE_PATH,
    dwh_context: Path = STAGE5AV_DWH_CONTEXT_PATH,
    out_guardrail: Path = STAGE5AV_GUARDRAIL_PATH,
    out_next_stage: Path = STAGE5AV_NEXT_STAGE_DECISION_PATH,
    out_summary: Path = STAGE5AV_SUMMARY_PATH,
    results_dir: Path = STAGE5AV_RESULTS_DIR,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    _ensure_results_dir(results_dir)
    ingest_payload = read_yaml(ingest)
    validation_payload = read_yaml(validation)
    decisions = read_yaml(decision_records)
    confirmed_payload = read_yaml(confirmed)
    unresolved_payload = read_yaml(unresolved_variants)
    extras_payload = read_yaml(reviewer_extras)
    impact = read_yaml(impact_summary)
    manifest = read_yaml(branch_manifest)
    canonical = read_yaml(canonical_update)
    null_update = read_yaml(null_control_update)
    dwh = read_yaml(dwh_context)
    guardrail = {
        "record_type": "stage5av_guardrail",
        "schema": "schemas/token-block/stage5av-guardrail-v0.schema.json",
        "stage_id": STAGE5AV_ID,
        "source_stage_id": STAGE5AU_ID,
        "token_block_id": TOKEN_BLOCK_ID,
        **FALSE_GUARDRAILS,
        "automatic_case_resolution_performed": False,
        "canonical_transcription_changed": False,
        "canonical_transcription_directly_edited": False,
        "variant_byte_streams_generated": False,
        "full_cartesian_product_enumerated": False,
        "experiment_execution_performed": False,
        "decode_attempt_performed": False,
        "dwh_hash_search_performed": False,
        "hidden_content_interpretation_performed": False,
        "llm_vision_interpretation_performed": False,
        "semantic_interpretation_performed": False,
    }
    validation_errors = validation_payload.get("validation_error_count", 0)
    compact_manifest_created = manifest.get("use_compact_branch_manifest") is True
    next_stage = {
        "record_type": "stage5av_next_stage_decision",
        "schema": "schemas/project-state/stage5av-summary-v0.schema.json",
        "stage_id": STAGE5AV_ID,
        "token_block_id": TOKEN_BLOCK_ID,
        "next_stage_id": "stage-5aw",
        "next_stage_title": "Stage 5AW - bounded token-block preflight manifest design without execution",
        "next_stage_selected": "Stage 5AW - bounded token-block preflight manifest design without execution",
        "decision_file_correction_required": bool(validation_errors),
        "manual_human_review_followup_required": unresolved_payload.get(
            "unresolved_token_variant_count",
            0,
        )
        > 0,
        "bounded_preflight_manifest_design_ready": (
            not validation_errors and compact_manifest_created
        ),
        "next_bounded_preflight_manifest_design_ready": (
            not validation_errors and compact_manifest_created
        ),
        "next_stage_rationale": (
            "Valid human decisions preserve 77 unresolved case variants in a compact "
            "branch manifest; the next stage should design bounded preflight manifests "
            "without enumerating variants or executing experiments."
        ),
        "execution_enabled": False,
        "solve_claim": False,
    }
    summary = {
        "record_type": "stage5av_summary",
        "schema": "schemas/project-state/stage5av-summary-v0.schema.json",
        "stage_id": STAGE5AV_ID,
        "stage_title": "Stage 5AV - integrate token case decisions",
        "status": "complete" if not validation_errors else "blocked_validation_errors",
        "source_stage_id": STAGE5AU_ID,
        "token_block_id": TOKEN_BLOCK_ID,
        "decision_file_found": ingest_payload.get("decision_file_found"),
        "decision_file_path": ingest_payload.get("decision_file_path"),
        "decision_file_sha256": ingest_payload.get("decision_file_sha256"),
        "decision_record_count": decisions.get("decision_record_count", 0),
        "keep_current_count": validation_payload.get("decision_counts", {}).get("keep_current", 0),
        "change_token_count": validation_payload.get("decision_counts", {}).get("change_token", 0),
        "unresolved_count": validation_payload.get("decision_counts", {}).get("unresolved", 0),
        "not_reviewable_count": validation_payload.get("decision_counts", {}).get("not_reviewable", 0),
        "confirmed_token_count": confirmed_payload.get("confirmed_token_count", 0),
        "unresolved_token_variant_count": unresolved_payload.get(
            "unresolved_token_variant_count",
            0,
        ),
        "reviewer_extra_possible_token_count": extras_payload.get(
            "reviewer_extra_possible_token_count",
            0,
        ),
        "primary60_mappable_possible_token_options": impact.get(
            "primary60_mappable_possible_token_options",
            0,
        ),
        "primary60_unmappable_possible_token_options": impact.get(
            "primary60_unmappable_possible_token_options",
            0,
        ),
        "branch_count_upper_bound_product": impact.get("branch_count_upper_bound_product"),
        "branch_count_upper_bound_log10": impact.get("branch_count_upper_bound_log10"),
        "compact_branch_manifest_created": compact_manifest_created,
        "full_cartesian_product_enumerated": False,
        "variant_byte_streams_generated": False,
        "canonical_transcription_changed": canonical.get("canonical_transcription_changed"),
        "canonical_transcription_change_count": canonical.get(
            "canonical_transcription_change_count",
        ),
        "null_controls_updated": null_update.get("baseline_current_control_preserved"),
        "dwh_context_updated": dwh.get("dwh_defined"),
        "validation_error_count": validation_payload.get("validation_error_count", 0),
        "validation_warning_count": validation_payload.get("validation_warning_count", 0),
        "decision_integration_status": "valid_user_decisions_ingested_with_unresolved_variants_preserved",
        "human_review_decisions_integrated": not validation_errors,
        "generated_outputs_committed": False,
        "raw_data_committed": False,
        "solve_claim": False,
        "cuda_execution_performed": False,
        "benchmark_performed": False,
        "next_stage": next_stage["next_stage_selected"],
    }
    write_yaml(out_guardrail, guardrail)
    write_yaml(out_next_stage, next_stage)
    write_yaml(out_summary, summary)
    write_json(results_dir / "summary.json", summary)
    return guardrail, next_stage, summary


def validate_stage5av(
    ingest: Path = STAGE5AV_DECISION_FILE_INGEST_PATH,
    validation: Path = STAGE5AV_DECISION_FILE_VALIDATION_PATH,
    decision_records: Path = STAGE5AV_HUMAN_REVIEW_DECISIONS_PATH,
    confirmed: Path = STAGE5AV_CONFIRMED_TOKENS_PATH,
    unresolved_variants: Path = STAGE5AV_UNRESOLVED_VARIANTS_PATH,
    reviewer_extras: Path = STAGE5AV_REVIEWER_EXTRA_TOKENS_PATH,
    impact_summary: Path = STAGE5AV_PRIMARY60_IMPACT_PATH,
    branch_manifest: Path = STAGE5AV_BRANCH_MANIFEST_PATH,
    canonical_update: Path = STAGE5AV_CANONICAL_UPDATE_PATH,
    null_control_update: Path = STAGE5AV_NULL_CONTROL_UPDATE_PATH,
    dwh_context: Path = STAGE5AV_DWH_CONTEXT_PATH,
    guardrail: Path = STAGE5AV_GUARDRAIL_PATH,
    next_stage: Path = STAGE5AV_NEXT_STAGE_DECISION_PATH,
    summary: Path = STAGE5AV_SUMMARY_PATH,
    results_dir: Path | None = STAGE5AV_RESULTS_DIR,
) -> tuple[dict[str, Any], list[str]]:
    paths = [
        ingest,
        validation,
        decision_records,
        confirmed,
        unresolved_variants,
        reviewer_extras,
        impact_summary,
        branch_manifest,
        canonical_update,
        null_control_update,
        dwh_context,
        guardrail,
        next_stage,
        summary,
    ]
    errors = [f"missing required Stage 5AV record: {path}" for path in paths if not path.exists()]
    if errors:
        return {"required_record_count": len(paths)}, errors
    ingest_payload = read_yaml(ingest)
    validation_payload = read_yaml(validation)
    decisions = read_yaml(decision_records)
    confirmed_payload = read_yaml(confirmed)
    unresolved_payload = read_yaml(unresolved_variants)
    extras_payload = read_yaml(reviewer_extras)
    impact = read_yaml(impact_summary)
    manifest = read_yaml(branch_manifest)
    canonical = read_yaml(canonical_update)
    null_update = read_yaml(null_control_update)
    dwh = read_yaml(dwh_context)
    guard = read_yaml(guardrail)
    next_payload = read_yaml(next_stage)
    summary_payload = read_yaml(summary)
    false_fields = [
        "solve_claim",
        "generated_outputs_committed",
        "raw_data_committed",
        "canonical_transcription_changed",
    ]
    for payload_name, payload in (
        ("ingest", ingest_payload),
        ("validation", validation_payload),
        ("decisions", decisions),
        ("confirmed", confirmed_payload),
        ("unresolved", unresolved_payload),
        ("extras", extras_payload),
        ("impact", impact),
        ("manifest", manifest),
        ("canonical", canonical),
        ("null_update", null_update),
        ("dwh", dwh),
        ("guardrail", guard),
        ("summary", summary_payload),
    ):
        for field in false_fields:
            if field in payload and payload[field] is not False:
                errors.append(f"{payload_name}: {field} must be false")
    if validation_payload.get("validation_error_count") != 0:
        errors.append("Stage 5AV validation errors are present")
    if decisions.get("decision_record_count") != 203:
        errors.append("decision_record_count must be 203")
    if confirmed_payload.get("confirmed_token_count") != 126:
        errors.append("confirmed_token_count must be 126")
    if unresolved_payload.get("unresolved_token_variant_count") != 77:
        errors.append("unresolved_token_variant_count must be 77")
    if validation_payload.get("decision_counts", {}).get("change_token", 0) != 0:
        errors.append("change_token count must remain 0")
    if manifest.get("full_cartesian_product_enumerated") is not False:
        errors.append("branch manifest must not enumerate full Cartesian product")
    if manifest.get("variant_byte_streams_generated") is not False:
        errors.append("branch manifest must not generate variant byte streams")
    if manifest.get("execution_performed") is not False:
        errors.append("branch manifest must not execute experiments")
    if next_payload.get("next_stage_id") != "stage-5aw":
        errors.append("next stage must be Stage 5AW")
    generated_reports_local_present = False
    if results_dir is not None:
        generated_reports_local_present = (results_dir / "summary.json").exists()
    counts = {
        "decision_file_found": ingest_payload.get("decision_file_found"),
        "decision_file_sha256": ingest_payload.get("decision_file_sha256"),
        "decision_record_count": decisions.get("decision_record_count", 0),
        "keep_current_count": validation_payload.get("decision_counts", {}).get("keep_current", 0),
        "change_token_count": validation_payload.get("decision_counts", {}).get("change_token", 0),
        "unresolved_count": validation_payload.get("decision_counts", {}).get("unresolved", 0),
        "not_reviewable_count": validation_payload.get("decision_counts", {}).get("not_reviewable", 0),
        "confirmed_token_count": confirmed_payload.get("confirmed_token_count", 0),
        "unresolved_token_variant_count": unresolved_payload.get(
            "unresolved_token_variant_count",
            0,
        ),
        "reviewer_extra_possible_token_count": extras_payload.get(
            "reviewer_extra_possible_token_count",
            0,
        ),
        "primary60_mappable_possible_token_options": impact.get(
            "primary60_mappable_possible_token_options",
            0,
        ),
        "primary60_unmappable_possible_token_options": impact.get(
            "primary60_unmappable_possible_token_options",
            0,
        ),
        "branch_count_upper_bound_product": impact.get("branch_count_upper_bound_product"),
        "branch_count_upper_bound_log10": impact.get("branch_count_upper_bound_log10"),
        "compact_branch_manifest_created": manifest.get("use_compact_branch_manifest"),
        "canonical_transcription_changed": canonical.get("canonical_transcription_changed"),
        "null_controls_updated": null_update.get("baseline_current_control_preserved"),
        "dwh_context_updated": dwh.get("dwh_defined"),
        "next_stage": next_payload.get("next_stage_selected"),
        "generated_reports_local_present": generated_reports_local_present,
        "validation_error_count": validation_payload.get("validation_error_count", 0),
        "validation_warning_count": validation_payload.get("validation_warning_count", 0),
    }
    return counts, errors
