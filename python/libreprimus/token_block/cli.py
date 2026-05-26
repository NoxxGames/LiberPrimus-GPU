"""Typer CLI for Stage 5AP token-block source-lock records."""

from __future__ import annotations

from pathlib import Path

import typer
from rich.console import Console

from .alphabets import build_alphabet_registry
from .case_policy import build_case_policy
from .coordinates import build_coordinate_records
from .coordinate_validation import validate_coordinate_payload
from .dwh_context import build_dwh_context
from .mapping import build_mapping_preflight
from .models import (
    ALPHABET_PATH,
    COORDINATE_PATH,
    DWH_CONTEXT_PATH,
    IMAGE_PROVENANCE_PATH,
    MAPPING_PATH,
    NEXT_STAGE_DECISION_PATH,
    NULL_CONTROL_PATH,
    RESEARCH_SUMMARY_PATH,
    RESULTS_DIR,
    SOURCE_LOCK_PATH,
    SUMMARY_PATH,
    STAGE5AR_CASE_AMBIGUITIES_PATH,
    STAGE5AR_CASE_POLICY_PATH,
    STAGE5AR_COORDINATE_VALIDATION_PATH,
    STAGE5AR_DWH_CONTEXT_PATH,
    STAGE5AR_GUARDRAIL_PATH,
    STAGE5AR_IMAGE_VARIANTS_PATH,
    STAGE5AR_NEXT_STAGE_DECISION_PATH,
    STAGE5AR_NULL_CONTROL_UPDATE_PATH,
    STAGE5AR_ORIGINAL_SOURCE_LOCK_PATH,
    STAGE5AR_PAGE_SPLIT_POLICY_PATH,
    STAGE5AR_PAGE_SPLIT_RECORDS_PATH,
    STAGE5AR_PIXEL_COORDINATE_POLICY_PATH,
    STAGE5AR_PIXEL_COORDINATE_RECORDS_PATH,
    STAGE5AR_RESULTS_DIR,
    STAGE5AR_SOURCE_LOCK_UPDATE_PATH,
    STAGE5AR_SUMMARY_PATH,
    STAGE5AT_CANONICAL_CHALLENGE_SET_PATH,
    STAGE5AT_CASE_REVIEW_CHALLENGE_SET_PATH,
    STAGE5AT_CASE_REVIEW_POLICY_PATH,
    STAGE5AT_CROP_MANIFEST_PATH,
    STAGE5AT_DECISION_TEMPLATE_PATH,
    STAGE5AT_DOC_DRIFT_PATH,
    STAGE5AT_DWH_CASE_CONTEXT_PATH,
    STAGE5AT_GUARDRAIL_PATH,
    STAGE5AT_NEXT_STAGE_DECISION_PATH,
    STAGE5AT_NULL_CONTROL_UPDATE_PATH,
    STAGE5AT_PACK_MANIFEST_PATH,
    STAGE5AT_RESULTS_DIR,
    STAGE5AT_REVIEW_PACK_ROOT,
    STAGE5AT_SUMMARY_PATH,
    STAGE5AT_VARIANT_REPAIR_PATH,
    STAGE5AU_CANONICAL_CHALLENGES_V2_PATH,
    STAGE5AU_CASE_CHALLENGES_V2_PATH,
    STAGE5AU_CROP_GEOMETRY_POLICY_PATH,
    STAGE5AU_CROP_QUALITY_PATH,
    STAGE5AU_DECISION_TEMPLATE_PATH,
    STAGE5AU_DWH_CONTEXT_PATH,
    STAGE5AU_GUARDRAIL_PATH,
    STAGE5AU_NEXT_STAGE_DECISION_PATH,
    STAGE5AU_NULL_CONTROL_UPDATE_PATH,
    STAGE5AU_PACK_MANIFEST_PATH,
    STAGE5AU_RESULTS_DIR,
    STAGE5AU_REVIEW_PACK_ROOT,
    STAGE5AU_SUMMARY_PATH,
    STAGE5AU_UI_COVERAGE_PATH,
    STAGE5AU_USABILITY_AUDIT_PATH,
    STAGE5AV_BRANCH_MANIFEST_PATH,
    STAGE5AV_CANONICAL_UPDATE_PATH,
    STAGE5AV_CONFIRMED_TOKENS_PATH,
    STAGE5AV_DECISION_FILE_INGEST_PATH,
    STAGE5AV_DECISION_FILE_VALIDATION_PATH,
    STAGE5AV_DWH_CONTEXT_PATH,
    STAGE5AV_GUARDRAIL_PATH,
    STAGE5AV_HUMAN_REVIEW_DECISIONS_PATH,
    STAGE5AV_LOCAL_DECISION_TEMPLATE_PATH,
    STAGE5AV_NEXT_STAGE_DECISION_PATH,
    STAGE5AV_NULL_CONTROL_UPDATE_PATH,
    STAGE5AV_PRIMARY60_IMPACT_PATH,
    STAGE5AV_RESULTS_DIR,
    STAGE5AV_REVIEWER_EXTRA_TOKENS_PATH,
    STAGE5AV_SUMMARY_PATH,
    STAGE5AV_UNRESOLVED_VARIANTS_PATH,
    STAGE5AW_CANONICAL_UPDATE_PATH,
    STAGE5AW_DECISION_PARSER_AUDIT_PATH,
    STAGE5AW_DWH_CONTEXT_PATH,
    STAGE5AW_GUARDRAIL_PATH,
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
    STAGE5AY_ALPHABET_CONTROL_MANIFEST_PATH,
    STAGE5AY_BOUNDED_VARIANT_FAMILY_MANIFEST_PATH,
    STAGE5AY_BRANCH_COUNT_BUDGET_PATH,
    STAGE5AY_BRANCH_ELIGIBILITY_POLICY_PATH,
    STAGE5AY_DWH_PREFLIGHT_CONTEXT_PATH,
    STAGE5AY_EXECUTION_GATES_PATH,
    STAGE5AY_FUTURE_RESULT_SCHEMA_PREVIEW_PATH,
    STAGE5AY_GUARDRAIL_PATH,
    STAGE5AY_NEXT_STAGE_DECISION_PATH,
    STAGE5AY_NULL_CONTROL_FAMILY_MANIFEST_PATH,
    STAGE5AY_PAGE_SPLIT_CONTROL_MANIFEST_PATH,
    STAGE5AY_PREFLIGHT_DESIGN_POLICY_PATH,
    STAGE5AY_PREFLIGHT_SOURCE_INPUTS_PATH,
    STAGE5AY_READING_ORDER_CONTROL_MANIFEST_PATH,
    STAGE5AY_RESULTS_DIR,
    STAGE5AY_SOURCE_CONTROL_MANIFEST_PATH,
    STAGE5AY_SUMMARY_PATH,
    TRANSCRIPTION_PATH,
    read_yaml,
)
from .null_controls import build_null_control_plan
from .original_images import build_original_image_source_lock
from .page_split import build_page_split
from .pixel_coordinates import build_pixel_coordinates
from .provenance import build_source_lock
from .stage5ap import build_next_stage_decision, build_research_summary, build_summary
from .stage5ar import build_stage5ar_summary, build_stage5ar_updates, validate_stage5ar
from .stage5at import (
    build_case_challenge_sets,
    build_case_review_policy,
    build_doc_drift_repair_summary,
    build_dwh_case_context,
    build_null_control_case_update,
    build_review_pack,
    build_stage5at_summary,
    validate_stage5at,
)
from .stage5au import (
    audit_stage5at_review_pack_usability,
    build_crop_geometry_policy,
    build_review_pack_v2,
    build_stage5au_dwh_review_pack_context,
    build_stage5au_null_control_update,
    build_stage5au_summary,
    validate_stage5au,
)
from .stage5av import (
    build_stage5av_decision_records,
    build_stage5av_summary,
    build_stage5av_updates,
    build_stage5av_variant_branch_manifest,
    ingest_stage5av_decisions,
    validate_stage5av,
)
from .stage5aw import (
    audit_stage5aw_decision_parser,
    build_stage5aw_repaired_branch_manifest,
    build_stage5aw_summary,
    build_stage5aw_updates,
    repair_stage5aw_decision_variants,
    validate_stage5aw,
)
from .stage5ay import (
    build_stage5ay_control_manifests,
    build_stage5ay_execution_gates,
    build_stage5ay_preflight_design,
    build_stage5ay_summary,
    validate_stage5ay,
)
from .transcription import build_transcription
from .validation import validate_stage5ap
from .variant_classifier import build_variant_classifier_repair_summary

console = Console()
app = typer.Typer(help="Stage 5AP page 49-51 token-block commands.", no_args_is_help=True)


@app.command("build-stage5ap-source-lock")
def build_stage5ap_source_lock_command(
    search_roots: list[Path] | None = typer.Option(None),
    results_dir: Path = typer.Option(RESULTS_DIR),
    out_source_lock: Path = typer.Option(SOURCE_LOCK_PATH),
    out_image_provenance: Path = typer.Option(IMAGE_PROVENANCE_PATH),
) -> None:
    roots = search_roots or [Path("third_party/LiberPrimusPages"), Path("data"), Path("research-inputs"), Path("website-export")]
    source, provenance = build_source_lock(
        search_roots=roots,
        out_source_lock=out_source_lock,
        out_image_provenance=out_image_provenance,
        results_dir=results_dir,
    )
    console.print(f"source_locked_page_image_count={source['source_locked_page_image_count']}")
    console.print(f"page_image_provenance_records={provenance['page_image_record_count']}")


@app.command("build-stage5ap-transcription")
def build_stage5ap_transcription_command(
    out: Path = typer.Option(TRANSCRIPTION_PATH),
    coordinates_out: Path = typer.Option(COORDINATE_PATH),
    results_dir: Path = typer.Option(RESULTS_DIR),
) -> None:
    record = build_transcription(out=out, results_dir=results_dir)
    coords = build_coordinate_records(transcription=out, out=coordinates_out, results_dir=results_dir)
    console.print(f"token_count={record['token_count']}")
    console.print(f"coordinate_record_count={coords['coordinate_record_count']}")


@app.command("build-stage5ap-alphabet-registry")
def build_stage5ap_alphabet_registry_command(
    transcription: Path = typer.Option(TRANSCRIPTION_PATH),
    out: Path = typer.Option(ALPHABET_PATH),
) -> None:
    record = build_alphabet_registry(transcription=transcription, out=out)
    console.print(f"primary_alphabet_length={record['primary_alphabet_length']}")
    console.print(f"observed_suffix_count={record['observed_suffix_count']}")


@app.command("build-stage5ap-mapping-preflight")
def build_stage5ap_mapping_preflight_command(
    transcription: Path = typer.Option(TRANSCRIPTION_PATH),
    alphabet_registry: Path = typer.Option(ALPHABET_PATH),
    out: Path = typer.Option(MAPPING_PATH),
    results_dir: Path = typer.Option(RESULTS_DIR),
) -> None:
    record = build_mapping_preflight(
        transcription=transcription,
        alphabet_registry=alphabet_registry,
        out=out,
        results_dir=results_dir,
    )
    console.print(f"value_min={record['value_min']}")
    console.print(f"value_max={record['value_max']}")


@app.command("build-stage5ap-null-control-plan")
def build_stage5ap_null_control_plan_command(out: Path = typer.Option(NULL_CONTROL_PATH)) -> None:
    record = build_null_control_plan(out=out)
    console.print(f"null_control_count={record['null_control_count']}")


@app.command("build-stage5ap-dwh-context")
def build_stage5ap_dwh_context_command(out: Path = typer.Option(DWH_CONTEXT_PATH)) -> None:
    record = build_dwh_context(out=out)
    console.print(f"context_status={record['context_status']}")


