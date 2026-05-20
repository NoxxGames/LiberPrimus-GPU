"""Stage 5C CUDA build/device detection CLI commands."""

from __future__ import annotations

from pathlib import Path

import typer
from rich.console import Console

from libreprimus.cuda_build.device_detection import detect_devices
from libreprimus.cuda_build.export import write_report
from libreprimus.cuda_build.models import (
    BUILD_PROFILES_PATH,
    DEVICE_PATH,
    SMOKE_BUILD_PATH,
    STAGE5C_OUTPUT_DIR,
    SUMMARY_PATH,
    TOOLCHAIN_PATH,
    TOOLCHAIN_REPORT,
)
from libreprimus.cuda_build.smoke_build import run_smoke_build
from libreprimus.cuda_build.summary import build_summary, load_summary
from libreprimus.cuda_build.toolchain_detection import build_profiles, detect_toolchain
from libreprimus.cuda_build.validation import validate_stage5c_results
from libreprimus.paths import repo_root

cuda_build_app = typer.Typer(no_args_is_help=True)
console = Console()


@cuda_build_app.command("profile-toolchain")
def cuda_build_profile_toolchain(
    manifest: Path = typer.Option(..., "--manifest", help="Stage 5C build/device manifest."),
    out_dir: Path = typer.Option(STAGE5C_OUTPUT_DIR, "--out-dir", help="Generated Stage 5C output directory."),
    profiles_out: Path = typer.Option(BUILD_PROFILES_PATH, "--profiles-out", help="Committed build profile YAML."),
    toolchain_out: Path = typer.Option(TOOLCHAIN_PATH, "--toolchain-out", help="Committed toolchain detection YAML."),
    allow_missing_cuda: bool = typer.Option(False, "--allow-missing-cuda", help="Record missing CUDA tools without failing."),
    allow_warnings: bool = typer.Option(False, "--allow-warnings", help="Allow missing optional toolchain records."),
) -> None:
    """Write no-GPU-safe CUDA build profiles and toolchain detection records."""

    _require_file(manifest)
    profiles = build_profiles(profiles_out=_resolve(profiles_out), out_dir=_resolve(out_dir))
    toolchain = detect_toolchain(toolchain_out=_resolve(toolchain_out), out_dir=_resolve(out_dir))
    write_report(_resolve(out_dir), TOOLCHAIN_REPORT, {"build_profiles": profiles, "toolchain_records": toolchain})
    toolchain_available = _toolchain_available(toolchain)
    console.print(f"build_profiles={len(profiles)}")
    console.print(f"toolchain_records={len(toolchain)}")
    console.print(f"cuda_toolchain_available={str(toolchain_available).lower()}")
    console.print("local_16gb_profile_required=false")
    console.print("compatibility_8gb_profile_present=true")
    console.print("no_gpu_ci_profile_present=true")
    if not toolchain_available and not (allow_missing_cuda or allow_warnings):
        raise typer.Exit(1)


@cuda_build_app.command("detect-device")
def cuda_build_detect_device(
    manifest: Path = typer.Option(..., "--manifest", help="Stage 5C build/device manifest."),
    out_dir: Path = typer.Option(STAGE5C_OUTPUT_DIR, "--out-dir", help="Generated Stage 5C output directory."),
    devices_out: Path = typer.Option(DEVICE_PATH, "--devices-out", help="Committed device detection YAML."),
    allow_no_gpu: bool = typer.Option(False, "--allow-no-gpu", help="Record no-GPU state without failing."),
    allow_warnings: bool = typer.Option(False, "--allow-warnings", help="Allow device detection warnings."),
) -> None:
    """Record CUDA device visibility without requiring a GPU."""

    _require_file(manifest)
    devices = detect_devices(devices_out=_resolve(devices_out), out_dir=_resolve(out_dir))
    device_available = any(record["device_status"] == "detected" for record in devices)
    local_16gb_detected = any(record.get("local_16gb_profile_detected") is True for record in devices)
    console.print(f"device_records={len(devices)}")
    console.print(f"cuda_device_available={str(device_available).lower()}")
    console.print(f"local_16gb_profile_detected={str(local_16gb_detected).lower()}")
    console.print("local_16gb_profile_required=false")
    console.print("compatibility_8gb_profile_present=true")
    console.print("no_gpu_ci_profile_present=true")
    if not device_available and not (allow_no_gpu or allow_warnings):
        raise typer.Exit(1)


@cuda_build_app.command("smoke-build")
def cuda_build_smoke_build(
    manifest: Path = typer.Option(..., "--manifest", help="Stage 5C smoke-build manifest."),
    out_dir: Path = typer.Option(STAGE5C_OUTPUT_DIR, "--out-dir", help="Generated Stage 5C output directory."),
    smoke_build_out: Path = typer.Option(SMOKE_BUILD_PATH, "--smoke-build-out", help="Committed smoke-build YAML."),
    attempt_build: bool = typer.Option(False, "--attempt-build", help="Configure/build existing CUDA smoke target if possible."),
    allow_missing_cuda: bool = typer.Option(False, "--allow-missing-cuda", help="Allow missing CUDA toolchain."),
    allow_no_gpu: bool = typer.Option(False, "--allow-no-gpu", help="Allow no-GPU environments."),
    allow_warnings: bool = typer.Option(False, "--allow-warnings", help="Allow skipped or failed optional smoke build."),
) -> None:
    """Optionally configure/build the existing CUDA smoke target without running it."""

    _require_file(manifest)
    smoke = run_smoke_build(
        smoke_build_out=_resolve(smoke_build_out),
        out_dir=_resolve(out_dir),
        attempt_build=attempt_build,
    )
    record = smoke[0]
    status = str(record["smoke_build_status"])
    console.print(f"smoke_build_records={len(smoke)}")
    console.print(f"smoke_build_attempted={str(record['smoke_build_attempted']).lower()}")
    console.print(f"smoke_build_status={_summary_smoke_status(status)}")
    console.print("smoke_test_executed=false")
    console.print("gpu_benchmark_performed=false")
    console.print("cuda_kernel_added=false")
    if status == "failed" and not allow_warnings:
        raise typer.Exit(1)
    if status == "skipped_missing_cuda" and not (allow_missing_cuda or allow_no_gpu or allow_warnings):
        raise typer.Exit(1)


