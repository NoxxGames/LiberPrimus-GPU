from __future__ import annotations

import hashlib

from libreprimus.cookie_refresh.hash_runner import run_exact_comparisons
from libreprimus.cookie_refresh.models import ExpandedCookieCandidate
from libreprimus.hash_preimage.models import CookieTarget


def test_stage4g_exact_match_works_on_synthetic_target() -> None:
    candidate = _candidate("match-me")
    target = CookieTarget(
        cookie_id="cookie-test",
        cookie_name="test",
        cookie_value=hashlib.sha256(b"match-me").hexdigest(),
    )
    records, matches = run_exact_comparisons(
        candidates=[candidate],
        targets=[target],
        algorithms=("sha256",),
        experiment_id="exp_stage4b_cookie_pack_v2",
    )
    assert len(records) == 1
    assert len(matches) == 1
    assert matches[0]["exact_match"] is True
    assert matches[0]["no_solve_claim"] is True
    assert matches[0]["cuda_used"] is False
    assert matches[0]["hashcat_used"] is False


def test_stage4g_non_match_stays_exact_only() -> None:
    candidate = _candidate("miss")
    target = CookieTarget(
        cookie_id="cookie-test",
        cookie_name="test",
        cookie_value=hashlib.sha256(b"match").hexdigest(),
    )
    records, matches = run_exact_comparisons(
        candidates=[candidate],
        targets=[target],
        algorithms=("sha256",),
        experiment_id="exp_stage4b_cookie_pack_v2",
    )
    assert len(matches) == 0
    assert records[0]["exact_match"] is False
    assert records[0]["exact_match_only"] is True
    assert records[0]["fuzzy_matching"] is False
    assert records[0]["partial_matching"] is False


def _candidate(text: str) -> ExpandedCookieCandidate:
    payload = text.encode("utf-8")
    return ExpandedCookieCandidate(
        candidate_id="stage4g-cookie-candidate-000001",
        base_string_id="base-1",
        source_record_id="source-1",
        source_basis="source-backed synthetic fixture",
        raw_string_redacted_if_needed=text,
        byte_variant="raw",
        encoding="utf-8",
        candidate_text=text,
        candidate_bytes=payload,
        candidate_bytes_sha256=hashlib.sha256(payload).hexdigest(),
        previous_pack_duplicate=False,
    )
