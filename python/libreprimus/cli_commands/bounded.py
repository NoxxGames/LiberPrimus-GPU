"""Bounded experiment, bounded run, candidate inspection, and scoring CLI commands."""
# ruff: noqa: F403,F405

from __future__ import annotations

import typer

from libreprimus.cli_commands.common import *

bounded_experiment_app = typer.Typer(no_args_is_help=True)
bounded_run_app = typer.Typer(no_args_is_help=True)
candidate_inspect_app = typer.Typer(no_args_is_help=True)
scoring_app = typer.Typer(no_args_is_help=True)


DEFAULT_STAGE2J_POLICY = Path("experiments/policies/operator-policy-v0.yaml")
DEFAULT_STAGE2J_QUEUE = Path("experiments/queues/stage2j-bounded-cpu-queue.yaml")
DEFAULT_STAGE2J_BOUNDED_RESULTS_DIR = Path("experiments/results/bounded-auto-runs/stage2j")
DEFAULT_STAGE3A_BOUNDED_RESULTS_DIR = Path("experiments/results/bounded-auto-runs/stage3a")
DEFAULT_STAGE3B_BOUNDED_RESULTS_DIR = Path("experiments/results/bounded-auto-runs/stage3b")
DEFAULT_STAGE3B_INSPECTION_MD = Path("research-log/2026-05-16-stage-3b-stage3a-lead-inspection.md")
DEFAULT_STAGE3C_CALIBRATION_RESULTS_DIR = Path("experiments/results/scoring-calibration/stage3c")
DEFAULT_STAGE3D_BOUNDED_RESULTS_DIR = Path("experiments/results/bounded-auto-runs/stage3d")
DEFAULT_STAGE3E_QUEUE = Path("experiments/queues/stage3e-bounded-cpu-queue.yaml")
DEFAULT_STAGE3E_BOUNDED_RESULTS_DIR = Path("experiments/results/bounded-auto-runs/stage3e")
DEFAULT_STAGE3F_BOUNDED_RESULTS_DIR = Path("experiments/results/bounded-auto-runs/stage3f")
DEFAULT_STAGE3G_BOUNDED_RESULTS_DIR = Path("experiments/results/bounded-auto-runs/stage3g")
DEFAULT_STAGE3H_QUEUE = Path("experiments/queues/stage3h-bounded-cpu-queue.yaml")
DEFAULT_STAGE3H_BOUNDED_RESULTS_DIR = Path("experiments/results/bounded-auto-runs/stage3h")
DEFAULT_STAGE3J_QUEUE = Path("experiments/queues/stage3j-bounded-cpu-queue.yaml")
DEFAULT_STAGE3J_BOUNDED_RESULTS_DIR = Path("experiments/results/bounded-auto-runs/stage3j")


@bounded_experiment_app.command("validate-policy")
def bounded_experiment_validate_policy(
    policy: Path = typer.Option(DEFAULT_STAGE2J_POLICY, "--policy", help="Operator policy path."),
) -> None:
    """Validate a standing bounded-experiment operator policy."""
    try:
        loaded = load_operator_policy(_resolve_existing_path(policy, "Operator policy"))
    except (FileNotFoundError, ValueError) as error:
        console.print(f"[red]{error}[/red]")
        raise typer.Exit(1) from error
    console.print("Operator policy validation OK")
    console.print(f"policy_id={loaded.policy_id}")
    console.print(f"max_candidate_count={loaded.max_candidate_count}")
    console.print(f"max_estimated_runtime_seconds={loaded.max_estimated_runtime_seconds}")
    console.print(f"max_generated_output_mb={loaded.max_generated_output_mb:g}")


@bounded_experiment_app.command("validate-queue")
def bounded_experiment_validate_queue(
    queue: Path = typer.Option(DEFAULT_STAGE2J_QUEUE, "--queue", help="Bounded experiment queue path."),
) -> None:
    """Validate a bounded experiment queue manifest."""
    try:
        loaded = load_bounded_queue(_resolve_existing_path(queue, "Bounded experiment queue"))
    except (FileNotFoundError, ValueError) as error:
        console.print(f"[red]{error}[/red]")
        raise typer.Exit(1) from error
    console.print("Bounded experiment queue validation OK")
    console.print(f"queue_id={loaded.queue_id}")
    console.print(f"policy_id={loaded.policy_id}")
    console.print(f"item_count={len(loaded.items)}")


