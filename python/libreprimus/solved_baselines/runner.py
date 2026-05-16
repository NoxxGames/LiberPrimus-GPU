"""Run solved-baseline manifests through the CPU transform registry."""

from __future__ import annotations

from collections import Counter
from pathlib import Path
from time import perf_counter

from libreprimus.paths import repo_root
from libreprimus.solved_baselines.models import (
    FixtureGroup,
    ManifestRunRecord,
    ManifestRunSummary,
    SolvedBaselineManifest,
)
from libreprimus.solved_baselines.validation import validate_manifest
from libreprimus.solved_fixtures.models import ReproductionRecord, to_jsonable
from libreprimus.solved_fixtures.reproduction import reproduce_fixtures
from libreprimus.transforms.registry import load_registry


def _resolve_repo_path(path: str | Path) -> Path:
    candidate = Path(path)
    return candidate if candidate.is_absolute() else repo_root() / candidate


def _fixture_pass_bucket(record: ReproductionRecord, group: FixtureGroup) -> str | None:
    if record.match_status != "pass":
        return None
    if group.fixture_group_id == "direct-translation-v0":
        return "direct"
    if group.fixture_group_id == "atbash-family-v0":
        return "atbash"
    if group.fixture_group_id == "vigenere-v0":
        return "vigenere"
    if group.fixture_group_id == "prime-stream-v0":
        return "prime"
    return None


def run_manifest(
    manifest: SolvedBaselineManifest,
    *,
    candidate_dir: Path | None = None,
) -> tuple[list[ManifestRunRecord], ManifestRunSummary, list[str]]:
    errors = validate_manifest(manifest)
    if errors:
        raise ValueError("; ".join(errors))
    start = perf_counter()
    registry = load_registry()
    candidate_path = candidate_dir or repo_root() / "data/normalized/corpus-candidates" / manifest.corpus_candidate_id
    if not candidate_path.is_dir():
        raise FileNotFoundError(f"Corpus candidate directory missing: {candidate_path}")

    records: list[ManifestRunRecord] = []
    warnings: list[str] = []
    pass_buckets = Counter()
    for group in manifest.fixture_groups:
        fixture_dir = _resolve_repo_path(group.fixture_dir)
        fixture_records, fixture_summary, fixture_warnings = reproduce_fixtures(
            fixture_dir=fixture_dir,
            candidate_dir=candidate_path,
            fixture_set_id=group.fixture_group_id,
            registry=registry,
        )
        if fixture_summary.fixture_count != group.expected_fixture_count:
            warnings.append(
                f"{group.fixture_group_id}: expected {group.expected_fixture_count} fixtures, "
                f"found {fixture_summary.fixture_count}."
            )
        if fixture_summary.pass_count != group.expected_pass_count:
            warnings.append(
                f"{group.fixture_group_id}: expected {group.expected_pass_count} passes, "
                f"found {fixture_summary.pass_count}."
            )
        warnings.extend(f"{group.fixture_group_id}: {warning}" for warning in fixture_warnings)
        for fixture_record in fixture_records:
            bucket = _fixture_pass_bucket(fixture_record, group)
            if bucket is not None:
                pass_buckets[bucket] += 1
            records.append(
                ManifestRunRecord(
                    record_type="solved_baseline_manifest_run_record",
                    manifest_id=manifest.manifest_id,
                    manifest_sha256=manifest.manifest_sha256,
                    registry_id=registry.registry_id,
                    registry_sha256=registry.sha256,
                    fixture_group_id=group.fixture_group_id,
                    fixture_id=fixture_record.fixture_id,
                    transform_id=fixture_record.transform_id,
                    canonical_transform_id=fixture_record.canonical_transform_id,
                    method_family=fixture_record.method_family,
                    match_status=fixture_record.match_status,
                    mismatch_reason=fixture_record.mismatch_reason,
                    search_performed=fixture_record.search_performed,
                    cuda_used=fixture_record.cuda_used,
                    scoring_used=fixture_record.scoring_used,
                    canonical_corpus_active=False,
                    page_boundaries_final=False,
                    trusted_as_canonical=False,
                    source_record=to_jsonable(fixture_record),
                )
            )

    counts = Counter(record.match_status for record in records)
    search_any = any(record.search_performed for record in records)
    cuda_any = any(record.cuda_used for record in records)
    scoring_any = any(record.scoring_used for record in records)
    summary = ManifestRunSummary(
        record_type="solved_baseline_manifest_run_summary",
        manifest_id=manifest.manifest_id,
        manifest_sha256=manifest.manifest_sha256,
        registry_id=registry.registry_id,
        registry_sha256=registry.sha256,
        fixture_group_count=len(manifest.fixture_groups),
        fixture_count=len(records),
        pass_count=counts["pass"],
        fail_count=counts["fail"],
        pending_count=counts["pending"],
        skipped_count=counts["skipped"],
        direct_translation_pass_count=pass_buckets["direct"],
        atbash_family_pass_count=pass_buckets["atbash"],
        vigenere_pass_count=pass_buckets["vigenere"],
        prime_stream_pass_count=pass_buckets["prime"],
        search_performed_any=search_any,
        cuda_used_any=cuda_any,
        scoring_used_any=scoring_any,
        canonical_corpus_active=False,
        page_boundaries_final=False,
        elapsed_ms=round((perf_counter() - start) * 1000, 3),
        warnings=warnings,
    )
    return records, summary, warnings
