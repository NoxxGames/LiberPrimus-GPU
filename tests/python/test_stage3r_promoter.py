from __future__ import annotations

import json
from pathlib import Path

import yaml

from libreprimus.discord_lead_promotion.promoter import promote_discord_leads


def _write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload), encoding="utf-8")


def _write_jsonl(path: Path, records: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(json.dumps(record) for record in records) + "\n", encoding="utf-8")


def _write_yaml(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(payload), encoding="utf-8")


def test_stage3r_promotes_sources_and_observations(tmp_path: Path) -> None:
    review_dir = tmp_path / "review"
    _write_json(review_dir / "review_bundle_summary.json", {"review_lead_count": 3, "public_link_count": 2})
    _write_jsonl(
        review_dir / "source_links_index.jsonl",
        [{"public_links": ["https://github.com/rtkd/iddqd", "https://cdn.discordapp.com/attachments/1/2/x.png?token=1"]}],
    )
    _write_jsonl(review_dir / "method_claims_index.jsonl", [])
    _write_jsonl(review_dir / "numeric_observations_index.jsonl", [])
    _write_jsonl(review_dir / "visual_observations_index.jsonl", [])
    _write_jsonl(review_dir / "debunks_and_false_positives_index.jsonl", [{"lead_id": "d1"}])
    stage3o = {"records": []}
    stage3o_path = tmp_path / "stage3o.yaml"
    _write_yaml(stage3o_path, stage3o)
    source_registry = tmp_path / "sources.yaml"
    _write_yaml(source_registry, {"records": [{"source_url": "https://github.com/rtkd/iddqd"}]})
    visual_registry = tmp_path / "visual.yaml"
    cookie_records = tmp_path / "cookies.yaml"
    _write_yaml(visual_registry, {"records": []})
    _write_yaml(cookie_records, {"records": []})

    summary = promote_discord_leads(
        review_dir=review_dir,
        stage3o_links=stage3o_path,
        stage3o_methods=stage3o_path,
        stage3o_numerics=stage3o_path,
        source_registry=source_registry,
        visual_registry=visual_registry,
        cookie_records=cookie_records,
        out_dir=tmp_path / "out",
        promoted_sources_out=tmp_path / "sources-out.yaml",
        promoted_observations_out=tmp_path / "observations-out.yaml",
        negative_controls_out=tmp_path / "negative-out.yaml",
        audit_summary_out=tmp_path / "summary-out.yaml",
        allow_warnings=True,
    )

    assert summary["source_records_promoted"] == 13
    assert summary["observation_records_promoted"] == 11
    assert summary["negative_controls_created"] == 11
    assert summary["duplicate_records_skipped"] >= 1
    assert summary["unsafe_private_records_rejected"] >= 1
    observations = yaml.safe_load((tmp_path / "observations-out.yaml").read_text(encoding="utf-8"))["records"]
    cuneiform = [record for record in observations if "cuneiform" in record["observation_id"]][0]
    assert cuneiform["review_status"] == "review_required"
    assert cuneiform["usable_as_experiment_seed"] is False
    dots = [record for record in observations if "dot" in record["observation_id"]][0]
    assert dots["review_status"] == "review_required"
    assert "binary" in dots["ambiguity_notes"].lower()
