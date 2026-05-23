from __future__ import annotations

import subprocess


def _ignored(path: str) -> bool:
    return subprocess.run(["git", "check-ignore", "-q", path], check=False).returncode == 0


def test_stage5ae_generated_outputs_are_ignored() -> None:
    assert _ignored("experiments/results/prime-minus-one-bounded-p56-corrected-reporting/stage5ae/summary.json")
    assert _ignored("experiments/results/prime-minus-one-bounded-p56-corrected-reporting/stage5ae/corrected_formula_parity_report.json")
    assert _ignored("experiments/results/prime-minus-one-bounded-p56-corrected-reporting/stage5ae/reference_contract_repair_report.json")


def test_stage5ae_raw_and_codex_output_are_ignored() -> None:
    assert _ignored("data/raw/stage5ae-example.txt")
    assert _ignored("codex-output/stage5ae-codex-completion.md")
