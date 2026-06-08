from __future__ import annotations

import importlib.util
import os
from pathlib import Path

import pytest

import libreprimus.operator_console.source_browser.path_aliases as path_aliases_module
from libreprimus.operator_console.source_browser.entries import SourceBrowserEntry

pytestmark = pytest.mark.skipif(importlib.util.find_spec("PySide6") is None, reason="PySide6 is optional")


@pytest.fixture(scope="module", autouse=True)
def _offscreen_qt() -> None:
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")


@pytest.fixture()
def app() -> object:
    from PySide6.QtWidgets import QApplication

    return QApplication.instance() or QApplication([])


def make_entry(image_path: str | None = None) -> SourceBrowserEntry:
    image_paths = [image_path] if image_path else []
    return SourceBrowserEntry(
        entry_id="stage5dr-detail-fixture",
        entry_type="synthetic_test_fixture",
        category="Images",
        title="Stage 5DR detail fixture",
        summary="Synthetic entry for detail-panel rendering.",
        stage_id="stage-5dr",
        record_type="stage5dr_detail_fixture",
        candidate_family_id="fixture-family",
        source_type="fixture",
        source_status=None,
        trust_tier="review_only",
        confidence="triage_only",
        selected_now=False,
        solve_claim=False,
        execution_allowed=False,
        source_lock_only=False,
        local_paths=["docs/operator-console/source-browser-v0.md", *image_paths],
        image_paths=image_paths,
        document_paths=["docs/operator-console/source-browser-v0.md"],
        urls=["https://example.invalid/source"],
        hashes={"fixture.sha256": "a" * 64},
        number_facts=[{"fact_id": "fixture-fact", "expression": "2+2", "result": 4}],
        links_to=["linked-source-id"],
        warnings=["Synthetic warning"],
        notes="No puzzle execution.",
        source_record_path="data/project-state/stage5dr-summary.yaml",
        schema_path="schemas/project-state/stage5dr-summary-v0.schema.json",
        raw_record={"record_type": "stage5dr_detail_fixture", "solve_claim": False},
    )


def test_detail_panel_renders_selected_entry_sections(app: object) -> None:
    from PySide6.QtCore import Qt
    from PySide6.QtWidgets import QPlainTextEdit, QScrollArea
    from libreprimus.operator_console.source_browser.detail_panel import EntryDetailPanel

    panel = EntryDetailPanel()
    panel.show_entry(make_entry())

    assert panel.header.text() == "Stage 5DR detail fixture"
    assert panel.tabs.count() == 5
    assert panel.raw_text.toPlainText()
    assert "stage5dr_detail_fixture" in panel.raw_text.toPlainText()
    assert panel.raw_text.lineWrapMode() == QPlainTextEdit.LineWrapMode.WidgetWidth
    assert panel.raw_text.horizontalScrollBarPolicy() == Qt.ScrollBarPolicy.ScrollBarAlwaysOff
    assert all(
        scroll.horizontalScrollBarPolicy() == Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        for scroll in panel.findChildren(QScrollArea)
    )


def test_detail_panel_renders_media_urls_number_facts_and_warnings(
    app: object,
    tmp_path: Path,
) -> None:
    from PySide6.QtGui import QColor, QImage
    from PySide6.QtWidgets import QPlainTextEdit, QToolButton, QWidget
    from libreprimus.operator_console.source_browser.detail_panel import EntryDetailPanel

    image_path = tmp_path / "fixture.png"
    image = QImage(12, 12, QImage.Format.Format_RGB32)
    image.fill(QColor("#224466"))
    assert image.save(str(image_path))

    panel = EntryDetailPanel()
    panel.show_entry(make_entry(str(image_path)))

    assert panel.findChildren(QToolButton, "sourceBrowserThumbnailButton")
    assert panel.findChildren(QWidget, "sourceBrowserPathRow")
    assert panel.findChildren(QWidget, "sourceBrowserUrlRow")
    assert any("fixture-fact" in text.toPlainText() for text in panel.findChildren(QPlainTextEdit))
    assert "Synthetic warning" in panel.raw_text.toPlainText()


def test_thumbnail_action_can_instantiate_image_viewer(app: object, tmp_path: Path) -> None:
    from PySide6.QtGui import QColor, QImage
    from libreprimus.operator_console.source_browser.image_viewer import ImageViewerDialog

    image_path = tmp_path / "fixture.png"
    image = QImage(10, 10, QImage.Format.Format_RGB32)
    image.fill(QColor("#113355"))
    assert image.save(str(image_path))

    dialog = ImageViewerDialog([str(image_path)], start_index=0)
    assert dialog.paths[0] == image_path
    assert dialog.label.pixmap() is not None


def test_image_viewer_resolves_archive_relative_image_path(
    app: object,
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    from PySide6.QtGui import QColor, QImage
    from libreprimus.operator_console.source_browser.image_viewer import ImageViewerDialog

    image_path = (
        tmp_path
        / "third_party"
        / "CicadaSolversIddqd"
        / "2014"
        / "additional images"
        / "OutguessfromLiberPrimusPage6.jpg"
    )
    image_path.parent.mkdir(parents=True)
    image = QImage(10, 10, QImage.Format.Format_RGB32)
    image.fill(QColor("#113355"))
    assert image.save(str(image_path))
    monkeypatch.setattr(path_aliases_module, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(
        path_aliases_module,
        "ARCHIVE_RELATIVE_ROOTS",
        (Path("third_party/CicadaSolversIddqd"),),
    )

    dialog = ImageViewerDialog(["2014/additional images/OutguessfromLiberPrimusPage6.jpg"])

    assert dialog.paths[0] == image_path
    assert dialog.label.pixmap() is not None
