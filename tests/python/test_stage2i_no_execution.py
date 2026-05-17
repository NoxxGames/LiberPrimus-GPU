from __future__ import annotations

import json
from pathlib import Path

from typer.testing import CliRunner

import libreprimus.approval_readiness.packet_generator as packet_generator
from libreprimus.cli import app

REPO = Path(__file__).resolve().parents[2]
STAGE2I = REPO / "experiments/proposals/stage2i"
PROPOSAL = STAGE2I / "stage2i-first-bounded-caesar-affine-review.yaml"
APPROVAL = STAGE2I / "approval-records/stage2i-first-bounded-caesar-affine-pending-approval.yaml"


def test_approval_readiness_cli_does_not_import_execution_runner() -> None:
    assert not hasattr(packet_generator, "run_cpu_execution_manifest")


def test_packet_generation_creates_no_execution_result(tmp_path: Path) -> None:
    result = CliRunner().invoke(
        app,
        [
            "approval-readiness",
            "packet",
            "--proposal",
            str(PROPOSAL),
            "--approval",
            str(APPROVAL),
            "--out-dir",
            str(tmp_path),
            "--allow-warnings",
        ],
    )

    assert result.exit_code == 0, result.output
    assert not list(tmp_path.glob("*execution-result*"))
    assert not list(tmp_path.glob("*execution-results*"))


def test_packet_has_no_candidate_plaintext_field(tmp_path: Path) -> None:
    result = CliRunner().invoke(
        app,
        [
            "approval-readiness",
            "packet",
            "--proposal",
            str(PROPOSAL),
            "--approval",
            str(APPROVAL),
            "--out-dir",
            str(tmp_path),
            "--allow-warnings",
        ],
    )
    assert result.exit_code == 0, result.output
    packet = json.loads(next(tmp_path.glob("*approval-readiness-packet.json")).read_text(encoding="utf-8"))

    assert "candidate_plaintext" not in json.dumps(packet)
    assert packet["execution_enabled"] is False
    assert packet["candidate_generation_enabled"] is False