@bounded_experiment_app.command("check-queue")
def bounded_experiment_check_queue(
    policy: Path = typer.Option(DEFAULT_STAGE2J_POLICY, "--policy", help="Operator policy path."),
    queue: Path = typer.Option(DEFAULT_STAGE2J_QUEUE, "--queue", help="Bounded experiment queue path."),
) -> None:
    """Check every queue item against the standing operator policy."""
    try:
        checks = check_bounded_queue_paths(
            _resolve_existing_path(policy, "Operator policy"),
            _resolve_existing_path(queue, "Bounded experiment queue"),
        )
    except (FileNotFoundError, ValueError) as error:
        console.print(f"[red]{error}[/red]")
        raise typer.Exit(1) from error
    _print_bounded_policy_checks(checks)


@bounded_experiment_app.command("run-next")
def bounded_experiment_run_next(
    policy: Path = typer.Option(DEFAULT_STAGE2J_POLICY, "--policy", help="Operator policy path."),
    queue: Path = typer.Option(DEFAULT_STAGE2J_QUEUE, "--queue", help="Bounded experiment queue path."),
    out_dir: Path = typer.Option(DEFAULT_STAGE2J_BOUNDED_RESULTS_DIR, "--out-dir", help="Generated output directory."),
    allow_warnings: bool = typer.Option(False, "--allow-warnings", help="Run warning-only policy-passing items."),
) -> None:
    """Run the next policy-passing bounded experiment item."""
    try:
        checks, results, summary_path = run_next_bounded_experiment(
            _resolve_existing_path(policy, "Operator policy"),
            _resolve_existing_path(queue, "Bounded experiment queue"),
            _resolve_output_path(out_dir),
            allow_warnings=allow_warnings,
        )
    except (FileNotFoundError, ValueError) as error:
        console.print(f"[red]{error}[/red]")
        raise typer.Exit(1) from error
    _print_bounded_policy_checks(checks)
    _print_bounded_run_results(results)
    console.print(f"summary={summary_path}")


@bounded_experiment_app.command("run-all")
def bounded_experiment_run_all(
    policy: Path = typer.Option(DEFAULT_STAGE2J_POLICY, "--policy", help="Operator policy path."),
    queue: Path = typer.Option(DEFAULT_STAGE2J_QUEUE, "--queue", help="Bounded experiment queue path."),
    out_dir: Path = typer.Option(DEFAULT_STAGE2J_BOUNDED_RESULTS_DIR, "--out-dir", help="Generated output directory."),
    allow_warnings: bool = typer.Option(False, "--allow-warnings", help="Run warning-only policy-passing items."),
) -> None:
    """Run every policy-passing bounded experiment item and block over-budget items."""
    try:
        checks, results, summary_path = run_all_bounded_experiments(
            _resolve_existing_path(policy, "Operator policy"),
            _resolve_existing_path(queue, "Bounded experiment queue"),
            _resolve_output_path(out_dir),
            allow_warnings=allow_warnings,
        )
    except (FileNotFoundError, ValueError) as error:
        console.print(f"[red]{error}[/red]")
        raise typer.Exit(1) from error
    _print_bounded_policy_checks(checks)
    _print_bounded_run_results(results)
    console.print(f"summary={summary_path}")


@bounded_experiment_app.command("summary")
def bounded_experiment_summary(
    results_dir: Path = typer.Option(
        DEFAULT_STAGE2J_BOUNDED_RESULTS_DIR,
        "--results-dir",
        help="Generated bounded auto-run results directory.",
    ),
) -> None:
    """Print generated bounded auto-run summary counts."""
    resolved = _resolve_output_path(results_dir)
    summary = load_bounded_experiment_summary(resolved)
    results = load_bounded_experiment_results(resolved)
    for key in [
        "item_count",
        "policy_pass_count",
        "policy_blocked_count",
        "executed_count",
        "deferred_count",
        "blocked_count",
        "result_count",
        "candidate_count_total",
    ]:
        console.print(f"{key}={summary.get(key, 0)}")
    for result in results:
        console.print(f"{result.get('item_id')}={result.get('execution_status')}")


