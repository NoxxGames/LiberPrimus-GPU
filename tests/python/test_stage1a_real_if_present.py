import subprocess
from pathlib import Path

import pytest

from libreprimus.solved_fixtures.fixture_loader import load_fixtures
from libreprimus.solved_fixtures.validation import validate_fixture_dir, validate_reproduction_results


REAL_READY = all(
    Path(path).exists()
    for path in [
        "data/raw/transcripts/rtkd/liber-primus__transcription--master.txt",
        "data/raw/transcripts/scream314/liber_primus.md",
        "data/profiles/gematria/gematria-primus-v0.json",
        "data/profiles/separators/rtkd-separator-grammar-v0.json",
        "data/profiles/glyph-variants/glyph-variants-v0.json",
    ]
)


@pytest.mark.skipif(not REAL_READY, reason="real Stage 1A sources absent")
def test_real_stage1a_smoke_outputs_are_noncanonical() -> None:
    subprocess.run(
        [
            ".\\.venv\\Scripts\\python.exe",
            "-m",
            "libreprimus.cli",
            "solved-fixture",
            "stage1a-smoke",
            "--fixture-dir",
            "data/fixtures/solved-pages/direct-translation-v0",
            "--candidate-dir",
            "data/normalized/corpus-candidates/rtkd-master-v0-candidate",
            "--out-dir",
            "data/normalized/solved-baselines/direct-translation-v0",
            "--allow-pending",
            "--allow-warnings",
        ],
        check=True,
    )

    assert validate_fixture_dir(Path("data/fixtures/solved-pages/direct-translation-v0")) == []
    assert validate_reproduction_results(
        Path("data/normalized/solved-baselines/direct-translation-v0"), allow_warnings=True
    ) == []
    fixtures = load_fixtures(Path("data/fixtures/solved-pages/direct-translation-v0"))
    assert {fixture.fixture_id for fixture in fixtures} >= {"p57-parable"}
    assert all(fixture.trusted_as_canonical is False for fixture in fixtures)
