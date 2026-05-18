from __future__ import annotations

import hashlib
import os
import stat
from pathlib import Path

import yaml

from libreprimus.stego.outguess_runner import run_outguess_regression


def test_stage3v_missing_tool_is_skipped(tmp_path: Path) -> None:
    artifacts, manifest = _write_fixture_files(tmp_path, expected_payload_sha256=None)

    summary = run_outguess_regression(
        manifest_path=manifest,
        artifacts_path=artifacts,
        out_dir=tmp_path / "out",
        outguess_path=tmp_path / "missing",
        allow_missing_tool=True,
        allow_missing_assets=True,
    )

    assert summary["attempted_count"] == 0
    assert summary["skipped_tool_missing_count"] == 1
    assert summary["solve_claim"] is False


def test_stage3v_missing_asset_is_skipped_with_fake_tool(tmp_path: Path) -> None:
    tool = _fake_outguess(tmp_path, payload=b"payload\n")
    artifacts, manifest = _write_fixture_files(tmp_path, local_path=tmp_path / "missing.jpg")

    summary = run_outguess_regression(
        manifest_path=manifest,
        artifacts_path=artifacts,
        out_dir=tmp_path / "out",
        outguess_path=tool,
        allow_missing_tool=True,
        allow_missing_assets=True,
    )

    assert summary["attempted_count"] == 0
    assert summary["skipped_asset_missing_count"] == 1


def test_stage3v_fake_outguess_expected_payload_match_passes(tmp_path: Path) -> None:
    payload = _fake_payload_bytes()
    tool = _fake_outguess(tmp_path, payload=payload)
    asset = tmp_path / "asset.jpg"
    asset.write_bytes(b"jpeg-ish")
    artifacts, manifest = _write_fixture_files(
        tmp_path,
        local_path=asset,
        expected_payload_sha256=hashlib.sha256(payload).hexdigest(),
    )

    summary = run_outguess_regression(
        manifest_path=manifest,
        artifacts_path=artifacts,
        out_dir=tmp_path / "out",
        outguess_path=tool,
    )

    assert summary["attempted_count"] == 1
    assert summary["passed_count"] == 1
    assert summary["failed_count"] == 0


def test_stage3v_fake_outguess_expected_payload_mismatch_fails(tmp_path: Path) -> None:
    tool = _fake_outguess(tmp_path, payload=_fake_payload_bytes())
    asset = tmp_path / "asset.jpg"
    asset.write_bytes(b"jpeg-ish")
    artifacts, manifest = _write_fixture_files(tmp_path, local_path=asset, expected_payload_sha256="0" * 64)

    summary = run_outguess_regression(
        manifest_path=manifest,
        artifacts_path=artifacts,
        out_dir=tmp_path / "out",
        outguess_path=tool,
    )

    assert summary["attempted_count"] == 1
    assert summary["failed_count"] == 1


def test_stage3v_fake_outguess_failure_records_extraction_error(tmp_path: Path) -> None:
    tool = _fake_outguess(tmp_path, payload=b"", fail=True)
    asset = tmp_path / "asset.jpg"
    asset.write_bytes(b"jpeg-ish")
    artifacts, manifest = _write_fixture_files(tmp_path, local_path=asset)

    summary = run_outguess_regression(
        manifest_path=manifest,
        artifacts_path=artifacts,
        out_dir=tmp_path / "out",
        outguess_path=tool,
    )

    assert summary["attempted_count"] == 1
    assert summary["extraction_error_count"] == 1


def _write_fixture_files(
    tmp_path: Path,
    *,
    local_path: Path | None = None,
    expected_payload_sha256: str | None = None,
) -> tuple[Path, Path]:
    asset_path = local_path or (tmp_path / "asset.jpg")
    if local_path is None:
        asset_path.write_bytes(b"jpeg-ish")
    artifacts = tmp_path / "artifacts.yaml"
    manifest = tmp_path / "manifest.yaml"
    artifact_record = {
        "record_type": "stego_artifact_record",
        "artifact_id": "artifact",
        "source_class": "synthetic_control",
        "source_url": None,
        "local_path": str(asset_path),
        "local_path_status": "present",
        "file_name": asset_path.name,
        "file_size_bytes": asset_path.stat().st_size if asset_path.exists() else None,
        "sha256": None,
        "media_type": "image/jpeg",
        "expected_role": "known_positive",
        "expected_payload_sha256": expected_payload_sha256,
        "expected_payload_text_sha256": None,
        "extraction_tool": "outguess",
        "trusted_as_canonical": False,
        "solve_claim": False,
        "notes": "fixture",
    }
    artifacts.write_text(yaml.safe_dump({"records": [artifact_record]}, sort_keys=False), encoding="utf-8")
    manifest.write_text(
        yaml.safe_dump(
            {
                "record_type": "outguess_regression_manifest",
                "manifest_id": "fixture",
                "description": "fixture",
                "tool_required": True,
                "allow_missing_tool": True,
                "allow_missing_assets": True,
                "cases": [
                    {
                        "case_id": "case",
                        "artifact_id": "artifact",
                        "enabled": True,
                        "expected_role": "known_positive",
                    }
                ],
                "expected_case_count_upper_bound": 1,
                "cpu_only": True,
                "cuda_enabled": False,
                "no_solve_claim": True,
                "generated_outputs_committed": False,
                "notes": "fixture",
            },
            sort_keys=False,
        ),
        encoding="utf-8",
    )
    return artifacts, manifest


def _fake_payload_bytes() -> bytes:
    return b"fake-payload\r\n" if os.name == "nt" else b"fake-payload\n"


def _fake_outguess(tmp_path: Path, *, payload: bytes, fail: bool = False) -> Path:
    if os.name == "nt":
        script = tmp_path / "outguess.cmd"
        if fail:
            script.write_text("@echo off\r\nif \"%1\"==\"--help\" (echo fake& exit /b 0)\r\nexit /b 7\r\n", encoding="utf-8")
        else:
            script.write_text(
                "@echo off\r\n"
                "if \"%1\"==\"--help\" (echo fake& exit /b 0)\r\n"
                "if \"%1\"==\"-h\" (echo fake& exit /b 0)\r\n"
                "if \"%1\"==\"-r\" (echo fake-payload> \"%3\"& exit /b 0)\r\n"
                "exit /b 2\r\n",
                encoding="utf-8",
            )
        return script
    script = tmp_path / "outguess"
    if fail:
        script.write_text("#!/usr/bin/env sh\n[ \"$1\" = \"--help\" ] && { echo fake; exit 0; }\nexit 7\n", encoding="utf-8")
    else:
        script.write_text(
            "#!/usr/bin/env sh\n"
            "[ \"$1\" = \"--help\" ] && { echo fake; exit 0; }\n"
            "[ \"$1\" = \"-h\" ] && { echo fake; exit 0; }\n"
            "if [ \"$1\" = \"-r\" ]; then printf 'fake-payload\\n' > \"$3\"; exit 0; fi\n"
            "exit 2\n",
            encoding="utf-8",
        )
    script.chmod(script.stat().st_mode | stat.S_IXUSR)
    assert payload in {b"", b"fake-payload\n", b"fake-payload\r\n"}
    return script