@app.command("build-stage5ap-summary")
def build_stage5ap_summary_command(
    source_lock: Path = typer.Option(SOURCE_LOCK_PATH),
    image_provenance: Path = typer.Option(IMAGE_PROVENANCE_PATH),
    transcription: Path = typer.Option(TRANSCRIPTION_PATH),
    coordinates: Path = typer.Option(COORDINATE_PATH),
    alphabet_registry: Path = typer.Option(ALPHABET_PATH),
    mapping_preflight: Path = typer.Option(MAPPING_PATH),
    null_control_plan: Path = typer.Option(NULL_CONTROL_PATH),
    dwh_context: Path = typer.Option(DWH_CONTEXT_PATH),
    outguess_toolchain: Path = typer.Option("data/stego/stage5ap-outguess-toolchain-readiness.yaml"),
    outguess_matrix: Path = typer.Option("data/stego/stage5ap-outguess-positive-control-matrix.yaml"),
    outguess_historical: Path = typer.Option("data/stego/stage5ap-outguess-historical-fixture-readiness.yaml"),
    outguess_guardrail: Path = typer.Option("data/stego/stage5ap-outguess-guardrail.yaml"),
    research_summary_out: Path = typer.Option(RESEARCH_SUMMARY_PATH),
    next_stage_decision_out: Path = typer.Option(NEXT_STAGE_DECISION_PATH),
    out: Path = typer.Option(SUMMARY_PATH),
    results_dir: Path = typer.Option(RESULTS_DIR),
) -> None:
    build_research_summary(
        source_lock=source_lock,
        transcription=transcription,
        alphabet_registry=alphabet_registry,
        mapping_preflight=mapping_preflight,
        dwh_context=dwh_context,
        out=research_summary_out,
    )
    decision = build_next_stage_decision(
        source_lock=source_lock,
        transcription=transcription,
        mapping_preflight=mapping_preflight,
        out=next_stage_decision_out,
    )
    summary = build_summary(
        source_lock=source_lock,
        image_provenance=image_provenance,
        transcription=transcription,
        coordinates=coordinates,
        alphabet_registry=alphabet_registry,
        mapping_preflight=mapping_preflight,
        null_control_plan=null_control_plan,
        dwh_context=dwh_context,
        outguess_toolchain=outguess_toolchain,
        outguess_matrix=outguess_matrix,
        outguess_historical=outguess_historical,
        outguess_guardrail=outguess_guardrail,
        research_summary=research_summary_out,
        next_stage_decision=next_stage_decision_out,
        out=out,
        results_dir=results_dir,
    )
    console.print(f"deep_research_next_ready={str(decision['deep_research_next_ready']).lower()}")
    console.print(f"token_count={summary['token_count']}")


@app.command("validate-stage5ap")
def validate_stage5ap_command(
    source_lock: Path = typer.Option(SOURCE_LOCK_PATH),
    image_provenance: Path = typer.Option(IMAGE_PROVENANCE_PATH),
    transcription: Path = typer.Option(TRANSCRIPTION_PATH),
    coordinates: Path = typer.Option(COORDINATE_PATH),
    alphabet_registry: Path = typer.Option(ALPHABET_PATH),
    mapping_preflight: Path = typer.Option(MAPPING_PATH),
    null_control_plan: Path = typer.Option(NULL_CONTROL_PATH),
    dwh_context: Path = typer.Option(DWH_CONTEXT_PATH),
    research_summary: Path = typer.Option(RESEARCH_SUMMARY_PATH),
    next_stage_decision: Path = typer.Option(NEXT_STAGE_DECISION_PATH),
    summary: Path = typer.Option(SUMMARY_PATH),
    results_dir: Path | None = typer.Option(None),
    outguess_toolchain: Path | None = typer.Option(None),
    outguess_policy: Path | None = typer.Option(None),
    outguess_matrix: Path | None = typer.Option(None),
    outguess_historical: Path | None = typer.Option(None),
    outguess_guardrail: Path | None = typer.Option(None),
) -> None:
    _ = (results_dir, outguess_toolchain, outguess_policy, outguess_matrix, outguess_historical, outguess_guardrail)
    counts, errors = validate_stage5ap(
        source_lock=source_lock,
        image_provenance=image_provenance,
        transcription=transcription,
        coordinates=coordinates,
        alphabet_registry=alphabet_registry,
        mapping_preflight=mapping_preflight,
        null_control_plan=null_control_plan,
        dwh_context=dwh_context,
        research_summary=research_summary,
        next_stage_decision=next_stage_decision,
        summary=summary,
    )
    for key, value in counts.items():
        console.print(f"{key}={str(value).lower() if isinstance(value, bool) else value}")
    for error in errors:
        console.print(error)
    if errors:
        raise typer.Exit(1)
    console.print("token_block_stage5ap_valid=true")


@app.command("build-stage5ar-original-image-source-lock")
def build_stage5ar_original_image_source_lock_command(
    search_roots: list[Path] = typer.Option(
        [Path("third_party"), Path("research-inputs"), Path("website-export"), Path("data")]
    ),
    stage5ap_image_provenance: Path = typer.Option(IMAGE_PROVENANCE_PATH),
    results_dir: Path = typer.Option(STAGE5AR_RESULTS_DIR),
    out_source_lock: Path = typer.Option(STAGE5AR_ORIGINAL_SOURCE_LOCK_PATH),
    out_variants: Path = typer.Option(STAGE5AR_IMAGE_VARIANTS_PATH),
) -> None:
    source, variants = build_original_image_source_lock(
        search_roots=search_roots,
        stage5ap_image_provenance=stage5ap_image_provenance,
        results_dir=results_dir,
        out_source_lock=out_source_lock,
        out_variants=out_variants,
    )
    console.print(f"selected_original_image_count={source['selected_original_image_count']}")
    console.print(f"variant_record_count={variants['variant_record_count']}")


@app.command("classify-stage5ar-image-variants")
def classify_stage5ar_image_variants_command(
    search_roots: list[Path] = typer.Option(
        [Path("third_party"), Path("research-inputs"), Path("website-export"), Path("data")]
    ),
    stage5ap_image_provenance: Path = typer.Option(IMAGE_PROVENANCE_PATH),
    results_dir: Path = typer.Option(STAGE5AR_RESULTS_DIR),
    out_source_lock: Path = typer.Option(STAGE5AR_ORIGINAL_SOURCE_LOCK_PATH),
    out_variants: Path = typer.Option(STAGE5AR_IMAGE_VARIANTS_PATH),
) -> None:
    source, variants = build_original_image_source_lock(
        search_roots=search_roots,
        stage5ap_image_provenance=stage5ap_image_provenance,
        results_dir=results_dir,
        out_source_lock=out_source_lock,
        out_variants=out_variants,
    )
    console.print(f"selected_original_image_count={source['selected_original_image_count']}")
    console.print(f"variant_record_count={variants['variant_record_count']}")


@app.command("build-stage5ar-page-split")
def build_stage5ar_page_split_command(
    stage5ap_transcription: Path = typer.Option(TRANSCRIPTION_PATH),
    original_image_source_lock: Path = typer.Option(STAGE5AR_ORIGINAL_SOURCE_LOCK_PATH),
    results_dir: Path = typer.Option(STAGE5AR_RESULTS_DIR),
    out_policy: Path = typer.Option(STAGE5AR_PAGE_SPLIT_POLICY_PATH),
    out_records: Path = typer.Option(STAGE5AR_PAGE_SPLIT_RECORDS_PATH),
) -> None:
    policy, records = build_page_split(
        stage5ap_transcription=stage5ap_transcription,
        original_image_source_lock=original_image_source_lock,
        results_dir=results_dir,
        out_policy=out_policy,
        out_records=out_records,
    )
    console.print(f"page_split_status={policy['page_split_status']}")
    console.print(f"row_count_sum={records['row_count_sum']}")


@app.command("build-stage5ar-pixel-coordinates")
def build_stage5ar_pixel_coordinates_command(
    stage5ap_transcription: Path = typer.Option(TRANSCRIPTION_PATH),
    stage5ap_logical_coordinates: Path = typer.Option(COORDINATE_PATH),
    original_image_source_lock: Path = typer.Option(STAGE5AR_ORIGINAL_SOURCE_LOCK_PATH),
    page_split_records: Path = typer.Option(STAGE5AR_PAGE_SPLIT_RECORDS_PATH),
    results_dir: Path = typer.Option(STAGE5AR_RESULTS_DIR),
    out_policy: Path = typer.Option(STAGE5AR_PIXEL_COORDINATE_POLICY_PATH),
    out_records: Path = typer.Option(STAGE5AR_PIXEL_COORDINATE_RECORDS_PATH),
) -> None:
    policy, records = build_pixel_coordinates(
        stage5ap_transcription=stage5ap_transcription,
        stage5ap_logical_coordinates=stage5ap_logical_coordinates,
        original_image_source_lock=original_image_source_lock,
        page_split_records=page_split_records,
        results_dir=results_dir,
        out_policy=out_policy,
        out_records=out_records,
    )
    console.print(f"coordinate_method={policy['coordinate_method']}")
    console.print(f"token_coordinate_record_count={records['coordinate_record_count']}")


@app.command("build-stage5ar-case-policy")
def build_stage5ar_case_policy_command(
    stage5ap_transcription: Path = typer.Option(TRANSCRIPTION_PATH),
    pixel_coordinate_records: Path = typer.Option(STAGE5AR_PIXEL_COORDINATE_RECORDS_PATH),
    results_dir: Path = typer.Option(STAGE5AR_RESULTS_DIR),
    out_policy: Path = typer.Option(STAGE5AR_CASE_POLICY_PATH),
    out_ambiguities: Path = typer.Option(STAGE5AR_CASE_AMBIGUITIES_PATH),
) -> None:
    policy, ambiguities = build_case_policy(
        stage5ap_transcription=stage5ap_transcription,
        pixel_coordinate_records=pixel_coordinate_records,
        results_dir=results_dir,
        out_policy=out_policy,
        out_ambiguities=out_ambiguities,
    )
    console.print(f"ambiguity_record_count={ambiguities['ambiguity_record_count']}")
    console.print(f"unresolved_ambiguity_class_count={policy['unresolved_ambiguity_class_count']}")


@app.command("validate-stage5ar-coordinates")
def validate_stage5ar_coordinates_command(
    original_image_source_lock: Path = typer.Option(STAGE5AR_ORIGINAL_SOURCE_LOCK_PATH),
    page_split_records: Path = typer.Option(STAGE5AR_PAGE_SPLIT_RECORDS_PATH),
    pixel_coordinate_policy: Path = typer.Option(STAGE5AR_PIXEL_COORDINATE_POLICY_PATH),
    pixel_coordinate_records: Path = typer.Option(STAGE5AR_PIXEL_COORDINATE_RECORDS_PATH),
    case_policy: Path = typer.Option(STAGE5AR_CASE_POLICY_PATH),
    case_ambiguities: Path = typer.Option(STAGE5AR_CASE_AMBIGUITIES_PATH),
    results_dir: Path = typer.Option(STAGE5AR_RESULTS_DIR),
    out: Path = typer.Option(STAGE5AR_COORDINATE_VALIDATION_PATH),
) -> None:
    record = validate_coordinate_payload(
        original_image_source_lock=original_image_source_lock,
        page_split_records=page_split_records,
        pixel_coordinate_policy=pixel_coordinate_policy,
        pixel_coordinate_records=pixel_coordinate_records,
        case_policy=case_policy,
        case_ambiguities=case_ambiguities,
        results_dir=results_dir,
        out=out,
    )
    console.print(f"coordinate_validation_status={record['coordinate_validation_status']}")
    console.print(f"validation_error_count={record['validation_error_count']}")
    if record["validation_error_count"]:
        raise typer.Exit(1)


