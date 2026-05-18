"""Load Stage 3O/3Q inputs for Stage 3R promotion."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.discord_lead_promotion.export import read_json, read_jsonl, read_yaml
from libreprimus.paths import repo_root


def load_stage3r_inputs(
    *,
    review_dir: Path,
    stage3o_links: Path,
    stage3o_methods: Path,
    stage3o_numerics: Path,
    source_registry: Path,
    visual_registry: Path,
    cookie_records: Path,
    allow_missing: bool = False,
) -> tuple[dict[str, Any], list[str]]:
    """Load available generated and committed lead inputs without requiring raw logs."""
    warnings: list[str] = []
    resolved_review = _resolve(review_dir)
    summary = _read_json_if_present(resolved_review / "review_bundle_summary.json", warnings, allow_missing)
    data = {
        "review_summary": summary,
        "source_links": _read_jsonl_if_present(resolved_review / "source_links_index.jsonl", warnings, allow_missing),
        "method_claims": _read_jsonl_if_present(resolved_review / "method_claims_index.jsonl", warnings, allow_missing),
        "numeric_observations": _read_jsonl_if_present(
            resolved_review / "numeric_observations_index.jsonl",
            warnings,
            allow_missing,
        ),
        "visual_observations": _read_jsonl_if_present(
            resolved_review / "visual_observations_index.jsonl",
            warnings,
            allow_missing,
        ),
        "debunks": _read_jsonl_if_present(
            resolved_review / "debunks_and_false_positives_index.jsonl",
            warnings,
            allow_missing,
        ),
        "stage3o_links": _read_yaml_records(_resolve(stage3o_links), warnings, allow_missing),
        "stage3o_methods": _read_yaml_records(_resolve(stage3o_methods), warnings, allow_missing),
        "stage3o_numerics": _read_yaml_records(_resolve(stage3o_numerics), warnings, allow_missing),
        "source_registry": _read_yaml_if_present(_resolve(source_registry), warnings, allow_missing),
        "visual_registry": _read_yaml_if_present(_resolve(visual_registry), warnings, allow_missing),
        "cookie_records": _read_yaml_if_present(_resolve(cookie_records), warnings, allow_missing),
    }
    return data, warnings


def _read_json_if_present(path: Path, warnings: list[str], allow_missing: bool) -> dict[str, Any]:
    if path.is_file():
        return read_json(path)
    if not allow_missing:
        raise FileNotFoundError(path)
    warnings.append(f"missing_json:{_display(path)}")
    return {}


def _read_jsonl_if_present(path: Path, warnings: list[str], allow_missing: bool) -> list[dict[str, Any]]:
    if path.is_file():
        return read_jsonl(path)
    if not allow_missing:
        raise FileNotFoundError(path)
    warnings.append(f"missing_jsonl:{_display(path)}")
    return []


def _read_yaml_records(path: Path, warnings: list[str], allow_missing: bool) -> list[dict[str, Any]]:
    if not path.is_file():
        if not allow_missing:
            raise FileNotFoundError(path)
        warnings.append(f"missing_yaml:{_display(path)}")
        return []
    payload = read_yaml(path)
    records = payload.get("records", [])
    return records if isinstance(records, list) else []


def _read_yaml_if_present(path: Path, warnings: list[str], allow_missing: bool) -> dict[str, Any]:
    if path.is_file():
        return read_yaml(path)
    if not allow_missing:
        raise FileNotFoundError(path)
    warnings.append(f"missing_yaml:{_display(path)}")
    return {}


def _resolve(path: Path) -> Path:
    return path if path.is_absolute() else repo_root() / path


def _display(path: Path) -> str:
    try:
        return path.resolve().relative_to(repo_root()).as_posix()
    except ValueError:
        return path.as_posix()
