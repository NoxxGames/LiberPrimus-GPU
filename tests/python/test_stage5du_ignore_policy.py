from __future__ import annotations

from test_stage5du_common import ensure_stage5du_built, git_check_ignore


def test_stage5du_local_raw_roots_and_completion_handoff_are_ignored() -> None:
    ensure_stage5du_built()
    ignored_paths = [
        "third_party/BigGapsFoundInLiberPrimus/messages.txt",
        "third_party/CribbingPage15/messages.txt",
        "third_party/Mobius_totient_first_page_theory/messages.txt",
        "third_party/PotentialCrib_RedRunes_Pages_54_55/messages.txt",
        "third_party/RedRunes_Possible_Koan_Connection/messages.txt",
        "third_party/StarArtifactsInLPPageImages/messages.txt",
        "codex-output/stage5du-codex-completion.md",
        "experiments/results/token-block/stage5du/summary.json",
    ]
    for path in ignored_paths:
        assert git_check_ignore(path)
