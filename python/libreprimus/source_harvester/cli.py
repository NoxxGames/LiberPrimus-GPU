"""Typer CLI for Stage 5AF Cicada source harvester."""

from __future__ import annotations

from pathlib import Path

import typer
from rich.console import Console

from .bundles import build_bundle_scaffolds
from .bundle_readiness import build_bundle_readiness
from .classification import classify_local_sources
from .community_arithmetic import build_community_arithmetic_preflight
from .community_attachments import build_community_attachment_index
from .community_claims import build_community_claim_records
from .community_facts import (
    build_community_facts_source_cards,
    inventory_community_facts,
    update_community_deep_research_packs,
)
from .content_index import build_content_index
from .curated_bundles import build_curated_bundles
from .deep_research_pack import build_deep_research_pack_index
from .export import write_json, write_jsonl
from .extractors import extract_html_file
from .extraction_fidelity import build_extraction_fidelity_policy
from .fetcher import fetch_source
from .hashing import inventory_archive, write_hash_path
from .important_links import parse_important_links
from .local_inventory import inventory_local_sources
from .manifest import validate_manifest
from .manifest_linkage import link_local_sources
from .missing_sources import build_missing_source_plan
from .models import (
    CLUE_TARGET_CATEGORIES_PATH,
    COLLECTION_PRIORITIES_PATH,
    DRY_RUN_SUMMARY_PATH,
    FAILURES_REPORT,
    HARVEST_PLAN_REPORT,
    NEXT_STAGE_DECISION_PATH,
    OUTPUT_DIR,
    RESEARCH_BUNDLE_PLAN_PATH,
    SOURCE_MANIFEST_PATH,
    STAGE5AG_ARCHIVE_SUMMARY_PATH,
    STAGE5AG_BUNDLE_READINESS_PATH,
    STAGE5AG_CANDIDATE_SUMMARY_PATH,
    STAGE5AG_FILE_SUMMARY_PATH,
    STAGE5AG_GAP_REPORT_PATH,
    STAGE5AG_GUARDRAIL_PATH,
    STAGE5AG_HASH_SUMMARY_PATH,
    STAGE5AG_LOCAL_LINKAGE_PATH,
    STAGE5AG_MANIFEST_EXTENSION_PATH,
    STAGE5AG_NEXT_STAGE_DECISION_PATH,
    STAGE5AG_OUTPUT_DIR,
    STAGE5AG_ROOT_INVENTORY_PATH,
    STAGE5AG_SUMMARY_PATH,
    STAGE5AI_BUNDLE_GENERATION_SUMMARY_PATH,
    STAGE5AI_BUNDLE_ROOT,
    STAGE5AI_CLASSIFICATION_PATH,
    STAGE5AI_CONTENT_INDEX_SUMMARY_PATH,
    STAGE5AI_DEEP_RESEARCH_PACK_FORMAT_PATH,
    STAGE5AI_GUARDRAIL_PATH,
    STAGE5AI_MISSING_SOURCE_PLAN_PATH,
    STAGE5AI_NEXT_STAGE_DECISION_PATH,
    STAGE5AI_OUTPUT_DIR,
    STAGE5AI_POLICY_PATH,
    STAGE5AI_READINESS_PATH,
    STAGE5AI_SOURCE_CARD_SUMMARY_PATH,
    STAGE5AI_SUMMARY_PATH,
    STAGE5AI_WEBSITE_INGEST_FORMAT_PATH,
    STAGE5AJ_BUNDLE_ROOT,
    STAGE5AJ_CONTENT_INDEX_SUMMARY_PATH,
    STAGE5AJ_DEEP_RESEARCH_UPDATE_PATH,
    STAGE5AJ_FIDELITY_POLICY_PATH,
    STAGE5AJ_GUARDRAIL_PATH,
    STAGE5AJ_IMPORTANT_LINKS_PATH,
    STAGE5AJ_INVENTORY_PATH,
    STAGE5AJ_MANIFEST_EXTENSION_PATH,
    STAGE5AJ_MISSING_SOURCE_PLAN_PATH,
    STAGE5AJ_NEW_CLUE_CATEGORIES_PATH,
    STAGE5AJ_NEXT_STAGE_DECISION_PATH,
    STAGE5AJ_OUTPUT_DIR,
    STAGE5AJ_READINESS_PATH,
    STAGE5AJ_REDACTION_POLICY_PATH,
    STAGE5AJ_SCRAPER_POLICY_PATH,
    STAGE5AJ_SOURCE_CARD_SUMMARY_PATH,
    STAGE5AJ_SOURCE_ROOT,
    STAGE5AJ_SUMMARY_PATH,
    STAGE5AJ_WEBSITE_UPDATE_PATH,
    STAGE5AJ_XLSX_SUMMARY_PATH,
    STAGE5AK_ARITHMETIC_PREFLIGHT_PATH,
    STAGE5AK_ATTACHMENT_INDEX_PATH,
    STAGE5AK_BUNDLE_ROOT,
    STAGE5AK_CLAIM_POLICY_PATH,
    STAGE5AK_CLAIM_RECORDS_PATH,
    STAGE5AK_CLUE_CATEGORIES_PATH,
    STAGE5AK_CONTENT_INDEX_SUMMARY_PATH,
    STAGE5AK_CORRECTION_LOG_PATH,
    STAGE5AK_DEEP_RESEARCH_UPDATE_PATH,
    STAGE5AK_GUARDRAIL_PATH,
    STAGE5AK_INVENTORY_PATH,
    STAGE5AK_MISSING_SOURCE_PLAN_PATH,
    STAGE5AK_NEXT_STAGE_DECISION_PATH,
    STAGE5AK_OUTPUT_DIR,
    STAGE5AK_READINESS_PATH,
    STAGE5AK_SOURCE_CARD_SUMMARY_PATH,
    STAGE5AK_SOURCE_ROOT,
    STAGE5AK_SUMMARY_PATH,
    STAGE5AK_WEBSITE_UPDATE_PATH,
    SUMMARY_PATH,
    TOOL_POLICY_PATH,
)
from .planning import build_plan
from .redaction_policy import build_redaction_policy
from .scraper_profiles import build_scraper_capture_policy
from .source_lock_candidates import build_source_lock_candidates
from .stage5ag_records import (
    build_stage5ag_guardrail,
    build_stage5ag_next_stage_decision,
    build_stage5ag_summary,
)
from .stage5ag_validation import validate_stage5ag
from .stage5ai_records import (
    build_stage5ai_guardrail,
    build_stage5ai_next_stage_decision,
    build_stage5ai_readiness,
    build_stage5ai_summary,
)
from .stage5ai_validation import validate_stage5ai
from .stage5aj_records import (
    build_stage5aj_guardrail,
    build_stage5aj_new_clue_categories,
    build_stage5aj_next_stage_decision,
    build_stage5aj_summary,
)
from .stage5aj_validation import validate_stage5aj
from .stage5ak_records import build_stage5ak_guardrail, build_stage5ak_next_stage_decision, build_stage5ak_summary
from .stage5ak_validation import validate_stage5ak
from .summary import summarize_stage5af
from .usefulfiles import (
    build_usefulfiles_source_cards,
    inventory_usefulfiles,
    update_deep_research_packs,
)
from .validation import validate_stage5af
from .website_ingest import build_website_ingest_index
from .xlsx_extraction import extract_xlsx_metadata

console = Console()
app = typer.Typer(help="Stage 5AF Cicada source-harvester commands.", no_args_is_help=True)


@app.command("validate-manifest")
def validate_manifest_command(
    manifest: Path = typer.Option(SOURCE_MANIFEST_PATH),
    out_dir: Path = typer.Option(OUTPUT_DIR),
) -> None:
    summary, errors = validate_manifest(manifest, out_dir=out_dir)
    console.print(f"source_manifest_records={summary['source_manifest_records']}")
    console.print(f"required_source_ids_present={str(summary['required_source_ids_present']).lower()}")
    console.print(f"validation_error_count={len(errors)}")
    if errors:
        raise typer.Exit(1)


@app.command("plan")
def plan_command(
    manifest: Path = typer.Option(SOURCE_MANIFEST_PATH),
    out: Path = typer.Option(OUTPUT_DIR / HARVEST_PLAN_REPORT),
    dry_run_summary_out: Path = typer.Option(DRY_RUN_SUMMARY_PATH),
    out_dir: Path = typer.Option(OUTPUT_DIR),
) -> None:
    records, summary = build_plan(
        manifest_path=manifest,
        out_path=out,
        dry_run_summary_out=dry_run_summary_out,
        out_dir=out_dir,
    )
    console.print(f"dry_run_plan_records={len(records)}")
    console.print(f"network_fetch_performed={str(summary['network_fetch_performed']).lower()}")


