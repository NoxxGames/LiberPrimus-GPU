"""Stage 3V OutGuess regression consistency checks."""

from __future__ import annotations

import subprocess
from pathlib import Path

from libreprimus.consistency.models import ConsistencyCheckResult, fail_result, pass_result
from libreprimus.paths import repo_root
from libreprimus.stego.outguess_manifest import validate_manifest_and_artifacts

GROUP = "stego"
MANIFEST = repo_root() / "experiments/manifests/stego/outguess-regression-v1.yaml"
ARTIFACTS = repo_root() / "data/observations/stego/outguess-artifacts-v0.yaml"


def check_stego_consistency(root: Path = repo_root()) -> list[ConsistencyCheckResult]:
    """Run raw-data-free stego/OutGuess checks."""
    results: list[ConsistencyCheckResult] = []
    summary, errors = validate_manifest_and_artifacts(MANIFEST, ARTIFACTS)
    if errors:
        for error in errors:
            results.append(fail_result(GROUP, "outguess_manifest_valid", error))
    else:
        results.append(
            pass_result(
                GROUP,
                "outguess_manifest_valid",
                f"OutGuess manifest validates with {summary.get('case_count')} cases.",
            )
        )
    for path in [
        "experiments/results/stego/outguess/stage3v/summary.json",
        "experiments/results/stego/outguess/stage3v/extraction_records.jsonl",
        "experiments/results/stego/outguess/stage3v/outguess_tool_record.json",
        "experiments/results/stego/outguess/stage3v/extracted_payloads/example.txt",
        "experiments/results/stego/outguess/stage3v/synthetic_inputs/example.jpg",
        "third_party/CicadaArchive/example.jpg",
        "third_party/CicadaOutGuess/example.jpg",
        "third_party/LiberPrimusDiscordChats/example.html",
        "third_party/LiberPrimusPages/example.jpg",
    ]:
        if _is_ignored(root, path):
            results.append(pass_result(GROUP, "stego_path_ignored", f"Ignored path is ignored: {path}", path=path))
        else:
            results.append(fail_result(GROUP, "stego_path_ignored", f"Expected ignored path is trackable: {path}", path=path))
    for path in [
        "schemas/stego/stego-artifact-record-v0.schema.json",
        "schemas/stego/outguess-regression-manifest-v0.schema.json",
        "schemas/stego/outguess-extraction-record-v0.schema.json",
        "schemas/stego/outguess-regression-summary-v0.schema.json",
        "schemas/stego/outguess-tool-record-v0.schema.json",
        "data/observations/stego/outguess-artifacts-v0.yaml",
        "data/locks/third-party/outguess-regression/outguess-regression-source-locks-v0.yaml",
        "experiments/manifests/stego/outguess-regression-v1.yaml",
    ]:
        if _is_ignored(root, path):
            results.append(fail_result(GROUP, "stego_metadata_trackable", f"Expected committed path is ignored: {path}", path=path))
        else:
            results.append(pass_result(GROUP, "stego_metadata_trackable", f"Committed path is trackable: {path}", path=path))
    return results


def _is_ignored(root: Path, path: str) -> bool:
    result = subprocess.run(
        ["git", "check-ignore", "-q", "--", path],
        cwd=root,
        check=False,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return result.returncode == 0