@app.command("build-stage5ar-updates")
def build_stage5ar_updates_command(
    stage5ap_source_lock: Path = typer.Option(SOURCE_LOCK_PATH),
    stage5ap_null_control_plan: Path = typer.Option(NULL_CONTROL_PATH),
    coordinate_validation: Path = typer.Option(STAGE5AR_COORDINATE_VALIDATION_PATH),
    case_policy: Path = typer.Option(STAGE5AR_CASE_POLICY_PATH),
    page_split_records: Path = typer.Option(STAGE5AR_PAGE_SPLIT_RECORDS_PATH),
    out_source_lock_update: Path = typer.Option(STAGE5AR_SOURCE_LOCK_UPDATE_PATH),
    out_null_control_update: Path = typer.Option(STAGE5AR_NULL_CONTROL_UPDATE_PATH),
    out_dwh_context: Path = typer.Option(STAGE5AR_DWH_CONTEXT_PATH),
) -> None:
    source_update, null_update, dwh = build_stage5ar_updates(
        stage5ap_source_lock=stage5ap_source_lock,
        stage5ap_null_control_plan=stage5ap_null_control_plan,
        coordinate_validation=coordinate_validation,
        case_policy=case_policy,
        page_split_records=page_split_records,
        out_source_lock_update=out_source_lock_update,
        out_null_control_update=out_null_control_update,
        out_dwh_context=out_dwh_context,
    )
    console.print(f"updated_source_lock_status={source_update['updated_source_lock_status']}")
    console.print(f"coordinate_specific_controls_created={str(null_update['coordinate_specific_controls_created']).lower()}")
    console.print(f"dwh_defined={str(dwh['dwh_defined']).lower()}")


@app.command("build-stage5ar-summary")
def build_stage5ar_summary_command(
    original_source_lock: Path = typer.Option(STAGE5AR_ORIGINAL_SOURCE_LOCK_PATH),
    variants: Path = typer.Option(STAGE5AR_IMAGE_VARIANTS_PATH),
    page_split_policy: Path = typer.Option(STAGE5AR_PAGE_SPLIT_POLICY_PATH),
    page_split_records: Path = typer.Option(STAGE5AR_PAGE_SPLIT_RECORDS_PATH),
    pixel_coordinate_policy: Path = typer.Option(STAGE5AR_PIXEL_COORDINATE_POLICY_PATH),
    pixel_coordinate_records: Path = typer.Option(STAGE5AR_PIXEL_COORDINATE_RECORDS_PATH),
    case_policy: Path = typer.Option(STAGE5AR_CASE_POLICY_PATH),
    case_ambiguities: Path = typer.Option(STAGE5AR_CASE_AMBIGUITIES_PATH),
    coordinate_validation: Path = typer.Option(STAGE5AR_COORDINATE_VALIDATION_PATH),
    source_lock_update: Path = typer.Option(STAGE5AR_SOURCE_LOCK_UPDATE_PATH),
    null_control_update: Path = typer.Option(STAGE5AR_NULL_CONTROL_UPDATE_PATH),
    dwh_context: Path = typer.Option(STAGE5AR_DWH_CONTEXT_PATH),
    out_guardrail: Path = typer.Option(STAGE5AR_GUARDRAIL_PATH),
    out_next_stage: Path = typer.Option(STAGE5AR_NEXT_STAGE_DECISION_PATH),
    out_summary: Path = typer.Option(STAGE5AR_SUMMARY_PATH),
    results_dir: Path = typer.Option(STAGE5AR_RESULTS_DIR),
) -> None:
    _, next_stage, summary = build_stage5ar_summary(
        original_source_lock=original_source_lock,
        variants=variants,
        page_split_policy=page_split_policy,
        page_split_records=page_split_records,
        pixel_coordinate_policy=pixel_coordinate_policy,
        pixel_coordinate_records=pixel_coordinate_records,
        case_policy=case_policy,
        case_ambiguities=case_ambiguities,
        coordinate_validation=coordinate_validation,
        source_lock_update=source_lock_update,
        null_control_update=null_control_update,
        dwh_context=dwh_context,
        out_guardrail=out_guardrail,
        out_next_stage=out_next_stage,
        out_summary=out_summary,
        results_dir=results_dir,
    )
    console.print(f"selected_next_stage_title={next_stage['selected_next_stage_title']}")
    console.print(f"token_pixel_coordinate_record_count={summary['token_pixel_coordinate_record_count']}")


@app.command("validate-stage5ar")
def validate_stage5ar_command(
    original_source_lock: Path = typer.Option(STAGE5AR_ORIGINAL_SOURCE_LOCK_PATH),
    variants: Path = typer.Option(STAGE5AR_IMAGE_VARIANTS_PATH),
    page_split_policy: Path = typer.Option(STAGE5AR_PAGE_SPLIT_POLICY_PATH),
    page_split_records: Path = typer.Option(STAGE5AR_PAGE_SPLIT_RECORDS_PATH),
    pixel_coordinate_policy: Path = typer.Option(STAGE5AR_PIXEL_COORDINATE_POLICY_PATH),
    pixel_coordinate_records: Path = typer.Option(STAGE5AR_PIXEL_COORDINATE_RECORDS_PATH),
    case_policy: Path = typer.Option(STAGE5AR_CASE_POLICY_PATH),
    case_ambiguities: Path = typer.Option(STAGE5AR_CASE_AMBIGUITIES_PATH),
    coordinate_validation: Path = typer.Option(STAGE5AR_COORDINATE_VALIDATION_PATH),
    source_lock_update: Path = typer.Option(STAGE5AR_SOURCE_LOCK_UPDATE_PATH),
    null_control_update: Path = typer.Option(STAGE5AR_NULL_CONTROL_UPDATE_PATH),
    dwh_context: Path = typer.Option(STAGE5AR_DWH_CONTEXT_PATH),
    guardrail: Path = typer.Option(STAGE5AR_GUARDRAIL_PATH),
    next_stage_decision: Path = typer.Option(STAGE5AR_NEXT_STAGE_DECISION_PATH),
    summary: Path = typer.Option(STAGE5AR_SUMMARY_PATH),
    results_dir: Path | None = typer.Option(None),
) -> None:
    _ = results_dir
    counts, errors = validate_stage5ar(
        original_source_lock=original_source_lock,
        variants=variants,
        page_split_policy=page_split_policy,
        page_split_records=page_split_records,
        pixel_coordinate_policy=pixel_coordinate_policy,
        pixel_coordinate_records=pixel_coordinate_records,
        case_policy=case_policy,
        case_ambiguities=case_ambiguities,
        coordinate_validation=coordinate_validation,
        source_lock_update=source_lock_update,
        null_control_update=null_control_update,
        dwh_context=dwh_context,
        guardrail=guardrail,
        next_stage_decision=next_stage_decision,
        summary=summary,
    )
    for key, value in counts.items():
        console.print(f"{key}={str(value).lower() if isinstance(value, bool) else value}")
    for error in errors:
        console.print(error)
    if errors:
        raise typer.Exit(1)
    console.print("token_block_stage5ar_valid=true")


@app.command("repair-stage5at-variant-classifier")
def repair_stage5at_variant_classifier_command(
    stage5ar_source_lock: Path = typer.Option(STAGE5AR_ORIGINAL_SOURCE_LOCK_PATH),
    stage5ar_variants: Path = typer.Option(STAGE5AR_IMAGE_VARIANTS_PATH),
    results_dir: Path = typer.Option(STAGE5AT_RESULTS_DIR),
    out: Path = typer.Option(STAGE5AT_VARIANT_REPAIR_PATH),
) -> None:
    summary = build_variant_classifier_repair_summary(
        stage5ar_source_lock=stage5ar_source_lock,
        stage5ar_variants=stage5ar_variants,
        results_dir=results_dir,
        out=out,
    )
    console.print(f"variant_classifier_repaired={str(summary['variant_classifier_repaired']).lower()}")
    console.print(f"unmodified_path_bug_test_passed={str(summary['unmodified_path_bug_test_passed']).lower()}")


@app.command("build-stage5at-case-review-policy")
def build_stage5at_case_review_policy_command(
    stage5ar_case_policy: Path = typer.Option(STAGE5AR_CASE_POLICY_PATH),
    stage5ar_case_ambiguities: Path = typer.Option(STAGE5AR_CASE_AMBIGUITIES_PATH),
    stage5ap_transcription: Path = typer.Option(TRANSCRIPTION_PATH),
    out: Path = typer.Option(STAGE5AT_CASE_REVIEW_POLICY_PATH),
) -> None:
    policy = build_case_review_policy(
        stage5ar_case_policy=stage5ar_case_policy,
        stage5ar_case_ambiguities=stage5ar_case_ambiguities,
        stage5ap_transcription=stage5ap_transcription,
        out=out,
    )
    console.print(f"active_ambiguity_class_count={policy['active_ambiguity_class_count']}")
    console.print(f"active_classes_match_stage5ar_data={str(policy['active_classes_match_stage5ar_data']).lower()}")


@app.command("build-stage5at-case-challenge-set")
def build_stage5at_case_challenge_set_command(
    stage5ar_case_ambiguities: Path = typer.Option(STAGE5AR_CASE_AMBIGUITIES_PATH),
    stage5ar_pixel_coordinates: Path = typer.Option(STAGE5AR_PIXEL_COORDINATE_RECORDS_PATH),
    stage5ap_transcription: Path = typer.Option(TRANSCRIPTION_PATH),
    stage5ap_alphabet_registry: Path = typer.Option(ALPHABET_PATH),
    results_dir: Path = typer.Option(STAGE5AT_RESULTS_DIR),
    out_case_challenges: Path = typer.Option(STAGE5AT_CASE_REVIEW_CHALLENGE_SET_PATH),
    out_canonical_challenges: Path = typer.Option(STAGE5AT_CANONICAL_CHALLENGE_SET_PATH),
) -> None:
    case_payload, canonical_payload = build_case_challenge_sets(
        stage5ar_case_ambiguities=stage5ar_case_ambiguities,
        stage5ar_pixel_coordinates=stage5ar_pixel_coordinates,
        stage5ap_transcription=stage5ap_transcription,
        stage5ap_alphabet_registry=stage5ap_alphabet_registry,
        results_dir=results_dir,
        out_case_challenges=out_case_challenges,
        out_canonical_challenges=out_canonical_challenges,
    )
    console.print(f"case_review_challenge_count={case_payload['challenge_count']}")
    console.print(f"canonical_transcription_challenge_count={canonical_payload['challenge_count']}")


@app.command("build-stage5at-decision-template")
def build_stage5at_decision_template_command(
    stage5ar_source_lock: Path = typer.Option(STAGE5AR_ORIGINAL_SOURCE_LOCK_PATH),
    stage5ar_pixel_coordinates: Path = typer.Option(STAGE5AR_PIXEL_COORDINATE_RECORDS_PATH),
    case_challenges: Path = typer.Option(STAGE5AT_CASE_REVIEW_CHALLENGE_SET_PATH),
    canonical_challenges: Path = typer.Option(STAGE5AT_CANONICAL_CHALLENGE_SET_PATH),
    out_root: Path = typer.Option(STAGE5AT_REVIEW_PACK_ROOT),
    results_dir: Path = typer.Option(STAGE5AT_RESULTS_DIR),
    out_crop_manifest: Path = typer.Option(STAGE5AT_CROP_MANIFEST_PATH),
    out_decision_template: Path = typer.Option(STAGE5AT_DECISION_TEMPLATE_PATH),
    out_pack_manifest: Path = typer.Option(STAGE5AT_PACK_MANIFEST_PATH),
) -> None:
    _, decision_template, _ = build_review_pack(
        stage5ar_source_lock=stage5ar_source_lock,
        stage5ar_pixel_coordinates=stage5ar_pixel_coordinates,
        case_challenges=case_challenges,
        canonical_challenges=canonical_challenges,
        out_root=out_root,
        results_dir=results_dir,
        out_crop_manifest=out_crop_manifest,
        out_decision_template=out_decision_template,
        out_pack_manifest=out_pack_manifest,
    )
    console.print(f"decision_template_records={decision_template['decision_count']}")
    console.print("template_status=empty_unfilled")