@bounded_experiment_app.command("dry-run-queue")
def bounded_experiment_dry_run_queue(
    policy: Path = typer.Option(DEFAULT_STAGE2J_POLICY, "--policy", help="Operator policy path."),
    queue: Path = typer.Option(DEFAULT_STAGE3E_QUEUE, "--queue", help="Stage 3E bounded experiment queue path."),
    out_dir: Path = typer.Option(DEFAULT_STAGE3E_BOUNDED_RESULTS_DIR, "--out-dir", help="Generated dry-run output directory."),
    allow_warnings: bool = typer.Option(False, "--allow-warnings", help="Accepted for symmetry; dry-run records warnings."),
) -> None:
    """Dry-run a bounded queue and validate deterministic candidate counts."""
    try:
        summary = dry_run_stage3e_queue(
            policy_path=_resolve_existing_path(policy, "Operator policy"),
            queue_path=_resolve_existing_path(queue, "Bounded experiment queue"),
            out_dir=_resolve_output_path(out_dir),
        )
    except (FileNotFoundError, ValueError) as error:
        console.print(f"[red]{error}[/red]")
        raise typer.Exit(1) from error
    if not allow_warnings and any(result.warnings for result in summary.results):
        console.print("[yellow]dry_run_warnings_present=true[/yellow]")
    console.print(f"queue_id={summary.queue_id}")
    console.print(f"item_count={summary.item_count}")
    console.print(f"total_candidate_estimate={summary.total_candidate_estimate}")
    console.print(f"runnable_now_count={summary.runnable_now_count}")
    console.print(f"needs_executor_count={summary.needs_executor_count}")
    console.print(f"dry_run_only_count={summary.dry_run_only_count}")
    console.print(f"blocked_count={summary.blocked_count}")
    for result in summary.results:
        console.print(
            f"{result.item_id}=declared:{result.declared_candidate_count};calculated:{result.calculated_candidate_count};"
            f"policy:{result.policy_status};executor:{result.executor_status}"
        )
        for warning in result.warnings:
            console.print(f"{result.item_id}_warning={warning}")
    console.print(f"summary={summary.output_path}")


@bounded_run_app.command("run-caesar-affine")
def bounded_run_caesar_affine(
    policy: Path = typer.Option(DEFAULT_STAGE2J_POLICY, "--policy", help="Operator policy path."),
    queue: Path = typer.Option(DEFAULT_STAGE2J_QUEUE, "--queue", help="Bounded experiment queue path."),
    item_id: str = typer.Option(
        "stage2j-caesar-affine-first-reviewable-slice",
        "--item-id",
        help="Queue item to run.",
    ),
    out_dir: Path = typer.Option(DEFAULT_STAGE3A_BOUNDED_RESULTS_DIR, "--out-dir", help="Generated output directory."),
    top_k: int = typer.Option(25, "--top-k", min=1, help="Number of top candidates to write."),
    allow_warnings: bool = typer.Option(False, "--allow-warnings", help="Run warning-only policy-passing items."),
    direction: str = typer.Option("auto", "--direction", help="Transform convention: auto, forward, or reverse."),
) -> None:
    """Run the bounded Stage 3A Caesar plus affine CPU candidate enumeration."""
    try:
        summary = run_caesar_affine_from_paths(
            _resolve_existing_path(policy, "Operator policy"),
            _resolve_existing_path(queue, "Bounded experiment queue"),
            item_id=item_id,
            out_dir=_resolve_output_path(out_dir),
            top_k=top_k,
            allow_warnings=allow_warnings,
            direction=direction,
        )
    except (FileNotFoundError, ValueError) as error:
        console.print(f"[red]{error}[/red]")
        raise typer.Exit(1) from error
    _print_stage3a_run_summary(summary)


@bounded_run_app.command("summary")
def bounded_run_summary(
    results_dir: Path = typer.Option(
        DEFAULT_STAGE3A_BOUNDED_RESULTS_DIR,
        "--results-dir",
        help="Generated Stage 3A bounded run directory.",
    ),
) -> None:
    """Print the generated Stage 3A bounded run summary."""
    try:
        summary = load_bounded_run_summary(_resolve_output_path(results_dir))
    except FileNotFoundError as error:
        console.print(f"[red]{error}[/red]")
        raise typer.Exit(1) from error
    _print_stage3a_summary_payload(summary)


@bounded_run_app.command("run-vigenere-key-list")
def bounded_run_vigenere_key_list(
    policy: Path = typer.Option(DEFAULT_STAGE2J_POLICY, "--policy", help="Operator policy path."),
    queue: Path = typer.Option(Path("experiments/queues/stage3c-bounded-cpu-queue.yaml"), "--queue", help="Bounded experiment queue path."),
    item_id: str = typer.Option(
        "stage3c-small-vigenere-known-motif-key-list",
        "--item-id",
        help="Queue item to run.",
    ),
    out_dir: Path = typer.Option(DEFAULT_STAGE3D_BOUNDED_RESULTS_DIR, "--out-dir", help="Generated output directory."),
    top_k: int = typer.Option(4, "--top-k", min=1, help="Number of top candidates to write."),
    allow_warnings: bool = typer.Option(False, "--allow-warnings", help="Run warning-only policy-passing items."),
) -> None:
    """Run the bounded Stage 3D explicit Vigenere key-list preview."""
    try:
        summary = run_vigenere_key_list_from_paths(
            _resolve_existing_path(policy, "Operator policy"),
            _resolve_existing_path(queue, "Bounded experiment queue"),
            item_id=item_id,
            out_dir=_resolve_output_path(out_dir),
            top_k=top_k,
            allow_warnings=allow_warnings,
        )
    except (FileNotFoundError, ValueError) as error:
        console.print(f"[red]{error}[/red]")
        raise typer.Exit(1) from error
    _print_stage3a_run_summary(summary)


