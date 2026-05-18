"""Stage 3V OutGuess regression runner."""

from __future__ import annotations

import hashlib
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from libreprimus.stego.models import OutGuessCase, OutGuessManifest, OutGuessTool, StegoArtifact
from libreprimus.stego.outguess_export import resolve_path, write_json, write_jsonl
from libreprimus.stego.outguess_manifest import load_artifacts, load_manifest
from libreprimus.stego.outguess_tool import detect_outguess, run_outguess_extract, tool_record
from libreprimus.stego.synthetic_images import write_synthetic_image

DEFAULT_MANIFEST = Path("experiments/manifests/stego/outguess-regression-v1.yaml")
DEFAULT_ARTIFACTS = Path("data/observations/stego/outguess-artifacts-v0.yaml")
DEFAULT_OUTPUT_DIR = Path("experiments/results/stego/outguess/stage3v")


def run_outguess_regression(
    *,
    manifest_path: Path = DEFAULT_MANIFEST,
    artifacts_path: Path = DEFAULT_ARTIFACTS,
    out_dir: Path = DEFAULT_OUTPUT_DIR,
    outguess_path: Path | None = None,
    allow_missing_tool: bool = False,
    allow_missing_assets: bool = False,
    allow_warnings: bool = False,
) -> dict[str, Any]:
    """Run explicit OutGuess regression cases."""
    manifest = load_manifest(manifest_path)
    artifacts = load_artifacts(artifacts_path)
    tool = detect_outguess(outguess_path)
    if not tool.available and not (allow_missing_tool or manifest.allow_missing_tool):
        raise ValueError("outguess tool missing")
    resolved_out = resolve_path(out_dir)
    run_id = f"stage3v-outguess-regression-{datetime.now(UTC).strftime('%Y%m%dT%H%M%SZ')}"
    warnings: list[str] = []
    records: list[dict[str, Any]] = []
    payload_dir = resolved_out / "extracted_payloads"
    synthetic_dir = resolved_out / "synthetic_inputs"
    for case in manifest.cases:
        artifact = artifacts.get(case.artifact_id)
        if artifact is None:
            warnings.append(f"{case.case_id}:missing_artifact_record")
            continue
        records.append(
            _run_case(
                run_id=run_id,
                case=case,
                artifact=artifact,
                manifest=manifest,
                tool=tool,
                payload_dir=payload_dir,
                synthetic_dir=synthetic_dir,
                allow_missing_tool=allow_missing_tool or manifest.allow_missing_tool,
                allow_missing_assets=allow_missing_assets or manifest.allow_missing_assets,
            )
        )
    if warnings and not allow_warnings:
        raise ValueError("; ".join(warnings))
    summary = _summary(
        run_id=run_id,
        manifest_path=manifest_path,
        tool=tool,
        case_count=len(manifest.cases),
        records=records,
        warnings=warnings,
        out_dir=resolved_out,
    )
    write_json(resolved_out / "outguess_tool_record.json", tool_record(tool))
    write_jsonl(resolved_out / "extraction_records.jsonl", records)
    write_json(resolved_out / "summary.json", summary)
    if warnings:
        write_jsonl(
            resolved_out / "warnings.jsonl",
            [{"record_type": "outguess_warning", "run_id": run_id, "warning": warning} for warning in warnings],
        )
    return summary


