"""Stage 5AL website-ingest staging builders."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from .export import read_yaml, resolve, write_json, write_jsonl, write_records, write_yaml
from .local_inventory import _staged_raw_files_present, _tracked_raw_files_present
from .models import (
    STAGE5AI_SUMMARY_PATH,
    STAGE5AJ_SUMMARY_PATH,
    STAGE5AK_ARITHMETIC_PREFLIGHT_PATH,
    STAGE5AK_CLAIM_RECORDS_PATH,
    STAGE5AK_CORRECTION_LOG_PATH,
    STAGE5AK_SUMMARY_PATH,
    STAGE5AK_WEBSITE_UPDATE_PATH,
    STAGE5AL_BUNDLE_ROOT,
    STAGE5AL_DEEP_RESEARCH_EXPORT_PATH,
    STAGE5AL_DEEP_RESEARCH_EXPORT_SUMMARY_PATH,
    STAGE5AL_FALSE_FLAGS,
    STAGE5AL_GUARDRAIL_PATH,
    STAGE5AL_ID,
    STAGE5AL_NEXT_STAGE_DECISION_PATH,
    STAGE5AL_OUTPUT_DIR,
    STAGE5AL_PUBLICATION_GATE_POLICY_PATH,
    STAGE5AL_REPORTS,
    STAGE5AL_RESEARCH_INDEX_VALIDATION_PATH,
    STAGE5AL_SOURCE_STAGE_ID,
    STAGE5AL_SUMMARY_PATH,
    STAGE5AL_WEBSITE_DATA_CONTRACT_PATH,
    STAGE5AL_WEBSITE_INGEST_DIR,
    STAGE5AL_WEBSITE_INGEST_SUMMARY_PATH,
)
from .publication_gates import build_publication_gate_records

ABSOLUTE_PATH_RE = re.compile(r"(^[A-Za-z]:[\\/]|^\\\\)")
FORBIDDEN_CLAIM_FIELDS = {
    "claim_text",
    "claim_formula",
    "claimed_values",
    "source_message_locator",
    "source_image_refs",
    "image_order",
}


def build_website_ingest_stage5al(
    *,
    stage5ai_summary_path: Path = STAGE5AI_SUMMARY_PATH,
    stage5aj_summary_path: Path = STAGE5AJ_SUMMARY_PATH,
    stage5ak_summary_path: Path = STAGE5AK_SUMMARY_PATH,
    stage5ak_claims_path: Path = STAGE5AK_CLAIM_RECORDS_PATH,
    stage5ak_corrections_path: Path = STAGE5AK_CORRECTION_LOG_PATH,
    stage5ak_arithmetic_path: Path = STAGE5AK_ARITHMETIC_PREFLIGHT_PATH,
    stage5ak_website_update_path: Path = STAGE5AK_WEBSITE_UPDATE_PATH,
    out_dir: Path = STAGE5AL_WEBSITE_INGEST_DIR,
    results_dir: Path = STAGE5AL_OUTPUT_DIR,
    summary_out: Path = STAGE5AL_WEBSITE_INGEST_SUMMARY_PATH,
    contract_out: Path = STAGE5AL_WEBSITE_DATA_CONTRACT_PATH,
    publication_gates_out: Path = STAGE5AL_PUBLICATION_GATE_POLICY_PATH,
) -> dict[str, Any]:
    """Build committed, metadata-only website-ingest records."""

    stage5ai = read_yaml(stage5ai_summary_path)
    stage5aj = read_yaml(stage5aj_summary_path)
    stage5ak = read_yaml(stage5ak_summary_path)
    claims_payload = read_yaml(stage5ak_claims_path)
    corrections = read_yaml(stage5ak_corrections_path)
    arithmetic = read_yaml(stage5ak_arithmetic_path)
    website_update = read_yaml(stage5ak_website_update_path)

    output = resolve(out_dir)
    output.mkdir(parents=True, exist_ok=True)
    result_root = resolve(results_dir)
    result_root.mkdir(parents=True, exist_ok=True)

    website_shell_present = _website_shell_present()
    source_cards = _source_cards()
    content_records = _content_records()
    bundle_records = _bundle_records()
    claim_records = [_claim_record(record) for record in claims_payload.get("records", [])]
    missing_sources = _missing_source_records()
    gates = build_publication_gate_records()
    research_index = _research_index(
        website_shell_present=website_shell_present,
        bundle_records=bundle_records,
        source_cards=source_cards,
        content_records=content_records,
        claim_records=claim_records,
        missing_sources=missing_sources,
        gate_records=gates,
    )
    contract = _data_contract()
    summary = _website_summary(
        stage5ai=stage5ai,
        stage5aj=stage5aj,
        stage5ak=stage5ak,
        website_update=website_update,
        corrections=corrections,
        arithmetic=arithmetic,
        website_shell_present=website_shell_present,
        source_cards=source_cards,
        content_records=content_records,
        bundle_records=bundle_records,
        claim_records=claim_records,
        missing_sources=missing_sources,
        gate_records=gates,
    )
    export_stub = _website_export_stub(summary)

    _write_package(output, research_index, bundle_records, source_cards, content_records, claim_records, gates, export_stub, missing_sources, summary)
    write_yaml(contract_out, contract)
    write_records(publication_gates_out, gates, **_gate_header(gates))
    write_yaml(summary_out, summary)
    write_json(result_root / STAGE5AL_REPORTS["source_inventory"], _source_inventory(source_cards, content_records, claim_records))
    write_json(result_root / STAGE5AL_REPORTS["research_index"], research_index)
    write_json(result_root / STAGE5AL_REPORTS["website_package"], summary)
    write_json(result_root / STAGE5AL_REPORTS["publication_gates"], {"records": gates})
    write_jsonl(result_root / STAGE5AL_REPORTS["warnings"], [])
    return {
        "summary": summary,
        "contract": contract,
        "publication_gates": {**_gate_header(gates), "records": gates},
        "research_index": research_index,
    }


def build_stage5al_guardrail(
    *,
    website_ingest_dir: Path = STAGE5AL_WEBSITE_INGEST_DIR,
    bundle_root: Path = STAGE5AL_BUNDLE_ROOT,
    results_dir: Path = STAGE5AL_OUTPUT_DIR,
    out: Path = STAGE5AL_GUARDRAIL_PATH,
) -> dict[str, Any]:
    """Write Stage 5AL guardrail record."""

    raw_root = Path("third_party")
    guardrail = {
        "record_type": "stage5al_guardrail",
        "schema": "schemas/website-ingest/stage5al-summary-v0.schema.json",
        "stage_id": STAGE5AL_ID,
        "source_stage_id": STAGE5AL_SOURCE_STAGE_ID,
        "website_ingest_dir": website_ingest_dir.as_posix(),
        "bundle_root": bundle_root.as_posix(),
        "results_dir": results_dir.as_posix(),
        "website_ingest_dir_exists": resolve(website_ingest_dir).exists(),
        "bundle_root_exists": resolve(bundle_root).exists(),
        "private_ids_published": False,
        "raw_bodies_published": False,
        **STAGE5AL_FALSE_FLAGS,
        "third_party_raw_staged": _staged_raw_files_present(raw_root),
        "third_party_raw_tracked_new": _tracked_raw_files_present(raw_root),
        "new_cuda_kernels_added": 0,
        "no_solve_claim": True,
    }
    write_yaml(out, guardrail)
    write_json(resolve(results_dir) / "guardrail.json", guardrail)
    return guardrail


def build_stage5al_next_stage_decision(
    *,
    website_validation_path: Path = STAGE5AL_RESEARCH_INDEX_VALIDATION_PATH,
    deep_research_export_summary_path: Path = STAGE5AL_DEEP_RESEARCH_EXPORT_SUMMARY_PATH,
    out: Path = STAGE5AL_NEXT_STAGE_DECISION_PATH,
) -> dict[str, Any]:
    """Select the next stage after website-ingest staging."""

    validation = read_yaml(website_validation_path)
    export_summary = read_yaml(deep_research_export_summary_path)
    export_ready = validation.get("website_ingest_valid") is True and export_summary.get("deep_research_export_ready") is True
    records = []
    options = [
        (
            "stage5am_deep_research_source_inventory_and_reliability_prompt",
            "Stage 5AM - Deep Research source inventory and reliability prompt",
            "The Stage 5AL website-ingest package and private Deep Research export validate without publishing raw or private bodies.",
            export_ready,
            True,
        ),
        (
            "stage5am_publication_gate_cleanup",
            "Stage 5AM - publication gate cleanup",
            "Use only if Stage 5AL validation fails or publication gates need manual review.",
            not export_ready,
            False,
        ),
        (
            "future_public_website_expansion",
            "Future public website expansion",
            "Deferred; Stage 5AL created data contracts only and public publication remains review-gated.",
            False,
            False,
        ),
    ]
    for option_id, title, reason, selected, deep_research in options:
        records.append(
            {
                "record_type": "stage5al_next_stage_decision_record",
                "schema": "schemas/website-ingest/stage5al-summary-v0.schema.json",
                "stage_id": STAGE5AL_ID,
                "source_stage_id": STAGE5AL_SOURCE_STAGE_ID,
                "option_id": option_id,
                "selected": selected,
                "recommended_next_prompt_type": "Deep Research" if deep_research and selected else ("Codex" if selected else None),
                "recommended_next_stage_title": title,
                "recommended_next_stage_reason": reason,
                "deep_research_recommended_next": deep_research and selected,
                "website_expansion_recommended_next": False,
                "scored_experiment_recommended_next": False,
                "unsolved_page_cuda_recommended_next": False,
                "execution_enabled": False,
                "solve_claim": False,
            }
        )
    selected_ids = [record["option_id"] for record in records if record["selected"]]
    header = {
        "record_type": "stage5al_next_stage_decisions",
        "schema": "schemas/website-ingest/stage5al-summary-v0.schema.json",
        "stage_id": STAGE5AL_ID,
        "source_stage_id": STAGE5AL_SOURCE_STAGE_ID,
        "selected_option_id": selected_ids[0],
        "solve_claim": False,
    }
    write_records(out, records, **header)
    return {**header, "records": records}


def build_stage5al_summary(
    *,
    website_ingest_summary_path: Path = STAGE5AL_WEBSITE_INGEST_SUMMARY_PATH,
    website_data_contract_path: Path = STAGE5AL_WEBSITE_DATA_CONTRACT_PATH,
    deep_research_export_path: Path = STAGE5AL_DEEP_RESEARCH_EXPORT_PATH,
    deep_research_export_summary_path: Path = STAGE5AL_DEEP_RESEARCH_EXPORT_SUMMARY_PATH,
    publication_gate_policy_path: Path = STAGE5AL_PUBLICATION_GATE_POLICY_PATH,
    research_index_validation_path: Path = STAGE5AL_RESEARCH_INDEX_VALIDATION_PATH,
    guardrail_path: Path = STAGE5AL_GUARDRAIL_PATH,
    next_stage_decision_path: Path = STAGE5AL_NEXT_STAGE_DECISION_PATH,
    out: Path = STAGE5AL_SUMMARY_PATH,
) -> dict[str, Any]:
    """Build the committed Stage 5AL aggregate summary."""

    website = read_yaml(website_ingest_summary_path)
    contract = read_yaml(website_data_contract_path)
    export = read_yaml(deep_research_export_path)
    export_summary = read_yaml(deep_research_export_summary_path)
    gates = read_yaml(publication_gate_policy_path)
    validation = read_yaml(research_index_validation_path)
    guardrail = read_yaml(guardrail_path)
    decision = read_yaml(next_stage_decision_path)
    selected = next(record for record in decision.get("records", []) if record.get("selected") is True)
    summary = {
        "record_type": "stage5al_website_ingest_and_deep_research_export_summary",
        "schema": "schemas/website-ingest/stage5al-summary-v0.schema.json",
        "stage_id": STAGE5AL_ID,
        "status": "complete",
        "source_stage_id": STAGE5AL_SOURCE_STAGE_ID,
        "website_shell_present": website.get("website_shell_present", False),
        "website_ingest_dir": website.get("website_ingest_dir"),
        "website_ingest_metadata_files": website.get("website_ingest_metadata_files", 0),
        "website_data_contract_ready": contract.get("website_data_contract_ready", False),
        "source_card_count": website.get("source_card_count", 0),
        "content_index_count": website.get("content_index_count", 0),
        "claim_record_count": website.get("claim_record_count", 0),
        "publication_gate_count": gates.get("publication_gate_count", 0),
        "bundle_count": website.get("bundle_count", 0),
        "missing_source_count": website.get("missing_source_count", 0),
        "public_website_ready_count": website.get("public_website_ready_count", 0),
        "metadata_only_safe_count": website.get("metadata_only_safe_count", 0),
        "private_only_count": website.get("private_only_count", 0),
        "review_blocked_count": website.get("review_blocked_count", 0),
        "blocked_private_or_sensitive_count": website.get("blocked_private_or_sensitive_count", 0),
        "deep_research_export_ready": export_summary.get("deep_research_export_ready", False),
        "deep_research_export_path": export.get("relative_path_or_ref"),
        "deep_research_bundle_count": export_summary.get("bundle_count", 0),
        "deep_research_source_count": export_summary.get("source_card_count", 0),
        "deep_research_claim_count": export_summary.get("claim_record_count", 0),
        "research_index_valid": validation.get("website_ingest_valid", False),
        "selected_next_prompt_type": selected.get("recommended_next_prompt_type"),
        "selected_next_stage_title": selected.get("recommended_next_stage_title"),
        "selected_next_stage_reason": selected.get("recommended_next_stage_reason"),
        "deep_research_recommended_next": selected.get("deep_research_recommended_next", False),
        **{key: guardrail.get(key, False) for key in STAGE5AL_FALSE_FLAGS},
        "new_cuda_kernels_added": 0,
        "no_solve_claim": True,
    }
    write_yaml(out, summary)
    write_json(resolve(STAGE5AL_OUTPUT_DIR) / STAGE5AL_REPORTS["summary"], summary)
    return summary


def _write_package(
    output: Path,
    research_index: dict[str, Any],
    bundle_records: list[dict[str, Any]],
    source_cards: list[dict[str, Any]],
    content_records: list[dict[str, Any]],
    claim_records: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    export_stub: dict[str, Any],
    missing_sources: list[dict[str, Any]],
    summary: dict[str, Any],
) -> None:
    payloads = {
        "research-index": research_index,
        "research-bundles": _records_payload("stage5al_research_bundles", "research-bundle-v0", bundle_records),
        "source-cards": _records_payload("stage5al_source_cards", "source-card-v0", source_cards),
        "content-index": _records_payload("stage5al_content_index", "content-index-record-v0", content_records),
        "community-claims": _records_payload("stage5al_community_claims", "community-claim-record-v0", claim_records),
        "publication-gates": {**_gate_header(gates), "records": gates},
        "deep-research-export": export_stub,
        "missing-sources": _records_payload("stage5al_missing_sources", "research-index-v0", missing_sources),
        "summary": summary,
    }
    for name, payload in payloads.items():
        write_yaml(output / f"{name}.yaml", payload)
        if name != "summary":
            write_json(output / f"{name}.json", payload)


def _records_payload(record_type: str, schema_name: str, records: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "record_type": record_type,
        "schema": f"schemas/website-ingest/{schema_name}.schema.json",
        "stage_id": STAGE5AL_ID,
        "source_stage_id": STAGE5AL_SOURCE_STAGE_ID,
        "record_count": len(records),
        "records": records,
        "solve_claim": False,
    }


def _gate_header(gates: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "record_type": "stage5al_publication_gate_policy",
        "schema": "schemas/website-ingest/publication-gate-v0.schema.json",
        "stage_id": STAGE5AL_ID,
        "source_stage_id": STAGE5AL_SOURCE_STAGE_ID,
        "publication_gate_count": len(gates),
        "public_website_ready_count": 0,
        "raw_source_never_publish_count": sum(1 for record in gates if record["status"] == "raw_source_never_publish"),
        "private_deep_research_only_count": sum(1 for record in gates if record["status"] == "private_deep_research_only"),
        "generated_extract_review_required_count": sum(1 for record in gates if record["status"] == "generated_extract_review_required"),
        "private_ids_published": False,
        "raw_bodies_published": False,
        "solve_claim": False,
    }


def _website_shell_present() -> bool:
    root = resolve(Path("."))
    website_files = [
        "package.json",
        "vite.config.ts",
        "vite.config.js",
        "astro.config.mjs",
        "next.config.js",
        "docusaurus.config.js",
        "mkdocs.yml",
    ]
    website_dirs = ["website", "web", "site", "app", "frontend", "docs-site", "public"]
    return any((root / name).exists() for name in website_files + website_dirs)


def _source_cards() -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for stage, path in [
        ("stage-5ai", Path("research-inputs/stage5ai/source_cards.jsonl")),
        ("stage-5aj", Path("research-inputs/stage5aj/source_cards.jsonl")),
        ("stage-5ak", Path("research-inputs/stage5ak/source_cards.jsonl")),
    ]:
        for record in _read_jsonl(path):
            records.append(_source_card(stage, record))
    return sorted(records, key=lambda item: (item["source_id"], item["source_stage_id"]))


def _source_card(stage: str, record: dict[str, Any]) -> dict[str, Any]:
    source_id = str(record.get("source_id", "unknown"))
    refs = _path_refs(record, stage)
    publication_status = "blocked_private_or_sensitive" if source_id == "community_facts_observations_local" else "public_website_review_required"
    return {
        "record_type": "stage5al_source_card",
        "schema": "schemas/website-ingest/source-card-v0.schema.json",
        "stage_id": STAGE5AL_ID,
        "source_stage_id": stage,
        "source_id": source_id,
        "title": str(record.get("title", source_id.replace("_", " "))),
        "source_type": str(record.get("source_type", "unknown")),
        "source_tier": str(record.get("source_tier", "unknown")),
        "priority": str(record.get("priority", "unknown")),
        "publication_status": publication_status,
        "review_status": "public_review_required",
        "private_deep_research_allowed": bool(record.get("private_deep_research_allowed", True)),
        "website_publication_allowed": False,
        "raw_content_publication_allowed": False,
        "generated_extract_publication_allowed": False,
        "path_kind": "committed_metadata",
        "relative_path_or_ref": f"data/website-ingest/stage5al/source-cards.yaml#{source_id}",
        "source_refs": refs,
        "hashes": _safe_list(record.get("hashes", [])),
        "risk_level": str(record.get("risk_level", "review_required")),
        "claim_family": None,
        "requires_null_controls": False,
        "requires_transcript_policy": False,
        "requires_image_coordinate_policy": False,
        "do_not_assume_tags": _safe_list(record.get("do_not_assume", [])) or ["metadata_is_not_source_evidence"],
        "known_questions_refs": _safe_list(record.get("known_questions", [])),
        "missing_source_refs": [],
        "solve_claim": False,
    }


def _content_records() -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for stage, path in [
        ("stage-5ai", Path("research-inputs/stage5ai/content_index.jsonl")),
        ("stage-5aj", Path("research-inputs/stage5aj/content_index.jsonl")),
        ("stage-5ak", Path("research-inputs/stage5ak/content_index.jsonl")),
    ]:
        for record in _read_jsonl(path):
            records.append(_content_record(stage, record))
    return sorted(records, key=lambda item: (item["content_id"], item["source_stage_id"]))


def _content_record(stage: str, record: dict[str, Any]) -> dict[str, Any]:
    content_id = str(record.get("content_id", f"{stage}:unknown"))
    source_id = str(record.get("source_id", "unknown"))
    path = record.get("relative_generated_path")
    ref = f"research-inputs/{stage.replace('-', '')}/{path}" if path else f"research-inputs/{stage.replace('-', '')}/content_index.jsonl#{content_id}"
    status = "blocked_private_or_sensitive" if stage == "stage-5ak" else "generated_extract_review_required"
    return {
        "record_type": "stage5al_content_index_record",
        "schema": "schemas/website-ingest/content-index-record-v0.schema.json",
        "stage_id": STAGE5AL_ID,
        "source_stage_id": stage,
        "content_id": content_id,
        "bundle_id": record.get("bundle_id"),
        "source_id": source_id,
        "title": str(record.get("title", content_id)),
        "source_type": "unknown",
        "source_tier": "unknown",
        "priority": "unknown",
        "content_kind": str(record.get("content_kind", "metadata_only")),
        "publication_status": status,
        "review_status": str(record.get("review_status", "review_required")),
        "private_deep_research_allowed": bool(record.get("private_deep_research_allowed", record.get("private_deep_research_ready", True))),
        "website_publication_allowed": False,
        "raw_content_publication_allowed": False,
        "generated_extract_publication_allowed": False,
        "path_kind": "ignored_private_extract",
        "relative_path_or_ref": _clean_ref(ref),
        "risk_level": "review_required",
        "claim_family": None,
        "requires_null_controls": False,
        "requires_transcript_policy": False,
        "requires_image_coordinate_policy": False,
        "do_not_assume_tags": _safe_list(record.get("do_not_assume_tags", [])) or ["generated_extract_not_publication_ready"],
        "known_questions_refs": [],
        "missing_source_refs": [],
        "solve_claim": False,
    }


def _bundle_records() -> list[dict[str, Any]]:
    pack_index = _read_json(Path("research-inputs/stage5ai/deep_research_pack_index.json"))
    packs = pack_index.get("packs", []) if isinstance(pack_index, dict) else []
    records = []
    for pack in packs:
        bundle_id = str(pack.get("bundle_id", "unknown"))
        records.append(
            {
                "record_type": "stage5al_research_bundle",
                "schema": "schemas/website-ingest/research-bundle-v0.schema.json",
                "stage_id": STAGE5AL_ID,
                "source_stage_id": STAGE5AL_SOURCE_STAGE_ID,
                "bundle_id": bundle_id,
                "title": str(pack.get("title", bundle_id.replace("-", " "))),
                "priority": "A1" if int(pack.get("sequential_order", 999)) <= 5 else "A2",
                "publication_status": "private_deep_research_only",
                "review_status": "private_export_validated",
                "private_deep_research_allowed": True,
                "website_publication_allowed": False,
                "raw_content_publication_allowed": False,
                "generated_extract_publication_allowed": False,
                "path_kind": "ignored_private_extract",
                "relative_path_or_ref": _bundle_ref(bundle_id),
                "source_ids": [],
                "claim_ids": [],
                "do_not_assume_tags": ["bundle_metadata_only", "generated_bodies_not_committed"],
                "known_questions_refs": [_clean_ref(f"research-inputs/stage5al/known_questions_global.md#{bundle_id}")],
                "missing_source_refs": [],
                "solve_claim": False,
            }
        )
    return sorted(records, key=lambda item: str(item["bundle_id"]))


def _claim_record(record: dict[str, Any]) -> dict[str, Any]:
    claim_id = str(record.get("claim_id", "unknown"))
    verification_status = str(record.get("verification_status", "review_required"))
    do_not_assume = ["community_claim_not_evidence", "not_execution_ready", "requires_null_controls"]
    if record.get("requires_exact_transcript"):
        do_not_assume.append("requires_transcript_policy")
    if record.get("requires_exact_image_source"):
        do_not_assume.append("requires_image_coordinate_policy")
    return {
        "record_type": "stage5al_community_claim",
        "schema": "schemas/website-ingest/community-claim-record-v0.schema.json",
        "stage_id": STAGE5AL_ID,
        "source_stage_id": "stage-5ak",
        "claim_id": claim_id,
        "claim_family": str(record.get("claim_family", "unknown")),
        "source_id": str(record.get("source_id", "community_facts_observations_local")),
        "title": str(record.get("claim_family", claim_id)).replace("_", " "),
        "source_type": "local_user_upload",
        "source_tier": "tier4_social_claim_or_screenshot",
        "priority": "A1" if record.get("requires_exact_transcript") else "A2",
        "publication_status": "blocked_private_or_sensitive",
        "review_status": verification_status,
        "private_deep_research_allowed": bool(record.get("deep_research_private_allowed", True)),
        "website_publication_allowed": False,
        "raw_content_publication_allowed": False,
        "generated_extract_publication_allowed": False,
        "path_kind": "committed_metadata",
        "relative_path_or_ref": f"data/source-harvester/stage5ak-community-facts-claim-records.yaml#{claim_id}",
        "risk_level": str(record.get("risk_level", "high")),
        "requires_null_controls": bool(record.get("requires_null_controls", True)),
        "requires_transcript_policy": bool(record.get("requires_exact_transcript", False)),
        "requires_image_coordinate_policy": bool(record.get("requires_exact_image_source", False)),
        "do_not_assume_tags": do_not_assume,
        "known_questions_refs": [str(record.get("recommended_future_test", "source review required"))],
        "missing_source_refs": ["source_lock_required"] if "source_lock" in verification_status else [],
        "execution_ready": False,
        "solve_claim": False,
    }


def _missing_source_records() -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for path in [
        Path("data/source-harvester/stage5ai-missing-source-plan.yaml"),
        Path("data/source-harvester/stage5aj-missing-source-plan-update.yaml"),
        Path("data/source-harvester/stage5ak-missing-source-plan-update.yaml"),
    ]:
        payload = read_yaml(path)
        for record in payload.get("records", []):
            source_id = str(record.get("source_id", "unknown"))
            records.append(
                {
                    "record_type": "stage5al_missing_source",
                    "schema": "schemas/website-ingest/research-index-v0.schema.json",
                    "stage_id": STAGE5AL_ID,
                    "source_stage_id": str(record.get("stage_id", payload.get("stage_id", "unknown"))),
                    "source_id": source_id,
                    "title": source_id.replace("_", " "),
                    "source_type": str(record.get("source_type", "unknown")),
                    "priority": str(record.get("priority", "unknown")),
                    "publication_status": "private_deep_research_only",
                    "path_kind": "committed_metadata",
                    "relative_path_or_ref": path.as_posix(),
                    "status": str(record.get("status", record.get("next_action", "review_required"))),
                    "network_fetch_performed": False,
                    "online_repo_clone_performed": False,
                    "google_drive_storage_used": False,
                    "solve_claim": False,
                }
            )
    return sorted(records, key=lambda item: (item["source_id"], item["source_stage_id"]))


def _research_index(
    *,
    website_shell_present: bool,
    bundle_records: list[dict[str, Any]],
    source_cards: list[dict[str, Any]],
    content_records: list[dict[str, Any]],
    claim_records: list[dict[str, Any]],
    missing_sources: list[dict[str, Any]],
    gate_records: list[dict[str, Any]],
) -> dict[str, Any]:
    return {
        "record_type": "stage5al_research_index",
        "schema": "schemas/website-ingest/research-index-v0.schema.json",
        "stage_id": STAGE5AL_ID,
        "source_stage_id": STAGE5AL_SOURCE_STAGE_ID,
        "website_shell_present": website_shell_present,
        "website_shell_reason": "no_static_website_framework_detected",
        "data_package_path": "data/website-ingest/stage5al",
        "bundle_count": len(bundle_records),
        "source_card_count": len(source_cards),
        "content_index_count": len(content_records),
        "claim_record_count": len(claim_records),
        "publication_gate_count": len(gate_records),
        "missing_source_count": len(missing_sources),
        "public_website_ready_count": 0,
        "private_deep_research_ready": True,
        "records": [
            {"record_kind": "research_bundles", "path": "data/website-ingest/stage5al/research-bundles.yaml"},
            {"record_kind": "source_cards", "path": "data/website-ingest/stage5al/source-cards.yaml"},
            {"record_kind": "content_index", "path": "data/website-ingest/stage5al/content-index.yaml"},
            {"record_kind": "community_claims", "path": "data/website-ingest/stage5al/community-claims.yaml"},
            {"record_kind": "publication_gates", "path": "data/website-ingest/stage5al/publication-gates.yaml"},
            {"record_kind": "deep_research_export", "path": "data/website-ingest/stage5al/deep-research-export.yaml"},
            {"record_kind": "missing_sources", "path": "data/website-ingest/stage5al/missing-sources.yaml"},
        ],
        **STAGE5AL_FALSE_FLAGS,
        "new_cuda_kernels_added": 0,
        "no_solve_claim": True,
    }


def _data_contract() -> dict[str, Any]:
    return {
        "record_type": "stage5al_website_data_contract",
        "schema": "schemas/website-ingest/stage5al-summary-v0.schema.json",
        "stage_id": STAGE5AL_ID,
        "source_stage_id": STAGE5AL_SOURCE_STAGE_ID,
        "website_data_contract_ready": True,
        "data_package_path": "data/website-ingest/stage5al",
        "required_files": [
            "research-index.yaml",
            "research-bundles.yaml",
            "source-cards.yaml",
            "content-index.yaml",
            "community-claims.yaml",
            "publication-gates.yaml",
            "deep-research-export.yaml",
            "missing-sources.yaml",
            "summary.yaml",
        ],
        "path_kinds": [
            "committed_metadata",
            "ignored_private_extract",
            "raw_source_ignored",
            "external_url",
            "generated_report_ignored",
        ],
        "forbidden_committed_fields": sorted(FORBIDDEN_CLAIM_FIELDS),
        "publication_gates_required": True,
        "raw_bodies_allowed": False,
        "private_ids_allowed": False,
        "public_website_ready_default": False,
        "deep_research_export_default": "private_deep_research_only",
        "solve_claim": False,
    }


def _website_summary(
    *,
    stage5ai: dict[str, Any],
    stage5aj: dict[str, Any],
    stage5ak: dict[str, Any],
    website_update: dict[str, Any],
    corrections: dict[str, Any],
    arithmetic: dict[str, Any],
    website_shell_present: bool,
    source_cards: list[dict[str, Any]],
    content_records: list[dict[str, Any]],
    bundle_records: list[dict[str, Any]],
    claim_records: list[dict[str, Any]],
    missing_sources: list[dict[str, Any]],
    gate_records: list[dict[str, Any]],
) -> dict[str, Any]:
    del corrections, arithmetic
    blocked_private = sum(1 for record in source_cards + content_records + claim_records if record.get("publication_status") == "blocked_private_or_sensitive")
    review_blocked = sum(1 for record in source_cards + content_records if record.get("publication_status") != "metadata_only_safe")
    return {
        "record_type": "stage5al_website_ingest_staging_summary",
        "schema": "schemas/website-ingest/stage5al-summary-v0.schema.json",
        "stage_id": STAGE5AL_ID,
        "status": "complete",
        "source_stage_id": STAGE5AL_SOURCE_STAGE_ID,
        "stage5ai_consumed": stage5ai.get("status") == "complete",
        "stage5aj_consumed": stage5aj.get("status") == "complete",
        "stage5ak_consumed": stage5ak.get("status") == "complete",
        "website_shell_present": website_shell_present,
        "website_shell_reason": "no_static_website_framework_detected",
        "website_ingest_dir": "data/website-ingest/stage5al",
        "website_ingest_metadata_files": 9,
        "bundle_count": len(bundle_records),
        "source_card_count": len(source_cards),
        "content_index_count": len(content_records),
        "claim_record_count": len(claim_records),
        "publication_gate_count": len(gate_records),
        "missing_source_count": len(missing_sources),
        "public_website_ready_count": 0,
        "metadata_only_safe_count": 0,
        "private_only_count": len(bundle_records),
        "review_blocked_count": review_blocked,
        "blocked_private_or_sensitive_count": blocked_private,
        "website_ingest_metadata_ready": website_update.get("website_ingest_metadata_ready", False),
        "private_deep_research_ready": True,
        "website_expansion_performed": False,
        "public_website_publication_performed": False,
        **{key: False for key in STAGE5AL_FALSE_FLAGS},
        "new_cuda_kernels_added": 0,
        "no_solve_claim": True,
    }


def _website_export_stub(summary: dict[str, Any]) -> dict[str, Any]:
    return {
        "record_type": "stage5al_deep_research_export_stub",
        "schema": "schemas/website-ingest/deep-research-export-v0.schema.json",
        "stage_id": STAGE5AL_ID,
        "source_stage_id": STAGE5AL_SOURCE_STAGE_ID,
        "relative_path_or_ref": "data/source-harvester/stage5al-deep-research-export.yaml",
        "bundle_count": summary["bundle_count"],
        "source_card_count": summary["source_card_count"],
        "claim_record_count": summary["claim_record_count"],
        "publication_gates_required": True,
        "private_deep_research_allowed": True,
        "website_publication_allowed": False,
        "raw_content_publication_allowed": False,
        "generated_extract_publication_allowed": False,
        "solve_claim": False,
    }


def _source_inventory(
    source_cards: list[dict[str, Any]],
    content_records: list[dict[str, Any]],
    claim_records: list[dict[str, Any]],
) -> dict[str, Any]:
    return {
        "stage_id": STAGE5AL_ID,
        "source_card_count": len(source_cards),
        "content_index_count": len(content_records),
        "claim_record_count": len(claim_records),
        "source_ids": sorted({record["source_id"] for record in source_cards if record.get("source_id")}),
        "claim_ids": sorted(record["claim_id"] for record in claim_records),
        "raw_content_included": False,
        "solve_claim": False,
    }


def _path_refs(record: dict[str, Any], stage: str) -> list[dict[str, str]]:
    refs = []
    for path in _safe_list(record.get("local_source_paths_redacted_or_relative", [])):
        refs.append({"path_kind": "raw_source_ignored", "relative_path_or_ref": _clean_ref(path)})
    if record.get("local_path_hint"):
        refs.append({"path_kind": "raw_source_ignored", "relative_path_or_ref": _clean_ref(str(record["local_path_hint"]))})
    if not refs:
        refs.append({"path_kind": "committed_metadata", "relative_path_or_ref": f"research-inputs/{stage.replace('-', '')}/source_cards.jsonl"})
    return refs


def _bundle_ref(bundle_id: str) -> str:
    stage5ak_manifest = resolve(Path("research-inputs/stage5ak") / bundle_id / "manifest.yaml")
    if stage5ak_manifest.exists():
        return f"research-inputs/stage5ak/{bundle_id}/manifest.yaml"
    return f"research-inputs/stage5ai/{bundle_id}/manifest.yaml"


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    resolved = resolve(path)
    if not resolved.exists():
        return []
    return [json.loads(line) for line in resolved.read_text(encoding="utf-8").splitlines() if line.strip()]


def _read_json(path: Path) -> dict[str, Any]:
    resolved = resolve(path)
    if not resolved.exists():
        return {}
    payload = json.loads(resolved.read_text(encoding="utf-8"))
    return payload if isinstance(payload, dict) else {}


def _safe_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _clean_ref(value: str) -> str:
    normalized = value.replace("\\", "/")
    if ABSOLUTE_PATH_RE.search(normalized):
        return Path(normalized).name
    return normalized
