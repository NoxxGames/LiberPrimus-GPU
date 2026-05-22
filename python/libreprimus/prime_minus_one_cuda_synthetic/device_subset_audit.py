"""Device-code subset audit for the Stage 5AA CUDA files."""

from __future__ import annotations

from pathlib import Path

from libreprimus.prime_minus_one_cuda_synthetic.export import resolve, write_json_report, write_records
from libreprimus.prime_minus_one_cuda_synthetic.models import (
    CUDA_HEADER,
    CUDA_SOURCE,
    DEVICE_SUBSET_AUDIT_PATH,
    OUTPUT_DIR,
    REPORT_FILES,
    base_record,
)

FORBIDDEN_PATTERNS = (
    "std::",
    "#include <vector>",
    "#include <string>",
    "#include <array>",
    "throw ",
    "try {",
    "catch ",
    "new ",
    "delete ",
    "std::vector",
    "std::string",
    "std::array",
)


def build_device_subset_audit(
    *,
    device_subset_audit_out: Path = DEVICE_SUBSET_AUDIT_PATH,
    out_dir: Path = OUTPUT_DIR,
) -> list[dict[str, object]]:
    findings = []
    scanned_files = [CUDA_HEADER, CUDA_SOURCE]
    for path in scanned_files:
        text = resolve(path).read_text(encoding="utf-8")
        for pattern in FORBIDDEN_PATTERNS:
            if pattern in text:
                findings.append({"path": str(path), "pattern": pattern})
    record = base_record(
        "prime_minus_one_cuda_device_subset_audit_record",
        "schemas/cuda/prime-minus-one-cuda-device-subset-audit-record-v0.schema.json",
        audit_record_id="stage5aa-prime-minus-one-cuda-device-subset-audit-v0",
        scanned_files=[str(path) for path in scanned_files],
        forbidden_patterns=list(FORBIDDEN_PATTERNS),
        forbidden_finding_count=len(findings),
        findings=findings,
        cuda_c_style_subset_status="passed" if not findings else "failed",
        blockers=[] if not findings else ["forbidden_cuda_device_subset_pattern_found"],
    )
    records = [record]
    write_records(device_subset_audit_out, records)
    write_json_report(out_dir, REPORT_FILES["device_audit"], {"records": records})
    return records