@app.command("build-stage5at-review-pack")
def build_stage5at_review_pack_command(
    stage5ar_source_lock: Path = typer.Option(STAGE5AR_ORIGINAL_SOURCE_LOCK_PATH),
    stage5ar_pixel_coordinates: Path = typer.Option(STAGE5AR_PIXEL_COORDINATE_RECORDS_PATH),
    case_challenges: Path = typer.Option(STAGE5AT_CASE_REVIEW_CHALLENGE_SET_PATH),
    canonical_challenges: Path = typer.Option(STAGE5AT_CANONICAL_CHALLENGE_SET_PATH),
    out_root: Path = typer.Option(STAGE5AT_REVIEW_PACK_ROOT),
    results_dir: Path = typer.Option(STAGE5AT_RESULTS_DIR),
    out_crop_manifest: Path = typer.Option(STAGE5AT_CROP_MANIFEST_PATH),
    out_decision_template: Path = typer.Option(STAGE5AT_DECISION_TEMPLATE_PATH),
    out_pack_manifest: Path = typer.Option(STAGE5AT_PACK_MANIFEST_PATH),
) -> None:
    crop_manifest, _, pack_manifest = build_review_pack(
        stage5ar_source_lock=stage5ar_source_lock,
        stage5ar_pixel_coordinates=stage5ar_pixel_coordinates,
        case_challenges=case_challenges,
        canonical_challenges=canonical_challenges,
        out_root=out_root,
        results_dir=results_dir,
        out_crop_manifest=out_crop_manifest,
        out_decision_template=out_decision_template,
        out_pack_manifest=out_pack_manifest,
    )
    console.print(f"generated_crop_count={crop_manifest['crop_count']}")
    console.print(f"review_pack_zip_path={pack_manifest['review_pack_zip_path']}")


@app.command("build-stage5at-null-control-update")
def build_stage5at_null_control_update_command(
    stage5ar_null_control_update: Path = typer.Option(STAGE5AR_NULL_CONTROL_UPDATE_PATH),
    case_challenges: Path = typer.Option(STAGE5AT_CASE_REVIEW_CHALLENGE_SET_PATH),
    out: Path = typer.Option(STAGE5AT_NULL_CONTROL_UPDATE_PATH),
) -> None:
    payload = build_null_control_case_update(
        stage5ar_null_control_update=stage5ar_null_control_update,
        case_challenges=case_challenges,
        out=out,
    )
    console.print(f"case_decision_controls_added={str(payload['case_decision_controls_added']).lower()}")
    console.print(f"value_sensitivity_controls_added={str(payload['value_sensitivity_controls_added']).lower()}")


@app.command("build-stage5at-dwh-case-context")
def build_stage5at_dwh_case_context_command(out: Path = typer.Option(STAGE5AT_DWH_CASE_CONTEXT_PATH)) -> None:
    payload = build_dwh_case_context(out=out)
    console.print(f"dwh_defined={str(payload['dwh_defined']).lower()}")
    console.print(f"hash_search_performed={str(payload['hash_search_performed']).lower()}")


@app.command("build-stage5at-summary")
def build_stage5at_summary_command(
    case_review_policy: Path = typer.Option(STAGE5AT_CASE_REVIEW_POLICY_PATH),
    case_challenges: Path = typer.Option(STAGE5AT_CASE_REVIEW_CHALLENGE_SET_PATH),
    canonical_challenges: Path = typer.Option(STAGE5AT_CANONICAL_CHALLENGE_SET_PATH),
    crop_manifest: Path = typer.Option(STAGE5AT_CROP_MANIFEST_PATH),
    decision_template: Path = typer.Option(STAGE5AT_DECISION_TEMPLATE_PATH),
    pack_manifest: Path = typer.Option(STAGE5AT_PACK_MANIFEST_PATH),
    variant_repair: Path = typer.Option(STAGE5AT_VARIANT_REPAIR_PATH),
    doc_drift_summary: Path = typer.Option(STAGE5AT_DOC_DRIFT_PATH),
    null_control_update: Path = typer.Option(STAGE5AT_NULL_CONTROL_UPDATE_PATH),
    dwh_case_context: Path = typer.Option(STAGE5AT_DWH_CASE_CONTEXT_PATH),
    results_dir: Path = typer.Option(STAGE5AT_RESULTS_DIR),
    out_guardrail: Path = typer.Option(STAGE5AT_GUARDRAIL_PATH),
    out_next_stage: Path = typer.Option(STAGE5AT_NEXT_STAGE_DECISION_PATH),
    out_summary: Path = typer.Option(STAGE5AT_SUMMARY_PATH),
) -> None:
    guardrail, next_stage, summary = build_stage5at_summary(
        case_review_policy=case_review_policy,
        case_challenges=case_challenges,
        canonical_challenges=canonical_challenges,
        crop_manifest=crop_manifest,
        decision_template=decision_template,
        pack_manifest=pack_manifest,
        variant_repair=variant_repair,
        doc_drift_summary=doc_drift_summary,
        null_control_update=null_control_update,
        dwh_case_context=dwh_case_context,
        results_dir=results_dir,
        out_guardrail=out_guardrail,
        out_next_stage=out_next_stage,
        out_summary=out_summary,
    )
    console.print(f"selected_next_stage_title={next_stage['selected_next_stage_title']}")
    console.print(f"case_review_challenge_count={summary['case_review_challenge_count']}")
    console.print(f"automatic_case_resolution_performed={str(guardrail['automatic_case_resolution_performed']).lower()}")


@app.command("build-stage5at-doc-drift-summary")
def build_stage5at_doc_drift_summary_command(
    case_review_policy: Path = typer.Option(STAGE5AT_CASE_REVIEW_POLICY_PATH),
    results_dir: Path = typer.Option(STAGE5AT_RESULTS_DIR),
    out: Path = typer.Option(STAGE5AT_DOC_DRIFT_PATH),
) -> None:
    payload = build_doc_drift_repair_summary(case_review_policy=case_review_policy, results_dir=results_dir, out=out)
    console.print(f"doc_drift_repaired={str(payload['doc_drift_repaired']).lower()}")
    console.print(f"doc_drift_active_classes_match_data={str(payload['doc_drift_active_classes_match_data']).lower()}")


@app.command("validate-stage5at")
def validate_stage5at_command(
    case_review_policy: Path = typer.Option(STAGE5AT_CASE_REVIEW_POLICY_PATH),
    case_challenges: Path = typer.Option(STAGE5AT_CASE_REVIEW_CHALLENGE_SET_PATH),
    canonical_challenges: Path = typer.Option(STAGE5AT_CANONICAL_CHALLENGE_SET_PATH),
    crop_manifest: Path = typer.Option(STAGE5AT_CROP_MANIFEST_PATH),
    decision_template: Path = typer.Option(STAGE5AT_DECISION_TEMPLATE_PATH),
    pack_manifest: Path = typer.Option(STAGE5AT_PACK_MANIFEST_PATH),
    variant_repair: Path = typer.Option(STAGE5AT_VARIANT_REPAIR_PATH),
    doc_drift_summary: Path = typer.Option(STAGE5AT_DOC_DRIFT_PATH),
    null_control_update: Path = typer.Option(STAGE5AT_NULL_CONTROL_UPDATE_PATH),
    dwh_case_context: Path = typer.Option(STAGE5AT_DWH_CASE_CONTEXT_PATH),
    guardrail: Path = typer.Option(STAGE5AT_GUARDRAIL_PATH),
    next_stage_decision: Path = typer.Option(STAGE5AT_NEXT_STAGE_DECISION_PATH),
    summary: Path = typer.Option(STAGE5AT_SUMMARY_PATH),
    review_pack_root: Path = typer.Option(STAGE5AT_REVIEW_PACK_ROOT),
    results_dir: Path = typer.Option(STAGE5AT_RESULTS_DIR),
) -> None:
    counts, errors = validate_stage5at(
        case_review_policy=case_review_policy,
        case_challenges=case_challenges,
        canonical_challenges=canonical_challenges,
        crop_manifest=crop_manifest,
        decision_template=decision_template,
        pack_manifest=pack_manifest,
        variant_repair=variant_repair,
        doc_drift_summary=doc_drift_summary,
        null_control_update=null_control_update,
        dwh_case_context=dwh_case_context,
        guardrail=guardrail,
        next_stage_decision=next_stage_decision,
        summary=summary,
        review_pack_root=review_pack_root,
        results_dir=results_dir,
    )
    for key, value in counts.items():
        console.print(f"{key}={str(value).lower() if isinstance(value, bool) else value}")
    for error in errors:
        console.print(error)
    if errors:
        raise typer.Exit(1)
    console.print("token_block_stage5at_valid=true")


@app.command("audit-stage5at-review-pack-usability")
def audit_stage5at_review_pack_usability_command(
    stage5at_review_pack_root: Path = typer.Option(STAGE5AT_REVIEW_PACK_ROOT),
    stage5at_pack_manifest: Path = typer.Option(STAGE5AT_PACK_MANIFEST_PATH),
    stage5at_case_challenges: Path = typer.Option(STAGE5AT_CASE_REVIEW_CHALLENGE_SET_PATH),
    stage5at_canonical_challenges: Path = typer.Option(STAGE5AT_CANONICAL_CHALLENGE_SET_PATH),
    results_dir: Path = typer.Option(STAGE5AU_RESULTS_DIR),
    out: Path = typer.Option(STAGE5AU_USABILITY_AUDIT_PATH),
) -> None:
    payload = audit_stage5at_review_pack_usability(
        stage5at_review_pack_root=stage5at_review_pack_root,
        stage5at_pack_manifest=stage5at_pack_manifest,
        stage5at_case_challenges=stage5at_case_challenges,
        stage5at_canonical_challenges=stage5at_canonical_challenges,
        results_dir=results_dir,
        out=out,
    )
    console.print(f"stage5at_pack_exists={str(payload['stage5at_pack_exists']).lower()}")
    console.print(f"stage5at_html_case_card_count={payload['stage5at_html_case_card_count']}")
    console.print(f"stage5at_manual_review_usable={str(payload['stage5at_manual_review_usable']).lower()}")
    console.print(f"repair_required={str(payload['repair_required']).lower()}")


@app.command("build-stage5au-crop-geometry-policy")
def build_stage5au_crop_geometry_policy_command(
    stage5ar_source_lock: Path = typer.Option(STAGE5AR_ORIGINAL_SOURCE_LOCK_PATH),
    stage5ar_pixel_coordinates: Path = typer.Option(STAGE5AR_PIXEL_COORDINATE_RECORDS_PATH),
    out: Path = typer.Option(STAGE5AU_CROP_GEOMETRY_POLICY_PATH),
) -> None:
    payload = build_crop_geometry_policy(
        stage5ar_source_lock=stage5ar_source_lock,
        stage5ar_pixel_coordinates=stage5ar_pixel_coordinates,
        out=out,
    )
    console.print(f"source_original_images_only={str(payload['source_original_images_only']).lower()}")
    console.print(f"crop_type_count={len(payload['crop_types'])}")


