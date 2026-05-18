from __future__ import annotations

from libreprimus.paths import repo_root
from libreprimus.research_synthesis.loader import load_all_record_sets
from libreprimus.research_synthesis.models import REQUIRED_METHOD_FAMILIES


def _records() -> dict[str, list[dict]]:
    return load_all_record_sets(repo_root() / "data/research")


def test_stage3y_every_required_method_family_present() -> None:
    records = _records()["method_families"]
    method_ids = {record["method_family_id"] for record in records}

    assert REQUIRED_METHOD_FAMILIES <= method_ids


def test_stage3y_every_method_family_has_reopen_conditions() -> None:
    for record in _records()["method_families"]:
        assert record["reopen_conditions"], record["method_family_id"]


def test_stage3y_every_retirement_references_method_family() -> None:
    records = _records()
    method_ids = {record["method_family_id"] for record in records["method_families"]}

    for record in records["method_retirements"]:
        assert record["method_family_id"] in method_ids


def test_stage3y_cuda_method_family_is_deferred() -> None:
    cuda = _method("cuda_gpu_acceleration")

    assert cuda["status"] == "deferred"
    assert "parity" in " ".join(cuda["reopen_conditions"]).lower()


def test_stage3y_caesar_affine_is_noisy_or_deprioritised() -> None:
    caesar = _method("caesar_affine")
    retirement = _retirement("caesar_affine")

    assert caesar["status"] == "noisy"
    assert retirement["retired_status"] == "deprioritised"


def test_stage3y_cookie_sha256_records_negative_no_broadening() -> None:
    cookie = _method("cookie_hash_sha256_packs")
    retirement = _retirement("cookie_hash_sha256_packs")
    combined = " ".join(cookie["stop_conditions"] + retirement["prohibited_expansions"]).lower()

    assert cookie["status"] == "negative"
    assert "broad" in combined
    assert "new source" in " ".join(cookie["stop_conditions"]).lower()


def _method(method_family_id: str) -> dict:
    return next(
        record
        for record in _records()["method_families"]
        if record["method_family_id"] == method_family_id
    )


def _retirement(method_family_id: str) -> dict:
    return next(
        record
        for record in _records()["method_retirements"]
        if record["method_family_id"] == method_family_id
    )
