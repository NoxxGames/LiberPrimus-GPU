"""Public CLI root app and command group registration."""
# ruff: noqa: F403,F405

from __future__ import annotations

import typer

from libreprimus.cli_commands.common import *
from libreprimus.cli_commands import (
    legacy_workbook,
    legacy_pastebin,
    transcripts,
    corpus_alignment,
    profiles,
    corpus_candidates,
    reference_sources,
    transforms,
    solved_baselines,
    results,
    consistency,
    experiments,
    execution,
    proposals,
    approval_execution,
    approval_readiness,
    bounded,
    archive_visual,
    discord,
    discord_full_review,
    source_lock_triage,
    visual_annotation,
    bounded_numeric,
    source_delta_audit,
    source_lock_snapshots,
    stego_fixtures,
    cookie_refresh,
    cpu_batch,
    scoring_consolidation_cli,
    observation_review,
    observation_promotion,
    image_preflight,
    stego_positive_controls,
    benchmark_planning,
    cuda_planning,
    cuda_parity,
    cuda_solved_family_readiness,
    cuda_candidate_batch_abi,
    native_candidate_batch_conformance,
    prime_minus_one_native_contract,
    prime_minus_one_native_parity,
    prime_minus_one_native_reporting,
    prime_minus_one_cuda_contract,
    prime_minus_one_cuda_synthetic,
    prime_minus_one_cuda_synthetic_reporting,
    bounded_p56_cuda_parity,
    bounded_p56_mismatch,
    corrected_bounded_p56_reporting,
    source_harvester,
    website_render,
    deep_research_export,
    token_block,
    historical_route,
    stego_controls,
    cuda_build,
    cuda_kernel,
    cuda_kernel_contract,
    cuda_parity_reporting,
    gematria_cuda_prep,
    gematria_cuda_kernel,
    gematria_cuda_parity_reporting,
    gematria_solved_fixture_cuda,
    gematria_solved_fixture_cuda_reporting,
    gematria_solved_fixture_cuda_repeat,
    gematria_cuda_result_store,
    gematria_expanded_cuda_result_store,
    gematria_expanded_solved_fixture_cuda,
    gematria_expansion_candidate_mapping,
    gematria_solved_fixture_mapping,
    gematria_shift_contract,
    native_cpu,
    post_discord,
    research_synthesis,
    stego,
    solved_fixtures,
    parallel_validation,
    operator_console,
    source_browser,
)

app = typer.Typer(no_args_is_help=True)


@app.command()
def smoke() -> None:
    """Print the Stage 0A Python smoke message."""
    console.print("LiberPrimus Python Stage 0A smoke OK")


@app.command()
def paths() -> None:
    """Print important project paths."""
    table = Table("Name", "Path")
    table.add_row("repo_root", str(repo_root()))
    table.add_row("package_root", str(package_root()))
    console.print(table)


@app.command()
def toolchain() -> None:
    """Print a concise toolchain report."""
    table = Table("Tool", "Present", "Path", "Version")
    report = collect_toolchain()
    for name, status in report.items():
        if isinstance(status, ToolStatus):
            table.add_row(name, str(status.present).lower(), status.path or "", status.version or "")
        else:
            table.add_row(name, "true" if status else "false", status or "", "")
    console.print(table)


_COMMAND_MODULES = (
    legacy_workbook,
    legacy_pastebin,
    transcripts,
    corpus_alignment,
    profiles,
    corpus_candidates,
    reference_sources,
    transforms,
    solved_baselines,
    results,
    consistency,
    experiments,
    execution,
    proposals,
    approval_execution,
    approval_readiness,
    bounded,
    archive_visual,
    discord,
    discord_full_review,
    source_lock_triage,
    visual_annotation,
    bounded_numeric,
    source_delta_audit,
    source_lock_snapshots,
    stego_fixtures,
    cookie_refresh,
    cpu_batch,
    scoring_consolidation_cli,
    observation_review,
    observation_promotion,
    image_preflight,
    stego_positive_controls,
    benchmark_planning,
    cuda_planning,
    cuda_parity,
    cuda_solved_family_readiness,
    cuda_candidate_batch_abi,
    native_candidate_batch_conformance,
    prime_minus_one_native_contract,
    prime_minus_one_native_parity,
    prime_minus_one_native_reporting,
    prime_minus_one_cuda_contract,
    prime_minus_one_cuda_synthetic,
    prime_minus_one_cuda_synthetic_reporting,
    bounded_p56_cuda_parity,
    bounded_p56_mismatch,
    corrected_bounded_p56_reporting,
    source_harvester,
    website_render,
    deep_research_export,
    token_block,
    historical_route,
    stego_controls,
    cuda_build,
    cuda_kernel,
    cuda_kernel_contract,
    cuda_parity_reporting,
    gematria_cuda_prep,
    gematria_cuda_kernel,
    gematria_cuda_parity_reporting,
    gematria_solved_fixture_cuda,
    gematria_solved_fixture_cuda_reporting,
    gematria_solved_fixture_cuda_repeat,
    gematria_cuda_result_store,
    gematria_expanded_cuda_result_store,
    gematria_expanded_solved_fixture_cuda,
    gematria_expansion_candidate_mapping,
    gematria_solved_fixture_mapping,
    gematria_shift_contract,
    native_cpu,
    post_discord,
    research_synthesis,
    stego,
    solved_fixtures,
    parallel_validation,
    operator_console,
    source_browser,
)


def register_commands(root_app: typer.Typer = app) -> None:
    """Register all domain command groups on the root Typer app."""
    for module in _COMMAND_MODULES:
        module.register(root_app)


register_commands(app)

__all__ = ["app", "register_commands"]
