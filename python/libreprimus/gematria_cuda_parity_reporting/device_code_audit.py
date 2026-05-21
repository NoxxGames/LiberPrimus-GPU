"""CUDA-facing device-code audit for Stage 5K."""

from __future__ import annotations

from pathlib import Path
import re
from typing import Any

from libreprimus.gematria_cuda_parity_reporting.export import write_record_set, write_report
from libreprimus.gematria_cuda_parity_reporting.models import (
    BANNED_CUDA_TOKENS,
    COMMON_POLICY_FLAGS,
    CUDA_SOURCE_PATHS,
    DEVICE_AUDIT_JSON,
    DEVICE_AUDIT_PATH,
    OUTPUT_DIR,
)
from libreprimus.paths import repo_root

LAMBDA_RE = re.compile(r"\[[^\]]*]\s*\(")
NEW_DELETE_RE = re.compile(r"\b(new|delete)\b")


def build_device_code_audit(
    *,
    device_code_audit_out: Path = DEVICE_AUDIT_PATH,
    out_dir: Path = OUTPUT_DIR,
    source_paths: tuple[Path, ...] = CUDA_SOURCE_PATHS,
) -> list[dict[str, Any]]:
    findings = scan_sources(source_paths)
    stl_findings = [
        finding
        for finding in findings
        if finding["token"] in BANNED_CUDA_TOKENS and finding["token"] != "throw"
    ]
    dynamic_findings = [finding for finding in findings if finding["token"] in {"new", "delete"}]
    record: dict[str, Any] = {
        "record_type": "gematria_cuda_device_code_audit_record",
        "audit_id": "stage5k-gematria-cuda-device-code-audit",
        "source_paths": [_path_text(path) for path in source_paths],
        "files_scanned": len(source_paths),
        "banned_token_findings": findings,
        "banned_token_finding_count": len(findings),
        "device_code_subset_compliant": not findings,
        "stl_used_in_cuda_device_path": bool(stl_findings),
        "std_array_used_in_cuda_device_path": any(
            finding["token"] in {"<array>", "std::array"} for finding in findings
        ),
        "std_vector_used_in_cuda_device_path": any(
            finding["token"] in {"<vector>", "std::vector"} for finding in findings
        ),
        "std_string_used_in_cuda_device_path": any(
            finding["token"] in {"<string>", "std::string"} for finding in findings
        ),
        "cxx_exceptions_in_cuda_device_path": any(finding["token"] == "throw" for finding in findings),
        "throw_used_in_cuda_device_path": any(finding["token"] == "throw" for finding in findings),
        "dynamic_allocation_in_device_code": bool(dynamic_findings),
        "lambdas_in_cuda_device_path": any(finding["token"] == "lambda" for finding in findings),
        "cxx_ownership_types_cross_kernel_boundary": any(
            finding["token"] in {"std::unique_ptr", "std::shared_ptr", "std::make_unique", "std::make_shared"}
            for finding in findings
        ),
        "policy": "conservative_cuda_c_subset",
        "notes": [
            "Stage 5K scans CUDA-facing .cu/.cuh files and does not modify CUDA source.",
            "cudaMalloc/cudaFree host-side runtime calls are not treated as C++ dynamic allocation in device code.",
        ],
        **COMMON_POLICY_FLAGS,
    }
    records = [record]
    write_record_set(device_code_audit_out, records)
    write_report(out_dir, DEVICE_AUDIT_JSON, {"records": records})
    return records


def scan_sources(source_paths: tuple[Path, ...]) -> list[dict[str, Any]]:
    root = repo_root()
    findings: list[dict[str, Any]] = []
    for relative_path in source_paths:
        path = root / relative_path
        text = path.read_text(encoding="utf-8")
        for line_number, line in enumerate(text.splitlines(), start=1):
            for token in BANNED_CUDA_TOKENS:
                if token in line:
                    findings.append({"path": _path_text(relative_path), "line": line_number, "token": token})
            lambda_match = LAMBDA_RE.search(line)
            if lambda_match:
                findings.append({"path": _path_text(relative_path), "line": line_number, "token": "lambda"})
            dynamic_match = NEW_DELETE_RE.search(line)
            if dynamic_match:
                findings.append({"path": _path_text(relative_path), "line": line_number, "token": dynamic_match.group(1)})
    return findings


def _path_text(path: Path) -> str:
    return str(path).replace("\\", "/")
