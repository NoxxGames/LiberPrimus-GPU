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
    TRANSCRIPTION_PATH,
)
from .null_controls import build_null_control_plan
from .original_images import build_original_image_source_lock
from .page_split import build_page_split
from .pixel_coordinates import build_pixel_coordinates
from .provenance import build_source_lock
from .stage5ap import build_next_stage_decision, build_research_summary, build_summary
from .stage5ar import build_stage5ar_summary, build_stage5ar_updates, validate_stage5ar
from .transcription import build_transcription
from .validation import validate_stage5ap

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


def register(root_app: typer.Typer) -> None:
    root_app.add_typer(app, name="token-block")
