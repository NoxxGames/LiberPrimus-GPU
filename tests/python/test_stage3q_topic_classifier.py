from __future__ import annotations

from libreprimus.discord_review.topic_classifier import classify_topic


def test_topic_classifier_routes_cuneiform_base60_text() -> None:
    assert classify_topic(text="cuneiform base60 Babylonian values 1033 3301") == "cuneiform-base60-and-babylonian"


def test_topic_classifier_routes_page_art_dots_text() -> None:
    assert classify_topic(text="page art dots binary braille stars") == "page-art-dots-binary-braille-stars"


def test_topic_classifier_routes_hash_cookie_text() -> None:
    assert classify_topic(text="deep web hash cookie 761 167") == "deep-web-hash-and-cookies"


def test_topic_classifier_routes_vigenere_text() -> None:
    assert classify_topic(text="Vigenere key literature") == "vigenere-keys-and-literature"
