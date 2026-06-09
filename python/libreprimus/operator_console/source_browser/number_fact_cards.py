"""Qt rendering helpers for Source Browser number-fact cards."""

from __future__ import annotations

import yaml
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPlainTextEdit,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from .number_facts import NumberFactCard


STATE_LABELS = {
    "rich_fact_card": "rich",
    "extracted_basic_fact": "basic",
    "vague_fact_enrichment_needed": "needs context",
    "zero_extracted_facts_not_reviewed": "not reviewed",
    "zero_extracted_facts_reviewed_none_found": "none found",
    "overlay_enriched_fact": "overlay",
    "quarantined_fact": "quarantine",
    "canonical_verification_required": "canonical check",
}


def number_fact_card_widget(card: NumberFactCard) -> QWidget:
    frame = QFrame()
    frame.setObjectName("sourceBrowserNumberFactCard")
    frame.setFrameShape(QFrame.Shape.StyledPanel)
    layout = QVBoxLayout(frame)
    layout.setContentsMargins(10, 8, 10, 8)
    layout.setSpacing(6)

    header = QHBoxLayout()
    badge = QLabel(STATE_LABELS.get(card.review_state, card.review_state))
    badge.setObjectName(f"numberFactBadge_{card.review_state}")
    badge.setProperty("review_state", card.review_state)
    badge.setStyleSheet(_badge_style(card.review_state))
    header.addWidget(badge, 0)

    title = QLabel(card.display_label)
    title.setObjectName("numberFactTitle")
    title.setWordWrap(True)
    title.setStyleSheet("font-weight: 600; color: #f1f1f1;")
    header.addWidget(title, 1)
    layout.addLayout(header)

    layout.addWidget(_wrapped_label(_value_line(card)))
    layout.addWidget(_wrapped_label(f"Relation: {card.relation or 'missing; enrichment needed'}"))
    layout.addWidget(_wrapped_label(f"Why stored: {card.why_stored or 'missing; enrichment needed'}"))
    layout.addWidget(_wrapped_label(f"Verification: {card.verification_status}"))
    risk_text = "; ".join(card.risk_notes) if card.risk_notes else "none recorded"
    layout.addWidget(_wrapped_label(f"Risk: {risk_text}"))
    source_text = f"{card.source_record_path}"
    if card.source_fact_path:
        source_text += f" / {card.source_fact_path}"
    layout.addWidget(_wrapped_label(f"Source: {source_text}"))
    if card.crosslinks:
        layout.addWidget(_wrapped_label(f"Links: {'; '.join(card.crosslinks)}"))
    if card.overlay_applied:
        layout.addWidget(_wrapped_label(f"Overlay: {card.overlay_path or 'applied'}"))

    raw = QPlainTextEdit()
    raw.setObjectName("numberFactRawPreview")
    raw.setReadOnly(True)
    raw.setLineWrapMode(QPlainTextEdit.LineWrapMode.WidgetWidth)
    raw.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
    raw.setPlainText(yaml.safe_dump(card.raw_fact, sort_keys=False, allow_unicode=False))
    raw.setMaximumHeight(90)
    layout.addWidget(raw)
    frame.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Maximum)
    return frame


def _wrapped_label(text: str) -> QLabel:
    label = QLabel(text)
    label.setWordWrap(True)
    label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
    label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
    return label


def _value_line(card: NumberFactCard) -> str:
    value = "unspecified" if card.value is None else str(card.value)
    return f"Value: {value}   Type: {card.value_type or 'unknown'}   Operation: {card.operation_type or 'unknown'}"


def _badge_style(review_state: str) -> str:
    colors = {
        "rich_fact_card": ("#1f3d2d", "#74d28b"),
        "overlay_enriched_fact": ("#203a4a", "#91d1ff"),
        "extracted_basic_fact": ("#33383f", "#d8d8d8"),
        "vague_fact_enrichment_needed": ("#4a3518", "#f4c266"),
        "canonical_verification_required": ("#40304a", "#e2b7ff"),
        "quarantined_fact": ("#4a2020", "#ff9b9b"),
    }
    bg, fg = colors.get(review_state, ("#303034", "#e8e8e8"))
    return (
        f"background: {bg}; color: {fg}; border: 1px solid #55555c; "
        "border-radius: 3px; padding: 2px 6px; font-weight: 600;"
    )
