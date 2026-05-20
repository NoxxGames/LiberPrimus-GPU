#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$repo_root"

python_bin="${PYTHON:-python}"
tmp_dir="$(mktemp -d)"
trap 'rm -rf "$tmp_dir"' EXIT

echo "Running full consistency suite"
"$python_bin" -m libreprimus.cli consistency check-all --allow-warnings

echo "Running state-drift consistency checks"
"$python_bin" -m libreprimus.cli consistency check-state-drift

echo "Validating Stage 3Y research synthesis records"
"$python_bin" -m libreprimus.cli research-synthesis validate --data-dir data/research --staged-plan docs/roadmap/staged-plan.md

echo "Validating Stage 4B source-lock triage records"
"$python_bin" -m libreprimus.cli source-lock-triage validate \
    --promoted-sources data/observations/archive/stage4b-promoted-source-records.yaml \
    --source-health data/locks/third-party/stage4b-source-health-records.yaml \
    --visual-observations data/observations/visual/stage4b-visual-observation-records.yaml \
    --negative-controls data/observations/research/stage4b-negative-control-records.yaml \
    --cookie-source-records data/observations/web/stage4b-cookie-candidate-source-records.yaml \
    --manifest-dir experiments/manifests/stage4b-disabled

echo "Validating Stage 4C visual annotation records"
"$python_bin" -m libreprimus.cli visual-annotation validate \
    --task data/observations/visual/stage4c-visual-annotation-tasks.yaml \
    --cuneiform data/observations/visual/stage4c-cuneiform-reading-candidates.yaml \
    --dot data/observations/visual/stage4c-dot-pattern-annotation-tasks.yaml \
    --delimiter data/observations/visual/stage4c-delimiter-annotation-tasks.yaml \
    --negative data/observations/visual/stage4c-visual-negative-control-annotation-tasks.yaml \
    --summary data/observations/visual/stage4c-annotation-pack-summary.yaml

echo "Running Stage 4D bounded numeric verifier synthetic/temp output"
"$python_bin" -m libreprimus.cli bounded-numeric run \
    --manifest-dir experiments/manifests/stage4b-disabled \
    --stage4b-visual data/observations/visual/stage4b-visual-observation-records.yaml \
    --stage4c-tasks data/observations/visual/stage4c-visual-annotation-tasks.yaml \
    --stage4c-cuneiform data/observations/visual/stage4c-cuneiform-reading-candidates.yaml \
    --stage4c-dot data/observations/visual/stage4c-dot-pattern-annotation-tasks.yaml \
    --stage4c-delimiter data/observations/visual/stage4c-delimiter-annotation-tasks.yaml \
    --stage4c-negative data/observations/visual/stage4c-visual-negative-control-annotation-tasks.yaml \
    --out-dir "$tmp_dir/stage4d-bounded-numeric" \
    --allow-warnings
"$python_bin" -m libreprimus.cli bounded-numeric validate --results-dir "$tmp_dir/stage4d-bounded-numeric"

echo "Validating Stage 4E source-delta audit records"
"$python_bin" -m libreprimus.cli source-delta-audit validate \
    --source-delta data/observations/archive/stage4e-cicada-solvers-iddqd-source-delta.yaml \
    --source-health data/locks/third-party/stage4e-cicada-solvers-iddqd-source-health.yaml \
    --image-artifact data/observations/visual/stage4e-image-compression-artifact-observations.yaml \
    --manifest-dir experiments/manifests/stage4e-disabled

echo "Validating Stage 4F stego/audio fixture records"
"$python_bin" -m libreprimus.cli stego-fixtures validate \
    --outguess-fixtures data/observations/stego/stage4f-outguess-fixture-source-records.yaml \
    --audio-fixtures data/observations/stego/stage4f-audio-fixture-source-records.yaml \
    --source-health data/locks/third-party/stage4f-stego-fixture-source-health.yaml \
    --toolchain data/observations/stego/stage4f-toolchain-requirements.yaml \
    --manifest-dir experiments/manifests/stego/stage4f-disabled

