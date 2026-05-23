"""Typer commands for Stage 5AD-fix bounded p56 mismatch investigation."""

from __future__ import annotations

from pathlib import Path

import typer
from rich.console import Console

from .formula_trace import build_formula_trace
from .guardrails import build_guardrails
from .hash_lineage import build_hash_lineage
from .hash_material import build_hash_material
from .models import (
    FORMULA_TRACE_PATH,
    GUARDRAIL_PATH,
    HASH_LINEAGE_PATH,
    HASH_MATERIAL_PATH,
    NEXT_STAGE_DECISION_PATH,
    OUTPUT_DIR,
    REFERENCE_CONTRACT_PATH,
    REPAIR_READINESS_PATH,
    ROOT_CAUSE_PATH,
    STREAM_TRACE_PATH,
    SUMMARY_PATH,
    TOKEN_TRACE_PATH,
)
from .next_stage_decision import build_next_stage_decision
from .reference_contract import build_reference_contract
from .repair_readiness import build_repair_readiness
from .root_cause import build_root_cause
from .stream_trace import build_stream_trace
from .summary import build_summary
from .token_trace import build_token_trace
from .validation import validate_stage5ad_fix_results

console = Console()
app = typer.Typer(help="Stage 5AD-fix bounded p56 mismatch commands.", no_args_is_help=True)


@app.command("build-hash-lineage")
def build_hash_lineage_command(
    hash_lineage_out: Path = typer.Option(HASH_LINEAGE_PATH),
    out_dir: Path = typer.Option(OUTPUT_DIR),
    allow_warnings: bool = typer.Option(False),
) -> None:
    records = build_hash_lineage(hash_lineage_out=hash_lineage_out, out_dir=out_dir)
    console.print(f"hash_lineage_records={len(records)}")
    console.print(f"allow_warnings={str(allow_warnings).lower()}")


@app.command("build-token-trace")
def build_token_trace_command(
    token_trace_out: Path = typer.Option(TOKEN_TRACE_PATH),
    out_dir: Path = typer.Option(OUTPUT_DIR),
    allow_warnings: bool = typer.Option(False),
) -> None:
    records = build_token_trace(token_trace_out=token_trace_out, out_dir=out_dir)
    console.print(f"token_trace_records={len(records)}")
    console.print(f"token_trace_status={records[0]['token_trace_status']}")
    console.print(f"allow_warnings={str(allow_warnings).lower()}")


@app.command("build-stream-trace")
def build_stream_trace_command(
    stream_trace_out: Path = typer.Option(STREAM_TRACE_PATH),
    out_dir: Path = typer.Option(OUTPUT_DIR),
    allow_warnings: bool = typer.Option(False),
) -> None:
    records = build_stream_trace(stream_trace_out=stream_trace_out, out_dir=out_dir)
    console.print(f"stream_trace_records={len(records)}")
    console.print(f"allow_warnings={str(allow_warnings).lower()}")


@app.command("build-formula-trace")
def build_formula_trace_command(
    formula_trace_out: Path = typer.Option(FORMULA_TRACE_PATH),
    out_dir: Path = typer.Option(OUTPUT_DIR),
    allow_warnings: bool = typer.Option(False),
) -> None:
    records = build_formula_trace(formula_trace_out=formula_trace_out, out_dir=out_dir)
    console.print(f"formula_trace_records={len(records)}")
    console.print(f"formula_output_token_hash={records[0]['formula_output_token_hash']}")
    console.print(f"allow_warnings={str(allow_warnings).lower()}")


@app.command("build-hash-material-trace")
def build_hash_material_command(
    hash_material_out: Path = typer.Option(HASH_MATERIAL_PATH),
    out_dir: Path = typer.Option(OUTPUT_DIR),
    allow_warnings: bool = typer.Option(False),
) -> None:
    records = build_hash_material(hash_material_out=hash_material_out, out_dir=out_dir)
    console.print(f"hash_material_records={len(records)}")
    console.print(f"allow_warnings={str(allow_warnings).lower()}")


@app.command("build-reference-contract")
def build_reference_contract_command(
    reference_contract_out: Path = typer.Option(REFERENCE_CONTRACT_PATH),
    out_dir: Path = typer.Option(OUTPUT_DIR),
    allow_warnings: bool = typer.Option(False),
) -> None:
    records = build_reference_contract(reference_contract_out=reference_contract_out, out_dir=out_dir)
    console.print(f"reference_contract_records={len(records)}")
    console.print(f"contract_status={records[0]['contract_status']}")
    console.print(f"allow_warnings={str(allow_warnings).lower()}")


@app.command("build-root-cause")
def build_root_cause_command(
    root_cause_out: Path = typer.Option(ROOT_CAUSE_PATH),
    out_dir: Path = typer.Option(OUTPUT_DIR),
    allow_warnings: bool = typer.Option(False),
) -> None:
    records = build_root_cause(root_cause_out=root_cause_out, out_dir=out_dir)
    selected = next(record for record in records if record["primary_root_cause"] is True)
    console.print(f"root_cause_records={len(records)}")
    console.print(f"primary_root_cause={selected['cause_id']}")
    console.print(f"allow_warnings={str(allow_warnings).lower()}")