def _run_case(
    *,
    run_id: str,
    case: OutGuessCase,
    artifact: StegoArtifact,
    manifest: OutGuessManifest,
    tool: OutGuessTool,
    payload_dir: Path,
    synthetic_dir: Path,
    allow_missing_tool: bool,
    allow_missing_assets: bool,
) -> dict[str, Any]:
    output_path = payload_dir / f"{case.case_id}.payload"
    input_path = resolve_path(artifact.local_path)
    if case.generate_synthetic:
        input_path = synthetic_dir / f"{artifact.artifact_id}.jpg"
        write_synthetic_image(case.generate_synthetic, input_path)
    if not case.enabled:
        return _record(run_id, case, artifact, tool, input_path.is_file(), False, None, None, None, "skipped_case_disabled", {})
    if not tool.available:
        if not allow_missing_tool:
            raise ValueError("outguess tool missing")
        return _record(run_id, case, artifact, tool, input_path.is_file(), False, None, None, None, "skipped_tool_missing", {})
    if not input_path.is_file():
        if not allow_missing_assets:
            raise ValueError(f"asset missing: {artifact.artifact_id}")
        return _record(run_id, case, artifact, tool, False, False, None, None, None, "skipped_asset_missing", {})
    result = run_outguess_extract(tool, input_path, output_path)
    output_paths = {
        "payload": str(output_path),
        "stdout_sha256": hashlib.sha256((result.stdout or "").encode()).hexdigest(),
        "stderr_sha256": hashlib.sha256((result.stderr or "").encode()).hexdigest(),
    }
    if result.returncode != 0:
        return _record(
            run_id,
            case,
            artifact,
            tool,
            True,
            True,
            result.returncode,
            None,
            None,
            "extraction_error",
            output_paths,
        )
    if not output_path.is_file() or output_path.stat().st_size == 0:
        return _record(run_id, case, artifact, tool, True, True, result.returncode, None, 0, "no_payload", output_paths)
    payload = output_path.read_bytes()
    payload_sha = hashlib.sha256(payload).hexdigest()
    payload_size = len(payload)
    if artifact.expected_payload_sha256:
        status = "passed" if payload_sha == artifact.expected_payload_sha256 else "failed"
    elif case.expected_role in {"synthetic_negative", "known_negative"}:
        status = "unexpected_payload"
    else:
        status = "reference_extraction_recorded"
    return _record(run_id, case, artifact, tool, True, True, result.returncode, payload_sha, payload_size, status, output_paths)


def _record(
    run_id: str,
    case: OutGuessCase,
    artifact: StegoArtifact,
    tool: OutGuessTool,
    asset_available: bool,
    attempted: bool,
    exit_code: int | None,
    payload_sha: str | None,
    payload_size: int | None,
    status: str,
    output_paths: dict[str, Any],
) -> dict[str, Any]:
    expected = artifact.expected_payload_sha256
    return {
        "record_type": "outguess_extraction_record",
        "run_id": run_id,
        "case_id": case.case_id,
        "artifact_id": artifact.artifact_id,
        "expected_role": case.expected_role,
        "tool_available": tool.available,
        "asset_available": asset_available,
        "extraction_attempted": attempted,
        "extraction_exit_code": exit_code,
        "extracted_payload_sha256": payload_sha,
        "extracted_payload_size_bytes": payload_size,
        "expected_payload_sha256": expected,
        "payload_match": payload_sha == expected if expected and payload_sha else None,
        "status": status,
        "output_paths": output_paths,
        "raw_payload_committed": False,
        "solve_claim": False,
        "cuda_used": False,
        "notes": case.notes,
    }


def _summary(
    *,
    run_id: str,
    manifest_path: Path,
    tool: OutGuessTool,
    case_count: int,
    records: list[dict[str, Any]],
    warnings: list[str],
    out_dir: Path,
) -> dict[str, Any]:
    def count(status: str) -> int:
        return sum(1 for record in records if record["status"] == status)

    attempted = sum(1 for record in records if record["extraction_attempted"])
    passed = count("passed")
    failed = count("failed")
    skipped_tool = count("skipped_tool_missing")
    skipped_asset = count("skipped_asset_missing")
    extraction_errors = count("extraction_error")
    unexpected = count("unexpected_payload")
    reference = count("reference_extraction_recorded")
    return {
        "record_type": "outguess_regression_summary",
        "run_id": run_id,
        "generated_at_utc": datetime.now(UTC).isoformat().replace("+00:00", "Z"),
        "manifest_path": str(resolve_path(manifest_path)),
        "tool_available": tool.available,
        "tool_path": str(tool.path) if tool.path is not None else None,
        "case_count": case_count,
        "attempted_count": attempted,
        "passed_count": passed,
        "failed_count": failed,
        "skipped_tool_missing_count": skipped_tool,
        "skipped_asset_missing_count": skipped_asset,
        "skipped_case_disabled_count": count("skipped_case_disabled"),
        "extraction_error_count": extraction_errors,
        "unexpected_payload_count": unexpected,
        "no_payload_count": count("no_payload"),
        "reference_extraction_recorded_count": reference,
        "output_paths": {
            "tool_record": str(out_dir / "outguess_tool_record.json"),
            "extraction_records": str(out_dir / "extraction_records.jsonl"),
            "summary": str(out_dir / "summary.json"),
            "extracted_payloads": str(out_dir / "extracted_payloads"),
            "synthetic_inputs": str(out_dir / "synthetic_inputs"),
        },
        "warnings": warnings,
        "raw_payloads_committed": False,
        "solve_claim": False,
        "cuda_used": False,
        "notes": "OutGuess regression harness records availability and exact payload hashes only.",
    }
