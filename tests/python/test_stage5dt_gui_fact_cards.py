from __future__ import annotations

import importlib.util
import os

import pytest

pytestmark = pytest.mark.skipif(importlib.util.find_spec("PySide6") is None, reason="PySide6 is optional")


@pytest.fixture(scope="module", autouse=True)
def _offscreen_qt() -> None:
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")


@pytest.fixture()
def app() -> object:
    from PySide6.QtWidgets import QApplication

    return QApplication.instance() or QApplication([])


def test_number_fact_card_widget_renders_review_state(app: object) -> None:
    from PySide6.QtWidgets import QLabel
    from libreprimus.operator_console.source_browser.number_fact_cards import number_fact_card_widget
    from libreprimus.operator_console.source_browser.number_facts import NumberFactCard

    card = NumberFactCard(
        fact_uid="abc",
        source_entry_id="entry",
        source_record_path="data/historical-route/fixture.yaml",
        source_fact_path="claims[0]",
        source_fact_id="claim",
        display_label="Claim needing context",
        short_label="1894",
        value=1894,
        review_state="vague_fact_enrichment_needed",
    )
    widget = number_fact_card_widget(card)

    assert any(label.property("review_state") == "vague_fact_enrichment_needed" for label in widget.findChildren(QLabel))
