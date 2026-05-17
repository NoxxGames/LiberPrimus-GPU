"""Stage 3M deterministic image-analysis consistency checks."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

from libreprimus.consistency.models import ConsistencyCheckResult, fail_result, pass_result
from libreprimus.image_analysis.validation import validate_results
from libreprimus.paths import repo_root

GROUP = "image_analysis"
RESULTS_DIR = repo_root() / "experiments/results/image-analysis/stage3m"
SCHEMA_PATHS = [
    repo_root() / "schemas/visual/image-analysis-record-v0.schema.json",
    repo_root() / "schemas/visual/image-threshold-summary-v0.schema.json",
    repo_root() / "schemas/visual/image-symmetry-record-v0.schema.json",
    repo_root() / "schemas/visual/image-bitplane-summary-v0.schema.json",
    repo_root() / "schemas/visual/image-component-summary-v0.schema.json",
    repo_root() / "schemas/visual/visual-feature-candidate-v0.schema.json",
    repo_root() / "schemas/visual/image-analysis-run-summary-v0.schema.json",
]


def check_image_analysis_consistency(root: Path = repo_root()) -> list[ConsistencyCheckResult]:
    results: list[ConsistencyCheckResult] = []
    for schema_path in SCHEMA_PATHS:
        try:
            payload = json.loads(schema_path.read_text(encoding="utf-8"))
        except Exception as exc:  # noqa: BLE001 - consistency reports collect validation failures.
            results.append(fail_result(GROUP, "schema_parse", str(exc), path=schema_path))
            continue
        if _schema_flag_const(payload, "trusted_as_canonical", False) and _schema_flag_const(payload, "solve_claim", False):
            results.append(pass_result(GROUP, "schema_flags", "Stage 3M schema requires false safety flags.", path=schema_path))
        else:
            results.append(fail_result(GROUP, "schema_flags", "Schema safety flags are not constrained to false.", path=schema_path))

    feature_schema = json.loads((root / "schemas/visual/visual-feature-candidate-v0.schema.json").read_text(encoding="utf-8"))
    if _schema_flag_const(feature_schema, "usable_as_experiment_seed", False):
        results.append(
            pass_result(
                GROUP,
                "feature_seed_flag",
                "Visual feature candidates cannot be experiment seeds by schema.",
                path="schemas/visual/visual-feature-candidate-v0.schema.json",
            )
        )
    else:
        results.append(
            fail_result(
                GROUP,
                "feature_seed_flag",
                "Visual feature candidate schema permits seed promotion.",
                path="schemas/visual/visual-feature-candidate-v0.schema.json",
            )
        )

    counts, errors = validate_results(RESULTS_DIR, allow_missing=True)
    if errors:
        for error in errors:
            results.append(fail_result(GROUP, "generated_results_valid", error, path=RESULTS_DIR))
    else:
        results.append(
            pass_result(
                GROUP,
                "generated_results_valid",
                f"Generated image-analysis records validate or are absent for raw-data-free CI: {counts}.",
                path=RESULTS_DIR,
            )
        )

    ignored_expectations = [
        "experiments/results/image-analysis/stage3m/image_analysis_records.jsonl",
        "experiments/results/image-analysis/stage3m/visual_feature_candidates.jsonl",
        "experiments/results/image-analysis/stage3m/summary.json",
        "third_party/LiberPrimusPages/example.jpg",
        "third_party/LiberPrimusPages/example.jpeg",
        "third_party/LiberPrimusPages/example.png",
    ]
    for path in ignored_expectations:
        if _is_ignored(root, path):
            results.append(pass_result(GROUP, "stage3m_path_ignored", f"Ignored path is ignored: {path}", path=path))
        else:
            results.append(fail_result(GROUP, "stage3m_path_ignored", f"Expected ignored path is trackable: {path}", path=path))
    return results


def _schema_flag_const(payload: dict, field: str, expected: bool) -> bool:
    properties = payload.get("properties", {})
    if not isinstance(properties, dict):
        return False
    definition = properties.get(field, {})
    return isinstance(definition, dict) and definition.get("const") is expected


def _is_ignored(root: Path, path: str) -> bool:
    result = subprocess.run(
        ["git", "check-ignore", "-q", "--", path],
        cwd=root,
        check=False,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return result.returncode == 0
