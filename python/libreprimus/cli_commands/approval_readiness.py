"""Approval readiness CLI commands."""
# ruff: noqa: F403,F405

from __future__ import annotations

import typer

from libreprimus.cli_commands.common import *

approval_readiness_app = typer.Typer(no_args_is_help=True)


DEFAULT_STAGE2I_PROPOSAL_DIR = Path("experiments/proposals/stage2i")
DEFAULT_STAGE2I_READINESS_DIR = Path("experiments/results/approval-readiness/stage2i")


@approval_readiness_app.command("validate")
def approval_readiness_validate(
    proposal: Path = typer.Option(..., "--proposal", help="Experiment proposal path."),
    approval: Path | None = typer.Option(None, "--approval", help="Approval record path."),
) -> None:
    """Validate Stage 2I proposal approval readiness without execution."""
    try:
        analysis = analyze_approval_readiness(
            _resolve_existing_path(proposal, "Experiment proposal"),
            approval_path=_resolve_existing_path(approval, "Approval record") if approval else None,
        )
    except (FileNotFoundError, ValueError) as error:
        console.print(f"[red]{error}[/red]")
        raise typer.Exit(1) from error
    _print_readiness_analysis(analysis)


@approval_readiness_app.command("human-summary")
def approval_readiness_human_summary(
    proposal: Path = typer.Option(..., "--proposal", help="Experiment proposal path."),
    approval: Path | None = typer.Option(None, "--approval", help="Approval record path."),
) -> None:
    """Print a concise human decision summary without generating outputs."""
    try:
        packet = build_approval_readiness_packet(
            _resolve_existing_path(proposal, "Experiment proposal"),
            approval_path=_resolve_existing_path(approval, "Approval record") if approval else None,
            out_dir=_resolve_output_path(DEFAULT_STAGE2I_READINESS_DIR),
        )
    except (FileNotFoundError, ValueError) as error:
        console.print(f"[red]{error}[/red]")
        raise typer.Exit(1) from error
    _print_human_readiness_summary(packet)


@approval_readiness_app.command("inspect-paths")
def approval_readiness_inspect_paths(
    proposal: Path = typer.Option(..., "--proposal", help="Experiment proposal path."),
) -> None:
    """Print exact files a reviewer may inspect for a Stage 2I proposal."""
    try:
        proposal_path = _resolve_existing_path(proposal, "Experiment proposal")
        approval_path = _matching_stage2i_pending_approval(proposal_path.parent, proposal_path)
        packet = build_approval_readiness_packet(
            proposal_path,
            approval_path=approval_path,
            out_dir=_resolve_output_path(DEFAULT_STAGE2I_READINESS_DIR),
        )
    except (FileNotFoundError, ValueError) as error:
        console.print(f"[red]{error}[/red]")
        raise typer.Exit(1) from error
    console.print(f"proposal_path={packet.proposal_path}")
    console.print(f"proposal_exists={str(Path(packet.proposal_path).is_file()).lower()}")
    console.print(f"approval_path={packet.approval_path}")
    console.print(f"approval_exists={str(Path(packet.approval_path).is_file()).lower()}")
    for key, path in packet.generated_output_preview.items():
        console.print(f"{key}={path}")
        console.print(f"{key}_exists={str(Path(path).is_file()).lower()}")
    for item in packet.corpus_slice.get("metadata_paths", []):
        console.print(f"metadata_path={item['path']}")
        console.print(f"metadata_path_exists={str(item['exists']).lower()}")
        console.print(f"metadata_path_role={item['role']}")


@approval_readiness_app.command("packet")
def approval_readiness_packet(
    proposal: Path = typer.Option(..., "--proposal", help="Experiment proposal path."),
    approval: Path | None = typer.Option(None, "--approval", help="Approval record path."),
    out_dir: Path = typer.Option(DEFAULT_STAGE2I_READINESS_DIR, "--out-dir", help="Generated readiness output directory."),
    allow_warnings: bool = typer.Option(False, "--allow-warnings", help="Return success despite warnings."),
) -> None:
    """Generate a Stage 2I approval-readiness packet without execution."""
    try:
        packet = build_approval_readiness_packet(
            _resolve_existing_path(proposal, "Experiment proposal"),
            approval_path=_resolve_existing_path(approval, "Approval record") if approval else None,
            out_dir=_resolve_output_path(out_dir),
        )
        paths = write_approval_readiness_outputs(_resolve_output_path(out_dir), packet)
    except (FileNotFoundError, ValueError) as error:
        console.print(f"[red]{error}[/red]")
        raise typer.Exit(1) from error
    for name, path in paths.items():
        console.print(f"{name}={path}")
    _print_readiness_packet(packet)
    if packet.warnings and not allow_warnings:
        raise typer.Exit(1)


