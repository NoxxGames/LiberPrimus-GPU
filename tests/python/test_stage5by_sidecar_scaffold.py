from test_stage5by_common import load_yaml


def test_stage5by_inactive_sidecar_scaffold_is_inactive() -> None:
    scaffold = load_yaml("data/token-block/stage5by-inactive-sidecar-planning-manifest-scaffold.yaml")
    assert scaffold["string4_inactive_sidecar_planning_manifest_scaffold_created"] is True
    assert scaffold["sidecar_status"] == "scaffolded_inactive"
    assert scaffold["sidecar_active"] is False
    assert scaffold["active_input"] is False
    assert scaffold["trusted_as_canonical"] is False


def test_stage5by_no_execution_planning_sidecar_is_inactive() -> None:
    sidecar = load_yaml("data/token-block/stage5by-no-execution-planning-ingestion-sidecar.yaml")
    assert sidecar["string4_no_execution_planning_ingestion_sidecar_created"] is True
    assert sidecar["planning_ingestion_sidecar_status"] == "inactive_no_execution"
    assert sidecar["planning_ingestion_performed"] is False
    assert sidecar["planning_ingestion_activated"] is False
