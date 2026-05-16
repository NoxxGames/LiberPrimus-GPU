"""Solved-page fixture reproduction pipeline."""

from __future__ import annotations

from collections import Counter
from datetime import datetime, timezone
import subprocess
from pathlib import Path
from time import perf_counter

from libreprimus.solved_fixtures.atbash_family import decode_atbash_family
from libreprimus.solved_fixtures.direct_translation import decode_direct_translation
from libreprimus.solved_fixtures.fixture_loader import load_fixtures
from libreprimus.solved_fixtures.models import ReproductionRecord, ReproductionSummary
from libreprimus.solved_fixtures.prime_stream import decode_prime_minus_one_stream
from libreprimus.solved_fixtures.span_selection import select_tokens
from libreprimus.solved_fixtures.vigenere import decode_vigenere_explicit_key

DIRECT_FIXTURE_SET_ID = "direct-translation-v0"
ATBASH_FIXTURE_SET_ID = "atbash-family-v0"
VIGENERE_FIXTURE_SET_ID = "vigenere-v0"
PRIME_STREAM_FIXTURE_SET_ID = "prime-stream-v0"


def _git_commit() -> str:
    try:
        result = subprocess.run(["git", "rev-parse", "HEAD"], check=True, capture_output=True, text=True)
    except (OSError, subprocess.CalledProcessError):
        return "unknown"
    return result.stdout.strip()


def reproduce_fixtures(
    *,
    fixture_dir: Path,
    candidate_dir: Path,
    fixture_set_id: str,
) -> tuple[list[ReproductionRecord], ReproductionSummary, list[str]]:
    start = perf_counter()
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    git_commit = _git_commit()
    fixtures = load_fixtures(fixture_dir)
    records: list[ReproductionRecord] = []
    warnings: list[str] = []
    for fixture in fixtures:
        decoded_text: str | None = None
        decoded_hash: str | None = None
        mismatch_reason: str | None = None
        rune_count = 0
        numeric_literal_count = 0
        separator_count = 0
        decoded_index_formula: str | None = None
        transform_parameters: dict[str, object] = {}
        key_text: str | None = None
        key_indices: list[int] = []
        skip_rule_applied_count = 0
        prime_values_used_count = 0
        stream_values_used_count = 0
        first_prime_values: list[int] = []
        first_stream_values_mod29: list[int] = []
        payload_check_results: list[dict[str, object]] = []
        record_warnings: list[str] = []
        supported_method = fixture.method_family in {
            "direct_translation",
            "reverse_gematria",
            "rotated_reverse_gematria",
            "vigenere",
            "prime_minus_one_stream",
            "phi_prime_stream",
        }
        if not supported_method or not fixture.in_scope_for_stage:
            status = "pending" if fixture.method_status.startswith("pending") else "skipped"
            mismatch_reason = fixture.method_status
        else:
            tokens, selection_error = select_tokens(candidate_dir, fixture.span_selector)
            if selection_error is not None:
                status = "skipped"
                mismatch_reason = selection_error
            else:
                if fixture.method_family == "direct_translation":
                    result = decode_direct_translation(tokens)
                    decoded_index_formula = "decoded_index = cipher_index"
                    transform_parameters = {}
                else:
                    if fixture.method_family == "vigenere":
                        result = decode_vigenere_explicit_key(tokens, transform_chain=fixture.transform_chain)
                    elif fixture.method_family in {"prime_minus_one_stream", "phi_prime_stream"}:
                        result = decode_prime_minus_one_stream(
                            tokens,
                            transform_chain=fixture.transform_chain,
                            payload_checks=fixture.payload_checks,
                        )
                    else:
                        result = decode_atbash_family(
                            tokens,
                            method_family=fixture.method_family,
                            transform_chain=fixture.transform_chain,
                        )
                    decoded_index_formula = str(result["decoded_index_formula"])
                    transform_parameters = dict(result["transform_parameters"])
                    key_text = result.get("key_text") if isinstance(result.get("key_text"), str) else None
                    key_indices = [int(item) for item in result.get("key_indices", [])]
                    skip_rule_applied_count = int(result.get("skip_rule_applied_count", 0))
                    prime_values_used_count = int(result.get("prime_values_used_count", 0))
                    stream_values_used_count = int(result.get("stream_values_used_count", 0))
                    first_prime_values = [int(item) for item in result.get("first_prime_values", [])]
                    first_stream_values_mod29 = [int(item) for item in result.get("first_stream_values_mod29", [])]
                    payload_check_results = [
                        dict(item) for item in result.get("payload_check_results", []) if isinstance(item, dict)
                    ]
                decoded_text = result["decoded_normalized_plaintext"]
                decoded_hash = result["decoded_normalized_plaintext_sha256"]
                rune_count = int(result["rune_count"])
                numeric_literal_count = int(result["numeric_literal_count"])
                separator_count = int(result["separator_count"])
                record_warnings = [str(item) for item in result["warnings"]]
                if fixture.expected_normalized_plaintext_sha256 is None:
                    status = "pending"
                    mismatch_reason = "fixture has no expected hash"
                elif decoded_hash == fixture.expected_normalized_plaintext_sha256:
                    status = "pass"
                else:
                    status = "fail"
                    mismatch_reason = "decoded plaintext SHA-256 did not match fixture expectation"
        if record_warnings:
            warnings.extend(f"{fixture.fixture_id}: {warning}" for warning in record_warnings)
        records.append(
            ReproductionRecord(
                record_type="solved_page_reproduction_record",
                fixture_id=fixture.fixture_id,
                corpus_candidate_id=fixture.corpus_candidate_id,
                generated_at_utc=now,
                git_commit=git_commit,
                method_family=fixture.method_family,
                transform_chain=fixture.transform_chain,
                decoded_index_formula=decoded_index_formula,
                transform_parameters=transform_parameters,
                key_text=key_text,
                key_indices=key_indices,
                skip_rule_applied_count=skip_rule_applied_count,
                prime_values_used_count=prime_values_used_count,
                stream_values_used_count=stream_values_used_count,
                first_prime_values=first_prime_values,
                first_stream_values_mod29=first_stream_values_mod29,
                payload_check_results=payload_check_results,
                span_selector=fixture.span_selector,
                decoded_normalized_plaintext=decoded_text,
                decoded_normalized_plaintext_sha256=decoded_hash,
                expected_normalized_plaintext_sha256=fixture.expected_normalized_plaintext_sha256,
                match_status=status,
                mismatch_reason=mismatch_reason,
                rune_count=rune_count,
                numeric_literal_count=numeric_literal_count,
                separator_count=separator_count,
                warnings=record_warnings,
                trusted_as_canonical=False,
                canonical_corpus_active=False,
                page_boundaries_final=False,
            )
        )
    counts = Counter(record.match_status for record in records)
    summary = ReproductionSummary(
        record_type="solved_page_reproduction_summary",
        fixture_set_id=fixture_set_id,
        generated_at_utc=now,
        git_commit=git_commit,
        fixture_count=len(records),
        pass_count=counts["pass"],
        fail_count=counts["fail"],
        pending_count=counts["pending"],
        skipped_count=counts["skipped"],
        direct_translation_pass_count=sum(
            1 for record in records if record.method_family == "direct_translation" and record.match_status == "pass"
        ),
        direct_translation_fail_count=sum(
            1 for record in records if record.method_family == "direct_translation" and record.match_status == "fail"
        ),
        canonical_corpus_active=False,
        page_boundaries_final=False,
        warnings=warnings,
        elapsed_ms=round((perf_counter() - start) * 1000, 3),
    )
    return records, summary, warnings


