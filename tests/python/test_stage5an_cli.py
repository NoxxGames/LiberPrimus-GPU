from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from libreprimus.paths import repo_root
from test_stage5an_content_pack_builder import write_stage5an_fixture


def test_deep_research_export_cli_builds_and_validates_synthetic_pack(tmp_path: Path) -> None:
    fixture = write_stage5an_fixture(tmp_path)
    pack = tmp_path / "pack"
    hosted = tmp_path / "hosted"
    webroot = tmp_path / "webroot"
    data = tmp_path / "data"
    data.mkdir()
    base = [sys.executable, "-m", "libreprimus.cli", "deep-research-export"]
    subprocess.run(
        [
            *base,
            "build-stage5an-content-pack",
            "--metadata-site-root",
            str(fixture["metadata"]),
            "--website-ingest-dir",
            str(fixture["ingest"]),
            "--research-input-roots",
            str(fixture["research"]),
            "--safe-local-source-roots",
            str(fixture["safe"]),
            "--out-root",
            str(pack),
            "--policy-out",
            str(data / "policy.yaml"),
            "--inputs-out",
            str(data / "inputs.yaml"),
            "--manifest-summary-out",
            str(data / "manifest.yaml"),
            "--file-selection-summary-out",
            str(data / "selection.yaml"),
            "--publication-gate-audit-out",
            str(data / "audit.yaml"),
        ],
        cwd=repo_root(),
        check=True,
        capture_output=True,
        text=True,
    )
    subprocess.run(
        [
            *base,
            "build-stage5an-hosted-export",
            "--content-pack-root",
            str(pack),
            "--metadata-site-root",
            str(fixture["metadata"]),
            "--out-root",
            str(hosted),
            "--summary-out",
            str(data / "hosted.yaml"),
            "--upload-instructions-out",
            str(data / "upload.yaml"),
            "--consumption-guide-out",
            str(data / "guide.yaml"),
        ],
        cwd=repo_root(),
        check=True,
        capture_output=True,
        text=True,
    )
    subprocess.run(
        [
            *base,
            "build-stage5an-combined-webroot",
            "--metadata-site-root",
            str(fixture["metadata"]),
            "--private-content-root",
            str(hosted),
            "--out-root",
            str(webroot),
            "--summary-out",
            str(data / "combined.yaml"),
        ],
        cwd=repo_root(),
        check=True,
        capture_output=True,
        text=True,
    )
    subprocess.run(
        [
            *base,
            "build-stage5an-guardrail",
            "--content-pack-root",
            str(pack),
            "--hosted-export-root",
            str(hosted),
            "--combined-webroot",
            str(webroot),
            "--out",
            str(data / "guardrail.yaml"),
        ],
        cwd=repo_root(),
        check=True,
        capture_output=True,
        text=True,
    )
    subprocess.run(
        [
            *base,
            "build-stage5an-next-stage-decision",
            "--manifest-summary",
            str(data / "manifest.yaml"),
            "--hosted-summary",
            str(data / "hosted.yaml"),
            "--combined-summary",
            str(data / "combined.yaml"),
            "--publication-gate-audit",
            str(data / "audit.yaml"),
            "--out",
            str(data / "decision.yaml"),
        ],
        cwd=repo_root(),
        check=True,
        capture_output=True,
        text=True,
    )
    subprocess.run(
        [
            *base,
            "build-stage5an-summary",
            "--policy",
            str(data / "policy.yaml"),
            "--inputs",
            str(data / "inputs.yaml"),
            "--manifest-summary",
            str(data / "manifest.yaml"),
            "--hosted-summary",
            str(data / "hosted.yaml"),
            "--combined-summary",
            str(data / "combined.yaml"),
            "--file-selection-summary",
            str(data / "selection.yaml"),
            "--publication-gate-audit",
            str(data / "audit.yaml"),
            "--upload-instructions",
            str(data / "upload.yaml"),
            "--consumption-guide",
            str(data / "guide.yaml"),
            "--guardrail",
            str(data / "guardrail.yaml"),
            "--next-stage-decision",
            str(data / "decision.yaml"),
            "--out",
            str(data / "summary.yaml"),
        ],
        cwd=repo_root(),
        check=True,
        capture_output=True,
        text=True,
    )
    completed = subprocess.run(
        [
            *base,
            "validate-stage5an",
            "--content-pack-root",
            str(pack),
            "--hosted-export-root",
            str(hosted),
            "--combined-webroot",
            str(webroot),
            "--policy",
            str(data / "policy.yaml"),
            "--inputs",
            str(data / "inputs.yaml"),
            "--manifest-summary",
            str(data / "manifest.yaml"),
            "--hosted-summary",
            str(data / "hosted.yaml"),
            "--combined-summary",
            str(data / "combined.yaml"),
            "--file-selection-summary",
            str(data / "selection.yaml"),
            "--publication-gate-audit",
            str(data / "audit.yaml"),
            "--upload-instructions",
            str(data / "upload.yaml"),
            "--consumption-guide",
            str(data / "guide.yaml"),
            "--guardrail",
            str(data / "guardrail.yaml"),
            "--next-stage-decision",
            str(data / "decision.yaml"),
            "--summary",
            str(data / "summary.yaml"),
        ],
        cwd=repo_root(),
        check=True,
        capture_output=True,
        text=True,
    )
    assert "deep_research_export_stage5an_valid=true" in completed.stdout