echo "Running Stage 4G cookie refresh synthetic/temp output"
"$python_bin" -m libreprimus.cli cookie-refresh run \
    --manifest experiments/manifests/stage4b-disabled/exp_stage4b_cookie_pack_v2.yaml \
    --candidate-sources data/observations/web/stage4b-cookie-candidate-source-records.yaml \
    --cookie-targets data/observations/web/cookie-hash-records-v0.yaml \
    --out-dir "$tmp_dir/stage4g-cookie-refresh" \
    --summary-out "$tmp_dir/stage4g-cookie-refresh-summary.yaml" \
    --allow-warnings
"$python_bin" -m libreprimus.cli cookie-refresh validate --results-dir "$tmp_dir/stage4g-cookie-refresh" --summary "$tmp_dir/stage4g-cookie-refresh-summary.yaml"

echo "Running Stage 4H CPU batch synthetic/temp output"
"$python_bin" -m libreprimus.cli cpu-batch validate-manifest \
    --manifest experiments/manifests/cpu-batch/stage4h-synthetic-smoke-batch.yaml
"$python_bin" -m libreprimus.cli cpu-batch run \
    --manifest experiments/manifests/cpu-batch/stage4h-synthetic-smoke-batch.yaml \
    --out-dir "$tmp_dir/stage4h-cpu-batch" \
    --allow-warnings
"$python_bin" -m libreprimus.cli cpu-batch adapter-coverage \
    --registry data/transform-registry/cpu-reference-transforms-v0.json \
    --out-dir "$tmp_dir/stage4h-cpu-batch" \
    --allow-warnings
"$python_bin" -m libreprimus.cli cpu-batch validate-results --results-dir "$tmp_dir/stage4h-cpu-batch"

echo "Validating Stage 4I scoring consolidation records"
"$python_bin" -m libreprimus.cli scoring consolidate \
    --out-dir "$tmp_dir/stage4i-scoring" \
    --data-dir "$tmp_dir/stage4i-scoring-data" \
    --allow-warnings
"$python_bin" -m libreprimus.cli scoring validate --data-dir data/scoring
"$python_bin" -m libreprimus.cli scoring check-cpu-batch-compatibility \
    --cpu-batch-summary data/research/stage4h-cpu-batch-api-summary.yaml \
    --data-dir data/scoring \
    --allow-warnings

echo "Validating Stage 4J observation review workflow records"
"$python_bin" -m libreprimus.cli observation-review validate \
    --policy data/observations/review/stage4j-observation-review-policy.yaml \
    --decisions data/observations/review/stage4j-observation-review-decisions.yaml \
    --promotions data/observations/review/stage4j-observation-promotion-records.yaml \
    --quarantine data/observations/review/stage4j-observation-quarantine-records.yaml \
    --summary data/observations/review/stage4j-observation-review-summary.yaml
"$python_bin" -m libreprimus.cli observation-review check-paths --repo-root .

echo "Validating Stage 4K source-lock snapshot records"
"$python_bin" -m libreprimus.cli source-lock-snapshots validate \
    --snapshot-records data/locks/third-party/source-snapshots/stage4k-source-lock-snapshot-records.yaml \
    --fetch-records data/locks/third-party/source-snapshots/stage4k-source-fetch-records.yaml \
    --copyright-records data/locks/third-party/source-snapshots/stage4k-source-copyright-policy-records.yaml \
    --summary data/locks/third-party/source-snapshots/stage4k-source-lock-summary.yaml

echo "Validating Stage 4L observation promotion records"
"$python_bin" -m libreprimus.cli observation-promotion validate \
    --ledger data/observations/review/stage4l-reviewed-observation-promotion-ledger.yaml \
    --readiness data/observations/review/stage4l-observation-promotion-readiness-records.yaml \
    --blockers data/observations/review/stage4l-observation-promotion-blocker-records.yaml \
    --manifest-readiness data/observations/review/stage4l-manifest-readiness-records.yaml \
    --summary data/observations/review/stage4l-reviewed-observation-promotion-summary.yaml