@app.command("fetch")
def fetch_command(
    manifest: Path = typer.Option(SOURCE_MANIFEST_PATH),
    source_id: str = typer.Option(...),
    out_root: Path | None = typer.Option(None),
    allow_network: bool = typer.Option(False),
    allow_downloads: bool = typer.Option(False),
    rate_limit_seconds: float = typer.Option(3.0),
) -> None:
    if out_root is None:
        raise typer.BadParameter("fetch requires --out-root")
    try:
        metadata = fetch_source(
            manifest_path=manifest,
            source_id=source_id,
            out_root=out_root,
            allow_network=allow_network,
            allow_downloads=allow_downloads,
            rate_limit_seconds=rate_limit_seconds,
        )
    except Exception as exc:
        write_jsonl(OUTPUT_DIR / FAILURES_REPORT, [{"source_id": source_id, "error": str(exc)}])
        raise typer.BadParameter(str(exc)) from exc
    console.print(f"fetched_source_id={metadata['source_id']}")
    console.print(f"sha256={metadata['sha256']}")


@app.command("extract")
def extract_command(
    input_path: Path = typer.Option(..., "--input"),
    out: Path = typer.Option(...),
    source_id: str | None = typer.Option(None),
) -> None:
    record = extract_html_file(input_path, source_id=source_id, out=out)
    console.print(f"link_count={len(record['links'])}")
    console.print(f"image_link_count={len(record['image_links'])}")


@app.command("inventory")
def inventory_command(
    path: Path = typer.Option(...),
    out: Path = typer.Option(...),
    source_id: str | None = typer.Option(None),
) -> None:
    records = write_hash_path(path, out=out, source_id=source_id)
    console.print(f"inventory_records={len(records)}")


@app.command("hash-path")
def hash_path_command(
    path: Path = typer.Option(...),
    out: Path = typer.Option(...),
    source_id: str | None = typer.Option(None),
) -> None:
    records = write_hash_path(path, out=out, source_id=source_id)
    console.print(f"hash_records={len(records)}")


@app.command("inventory-archive")
def inventory_archive_command(
    source_id: str = typer.Option(...),
    path: Path = typer.Option(...),
    out_root: Path | None = typer.Option(None),
    out: Path | None = typer.Option(None),
) -> None:
    if out is None:
        if out_root is None:
            raise typer.BadParameter("inventory-archive requires --out or --out-root")
        out = out_root / f"{source_id}-archive-inventory.jsonl"
    records = inventory_archive(path=path, source_id=source_id, out=out)
    console.print(f"archive_inventory_records={len(records)}")


@app.command("build-bundles")
def build_bundles_command(
    bundle_plan: Path = typer.Option(RESEARCH_BUNDLE_PLAN_PATH),
    out_root: Path = typer.Option(OUTPUT_DIR / "research_bundles_preview"),
) -> None:
    records = build_bundle_scaffolds(bundle_plan_path=bundle_plan, out_root=out_root)
    console.print(f"bundle_scaffolds={len(records)}")
    console.print("do_not_assume_generated=true")
    console.print("known_questions_generated=true")


@app.command("summarize")
def summarize_command(
    manifest: Path = typer.Option(SOURCE_MANIFEST_PATH),
    collection_priorities: Path = typer.Option(COLLECTION_PRIORITIES_PATH),
    clue_target_categories: Path = typer.Option(CLUE_TARGET_CATEGORIES_PATH),
    bundle_plan: Path = typer.Option(RESEARCH_BUNDLE_PLAN_PATH),
    tool_policy: Path = typer.Option(TOOL_POLICY_PATH),
    dry_run_summary: Path = typer.Option(DRY_RUN_SUMMARY_PATH),
    next_stage_decision_out: Path = typer.Option(NEXT_STAGE_DECISION_PATH),
    summary_out: Path = typer.Option(SUMMARY_PATH),
    out: Path = typer.Option(OUTPUT_DIR / "summary.json"),
) -> None:
    summary = summarize_stage5af(
        source_manifest_path=manifest,
        collection_priorities_path=collection_priorities,
        clue_target_categories_path=clue_target_categories,
        research_bundle_plan_path=bundle_plan,
        tool_policy_path=tool_policy,
        dry_run_summary_path=dry_run_summary,
        next_stage_decision_out=next_stage_decision_out,
        summary_out=summary_out,
        out_dir=out.parent,
    )
    write_json(out, summary)
    write_jsonl(out.parent / FAILURES_REPORT, [])
    console.print(f"source_manifest_records={summary['source_manifest_records']}")
    console.print(f"recommended_next_stage_title={summary['recommended_next_stage_title']}")


@app.command("validate-stage5af")
def validate_stage5af_command(
    source_manifest: Path = typer.Option(SOURCE_MANIFEST_PATH),
    collection_priorities: Path = typer.Option(COLLECTION_PRIORITIES_PATH),
    clue_target_categories: Path = typer.Option(CLUE_TARGET_CATEGORIES_PATH),
    research_bundle_plan: Path = typer.Option(RESEARCH_BUNDLE_PLAN_PATH),
    tool_policy: Path = typer.Option(TOOL_POLICY_PATH),
    dry_run_summary: Path = typer.Option(DRY_RUN_SUMMARY_PATH),
    next_stage_decision: Path = typer.Option(NEXT_STAGE_DECISION_PATH),
    summary: Path = typer.Option(SUMMARY_PATH),
    results_dir: Path = typer.Option(OUTPUT_DIR),
) -> None:
    counts, errors = validate_stage5af(
        source_manifest_path=source_manifest,
        collection_priorities_path=collection_priorities,
        clue_target_categories_path=clue_target_categories,
        research_bundle_plan_path=research_bundle_plan,
        tool_policy_path=tool_policy,
        dry_run_summary_path=dry_run_summary,
        next_stage_decision_path=next_stage_decision,
        summary_path=summary,
        results_dir=results_dir,
    )
    for key, value in counts.items():
        console.print(f"{key}={str(value).lower() if isinstance(value, bool) else value}")
    console.print(f"validation_error_count={len(errors)}")
    for error in errors:
        console.print(error)
    if errors:
        raise typer.Exit(1)
    console.print("source_harvester_stage5af_valid=true")


@app.command("summary")
def summary_command(summary: Path = typer.Option(SUMMARY_PATH)) -> None:
    from .export import read_yaml

    payload = read_yaml(summary)
    for key in (
        "source_manifest_records",
        "clue_target_category_records",
        "research_bundle_plan_records",
        "network_fetch_performed",
        "raw_downloads_committed",
        "recommended_next_stage_title",
    ):
        console.print(f"{key}={payload.get(key)}")


@app.command("inventory-local-sources")
def inventory_local_sources_command(
    manifest: Path = typer.Option(SOURCE_MANIFEST_PATH),
    source_root: Path = typer.Option(Path("third_party")),
    results_dir: Path = typer.Option(STAGE5AG_OUTPUT_DIR),
    out_root_inventory: Path = typer.Option(STAGE5AG_ROOT_INVENTORY_PATH),
    out_file_summary: Path = typer.Option(STAGE5AG_FILE_SUMMARY_PATH),
    out_archive_summary: Path = typer.Option(STAGE5AG_ARCHIVE_SUMMARY_PATH),
    out_hash_summary: Path = typer.Option(STAGE5AG_HASH_SUMMARY_PATH),
) -> None:
    del manifest
    result = inventory_local_sources(
        source_root=source_root,
        results_dir=results_dir,
        out_root_inventory=out_root_inventory,
        out_file_summary=out_file_summary,
        out_archive_summary=out_archive_summary,
        out_hash_summary=out_hash_summary,
    )
    root = result["root_inventory"]
    archive = result["archive_summary"]
    console.print(f"source_root_exists={str(root['root_exists']).lower()}")
    console.print(f"total_local_files={root['total_files']}")
    console.print(f"archives_inventoried={archive['archive_record_count']}")
    console.print(f"unsupported_archive_count={archive['unsupported_archive_count']}")