@cuda_build_app.command("build-summary")
def cuda_build_build_summary(
    profiles: Path = typer.Option(BUILD_PROFILES_PATH, "--profiles", help="Committed build profiles YAML."),
    toolchain: Path = typer.Option(TOOLCHAIN_PATH, "--toolchain", help="Committed toolchain detection YAML."),
    devices: Path = typer.Option(DEVICE_PATH, "--devices", help="Committed device detection YAML."),
    smoke_build: Path = typer.Option(SMOKE_BUILD_PATH, "--smoke-build", help="Committed smoke-build YAML."),
    summary_out: Path = typer.Option(SUMMARY_PATH, "--summary-out", help="Committed Stage 5C summary YAML."),
    out_dir: Path = typer.Option(STAGE5C_OUTPUT_DIR, "--out-dir", help="Generated Stage 5C output directory."),
    allow_warnings: bool = typer.Option(False, "--allow-warnings", help="Allow no-GPU and skipped smoke-build states."),
) -> None:
    """Write the committed Stage 5C aggregate summary."""

    for path in (profiles, toolchain, devices, smoke_build):
        _require_file(path)
    summary = build_summary(
        profiles_path=_resolve(profiles),
        toolchain_path=_resolve(toolchain),
        devices_path=_resolve(devices),
        smoke_build_path=_resolve(smoke_build),
        summary_out=_resolve(summary_out),
        out_dir=_resolve(out_dir),
    )
    for key in _SUMMARY_KEYS:
        console.print(f"{key}={_format_value(summary[key])}")
    if summary["smoke_build_status"] == "failed" and not allow_warnings:
        raise typer.Exit(1)


@cuda_build_app.command("validate-stage5c")
def cuda_build_validate_stage5c(
    profiles: Path = typer.Option(BUILD_PROFILES_PATH, "--profiles", help="Committed build profiles YAML."),
    toolchain: Path = typer.Option(TOOLCHAIN_PATH, "--toolchain", help="Committed toolchain detection YAML."),
    devices: Path = typer.Option(DEVICE_PATH, "--devices", help="Committed device detection YAML."),
    smoke_build: Path = typer.Option(SMOKE_BUILD_PATH, "--smoke-build", help="Committed smoke-build YAML."),
    summary: Path = typer.Option(SUMMARY_PATH, "--summary", help="Committed Stage 5C summary YAML."),
    results_dir: Path = typer.Option(STAGE5C_OUTPUT_DIR, "--results-dir", help="Generated Stage 5C output directory."),
) -> None:
    """Validate Stage 5C CUDA build/device detection records."""

    try:
        counts, errors = validate_stage5c_results(
            profiles_path=_resolve(profiles),
            toolchain_path=_resolve(toolchain),
            devices_path=_resolve(devices),
            smoke_build_path=_resolve(smoke_build),
            summary_path=_resolve(summary),
            results_dir=_resolve(results_dir),
        )
    except (FileNotFoundError, ValueError) as error:
        console.print(f"[red]{error}[/red]")
        raise typer.Exit(1) from error
    for key, value in counts.items():
        console.print(f"{key}={_format_value(value)}")
    console.print(f"validation_error_count={len(errors)}")
    for error in errors:
        console.print(f"[red]{error}[/red]")
    if errors:
        raise typer.Exit(1)
    console.print("cuda_build_stage5c_valid=true")


@cuda_build_app.command("summary")
def cuda_build_summary(
    summary: Path = typer.Option(SUMMARY_PATH, "--summary", help="Committed Stage 5C summary YAML."),
) -> None:
    """Print the committed Stage 5C summary."""

    payload = load_summary(_resolve(summary))
    for key in _SUMMARY_KEYS:
        console.print(f"{key}={_format_value(payload[key])}")


_SUMMARY_KEYS = (
    "build_profile_records",
    "toolchain_detection_records",
    "device_detection_records",
    "smoke_build_records",
    "cuda_toolchain_available",
    "cuda_device_available",
    "local_16gb_profile_detected",
    "local_16gb_profile_required",
    "compatibility_8gb_profile_present",
    "no_gpu_ci_profile_present",
    "smoke_build_attempted",
    "smoke_build_status",
)


def _resolve(path: Path) -> Path:
    return path if path.is_absolute() else repo_root() / path


def _require_file(path: Path) -> None:
    resolved = _resolve(path)
    if not resolved.is_file():
        console.print(f"[red]required file missing: {path}[/red]")
        raise typer.Exit(1)


def _toolchain_available(records: list[dict[str, object]]) -> bool:
    statuses = {record.get("tool_id"): record.get("tool_status") for record in records}
    return statuses.get("cmake") == "detected" and statuses.get("nvcc") == "detected"


def _summary_smoke_status(status: str) -> str:
    if status == "passed":
        return "passed"
    if status == "failed":
        return "failed"
    return "skipped"


def _format_value(value: object) -> str:
    if isinstance(value, bool):
        return str(value).lower()
    return str(value)


def register(root_app: typer.Typer) -> None:
    """Register the Stage 5C CUDA build command group."""

    root_app.add_typer(cuda_build_app, name="cuda-build")
