"""Classify historical stego/audio fixture source candidates."""

from __future__ import annotations

from typing import Any

from libreprimus.stego_fixtures.loaders import find_stage4b_source
from libreprimus.stego_fixtures.models import IDDDQ_REPO_BLOB_BASE, IDDDQ_REPO_TREE_BASE


def build_outguess_fixture_records(
    stage4e_candidates: list[dict[str, Any]],
    stage4b_sources: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Build Stage 4F OutGuess/stego fixture source records."""

    del stage4e_candidates
    records = [
        _fixture(
            fixture_id="stage4f-iddqd-lp-outguessed-tree",
            source_id="stage4e-cicada-solvers-iddqd",
            source_url=f"{IDDDQ_REPO_TREE_BASE}/lp_outguessed",
            source_path="lp_outguessed/",
            artifact_type="lp_outguessed",
            expected_role="known_positive_candidate",
            local_availability="source_only",
            toolchain=["outguess"],
            notes="Selected for future positive/negative OutGuess fixture matrix; raw files are not downloaded in Stage 4F.",
        ),
        _fixture(
            fixture_id="stage4f-iddqd-2016-4gq25-image",
            source_id="stage4e-cicada-solvers-iddqd",
            source_url=f"{IDDDQ_REPO_BLOB_BASE}/2016/01/4gq25.jpg",
            source_path="2016/01/4gq25.jpg",
            artifact_type="image_fixture_candidate",
            expected_role="known_positive_candidate",
            local_availability="source_only",
            toolchain=["outguess"],
            notes="2016 image fixture candidate; future stage must source-lock the asset before extraction.",
        ),
        _fixture(
            fixture_id="stage4f-iddqd-2013-02-assets",
            source_id="stage4e-cicada-solvers-iddqd",
            source_url=f"{IDDDQ_REPO_TREE_BASE}/2013/02",
            source_path="2013/02/",
            artifact_type="historical_2013",
            expected_role="future_download_candidate",
            local_availability="source_only",
            toolchain=["outguess", "hexdump/strings"],
            notes="Historical 2013 asset tree; metadata only until a fixture-source stage selects individual files.",
        ),
    ]
    for source_id, fixture_id, path, toolchain in [
        ("stage4b-uncovering-outguess", "stage4f-uncovering-outguess-page", "Uncovering Cicada OutGuess", ["outguess"]),
        (
            "stage4b-complete-archive-magicsquares",
            "stage4f-complete-archive-magicsquares-openpuff-context",
            "assets/2014/stage07/magicsquares.txt",
            ["openpuff"],
        ),
    ]:
        source = find_stage4b_source(stage4b_sources, source_id)
        if source is None:
            continue
        records.append(
            _fixture(
                fixture_id=fixture_id,
                source_id=source_id,
                source_url=str(source.get("url")),
                source_path=path,
                artifact_type="reference_source",
                expected_role="reference_only",
                local_availability="deferred",
                toolchain=toolchain,
                notes="Stage 4B public source used as fixture context; no tool execution in Stage 4F.",
            )
        )
    return records


def build_audio_fixture_records(stage4b_sources: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Build Stage 4F audio fixture source records."""

    records = [
        _fixture(
            fixture_id="stage4f-iddqd-interconnectedness-mp3",
            source_id="stage4e-cicada-solvers-iddqd",
            source_url=f"{IDDDQ_REPO_BLOB_BASE}/2014/05/3301%20-%20Interconnectedness.mp3",
            source_path="2014/05/3301 - Interconnectedness.mp3",
            artifact_type="audio_fixture_candidate",
            expected_role="known_positive_candidate",
            local_availability="source_only",
            toolchain=["openpuff", "audio_rendering", "hexdump/strings"],
            notes="Interconnectedness MP3 fixture candidate; future source-lock only before any analysis.",
            record_type="audio_fixture_source_record",
        ),
        _fixture(
            fixture_id="stage4f-iddqd-761-mp3-instar",
            source_id="stage4e-cicada-solvers-iddqd",
            source_url=f"{IDDDQ_REPO_BLOB_BASE}/2013/02/761.MP3",
            source_path="2013/02/761.MP3",
            artifact_type="audio_fixture_candidate",
            expected_role="known_positive_candidate",
            local_availability="source_only",
            toolchain=["mp3stego", "audio_rendering", "hexdump/strings"],
            notes="Instar-era MP3 fixture candidate; metadata only in Stage 4F.",
            record_type="audio_fixture_source_record",
        ),
    ]
    for source_id, fixture_id, path, toolchain in [
        (
            "stage4b-uncovering-instar-emergence",
            "stage4f-uncovering-instar-emergence-page",
            "Instar emergence source page",
            ["mp3stego", "audio_rendering"],
        ),
        (
            "stage4b-uncovering-what-happened-2014",
            "stage4f-uncovering-what-happened-2014-openpuff-page",
            "What Happened Part 1 2014 source page",
            ["openpuff"],
        ),
        (
            "stage4b-charleswyt-mp3stego",
            "stage4f-charleswyt-mp3stego-reference",
            "MP3Stego reference repository",
            ["mp3stego"],
        ),
    ]:
        source = find_stage4b_source(stage4b_sources, source_id)
        if source is None:
            continue
        records.append(
            _fixture(
                fixture_id=fixture_id,
                source_id=source_id,
                source_url=str(source.get("url")),
                source_path=path,
                artifact_type="reference_source",
                expected_role="reference_only",
                local_availability="deferred",
                toolchain=toolchain,
                notes="Public source context only; no audio or stego tooling was run in Stage 4F.",
                record_type="audio_fixture_source_record",
            )
        )
    return records


def _fixture(
    *,
    fixture_id: str,
    source_id: str,
    source_url: str,
    source_path: str,
    artifact_type: str,
    expected_role: str,
    local_availability: str,
    toolchain: list[str],
    notes: str,
    record_type: str = "stego_fixture_source_record",
) -> dict[str, Any]:
    return {
        "record_type": record_type,
        "fixture_id": fixture_id,
        "source_id": source_id,
        "source_url": source_url,
        "source_path": source_path,
        "artifact_type": artifact_type,
        "expected_role": expected_role,
        "local_availability": local_availability,
        "toolchain": toolchain,
        "raw_file_committed": False,
        "binary_committed": False,
        "audio_committed": False,
        "image_committed": False,
        "extracted_payload_committed": False,
        "font_committed": False,
        "trusted_as_canonical": False,
        "solve_claim": False,
        "notes": notes,
    }