@app.command("link-local-sources")
def link_local_sources_command(
    manifest: Path = typer.Option(SOURCE_MANIFEST_PATH),
    source_root: Path = typer.Option(Path("third_party")),
    results_dir: Path = typer.Option(STAGE5AG_OUTPUT_DIR),
    out: Path = typer.Option(STAGE5AG_LOCAL_LINKAGE_PATH),
    out_extension: Path = typer.Option(STAGE5AG_MANIFEST_EXTENSION_PATH),
) -> None:
    linkage = link_local_sources(
        manifest_path=manifest,
        source_root=source_root,
        results_dir=results_dir,
        out=out,
        out_extension=out_extension,
    )
    console.print(f"manifest_records_consumed={linkage['manifest_records_consumed']}")
    console.print(f"matched_count={linkage['matched_count']}")
    console.print(f"missing_count={linkage['missing_count']}")
    console.print(f"unclassified_local_count={linkage['unclassified_local_count']}")


@app.command("build-source-lock-candidates")
def build_source_lock_candidates_command(
    manifest: Path = typer.Option(SOURCE_MANIFEST_PATH),
    local_linkage: Path = typer.Option(STAGE5AG_LOCAL_LINKAGE_PATH),
    out: Path = typer.Option(STAGE5AG_CANDIDATE_SUMMARY_PATH),
    gap_report: Path = typer.Option(STAGE5AG_GAP_REPORT_PATH),
) -> None:
    del manifest
    result = build_source_lock_candidates(
        local_linkage_path=local_linkage,
        out=out,
        gap_report=gap_report,
    )
    summary = result["summary"]
    gaps = result["gap_report"]
    console.print(f"source_lock_candidates_ready={summary['ready_count']}")
    console.print(f"source_lock_candidates_needing_review={summary['needs_review_count']}")
    console.print(f"source_gap_records={gaps['gap_count']}")


@app.command("build-bundle-readiness")
def build_bundle_readiness_command(
    bundle_plan: Path = typer.Option(RESEARCH_BUNDLE_PLAN_PATH),
    local_linkage: Path = typer.Option(STAGE5AG_LOCAL_LINKAGE_PATH),
    out: Path = typer.Option(STAGE5AG_BUNDLE_READINESS_PATH),
    results_dir: Path = typer.Option(STAGE5AG_OUTPUT_DIR),
) -> None:
    summary = build_bundle_readiness(
        bundle_plan_path=bundle_plan,
        local_linkage_path=local_linkage,
        out=out,
        results_dir=results_dir,
    )
    console.print(f"research_bundle_records={summary['bundle_records']}")
    console.print(f"research_bundles_ready_for_extraction_prep={summary['ready_for_extraction_prep_count']}")
    console.print(f"research_bundles_not_ready={summary['not_ready_count']}")


@app.command("build-stage5ag-guardrail")
def build_stage5ag_guardrail_command(
    source_root: Path = typer.Option(Path("third_party")),
    results_dir: Path = typer.Option(STAGE5AG_OUTPUT_DIR),
    out: Path = typer.Option(STAGE5AG_GUARDRAIL_PATH),
) -> None:
    guardrail = build_stage5ag_guardrail(source_root=source_root, results_dir=results_dir, out=out)
    console.print(f"network_fetch_performed={str(guardrail['network_fetch_performed']).lower()}")
    console.print(f"online_repo_clone_performed={str(guardrail['online_repo_clone_performed']).lower()}")
    console.print(f"google_drive_storage_used={str(guardrail['google_drive_storage_used']).lower()}")
    console.print(f"source_root_raw_content_ignored={str(guardrail['source_root_raw_content_ignored']).lower()}")


@app.command("build-stage5ag-next-stage-decision")
def build_stage5ag_next_stage_decision_command(
    summary_inputs: list[Path] = typer.Option(None),
    root_inventory: Path | None = typer.Option(None),
    local_linkage: Path | None = typer.Option(None),
    bundle_readiness: Path | None = typer.Option(None),
    out: Path = typer.Option(STAGE5AG_NEXT_STAGE_DECISION_PATH),
) -> None:
    if summary_inputs:
        if len(summary_inputs) != 3:
            raise typer.BadParameter("--summary-inputs requires root inventory, local linkage, and bundle readiness")
        root_inventory, local_linkage, bundle_readiness = summary_inputs
    if root_inventory is None or local_linkage is None or bundle_readiness is None:
        raise typer.BadParameter("provide --summary-inputs or explicit --root-inventory/--local-linkage/--bundle-readiness")
    result = build_stage5ag_next_stage_decision(
        root_inventory_path=root_inventory,
        local_linkage_path=local_linkage,
        bundle_readiness_path=bundle_readiness,
        out=out,
    )
    console.print(f"selected_option_id={result['selected_option_id']}")


@app.command("build-stage5ag-summary")
def build_stage5ag_summary_command(
    root_inventory: Path = typer.Option(STAGE5AG_ROOT_INVENTORY_PATH),
    file_summary: Path = typer.Option(STAGE5AG_FILE_SUMMARY_PATH),
    archive_summary: Path = typer.Option(STAGE5AG_ARCHIVE_SUMMARY_PATH),
    hash_summary: Path = typer.Option(STAGE5AG_HASH_SUMMARY_PATH),
    local_linkage: Path = typer.Option(STAGE5AG_LOCAL_LINKAGE_PATH),
    candidate_summary: Path = typer.Option(STAGE5AG_CANDIDATE_SUMMARY_PATH),
    gap_report: Path = typer.Option(STAGE5AG_GAP_REPORT_PATH),
    bundle_readiness: Path = typer.Option(STAGE5AG_BUNDLE_READINESS_PATH),
    guardrail: Path = typer.Option(STAGE5AG_GUARDRAIL_PATH),
    next_stage_decision: Path = typer.Option(STAGE5AG_NEXT_STAGE_DECISION_PATH),
    out: Path = typer.Option(STAGE5AG_SUMMARY_PATH),
    results_dir: Path = typer.Option(STAGE5AG_OUTPUT_DIR),
) -> None:
    summary = build_stage5ag_summary(
        root_inventory_path=root_inventory,
        file_summary_path=file_summary,
        archive_summary_path=archive_summary,
        hash_summary_path=hash_summary,
        local_linkage_path=local_linkage,
        candidate_summary_path=candidate_summary,
        gap_report_path=gap_report,
        bundle_readiness_path=bundle_readiness,
        guardrail_path=guardrail,
        next_stage_decision_path=next_stage_decision,
        out=out,
        results_dir=results_dir,
    )
    console.print(f"stage_id={summary['stage_id']}")
    console.print(f"total_local_files={summary['total_local_files']}")
    console.print(f"recommended_next_stage_title={summary['recommended_next_stage_title']}")


@app.command("validate-stage5ag")
def validate_stage5ag_command(
    root_inventory: Path = typer.Option(STAGE5AG_ROOT_INVENTORY_PATH),
    file_summary: Path = typer.Option(STAGE5AG_FILE_SUMMARY_PATH),
    archive_summary: Path = typer.Option(STAGE5AG_ARCHIVE_SUMMARY_PATH),
    hash_summary: Path = typer.Option(STAGE5AG_HASH_SUMMARY_PATH),
    local_linkage: Path = typer.Option(STAGE5AG_LOCAL_LINKAGE_PATH),
    candidate_summary: Path = typer.Option(STAGE5AG_CANDIDATE_SUMMARY_PATH),
    gap_report: Path = typer.Option(STAGE5AG_GAP_REPORT_PATH),
    bundle_readiness: Path = typer.Option(STAGE5AG_BUNDLE_READINESS_PATH),
    guardrail: Path = typer.Option(STAGE5AG_GUARDRAIL_PATH),
    next_stage_decision: Path = typer.Option(STAGE5AG_NEXT_STAGE_DECISION_PATH),
    summary: Path = typer.Option(STAGE5AG_SUMMARY_PATH),
    results_dir: Path = typer.Option(STAGE5AG_OUTPUT_DIR),
) -> None:
    counts, errors = validate_stage5ag(
        root_inventory_path=root_inventory,
        file_summary_path=file_summary,
        archive_summary_path=archive_summary,
        hash_summary_path=hash_summary,
        local_linkage_path=local_linkage,
        candidate_summary_path=candidate_summary,
        gap_report_path=gap_report,
        bundle_readiness_path=bundle_readiness,
        guardrail_path=guardrail,
        next_stage_decision_path=next_stage_decision,
        summary_path=summary,
        results_dir=results_dir,
    )
    for key, value in counts.items():
        console.print(f"{key}={str(value).lower() if isinstance(value, bool) else value}")
    console.print(f"validation_error_count={len(errors)}")
    for error in errors:
        console.print(error)
    if errors:
        raise typer.Exit(1)
    console.print("source_harvester_stage5ag_valid=true")


