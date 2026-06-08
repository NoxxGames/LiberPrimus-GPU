from __future__ import annotations

import importlib.util
import os

import pytest

from libreprimus.operator_console.source_browser.entries import SourceBrowserEntry

pytestmark = pytest.mark.skipif(importlib.util.find_spec("PySide6") is None, reason="PySide6 is optional")


@pytest.fixture(scope="module", autouse=True)
def _offscreen_qt() -> None:
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")


@pytest.fixture()
def app() -> object:
    from PySide6.QtWidgets import QApplication

    return QApplication.instance() or QApplication([])


def make_entry() -> SourceBrowserEntry:
    return SourceBrowserEntry(
        entry_id="stage5dr-table-fixture",
        entry_type="synthetic_test_fixture",
        category="References",
        title="Stage 5DR table fixture",
        summary="Synthetic entry for table interaction tests.",
        stage_id="stage-5dr",
        record_type="stage5dr_table_fixture",
        candidate_family_id=None,
        source_type=None,
        source_status=None,
        trust_tier=None,
        confidence=None,
        selected_now=False,
        solve_claim=False,
        execution_allowed=False,
        source_lock_only=False,
        local_paths=["docs/operator-console/source-browser-v0.md"],
        image_paths=["missing-image.png"],
        document_paths=["docs/operator-console/source-browser-v0.md"],
        urls=["https://example.invalid/source"],
        source_record_path="data/project-state/stage5dr-summary.yaml",
        raw_record={"record_type": "stage5dr_table_fixture"},
    )


def test_blank_status_display_does_not_mutate_entry(app: object) -> None:
    from PySide6.QtCore import Qt
    from libreprimus.operator_console.source_browser.status_display import STATUS_UNSPECIFIED_TOOLTIP
    from libreprimus.operator_console.source_browser.table_model import SourceBrowserTableModel

    entry = make_entry()
    model = SourceBrowserTableModel([entry], [{"key": "status", "label": "Status"}])
    index = model.index(0, 0)

    assert model.data(index) == "unspecified"
    assert model.data(index, Qt.ItemDataRole.ToolTipRole) == STATUS_UNSPECIFIED_TOOLTIP
    assert entry.source_status is None


def test_table_context_menu_has_expected_actions(app: object) -> None:
    from libreprimus.operator_console.main_window import MainWindow

    window = MainWindow()
    menu = window._build_table_context_menu(make_entry())
    labels = [action.text() for action in menu.actions() if action.text()]

    assert "Show Details" in labels
    assert "Open Image Viewer" in labels
    assert "Open First File" in labels
    assert "Open File Location" in labels
    assert "Open First URL" in labels
    assert "Copy Entry ID" in labels
    assert "Copy Source Record Path" in labels
    assert "Copy First File Path" in labels
    assert "Copy First URL" in labels


def test_detail_panel_can_be_hidden_and_shown(app: object) -> None:
    from libreprimus.operator_console.main_window import MainWindow

    window = MainWindow()
    assert window.detail.isVisible() is False or window.show_details_action.isChecked() is True
    window.toggle_details_panel(False)
    assert window.detail.isVisible() is False
    window.toggle_details_panel(True)
    assert window.show_details_action.isChecked() is True
