"""Ignored-output policy consistency checks."""

from __future__ import annotations

import subprocess
from pathlib import Path

from libreprimus.consistency.models import ConsistencyCheckResult, fail_result, pass_result
from libreprimus.paths import repo_root

GROUP = "ignored_outputs"


def check_ignored_output_consistency(root: Path = repo_root()) -> list[ConsistencyCheckResult]:
    results: list[ConsistencyCheckResult] = []
    ignored_paths = [
        "data/raw/transcripts/rtkd/liber-primus__transcription--master.txt",
        "data/normalized/corpus-candidates/rtkd-master-v0-candidate/corpus_candidate_manifest.json",
        "experiments/results/solved-baselines/stage2a/summary.json",
        "experiments/results/result-store/stage2b/results.sqlite3",
        "experiments/results/consistency/stage2d/consistency_summary.json",
        "experiments/results/exploratory-dry-runs/stage2e/summary.json",
        "experiments/results/cpu-execution/stage2f/summary.json",
        "experiments/results/proposal-reviews/stage2g/summary.json",
        "experiments/results/approval-gated-execution/stage2h/summary.json",
        "experiments/results/approval-readiness/stage2i/summary.json",
        "experiments/results/bounded-auto-runs/stage2j/summary.json",
        "experiments/results/bounded-auto-runs/stage3a/candidate_records.jsonl",
        "experiments/results/bounded-auto-runs/stage3a/top_candidates.jsonl",
        "experiments/results/bounded-auto-runs/stage3a/summary.json",
        "experiments/results/bounded-auto-runs/stage3b/reranked_top_candidates.jsonl",
        "experiments/results/bounded-auto-runs/stage3b/rerank_summary.json",
        "experiments/results/bounded-auto-runs/stage3b/reverse_direction/candidate_records.jsonl",
        "experiments/results/bounded-auto-runs/stage3b/reverse_direction/top_candidates.jsonl",
        "experiments/results/bounded-auto-runs/stage3b/reverse_direction/summary.json",
        "experiments/results/scoring-calibration/stage3c/calibration_summary.json",
        "experiments/results/scoring-calibration/stage3c/null_control_scores.jsonl",
        "experiments/results/scoring-calibration/stage3c/stage3_candidates_calibrated.jsonl",
        "experiments/results/hash-preimage/stage3l/hash_candidate_records.jsonl",
        "experiments/results/hash-preimage/stage3l/exact_matches.jsonl",
        "experiments/results/hash-preimage/stage3l/summary.json",
        "experiments/results/image-analysis/stage3m/image_analysis_records.jsonl",
        "experiments/results/image-analysis/stage3m/visual_feature_candidates.jsonl",
        "experiments/results/image-analysis/stage3m/summary.json",
        "experiments/results/image-transforms/stage3p/review_index.html",
        "experiments/results/image-transforms/stage3p/transform_records.jsonl",
        "experiments/results/image-transforms/stage3p/visual_transform_candidates.jsonl",
        "experiments/results/image-transforms/stage3p/contact_sheets/example.jpg",
        "experiments/results/image-transforms/stage3p/derived_images/example/example.png",
        "experiments/results/discord-ingestion/stage3n/discord_extracted_links.jsonl",
        "experiments/results/discord-ingestion/stage3n/local_review_index.html",
        "experiments/results/discord-ingestion/stage3n/discord_ingestion_summary.json",
        "experiments/results/discord-promotion/stage3o/promotion_candidates.jsonl",
        "experiments/results/discord-promotion/stage3o/promotion_summary.json",
        "experiments/results/discord-review-bundles/stage3q/redacted_message_stream.jsonl",
        "experiments/results/discord-review-bundles/stage3q/topic_shards/source-links-and-datasets.md",
        "experiments/results/discord-review-bundles/stage3q/review_index.html",
        "experiments/results/wiki-sync/stage3o/wiki-sync-report.json",
        ".wiki-worktree/Home.md",
        "experiments/results/bounded-auto-runs/stage3d/candidate_records.jsonl",
        "experiments/results/bounded-auto-runs/stage3d/top_candidates.jsonl",
        "experiments/results/bounded-auto-runs/stage3d/summary.json",
        "experiments/results/bounded-auto-runs/stage3d/calibrated_scores.jsonl",
        "experiments/results/bounded-auto-runs/stage3e/stage3e_queue_dry_run_summary.json",
        "experiments/results/bounded-auto-runs/stage3f/candidate_records.jsonl",
        "experiments/results/bounded-auto-runs/stage3f/top_candidates.jsonl",
        "experiments/results/bounded-auto-runs/stage3f/summary.json",
        "experiments/results/bounded-auto-runs/stage3f/calibrated_scores.jsonl",
        "experiments/results/archive-visual-registry/stage3k/local-image-scan-summary.json",
        "third_party/LiberPrimusPages/example.jpg",
        "third_party/LiberPrimusPages/example.jpeg",
        "third_party/LiberPrimusPages/example.png",
        "third_party/LiberPrimusDiscordChats/example.html",
        "third_party/LiberPrimusDiscordChats/example.htm",
        "local-test.sqlite3",
    ]
    trackable_paths = [
        "data/profiles/gematria/gematria-primus-v0.json",
        "data/fixtures/solved-pages/direct-translation-v0/an-instruction-direct.fixture.json",
        "schemas/results/experiment-run-record-v0.schema.json",
        "schemas/experiments/exploratory-experiment-manifest-v0.schema.json",
        "schemas/experiments/cpu-execution-manifest-v0.schema.json",
        "schemas/experiments/experiment-proposal-v0.schema.json",
        "schemas/experiments/approval-gated-execution-request-v0.schema.json",
        "schemas/experiments/approval-readiness-packet-v0.schema.json",
        "schemas/experiments/operator-policy-v0.schema.json",
        "schemas/experiments/bounded-experiment-queue-v0.schema.json",
        "schemas/experiments/bounded-candidate-record-v0.schema.json",
        "schemas/experiments/method-backlog-v0.schema.json",
        "schemas/experiments/method-backlog-item-v0.schema.json",
        "schemas/experiments/stage3e-queue-item-v0.schema.json",
        "schemas/scoring/minimal-triage-score-v0.schema.json",
        "schemas/history/source-archive-record-v0.schema.json",
        "schemas/history/source-lock-record-v0.schema.json",
        "schemas/history/cookie-hash-record-v0.schema.json",
        "schemas/visual/image-artifact-record-v0.schema.json",
        "schemas/visual/visual-numeric-observation-v0.schema.json",
        "schemas/visual/visual-observation-reading-v0.schema.json",
        "schemas/visual/image-analysis-summary-v0.schema.json",
        "schemas/visual/image-analysis-record-v0.schema.json",
        "schemas/visual/image-threshold-summary-v0.schema.json",
        "schemas/visual/image-symmetry-record-v0.schema.json",
        "schemas/visual/image-bitplane-summary-v0.schema.json",
        "schemas/visual/image-component-summary-v0.schema.json",
        "schemas/visual/visual-feature-candidate-v0.schema.json",
        "schemas/visual/image-analysis-run-summary-v0.schema.json",
        "schemas/visual/image-transform-record-v0.schema.json",
        "schemas/visual/image-transform-metric-record-v0.schema.json",
        "schemas/visual/visual-transform-candidate-v0.schema.json",
        "schemas/visual/contact-sheet-record-v0.schema.json",
        "schemas/visual/image-transform-run-summary-v0.schema.json",
        "schemas/web/hash-preimage-candidate-pack-v0.schema.json",
        "schemas/web/hash-preimage-candidate-record-v0.schema.json",
        "schemas/web/hash-preimage-run-summary-v0.schema.json",
        "schemas/web/hash-preimage-match-record-v0.schema.json",
        "schemas/history/discord-archive-record-v0.schema.json",
        "schemas/history/discord-html-file-lock-v0.schema.json",
        "schemas/history/discord-extracted-link-v0.schema.json",
        "schemas/history/discord-attachment-candidate-v0.schema.json",
        "schemas/history/discord-method-claim-candidate-v0.schema.json",
        "schemas/history/discord-numeric-observation-candidate-v0.schema.json",
        "schemas/history/discord-ingestion-summary-v0.schema.json",
        "schemas/history/discord-redacted-message-record-v0.schema.json",
        "schemas/history/discord-topic-shard-record-v0.schema.json",
        "schemas/history/discord-review-lead-record-v0.schema.json",
        "schemas/history/discord-review-bundle-summary-v0.schema.json",
        "data/scoring/english-common-words-tiny-v0.txt",
        "data/scoring/english-impossible-bigrams-tiny-v0.txt",
        "data/scoring/cribs-tiny-v0.txt",
        "data/scoring/null-control-policy-v0.yaml",
        "data/observations/archive/source-archive-records-v0.yaml",
        "data/observations/visual/visual-numeric-observations-v0.yaml",
        "data/observations/visual/liber-primus-page-image-artifacts-v0.jsonl",
        "data/observations/web/cookie-hash-records-v0.yaml",
        "data/observations/web/hash-preimage-candidate-packs/hist-cookie-literal-pack-v1.yaml",
        "data/observations/web/hash-preimage-candidate-packs/hist-cookie-base29-numeric-pack-v1.yaml",
        "data/locks/third-party/liber-primus-pages/liber-primus-page-image-locks-v0.jsonl",
        "data/observations/discord/discord-ingestion-aggregate-summary-v0.yaml",
        "data/locks/third-party/discord-chats/discord-archive-summary-v0.yaml",
        "data/observations/discord/promoted-public-source-links-stage3o.yaml",
        "data/observations/discord/promoted-method-claim-candidates-stage3o.yaml",
        "data/observations/discord/promoted-numeric-observation-candidates-stage3o.yaml",
        "data/observations/discord/discord-review-bundle-aggregate-stage3q.yaml",
        "docs/wiki-source/Home.md",
        "docs/wiki-source/_Sidebar.md",
        "scripts/github/sync-tutorials-to-wiki.ps1",
        "scripts/github/validate-wiki-source.ps1",
        "experiments/manifests/solved-baselines/stage2a-all-known-solved-baselines.yaml",
        "experiments/manifests/exploratory/stage2e-caesar-preview-dry-run.yaml",
        "experiments/manifests/cpu-execution/stage2f-synthetic-direct-execution.yaml",
        "experiments/proposals/stage2g/stage2g-caesar-page-candidate-proposal.yaml",
        "experiments/proposals/stage2h/stage2h-approved-synthetic-direct-request.yaml",
        "experiments/proposals/stage2i/stage2i-first-bounded-caesar-affine-review.yaml",
        "experiments/policies/operator-policy-v0.yaml",
        "experiments/queues/stage2j-bounded-cpu-queue.yaml",
        "experiments/queues/stage3b-bounded-cpu-queue.yaml",
        "experiments/queues/stage3c-bounded-cpu-queue.yaml",
        "experiments/queues/stage3e-method-backlog.yaml",
        "experiments/queues/stage3e-bounded-cpu-queue.yaml",
    ]
    for path in ignored_paths:
        if _is_ignored(root, path):
            results.append(pass_result(GROUP, "path_ignored", f"Ignored path is ignored: {path}", path=path))
        else:
            results.append(fail_result(GROUP, "path_ignored", f"Expected ignored path is trackable: {path}", path=path))
    for path in trackable_paths:
        if _is_ignored(root, path):
            results.append(
                fail_result(GROUP, "path_trackable", f"Expected committed path is ignored: {path}", path=path)
            )
        else:
            results.append(pass_result(GROUP, "path_trackable", f"Committed path is trackable: {path}", path=path))
    return results


def _is_ignored(root: Path, path: str) -> bool:
    result = subprocess.run(
        ["git", "check-ignore", "-q", "--", path],
        cwd=root,
        check=False,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return result.returncode == 0