@bounded_run_app.command("run-vigenere-key-pack")
def bounded_run_vigenere_key_pack(
    policy: Path = typer.Option(DEFAULT_STAGE2J_POLICY, "--policy", help="Operator policy path."),
    queue: Path = typer.Option(DEFAULT_STAGE3E_QUEUE, "--queue", help="Bounded experiment queue path."),
    item_id: str = typer.Option(
        "stage3e_vig_lp_evidence_pack_v1",
        "--item-id",
        help="Queue item to run.",
    ),
    out_dir: Path = typer.Option(DEFAULT_STAGE3F_BOUNDED_RESULTS_DIR, "--out-dir", help="Generated output directory."),
    top_k: int = typer.Option(25, "--top-k", min=1, help="Number of top candidates to write."),
    allow_warnings: bool = typer.Option(False, "--allow-warnings", help="Run warning-only policy-passing items."),
) -> None:
    """Run a bounded explicit Vigenere key-pack queue item."""
    try:
        summary = run_vigenere_key_pack_from_paths(
            _resolve_existing_path(policy, "Operator policy"),
            _resolve_existing_path(queue, "Bounded experiment queue"),
            item_id=item_id,
            out_dir=_resolve_output_path(out_dir),
            top_k=top_k,
            allow_warnings=allow_warnings,
        )
    except (FileNotFoundError, ValueError) as error:
        console.print(f"[red]{error}[/red]")
        raise typer.Exit(1) from error
    _print_stage3a_run_summary(summary)


@bounded_run_app.command("run-prime-offset-sweep")
def bounded_run_prime_offset_sweep(
    policy: Path = typer.Option(DEFAULT_STAGE2J_POLICY, "--policy", help="Operator policy path."),
    queue: Path = typer.Option(DEFAULT_STAGE3E_QUEUE, "--queue", help="Bounded experiment queue path."),
    item_id: str = typer.Option(
        "stage3e_prime_minus_one_offsets_v1",
        "--item-id",
        help="Queue item to run.",
    ),
    out_dir: Path = typer.Option(DEFAULT_STAGE3G_BOUNDED_RESULTS_DIR, "--out-dir", help="Generated output directory."),
    top_k: int = typer.Option(25, "--top-k", min=1, help="Number of top candidates to write."),
    allow_warnings: bool = typer.Option(False, "--allow-warnings", help="Run warning-only policy-passing items."),
) -> None:
    """Run the bounded Stage 3G p56-local prime-minus-one offset sweep."""
    try:
        summary = run_prime_offset_sweep_from_paths(
            _resolve_existing_path(policy, "Operator policy"),
            _resolve_existing_path(queue, "Bounded experiment queue"),
            item_id=item_id,
            out_dir=_resolve_output_path(out_dir),
            top_k=top_k,
            allow_warnings=allow_warnings,
        )
    except (FileNotFoundError, ValueError) as error:
        console.print(f"[red]{error}[/red]")
        raise typer.Exit(1) from error
    _print_stage3a_run_summary(summary)


@bounded_run_app.command("run-reset-advance-ablation")
def bounded_run_reset_advance_ablation(
    policy: Path = typer.Option(DEFAULT_STAGE2J_POLICY, "--policy", help="Operator policy path."),
    queue: Path = typer.Option(DEFAULT_STAGE3H_QUEUE, "--queue", help="Bounded experiment queue path."),
    item_id: str = typer.Option(
        "stage3h_reset_advance_ablation_v1",
        "--item-id",
        help="Queue item to run.",
    ),
    out_dir: Path = typer.Option(DEFAULT_STAGE3H_BOUNDED_RESULTS_DIR, "--out-dir", help="Generated output directory."),
    top_k: int = typer.Option(25, "--top-k", min=1, help="Number of top candidates to write."),
    allow_warnings: bool = typer.Option(False, "--allow-warnings", help="Run warning-only policy-passing items."),
) -> None:
    """Run the bounded Stage 3H reset/advance ablation."""
    try:
        summary = run_reset_advance_ablation_from_paths(
            _resolve_existing_path(policy, "Operator policy"),
            _resolve_existing_path(queue, "Bounded experiment queue"),
            item_id=item_id,
            out_dir=_resolve_output_path(out_dir),
            top_k=top_k,
            allow_warnings=allow_warnings,
        )
    except (FileNotFoundError, ValueError) as error:
        console.print(f"[red]{error}[/red]")
        raise typer.Exit(1) from error
    _print_stage3a_run_summary(summary)


