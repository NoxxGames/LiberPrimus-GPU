from __future__ import annotations

from libreprimus.parallel_validation import pytest_runner


def test_xdist_detection_returns_boolean() -> None:
    assert isinstance(pytest_runner.pytest_xdist_available(), bool)


def test_auto_mode_falls_back_to_shard_without_xdist(monkeypatch) -> None:
    monkeypatch.setattr(pytest_runner, "pytest_xdist_available", lambda: False)
    assert pytest_runner.select_pytest_mode("auto") == ("shard", False, True)


def test_auto_mode_uses_shards_on_windows(monkeypatch) -> None:
    monkeypatch.setattr(pytest_runner, "pytest_xdist_available", lambda: True)
    monkeypatch.setattr(pytest_runner.sys, "platform", "win32")
    assert pytest_runner.select_pytest_mode("auto") == ("shard", True, True)


def test_xdist_mode_falls_back_when_unavailable(monkeypatch) -> None:
    monkeypatch.setattr(pytest_runner, "pytest_xdist_available", lambda: False)
    assert pytest_runner.select_pytest_mode("xdist") == ("shard", False, True)