@app.command("build-repair-readiness")
def build_repair_readiness_command(
    repair_readiness_out: Path = typer.Option(REPAIR_READINESS_PATH),
    out_dir: Path = typer.Option(OUTPUT_DIR),
    allow_warnings: bool = typer.Option(False),
) -> None:
    records = build_repair_readiness(repair_readiness_out=repair_readiness_out, out_dir=out_dir)
    console.print(f"repair_readiness_records={len(records)}")
    console.print(f"allow_warnings={str(allow_warnings).lower()}")


@app.command("build-guardrails")
def build_guardrails_command(
    guardrail_out: Path = typer.Option(GUARDRAIL_PATH),
    out_dir: Path = typer.Option(OUTPUT_DIR),
    allow_warnings: bool = typer.Option(False),
) -> None:
    records = build_guardrails(guardrail_out=guardrail_out, out_dir=out_dir)
    console.print(f"guardrail_records={len(records)}")
    console.print(f"guardrail_status={records[0]['guardrail_status']}")
    console.print(f"allow_warnings={str(allow_warnings).lower()}")


@app.command("build-next-stage-decision")
def build_next_stage_command(
    next_stage_decision_out: Path = typer.Option(NEXT_STAGE_DECISION_PATH),
    out_dir: Path = typer.Option(OUTPUT_DIR),
    allow_warnings: bool = typer.Option(False),
) -> None:
    records = build_next_stage_decision(next_stage_decision_out=next_stage_decision_out, out_dir=out_dir)
    selected = next(record for record in records if record["selected"] is True)
    console.print(f"next_stage_decision_records={len(records)}")
    console.print(f"recommended_next_stage_title={selected['recommended_stage_title']}")
    console.print(f"allow_warnings={str(allow_warnings).lower()}")


@app.command("build-summary")
def build_summary_command(
    hash_lineage: Path = typer.Option(HASH_LINEAGE_PATH),
    token_trace: Path = typer.Option(TOKEN_TRACE_PATH),
    stream_trace: Path = typer.Option(STREAM_TRACE_PATH),
    formula_trace: Path = typer.Option(FORMULA_TRACE_PATH),
    hash_material: Path = typer.Option(HASH_MATERIAL_PATH),
    reference_contract: Path = typer.Option(REFERENCE_CONTRACT_PATH),
    root_cause: Path = typer.Option(ROOT_CAUSE_PATH),
    repair_readiness: Path = typer.Option(REPAIR_READINESS_PATH),
    guardrail: Path = typer.Option(GUARDRAIL_PATH),
    next_stage_decision: Path = typer.Option(NEXT_STAGE_DECISION_PATH),
    summary_out: Path = typer.Option(SUMMARY_PATH),
    out_dir: Path = typer.Option(OUTPUT_DIR),
    allow_warnings: bool = typer.Option(False),
) -> None:
    summary = build_summary(
        hash_lineage=hash_lineage,
        token_trace=token_trace,
        stream_trace=stream_trace,
        formula_trace=formula_trace,
        hash_material=hash_material,
        reference_contract=reference_contract,
        root_cause=root_cause,
        repair_readiness=repair_readiness,
        guardrail=guardrail,
        next_stage_decision=next_stage_decision,
        summary_out=summary_out,
        out_dir=out_dir,
    )
    console.print(f"primary_root_cause={summary['primary_root_cause']}")
    console.print(f"recommended_next_stage_title={summary['recommended_next_stage_title']}")
    console.print(f"allow_warnings={str(allow_warnings).lower()}")


@app.command("validate-stage5ad-fix")
def validate_stage5ad_fix(
    hash_lineage: Path = typer.Option(HASH_LINEAGE_PATH),
    token_trace: Path = typer.Option(TOKEN_TRACE_PATH),
    stream_trace: Path = typer.Option(STREAM_TRACE_PATH),
    formula_trace: Path = typer.Option(FORMULA_TRACE_PATH),
    hash_material: Path = typer.Option(HASH_MATERIAL_PATH),
    reference_contract: Path = typer.Option(REFERENCE_CONTRACT_PATH),
    root_cause: Path = typer.Option(ROOT_CAUSE_PATH),
    repair_readiness: Path = typer.Option(REPAIR_READINESS_PATH),
    guardrail: Path = typer.Option(GUARDRAIL_PATH),
    next_stage_decision: Path = typer.Option(NEXT_STAGE_DECISION_PATH),
    summary: Path = typer.Option(SUMMARY_PATH),
    results_dir: Path = typer.Option(OUTPUT_DIR),
) -> None:
    counts, errors = validate_stage5ad_fix_results(
        hash_lineage_path=hash_lineage,
        token_trace_path=token_trace,
        stream_trace_path=stream_trace,
        formula_trace_path=formula_trace,
        hash_material_path=hash_material,
        reference_contract_path=reference_contract,
        root_cause_path=root_cause,
        repair_readiness_path=repair_readiness,
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
    console.print("bounded_p56_mismatch_stage5ad_fix_valid=true")


@app.command("summary")
def summary_command(summary: Path = typer.Option(SUMMARY_PATH)) -> None:
    from .export import read_yaml

    payload = read_yaml(summary)
    for key in (
        "primary_root_cause",
        "cuda_formula_matches_stage5x_formula",
        "cuda_formula_matches_stage5w_expected",
        "reference_contract_repair_required",
        "cuda_kernel_repair_required",
        "hash_material_policy_repair_required",
        "recommended_next_stage_title",
    ):
        console.print(f"{key}={payload.get(key)}")


def register(root_app: typer.Typer) -> None:
    root_app.add_typer(app, name="bounded-p56-mismatch")