@bounded_run_app.command("run-mersenne-stream-probe")
def bounded_run_mersenne_stream_probe(
    policy: Path = typer.Option(DEFAULT_STAGE2J_POLICY, "--policy", help="Operator policy path."),
    queue: Path = typer.Option(DEFAULT_STAGE3J_QUEUE, "--queue", help="Bounded experiment queue path."),
    item_id: str = typer.Option(
        "stage3j_mersenne_prime_stream_tiny_v1",
        "--item-id",
        help="Queue item to run.",
    ),
    out_dir: Path = typer.Option(DEFAULT_STAGE3J_BOUNDED_RESULTS_DIR, "--out-dir", help="Generated output directory."),
    top_k: int = typer.Option(25, "--top-k", min=1, help="Number of top candidates to write."),
    allow_warnings: bool = typer.Option(False, "--allow-warnings", help="Run warning-only policy-passing items."),
) -> None:
    """Run the bounded Stage 3J Mersenne/perfect-number stream probe."""
    try:
        summary = run_mersenne_stream_probe_from_paths(
            _resolve_existing_path(policy, "Operator policy"),
            _resolve_existing_path(queue, "Bounded experiment queue"),
            item_id=item_id,
            out_dir=_resolve_output_path(out_dir),
            top_k=top_k,
            allow_warnings=allow_warnings,
        )
    except (FileNotFoundError, ValueError) as error:
        console.print(f"[red]{error}[/red]")
        raise typer.Exit(1) from error
    _print_stage3a_run_summary(summary)


@bounded_run_app.command("rerank")
def bounded_run_rerank(
    results_dir: Path = typer.Option(DEFAULT_STAGE3A_BOUNDED_RESULTS_DIR, "--results-dir", help="Existing generated results directory."),
    out_dir: Path = typer.Option(DEFAULT_STAGE3B_BOUNDED_RESULTS_DIR, "--out-dir", help="Generated rerank output directory."),
    top_k: int = typer.Option(25, "--top-k", min=1, help="Number of reranked top candidates to write."),
    allow_warnings: bool = typer.Option(False, "--allow-warnings", help="Allow warning-bearing rerank input."),
) -> None:
    """Rerank generated candidates with the current refined minimal triage scorer."""
    try:
        records = load_candidate_records(_resolve_output_path(results_dir))
        reranked = rerank_candidates(records)
    except (FileNotFoundError, ValueError) as error:
        console.print(f"[red]{error}[/red]")
        raise typer.Exit(1) from error
    warnings = [] if allow_warnings else []
    top_records = reranked[:top_k]
    original_top = max(records, key=lambda record: float(record.get("score_summary", {}).get("total_score", 0.0)))
    refined_top = top_records[0]
    output_dir = _resolve_output_path(out_dir)
    reranked_path = write_inspection_jsonl(output_dir / "reranked_top_candidates.jsonl", top_records)
    summary_payload = {
        "record_type": "stage3b_rerank_summary",
        "source_results_dir": str(_resolve_output_path(results_dir)),
        "candidate_count": len(records),
        "top_k": len(top_records),
        "original_top": _candidate_cli_summary(original_top),
        "refined_top": _candidate_cli_summary(refined_top),
        "top_candidate_changed": original_top.get("candidate_index") != refined_top.get("candidate_index"),
        "confidence_label": refined_top.get("score_summary", {}).get("confidence_label", "unlabeled"),
        "solve_claim": False,
        "cuda_used": False,
        "generated_outputs_ignored": True,
        "output_paths": {"reranked_top_candidates": str(reranked_path)},
    }
    summary_path = write_inspection_json(output_dir / "rerank_summary.json", summary_payload)
    warning_path = None
    if warnings:
        warning_path = write_inspection_jsonl(output_dir / "warnings.jsonl", [{"record_type": "stage3b_rerank_warning", "warning": warning} for warning in warnings])
    console.print("rerank_executed=true")
    console.print(f"candidate_count={len(records)}")
    console.print(f"original_top_params={json.dumps(original_top.get('transform_parameters', {}), sort_keys=True)}")
    console.print(f"refined_top_params={json.dumps(refined_top.get('transform_parameters', {}), sort_keys=True)}")
    console.print(f"top_candidate_changed={str(summary_payload['top_candidate_changed']).lower()}")
    console.print(f"confidence_label={summary_payload['confidence_label']}")
    console.print(f"reranked_top_candidates={reranked_path}")
    console.print(f"rerank_summary={summary_path}")
    if warning_path:
        console.print(f"warnings={warning_path}")


