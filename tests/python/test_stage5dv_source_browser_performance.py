from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

from libreprimus.operator_console.source_browser.entries import SourceBrowserEntry
from libreprimus.operator_console.source_browser.path_aliases import PathResolutionCache
from libreprimus.operator_console.source_browser.thumbnails import ThumbnailCache
from test_stage5dv_common import ensure_stage5dv_built, load_yaml


def _entry() -> SourceBrowserEntry:
    return SourceBrowserEntry(
        entry_id="stage5dv-test-entry",
        entry_type="test",
        category="Images",
        title="Test",
        summary="Test entry",
        stage_id="stage-5dv",
        record_type="stage5dv_test_record",
        candidate_family_id=None,
        source_type=None,
        source_status=None,
        trust_tier=None,
        confidence=None,
        selected_now=False,
        solve_claim=False,
        execution_allowed=False,
        source_lock_only=False,
        image_paths=["third_party/NumberFactsCollection/google_doc_1.png"] * 3,
        document_paths=["data/project-state/stage5dv-summary.yaml"] * 2,
        urls=["https://example.invalid"],
        warnings=["warning"],
        number_facts=[],
    )


def test_table_model_display_uses_compact_counts() -> None:
    if importlib.util.find_spec("PySide6") is None:
        pytest.skip("PySide6 is optional")

    from libreprimus.operator_console.source_browser.table_model import SourceBrowserTableModel

    entry = _entry()
    columns = [
        {"key": "images", "label": "Images"},
        {"key": "document_paths", "label": "Docs"},
        {"key": "urls", "label": "URLs"},
        {"key": "warnings", "label": "Warnings"},
    ]
    model = SourceBrowserTableModel([entry], columns)
    assert model._display(entry, "images") == "3 images"  # noqa: SLF001
    assert model._display(entry, "document_paths") == "2 docs"  # noqa: SLF001
    assert model._display(entry, "urls") == "1 url"  # noqa: SLF001
    assert model._display(entry, "warnings") == "1 warning"  # noqa: SLF001
    assert "3 images" in model._display_cache.values()  # noqa: SLF001


def test_path_resolution_cache_reuses_resolution_result() -> None:
    cache = PathResolutionCache([])
    first = cache.resolve("ChatGPT-ContextFile.md")
    second = cache.resolve("ChatGPT-ContextFile.md")
    assert first == second
    assert cache.exists_checks == 1


def test_thumbnail_cache_is_lazy_and_cached(monkeypatch) -> None:
    calls: list[Path] = []

    def fake_build_thumbnail(source_path: Path, size: tuple[int, int]) -> Path | None:
        calls.append(source_path)
        return Path(".cache/operator-console/thumbnails/test.png")

    monkeypatch.setattr(
        "libreprimus.operator_console.source_browser.thumbnails.build_thumbnail",
        fake_build_thumbnail,
    )
    cache = ThumbnailCache((128, 96))
    source = Path("third_party/NumberFactsCollection/google_doc_1.png")
    assert cache.get(source) == Path(".cache/operator-console/thumbnails/test.png")
    assert cache.get(source) == Path(".cache/operator-console/thumbnails/test.png")
    assert calls == [source]


def test_stage5dv_performance_policy_records_lazy_table_contract() -> None:
    ensure_stage5dv_built()
    policy = load_yaml("data/operator-console/source-browser/performance-policy.yaml")
    assert policy["table_cells_create_widgets"] is False
    assert policy["table_cells_load_pixmaps"] is False
    assert policy["raw_preview_lazy_or_cached"] is True
    assert policy["search_text_precomputed"] is True