@app.command("build-stage5au-review-pack-v2")
def build_stage5au_review_pack_v2_command(
    stage5ar_source_lock: Path = typer.Option(STAGE5AR_ORIGINAL_SOURCE_LOCK_PATH),
    stage5ar_pixel_coordinates: Path = typer.Option(STAGE5AR_PIXEL_COORDINATE_RECORDS_PATH),
    stage5at_case_challenges: Path = typer.Option(STAGE5AT_CASE_REVIEW_CHALLENGE_SET_PATH),
    stage5at_canonical_challenges: Path = typer.Option(STAGE5AT_CANONICAL_CHALLENGE_SET_PATH),
    crop_geometry_policy: Path = typer.Option(STAGE5AU_CROP_GEOMETRY_POLICY_PATH),
    out_root: Path = typer.Option(STAGE5AU_REVIEW_PACK_ROOT),
    results_dir: Path = typer.Option(STAGE5AU_RESULTS_DIR),
    out_crop_quality: Path = typer.Option(STAGE5AU_CROP_QUALITY_PATH),
    out_case_challenges_v2: Path = typer.Option(STAGE5AU_CASE_CHALLENGES_V2_PATH),
    out_canonical_challenges_v2: Path = typer.Option(STAGE5AU_CANONICAL_CHALLENGES_V2_PATH),
    out_pack_manifest: Path = typer.Option(STAGE5AU_PACK_MANIFEST_PATH),
    out_ui_coverage: Path = typer.Option(STAGE5AU_UI_COVERAGE_PATH),
    out_decision_template: Path = typer.Option(STAGE5AU_DECISION_TEMPLATE_PATH),
) -> None:
    quality, cases, canonical, pack, ui = build_review_pack_v2(
        stage5ar_source_lock=stage5ar_source_lock,
        stage5ar_pixel_coordinates=stage5ar_pixel_coordinates,
        stage5at_case_challenges=stage5at_case_challenges,
        stage5at_canonical_challenges=stage5at_canonical_challenges,
        crop_geometry_policy=crop_geometry_policy,
        out_root=out_root,
        results_dir=results_dir,
        out_crop_quality=out_crop_quality,
        out_case_challenges_v2=out_case_challenges_v2,
        out_canonical_challenges_v2=out_canonical_challenges_v2,
        out_pack_manifest=out_pack_manifest,
        out_ui_coverage=out_ui_coverage,
        out_decision_template=out_decision_template,
    )
    console.print(f"case_challenges_rendered={cases['challenge_count']}")
    console.print(f"canonical_challenges_rendered={canonical['challenge_count']}")
    console.print(f"generated_crop_count={pack['generated_crop_count']}")
    console.print(f"overlay_count={quality['overlay_count']}")
    console.print(f"all_case_challenges_visible={str(ui['all_203_case_challenges_visible_or_linked']).lower()}")


@app.command("validate-stage5au-review-pack-v2")
def validate_stage5au_review_pack_v2_command(
    ui_coverage: Path = typer.Option(STAGE5AU_UI_COVERAGE_PATH),
    pack_manifest: Path = typer.Option(STAGE5AU_PACK_MANIFEST_PATH),
) -> None:
    ui = read_yaml(ui_coverage)
    pack = read_yaml(pack_manifest)
    console.print(f"case_challenges_rendered={ui['case_challenges_rendered']}")
    console.print(f"canonical_challenges_rendered={ui['canonical_challenges_rendered']}")
    console.print(f"review_pack_v2_zip_path={pack['review_pack_v2_zip_path']}")
    if not ui.get("manual_review_usable"):
        raise typer.Exit(1)
    console.print("token_block_stage5au_review_pack_v2_valid=true")


@app.command("build-stage5au-null-control-update")
def build_stage5au_null_control_update_command(
    stage5at_null_control_update: Path = typer.Option(STAGE5AT_NULL_CONTROL_UPDATE_PATH),
    case_challenges_v2: Path = typer.Option(STAGE5AU_CASE_CHALLENGES_V2_PATH),
    crop_quality: Path = typer.Option(STAGE5AU_CROP_QUALITY_PATH),
    out: Path = typer.Option(STAGE5AU_NULL_CONTROL_UPDATE_PATH),
) -> None:
    payload = build_stage5au_null_control_update(
        stage5at_null_control_update=stage5at_null_control_update,
        case_challenges_v2=case_challenges_v2,
        crop_quality=crop_quality,
        out=out,
    )
    console.print(f"review_pack_v2_null_controls_added={str(payload['review_pack_v2_null_controls_added']).lower()}")


@app.command("build-stage5au-dwh-review-pack-context")
def build_stage5au_dwh_review_pack_context_command(out: Path = typer.Option(STAGE5AU_DWH_CONTEXT_PATH)) -> None:
    payload = build_stage5au_dwh_review_pack_context(out=out)
    console.print(f"dwh_expansion={payload['dwh_expansion']}")
    console.print(f"hash_search_performed={str(payload['hash_search_performed']).lower()}")


@app.command("build-stage5au-summary")
def build_stage5au_summary_command(
    usability_audit: Path = typer.Option(STAGE5AU_USABILITY_AUDIT_PATH),
    crop_geometry_policy: Path = typer.Option(STAGE5AU_CROP_GEOMETRY_POLICY_PATH),
    crop_quality: Path = typer.Option(STAGE5AU_CROP_QUALITY_PATH),
    case_challenges_v2: Path = typer.Option(STAGE5AU_CASE_CHALLENGES_V2_PATH),
    canonical_challenges_v2: Path = typer.Option(STAGE5AU_CANONICAL_CHALLENGES_V2_PATH),
    pack_manifest: Path = typer.Option(STAGE5AU_PACK_MANIFEST_PATH),
    ui_coverage: Path = typer.Option(STAGE5AU_UI_COVERAGE_PATH),
    decision_template_v2: Path = typer.Option(STAGE5AU_DECISION_TEMPLATE_PATH),
    null_control_update: Path = typer.Option(STAGE5AU_NULL_CONTROL_UPDATE_PATH),
    dwh_context: Path = typer.Option(STAGE5AU_DWH_CONTEXT_PATH),
    out_guardrail: Path = typer.Option(STAGE5AU_GUARDRAIL_PATH),
    out_next_stage: Path = typer.Option(STAGE5AU_NEXT_STAGE_DECISION_PATH),
    out_summary: Path = typer.Option(STAGE5AU_SUMMARY_PATH),
) -> None:
    guard, next_stage, summary = build_stage5au_summary(
        usability_audit=usability_audit,
        crop_geometry_policy=crop_geometry_policy,
        crop_quality=crop_quality,
        case_challenges_v2=case_challenges_v2,
        canonical_challenges_v2=canonical_challenges_v2,
        pack_manifest=pack_manifest,
        ui_coverage=ui_coverage,
        decision_template_v2=decision_template_v2,
        null_control_update=null_control_update,
        dwh_context=dwh_context,
        out_guardrail=out_guardrail,
        out_next_stage=out_next_stage,
        out_summary=out_summary,
    )
    console.print(f"selected_next_stage_title={next_stage['selected_next_stage_title']}")
    console.print(f"review_pack_v2_zip_sha256={summary['review_pack_v2_zip_sha256']}")
    console.print(f"automatic_case_resolution_performed={str(guard['automatic_case_resolution_performed']).lower()}")


@app.command("validate-stage5au")
def validate_stage5au_command(
    usability_audit: Path = typer.Option(STAGE5AU_USABILITY_AUDIT_PATH),
    crop_geometry_policy: Path = typer.Option(STAGE5AU_CROP_GEOMETRY_POLICY_PATH),
    crop_quality: Path = typer.Option(STAGE5AU_CROP_QUALITY_PATH),
    case_challenges_v2: Path = typer.Option(STAGE5AU_CASE_CHALLENGES_V2_PATH),
    canonical_challenges_v2: Path = typer.Option(STAGE5AU_CANONICAL_CHALLENGES_V2_PATH),
    pack_manifest: Path = typer.Option(STAGE5AU_PACK_MANIFEST_PATH),
    ui_coverage: Path = typer.Option(STAGE5AU_UI_COVERAGE_PATH),
    decision_template_v2: Path = typer.Option(STAGE5AU_DECISION_TEMPLATE_PATH),
    null_control_update: Path = typer.Option(STAGE5AU_NULL_CONTROL_UPDATE_PATH),
    dwh_context: Path = typer.Option(STAGE5AU_DWH_CONTEXT_PATH),
    guardrail: Path = typer.Option(STAGE5AU_GUARDRAIL_PATH),
    next_stage_decision: Path = typer.Option(STAGE5AU_NEXT_STAGE_DECISION_PATH),
    summary: Path = typer.Option(STAGE5AU_SUMMARY_PATH),
    review_pack_root: Path = typer.Option(STAGE5AU_REVIEW_PACK_ROOT),
    results_dir: Path = typer.Option(STAGE5AU_RESULTS_DIR),
) -> None:
    counts, errors = validate_stage5au(
        usability_audit=usability_audit,
        crop_geometry_policy=crop_geometry_policy,
        crop_quality=crop_quality,
        case_challenges_v2=case_challenges_v2,
        canonical_challenges_v2=canonical_challenges_v2,
        pack_manifest=pack_manifest,
        ui_coverage=ui_coverage,
        decision_template_v2=decision_template_v2,
        null_control_update=null_control_update,
        dwh_context=dwh_context,
        guardrail=guardrail,
        next_stage_decision=next_stage_decision,
        summary=summary,
        review_pack_root=review_pack_root,
        results_dir=results_dir,
    )
    for key, value in counts.items():
        console.print(f"{key}={str(value).lower() if isinstance(value, bool) else value}")
    for error in errors:
        console.print(error)
    if errors:
        raise typer.Exit(1)
    console.print("token_block_stage5au_valid=true")


@app.command("ingest-stage5av-decisions")
def ingest_stage5av_decisions_command(
    decision_file: Path = typer.Option(STAGE5AV_LOCAL_DECISION_TEMPLATE_PATH),
    case_challenges_v2: Path = typer.Option(STAGE5AU_CASE_CHALLENGES_V2_PATH),
    canonical_challenges_v2: Path = typer.Option(STAGE5AU_CANONICAL_CHALLENGES_V2_PATH),
    stage5ap_transcription: Path = typer.Option(TRANSCRIPTION_PATH),
    results_dir: Path = typer.Option(STAGE5AV_RESULTS_DIR),
    out_ingest: Path = typer.Option(STAGE5AV_DECISION_FILE_INGEST_PATH),
    out_validation: Path = typer.Option(STAGE5AV_DECISION_FILE_VALIDATION_PATH),
) -> None:
    ingest, validation = ingest_stage5av_decisions(
        decision_file=decision_file,
        case_challenges_v2=case_challenges_v2,
        canonical_challenges_v2=canonical_challenges_v2,
        stage5ap_transcription=stage5ap_transcription,
        results_dir=results_dir,
        out_ingest=out_ingest,
        out_validation=out_validation,
    )
    console.print(f"decision_file_found={str(ingest['decision_file_found']).lower()}")
    console.print(f"decision_record_count={ingest['decision_record_count']}")
    for decision, count in validation.get("decision_counts", {}).items():
        console.print(f"{decision}_count={count}")
    if validation.get("validation_error_count"):
        raise typer.Exit(1)


@app.command("validate-stage5av-decisions")
def validate_stage5av_decisions_command(
    validation: Path = typer.Option(STAGE5AV_DECISION_FILE_VALIDATION_PATH),
) -> None:
    payload = read_yaml(validation)
    console.print(f"valid_for_stage5av_integration={str(payload['valid_for_stage5av_integration']).lower()}")
    console.print(f"validation_error_count={payload['validation_error_count']}")
    console.print(f"validation_warning_count={payload['validation_warning_count']}")
    if payload.get("validation_error_count"):
        raise typer.Exit(1)