@app.command("classify-local-sources")
def classify_local_sources_command(
    candidate_summary: Path = typer.Option(STAGE5AG_CANDIDATE_SUMMARY_PATH),
    local_linkage: Path = typer.Option(STAGE5AG_LOCAL_LINKAGE_PATH),
    out: Path = typer.Option(STAGE5AI_CLASSIFICATION_PATH),
    results_dir: Path = typer.Option(STAGE5AI_OUTPUT_DIR),
) -> None:
    result = classify_local_sources(
        candidate_summary_path=candidate_summary,
        local_linkage_path=local_linkage,
        out=out,
        results_dir=results_dir,
    )
    console.print(f"unclassified_source_classification_records={result['classification_records']}")
    console.print(f"provisionally_classified_count={result['provisionally_classified_count']}")


@app.command("build-source-cards")
def build_source_cards_command(
    local_linkage: Path = typer.Option(STAGE5AG_LOCAL_LINKAGE_PATH),
    candidate_summary: Path = typer.Option(STAGE5AG_CANDIDATE_SUMMARY_PATH),
    classification: Path = typer.Option(STAGE5AI_CLASSIFICATION_PATH),
    bundle_plan: Path = typer.Option(RESEARCH_BUNDLE_PLAN_PATH),
    bundle_root: Path = typer.Option(STAGE5AI_BUNDLE_ROOT),
    results_dir: Path = typer.Option(STAGE5AI_OUTPUT_DIR),
    out: Path = typer.Option(STAGE5AI_SOURCE_CARD_SUMMARY_PATH),
) -> None:
    from .source_cards import build_source_cards

    result = build_source_cards(
        local_linkage_path=local_linkage,
        candidate_summary_path=candidate_summary,
        classification_path=classification,
        bundle_plan_path=bundle_plan,
        bundle_root=bundle_root,
        results_dir=results_dir,
        out=out,
    )
    console.print(f"source_card_records={result['source_card_records']}")
    console.print(f"unclassified_source_cards={result['unclassified_source_cards']}")


@app.command("build-curated-bundles")
def build_curated_bundles_command(
    local_linkage: Path = typer.Option(STAGE5AG_LOCAL_LINKAGE_PATH),
    bundle_readiness: Path = typer.Option(STAGE5AG_BUNDLE_READINESS_PATH),
    bundle_plan: Path = typer.Option(RESEARCH_BUNDLE_PLAN_PATH),
    classification: Path = typer.Option(STAGE5AI_CLASSIFICATION_PATH),
    source_root: Path = typer.Option(Path("third_party")),
    bundle_root: Path = typer.Option(STAGE5AI_BUNDLE_ROOT),
    results_dir: Path = typer.Option(STAGE5AI_OUTPUT_DIR),
    out_policy: Path = typer.Option(STAGE5AI_POLICY_PATH),
    out_summary: Path = typer.Option(STAGE5AI_BUNDLE_GENERATION_SUMMARY_PATH),
) -> None:
    result = build_curated_bundles(
        local_linkage_path=local_linkage,
        bundle_readiness_path=bundle_readiness,
        bundle_plan_path=bundle_plan,
        classification_path=classification,
        source_root=source_root,
        bundle_root=bundle_root,
        results_dir=results_dir,
        out_policy=out_policy,
        out_summary=out_summary,
    )
    console.print(f"curated_bundle_records={result['curated_bundle_records']}")
    console.print(f"bundles_with_generated_skeleton={result['bundles_with_generated_skeleton']}")
    console.print(f"bundles_with_extracted_local_content={result['bundles_with_extracted_local_content']}")


@app.command("build-content-index")
def build_content_index_command(
    bundle_root: Path = typer.Option(STAGE5AI_BUNDLE_ROOT),
    results_dir: Path = typer.Option(STAGE5AI_OUTPUT_DIR),
    out: Path = typer.Option(STAGE5AI_CONTENT_INDEX_SUMMARY_PATH),
) -> None:
    result = build_content_index(bundle_root=bundle_root, results_dir=results_dir, out=out)
    console.print(f"content_index_records={result['content_index_records']}")
    console.print(f"blocked_private_or_sensitive_count={result['blocked_private_or_sensitive_count']}")


@app.command("build-website-ingest-index")
def build_website_ingest_index_command(
    bundle_root: Path = typer.Option(STAGE5AI_BUNDLE_ROOT),
    results_dir: Path = typer.Option(STAGE5AI_OUTPUT_DIR),
    out: Path = typer.Option(STAGE5AI_WEBSITE_INGEST_FORMAT_PATH),
) -> None:
    result = build_website_ingest_index(bundle_root=bundle_root, results_dir=results_dir, out=out)
    console.print(f"website_ingest_metadata_ready={str(result['website_ingest_metadata_ready']).lower()}")
    console.print(f"website_ingest_source_card_records={result['website_ingest_source_card_records']}")
    console.print(f"website_ingest_content_records={result['website_ingest_content_records']}")


@app.command("build-deep-research-pack-index")
def build_deep_research_pack_index_command(
    bundle_root: Path = typer.Option(STAGE5AI_BUNDLE_ROOT),
    results_dir: Path = typer.Option(STAGE5AI_OUTPUT_DIR),
    out: Path = typer.Option(STAGE5AI_DEEP_RESEARCH_PACK_FORMAT_PATH),
) -> None:
    result = build_deep_research_pack_index(bundle_root=bundle_root, results_dir=results_dir, out=out)
    console.print(f"deep_research_pack_records={result['deep_research_pack_records']}")
    console.print(f"sequential_order_present={str(result['sequential_order_present']).lower()}")


@app.command("build-missing-source-plan")
def build_missing_source_plan_command(
    stage5ag_readiness: Path = typer.Option(STAGE5AG_BUNDLE_READINESS_PATH),
    local_linkage: Path = typer.Option(STAGE5AG_LOCAL_LINKAGE_PATH),
    out: Path = typer.Option(STAGE5AI_MISSING_SOURCE_PLAN_PATH),
    results_dir: Path = typer.Option(STAGE5AI_OUTPUT_DIR),
) -> None:
    result = build_missing_source_plan(
        stage5ag_readiness_path=stage5ag_readiness,
        local_linkage_path=local_linkage,
        out=out,
        results_dir=results_dir,
    )
    console.print(f"missing_source_records={result['missing_source_records']}")
    console.print(f"missing_a1_a2_count={result['missing_a1_a2_count']}")


@app.command("build-stage5ai-guardrail")
def build_stage5ai_guardrail_command(
    bundle_root: Path = typer.Option(STAGE5AI_BUNDLE_ROOT),
    results_dir: Path = typer.Option(STAGE5AI_OUTPUT_DIR),
    out: Path = typer.Option(STAGE5AI_GUARDRAIL_PATH),
) -> None:
    result = build_stage5ai_guardrail(bundle_root=bundle_root, results_dir=results_dir, out=out)
    console.print(f"network_fetch_performed={str(result['network_fetch_performed']).lower()}")
    console.print(f"online_repo_clone_performed={str(result['online_repo_clone_performed']).lower()}")
    console.print(f"google_drive_storage_used={str(result['google_drive_storage_used']).lower()}")


@app.command("build-stage5ai-readiness")
def build_stage5ai_readiness_command(
    bundle_root: Path = typer.Option(STAGE5AI_BUNDLE_ROOT),
    stage5ag_readiness: Path = typer.Option(STAGE5AG_BUNDLE_READINESS_PATH),
    out: Path = typer.Option(STAGE5AI_READINESS_PATH),
) -> None:
    result = build_stage5ai_readiness(bundle_root=bundle_root, stage5ag_readiness_path=stage5ag_readiness, out=out)
    console.print(f"curated_bundle_records={result['curated_bundle_records']}")
    console.print(f"bundles_ready_for_private_deep_research={result['bundles_ready_for_private_deep_research']}")


