"""Experiment proposal CLI commands."""
# ruff: noqa: F403,F405

from __future__ import annotations

import typer

from libreprimus.cli_commands.common import *

proposal_app = typer.Typer(no_args_is_help=True)


DEFAULT_STAGE2G_PROPOSAL_DIR = Path("experiments/proposals/stage2g")
DEFAULT_STAGE2G_REVIEW_DIR = Path("experiments/results/proposal-reviews/stage2g")


@proposal_app.command("validate")
def proposal_validate(
    proposal: Path = typer.Option(..., "--proposal", help="Experiment proposal path."),
) -> None:
    """Validate a Stage 2G experiment proposal without execution."""
    try:
        loaded = load_experiment_proposal(_resolve_existing_path(proposal, "Experiment proposal"))
    except (FileNotFoundError, ValueError) as error:
        console.print(f"[red]{error}[/red]")
        raise typer.Exit(1) from error
    console.print("Experiment proposal validation OK")
    console.print(f"proposal_id={loaded.proposal_id}")
    console.print(f"proposal_sha256={loaded.sha256}")
    console.print("execution_enabled=false")
    console.print("approved_for_execution=false")
    console.print("search_execution_enabled=false")
    console.print("candidate_generation_enabled=false")
    console.print("scoring_enabled=false")
    console.print("cuda_enabled=false")


@proposal_app.command("review-packet")
def proposal_review_packet(
    proposal: Path = typer.Option(..., "--proposal", help="Experiment proposal path."),
    out_dir: Path = typer.Option(DEFAULT_STAGE2G_REVIEW_DIR, "--out-dir", help="Generated review packet output directory."),
    allow_warnings: bool = typer.Option(False, "--allow-warnings", help="Return success despite review warnings."),
) -> None:
    """Generate a human-review packet without executing the proposal."""
    try:
        loaded = load_experiment_proposal(_resolve_existing_path(proposal, "Experiment proposal"))
        output_dir = _resolve_output_path(out_dir)
        packet = build_review_packet(loaded, out_dir=output_dir)
        paths = write_review_packet_outputs(output_dir, packet)
    except (FileNotFoundError, ValueError) as error:
        console.print(f"[red]{error}[/red]")
        raise typer.Exit(1) from error
    for name, path in paths.items():
        console.print(f"{name}={path}")
    console.print(f"packet_id={packet.packet_id}")
    console.print(f"proposal_id={packet.proposal_id}")
    console.print(f"approval_status={packet.approval_status}")
    console.print(f"approved_for_execution={str(packet.approved_for_execution).lower()}")
    console.print(f"execution_blocked={str(packet.execution_blocked).lower()}")
    if packet.warnings and not allow_warnings:
        console.print("[red]Review packet produced warnings.[/red]")
        raise typer.Exit(1)


@proposal_app.command("check-approval")
def proposal_check_approval(
    proposal: Path = typer.Option(..., "--proposal", help="Experiment proposal path."),
    approval: Path | None = typer.Option(None, "--approval", help="Approval record path."),
) -> None:
    """Check whether a proposal has a valid approval record."""
    try:
        loaded = load_experiment_proposal(_resolve_existing_path(proposal, "Experiment proposal"))
        approval_record = load_approval_record(_resolve_existing_path(approval, "Approval record")) if approval else None
        gate = evaluate_approval_gate(loaded, approval_record)
    except (FileNotFoundError, ValueError) as error:
        console.print(f"[red]{error}[/red]")
        raise typer.Exit(1) from error
    console.print(f"proposal_id={gate.proposal_id}")
    console.print(f"approval_status={gate.approval_status}")
    console.print(f"approved_for_execution={str(gate.approved_for_execution).lower()}")
    console.print(f"execution_blocked={str(gate.execution_blocked).lower()}")
    console.print(f"reason={gate.reason}")


@proposal_app.command("stage2g-review-all")
def proposal_stage2g_review_all(
    proposal_dir: Path = typer.Option(DEFAULT_STAGE2G_PROPOSAL_DIR, "--proposal-dir", help="Directory containing Stage 2G proposals."),
    out_dir: Path = typer.Option(DEFAULT_STAGE2G_REVIEW_DIR, "--out-dir", help="Generated review packet output directory."),
    allow_warnings: bool = typer.Option(False, "--allow-warnings", help="Return success despite review warnings."),
) -> None:
    """Validate and review all Stage 2G proposal examples without execution."""
    resolved_dir = _resolve_output_path(proposal_dir)
    output_dir = _resolve_output_path(out_dir)
    packets = []
    warning_count = 0
    for proposal_path in sorted(resolved_dir.glob("*.yaml")):
        try:
            loaded = load_experiment_proposal(proposal_path)
            packet = build_review_packet(loaded, out_dir=output_dir)
            write_review_packet_outputs(output_dir, packet)
        except ValueError as error:
            console.print(f"[red]{proposal_path.name}: {error}[/red]")
            raise typer.Exit(1) from error
        packets.append(packet)
        warning_count += len(packet.warnings)
        console.print(f"{loaded.proposal_id}=blocked:{str(packet.execution_blocked).lower()}")
    summary_path = write_review_packet_summary(output_dir, packets)
    console.print(f"summary={summary_path}")
    console.print(f"proposal_count={len(packets)}")
    console.print(f"review_packet_count={len(packets)}")
    console.print(f"blocked_count={sum(1 for packet in packets if packet.execution_blocked)}")
    console.print(f"approved_count={sum(1 for packet in packets if packet.approved_for_execution)}")
    if warning_count and not allow_warnings:
        console.print("[red]Stage 2G review packets produced warnings.[/red]")
        raise typer.Exit(1)


@proposal_app.command("review-summary")
def proposal_review_summary(
    results_dir: Path = typer.Option(DEFAULT_STAGE2G_REVIEW_DIR, "--results-dir", help="Generated review packet directory."),
) -> None:
    """Print generated Stage 2G proposal review summary counts."""
    resolved = _resolve_output_path(results_dir)
    summary = load_review_packet_summary(resolved)
    packets = load_review_packets(resolved)
    for key in [
        "packet_count",
        "blocked_count",
        "approved_count",
        "pending_or_missing_count",
        "denied_count",
    ]:
        console.print(f"{key}={summary.get(key, 0)}")
    console.print(f"review_packet_records={len(packets)}")




def register(root_app: typer.Typer) -> None:
    """Register this module's Typer apps on the public root app."""
    root_app.add_typer(proposal_app, name="proposal")