echo "Validating Stage 4M image preflight records"
"$python_bin" -m libreprimus.cli image-preflight validate \
    --source-variant data/observations/visual/stage4m-image-source-variant-preflight-records.yaml \
    --compression data/observations/visual/stage4m-image-compression-preflight-records.yaml \
    --artifact-candidates data/observations/visual/stage4m-image-artifact-review-candidates.yaml \
    --summary data/observations/visual/stage4m-image-preflight-summary.yaml \
    --bigram-readiness data/observations/review/stage4m-bigram-frequency-pattern-readiness.yaml

echo "Validating Stage 4N stego/audio positive-control records"
"$python_bin" -m libreprimus.cli stego-positive-controls validate \
    --outguess-readiness data/observations/stego/stage4n-outguess-positive-control-readiness.yaml \
    --audio-readiness data/observations/stego/stage4n-audio-positive-control-readiness.yaml \
    --fixture-cache data/observations/stego/stage4n-fixture-cache-records.yaml \
    --expected-output data/observations/stego/stage4n-expected-output-records.yaml \
    --toolchain data/observations/stego/stage4n-toolchain-readiness.yaml \
    --summary data/observations/stego/stage4n-positive-control-summary.yaml

echo "Running Stage 4O CPU batch adapter expansion synthetic/temp output"
"$python_bin" -m libreprimus.cli cpu-batch solved-fixture-parity \
    --manifest experiments/manifests/cpu-batch/stage4o-solved-fixture-parity-batch.yaml \
    --out-dir "$tmp_dir/stage4o-cpu-batch" \
    --allow-warnings
"$python_bin" -m libreprimus.cli cpu-batch adapter-expansion \
    --manifest experiments/manifests/cpu-batch/stage4o-adapter-expansion-smoke-batch.yaml \
    --registry data/transform-registry/cpu-reference-transforms-v0.json \
    --out-dir "$tmp_dir/stage4o-cpu-batch" \
    --allow-warnings
"$python_bin" -m libreprimus.cli cpu-batch parity-readiness \
    --manifest experiments/manifests/cpu-batch/stage4o-cpu-cuda-parity-readiness.yaml \
    --out-dir "$tmp_dir/stage4o-cpu-batch" \
    --summary-out "$tmp_dir/stage4o-cpu-batch-summary.yaml" \
    --allow-warnings
"$python_bin" -m libreprimus.cli cpu-batch validate-stage4o \
    --results-dir "$tmp_dir/stage4o-cpu-batch" \
    --summary "$tmp_dir/stage4o-cpu-batch-summary.yaml"

echo "Running Stage 4P result-store unification synthetic/temp output"
"$python_bin" -m libreprimus.cli result-store build-source-inventory \
    --manifest experiments/manifests/result-store/stage4p-result-source-inventory.yaml \
    --out-dir "$tmp_dir/stage4p-result-store-unification" \
    --allow-warnings
"$python_bin" -m libreprimus.cli result-store unify-score-summaries \
    --manifest experiments/manifests/result-store/stage4p-score-summary-unification.yaml \
    --out-dir "$tmp_dir/stage4p-result-store-unification" \
    --allow-warnings
"$python_bin" -m libreprimus.cli result-store build-cross-stage-report \
    --manifest experiments/manifests/result-store/stage4p-cross-stage-report.yaml \
    --out-dir "$tmp_dir/stage4p-result-store-unification" \
    --summary-out "$tmp_dir/stage4p-result-store-score-summary-unification-summary.yaml" \
    --allow-warnings
"$python_bin" -m libreprimus.cli result-store validate-stage4p \
    --results-dir "$tmp_dir/stage4p-result-store-unification" \
    --summary "$tmp_dir/stage4p-result-store-score-summary-unification-summary.yaml"

echo "Running Stage 4Q benchmark planning synthetic/temp output"
"$python_bin" -m libreprimus.cli benchmark-planning environment \
    --manifest experiments/manifests/benchmarks/stage4q-benchmark-environment.yaml \
    --out-dir "$tmp_dir/stage4q-benchmark-planning" \
    --allow-warnings