@app.command("build-stage5ai-next-stage-decision")
def build_stage5ai_next_stage_decision_command(
    readiness: Path = typer.Option(STAGE5AI_READINESS_PATH),
    missing_source_plan: Path = typer.Option(STAGE5AI_MISSING_SOURCE_PLAN_PATH),
    out: Path = typer.Option(STAGE5AI_NEXT_STAGE_DECISION_PATH),
) -> None:
    result = build_stage5ai_next_stage_decision(readiness_path=readiness, missing_source_plan_path=missing_source_plan, out=out)
    console.print(f"selected_option_id={result['selected_option_id']}")


@app.command("build-stage5ai-summary")
def build_stage5ai_summary_command(
    policy: Path = typer.Option(STAGE5AI_POLICY_PATH),
    source_card_summary: Path = typer.Option(STAGE5AI_SOURCE_CARD_SUMMARY_PATH),
    content_index_summary: Path = typer.Option(STAGE5AI_CONTENT_INDEX_SUMMARY_PATH),
    website_ingest_format: Path = typer.Option(STAGE5AI_WEBSITE_INGEST_FORMAT_PATH),
    deep_research_pack_format: Path = typer.Option(STAGE5AI_DEEP_RESEARCH_PACK_FORMAT_PATH),
    bundle_generation_summary: Path = typer.Option(STAGE5AI_BUNDLE_GENERATION_SUMMARY_PATH),
    classification: Path = typer.Option(STAGE5AI_CLASSIFICATION_PATH),
    missing_source_plan: Path = typer.Option(STAGE5AI_MISSING_SOURCE_PLAN_PATH),
    readiness: Path = typer.Option(STAGE5AI_READINESS_PATH),
    guardrail: Path = typer.Option(STAGE5AI_GUARDRAIL_PATH),
    next_stage_decision: Path = typer.Option(STAGE5AI_NEXT_STAGE_DECISION_PATH),
    out: Path = typer.Option(STAGE5AI_SUMMARY_PATH),
    results_dir: Path = typer.Option(STAGE5AI_OUTPUT_DIR),
) -> None:
    result = build_stage5ai_summary(
        policy_path=policy,
        source_card_summary_path=source_card_summary,
        content_index_summary_path=content_index_summary,
        website_ingest_format_path=website_ingest_format,
        deep_research_pack_format_path=deep_research_pack_format,
        bundle_generation_summary_path=bundle_generation_summary,
        classification_path=classification,
        missing_source_plan_path=missing_source_plan,
        readiness_path=readiness,
        guardrail_path=guardrail,
        next_stage_decision_path=next_stage_decision,
        out=out,
        results_dir=results_dir,
    )
    console.print(f"stage_id={result['stage_id']}")
    console.print(f"curated_bundle_records={result['curated_bundle_records']}")
    console.print(f"recommended_next_stage_title={result['recommended_next_stage_title']}")


@app.command("validate-stage5ai")
def validate_stage5ai_command(
    policy: Path = typer.Option(STAGE5AI_POLICY_PATH),
    source_card_summary: Path = typer.Option(STAGE5AI_SOURCE_CARD_SUMMARY_PATH),
    content_index_summary: Path = typer.Option(STAGE5AI_CONTENT_INDEX_SUMMARY_PATH),
    website_ingest_format: Path = typer.Option(STAGE5AI_WEBSITE_INGEST_FORMAT_PATH),
    deep_research_pack_format: Path = typer.Option(STAGE5AI_DEEP_RESEARCH_PACK_FORMAT_PATH),
    bundle_generation_summary: Path = typer.Option(STAGE5AI_BUNDLE_GENERATION_SUMMARY_PATH),
    classification: Path = typer.Option(STAGE5AI_CLASSIFICATION_PATH),
    missing_source_plan: Path = typer.Option(STAGE5AI_MISSING_SOURCE_PLAN_PATH),
    readiness: Path = typer.Option(STAGE5AI_READINESS_PATH),
    guardrail: Path = typer.Option(STAGE5AI_GUARDRAIL_PATH),
    next_stage_decision: Path = typer.Option(STAGE5AI_NEXT_STAGE_DECISION_PATH),
    summary: Path = typer.Option(STAGE5AI_SUMMARY_PATH),
    bundle_root: Path = typer.Option(STAGE5AI_BUNDLE_ROOT),
    results_dir: Path = typer.Option(STAGE5AI_OUTPUT_DIR),
) -> None:
    counts, errors = validate_stage5ai(
        policy_path=policy,
        source_card_summary_path=source_card_summary,
        content_index_summary_path=content_index_summary,
        website_ingest_format_path=website_ingest_format,
        deep_research_pack_format_path=deep_research_pack_format,
        bundle_generation_summary_path=bundle_generation_summary,
        classification_path=classification,
        missing_source_plan_path=missing_source_plan,
        readiness_path=readiness,
        guardrail_path=guardrail,
        next_stage_decision_path=next_stage_decision,
        summary_path=summary,
        bundle_root=bundle_root,
        results_dir=results_dir,
    )
    for key, value in counts.items():
        console.print(f"{key}={str(value).lower() if isinstance(value, bool) else value}")
    console.print(f"validation_error_count={len(errors)}")
    for error in errors:
        console.print(error)
    if errors:
        raise typer.Exit(1)
    console.print("source_harvester_stage5ai_valid=true")


@app.command("inventory-usefulfiles")
def inventory_usefulfiles_command(
    source_root: Path = typer.Option(STAGE5AJ_SOURCE_ROOT),
    results_dir: Path = typer.Option(STAGE5AJ_OUTPUT_DIR),
    out: Path = typer.Option(STAGE5AJ_INVENTORY_PATH),
) -> None:
    result = inventory_usefulfiles(source_root=source_root, results_dir=results_dir, out=out)
    console.print(f"local_folder_exists={str(result['local_folder_exists']).lower()}")
    console.print(f"usefulfiles_local_file_count={result['usefulfiles_local_file_count']}")
    console.print(f"xlsx_files_found={result['xlsx_files_found']}")


@app.command("extract-xlsx-metadata")
def extract_xlsx_metadata_command(
    source_root: Path = typer.Option(STAGE5AJ_SOURCE_ROOT),
    results_dir: Path = typer.Option(STAGE5AJ_OUTPUT_DIR),
    out: Path = typer.Option(STAGE5AJ_XLSX_SUMMARY_PATH),
) -> None:
    result = extract_xlsx_metadata(source_root=source_root, results_dir=results_dir, out=out)
    console.print(f"xlsx_workbooks_detected={result['xlsx_workbooks_detected']}")
    console.print(f"xlsx_workbooks_summarized={result['xlsx_workbooks_summarized']}")
    console.print(f"lp_excel_detected={str(result['lp_excel_detected']).lower()}")


@app.command("parse-important-links")
def parse_important_links_command(
    source_root: Path = typer.Option(STAGE5AJ_SOURCE_ROOT),
    existing_manifest: Path = typer.Option(SOURCE_MANIFEST_PATH),
    results_dir: Path = typer.Option(STAGE5AJ_OUTPUT_DIR),
    out: Path = typer.Option(STAGE5AJ_IMPORTANT_LINKS_PATH),
    out_manifest_extension: Path = typer.Option(STAGE5AJ_MANIFEST_EXTENSION_PATH),
) -> None:
    result = parse_important_links(
        source_root=source_root,
        existing_manifest_path=existing_manifest,
        results_dir=results_dir,
        out=out,
        out_manifest_extension=out_manifest_extension,
    )
    console.print(f"important_links_urls_found={result['important_links_urls_found']}")
    console.print(f"important_links_new_urls={result['important_links_new_urls']}")
    console.print(f"manifest_extension_records={result['manifest_extension_records']}")


@app.command("build-usefulfiles-source-cards")
def build_usefulfiles_source_cards_command(
    inventory: Path = typer.Option(STAGE5AJ_INVENTORY_PATH),
    xlsx_summary: Path = typer.Option(STAGE5AJ_XLSX_SUMMARY_PATH),
    important_links: Path = typer.Option(STAGE5AJ_IMPORTANT_LINKS_PATH),
    manifest_extension: Path = typer.Option(STAGE5AJ_MANIFEST_EXTENSION_PATH),
    bundle_plan: Path = typer.Option(RESEARCH_BUNDLE_PLAN_PATH),
    out_source_card_summary: Path = typer.Option(STAGE5AJ_SOURCE_CARD_SUMMARY_PATH),
    out_content_index_summary: Path = typer.Option(STAGE5AJ_CONTENT_INDEX_SUMMARY_PATH),
    results_dir: Path = typer.Option(STAGE5AJ_OUTPUT_DIR),
) -> None:
    result = build_usefulfiles_source_cards(
        inventory_path=inventory,
        xlsx_summary_path=xlsx_summary,
        important_links_path=important_links,
        manifest_extension_path=manifest_extension,
        bundle_plan_path=bundle_plan,
        out_source_card_summary=out_source_card_summary,
        out_content_index_summary=out_content_index_summary,
        results_dir=results_dir,
    )
    console.print(f"source_card_updates={result['source_card_records']}")
    console.print(f"content_index_updates={result['content_index_records']}")


