from libreprimus.alignment.boundary_audit import audit_page_boundaries
from libreprimus.alignment.models import PageBoundaryCandidate


def _boundary(**overrides: object) -> PageBoundaryCandidate:
    payload = {
        "record_type": "lp2_page_boundary_candidate",
        "source_id": "pastebin-vGMK330j",
        "pastebin_source_sha256": "pastebin-sha",
        "transcript_source_id": "rtkd-master-transcription",
        "transcript_source_sha256": "transcript-sha",
        "candidate_local_page_index": None,
        "candidate_page_label": None,
        "start_pair_index": None,
        "end_pair_index": None,
        "start_transcript_line": None,
        "end_transcript_line": None,
        "confidence": "low",
        "canonical_page_boundary": False,
        "evidence": [],
    }
    payload.update(overrides)
    return PageBoundaryCandidate(**payload)


def test_empty_pair_alone_cannot_create_high_boundary() -> None:
    audits, summary = audit_page_boundaries(
        [
            _boundary(
                confidence="low",
                evidence=["empty pair structural separator"],
                explicit_marker=False,
                anchor_supported=False,
            )
        ]
    )

    assert audits[0].empty_pair_only is True
    assert summary.high_count == 0
    assert summary.canonical_page_boundary_all_false is True


def test_explicit_marker_with_alignment_can_be_high() -> None:
    _, summary = audit_page_boundaries(
        [
            _boundary(
                confidence="high",
                evidence=["explicit rtkd percent page marker", "nearby strong alignment evidence"],
                explicit_marker=True,
                aligned_pair_count_near_boundary=2,
            )
        ]
    )

    assert summary.high_count == 1
    assert summary.candidates_with_explicit_marker == 1


def test_overgenerated_boundaries_trigger_warning() -> None:
    boundaries = [_boundary(confidence="low") for _ in range(59)]

    _, summary = audit_page_boundaries(boundaries)

    assert summary.overgeneration_warning is True
    assert summary.candidates_exceed_expected_lp2_page_count is True
