from __future__ import annotations

import importlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PYTHON_PACKAGE = ROOT / "python" / "libreprimus"


def test_stage3x_cli_module_imports_without_circular_errors() -> None:
    module = importlib.import_module("libreprimus.cli")

    assert module.app is not None


def test_stage3x_cli_commands_package_exists_without_cli_package_conflict() -> None:
    assert (PYTHON_PACKAGE / "cli.py").is_file()
    assert not (PYTHON_PACKAGE / "cli").exists()
    assert (PYTHON_PACKAGE / "cli_commands").is_dir()


def test_stage3x_cli_entrypoint_is_thin() -> None:
    line_count = len((PYTHON_PACKAGE / "cli.py").read_text(encoding="utf-8").splitlines())

    assert line_count <= 800


def test_stage3x_domain_command_modules_exist() -> None:
    expected = {
        "root.py",
        "common.py",
        "legacy_workbook.py",
        "legacy_pastebin.py",
        "transcripts.py",
        "corpus_alignment.py",
        "profiles.py",
        "corpus_candidates.py",
        "solved_fixtures.py",
        "solved_baselines.py",
        "results.py",
        "consistency.py",
        "bounded.py",
        "archive_visual.py",
        "discord.py",
        "post_discord.py",
        "stego.py",
    }
    existing = {path.name for path in (PYTHON_PACKAGE / "cli_commands").glob("*.py")}

    assert expected <= existing


def test_stage3x_command_modules_import_without_raw_data_side_effects() -> None:
    modules = [
        "libreprimus.cli_commands.root",
        "libreprimus.cli_commands.consistency",
        "libreprimus.cli_commands.discord",
        "libreprimus.cli_commands.post_discord",
        "libreprimus.cli_commands.stego",
    ]

    for module_name in modules:
        importlib.import_module(module_name)
