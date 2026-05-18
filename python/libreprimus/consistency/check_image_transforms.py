"""Stage 3P deterministic image-transform consistency checks."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

from libreprimus.consistency.models import ConsistencyCheckResult, fail_result, pass_result
from libreprimus.image_transforms.validation import validate_results
from libreprimus.paths import repo_root

GROUP = "image_transforms"
RESULTS_DIR = repo_root() / "experiments/results/image-transforms/stage3p"
SCHEMA_PATHS = [
    repo_root() / "schemas/visual/image-transform-record-v0.schema.json",
    repo_root() / "schemas/visual/image-transform-metric-record-v0.schema.json",
    repo_root() / "schemas/visual/visual-transform-candidate-v0.schema.json",
    repo_root() / "schemas/visual/contact-sheet-record-v0.schema.json",
    repo_root() / "schemas/visual/image-transform-run-summary-v0.schema.json",
]


def check_image_transform_consistency(root: Path = repo_root()) -> list[ConsistencyCheckResult]:
    """Return Stage 3P consistency checks that do not require raw local images."""
    results: list[ConsistencyCheckResult] = []
    for schema_path in SCHEMA_PATHS:
        try:
            payload = json.loads(schema_path.read_text(encoding="utf-8"))
        except Exception as exc:  # noqa: BLE001 - consistency reports collect validation failures.
            results.append(fail_result(GROUP, "schema_parse", str(exc), path=schema_path))
            continue
        if _schema_flag_const(payload, "trusted_as_canonical", False) and _schema_flag_const(payload, "solve_claim", False):
            results.append(
                pass_result(GROUP, "schema_flags", "Stage 3P schema requires false safety flags.", path=schema_path)
            )
        else:
            results.append(
                fail_result(GROUP, "schema_flags", "Schema safety flags are not constrained to false.", path=schema_path)
            )

    candidate_schema = json.loads((root / "schemas/visual/visual-transform-candidate-v0.schema.json").read_text(encoding="utf-8"))
    if _schema_flag_const(candidate_schema, "usable_as_experiment_seed", False):
        results.append(
            pass_result(
                GROUP,
                "candidate_seed_flag",
                "Visual transform candidates cannot be experiment seeds by schema.",
                path="schemas/visual/visual-transform-candidate-v0.schema.json",
            )
        )
    else:
        results.append(
            fail_result(
                GROUP,
                "candidate_seed_flag",
                "Visual transform candidate schema permits seed promotion.",
                path="schemas/visual/visual-transform-candidate-v0.schema.json",
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
                f"Generated image-transform records validate or are absent for raw-data-free CI: {counts}.",
                path=RESULTS_DIR,
            )
        )

    ignored_expectations = [
        "experiments/results/image-transforms/stage3p/review_index.html",
        "experiments/results/image-transforms/stage3p/transform_records.jsonl",
        "experiments/results/image-transforms/stage3p/visual_transform_candidates.jsonl",
        "experiments/results/image-transforms/stage3p/contact_sheets/example.jpg",
        "experiments/results/image-transforms/stage3p/derived_images/example/example.png",
        "third_party/LiberPrimusPages/example.jpg",
        "third_party/LiberPrimusPages/example.jpeg",
        "third_party/LiberPrimusPages/example.png",
        "third_party/LiberPrimusDiscordChats/example.html",
    ]
    for path in ignored_expectations:
        if _is_ignored(root, path):
            results.append(pass_result(GROUP, "stage3p_path_ignored", f"Ignored path is ignored: {path}", path=path))
        else:
            results.append(fail_result(GROUP, "stage3p_path_ignored", f"Expected ignored path is trackable: {path}", path=path))
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