def _print_stage3a_run_summary(summary) -> None:
    payload = {
        "run_id": summary.run_id,
        "queue_item_id": summary.queue_item_id,
        "input_slice_id": summary.input_slice_id,
        "input_length": summary.input_length,
        "candidate_count": summary.candidate_count,
        "expected_candidate_count": summary.expected_candidate_count,
        "executed_candidate_count": summary.executed_candidate_count,
        "deferred_candidate_count": summary.deferred_candidate_count,
        "caesar_candidate_count": summary.caesar_candidate_count,
        "affine_candidate_count": summary.affine_candidate_count,
        "vigenere_candidate_count": summary.vigenere_candidate_count,
        "prime_candidate_count": summary.prime_candidate_count,
        "reset_advance_candidate_count": summary.reset_advance_candidate_count,
        "negative_control_count": summary.negative_control_count,
        "mersenne_candidate_count": summary.mersenne_candidate_count,
        "unique_stream_signature_count": summary.unique_stream_signature_count,
        "duplicate_stream_signature_count": summary.duplicate_stream_signature_count,
        "key_count": summary.key_count,
        "stream_variants": ",".join(summary.stream_variants or []),
        "directions": ",".join(summary.directions or []),
        "reset_modes": ",".join(summary.reset_modes or []),
        "advance_modes": ",".join(summary.advance_modes or []),
        "top_k_count": summary.top_k_count,
        "top_candidate_score": summary.top_candidate.get("total_score"),
        "top_candidate_length_normalized_score": summary.top_candidate.get("length_normalized_score"),
        "top_candidate_confidence_label": summary.top_candidate.get("confidence_label"),
        "top_candidate_calibrated_confidence_label": summary.top_candidate.get("calibrated_confidence_label"),
        "top_candidate_transform_family": summary.top_candidate.get("transform_family"),
        "top_candidate_transform_parameters": json.dumps(summary.top_candidate.get("transform_parameters", {}), sort_keys=True),
        "top_candidate_key_text": summary.top_candidate.get("key_text"),
        "top_candidate_base_transform_id": summary.top_candidate.get("base_transform_id"),
        "top_candidate_base_transform_family": summary.top_candidate.get("base_transform_family"),
        "top_candidate_offset": summary.top_candidate.get("offset"),
        "top_candidate_direction": summary.top_candidate.get("direction"),
        "top_candidate_reset_mode": summary.top_candidate.get("reset_mode"),
        "top_candidate_advance_mode": summary.top_candidate.get("advance_mode"),
        "top_candidate_stream_variant": summary.top_candidate.get("stream_variant"),
        "top_candidate_stream_signature_sha256": summary.top_candidate.get("stream_signature_sha256"),
        "solve_claim": summary.solve_claim,
    }
    for key, value in payload.items():
        if isinstance(value, bool):
            value = str(value).lower()
        console.print(f"{key}={value}")
    for key, path in summary.output_paths.items():
        console.print(f"{key}={path}")


def _print_stage3a_summary_payload(summary: dict) -> None:
    top = summary.get("top_candidate", {})
    for key in [
        "run_id",
        "queue_item_id",
        "input_slice_id",
        "input_length",
        "candidate_count",
        "expected_candidate_count",
        "executed_candidate_count",
        "deferred_candidate_count",
        "caesar_candidate_count",
        "affine_candidate_count",
        "vigenere_candidate_count",
        "prime_candidate_count",
        "reset_advance_candidate_count",
        "negative_control_count",
        "mersenne_candidate_count",
        "unique_stream_signature_count",
        "duplicate_stream_signature_count",
        "key_count",
        "stream_variants",
        "directions",
        "reset_modes",
        "advance_modes",
        "top_k_count",
    ]:
        console.print(f"{key}={summary.get(key)}")
    console.print(f"top_candidate_score={top.get('total_score')}")
    console.print(f"top_candidate_length_normalized_score={top.get('length_normalized_score')}")
    console.print(f"top_candidate_confidence_label={top.get('confidence_label')}")
    console.print(f"top_candidate_calibrated_confidence_label={top.get('calibrated_confidence_label')}")
    console.print(f"top_candidate_transform_family={top.get('transform_family')}")
    console.print(f"top_candidate_transform_parameters={json.dumps(top.get('transform_parameters', {}), sort_keys=True)}")
    console.print(f"top_candidate_key_text={top.get('key_text')}")
    console.print(f"top_candidate_base_transform_id={top.get('base_transform_id')}")
    console.print(f"top_candidate_base_transform_family={top.get('base_transform_family')}")
    console.print(f"top_candidate_offset={top.get('offset')}")
    console.print(f"top_candidate_direction={top.get('direction')}")
    console.print(f"top_candidate_reset_mode={top.get('reset_mode')}")
    console.print(f"top_candidate_advance_mode={top.get('advance_mode')}")
    console.print(f"top_candidate_stream_variant={top.get('stream_variant')}")
    console.print(f"top_candidate_stream_signature_sha256={top.get('stream_signature_sha256')}")
    console.print(f"solve_claim={str(summary.get('solve_claim')).lower()}")
    for key, path in summary.get("output_paths", {}).items():
        console.print(f"{key}={path}")