@app.command("build-scraper-capture-policy")
def build_scraper_capture_policy_command(
    out: Path = typer.Option(STAGE5AJ_SCRAPER_POLICY_PATH),
    results_dir: Path = typer.Option(STAGE5AJ_OUTPUT_DIR),
) -> None:
    result = build_scraper_capture_policy(out=out, results_dir=results_dir)
    console.print(f"scraper_capture_policy_created={str(bool(result['capture_profiles'])).lower()}")


@app.command("build-redaction-policy")
def build_redaction_policy_command(
    out: Path = typer.Option(STAGE5AJ_REDACTION_POLICY_PATH),
    results_dir: Path = typer.Option(STAGE5AJ_OUTPUT_DIR),
) -> None:
    result = build_redaction_policy(out=out, results_dir=results_dir)
    console.print(f"redaction_log_required={str(result['redaction_log_required']).lower()}")


@app.command("build-extraction-fidelity-policy")
def build_extraction_fidelity_policy_command(
    out: Path = typer.Option(STAGE5AJ_FIDELITY_POLICY_PATH),
    results_dir: Path = typer.Option(STAGE5AJ_OUTPUT_DIR),
) -> None:
    result = build_extraction_fidelity_policy(out=out, results_dir=results_dir)
    console.print(
        "no_over_redaction_policy_created="
        f"{str(result['private_deep_research_extract_view']['minimal_redaction_only']).lower()}"
    )


@app.command("build-stage5aj-new-clue-categories")
def build_stage5aj_new_clue_categories_command(
    out: Path = typer.Option(STAGE5AJ_NEW_CLUE_CATEGORIES_PATH),
) -> None:
    result = build_stage5aj_new_clue_categories(out=out)
    console.print(f"new_clue_category_records={result['new_clue_category_records']}")


@app.command("update-deep-research-packs")
def update_deep_research_packs_command(
    stage5ai_bundle_root: Path = typer.Option(STAGE5AI_BUNDLE_ROOT),
    usefulfiles_inventory: Path = typer.Option(STAGE5AJ_INVENTORY_PATH),
    source_card_summary: Path = typer.Option(STAGE5AJ_SOURCE_CARD_SUMMARY_PATH),
    content_index_summary: Path = typer.Option(STAGE5AJ_CONTENT_INDEX_SUMMARY_PATH),
    bundle_root: Path = typer.Option(STAGE5AJ_BUNDLE_ROOT),
    results_dir: Path = typer.Option(STAGE5AJ_OUTPUT_DIR),
    out_website_update: Path = typer.Option(STAGE5AJ_WEBSITE_UPDATE_PATH),
    out_deep_research_update: Path = typer.Option(STAGE5AJ_DEEP_RESEARCH_UPDATE_PATH),
    out_readiness: Path = typer.Option(STAGE5AJ_READINESS_PATH),
    out_missing_source_plan: Path = typer.Option(STAGE5AJ_MISSING_SOURCE_PLAN_PATH),
) -> None:
    result = update_deep_research_packs(
        stage5ai_bundle_root=stage5ai_bundle_root,
        usefulfiles_inventory_path=usefulfiles_inventory,
        source_card_summary_path=source_card_summary,
        content_index_summary_path=content_index_summary,
        bundle_root=bundle_root,
        results_dir=results_dir,
        out_website_update=out_website_update,
        out_deep_research_update=out_deep_research_update,
        out_readiness=out_readiness,
        out_missing_source_plan=out_missing_source_plan,
    )
    console.print(f"deep_research_pack_updates={result['deep_research_pack_records']}")
    console.print(
        "bundles_ready_for_private_deep_research="
        f"{result['readiness']['bundles_ready_for_private_deep_research']}"
    )


@app.command("build-stage5aj-guardrail")
def build_stage5aj_guardrail_command(
    source_root: Path = typer.Option(STAGE5AJ_SOURCE_ROOT),
    results_dir: Path = typer.Option(STAGE5AJ_OUTPUT_DIR),
    out: Path = typer.Option(STAGE5AJ_GUARDRAIL_PATH),
) -> None:
    result = build_stage5aj_guardrail(source_root=source_root, results_dir=results_dir, out=out)
    console.print(f"network_fetch_performed={str(result['network_fetch_performed']).lower()}")
    console.print(f"raw_xlsx_committed={str(result['raw_xlsx_committed']).lower()}")
    console.print(f"new_cuda_kernels_added={result['new_cuda_kernels_added']}")


@app.command("build-stage5aj-next-stage-decision")
def build_stage5aj_next_stage_decision_command(
    summary_inputs: list[Path] = typer.Option(...),
    out: Path = typer.Option(STAGE5AJ_NEXT_STAGE_DECISION_PATH),
) -> None:
    if len(summary_inputs) != 2:
        raise typer.BadParameter("--summary-inputs requires readiness and missing-source-plan paths")
    result = build_stage5aj_next_stage_decision(summary_inputs=summary_inputs, out=out)
    console.print(f"selected_option_id={result['selected_option_id']}")


@app.command("build-stage5aj-summary")
def build_stage5aj_summary_command(
    inventory: Path = typer.Option(STAGE5AJ_INVENTORY_PATH),
    manifest_extension: Path = typer.Option(STAGE5AJ_MANIFEST_EXTENSION_PATH),
    source_card_summary: Path = typer.Option(STAGE5AJ_SOURCE_CARD_SUMMARY_PATH),
    content_index_summary: Path = typer.Option(STAGE5AJ_CONTENT_INDEX_SUMMARY_PATH),
    xlsx_summary: Path = typer.Option(STAGE5AJ_XLSX_SUMMARY_PATH),
    important_links: Path = typer.Option(STAGE5AJ_IMPORTANT_LINKS_PATH),
    new_clue_categories: Path = typer.Option(STAGE5AJ_NEW_CLUE_CATEGORIES_PATH),
    fidelity_policy: Path = typer.Option(STAGE5AJ_FIDELITY_POLICY_PATH),
    redaction_policy: Path = typer.Option(STAGE5AJ_REDACTION_POLICY_PATH),
    scraper_policy: Path = typer.Option(STAGE5AJ_SCRAPER_POLICY_PATH),
    website_update: Path = typer.Option(STAGE5AJ_WEBSITE_UPDATE_PATH),
    deep_research_update: Path = typer.Option(STAGE5AJ_DEEP_RESEARCH_UPDATE_PATH),
    readiness: Path = typer.Option(STAGE5AJ_READINESS_PATH),
    missing_source_plan: Path = typer.Option(STAGE5AJ_MISSING_SOURCE_PLAN_PATH),
    guardrail: Path = typer.Option(STAGE5AJ_GUARDRAIL_PATH),
    next_stage_decision: Path = typer.Option(STAGE5AJ_NEXT_STAGE_DECISION_PATH),
    out: Path = typer.Option(STAGE5AJ_SUMMARY_PATH),
    results_dir: Path = typer.Option(STAGE5AJ_OUTPUT_DIR),
) -> None:
    result = build_stage5aj_summary(
        inventory_path=inventory,
        manifest_extension_path=manifest_extension,
        source_card_summary_path=source_card_summary,
        content_index_summary_path=content_index_summary,
        xlsx_summary_path=xlsx_summary,
        important_links_path=important_links,
        new_clue_categories_path=new_clue_categories,
        fidelity_policy_path=fidelity_policy,
        redaction_policy_path=redaction_policy,
        scraper_policy_path=scraper_policy,
        website_update_path=website_update,
        deep_research_update_path=deep_research_update,
        readiness_path=readiness,
        missing_source_plan_path=missing_source_plan,
        guardrail_path=guardrail,
        next_stage_decision_path=next_stage_decision,
        out=out,
        results_dir=results_dir,
    )
    console.print(f"stage_id={result['stage_id']}")
    console.print(f"new_local_source_records={result['new_local_source_records']}")
    console.print(f"recommended_next_stage_title={result['recommended_next_stage_title']}")