"$python_bin" -m libreprimus.cli benchmark-planning cpu-smoke \
    --manifest experiments/manifests/benchmarks/stage4q-cpu-benchmark-smoke.yaml \
    --out-dir "$tmp_dir/stage4q-benchmark-planning" \
    --allow-warnings
"$python_bin" -m libreprimus.cli benchmark-planning build-plan \
    --manifest experiments/manifests/benchmarks/stage4q-cuda-parity-readiness.yaml \
    --plan-out "$tmp_dir/stage4q-cpu-benchmark-plan.yaml" \
    --readiness-out "$tmp_dir/stage4q-cuda-parity-readiness.yaml" \
    --summary-out "$tmp_dir/stage4q-cpu-benchmark-parity-planning-summary.yaml" \
    --out-dir "$tmp_dir/stage4q-benchmark-planning" \
    --allow-warnings
"$python_bin" -m libreprimus.cli benchmark-planning validate-stage4q \
    --results-dir "$tmp_dir/stage4q-benchmark-planning" \
    --plan "$tmp_dir/stage4q-cpu-benchmark-plan.yaml" \
    --readiness "$tmp_dir/stage4q-cuda-parity-readiness.yaml" \
    --summary "$tmp_dir/stage4q-cpu-benchmark-parity-planning-summary.yaml"

echo "Running result-store consistency suite"
"$python_bin" -m libreprimus.cli consistency check-result-store --allow-missing-generated --allow-warnings

echo "Exporting consistency summary to temp"
"$python_bin" -m libreprimus.cli consistency check-all --out "$tmp_dir/consistency_summary.json" --allow-warnings

echo "Validating Stage 3K archive and observation registries"
"$python_bin" -m libreprimus.cli archive validate-sources --records data/observations/archive/source-archive-records-v0.yaml
"$python_bin" -m libreprimus.cli archive validate-image-locks --locks data/locks/third-party/liber-primus-pages/liber-primus-page-image-locks-v0.jsonl --artifacts data/observations/visual/liber-primus-page-image-artifacts-v0.jsonl --allow-empty
"$python_bin" -m libreprimus.cli observation validate-visual --records data/observations/visual/visual-numeric-observations-v0.yaml
"$python_bin" -m libreprimus.cli observation validate-cookies --records data/observations/web/cookie-hash-records-v0.yaml

echo "Validating Stage 3L hash preimage candidate packs"
"$python_bin" -m libreprimus.cli hash-preimage validate-packs --pack-dir data/observations/web/hash-preimage-candidate-packs

echo "Validating Stage 3M deterministic image-analysis raw-data-free mode"
"$python_bin" -m libreprimus.cli image-analysis validate-results --results-dir "$tmp_dir/stage3m-image-analysis" --allow-missing

echo "Validating Stage 3P deterministic image-transform raw-data-free mode"
"$python_bin" -m libreprimus.cli image-transform validate-results --results-dir "$tmp_dir/stage3p-image-transforms" --allow-missing

echo "Validating Stage 3N Discord ingestion raw-log-free mode"
"$python_bin" -m libreprimus.cli discord-ingest scan --source-dir "$tmp_dir/missing-discord" --out-dir "$tmp_dir/stage3n-discord" --allow-missing --allow-warnings
"$python_bin" -m libreprimus.cli discord-ingest validate-results --results-dir "$tmp_dir/stage3n-discord" --allow-missing

echo "Validating Stage 3O Discord promotion and Wiki mirror"
"$python_bin" -m libreprimus.cli discord-promote validate-promoted --links data/observations/discord/promoted-public-source-links-stage3o.yaml --methods data/observations/discord/promoted-method-claim-candidates-stage3o.yaml --numerics data/observations/discord/promoted-numeric-observation-candidates-stage3o.yaml --allow-empty
bash scripts/github/validate-wiki-source.sh

