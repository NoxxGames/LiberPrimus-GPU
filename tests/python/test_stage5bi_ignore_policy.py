import subprocess


def _git(*args: str) -> str:
    return subprocess.check_output(["git", *args], text=True).strip()


def test_stage5bi_raw_and_generated_paths_not_staged() -> None:
    staged = set(_git("diff", "--cached", "--name-only").splitlines())
    forbidden_prefixes = (
        "third_party/CicadaSolversIddqd/",
        "third_party/SourceSnapshots/",
        "third_party/3N_3p_Bases_49-51.jpg.xlsx",
        "data/raw/",
        "experiments/results/",
    )

    assert not any(path.startswith(forbidden_prefixes) for path in staged)


def test_stage5bi_spreadsheet_and_archive_raw_files_are_not_tracked() -> None:
    tracked_spreadsheet = _git("ls-files", "third_party/3N_3p_Bases_49-51.jpg.xlsx")
    tracked_archive = _git("ls-files", "third_party/CicadaSolversIddqd")

    assert tracked_spreadsheet == ""
    assert "third_party/CicadaSolversIddqd/README.md" in tracked_archive
    assert "third_party/CicadaSolversIddqd/.gitkeep" in tracked_archive
    assert "third_party/CicadaSolversIddqd/2014/" not in tracked_archive