@candidate_inspect_app.command("inspect-stage3a")
def candidate_inspect_stage3a(
    results_dir: Path = typer.Option(DEFAULT_STAGE3A_BOUNDED_RESULTS_DIR, "--results-dir", help="Generated Stage 3A results directory."),
    top_n: int = typer.Option(25, "--top-n", min=1, help="Number of top candidates to inspect."),
    out_markdown: Path = typer.Option(DEFAULT_STAGE3B_INSPECTION_MD, "--out-markdown", help="Committed summary Markdown path."),
) -> None:
    """Inspect Stage 3A leads and write a summary-only Markdown report."""
    try:
        inspection = inspect_results(_resolve_output_path(results_dir), top_n=top_n, rerank=True)
        written = write_inspection_markdown(out_markdown, inspection)
        validate_no_full_dump_in_markdown(written.read_text(encoding="utf-8"))
        payload = validate_summary_payload(to_summary_payload(inspection))
    except (FileNotFoundError, ValueError) as error:
        console.print(f"[red]{error}[/red]")
        raise typer.Exit(1) from error
    console.print(f"candidate_count={payload['candidate_count']}")
    console.print(f"top_candidate_transform={payload['top_candidate']['transform_family']}")
    console.print(f"refined_top_transform={payload['refined_top_candidate']['transform_family']}")
    console.print(f"qualitative_label={payload['qualitative_label']}")
    console.print(f"recommendation={payload['recommendation']}")
    console.print(f"markdown={written}")


@candidate_inspect_app.command("summary")
def candidate_inspect_summary(
    results_dir: Path = typer.Option(DEFAULT_STAGE3A_BOUNDED_RESULTS_DIR, "--results-dir", help="Generated results directory."),
) -> None:
    """Print a concise candidate-inspection summary without full candidate dumps."""
    try:
        inspection = inspect_results(_resolve_output_path(results_dir), top_n=25, rerank=False)
        payload = validate_summary_payload(to_summary_payload(inspection))
    except (FileNotFoundError, ValueError) as error:
        console.print(f"[red]{error}[/red]")
        raise typer.Exit(1) from error
    console.print(f"run_id={payload['run_id']}")
    console.print(f"candidate_count={payload['candidate_count']}")
    console.print(f"top_transform_family={payload['top_candidate']['transform_family']}")
    console.print(f"top_transform_parameters={json.dumps(payload['top_candidate']['transform_parameters'], sort_keys=True)}")
    console.print(f"top_score={payload['top_candidate']['total_score']}")
    console.print(f"qualitative_label={payload['qualitative_label']}")
    console.print(f"warning_count={len(payload['warnings'])}")


@scoring_app.command("calibrate")
def scoring_calibrate(
    stage3_results_dir: Path = typer.Option(DEFAULT_STAGE3A_BOUNDED_RESULTS_DIR, "--stage3-results-dir", help="Generated Stage 3A results directory."),
    stage3b_results_dir: Path = typer.Option(DEFAULT_STAGE3B_BOUNDED_RESULTS_DIR, "--stage3b-results-dir", help="Generated Stage 3B results directory."),
    out_dir: Path = typer.Option(DEFAULT_STAGE3C_CALIBRATION_RESULTS_DIR, "--out-dir", help="Generated calibration output directory."),
    allow_warnings: bool = typer.Option(False, "--allow-warnings", help="Allow warning-bearing calibration inputs."),
) -> None:
    """Run Stage 3C scoring calibration against controls and bounded candidates."""
    try:
        result = run_scoring_calibration(
            stage3_results_dir=_resolve_output_path(stage3_results_dir),
            stage3b_results_dir=_resolve_output_path(stage3b_results_dir),
            out_dir=_resolve_output_path(out_dir),
            allow_warnings=allow_warnings,
        )
    except Exception as error:  # noqa: BLE001 - CLI reports errors consistently.
        console.print(f"[red]{error}[/red]")
        raise typer.Exit(1) from error
    summary = result.summary
    console.print("calibration_executed=true")
    console.print(f"positive_control_count={summary['positive_control_count']}")
    console.print(f"null_control_count={summary['null_control_count']}")
    console.print(f"negative_control_count={summary['negative_control_count']}")
    console.print(f"candidate_count={summary['candidate_count']}")
    console.print(f"stage3a_top_classification={summary['stage3a_top_classification']}")
    console.print(f"stage3b_top_classification={summary['stage3b_top_classification']}")
    console.print(f"recommended_next_step={summary['recommended_next_step']}")
    for name, path in result.output_paths.items():
        console.print(f"{name}={path}")