echo "Validating Stage 3Q Discord review-bundle raw-log-free mode"
"$python_bin" -m libreprimus.cli discord-review build-bundles --ingestion-dir "$tmp_dir/missing-stage3n" --promotion-dir "$tmp_dir/missing-stage3o" --raw-dir "$tmp_dir/missing-discord" --out-dir "$tmp_dir/stage3q-discord-review" --aggregate-out "$tmp_dir/stage3q-discord-review-aggregate.yaml" --allow-missing --allow-warnings
"$python_bin" -m libreprimus.cli discord-review validate-bundles --results-dir "$tmp_dir/stage3q-discord-review" --aggregate "$tmp_dir/stage3q-discord-review-aggregate.yaml" --allow-missing

echo "Validating Stage 4A Discord full-review synthetic build"
mkdir -p "$tmp_dir/stage4a-discord" "$tmp_dir/stage4a-pages"
"$python_bin" - <<PY
from pathlib import Path
from PIL import Image
discord = Path("$tmp_dir/stage4a-discord")
pages = Path("$tmp_dir/stage4a-pages")
(discord / "CicadaSolvers - Cicada - ci-test [123456789012345678].html").write_text(
    '<div class="chatlog__message"><span class="chatlog__author-name">User</span>'
    '<div class="chatlog__content">cuneiform base60 onion 7 https://example.org/source '
    'https://cdn.discordapp.com/attachments/1/2/test.png?secret=1</div></div>',
    encoding="utf-8",
)
Image.new("RGB", (32, 32), "white").save(pages / "page001.jpg")
PY
"$python_bin" -m libreprimus.cli discord-full-review build --discord-dir "$tmp_dir/stage4a-discord" --lp-pages-dir "$tmp_dir/stage4a-pages" --out-dir "$tmp_dir/stage4a-full-review" --privacy-mode redacted_public --include-lp-page-gallery --allow-warnings
"$python_bin" -m libreprimus.cli discord-full-review validate --results-dir "$tmp_dir/stage4a-full-review"

echo "Validating Stage 3R Discord lead promotion records and disabled manifests"
"$python_bin" -m libreprimus.cli discord-leads validate --promoted-sources data/observations/discord/stage3r-promoted-source-records.yaml --promoted-observations data/observations/discord/stage3r-promoted-observation-records.yaml --negative-controls data/observations/discord/stage3r-negative-control-records.yaml --manifest-dir experiments/manifests/post-discord --allow-empty

echo "Validating Stage 3S post-Discord Onion 7 manifest"
"$python_bin" -m libreprimus.cli post-discord validate-manifest --manifest experiments/manifests/post-discord/EXP-3R-003-onion7-raw-prime-order-seed-pack-a.yaml

echo "Validating Stage 3T GP/rune claim verifier manifest"
"$python_bin" -m libreprimus.cli post-discord validate-gp-rune-manifest --manifest experiments/manifests/post-discord/EXP-3R-004-gp-rune-claim-verifier-a.yaml

echo "Validating Stage 3U cookie signed-variant manifest"
"$python_bin" -m libreprimus.cli post-discord validate-cookie-manifest --manifest experiments/manifests/post-discord/EXP-3R-001-cookie-sha256-signed-variants-a.yaml

echo "Validating Stage 3V OutGuess regression manifest and missing-tool-safe detection"
"$python_bin" -m libreprimus.cli stego outguess-validate-manifest --manifest experiments/manifests/stego/outguess-regression-v1.yaml --artifacts data/observations/stego/outguess-artifacts-v0.yaml
"$python_bin" -m libreprimus.cli stego outguess-detect --out-dir "$tmp_dir/stage3v-outguess" --allow-missing-tool

echo "Validating Stage 2E exploratory manifests"
"$python_bin" -m libreprimus.cli experiment validate-exploratory --manifest experiments/manifests/exploratory/stage2e-caesar-preview-dry-run.yaml
"$python_bin" -m libreprimus.cli experiment validate-exploratory --manifest experiments/manifests/exploratory/stage2e-affine-preview-dry-run.yaml