@app.command("build-stage5av-decision-records")
def build_stage5av_decision_records_command(
    decision_file: Path = typer.Option(STAGE5AV_LOCAL_DECISION_TEMPLATE_PATH),
    validation: Path = typer.Option(STAGE5AV_DECISION_FILE_VALIDATION_PATH),
    case_challenges_v2: Path = typer.Option(STAGE5AU_CASE_CHALLENGES_V2_PATH),
    stage5ap_alphabet_registry: Path = typer.Option(ALPHABET_PATH),
    results_dir: Path = typer.Option(STAGE5AV_RESULTS_DIR),
    out_decisions: Path = typer.Option(STAGE5AV_HUMAN_REVIEW_DECISIONS_PATH),
    out_confirmed: Path = typer.Option(STAGE5AV_CONFIRMED_TOKENS_PATH),
    out_unresolved: Path = typer.Option(STAGE5AV_UNRESOLVED_VARIANTS_PATH),
    out_extras: Path = typer.Option(STAGE5AV_REVIEWER_EXTRA_TOKENS_PATH),
) -> None:
    decisions, confirmed, unresolved, extras = build_stage5av_decision_records(
        decision_file=decision_file,
        validation=validation,
        case_challenges_v2=case_challenges_v2,
        stage5ap_alphabet_registry=stage5ap_alphabet_registry,
        results_dir=results_dir,
        out_decisions=out_decisions,
        out_confirmed=out_confirmed,
        out_unresolved=out_unresolved,
        out_extras=out_extras,
    )
    console.print(f"decision_record_count={decisions['decision_record_count']}")
    console.print(f"confirmed_token_count={confirmed['confirmed_token_count']}")
    console.print(f"unresolved_token_variant_count={unresolved['unresolved_token_variant_count']}")
    console.print(f"reviewer_extra_possible_token_count={extras['reviewer_extra_possible_token_count']}")


@app.command("build-stage5av-variant-branch-manifest")
def build_stage5av_variant_branch_manifest_command(
    decision_records: Path = typer.Option(STAGE5AV_HUMAN_REVIEW_DECISIONS_PATH),
    unresolved_variants: Path = typer.Option(STAGE5AV_UNRESOLVED_VARIANTS_PATH),
    reviewer_extras: Path = typer.Option(STAGE5AV_REVIEWER_EXTRA_TOKENS_PATH),
    stage5ap_transcription: Path = typer.Option(TRANSCRIPTION_PATH),
    stage5ap_mapping_preflight: Path = typer.Option(MAPPING_PATH),
    results_dir: Path = typer.Option(STAGE5AV_RESULTS_DIR),
    out_impact: Path = typer.Option(STAGE5AV_PRIMARY60_IMPACT_PATH),
    out_branch_manifest: Path = typer.Option(STAGE5AV_BRANCH_MANIFEST_PATH),
) -> None:
    impact, manifest = build_stage5av_variant_branch_manifest(
        decision_records=decision_records,
        unresolved_variants=unresolved_variants,
        reviewer_extras=reviewer_extras,
        stage5ap_transcription=stage5ap_transcription,
        stage5ap_mapping_preflight=stage5ap_mapping_preflight,
        results_dir=results_dir,
        out_impact=out_impact,
        out_branch_manifest=out_branch_manifest,
    )
    console.print(f"branch_count_upper_bound_log10={impact['branch_count_upper_bound_log10']}")
    console.print(f"use_compact_branch_manifest={str(manifest['use_compact_branch_manifest']).lower()}")
    console.print(f"full_cartesian_product_enumerated={str(manifest['full_cartesian_product_enumerated']).lower()}")


@app.command("build-stage5av-updates")
def build_stage5av_updates_command(
    decision_records: Path = typer.Option(STAGE5AV_HUMAN_REVIEW_DECISIONS_PATH),
    unresolved_variants: Path = typer.Option(STAGE5AV_UNRESOLVED_VARIANTS_PATH),
    impact_summary: Path = typer.Option(STAGE5AV_PRIMARY60_IMPACT_PATH),
    branch_manifest: Path = typer.Option(STAGE5AV_BRANCH_MANIFEST_PATH),
    out_canonical_update: Path = typer.Option(STAGE5AV_CANONICAL_UPDATE_PATH),
    out_null_control_update: Path = typer.Option(STAGE5AV_NULL_CONTROL_UPDATE_PATH),
    out_dwh_context: Path = typer.Option(STAGE5AV_DWH_CONTEXT_PATH),
) -> None:
    canonical, null_update, dwh = build_stage5av_updates(
        decision_records=decision_records,
        unresolved_variants=unresolved_variants,
        impact_summary=impact_summary,
        branch_manifest=branch_manifest,
        out_canonical_update=out_canonical_update,
        out_null_control_update=out_null_control_update,
        out_dwh_context=out_dwh_context,
    )
    console.print(f"canonical_transcription_changed={str(canonical['canonical_transcription_changed']).lower()}")
    console.print(f"null_controls_updated={str(null_update['baseline_current_control_preserved']).lower()}")
    console.print(f"dwh_defined={str(dwh['dwh_defined']).lower()}")


@app.command("build-stage5av-summary")
def build_stage5av_summary_command(
    ingest: Path = typer.Option(STAGE5AV_DECISION_FILE_INGEST_PATH),
    validation: Path = typer.Option(STAGE5AV_DECISION_FILE_VALIDATION_PATH),
    decision_records: Path = typer.Option(STAGE5AV_HUMAN_REVIEW_DECISIONS_PATH),
    confirmed: Path = typer.Option(STAGE5AV_CONFIRMED_TOKENS_PATH),
    unresolved_variants: Path = typer.Option(STAGE5AV_UNRESOLVED_VARIANTS_PATH),
    reviewer_extras: Path = typer.Option(STAGE5AV_REVIEWER_EXTRA_TOKENS_PATH),
    impact_summary: Path = typer.Option(STAGE5AV_PRIMARY60_IMPACT_PATH),
    branch_manifest: Path = typer.Option(STAGE5AV_BRANCH_MANIFEST_PATH),
    canonical_update: Path = typer.Option(STAGE5AV_CANONICAL_UPDATE_PATH),
    null_control_update: Path = typer.Option(STAGE5AV_NULL_CONTROL_UPDATE_PATH),
    dwh_context: Path = typer.Option(STAGE5AV_DWH_CONTEXT_PATH),
    out_guardrail: Path = typer.Option(STAGE5AV_GUARDRAIL_PATH),
    out_next_stage: Path = typer.Option(STAGE5AV_NEXT_STAGE_DECISION_PATH),
    out_summary: Path = typer.Option(STAGE5AV_SUMMARY_PATH),
    results_dir: Path = typer.Option(STAGE5AV_RESULTS_DIR),
) -> None:
    guard, next_stage, summary = build_stage5av_summary(
        ingest=ingest,
        validation=validation,
        decision_records=decision_records,
        confirmed=confirmed,
        unresolved_variants=unresolved_variants,
        reviewer_extras=reviewer_extras,
        impact_summary=impact_summary,
        branch_manifest=branch_manifest,
        canonical_update=canonical_update,
        null_control_update=null_control_update,
        dwh_context=dwh_context,
        out_guardrail=out_guardrail,
        out_next_stage=out_next_stage,
        out_summary=out_summary,
        results_dir=results_dir,
    )
    console.print(f"automatic_case_resolution_performed={str(guard['automatic_case_resolution_performed']).lower()}")
    console.print(f"next_stage={next_stage['next_stage_selected']}")
    console.print(f"decision_record_count={summary['decision_record_count']}")


@app.command("validate-stage5av")
def validate_stage5av_command(
    ingest: Path = typer.Option(STAGE5AV_DECISION_FILE_INGEST_PATH),
    validation: Path = typer.Option(STAGE5AV_DECISION_FILE_VALIDATION_PATH),
    decision_records: Path = typer.Option(STAGE5AV_HUMAN_REVIEW_DECISIONS_PATH),
    confirmed: Path = typer.Option(STAGE5AV_CONFIRMED_TOKENS_PATH),
    unresolved_variants: Path = typer.Option(STAGE5AV_UNRESOLVED_VARIANTS_PATH),
    reviewer_extras: Path = typer.Option(STAGE5AV_REVIEWER_EXTRA_TOKENS_PATH),
    impact_summary: Path = typer.Option(STAGE5AV_PRIMARY60_IMPACT_PATH),
    branch_manifest: Path = typer.Option(STAGE5AV_BRANCH_MANIFEST_PATH),
    canonical_update: Path = typer.Option(STAGE5AV_CANONICAL_UPDATE_PATH),
    null_control_update: Path = typer.Option(STAGE5AV_NULL_CONTROL_UPDATE_PATH),
    dwh_context: Path = typer.Option(STAGE5AV_DWH_CONTEXT_PATH),
    guardrail: Path = typer.Option(STAGE5AV_GUARDRAIL_PATH),
    next_stage: Path = typer.Option(STAGE5AV_NEXT_STAGE_DECISION_PATH),
    summary: Path = typer.Option(STAGE5AV_SUMMARY_PATH),
    results_dir: Path = typer.Option(STAGE5AV_RESULTS_DIR),
) -> None:
    counts, errors = validate_stage5av(
        ingest=ingest,
        validation=validation,
        decision_records=decision_records,
        confirmed=confirmed,
        unresolved_variants=unresolved_variants,
        reviewer_extras=reviewer_extras,
        impact_summary=impact_summary,
        branch_manifest=branch_manifest,
        canonical_update=canonical_update,
        null_control_update=null_control_update,
        dwh_context=dwh_context,
        guardrail=guardrail,
        next_stage=next_stage,
        summary=summary,
        results_dir=results_dir,
    )
    for key, value in counts.items():
        console.print(f"{key}={str(value).lower() if isinstance(value, bool) else value}")
    for error in errors:
        console.print(error)
    if errors:
        raise typer.Exit(1)
    console.print("token_block_stage5av_valid=true")


@app.command("audit-stage5aw-decision-parser")
def audit_stage5aw_decision_parser_command(
    decision_file: Path = typer.Option(STAGE5AV_LOCAL_DECISION_TEMPLATE_PATH),
    stage5av_extras: Path = typer.Option(STAGE5AV_REVIEWER_EXTRA_TOKENS_PATH),
    stage5av_branch_manifest: Path = typer.Option(STAGE5AV_BRANCH_MANIFEST_PATH),
    results_dir: Path = typer.Option(STAGE5AW_RESULTS_DIR),
    out_audit: Path = typer.Option(STAGE5AW_DECISION_PARSER_AUDIT_PATH),
    out_policy: Path = typer.Option(STAGE5AW_PARSER_POLICY_PATH),
) -> None:
    audit, policy = audit_stage5aw_decision_parser(
        decision_file=decision_file,
        stage5av_extras=stage5av_extras,
        stage5av_branch_manifest=stage5av_branch_manifest,
        results_dir=results_dir,
        out_audit=out_audit,
        out_policy=out_policy,
    )
    console.print(f"stage5av_malformed_reviewer_extra_count={audit['stage5av_malformed_reviewer_extra_count']}")
    console.print(f"parser_policy_status={policy['policy_status']}")


