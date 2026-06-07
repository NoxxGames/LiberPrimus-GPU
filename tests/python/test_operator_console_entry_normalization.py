from __future__ import annotations

from pathlib import Path

from libreprimus.operator_console.source_browser.normalizer import context_entry, normalize_record


def test_source_browser_entry_normalization_extracts_review_fields() -> None:
    entry = normalize_record(
        Path("data/project-state/example.yaml"),
        {
            "record_type": "example_source_lock",
            "stage_id": "stage-5dq",
            "candidate_family_id": "mayfly_candidate_v0",
            "source_type": "local_metadata",
            "status": "complete",
            "trust_tier": "local_ignored",
            "confidence": "review_only",
            "summary": "Compact metadata only.",
            "local_path": "third_party/example/source.txt",
            "image_path": "third_party/example/image.jpg",
            "url": "https://example.invalid/source",
            "sha256": "a" * 64,
            "warnings": ["missing local source on CI"],
            "solve_claim": False,
            "execution_allowed": False,
        },
    )

    assert entry.stage_id == "stage-5dq"
    assert entry.category == "Mayfly"
    assert "third_party/example/image.jpg" in entry.image_paths
    assert "third_party/example/source.txt" in entry.local_paths
    assert entry.urls == ["https://example.invalid/source"]
    assert entry.hashes["sha256"] == "a" * 64
    assert entry.solve_claim is False
    assert entry.execution_allowed is False


def test_context_entry_is_review_only() -> None:
    entry = context_entry(Path("ChatGPT-ContextFile.md"))

    assert entry.entry_id == "chatgpt-context-file"
    assert entry.solve_claim is False
    assert entry.execution_allowed is False
    assert entry.category == "ChatGPT context"