@app.command("validate-stage5aj")
def validate_stage5aj_command(
    inventory: Path = typer.Option(STAGE5AJ_INVENTORY_PATH),
    manifest_extension: Path = typer.Option(STAGE5AJ_MANIFEST_EXTENSION_PATH),
    source_card_summary: Path = typer.Option(STAGE5AJ_SOURCE_CARD_SUMMARY_PATH),
    content_index_summary: Path = typer.Option(STAGE5AJ_CONTENT_INDEX_SUMMARY_PATH),
    xlsx_summary: Path = typer.Option(STAGE5AJ_XLSX_SUMMARY_PATH),
    important_links: Path = typer.Option(STAGE5AJ_IMPORTANT_LINKS_PATH),
    new_clue_categories: Path = typer.Option(STAGE5AJ_NEW_CLUE_CATEGORIES_PATH),
    fidelity_policy: Path = typer.Option(STAGE5AJ_FIDELITY_POLICY_PATH),
    redaction_policy: Path = typer.Option(STAGE5AJ_REDACTION_POLICY_PATH),
    scraper_policy: Path = typer.Option(STAGE5AJ_SCRAPER_POLICY_PATH),
    website_update: Path = typer.Option(STAGE5AJ_WEBSITE_UPDATE_PATH),
    deep_research_update: Path = typer.Option(STAGE5AJ_DEEP_RESEARCH_UPDATE_PATH),
    readiness: Path = typer.Option(STAGE5AJ_READINESS_PATH),
    missing_source_plan: Path = typer.Option(STAGE5AJ_MISSING_SOURCE_PLAN_PATH),
    guardrail: Path = typer.Option(STAGE5AJ_GUARDRAIL_PATH),
    next_stage_decision: Path = typer.Option(STAGE5AJ_NEXT_STAGE_DECISION_PATH),
    summary: Path = typer.Option(STAGE5AJ_SUMMARY_PATH),
    results_dir: Path = typer.Option(STAGE5AJ_OUTPUT_DIR),
) -> None:
    counts, errors = validate_stage5aj(
        inventory_path=inventory,
        manifest_extension_path=manifest_extension,
        source_card_summary_path=source_card_summary,
        content_index_summary_path=content_index_summary,
        xlsx_summary_path=xlsx_summary,
        important_links_path=important_links,
        new_clue_categories_path=new_clue_categories,
        fidelity_policy_path=fidelity_policy,
        redaction_policy_path=redaction_policy,
        scraper_policy_path=scraper_policy,
        website_update_path=website_update,
        deep_research_update_path=deep_research_update,
        readiness_path=readiness,
        missing_source_plan_path=missing_source_plan,
        guardrail_path=guardrail,
        next_stage_decision_path=next_stage_decision,
        summary_path=summary,
        results_dir=results_dir,
    )
    for key, value in counts.items():
        console.print(f"{key}={str(value).lower() if isinstance(value, bool) else value}")
    console.print(f"validation_error_count={len(errors)}")
    for error in errors:
        console.print(error)
    if errors:
        raise typer.Exit(1)
    console.print("source_harvester_stage5aj_valid=true")


@app.command("inventory-community-facts")
def inventory_community_facts_command(
    source_root: Path = typer.Option(STAGE5AK_SOURCE_ROOT),
    results_dir: Path = typer.Option(STAGE5AK_OUTPUT_DIR),
    out: Path = typer.Option(STAGE5AK_INVENTORY_PATH),
) -> None:
    result = inventory_community_facts(source_root=source_root, results_dir=results_dir, out=out)
    console.print(f"local_folder_exists={str(result['local_folder_exists']).lower()}")
    console.print(f"community_facts_file_count={result['community_facts_file_count']}")
    console.print(f"message_log_detected={str(result['message_log_detected']).lower()}")


@app.command("build-community-attachment-index")
def build_community_attachment_index_command(
    source_root: Path = typer.Option(STAGE5AK_SOURCE_ROOT),
    results_dir: Path = typer.Option(STAGE5AK_OUTPUT_DIR),
    out: Path = typer.Option(STAGE5AK_ATTACHMENT_INDEX_PATH),
) -> None:
    result = build_community_attachment_index(source_root=source_root, results_dir=results_dir, out=out)
    console.print(f"attachment_index_records={result['attachment_index_records']}")
    console.print(f"attachment_images_detected={result['attachment_images_detected']}")


@app.command("build-community-facts-source-cards")
def build_community_facts_source_cards_command(
    inventory: Path = typer.Option(STAGE5AK_INVENTORY_PATH),
    attachment_index: Path = typer.Option(STAGE5AK_ATTACHMENT_INDEX_PATH),
    bundle_plan: Path = typer.Option(RESEARCH_BUNDLE_PLAN_PATH),
    out_source_card_summary: Path = typer.Option(STAGE5AK_SOURCE_CARD_SUMMARY_PATH),
    out_content_index_summary: Path = typer.Option(STAGE5AK_CONTENT_INDEX_SUMMARY_PATH),
    results_dir: Path = typer.Option(STAGE5AK_OUTPUT_DIR),
) -> None:
    result = build_community_facts_source_cards(
        inventory_path=inventory,
        attachment_index_path=attachment_index,
        bundle_plan_path=bundle_plan,
        out_source_card_summary=out_source_card_summary,
        out_content_index_summary=out_content_index_summary,
        results_dir=results_dir,
    )
    console.print(f"source_card_updates={result['source_card_updates']}")
    console.print(f"content_index_updates={result['content_index_records']}")


@app.command("build-community-claim-records")
def build_community_claim_records_command(
    source_root: Path = typer.Option(STAGE5AK_SOURCE_ROOT),
    attachment_index: Path = typer.Option(STAGE5AK_ATTACHMENT_INDEX_PATH),
    claim_policy_out: Path = typer.Option(STAGE5AK_CLAIM_POLICY_PATH),
    claim_records_out: Path = typer.Option(STAGE5AK_CLAIM_RECORDS_PATH),
    correction_log_out: Path = typer.Option(STAGE5AK_CORRECTION_LOG_PATH),
    clue_categories_out: Path = typer.Option(STAGE5AK_CLUE_CATEGORIES_PATH),
    results_dir: Path = typer.Option(STAGE5AK_OUTPUT_DIR),
) -> None:
    result = build_community_claim_records(
        source_root=source_root,
        attachment_index_path=attachment_index,
        claim_policy_out=claim_policy_out,
        claim_records_out=claim_records_out,
        correction_log_out=correction_log_out,
        clue_categories_out=clue_categories_out,
        results_dir=results_dir,
    )
    console.print(f"claim_record_count={result['claims']['claim_record_count']}")
    console.print(f"correction_record_count={result['corrections']['correction_record_count']}")
    console.print(f"new_clue_category_records={result['categories']['new_clue_category_records']}")


@app.command("build-community-arithmetic-preflight")
def build_community_arithmetic_preflight_command(
    claim_records: Path = typer.Option(STAGE5AK_CLAIM_RECORDS_PATH),
    correction_log: Path = typer.Option(STAGE5AK_CORRECTION_LOG_PATH),
    out: Path = typer.Option(STAGE5AK_ARITHMETIC_PREFLIGHT_PATH),
    results_dir: Path = typer.Option(STAGE5AK_OUTPUT_DIR),
) -> None:
    result = build_community_arithmetic_preflight(
        claim_records_path=claim_records,
        correction_log_path=correction_log,
        out=out,
        results_dir=results_dir,
    )
    console.print(f"arithmetic_preflight_records={result['arithmetic_preflight_records']}")
    console.print(f"arithmetic_verified_count={result['arithmetic_verified_count']}")
    console.print(f"arithmetic_error_count={result['arithmetic_error_count']}")


