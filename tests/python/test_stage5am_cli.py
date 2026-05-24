from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from libreprimus.paths import repo_root


def test_website_render_cli_build_and_validate_site(tmp_path: Path) -> None:
    site_root = tmp_path / "research-index"
    results_dir = tmp_path / "results"
    policy = tmp_path / "policy.yaml"
    inputs = tmp_path / "inputs.yaml"
    manifest = tmp_path / "manifest.yaml"
    audit = tmp_path / "audit.yaml"
    upload = tmp_path / "upload.yaml"
    validation = tmp_path / "validation.yaml"
    build = [
        sys.executable,
        "-m",
        "libreprimus.cli",
        "website-render",
        "build-stage5am-site",
        "--website-ingest-dir",
        "data/website-ingest/stage5al",
        "--stage5al-summary",
        "data/source-harvester/stage5al-summary.yaml",
        "--out-root",
        str(site_root),
        "--results-dir",
        str(results_dir),
        "--render-policy-out",
        str(policy),
        "--render-inputs-out",
        str(inputs),
        "--manifest-out",
        str(manifest),
        "--privacy-audit-out",
        str(audit),
        "--upload-instructions-out",
        str(upload),
    ]
    completed = subprocess.run(build, cwd=repo_root(), check=True, capture_output=True, text=True)
    assert "website_export_generated=true" in completed.stdout
    validate = [
        sys.executable,
        "-m",
        "libreprimus.cli",
        "website-render",
        "validate-stage5am-site",
        "--site-root",
        str(site_root),
        "--manifest",
        str(manifest),
        "--privacy-audit",
        str(audit),
        "--results-dir",
        str(results_dir),
        "--out",
        str(validation),
    ]
    completed = subprocess.run(validate, cwd=repo_root(), check=True, capture_output=True, text=True)
    assert "static_site_validation_passed=true" in completed.stdout


def test_website_render_cli_full_validate_committed_records() -> None:
    command = [
        sys.executable,
        "-m",
        "libreprimus.cli",
        "website-render",
        "validate-stage5am",
        "--render-policy",
        "data/website-render/stage5am-render-policy.yaml",
        "--render-inputs",
        "data/website-render/stage5am-render-inputs.yaml",
        "--manifest",
        "data/website-render/stage5am-render-output-manifest.yaml",
        "--validation",
        "data/website-render/stage5am-static-site-validation.yaml",
        "--privacy-audit",
        "data/website-render/stage5am-privacy-publication-audit.yaml",
        "--upload-instructions",
        "data/website-render/stage5am-upload-instructions.yaml",
        "--guardrail",
        "data/website-render/stage5am-guardrail.yaml",
        "--next-stage-decision",
        "data/website-render/stage5am-next-stage-decision.yaml",
        "--summary",
        "data/website-render/stage5am-summary.yaml",
        "--site-root",
        "website-export/stage5am/research-index",
        "--results-dir",
        "experiments/results/website-render/stage5am",
    ]
    completed = subprocess.run(command, cwd=repo_root(), check=True, capture_output=True, text=True)
    assert "website_render_stage5am_valid=true" in completed.stdout
