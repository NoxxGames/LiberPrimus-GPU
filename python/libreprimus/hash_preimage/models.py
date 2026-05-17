"""Typed records for bounded hash-preimage runs."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CookieTarget:
    cookie_id: str
    cookie_name: str
    cookie_value: str


@dataclass(frozen=True)
class CandidateText:
    pack_id: str
    candidate_group: str
    source_literal: str
    literal_text: str
    byte_variant: str
    encoding: str = "utf-8"


@dataclass(frozen=True)
class ExpandedPack:
    pack_id: str
    algorithm: str
    candidates: list[CandidateText]
    total_generated_before_dedup: int
    duplicate_count: int
    candidate_count_upper_bound: int