@scoring_app.command("crib-check")
def scoring_crib_check(
    text: str = typer.Option(..., "--text", help="Text to check against the tiny crib list."),
    cribs: Path = typer.Option(DEFAULT_CRIBS_PATH, "--cribs", help="Tiny crib-list path."),
) -> None:
    """Run a tiny transparent crib check on inline text."""
    try:
        crib_terms = load_cribs(_resolve_output_path(cribs))
        result = crib_check(text, cribs=crib_terms)
    except Exception as error:  # noqa: BLE001 - CLI reports errors consistently.
        console.print(f"[red]{error}[/red]")
        raise typer.Exit(1) from error
    console.print(f"crib_hit_count={result['crib_hit_count']}")
    console.print(f"crib_hits={','.join(result['crib_hits'])}")
    console.print("solve_claim=false")


@scoring_app.command("calibration-summary")
def scoring_calibration_summary(
    results_dir: Path = typer.Option(DEFAULT_STAGE3C_CALIBRATION_RESULTS_DIR, "--results-dir", help="Generated calibration results directory."),
) -> None:
    """Print a concise generated Stage 3C calibration summary."""
    path = _resolve_output_path(results_dir) / "calibration_summary.json"
    if not path.is_file():
        console.print(f"[red]Missing calibration summary: {path}[/red]")
        raise typer.Exit(1)
    summary = json.loads(path.read_text(encoding="utf-8"))
    console.print(f"calibration_id={summary.get('calibration_id')}")
    console.print(f"positive_control_count={summary.get('positive_control_count')}")
    console.print(f"null_control_count={summary.get('null_control_count')}")
    console.print(f"negative_control_count={summary.get('negative_control_count')}")
    console.print(f"candidate_count={summary.get('candidate_count')}")
    console.print(f"positive_score_range={json.dumps(summary.get('positive_score_range'), sort_keys=True)}")
    console.print(f"null_score_range={json.dumps(summary.get('null_score_range'), sort_keys=True)}")
    console.print(f"negative_score_range={json.dumps(summary.get('negative_score_range'), sort_keys=True)}")
    console.print(f"stage3a_top_classification={summary.get('stage3a_top_classification')}")
    console.print(f"stage3b_top_classification={summary.get('stage3b_top_classification')}")
    console.print(f"recommended_next_step={summary.get('recommended_next_step')}")
    console.print(f"solve_claim={str(summary.get('solve_claim')).lower()}")


def _candidate_cli_summary(record: dict) -> dict:
    score = dict(record.get("score_summary", {}))
    return {
        "candidate_index": record.get("candidate_index"),
        "transform_family": record.get("transform_family"),
        "transform_parameters": record.get("transform_parameters", {}),
        "total_score": score.get("total_score"),
        "length_normalized_score": score.get("length_normalized_score"),
        "confidence_label": score.get("confidence_label"),
        "output_sha256": record.get("output_sha256"),
    }


def _print_bounded_policy_checks(checks) -> None:
    console.print(f"item_count={len(checks)}")
    console.print(f"policy_pass_count={sum(1 for check in checks if not check.blocking_reasons)}")
    console.print(f"policy_blocked_count={sum(1 for check in checks if check.blocking_reasons)}")
    for check in checks:
        console.print(f"{check.item_id}=policy:{check.status}")
        for reason in check.blocking_reasons:
            console.print(f"{check.item_id}_blocking_reason={reason}")


def _print_bounded_run_results(results) -> None:
    console.print(f"result_count={len(results)}")
    console.print(f"executed_count={sum(1 for result in results if result.execution_performed)}")
    console.print(f"deferred_count={sum(1 for result in results if result.execution_status == 'deferred')}")
    console.print(f"blocked_count={sum(1 for result in results if result.execution_status == 'blocked')}")
    for result in results:
        console.print(f"{result.item_id}=execution:{result.execution_status}")
        if result.deferred_reason:
            console.print(f"{result.item_id}_deferred_reason={result.deferred_reason}")



def register(root_app: typer.Typer) -> None:
    """Register this module's Typer apps on the public root app."""
    root_app.add_typer(bounded_experiment_app, name="bounded-experiment")
    root_app.add_typer(bounded_run_app, name="bounded-run")
    root_app.add_typer(candidate_inspect_app, name="candidate-inspect")
    root_app.add_typer(scoring_app, name="scoring")
