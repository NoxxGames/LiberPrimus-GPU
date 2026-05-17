"""Validation helpers for bounded hash-preimage inputs and outputs."""

from __future__ import annotations

import json
from pathlib import Path

from libreprimus.hash_preimage.candidate_packs import validate_pack_dir
from libreprimus.hash_preimage.models import CookieTarget
from libreprimus.history.source_records import resolve_repo_path
from libreprimus.visual_observations.validation import load_records


def load_cookie_targets(path: Path) -> list[CookieTarget]:
    records = load_records(path)
    targets: list[CookieTarget] = []
    errors: list[str] = []
    for record in records:
        cookie_id = str(record.get("cookie_id", ""))
        value = str(record.get("cookie_value", ""))
        if record.get("record_type") != "cookie_hash_record":
            errors.append(f"{cookie_id}: invalid record_type")
        if len(value) != 64 or any(ch not in "0123456789abcdefABCDEF" for ch in value):
            errors.append(f"{cookie_id}: cookie value must be hex64")
        if record.get("preimage_status") not in {"unknown", "not_attempted", "rejected"}:
            errors.append(f"{cookie_id}: cookie record must not claim preimage")
        targets.append(
            CookieTarget(
                cookie_id=cookie_id,
                cookie_name=str(record.get("cookie_name", "")),
                cookie_value=value.lower(),
            )
        )
    if errors:
        raise ValueError("; ".join(errors))
    return targets


def validate_candidate_packs(pack_dir: Path) -> tuple[int, list[str]]:
    return validate_pack_dir(pack_dir)


def validate_summary_file(path: Path) -> list[str]:
    resolved = resolve_repo_path(path)
    payload = json.loads(resolved.read_text(encoding="utf-8"))
    errors: list[str] = []
    if payload.get("record_type") != "hash_preimage_run_summary":
        errors.append("summary has wrong record_type")
    if payload.get("algorithm") != "sha256":
        errors.append("summary algorithm must be sha256")
    if payload.get("solve_claim") is not False:
        errors.append("summary solve_claim must be false")
    if payload.get("cuda_used") is not False:
        errors.append("summary cuda_used must be false")
    if payload.get("trusted_as_canonical") is not False:
        errors.append("summary trusted_as_canonical must be false")
    return errors