def reproduce_direct_translation_fixtures(
    *,
    fixture_dir: Path,
    candidate_dir: Path,
) -> tuple[list[ReproductionRecord], ReproductionSummary, list[str]]:
    return reproduce_fixtures(
        fixture_dir=fixture_dir,
        candidate_dir=candidate_dir,
        fixture_set_id=DIRECT_FIXTURE_SET_ID,
    )


def reproduce_atbash_family_fixtures(
    *,
    fixture_dir: Path,
    candidate_dir: Path,
) -> tuple[list[ReproductionRecord], ReproductionSummary, list[str]]:
    return reproduce_fixtures(
        fixture_dir=fixture_dir,
        candidate_dir=candidate_dir,
        fixture_set_id=ATBASH_FIXTURE_SET_ID,
    )


def reproduce_vigenere_fixtures(
    *,
    fixture_dir: Path,
    candidate_dir: Path,
) -> tuple[list[ReproductionRecord], ReproductionSummary, list[str]]:
    return reproduce_fixtures(
        fixture_dir=fixture_dir,
        candidate_dir=candidate_dir,
        fixture_set_id=VIGENERE_FIXTURE_SET_ID,
    )


def reproduce_prime_stream_fixtures(
    *,
    fixture_dir: Path,
    candidate_dir: Path,
) -> tuple[list[ReproductionRecord], ReproductionSummary, list[str]]:
    return reproduce_fixtures(
        fixture_dir=fixture_dir,
        candidate_dir=candidate_dir,
        fixture_set_id=PRIME_STREAM_FIXTURE_SET_ID,
    )
