"""Small Stage 5BD dry-run model helpers."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ManifestReference:
    """A manifest role/path pair from the active registry."""

    role: str
    path: str
    active: bool


@dataclass(frozen=True)
class DryRunPlan:
    """A metadata-only dry-run plan identifier."""

    run_plan_id: str
    variant_family_id: str
    input_digest: str


ManifestRole = str
ManifestRegistry = dict[str, object]
DryRunPlanIdPolicy = dict[str, object]
DryRunPlanIdRegistry = dict[str, object]
FutureResultPathPolicy = dict[str, object]
FutureResultPathValidation = dict[str, object]
BranchFamilyPlanCounter = dict[str, object]
NullControlPlanCounter = dict[str, object]
ControlFamilyPlanCounter = dict[str, object]
