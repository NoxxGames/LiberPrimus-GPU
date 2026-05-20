from __future__ import annotations

from pathlib import Path

import yaml

from libreprimus.cuda_build import smoke_build


def test_stage5c_smoke_build_default_does_not_execute(monkeypatch: object, tmp_path: Path) -> None:
    called = False

    def forbidden(_out_dir: Path) -> tuple[str, int | None, int | None]:
        nonlocal called
        called = True
        return ("failed", 1, None)

    monkeypatch.setattr(smoke_build, "_configure_and_build", forbidden)
    out = tmp_path / "smoke.yaml"

    records = smoke_build.run_smoke_build(smoke_build_out=out, out_dir=tmp_path / "out", attempt_build=False)
    payload = yaml.safe_load(out.read_text(encoding="utf-8"))

    assert records == payload["records"]
    assert called is False
    assert records[0]["smoke_build_status"] == "skipped_not_requested"
    assert records[0]["smoke_test_executed"] is False
    assert records[0]["gpu_benchmark_performed"] is False