@app.command("repair-stage5aw-decision-variants")
def repair_stage5aw_decision_variants_command(
    decision_file: Path = typer.Option(STAGE5AV_LOCAL_DECISION_TEMPLATE_PATH),
    stage5au_case_challenges: Path = typer.Option(STAGE5AU_CASE_CHALLENGES_V2_PATH),
    stage5ap_alphabet_registry: Path = typer.Option(ALPHABET_PATH),
    parser_policy: Path = typer.Option(STAGE5AW_PARSER_POLICY_PATH),
    results_dir: Path = typer.Option(STAGE5AW_RESULTS_DIR),
    out_decisions: Path = typer.Option(STAGE5AW_REPAIRED_HUMAN_REVIEW_DECISIONS_PATH),
    out_unresolved: Path = typer.Option(
        STAGE5AW_REPAIRED_UNRESOLVED_VARIANTS_PATH,
        "--out-unresolved-variants",
        "--out-unresolved",
    ),
    out_extras: Path = typer.Option(
        STAGE5AW_REPAIRED_REVIEWER_EXTRA_TOKENS_PATH,
        "--out-reviewer-extras",
        "--out-extras",
    ),
    out_malformed: Path = typer.Option(STAGE5AW_MALFORMED_FRAGMENTS_PATH),
) -> None:
    decisions, unresolved, extras, malformed = repair_stage5aw_decision_variants(
        decision_file=decision_file,
        stage5au_case_challenges=stage5au_case_challenges,
        stage5ap_alphabet_registry=stage5ap_alphabet_registry,
        parser_policy=parser_policy,
        results_dir=results_dir,
        out_decisions=out_decisions,
        out_unresolved=out_unresolved,
        out_extras=out_extras,
        out_malformed=out_malformed,
    )
    console.print(f"repaired_decision_record_count={decisions['decision_record_count']}")
    console.print(f"repaired_unresolved_variant_count={unresolved['unresolved_token_variant_count']}")
    console.print(f"repaired_reviewer_extra_possible_token_count={extras['repaired_reviewer_extra_possible_token_count']}")
    console.print(f"malformed_possible_token_fragment_count={malformed['malformed_possible_token_fragment_count']}")


@app.command("build-stage5aw-repaired-branch-manifest")
def build_stage5aw_repaired_branch_manifest_command(
    repaired_decisions: Path = typer.Option(STAGE5AW_REPAIRED_HUMAN_REVIEW_DECISIONS_PATH),
    repaired_unresolved: Path = typer.Option(
        STAGE5AW_REPAIRED_UNRESOLVED_VARIANTS_PATH,
        "--repaired-unresolved-variants",
        "--repaired-unresolved",
    ),
    repaired_extras: Path = typer.Option(
        STAGE5AW_REPAIRED_REVIEWER_EXTRA_TOKENS_PATH,
        "--repaired-reviewer-extras",
        "--repaired-extras",
    ),
    malformed_fragments: Path = typer.Option(STAGE5AW_MALFORMED_FRAGMENTS_PATH),
    stage5ap_transcription: Path = typer.Option(TRANSCRIPTION_PATH),
    stage5ap_mapping_preflight: Path = typer.Option(MAPPING_PATH),
    results_dir: Path = typer.Option(STAGE5AW_RESULTS_DIR),
    out_impact: Path = typer.Option(STAGE5AW_REPAIRED_PRIMARY60_IMPACT_PATH),
    out_branch_manifest: Path = typer.Option(STAGE5AW_REPAIRED_BRANCH_MANIFEST_PATH),
) -> None:
    impact, manifest = build_stage5aw_repaired_branch_manifest(
        repaired_decisions=repaired_decisions,
        repaired_unresolved=repaired_unresolved,
        repaired_extras=repaired_extras,
        malformed_fragments=malformed_fragments,
        stage5ap_transcription=stage5ap_transcription,
        stage5ap_mapping_preflight=stage5ap_mapping_preflight,
        results_dir=results_dir,
        out_impact=out_impact,
        out_branch_manifest=out_branch_manifest,
    )
    console.print(f"primary60_mappable_option_count={impact['primary60_mappable_option_count']}")
    console.print(f"primary60_unmappable_option_count={impact['primary60_unmappable_option_count']}")
    console.print(f"branch_count_upper_bound_product={manifest['branch_count_upper_bound_product']}")


@app.command("build-stage5aw-updates")
def build_stage5aw_updates_command(
    repaired_unresolved: Path = typer.Option(
        STAGE5AW_REPAIRED_UNRESOLVED_VARIANTS_PATH,
        "--repaired-unresolved-variants",
        "--repaired-unresolved",
    ),
    impact_summary: Path = typer.Option(STAGE5AW_REPAIRED_PRIMARY60_IMPACT_PATH),
    branch_manifest: Path = typer.Option(STAGE5AW_REPAIRED_BRANCH_MANIFEST_PATH),
    out_canonical_update: Path = typer.Option(STAGE5AW_CANONICAL_UPDATE_PATH),
    out_null_control: Path = typer.Option(
        STAGE5AW_NULL_CONTROL_UPDATE_PATH,
        "--out-null-control-update",
        "--out-null-control",
    ),
    out_dwh_context: Path = typer.Option(STAGE5AW_DWH_CONTEXT_PATH),
) -> None:
    canonical, null_control, dwh = build_stage5aw_updates(
        repaired_unresolved=repaired_unresolved,
        impact_summary=impact_summary,
        branch_manifest=branch_manifest,
        out_canonical_update=out_canonical_update,
        out_null_control=out_null_control,
        out_dwh_context=out_dwh_context,
    )
    console.print(f"canonical_transcription_changed={str(canonical['canonical_transcription_changed']).lower()}")
    console.print(f"future_preflight_must_use_stage5aw_repaired_manifest={str(null_control['future_preflight_must_use_stage5aw_repaired_manifest']).lower()}")
    console.print(f"dwh_defined={str(dwh['dwh_defined']).lower()}")


@app.command("build-stage5aw-summary")
def build_stage5aw_summary_command(
    audit: Path = typer.Option(STAGE5AW_DECISION_PARSER_AUDIT_PATH),
    policy: Path = typer.Option(STAGE5AW_PARSER_POLICY_PATH),
    repaired_decisions: Path = typer.Option(STAGE5AW_REPAIRED_HUMAN_REVIEW_DECISIONS_PATH),
    repaired_unresolved: Path = typer.Option(
        STAGE5AW_REPAIRED_UNRESOLVED_VARIANTS_PATH,
        "--repaired-unresolved-variants",
        "--repaired-unresolved",
    ),
    repaired_extras: Path = typer.Option(
        STAGE5AW_REPAIRED_REVIEWER_EXTRA_TOKENS_PATH,
        "--repaired-reviewer-extras",
        "--repaired-extras",
    ),
    malformed_fragments: Path = typer.Option(STAGE5AW_MALFORMED_FRAGMENTS_PATH),
    impact_summary: Path = typer.Option(STAGE5AW_REPAIRED_PRIMARY60_IMPACT_PATH),
    branch_manifest: Path = typer.Option(STAGE5AW_REPAIRED_BRANCH_MANIFEST_PATH),
    canonical_update: Path = typer.Option(STAGE5AW_CANONICAL_UPDATE_PATH),
    null_control: Path = typer.Option(
        STAGE5AW_NULL_CONTROL_UPDATE_PATH,
        "--null-control-update",
        "--null-control",
    ),
    dwh_context: Path = typer.Option(STAGE5AW_DWH_CONTEXT_PATH),
    out_guardrail: Path = typer.Option(STAGE5AW_GUARDRAIL_PATH),
    out_next_stage: Path = typer.Option(STAGE5AW_NEXT_STAGE_DECISION_PATH),
    out_summary: Path = typer.Option(STAGE5AW_SUMMARY_PATH),
    results_dir: Path = typer.Option(STAGE5AW_RESULTS_DIR),
) -> None:
    guard, next_stage, summary = build_stage5aw_summary(
        audit=audit,
        policy=policy,
        repaired_decisions=repaired_decisions,
        repaired_unresolved=repaired_unresolved,
        repaired_extras=repaired_extras,
        malformed_fragments=malformed_fragments,
        impact_summary=impact_summary,
        branch_manifest=branch_manifest,
        canonical_update=canonical_update,
        null_control=null_control,
        dwh_context=dwh_context,
        out_guardrail=out_guardrail,
        out_next_stage=out_next_stage,
        out_summary=out_summary,
        results_dir=results_dir,
    )
    console.print(f"parser_repair_only={str(guard['parser_repair_only']).lower()}")
    console.print(f"selected_next_stage_title={next_stage['selected_next_stage_title']}")
    console.print(f"stage5aw_repaired_reviewer_extra_possible_token_count={summary['stage5aw_repaired_reviewer_extra_possible_token_count']}")


@app.command("validate-stage5aw")
def validate_stage5aw_command(
    audit: Path = typer.Option(STAGE5AW_DECISION_PARSER_AUDIT_PATH),
    policy: Path = typer.Option(STAGE5AW_PARSER_POLICY_PATH),
    repaired_decisions: Path = typer.Option(STAGE5AW_REPAIRED_HUMAN_REVIEW_DECISIONS_PATH),
    repaired_unresolved: Path = typer.Option(
        STAGE5AW_REPAIRED_UNRESOLVED_VARIANTS_PATH,
        "--repaired-unresolved-variants",
        "--repaired-unresolved",
    ),
    repaired_extras: Path = typer.Option(
        STAGE5AW_REPAIRED_REVIEWER_EXTRA_TOKENS_PATH,
        "--repaired-reviewer-extras",
        "--repaired-extras",
    ),
    malformed_fragments: Path = typer.Option(STAGE5AW_MALFORMED_FRAGMENTS_PATH),
    impact_summary: Path = typer.Option(STAGE5AW_REPAIRED_PRIMARY60_IMPACT_PATH),
    branch_manifest: Path = typer.Option(STAGE5AW_REPAIRED_BRANCH_MANIFEST_PATH),
    canonical_update: Path = typer.Option(STAGE5AW_CANONICAL_UPDATE_PATH),
    null_control: Path = typer.Option(
        STAGE5AW_NULL_CONTROL_UPDATE_PATH,
        "--null-control-update",
        "--null-control",
    ),
    dwh_context: Path = typer.Option(STAGE5AW_DWH_CONTEXT_PATH),
    guardrail: Path = typer.Option(STAGE5AW_GUARDRAIL_PATH),
    next_stage: Path = typer.Option(STAGE5AW_NEXT_STAGE_DECISION_PATH, "--next-stage-decision", "--next-stage"),
    summary: Path = typer.Option(STAGE5AW_SUMMARY_PATH),
    results_dir: Path = typer.Option(STAGE5AW_RESULTS_DIR),
) -> None:
    counts, errors = validate_stage5aw(
        audit=audit,
        policy=policy,
        repaired_decisions=repaired_decisions,
        repaired_unresolved=repaired_unresolved,
        repaired_extras=repaired_extras,
        malformed_fragments=malformed_fragments,
        impact_summary=impact_summary,
        branch_manifest=branch_manifest,
        canonical_update=canonical_update,
        null_control=null_control,
        dwh_context=dwh_context,
        guardrail=guardrail,
        next_stage=next_stage,
        summary=summary,
        results_dir=results_dir,
    )
    for key, value in counts.items():
        console.print(f"{key}={str(value).lower() if isinstance(value, bool) else value}")
    for error in errors:
        console.print(error)
    if errors:
        raise typer.Exit(1)
    console.print("token_block_stage5aw_valid=true")


