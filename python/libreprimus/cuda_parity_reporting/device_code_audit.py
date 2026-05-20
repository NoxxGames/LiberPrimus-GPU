"""CUDA device-code subset audit for Stage 5G."""

from __future__ import annotations

from pathlib import Path
import re
from typing import Any

from libreprimus.cuda_parity_reporting.export import write_record_set, write_report
from libreprimus.cuda_parity_reporting.models import (
    BANNED_CUDA_TOKENS,
    COMMON_POLICY_FLAGS,
    CUDA_SOURCE_PATHS,
    DEVICE_AUDIT_JSON,
    DEVICE_AUDIT_PATH,
    OUTPUT_DIR,
    STAGE_ID,
)
from libreprimus.paths import repo_root


LAMBDA_RE = re.compile(r"\[[^\]]*]\s*\(")
NEW_DELETE_RE = re.compile(r"\b(new|delete)\b")


def build_device_code_subset_audit(
    *,
    device_code_audit_out: Path = DEVICE_AUDIT_PATH,
    out_dir: Path = OUTPUT_DIR,
    source_paths: tuple[Path, ...] = CUDA_SOURCE_PATHS,
) -> list[dict[str, Any]]:
    findings = _scan_sources(source_paths)
    stl_findings = [
        item
        for item in findings
        if item["token"] in BANNED_CUDA_TOKENS and item["token"] not in {"throw"}
    ]
    std_array_findings = [item for item in findings if item["token"] in {"<array>", "std::array"}]
    exception_findings = [item for item in findings if item["token"] == "throw"]
    dynamic_findings = [item for item in findings if item["token"] in {"new", "delete"}]
    record: dict[str, Any] = {
        "record_type": "cuda_device_code_subset_audit_record",
        "stage_id": STAGE_ID,
        "audit_id": "stage5g-cuda-device-code-subset-audit",
        "source_paths": [str(path) for path in source_paths],
        "files_scanned": len(source_paths),
        "banned_token_findings": findings,
        "banned_token_finding_count": len(findings),
        "device_code_subset_compliant": not findings,
        "stl_used_in_cuda_device_path": bool(stl_findings),
        "std_array_used_in_cuda_device_path": bool(std_array_findings),
        "std_vector_used_in_cuda_device_path": any(item["token"] in {"<vector>", "std::vector"} for item in findings),
        "std_string_used_in_cuda_device_path": any(item["token"] in {"<string>", "std::string"} for item in findings),
        "cxx_exceptions_in_cuda_device_path": bool(exception_findings),
        "dynamic_allocation_in_device_code": bool(dynamic_findings),
        "cuda_source_modified": True,
        "new_cuda_kernels_added": 0,
        "policy": "conservative_cuda_c_subset",
        "notes": [
            "CUDA-facing .cu/.cuh files are scanned for STL/convenience C++ tokens and exceptions.",
            "Host-side test .cpp files are outside this device-code subset audit.",
        ],
        **COMMON_POLICY_FLAGS,
    }
    records = [record]
    write_record_set(device_code_audit_out, records)
    write_report(out_dir, DEVICE_AUDIT_JSON, {"records": records})
    return records


def _scan_sources(source_paths: tuple[Path, ...]) -> list[dict[str, Any]]:
    root = repo_root()
    findings: list[dict[str, Any]] = []
    for relative_path in source_paths:
        path = root / relative_path
        text = path.read_text(encoding="utf-8")
        for line_number, line in enumerate(text.splitlines(), start=1):
            for token in BANNED_CUDA_TOKENS:
                if token in line:
                    findings.append({"path": str(relative_path), "line": line_number, "token": token})
            if LAMBDA_RE.search(line):
                findings.append({"path": str(relative_path), "line": line_number, "token": "lambda"})
            if NEW_DELETE_RE.search(line):
                findings.append({"path": str(relative_path), "line": line_number, "token": NEW_DELETE_RE.search(line).group(1)})
    return findings
