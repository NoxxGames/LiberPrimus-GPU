from __future__ import annotations

from pathlib import Path
import subprocess

from typer.testing import CliRunner

from libreprimus.cli import app


def test_source_delta_cli_with_synthetic_local_git_tree(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    _init_repo(repo)
    out = tmp_path / "out"
    records = tmp_path / "records"
    manifests = tmp_path / "manifests"
    result = CliRunner().invoke(
        app,
        [
            "source-delta-audit",
            "run",
            "--repo-url",
            str(repo),
            "--cache-dir",
            str(tmp_path / "cache"),
            "--out-dir",
            str(out),
            "--source-delta-out",
            str(records / "delta.yaml"),
            "--source-health-out",
            str(records / "health.yaml"),
            "--image-artifact-out",
            str(records / "artifact.yaml"),
            "--manifest-out-dir",
            str(manifests),
            "--allow-warnings",
        ],
    )
    assert result.exit_code == 0, result.output
    assert "remote_reachable=true" in result.output
    assert "category_lp_full_image=1" in result.output
    validate = CliRunner().invoke(
        app,
        [
            "source-delta-audit",
            "validate",
            "--source-delta",
            str(records / "delta.yaml"),
            "--source-health",
            str(records / "health.yaml"),
            "--image-artifact",
            str(records / "artifact.yaml"),
            "--manifest-dir",
            str(manifests),
        ],
    )
    assert validate.exit_code == 0, validate.output
    assert "source_delta_audit_valid=true" in validate.output


def test_source_delta_cli_network_unavailable_deferred(tmp_path: Path) -> None:
    records = tmp_path / "records"
    manifests = tmp_path / "manifests"
    result = CliRunner().invoke(
        app,
        [
            "source-delta-audit",
            "run",
            "--repo-url",
            "https://example.invalid/no-network.git",
            "--cache-dir",
            str(tmp_path / "cache"),
            "--out-dir",
            str(tmp_path / "out"),
            "--source-delta-out",
            str(records / "delta.yaml"),
            "--source-health-out",
            str(records / "health.yaml"),
            "--image-artifact-out",
            str(records / "artifact.yaml"),
            "--manifest-out-dir",
            str(manifests),
            "--allow-warnings",
        ],
    )
    assert result.exit_code == 0, result.output
    assert "remote_reachable=false" in result.output
    assert (tmp_path / "out" / "warnings.jsonl").is_file()


def _init_repo(repo: Path) -> None:
    (repo / "liber-primus__images--full").mkdir(parents=True)
    (repo / "lp_outguessed").mkdir()
    (repo / "2014" / "05").mkdir(parents=True)
    (repo / "ttf").mkdir()
    (repo / "liber-primus__images--full" / "00.jpg").write_text("image", encoding="utf-8")
    (repo / "lp_outguessed" / "00.txt").write_text("payload", encoding="utf-8")
    (repo / "2014" / "05" / "3301 - Interconnectedness.mp3").write_text("audio", encoding="utf-8")
    (repo / "ttf" / "font.ttf").write_text("font", encoding="utf-8")
    subprocess.run(["git", "init"], cwd=repo, check=True, capture_output=True)
    subprocess.run(["git", "config", "user.email", "test@example.invalid"], cwd=repo, check=True)
    subprocess.run(["git", "config", "user.name", "Test"], cwd=repo, check=True)
    subprocess.run(["git", "add", "."], cwd=repo, check=True)
    subprocess.run(["git", "commit", "-m", "fixture"], cwd=repo, check=True, capture_output=True)
