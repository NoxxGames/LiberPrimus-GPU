"""Operator Console exception types."""

from __future__ import annotations


class OperatorConsoleError(RuntimeError):
    """Base error for operator-console failures."""


class GuiDependencyError(OperatorConsoleError):
    """Raised when optional GUI dependencies are unavailable."""
