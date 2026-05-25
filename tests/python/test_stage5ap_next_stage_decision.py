from __future__ import annotations

from pathlib import Path

from PIL import Image

from libreprimus.stego_controls.outguess_controls import build_guardrail, build_positive_control_matrix
from libreprimus.stego_controls.outguess_fixtures import build_historical_fixture_readiness
from libreprimus.stego_controls.outguess_toolchain import detect_outguess_toolchain
from libreprimus.token_block.alphabets import build_alphabet_registry
from libreprimus.token_block.coordinates import build_coordinate_records
from libreprimus.token_block.dwh_context import build_dwh_context
from libreprimus.token_block.mapping import build_mapping_preflight
from libreprimus.token_block.null_controls import build_null_control_plan
from libreprimus.token_block.provenance import build_source_lock
from libreprimus.token_block.stage5ap import build_next_stage_decision, build_research_summary, build_summary
from libreprimus.token_block.transcription import build_transcription


def test_stage5ap_next_stage_selects_deep_research_when_source_lock_ready(tmp_path: Path) -> None:
    image_root = tmp_path / "pages"
    image_root.mkdir()
    for page in ("49", "50", "51"):
        Image.new("RGB", (3, 2), "white").save(image_root / f"{page}.jpg")
    source = tmp_path / "source.yaml"
    provenance = tmp_path / "provenance.yaml"
    transcription = tmp_path / "transcription.yaml"
    coordinates = tmp_path / "coordinates.yaml"
    alphabet = tmp_path / "alphabet.yaml"
    mapping = tmp_path / "mapping.yaml"
    nulls = tmp_path / "nulls.yaml"
    dwh = tmp_path / "dwh.yaml"
    toolchain = tmp_path / "toolchain.yaml"
    matrix = tmp_path / "matrix.yaml"
    historical = tmp_path / "historical.yaml"
    guardrail = tmp_path / "guardrail.yaml"
    research = tmp_path / "research.yaml"
    decision = tmp_path / "decision.yaml"
    summary = tmp_path / "summary.yaml"
    build_source_lock(search_roots=[image_root], out_source_lock=source, out_image_provenance=provenance)
    build_transcription(out=transcription)
    build_coordinate_records(transcription=transcription, out=coordinates)
    build_alphabet_registry(transcription=transcription, out=alphabet)
    build_mapping_preflight(transcription=transcription, alphabet_registry=alphabet, out=mapping)
    build_null_control_plan(out=nulls)
    build_dwh_context(out=dwh)
    detect_outguess_toolchain(out=toolchain)
    build_positive_control_matrix(toolchain=toolchain, out=matrix, results_dir=None)
    build_historical_fixture_readiness(out=historical, results_dir=None)
    build_guardrail(out=guardrail)
    build_research_summary(source_lock=source, transcription=transcription, alphabet_registry=alphabet, mapping_preflight=mapping, dwh_context=dwh, out=research)
    next_record = build_next_stage_decision(source_lock=source, transcription=transcription, mapping_preflight=mapping, out=decision)
    final = build_summary(
        source_lock=source,
        image_provenance=provenance,
        transcription=transcription,
        coordinates=coordinates,
        alphabet_registry=alphabet,
        mapping_preflight=mapping,
        null_control_plan=nulls,
        dwh_context=dwh,
        outguess_toolchain=toolchain,
        outguess_matrix=matrix,
        outguess_historical=historical,
        outguess_guardrail=guardrail,
        research_summary=research,
        next_stage_decision=decision,
        out=summary,
    )
    assert next_record["deep_research_next_ready"] is True
    assert final["selected_next_stage_title"].startswith("Stage 5AQ")