echo "Dry-running Stage 2E Caesar preview to temp"
"$python_bin" -m libreprimus.cli experiment dry-run --manifest experiments/manifests/exploratory/stage2e-caesar-preview-dry-run.yaml --out-dir "$tmp_dir/stage2e-dry-run" --allow-warnings

echo "Validating Stage 2F CPU execution manifests"
"$python_bin" -m libreprimus.cli execution validate --manifest experiments/manifests/cpu-execution/stage2f-synthetic-direct-execution.yaml
"$python_bin" -m libreprimus.cli execution validate --manifest experiments/manifests/cpu-execution/stage2f-solved-baseline-replay.yaml

echo "Running Stage 2F synthetic direct execution"
"$python_bin" -m libreprimus.cli execution run --manifest experiments/manifests/cpu-execution/stage2f-synthetic-direct-execution.yaml --out-dir experiments/results/cpu-execution/stage2f --allow-warnings

echo "Validating Stage 2G proposals and approval gates"
"$python_bin" -m libreprimus.cli proposal validate --proposal experiments/proposals/stage2g/stage2g-caesar-page-candidate-proposal.yaml
"$python_bin" -m libreprimus.cli proposal check-approval --proposal experiments/proposals/stage2g/stage2g-caesar-page-candidate-proposal.yaml --approval experiments/proposals/stage2g/approval-records/stage2g-example-pending-approval.yaml

echo "Generating Stage 2G review packet to temp"
"$python_bin" -m libreprimus.cli proposal review-packet --proposal experiments/proposals/stage2g/stage2g-caesar-page-candidate-proposal.yaml --out-dir "$tmp_dir/stage2g-review" --allow-warnings

echo "Validating Stage 2H approval-gated requests"
"$python_bin" -m libreprimus.cli approval-execution validate --request experiments/proposals/stage2h/stage2h-approved-synthetic-direct-request.yaml
"$python_bin" -m libreprimus.cli approval-execution validate --request experiments/proposals/stage2h/stage2h-noop-real-request.yaml

echo "Running Stage 2H approved synthetic request to temp"
"$python_bin" -m libreprimus.cli approval-execution run --request experiments/proposals/stage2h/stage2h-approved-synthetic-direct-request.yaml --out-dir "$tmp_dir/stage2h-approval-execution" --allow-warnings

echo "Validating Stage 2I approval-readiness proposal"
"$python_bin" -m libreprimus.cli approval-readiness validate --proposal experiments/proposals/stage2i/stage2i-first-bounded-caesar-affine-review.yaml --approval experiments/proposals/stage2i/approval-records/stage2i-first-bounded-caesar-affine-pending-approval.yaml

echo "Generating Stage 2I readiness packet to temp"
"$python_bin" -m libreprimus.cli approval-readiness packet --proposal experiments/proposals/stage2i/stage2i-first-bounded-caesar-affine-review.yaml --approval experiments/proposals/stage2i/approval-records/stage2i-first-bounded-caesar-affine-pending-approval.yaml --out-dir "$tmp_dir/stage2i-readiness" --allow-warnings

echo "Validating Stage 2J bounded operator policy and queue"
"$python_bin" -m libreprimus.cli bounded-experiment validate-policy --policy experiments/policies/operator-policy-v0.yaml
"$python_bin" -m libreprimus.cli bounded-experiment validate-queue --queue experiments/queues/stage2j-bounded-cpu-queue.yaml
"$python_bin" -m libreprimus.cli bounded-experiment check-queue --policy experiments/policies/operator-policy-v0.yaml --queue experiments/queues/stage2j-bounded-cpu-queue.yaml

echo "Running Stage 2J bounded queue to temp"
"$python_bin" -m libreprimus.cli bounded-experiment run-all --policy experiments/policies/operator-policy-v0.yaml --queue experiments/queues/stage2j-bounded-cpu-queue.yaml --out-dir "$tmp_dir/stage2j-bounded" --allow-warnings