@app.command("build-stage5ay-preflight-design")
def build_stage5ay_preflight_design_command(
    stage5ap_transcription: Path = typer.Option(TRANSCRIPTION_PATH),
    stage5ap_alphabet_registry: Path = typer.Option(ALPHABET_PATH),
    stage5ap_mapping_preflight: Path = typer.Option(MAPPING_PATH),
    stage5ar_coordinate_validation: Path = typer.Option(STAGE5AR_COORDINATE_VALIDATION_PATH),
    stage5aw_branch_manifest: Path = typer.Option(STAGE5AW_REPAIRED_BRANCH_MANIFEST_PATH),
    stage5aw_impact_summary: Path = typer.Option(STAGE5AW_REPAIRED_PRIMARY60_IMPACT_PATH),
    stage5aw_null_control: Path = typer.Option(STAGE5AW_NULL_CONTROL_UPDATE_PATH),
    stage5ax_run_summary: Path = typer.Option("data/ci/stage5ax-parallel-validation-run-summary.yaml"),
    results_dir: Path = typer.Option(STAGE5AY_RESULTS_DIR),
    out_source_inputs: Path = typer.Option(STAGE5AY_PREFLIGHT_SOURCE_INPUTS_PATH),
    out_policy: Path = typer.Option(STAGE5AY_PREFLIGHT_DESIGN_POLICY_PATH),
    out_branch_eligibility: Path = typer.Option(STAGE5AY_BRANCH_ELIGIBILITY_POLICY_PATH),
    out_branch_budget: Path = typer.Option(STAGE5AY_BRANCH_COUNT_BUDGET_PATH),
) -> None:
    source_inputs, policy, eligibility, budget = build_stage5ay_preflight_design(
        stage5ap_transcription=stage5ap_transcription,
        stage5ap_alphabet_registry=stage5ap_alphabet_registry,
        stage5ap_mapping_preflight=stage5ap_mapping_preflight,
        stage5ar_coordinate_validation=stage5ar_coordinate_validation,
        stage5aw_branch_manifest=stage5aw_branch_manifest,
        stage5aw_impact_summary=stage5aw_impact_summary,
        stage5aw_null_control=stage5aw_null_control,
        stage5ax_run_summary=stage5ax_run_summary,
        results_dir=results_dir,
        out_source_inputs=out_source_inputs,
        out_policy=out_policy,
        out_branch_eligibility=out_branch_eligibility,
        out_branch_budget=out_branch_budget,
    )
    console.print(f"source_input_record_count={source_inputs['source_record_count']}")
    console.print(f"branch_eligibility_option_record_count={eligibility['option_record_count']}")
    console.print(f"branch_upper_bound_product={budget['branch_count_upper_bound_product']}")
    console.print(f"stage5aw_repaired_branch_manifest_used={str(policy['stage5aw_repaired_branch_manifest_used']).lower()}")


@app.command("build-stage5ay-control-manifests")
def build_stage5ay_control_manifests_command(
    preflight_policy: Path = typer.Option(STAGE5AY_PREFLIGHT_DESIGN_POLICY_PATH),
    branch_eligibility: Path = typer.Option(STAGE5AY_BRANCH_ELIGIBILITY_POLICY_PATH),
    stage5ap_null_control: Path = typer.Option(NULL_CONTROL_PATH),
    stage5aw_null_control: Path = typer.Option(STAGE5AW_NULL_CONTROL_UPDATE_PATH),
    results_dir: Path = typer.Option(STAGE5AY_RESULTS_DIR),
    out_variant_family: Path = typer.Option(STAGE5AY_BOUNDED_VARIANT_FAMILY_MANIFEST_PATH),
    out_null_control_family: Path = typer.Option(STAGE5AY_NULL_CONTROL_FAMILY_MANIFEST_PATH),
    out_alphabet_control: Path = typer.Option(STAGE5AY_ALPHABET_CONTROL_MANIFEST_PATH),
    out_reading_order: Path = typer.Option(STAGE5AY_READING_ORDER_CONTROL_MANIFEST_PATH),
    out_page_split: Path = typer.Option(STAGE5AY_PAGE_SPLIT_CONTROL_MANIFEST_PATH),
    out_source_control: Path = typer.Option(STAGE5AY_SOURCE_CONTROL_MANIFEST_PATH),
) -> None:
    variant, null_control, alphabet, reading, page_split, source = build_stage5ay_control_manifests(
        preflight_policy=preflight_policy,
        branch_eligibility=branch_eligibility,
        stage5ap_null_control=stage5ap_null_control,
        stage5aw_null_control=stage5aw_null_control,
        results_dir=results_dir,
        out_variant_family=out_variant_family,
        out_null_control_family=out_null_control_family,
        out_alphabet_control=out_alphabet_control,
        out_reading_order=out_reading_order,
        out_page_split=out_page_split,
        out_source_control=out_source_control,
    )
    control_count = (
        len(null_control["families"])
        + len(alphabet["families"])
        + len(reading["families"])
        + len(page_split["families"])
        + len(source["families"])
    )
    console.print(f"variant_family_count={variant['family_count']}")
    console.print(f"control_family_count={control_count}")
    console.print("controls_executed=false")


@app.command("build-stage5ay-execution-gates")
def build_stage5ay_execution_gates_command(
    source_inputs: Path = typer.Option(STAGE5AY_PREFLIGHT_SOURCE_INPUTS_PATH),
    branch_budget: Path = typer.Option(STAGE5AY_BRANCH_COUNT_BUDGET_PATH),
    variant_family: Path = typer.Option(STAGE5AY_BOUNDED_VARIANT_FAMILY_MANIFEST_PATH),
    null_control_family: Path = typer.Option(STAGE5AY_NULL_CONTROL_FAMILY_MANIFEST_PATH),
    results_dir: Path = typer.Option(STAGE5AY_RESULTS_DIR),
    out_result_schema_preview: Path = typer.Option(STAGE5AY_FUTURE_RESULT_SCHEMA_PREVIEW_PATH),
    out_execution_gates: Path = typer.Option(STAGE5AY_EXECUTION_GATES_PATH),
    out_dwh_context: Path = typer.Option(STAGE5AY_DWH_PREFLIGHT_CONTEXT_PATH),
) -> None:
    result_schema, gates, dwh = build_stage5ay_execution_gates(
        source_inputs=source_inputs,
        branch_budget=branch_budget,
        variant_family=variant_family,
        null_control_family=null_control_family,
        results_dir=results_dir,
        out_result_schema_preview=out_result_schema_preview,
        out_execution_gates=out_execution_gates,
        out_dwh_context=out_dwh_context,
    )
    console.print(f"execution_gate_count={len(gates['gates'])}")
    console.print(f"dwh_operational_status={dwh['dwh_operational_status']}")
    console.print(f"future_result_schema_preview_only={str(result_schema['future_result_schema_preview_only']).lower()}")


@app.command("build-stage5ay-summary")
def build_stage5ay_summary_command(
    source_inputs: Path = typer.Option(STAGE5AY_PREFLIGHT_SOURCE_INPUTS_PATH),
    policy: Path = typer.Option(STAGE5AY_PREFLIGHT_DESIGN_POLICY_PATH),
    branch_eligibility: Path = typer.Option(STAGE5AY_BRANCH_ELIGIBILITY_POLICY_PATH),
    variant_family: Path = typer.Option(STAGE5AY_BOUNDED_VARIANT_FAMILY_MANIFEST_PATH),
    null_control_family: Path = typer.Option(STAGE5AY_NULL_CONTROL_FAMILY_MANIFEST_PATH),
    alphabet_control: Path = typer.Option(STAGE5AY_ALPHABET_CONTROL_MANIFEST_PATH),
    reading_order: Path = typer.Option(STAGE5AY_READING_ORDER_CONTROL_MANIFEST_PATH),
    page_split: Path = typer.Option(STAGE5AY_PAGE_SPLIT_CONTROL_MANIFEST_PATH),
    source_control: Path = typer.Option(STAGE5AY_SOURCE_CONTROL_MANIFEST_PATH),
    branch_budget: Path = typer.Option(STAGE5AY_BRANCH_COUNT_BUDGET_PATH),
    result_schema_preview: Path = typer.Option(STAGE5AY_FUTURE_RESULT_SCHEMA_PREVIEW_PATH),
    execution_gates: Path = typer.Option(STAGE5AY_EXECUTION_GATES_PATH),
    dwh_context: Path = typer.Option(STAGE5AY_DWH_PREFLIGHT_CONTEXT_PATH),
    out_guardrail: Path = typer.Option(STAGE5AY_GUARDRAIL_PATH),
    out_next_stage: Path = typer.Option(STAGE5AY_NEXT_STAGE_DECISION_PATH),
    out_summary: Path = typer.Option(STAGE5AY_SUMMARY_PATH),
) -> None:
    _guardrail, next_stage, summary = build_stage5ay_summary(
        source_inputs=source_inputs,
        policy=policy,
        branch_eligibility=branch_eligibility,
        variant_family=variant_family,
        null_control_family=null_control_family,
        alphabet_control=alphabet_control,
        reading_order=reading_order,
        page_split=page_split,
        source_control=source_control,
        branch_budget=branch_budget,
        result_schema_preview=result_schema_preview,
        execution_gates=execution_gates,
        dwh_context=dwh_context,
        out_guardrail=out_guardrail,
        out_next_stage=out_next_stage,
        out_summary=out_summary,
    )
    console.print(f"selected_next_stage_title={next_stage['selected_next_stage_title']}")
    console.print(f"manifest_family_count={summary['manifest_family_count']}")
    console.print(f"token_experiments_executed={str(summary['token_experiments_executed']).lower()}")


@app.command("validate-stage5ay")
def validate_stage5ay_command(
    source_inputs: Path = typer.Option(STAGE5AY_PREFLIGHT_SOURCE_INPUTS_PATH),
    policy: Path = typer.Option(STAGE5AY_PREFLIGHT_DESIGN_POLICY_PATH),
    branch_eligibility: Path = typer.Option(STAGE5AY_BRANCH_ELIGIBILITY_POLICY_PATH),
    variant_family: Path = typer.Option(STAGE5AY_BOUNDED_VARIANT_FAMILY_MANIFEST_PATH),
    null_control_family: Path = typer.Option(STAGE5AY_NULL_CONTROL_FAMILY_MANIFEST_PATH),
    alphabet_control: Path = typer.Option(STAGE5AY_ALPHABET_CONTROL_MANIFEST_PATH),
    reading_order: Path = typer.Option(STAGE5AY_READING_ORDER_CONTROL_MANIFEST_PATH),
    page_split: Path = typer.Option(STAGE5AY_PAGE_SPLIT_CONTROL_MANIFEST_PATH),
    source_control: Path = typer.Option(STAGE5AY_SOURCE_CONTROL_MANIFEST_PATH),
    branch_budget: Path = typer.Option(STAGE5AY_BRANCH_COUNT_BUDGET_PATH),
    result_schema_preview: Path = typer.Option(STAGE5AY_FUTURE_RESULT_SCHEMA_PREVIEW_PATH),
    execution_gates: Path = typer.Option(STAGE5AY_EXECUTION_GATES_PATH),
    dwh_context: Path = typer.Option(STAGE5AY_DWH_PREFLIGHT_CONTEXT_PATH),
    guardrail: Path = typer.Option(STAGE5AY_GUARDRAIL_PATH),
    next_stage_decision: Path = typer.Option(STAGE5AY_NEXT_STAGE_DECISION_PATH),
    summary: Path = typer.Option(STAGE5AY_SUMMARY_PATH),
    results_dir: Path = typer.Option(STAGE5AY_RESULTS_DIR),
) -> None:
    counts, errors = validate_stage5ay(
        source_inputs=source_inputs,
        policy=policy,
        branch_eligibility=branch_eligibility,
        variant_family=variant_family,
        null_control_family=null_control_family,
        alphabet_control=alphabet_control,
        reading_order=reading_order,
        page_split=page_split,
        source_control=source_control,
        branch_budget=branch_budget,
        result_schema_preview=result_schema_preview,
        execution_gates=execution_gates,
        dwh_context=dwh_context,
        guardrail=guardrail,
        next_stage_decision=next_stage_decision,
        summary=summary,
        results_dir=results_dir,
    )
    for key, value in counts.items():
        console.print(f"{key}={str(value).lower() if isinstance(value, bool) else value}")
    for error in errors:
        console.print(error)
    if errors:
        raise typer.Exit(1)
    console.print("token_block_stage5ay_valid=true")


def register(root_app: typer.Typer) -> None:
    root_app.add_typer(app, name="token-block")
