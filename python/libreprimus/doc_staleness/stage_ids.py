"""Dynamic stage identifier parsing and ordering."""

from __future__ import annotations

from dataclasses import dataclass
import re

STAGE_PATTERN = re.compile(r"\b(?:Stage|stage)[\s-]*(?P<number>\d+)(?P<suffix>[A-Za-z]+)?\b")


@dataclass(frozen=True, order=True)
class StageId:
    """Comparable stage identifier such as Stage 5Z or Stage 5AB."""

    number: int
    suffix_value: int
    suffix: str = ""

    @property
    def label(self) -> str:
        return f"Stage {self.number}{self.suffix}"

    @property
    def key(self) -> str:
        return f"stage-{self.number}{self.suffix.lower()}"


def parse_stage_id(text: str) -> StageId:
    """Parse the first stage identifier in ``text``."""

    match = STAGE_PATTERN.search(text)
    if not match:
        raise ValueError(f"No stage id found in {text!r}")
    suffix = (match.group("suffix") or "").upper()
    return StageId(
        number=int(match.group("number")),
        suffix_value=_suffix_to_int(suffix),
        suffix=suffix,
    )


def find_stage_ids(text: str) -> list[StageId]:
    """Return every stage identifier in deterministic order of appearance."""

    stages: list[StageId] = []
    for match in STAGE_PATTERN.finditer(text):
        suffix = (match.group("suffix") or "").upper()
        stages.append(
            StageId(
                number=int(match.group("number")),
                suffix_value=_suffix_to_int(suffix),
                suffix=suffix,
            )
        )
    return stages


def _suffix_to_int(suffix: str) -> int:
    if not suffix:
        return 0
    value = 0
    for char in suffix:
        if not ("A" <= char <= "Z"):
            raise ValueError(f"Invalid stage suffix {suffix!r}")
        value = value * 26 + (ord(char) - ord("A") + 1)
    return value