@approval_readiness_app.command("stage2i-review")
def approval_readiness_stage2i_review(
    proposal_dir: Path = typer.Option(
        DEFAULT_STAGE2I_PROPOSAL_DIR,
        "--proposal-dir",
        help="Directory containing Stage 2I proposals.",
    ),
    out_dir: Path = typer.Option(DEFAULT_STAGE2I_READINESS_DIR, "--out-dir", help="Generated readiness output directory."),
    allow_warnings: bool = typer.Option(False, "--allow-warnings", help="Return success despite warnings."),
) -> None:
    """Generate readiness packets for every Stage 2I proposal."""
    resolved_dir = _resolve_output_path(proposal_dir)
    output_dir = _resolve_output_path(out_dir)
    packets = []
    warning_count = 0
    for proposal_path in sorted(path for path in resolved_dir.glob("*.yaml") if "request" not in path.name):
        approval_path = _matching_stage2i_pending_approval(resolved_dir, proposal_path)
        try:
            packet = build_approval_readiness_packet(proposal_path, approval_path=approval_path, out_dir=output_dir)
            write_approval_readiness_outputs(output_dir, packet)
        except (FileNotFoundError, ValueError) as error:
            console.print(f"[red]{proposal_path.name}: {error}[/red]")
            raise typer.Exit(1) from error
        packets.append(packet)
        warning_count += len(packet.warnings)
        console.print(f"{packet.proposal_id}=approval_status:{packet.approval_status}")
    summary_path = write_approval_readiness_summary(output_dir, packets)
    console.print(f"summary={summary_path}")
    console.print(f"proposal_count={len(packets)}")
    console.print(f"packet_count={len(packets)}")
    console.print(f"pending_count={sum(1 for packet in packets if packet.approval_status == 'pending')}")
    console.print(f"approved_count={sum(1 for packet in packets if packet.approval_status == 'approved')}")
    console.print(f"candidate_count_estimate_total={sum(packet.candidate_count_estimate for packet in packets)}")
    console.print(f"blocking_condition_count={sum(len(packet.blocking_conditions) for packet in packets)}")
    if warning_count and not allow_warnings:
        raise typer.Exit(1)


@approval_readiness_app.command("summary")
def approval_readiness_summary(
    results_dir: Path = typer.Option(
        DEFAULT_STAGE2I_READINESS_DIR,
        "--results-dir",
        help="Generated approval-readiness result directory.",
    ),
) -> None:
    """Print generated Stage 2I approval-readiness summary counts."""
    resolved = _resolve_output_path(results_dir)
    summary = load_approval_readiness_summary(resolved)
    packets = load_approval_readiness_packets(resolved)
    for key in [
        "proposal_count",
        "packet_count",
        "pending_count",
        "approved_count",
        "candidate_count_estimate_total",
        "blocking_condition_count",
    ]:
        console.print(f"{key}={summary.get(key, 0)}")
    for packet in packets:
        console.print(f"{packet['proposal_id']}={packet['approval_status']}")
        preview = packet.get("generated_output_preview", {})
        if isinstance(preview, dict) and preview.get("review_markdown"):
            console.print(f"{packet['proposal_id']}_review_markdown={preview['review_markdown']}")


def _matching_stage2i_pending_approval(proposal_dir: Path, proposal_path: Path) -> Path | None:
    expected = proposal_dir / "approval-records" / f"{proposal_path.stem.replace('-review', '-pending-approval')}.yaml"
    if expected.is_file():
        return expected
    candidates = sorted((proposal_dir / "approval-records").glob("*pending-approval.yaml"))
    return candidates[0] if candidates else None


def _print_readiness_analysis(analysis) -> None:
    console.print("Approval-readiness validation OK")
    console.print(f"proposal_id={analysis.proposal.proposal_id}")
    console.print(f"proposal_sha256={analysis.proposal.sha256}")
    console.print(f"readiness_status={analysis.readiness_status}")
    console.print(f"approval_status={analysis.approval_status}")
    console.print(f"real_unsolved_material_touched={str(analysis.real_unsolved_material_touched).lower()}")
    console.print(f"candidate_count_estimate={analysis.candidate_count_estimate}")
    console.print(f"candidate_count_upper_bound={analysis.candidate_count_upper_bound}")
    console.print(f"blocking_condition_count={len(analysis.blocking_conditions)}")
    console.print("execution_enabled=false")
    console.print("approved_for_execution=false")
    console.print("candidate_generation_enabled=false")
    console.print("scoring_enabled=false")
    console.print("cuda_enabled=false")


def _print_readiness_packet(packet) -> None:
    console.print(f"packet_id={packet.packet_id}")
    console.print(f"proposal_id={packet.proposal_id}")
    console.print(f"approval_status={packet.approval_status}")
    console.print(f"approved_for_execution={str(packet.approved_for_execution).lower()}")
    console.print(f"execution_enabled={str(packet.execution_enabled).lower()}")
    console.print(f"candidate_count_estimate={packet.candidate_count_estimate}")
    console.print(f"candidate_count_upper_bound={packet.candidate_count_upper_bound}")
    console.print(f"blocking_condition_count={len(packet.blocking_conditions)}")
    console.print(f"real_unsolved_material_touched={str(packet.real_unsolved_material_touched).lower()}")
    console.print(f"recommended_decision={packet.recommended_decision}")


def _print_human_readiness_summary(packet) -> None:
    console.print(f"proposal_id={packet.proposal_id}")
    console.print(f"approval_status={packet.approval_status}")
    console.print(f"approved_for_execution={str(packet.approved_for_execution).lower()}")
    console.print(f"execution_enabled={str(packet.execution_enabled).lower()}")
    console.print(f"candidate_count={packet.transform_summary['total_candidate_count']}")
    console.print(f"candidate_count_upper_bound={packet.transform_summary['candidate_count_upper_bound']}")
    console.print(f"search_execution_enabled={str(packet.search_execution_enabled).lower()}")
    console.print(f"candidate_generation_enabled={str(packet.candidate_generation_enabled).lower()}")
    console.print(f"scoring_enabled={str(packet.scoring_enabled).lower()}")
    console.print(f"cuda_enabled={str(packet.cuda_enabled).lower()}")
    console.print(f"blocking_conditions={len(packet.blocking_conditions)}")
    console.print(f"recommended_decision={packet.recommended_decision}")
    for condition in packet.blocking_conditions:
        console.print(f"blocking_condition={condition}")
    for option in packet.decision_options:
        console.print(f"decision_option_{option['option']}={option['decision']}")




def register(root_app: typer.Typer) -> None:
    """Register this module's Typer apps on the public root app."""
    root_app.add_typer(approval_readiness_app, name="approval-readiness")