@app.command("update-community-deep-research-packs")
def update_community_deep_research_packs_command(
    stage5aj_bundle_root: Path = typer.Option(STAGE5AJ_BUNDLE_ROOT),
    source_card_summary: Path = typer.Option(STAGE5AK_SOURCE_CARD_SUMMARY_PATH),
    content_index_summary: Path = typer.Option(STAGE5AK_CONTENT_INDEX_SUMMARY_PATH),
    claim_records: Path = typer.Option(STAGE5AK_CLAIM_RECORDS_PATH),
    correction_log: Path = typer.Option(STAGE5AK_CORRECTION_LOG_PATH),
    bundle_root: Path = typer.Option(STAGE5AK_BUNDLE_ROOT),
    results_dir: Path = typer.Option(STAGE5AK_OUTPUT_DIR),
    out_website_update: Path = typer.Option(STAGE5AK_WEBSITE_UPDATE_PATH),
    out_deep_research_update: Path = typer.Option(STAGE5AK_DEEP_RESEARCH_UPDATE_PATH),
    out_readiness: Path = typer.Option(STAGE5AK_READINESS_PATH),
    out_missing_source_plan: Path = typer.Option(STAGE5AK_MISSING_SOURCE_PLAN_PATH),
) -> None:
    result = update_community_deep_research_packs(
        stage5aj_bundle_root=stage5aj_bundle_root,
        source_card_summary_path=source_card_summary,
        content_index_summary_path=content_index_summary,
        claim_records_path=claim_records,
        correction_log_path=correction_log,
        bundle_root=bundle_root,
        results_dir=results_dir,
        out_website_update=out_website_update,
        out_deep_research_update=out_deep_research_update,
        out_readiness=out_readiness,
        out_missing_source_plan=out_missing_source_plan,
    )
    console.print(f"deep_research_pack_updates={result['deep']['deep_research_pack_updates']}")
    console.print(
        "bundles_ready_for_private_deep_research="
        f"{result['readiness']['bundles_ready_for_private_deep_research']}"
    )


@app.command("build-stage5ak-guardrail")
def build_stage5ak_guardrail_command(
    source_root: Path = typer.Option(STAGE5AK_SOURCE_ROOT),
    results_dir: Path = typer.Option(STAGE5AK_OUTPUT_DIR),
    out: Path = typer.Option(STAGE5AK_GUARDRAIL_PATH),
) -> None:
    result = build_stage5ak_guardrail(source_root=source_root, results_dir=results_dir, out=out)
    console.print(f"network_fetch_performed={str(result['network_fetch_performed']).lower()}")
    console.print(f"raw_text_committed={str(result['raw_text_committed']).lower()}")
    console.print(f"new_cuda_kernels_added={result['new_cuda_kernels_added']}")


@app.command("build-stage5ak-next-stage-decision")
def build_stage5ak_next_stage_decision_command(
    readiness: Path = typer.Option(STAGE5AK_READINESS_PATH),
    claim_records: Path = typer.Option(STAGE5AK_CLAIM_RECORDS_PATH),
    missing_source_plan: Path = typer.Option(STAGE5AK_MISSING_SOURCE_PLAN_PATH),
    out: Path = typer.Option(STAGE5AK_NEXT_STAGE_DECISION_PATH),
) -> None:
    result = build_stage5ak_next_stage_decision(
        readiness_path=readiness,
        claim_records_path=claim_records,
        missing_source_plan_path=missing_source_plan,
        out=out,
    )
    console.print(f"selected_option_id={result['selected_option_id']}")


@app.command("build-stage5ak-summary")
def build_stage5ak_summary_command(
    inventory: Path = typer.Option(STAGE5AK_INVENTORY_PATH),
    source_card_summary: Path = typer.Option(STAGE5AK_SOURCE_CARD_SUMMARY_PATH),
    content_index_summary: Path = typer.Option(STAGE5AK_CONTENT_INDEX_SUMMARY_PATH),
    attachment_index: Path = typer.Option(STAGE5AK_ATTACHMENT_INDEX_PATH),
    clue_categories: Path = typer.Option(STAGE5AK_CLUE_CATEGORIES_PATH),
    claim_policy: Path = typer.Option(STAGE5AK_CLAIM_POLICY_PATH),
    claim_records: Path = typer.Option(STAGE5AK_CLAIM_RECORDS_PATH),
    correction_log: Path = typer.Option(STAGE5AK_CORRECTION_LOG_PATH),
    arithmetic_preflight: Path = typer.Option(STAGE5AK_ARITHMETIC_PREFLIGHT_PATH),
    website_update: Path = typer.Option(STAGE5AK_WEBSITE_UPDATE_PATH),
    deep_research_update: Path = typer.Option(STAGE5AK_DEEP_RESEARCH_UPDATE_PATH),
    readiness: Path = typer.Option(STAGE5AK_READINESS_PATH),
    missing_source_plan: Path = typer.Option(STAGE5AK_MISSING_SOURCE_PLAN_PATH),
    guardrail: Path = typer.Option(STAGE5AK_GUARDRAIL_PATH),
    next_stage_decision: Path = typer.Option(STAGE5AK_NEXT_STAGE_DECISION_PATH),
    out: Path = typer.Option(STAGE5AK_SUMMARY_PATH),
    results_dir: Path = typer.Option(STAGE5AK_OUTPUT_DIR),
) -> None:
    result = build_stage5ak_summary(
        inventory_path=inventory,
        source_card_summary_path=source_card_summary,
        content_index_summary_path=content_index_summary,
        attachment_index_path=attachment_index,
        clue_categories_path=clue_categories,
        claim_policy_path=claim_policy,
        claim_records_path=claim_records,
        correction_log_path=correction_log,
        arithmetic_preflight_path=arithmetic_preflight,
        website_update_path=website_update,
        deep_research_update_path=deep_research_update,
        readiness_path=readiness,
        missing_source_plan_path=missing_source_plan,
        guardrail_path=guardrail,
        next_stage_decision_path=next_stage_decision,
        out=out,
        results_dir=results_dir,
    )
    console.print(f"stage_id={result['stage_id']}")
    console.print(f"community_claim_records={result['community_claim_records']}")
    console.print(f"recommended_next_stage_title={result['recommended_next_stage_title']}")


@app.command("validate-stage5ak")
def validate_stage5ak_command(
    inventory: Path = typer.Option(STAGE5AK_INVENTORY_PATH),
    source_card_summary: Path = typer.Option(STAGE5AK_SOURCE_CARD_SUMMARY_PATH),
    content_index_summary: Path = typer.Option(STAGE5AK_CONTENT_INDEX_SUMMARY_PATH),
    attachment_index: Path = typer.Option(STAGE5AK_ATTACHMENT_INDEX_PATH),
    clue_categories: Path = typer.Option(STAGE5AK_CLUE_CATEGORIES_PATH),
    claim_policy: Path = typer.Option(STAGE5AK_CLAIM_POLICY_PATH),
    claim_records: Path = typer.Option(STAGE5AK_CLAIM_RECORDS_PATH),
    correction_log: Path = typer.Option(STAGE5AK_CORRECTION_LOG_PATH),
    arithmetic_preflight: Path = typer.Option(STAGE5AK_ARITHMETIC_PREFLIGHT_PATH),
    website_update: Path = typer.Option(STAGE5AK_WEBSITE_UPDATE_PATH),
    deep_research_update: Path = typer.Option(STAGE5AK_DEEP_RESEARCH_UPDATE_PATH),
    readiness: Path = typer.Option(STAGE5AK_READINESS_PATH),
    missing_source_plan: Path = typer.Option(STAGE5AK_MISSING_SOURCE_PLAN_PATH),
    guardrail: Path = typer.Option(STAGE5AK_GUARDRAIL_PATH),
    next_stage_decision: Path = typer.Option(STAGE5AK_NEXT_STAGE_DECISION_PATH),
    summary: Path = typer.Option(STAGE5AK_SUMMARY_PATH),
    results_dir: Path = typer.Option(STAGE5AK_OUTPUT_DIR),
) -> None:
    counts, errors = validate_stage5ak(
        inventory_path=inventory,
        source_card_summary_path=source_card_summary,
        content_index_summary_path=content_index_summary,
        attachment_index_path=attachment_index,
        clue_categories_path=clue_categories,
        claim_policy_path=claim_policy,
        claim_records_path=claim_records,
        correction_log_path=correction_log,
        arithmetic_preflight_path=arithmetic_preflight,
        website_update_path=website_update,
        deep_research_update_path=deep_research_update,
        readiness_path=readiness,
        missing_source_plan_path=missing_source_plan,
        guardrail_path=guardrail,
        next_stage_decision_path=next_stage_decision,
        summary_path=summary,
        results_dir=results_dir,
    )
    for key, value in counts.items():
        console.print(f"{key}={str(value).lower() if isinstance(value, bool) else value}")
    console.print(f"validation_error_count={len(errors)}")
    for error in errors:
        console.print(error)
    if errors:
        raise typer.Exit(1)
    console.print("source_harvester_stage5ak_valid=true")


def register(root_app: typer.Typer) -> None:
    root_app.add_typer(app, name="source-harvester")
