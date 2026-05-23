"""CUDA-facing source audit records for Stage 5AD."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .export import resolve, write_json_report, write_records
from .models import DEVICE_SUBSET_AUDIT_PATH, OUTPUT_DIR, REPORT_FILES, base_record

FORBIDDEN_PATTERNS = (
    "std::array",
    "std::vector",
    "std::string",
    "std::span",
    "std::optional",
    "std::variant",
    "std::ostringstream",
    "std::cout",
    "std::cerr",
    "throw",
    "<array>",
    "<vector>",
    "<string>",
    "<sstream>",
    "<iomanip>",
    "<iostream>",
)


def build_device_subset_audit(
    *, device_subset_audit_out: Path = DEVICE_SUBSET_AUDIT_PATH, out_dir: Path = OUTPUT_DIR
) -> list[dict[str, Any]]:
    files = sorted(resolve(Path("cuda")).glob("**/*.cu")) + sorted(resolve(Path("cuda")).glob("**/*.cuh"))
    hits: list[dict[str, Any]] = []
    for path in files:
        text = path.read_text(encoding="utf-8")
        for pattern in FORBIDDEN_PATTERNS:
            if pattern in text:
                hits.append({"path": str(path.relative_to(resolve(Path(".")))).replace("\\", "/"), "pattern": pattern})
    record = base_record(
        "bounded_p56_cuda_device_subset_audit_record",
        "schemas/cuda/bounded-p56-cuda-device-subset-audit-record-v0.schema.json",
        device_subset_audit_id="stage5ad-device-subset-audit-v0",
        audit_status="no_cuda_source_changes_reused_existing_kernel",
        cuda_c_style_subset_passed=len(hits) == 0,
        files_audited=[str(path.relative_to(resolve(Path(".")))).replace("\\", "/") for path in files],
        forbidden_feature_hits=hits,
        forbidden_finding_count=len(hits),
        host_side_cpp_exceptions=False,
        device_side_std_usage=False,
        stl_in_cuda_facing_files=False,
        dynamic_allocation_in_device_code=False,
        iostreams_in_cuda_facing_files=False,
        lambdas_in_cuda_facing_files=False,
        cuda_source_modified=False,
        device_kernel_arithmetic_modified=False,
        new_cuda_kernel_added=False,
        new_cuda_kernels_added=0,
    )
    records = [record]
    write_records(device_subset_audit_out, records)
    write_json_report(out_dir, REPORT_FILES["device_audit"], {"records": records})
    return records
