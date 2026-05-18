"""OutGuess tool detection and command wrapper."""

from __future__ import annotations

import hashlib
import platform
import shutil
import subprocess
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from libreprimus.stego.models import OutGuessTool
from libreprimus.stego.outguess_export import resolve_path


def detect_outguess(explicit_path: Path | None = None) -> OutGuessTool:
    """Detect OutGuess from an explicit path or PATH."""
    candidate: Path | None = None
    if explicit_path is not None:
        resolved = resolve_path(explicit_path)
        if resolved.is_file():
            candidate = resolved
    if candidate is None:
        found = shutil.which("outguess") or shutil.which("outguess.exe")
        if found:
            candidate = Path(found)
    if candidate is None:
        return OutGuessTool(
            available=False,
            path=None,
            help_output_sha256=None,
            help_output="",
            notes="OutGuess tool not found on PATH and no usable explicit path was provided.",
        )
    help_output = _capture_help(candidate)
    return OutGuessTool(
        available=True,
        path=candidate,
        help_output_sha256=hashlib.sha256(help_output.encode("utf-8", errors="replace")).hexdigest(),
        help_output=help_output,
        notes="OutGuess tool detected.",
    )


def tool_record(tool: OutGuessTool) -> dict[str, Any]:
    """Return a public-safe tool detection record."""
    return {
        "record_type": "outguess_tool_record",
        "tool_name": "outguess",
        "tool_available": tool.available,
        "tool_path": str(tool.path) if tool.path is not None else None,
        "help_output_sha256": tool.help_output_sha256,
        "detected_at_utc": datetime.now(UTC).isoformat().replace("+00:00", "Z"),
        "platform": platform.platform(),
        "notes": tool.notes,
    }


def run_outguess_extract(tool: OutGuessTool, input_path: Path, output_path: Path) -> subprocess.CompletedProcess[str]:
    """Run `outguess -r input output` and capture command output."""
    if not tool.available or tool.path is None:
        raise ValueError("outguess tool is not available")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    return subprocess.run(
        [str(tool.path), "-r", str(input_path), str(output_path)],
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def _capture_help(path: Path) -> str:
    chunks: list[str] = []
    for flag in ("--help", "-h"):
        try:
            result = subprocess.run(
                [str(path), flag],
                check=False,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=10,
            )
        except Exception as exc:  # noqa: BLE001
            chunks.append(f"{flag}: {exc}")
            continue
        combined = (result.stdout or "") + (result.stderr or "")
        if combined.strip():
            chunks.append(combined)
            break
    return "\n".join(chunks)
