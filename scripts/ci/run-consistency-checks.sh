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

echo "Running document staleness checks"
"$python_bin" -m libreprimus.cli consistency check-doc-staleness \
    --source-of-truth data/project-state/stage5ah-doc-staleness-source-of-truth.yaml \
    --strict

echo "Running Stage 5AH doc-staleness coverage checks"
stage5ah_out="$tmp_dir/stage5ah-doc-staleness"
mkdir -p "$stage5ah_out"
"$python_bin" -m libreprimus.cli consistency check-stage-ledger-staleness \
    --expected-latest-stage "Stage 5AK" \
    --expected-next-stage "Stage 5AL" \
    --out "$stage5ah_out/stale_stage_ledger_report.json"
"$python_bin" -m libreprimus.cli consistency check-operational-file-map-coverage \
    --out "$stage5ah_out/operational_file_map_coverage_report.json"
"$python_bin" -m libreprimus.cli consistency check-current-next-stage-consistency \
    --expected-latest-stage "Stage 5AK" \
    --expected-next-stage "Stage 5AL" \
    --out "$stage5ah_out/current_next_stage_report.json"
"$python_bin" - <<PY
import json
from pathlib import Path
import yaml
from libreprimus.doc_staleness.stage_ledger import stage_ledger_findings_for_text

out = Path("$stage5ah_out")
readme = Path("README.md").read_text(encoding="utf-8")
findings = [
    finding.to_dict()
    for finding in stage_ledger_findings_for_text(
        readme,
        path="README.md",
        expected_latest_stage="Stage 5AK",
    )
]
(out / "readme_stage_coverage_report.json").write_text(
    json.dumps(
        {
            "record_type": "readme_stage_coverage_report",
            "expected_latest_stage": "Stage 5AK",
            "finding_count": len(findings),
            "findings": findings,
        },
        indent=2,
        sort_keys=True,
    )
    + "\n",
    encoding="utf-8",
)
summary = yaml.safe_load(Path("data/project-state/stage5ah-doc-staleness-summary.yaml").read_text(encoding="utf-8"))
(out / "doc_staleness_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
(out / "warnings.jsonl").write_text("", encoding="utf-8")
PY
"$python_bin" -m libreprimus.cli consistency validate-stage5ah-doc-staleness \
    --source-of-truth data/project-state/stage5ah-doc-staleness-source-of-truth.yaml \
    --findings data/project-state/stage5ah-doc-staleness-findings.yaml \
    --stage-ledger-coverage data/project-state/stage5ah-stage-ledger-coverage.yaml \
    --operational-file-map-coverage data/project-state/stage5ah-operational-file-map-coverage.yaml \
    --next-stage-decision data/project-state/stage5ah-next-stage-decision.yaml \
    --summary data/project-state/stage5ah-doc-staleness-summary.yaml \
    --results-dir "$stage5ah_out"

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

echo "Running Stage 5A CUDA planning synthetic/temp output"
"$python_bin" -m libreprimus.cli cuda-planning build-target-plan \
    --manifest experiments/manifests/cuda/stage5a-cuda-target-plan.yaml \
    --out-dir "$tmp_dir/stage5a-cuda-planning" \
    --target-plan-out "$tmp_dir/stage5a-cuda-target-plan.yaml" \
    --non-targets-out "$tmp_dir/stage5a-cuda-non-targets.yaml" \
    --allow-warnings
"$python_bin" -m libreprimus.cli cuda-planning build-parity-scaffold \
    --manifest experiments/manifests/cuda/stage5a-cuda-parity-scaffold.yaml \
    --out-dir "$tmp_dir/stage5a-cuda-planning" \
    --parity-scaffold-out "$tmp_dir/stage5a-cuda-parity-scaffold.yaml" \
    --allow-warnings
"$python_bin" -m libreprimus.cli cuda-planning build-implementation-gates \
    --manifest experiments/manifests/cuda/stage5a-cuda-implementation-gates.yaml \
    --out-dir "$tmp_dir/stage5a-cuda-planning" \
    --implementation-gates-out "$tmp_dir/stage5a-cuda-implementation-gates.yaml" \
    --summary-out "$tmp_dir/stage5a-cuda-planning-summary.yaml" \
    --allow-warnings
"$python_bin" -m libreprimus.cli cuda-planning validate-stage5a \
    --target-plan "$tmp_dir/stage5a-cuda-target-plan.yaml" \
    --parity-scaffold "$tmp_dir/stage5a-cuda-parity-scaffold.yaml" \
    --implementation-gates "$tmp_dir/stage5a-cuda-implementation-gates.yaml" \
    --non-targets "$tmp_dir/stage5a-cuda-non-targets.yaml" \
    --summary "$tmp_dir/stage5a-cuda-planning-summary.yaml" \
    --results-dir "$tmp_dir/stage5a-cuda-planning"

echo "Running Stage 5B CUDA parity harness synthetic/temp output"
"$python_bin" -m libreprimus.cli cuda-parity build-harness-plan \
    --manifest experiments/manifests/cuda/stage5b-cuda-parity-harness-plan.yaml \
    --target-plan data/cuda/stage5a-cuda-target-plan.yaml \
    --parity-scaffold data/cuda/stage5a-cuda-parity-scaffold.yaml \
    --implementation-gates data/cuda/stage5a-cuda-implementation-gates.yaml \
    --non-targets data/cuda/stage5a-cuda-non-targets.yaml \
    --stage5a-summary data/cuda/stage5a-cuda-planning-summary.yaml \
    --stage4q-readiness data/benchmarks/stage4q-cuda-parity-readiness.yaml \
    --stage4q-summary data/research/stage4q-cpu-benchmark-parity-planning-summary.yaml \
    --stage4o-summary data/research/stage4o-cpu-batch-adapter-expansion-summary.yaml \
    --stage4p-summary data/research/stage4p-result-store-score-summary-unification-summary.yaml \
    --out-dir "$tmp_dir/stage5b-cuda-parity" \
    --harness-plan-out "$tmp_dir/stage5b-cuda-parity-harness-plan.yaml" \
    --parity-fixtures-out "$tmp_dir/stage5b-cuda-parity-fixtures.yaml" \
    --summary-out "$tmp_dir/stage5b-cuda-parity-harness-summary.yaml" \
    --allow-warnings
"$python_bin" -m libreprimus.cli cuda-parity build-backend-capability \
    --manifest experiments/manifests/cuda/stage5b-cuda-backend-capability.yaml \
    --out-dir "$tmp_dir/stage5b-cuda-parity" \
    --backend-capability-out "$tmp_dir/stage5b-cuda-backend-capability.yaml" \
    --allow-missing-cuda \
    --allow-warnings
"$python_bin" -m libreprimus.cli cuda-parity build-future-kernel-matrix \
    --manifest experiments/manifests/cuda/stage5b-future-kernel-parity-matrix.yaml \
    --target-plan data/cuda/stage5a-cuda-target-plan.yaml \
    --harness-plan "$tmp_dir/stage5b-cuda-parity-harness-plan.yaml" \
    --parity-fixtures "$tmp_dir/stage5b-cuda-parity-fixtures.yaml" \
    --backend-capability "$tmp_dir/stage5b-cuda-backend-capability.yaml" \
    --out-dir "$tmp_dir/stage5b-cuda-parity" \
    --future-kernel-matrix-out "$tmp_dir/stage5b-future-kernel-parity-matrix.yaml" \
    --summary-out "$tmp_dir/stage5b-cuda-parity-harness-summary.yaml" \
    --allow-warnings
"$python_bin" -m libreprimus.cli cuda-parity validate-stage5b \
    --harness-plan "$tmp_dir/stage5b-cuda-parity-harness-plan.yaml" \
    --parity-fixtures "$tmp_dir/stage5b-cuda-parity-fixtures.yaml" \
    --backend-capability "$tmp_dir/stage5b-cuda-backend-capability.yaml" \
    --future-kernel-matrix "$tmp_dir/stage5b-future-kernel-parity-matrix.yaml" \
    --summary "$tmp_dir/stage5b-cuda-parity-harness-summary.yaml" \
    --results-dir "$tmp_dir/stage5b-cuda-parity"

echo "Running Stage 5C CUDA build/device detection synthetic/temp output"
"$python_bin" -m libreprimus.cli cuda-build profile-toolchain \
    --manifest experiments/manifests/cuda/stage5c-cuda-build-device-detection.yaml \
    --out-dir "$tmp_dir/stage5c-cuda-build" \
    --profiles-out "$tmp_dir/stage5c-cuda-build-profiles.yaml" \
    --toolchain-out "$tmp_dir/stage5c-cuda-toolchain-detection.yaml" \
    --allow-missing-cuda \
    --allow-warnings
"$python_bin" -m libreprimus.cli cuda-build detect-device \
    --manifest experiments/manifests/cuda/stage5c-cuda-build-device-detection.yaml \
    --out-dir "$tmp_dir/stage5c-cuda-build" \
    --devices-out "$tmp_dir/stage5c-cuda-device-detection.yaml" \
    --allow-no-gpu \
    --allow-warnings
"$python_bin" -m libreprimus.cli cuda-build smoke-build \
    --manifest experiments/manifests/cuda/stage5c-cuda-no-gpu-ci-profile.yaml \
    --out-dir "$tmp_dir/stage5c-cuda-build" \
    --smoke-build-out "$tmp_dir/stage5c-cuda-smoke-build-records.yaml" \
    --allow-missing-cuda \
    --allow-no-gpu \
    --allow-warnings
"$python_bin" -m libreprimus.cli cuda-build build-summary \
    --profiles "$tmp_dir/stage5c-cuda-build-profiles.yaml" \
    --toolchain "$tmp_dir/stage5c-cuda-toolchain-detection.yaml" \
    --devices "$tmp_dir/stage5c-cuda-device-detection.yaml" \
    --smoke-build "$tmp_dir/stage5c-cuda-smoke-build-records.yaml" \
    --summary-out "$tmp_dir/stage5c-cuda-build-device-summary.yaml" \
    --out-dir "$tmp_dir/stage5c-cuda-build" \
    --allow-warnings
"$python_bin" -m libreprimus.cli cuda-build validate-stage5c \
    --profiles "$tmp_dir/stage5c-cuda-build-profiles.yaml" \
    --toolchain "$tmp_dir/stage5c-cuda-toolchain-detection.yaml" \
    --devices "$tmp_dir/stage5c-cuda-device-detection.yaml" \
    --smoke-build "$tmp_dir/stage5c-cuda-smoke-build-records.yaml" \
    --summary "$tmp_dir/stage5c-cuda-build-device-summary.yaml" \
    --results-dir "$tmp_dir/stage5c-cuda-build"

echo "Running Stage 5D native CPU backend synthetic/temp output"
cat > "$tmp_dir/stage5d-fake-native.py" <<'PY'
import json
import sys
from libreprimus.native_cpu.runner import python_reference_run
thread_count = 1
for index, arg in enumerate(sys.argv):
    if arg == "--threads" and index + 1 < len(sys.argv):
        thread_count = int(sys.argv[index + 1])
json.dump(python_reference_run(threads=thread_count), sys.stdout, sort_keys=True)
PY
"$python_bin" -m libreprimus.cli native-cpu run-smoke \
    --native-executable "$tmp_dir/stage5d-fake-native.py" \
    --manifest experiments/manifests/native-cpu/stage5d-native-cpu-smoke.yaml \
    --out-dir "$tmp_dir/stage5d-native-cpu" \
    --capabilities-out "$tmp_dir/stage5d-native-cpu-backend-capabilities.yaml" \
    --diagnostics-out "$tmp_dir/stage5d-native-cpu-diagnostic-records.yaml" \
    --allow-warnings
"$python_bin" -m libreprimus.cli native-cpu check-threading-parity \
    --native-executable "$tmp_dir/stage5d-fake-native.py" \
    --manifest experiments/manifests/native-cpu/stage5d-native-cpu-threading-parity.yaml \
    --out-dir "$tmp_dir/stage5d-native-cpu" \
    --threading-out "$tmp_dir/stage5d-native-cpu-threading-records.yaml" \
    --thread-counts 1,2,4 \
    --allow-warnings
"$python_bin" -m libreprimus.cli native-cpu check-python-parity \
    --native-executable "$tmp_dir/stage5d-fake-native.py" \
    --manifest experiments/manifests/native-cpu/stage5d-native-python-parity.yaml \
    --out-dir "$tmp_dir/stage5d-native-cpu" \
    --parity-out "$tmp_dir/stage5d-native-cpu-parity-records.yaml" \
    --allow-warnings
"$python_bin" -m libreprimus.cli native-cpu build-summary \
    --capabilities "$tmp_dir/stage5d-native-cpu-backend-capabilities.yaml" \
    --threading "$tmp_dir/stage5d-native-cpu-threading-records.yaml" \
    --parity "$tmp_dir/stage5d-native-cpu-parity-records.yaml" \
    --diagnostics "$tmp_dir/stage5d-native-cpu-diagnostic-records.yaml" \
    --summary-out "$tmp_dir/stage5d-native-cpu-summary.yaml" \
    --out-dir "$tmp_dir/stage5d-native-cpu" \
    --allow-warnings
"$python_bin" -m libreprimus.cli native-cpu validate-stage5d \
    --capabilities "$tmp_dir/stage5d-native-cpu-backend-capabilities.yaml" \
    --threading "$tmp_dir/stage5d-native-cpu-threading-records.yaml" \
    --parity "$tmp_dir/stage5d-native-cpu-parity-records.yaml" \
    --diagnostics "$tmp_dir/stage5d-native-cpu-diagnostic-records.yaml" \
    --summary "$tmp_dir/stage5d-native-cpu-summary.yaml" \
    --results-dir "$tmp_dir/stage5d-native-cpu"

echo "Running Stage 5E CUDA kernel contract synthetic/temp output"
"$python_bin" -m libreprimus.cli cuda-kernel-contract select-first-kernel \
    --manifest experiments/manifests/cuda/stage5e-first-kernel-contract.yaml \
    --out-dir "$tmp_dir/stage5e-cuda-kernel-contract" \
    --contract-out "$tmp_dir/stage5e-first-kernel-contract.yaml" \
    --adapter-selection-out "$tmp_dir/stage5e-cuda-adapter-selection.yaml" \
    --allow-warnings
"$python_bin" -m libreprimus.cli cuda-kernel-contract build-native-parity-map \
    --manifest experiments/manifests/cuda/stage5e-adapter-selection.yaml \
    --contract "$tmp_dir/stage5e-first-kernel-contract.yaml" \
    --out-dir "$tmp_dir/stage5e-cuda-kernel-contract" \
    --native-parity-out "$tmp_dir/stage5e-native-parity-adapter-map.yaml" \
    --allow-warnings
"$python_bin" -m libreprimus.cli cuda-kernel-contract build-readiness \
    --manifest experiments/manifests/cuda/stage5e-implementation-readiness.yaml \
    --contract "$tmp_dir/stage5e-first-kernel-contract.yaml" \
    --native-parity "$tmp_dir/stage5e-native-parity-adapter-map.yaml" \
    --out-dir "$tmp_dir/stage5e-cuda-kernel-contract" \
    --readiness-out "$tmp_dir/stage5e-implementation-readiness.yaml" \
    --allow-warnings
"$python_bin" -m libreprimus.cli cuda-kernel-contract build-summary \
    --contract "$tmp_dir/stage5e-first-kernel-contract.yaml" \
    --adapter-selection "$tmp_dir/stage5e-cuda-adapter-selection.yaml" \
    --native-parity "$tmp_dir/stage5e-native-parity-adapter-map.yaml" \
    --readiness "$tmp_dir/stage5e-implementation-readiness.yaml" \
    --out-dir "$tmp_dir/stage5e-cuda-kernel-contract" \
    --summary-out "$tmp_dir/stage5e-first-kernel-contract-summary.yaml" \
    --allow-warnings
"$python_bin" -m libreprimus.cli cuda-kernel-contract validate-stage5e \
    --contract "$tmp_dir/stage5e-first-kernel-contract.yaml" \
    --adapter-selection "$tmp_dir/stage5e-cuda-adapter-selection.yaml" \
    --native-parity "$tmp_dir/stage5e-native-parity-adapter-map.yaml" \
    --readiness "$tmp_dir/stage5e-implementation-readiness.yaml" \
    --summary "$tmp_dir/stage5e-first-kernel-contract-summary.yaml" \
    --results-dir "$tmp_dir/stage5e-cuda-kernel-contract"

echo "Running Stage 5F synthetic CUDA kernel no-GPU-safe/temp output"
"$python_bin" -m libreprimus.cli cuda-kernel build-implementation-records \
    --manifest experiments/manifests/cuda/stage5f-shift-score-synthetic-parity.yaml \
    --out-dir "$tmp_dir/stage5f-cuda-kernel" \
    --implementation-out "$tmp_dir/stage5f-cuda-synthetic-kernel-implementation.yaml" \
    --allow-warnings
"$python_bin" -m libreprimus.cli cuda-kernel attempt-build \
    --manifest experiments/manifests/cuda/stage5f-cuda-no-gpu-ci-skip.yaml \
    --out-dir "$tmp_dir/stage5f-cuda-kernel" \
    --build-records-out "$tmp_dir/stage5f-cuda-kernel-build-records.yaml" \
    --build-dir "$tmp_dir/stage5f-cuda-build" \
    --skip-build \
    --allow-warnings
"$python_bin" -m libreprimus.cli cuda-kernel run-synthetic-parity \
    --manifest experiments/manifests/cuda/stage5f-shift-score-synthetic-parity.yaml \
    --build-records "$tmp_dir/stage5f-cuda-kernel-build-records.yaml" \
    --out-dir "$tmp_dir/stage5f-cuda-kernel" \
    --parity-records-out "$tmp_dir/stage5f-cuda-synthetic-parity-records.yaml" \
    --build-dir "$tmp_dir/stage5f-cuda-build" \
    --allow-warnings
"$python_bin" -m libreprimus.cli cuda-kernel build-summary \
    --implementation "$tmp_dir/stage5f-cuda-synthetic-kernel-implementation.yaml" \
    --build-records "$tmp_dir/stage5f-cuda-kernel-build-records.yaml" \
    --parity-records "$tmp_dir/stage5f-cuda-synthetic-parity-records.yaml" \
    --summary-out "$tmp_dir/stage5f-cuda-synthetic-kernel-summary.yaml" \
    --out-dir "$tmp_dir/stage5f-cuda-kernel" \
    --allow-warnings
"$python_bin" -m libreprimus.cli cuda-kernel validate-stage5f \
    --implementation "$tmp_dir/stage5f-cuda-synthetic-kernel-implementation.yaml" \
    --build-records "$tmp_dir/stage5f-cuda-kernel-build-records.yaml" \
    --parity-records "$tmp_dir/stage5f-cuda-synthetic-parity-records.yaml" \
    --summary "$tmp_dir/stage5f-cuda-synthetic-kernel-summary.yaml" \
    --results-dir "$tmp_dir/stage5f-cuda-kernel"

echo "Running Stage 5G CUDA parity reporting no-GPU-safe/temp output"
"$python_bin" -m libreprimus.cli cuda-parity-reporting build-parity-report \
    --manifest experiments/manifests/cuda/stage5g-shift-score-parity-reporting.yaml \
    --out-dir "$tmp_dir/stage5g-cuda-parity-reporting" \
    --parity-report-out "$tmp_dir/stage5g-shift-score-parity-report.yaml" \
    --allow-warnings
"$python_bin" -m libreprimus.cli cuda-parity-reporting audit-device-code-subset \
    --manifest experiments/manifests/cuda/stage5g-device-code-subset-audit.yaml \
    --out-dir "$tmp_dir/stage5g-cuda-parity-reporting" \
    --device-code-audit-out "$tmp_dir/stage5g-cuda-device-code-subset-audit.yaml" \
    --allow-warnings
"$python_bin" -m libreprimus.cli cuda-parity-reporting build-solved-fixture-preflight \
    --manifest experiments/manifests/cuda/stage5g-solved-fixture-safe-adapter-preflight.yaml \
    --out-dir "$tmp_dir/stage5g-cuda-parity-reporting" \
    --preflight-out "$tmp_dir/stage5g-solved-fixture-safe-adapter-preflight.yaml" \
    --allow-warnings
"$python_bin" -m libreprimus.cli cuda-parity-reporting build-summary \
    --parity-report "$tmp_dir/stage5g-shift-score-parity-report.yaml" \
    --device-code-audit "$tmp_dir/stage5g-cuda-device-code-subset-audit.yaml" \
    --preflight "$tmp_dir/stage5g-solved-fixture-safe-adapter-preflight.yaml" \
    --summary-out "$tmp_dir/stage5g-cuda-parity-reporting-summary.yaml" \
    --out-dir "$tmp_dir/stage5g-cuda-parity-reporting" \
    --allow-warnings
"$python_bin" -m libreprimus.cli cuda-parity-reporting validate-stage5g \
    --parity-report "$tmp_dir/stage5g-shift-score-parity-report.yaml" \
    --device-code-audit "$tmp_dir/stage5g-cuda-device-code-subset-audit.yaml" \
    --preflight "$tmp_dir/stage5g-solved-fixture-safe-adapter-preflight.yaml" \
    --summary "$tmp_dir/stage5g-cuda-parity-reporting-summary.yaml" \
    --results-dir "$tmp_dir/stage5g-cuda-parity-reporting"

echo "Running Stage 5H Gematria shift contract no-GPU-safe/temp output"
"$python_bin" -m libreprimus.cli gematria-shift-contract build-contract \
    --manifest experiments/manifests/cuda/stage5h-gematria-shift-score-contract.yaml \
    --out-dir "$tmp_dir/stage5h-gematria-shift-contract" \
    --contract-out "$tmp_dir/stage5h-gematria-shift-score-contract.yaml" \
    --allow-warnings
"$python_bin" -m libreprimus.cli gematria-shift-contract build-native-fixtures \
    --manifest experiments/manifests/cuda/stage5h-gematria-native-parity-fixtures.yaml \
    --out-dir "$tmp_dir/stage5h-gematria-shift-contract" \
    --fixtures-out "$tmp_dir/stage5h-gematria-native-parity-fixtures.yaml" \
    --allow-warnings
"$python_bin" -m libreprimus.cli gematria-shift-contract build-solved-fixture-mapping \
    --manifest experiments/manifests/cuda/stage5h-solved-fixture-safe-mapping.yaml \
    --source-manifest experiments/manifests/cpu-batch/stage4o-solved-fixture-parity-batch.yaml \
    --out-dir "$tmp_dir/stage5h-gematria-shift-contract" \
    --mapping-out "$tmp_dir/stage5h-gematria-solved-fixture-safe-mapping.yaml" \
    --allow-warnings
"$python_bin" -m libreprimus.cli gematria-shift-contract build-score-summary-plan \
    --manifest experiments/manifests/cuda/stage5h-gematria-shift-score-contract.yaml \
    --out-dir "$tmp_dir/stage5h-gematria-shift-contract" \
    --score-summary-plan-out "$tmp_dir/stage5h-gematria-score-summary-parity-plan.yaml" \
    --allow-warnings
"$python_bin" -m libreprimus.cli gematria-shift-contract build-summary \
    --contract "$tmp_dir/stage5h-gematria-shift-score-contract.yaml" \
    --fixtures "$tmp_dir/stage5h-gematria-native-parity-fixtures.yaml" \
    --mapping "$tmp_dir/stage5h-gematria-solved-fixture-safe-mapping.yaml" \
    --score-summary-plan "$tmp_dir/stage5h-gematria-score-summary-parity-plan.yaml" \
    --summary-out "$tmp_dir/stage5h-gematria-shift-contract-summary.yaml" \
    --out-dir "$tmp_dir/stage5h-gematria-shift-contract" \
    --allow-warnings
"$python_bin" -m libreprimus.cli gematria-shift-contract validate-stage5h \
    --contract "$tmp_dir/stage5h-gematria-shift-score-contract.yaml" \
    --fixtures "$tmp_dir/stage5h-gematria-native-parity-fixtures.yaml" \
    --mapping "$tmp_dir/stage5h-gematria-solved-fixture-safe-mapping.yaml" \
    --score-summary-plan "$tmp_dir/stage5h-gematria-score-summary-parity-plan.yaml" \
    --summary "$tmp_dir/stage5h-gematria-shift-contract-summary.yaml" \
    --results-dir "$tmp_dir/stage5h-gematria-shift-contract"

echo "Running Stage 5I Gematria CUDA preparation no-GPU-safe/temp output"
"$python_bin" -m libreprimus.cli gematria-cuda-prep build-kernel-preparation \
    --manifest experiments/manifests/cuda/stage5i-gematria-cuda-kernel-preparation.yaml \
    --out-dir "$tmp_dir/stage5i-gematria-cuda-prep" \
    --preparation-out "$tmp_dir/stage5i-gematria-cuda-kernel-preparation.yaml" \
    --allow-warnings
"$python_bin" -m libreprimus.cli gematria-cuda-prep build-abi-plan \
    --manifest experiments/manifests/cuda/stage5i-gematria-cuda-abi-plan.yaml \
    --out-dir "$tmp_dir/stage5i-gematria-cuda-prep" \
    --abi-plan-out "$tmp_dir/stage5i-gematria-cuda-abi-plan.yaml" \
    --allow-warnings
"$python_bin" -m libreprimus.cli gematria-cuda-prep build-validation-vectors \
    --manifest experiments/manifests/cuda/stage5i-gematria-cuda-validation-vectors.yaml \
    --out-dir "$tmp_dir/stage5i-gematria-cuda-prep" \
    --validation-vectors-out "$tmp_dir/stage5i-gematria-cuda-validation-vectors.yaml" \
    --allow-warnings
"$python_bin" -m libreprimus.cli gematria-cuda-prep build-implementation-checklist \
    --out-dir "$tmp_dir/stage5i-gematria-cuda-prep" \
    --implementation-checklist-out "$tmp_dir/stage5i-gematria-cuda-implementation-checklist.yaml" \
    --allow-warnings
"$python_bin" -m libreprimus.cli gematria-cuda-prep build-summary \
    --preparation "$tmp_dir/stage5i-gematria-cuda-kernel-preparation.yaml" \
    --abi-plan "$tmp_dir/stage5i-gematria-cuda-abi-plan.yaml" \
    --validation-vectors "$tmp_dir/stage5i-gematria-cuda-validation-vectors.yaml" \
    --implementation-checklist "$tmp_dir/stage5i-gematria-cuda-implementation-checklist.yaml" \
    --summary-out "$tmp_dir/stage5i-gematria-cuda-preparation-summary.yaml" \
    --out-dir "$tmp_dir/stage5i-gematria-cuda-prep" \
    --allow-warnings
"$python_bin" -m libreprimus.cli gematria-cuda-prep validate-stage5i \
    --preparation "$tmp_dir/stage5i-gematria-cuda-kernel-preparation.yaml" \
    --abi-plan "$tmp_dir/stage5i-gematria-cuda-abi-plan.yaml" \
    --validation-vectors "$tmp_dir/stage5i-gematria-cuda-validation-vectors.yaml" \
    --implementation-checklist "$tmp_dir/stage5i-gematria-cuda-implementation-checklist.yaml" \
    --summary "$tmp_dir/stage5i-gematria-cuda-preparation-summary.yaml" \
    --results-dir "$tmp_dir/stage5i-gematria-cuda-prep"

echo "Running Stage 5J Gematria CUDA kernel no-GPU-safe/temp output"
"$python_bin" -m libreprimus.cli gematria-cuda-kernel build-implementation-records \
    --manifest experiments/manifests/cuda/stage5j-gematria-cuda-kernel.yaml \
    --out-dir "$tmp_dir/stage5j-gematria-cuda-kernel" \
    --implementation-out "$tmp_dir/stage5j-gematria-cuda-kernel-implementation.yaml" \
    --allow-warnings
"$python_bin" -m libreprimus.cli gematria-cuda-kernel attempt-build \
    --manifest experiments/manifests/cuda/stage5j-gematria-cuda-no-gpu-ci-skip.yaml \
    --out-dir "$tmp_dir/stage5j-gematria-cuda-kernel" \
    --build-records-out "$tmp_dir/stage5j-gematria-cuda-kernel-build-records.yaml" \
    --build-dir "$tmp_dir/stage5j-cuda-build" \
    --skip-build \
    --allow-warnings
"$python_bin" -m libreprimus.cli gematria-cuda-kernel run-synthetic-parity \
    --manifest experiments/manifests/cuda/stage5j-gematria-cuda-kernel.yaml \
    --build-records "$tmp_dir/stage5j-gematria-cuda-kernel-build-records.yaml" \
    --out-dir "$tmp_dir/stage5j-gematria-cuda-kernel" \
    --parity-records-out "$tmp_dir/stage5j-gematria-cuda-synthetic-parity-records.yaml" \
    --build-dir "$tmp_dir/stage5j-cuda-build" \
    --allow-warnings
"$python_bin" -m libreprimus.cli gematria-cuda-kernel build-summary \
    --implementation "$tmp_dir/stage5j-gematria-cuda-kernel-implementation.yaml" \
    --build-records "$tmp_dir/stage5j-gematria-cuda-kernel-build-records.yaml" \
    --parity-records "$tmp_dir/stage5j-gematria-cuda-synthetic-parity-records.yaml" \
    --summary-out "$tmp_dir/stage5j-gematria-cuda-kernel-summary.yaml" \
    --out-dir "$tmp_dir/stage5j-gematria-cuda-kernel" \
    --allow-warnings
"$python_bin" -m libreprimus.cli gematria-cuda-kernel validate-stage5j \
    --implementation "$tmp_dir/stage5j-gematria-cuda-kernel-implementation.yaml" \
    --build-records "$tmp_dir/stage5j-gematria-cuda-kernel-build-records.yaml" \
    --parity-records "$tmp_dir/stage5j-gematria-cuda-synthetic-parity-records.yaml" \
    --summary "$tmp_dir/stage5j-gematria-cuda-kernel-summary.yaml" \
    --results-dir "$tmp_dir/stage5j-gematria-cuda-kernel"

echo "Running Stage 5K Gematria CUDA parity reporting no-GPU-safe/temp output"
"$python_bin" -m libreprimus.cli gematria-cuda-parity-reporting build-parity-report \
    --manifest experiments/manifests/cuda/stage5k-gematria-cuda-parity-reporting.yaml \
    --out-dir "$tmp_dir/stage5k-gematria-cuda-parity-reporting" \
    --parity-report-out "$tmp_dir/stage5k-gematria-cuda-parity-report.yaml" \
    --allow-warnings
"$python_bin" -m libreprimus.cli gematria-cuda-parity-reporting audit-device-code \
    --manifest experiments/manifests/cuda/stage5k-gematria-device-code-audit.yaml \
    --out-dir "$tmp_dir/stage5k-gematria-cuda-parity-reporting" \
    --device-code-audit-out "$tmp_dir/stage5k-gematria-cuda-device-code-audit.yaml" \
    --allow-warnings
"$python_bin" -m libreprimus.cli gematria-cuda-parity-reporting build-solved-fixture-preflight \
    --manifest experiments/manifests/cuda/stage5k-solved-fixture-safe-preflight.yaml \
    --out-dir "$tmp_dir/stage5k-gematria-cuda-parity-reporting" \
    --preflight-out "$tmp_dir/stage5k-gematria-solved-fixture-safe-preflight.yaml" \
    --allow-warnings
"$python_bin" -m libreprimus.cli gematria-cuda-parity-reporting build-score-summary-preflight \
    --manifest experiments/manifests/cuda/stage5k-solved-fixture-safe-preflight.yaml \
    --out-dir "$tmp_dir/stage5k-gematria-cuda-parity-reporting" \
    --score-summary-preflight-out "$tmp_dir/stage5k-gematria-cuda-score-summary-preflight.yaml" \
    --allow-warnings
"$python_bin" -m libreprimus.cli gematria-cuda-parity-reporting build-summary \
    --parity-report "$tmp_dir/stage5k-gematria-cuda-parity-report.yaml" \
    --device-code-audit "$tmp_dir/stage5k-gematria-cuda-device-code-audit.yaml" \
    --preflight "$tmp_dir/stage5k-gematria-solved-fixture-safe-preflight.yaml" \
    --score-summary-preflight "$tmp_dir/stage5k-gematria-cuda-score-summary-preflight.yaml" \
    --summary-out "$tmp_dir/stage5k-gematria-cuda-parity-reporting-summary.yaml" \
    --out-dir "$tmp_dir/stage5k-gematria-cuda-parity-reporting" \
    --allow-warnings
"$python_bin" -m libreprimus.cli gematria-cuda-parity-reporting validate-stage5k \
    --parity-report "$tmp_dir/stage5k-gematria-cuda-parity-report.yaml" \
    --device-code-audit "$tmp_dir/stage5k-gematria-cuda-device-code-audit.yaml" \
    --preflight "$tmp_dir/stage5k-gematria-solved-fixture-safe-preflight.yaml" \
    --score-summary-preflight "$tmp_dir/stage5k-gematria-cuda-score-summary-preflight.yaml" \
    --summary "$tmp_dir/stage5k-gematria-cuda-parity-reporting-summary.yaml" \
    --results-dir "$tmp_dir/stage5k-gematria-cuda-parity-reporting"

echo "Running Stage 5L solved-fixture Gematria token mapping no-GPU-safe/temp output"
"$python_bin" -m libreprimus.cli gematria-solved-fixture-mapping build-token-mapping \
    --manifest experiments/manifests/cuda/stage5l-solved-fixture-token-mapping.yaml \
    --preflight data/cuda/stage5k-gematria-solved-fixture-safe-preflight.yaml \
    --out-dir "$tmp_dir/stage5l-gematria-solved-fixture-mapping" \
    --token-mapping-out "$tmp_dir/stage5l-gematria-solved-fixture-token-mapping.yaml" \
    --allow-warnings
"$python_bin" -m libreprimus.cli gematria-solved-fixture-mapping build-native-parity \
    --token-mapping "$tmp_dir/stage5l-gematria-solved-fixture-token-mapping.yaml" \
    --out-dir "$tmp_dir/stage5l-gematria-solved-fixture-mapping" \
    --native-parity-out "$tmp_dir/stage5l-gematria-solved-fixture-native-parity.yaml" \
    --allow-warnings
"$python_bin" -m libreprimus.cli gematria-solved-fixture-mapping build-output-hash-contract \
    --native-parity "$tmp_dir/stage5l-gematria-solved-fixture-native-parity.yaml" \
    --out-dir "$tmp_dir/stage5l-gematria-solved-fixture-mapping" \
    --output-hash-contract-out "$tmp_dir/stage5l-gematria-solved-fixture-output-hash-contract.yaml" \
    --allow-warnings
"$python_bin" -m libreprimus.cli gematria-solved-fixture-mapping build-score-summary-shape \
    --out-dir "$tmp_dir/stage5l-gematria-solved-fixture-mapping" \
    --score-summary-shape-out "$tmp_dir/stage5l-gematria-solved-fixture-score-summary-shape.yaml" \
    --allow-warnings
"$python_bin" -m libreprimus.cli gematria-solved-fixture-mapping build-summary \
    --token-mapping "$tmp_dir/stage5l-gematria-solved-fixture-token-mapping.yaml" \
    --native-parity "$tmp_dir/stage5l-gematria-solved-fixture-native-parity.yaml" \
    --output-hash-contract "$tmp_dir/stage5l-gematria-solved-fixture-output-hash-contract.yaml" \
    --score-summary-shape "$tmp_dir/stage5l-gematria-solved-fixture-score-summary-shape.yaml" \
    --summary-out "$tmp_dir/stage5l-solved-fixture-token-mapping-summary.yaml" \
    --out-dir "$tmp_dir/stage5l-gematria-solved-fixture-mapping" \
    --allow-warnings
"$python_bin" -m libreprimus.cli gematria-solved-fixture-mapping validate-stage5l \
    --token-mapping "$tmp_dir/stage5l-gematria-solved-fixture-token-mapping.yaml" \
    --native-parity "$tmp_dir/stage5l-gematria-solved-fixture-native-parity.yaml" \
    --output-hash-contract "$tmp_dir/stage5l-gematria-solved-fixture-output-hash-contract.yaml" \
    --score-summary-shape "$tmp_dir/stage5l-gematria-solved-fixture-score-summary-shape.yaml" \
    --summary "$tmp_dir/stage5l-solved-fixture-token-mapping-summary.yaml" \
    --results-dir "$tmp_dir/stage5l-gematria-solved-fixture-mapping"

echo "Running Stage 5M solved-fixture Gematria CUDA parity no-GPU-safe/temp output"
"$python_bin" -m libreprimus.cli gematria-solved-fixture-cuda build-run-records \
    --token-mapping data/cuda/stage5l-gematria-solved-fixture-token-mapping.yaml \
    --native-parity data/cuda/stage5l-gematria-solved-fixture-native-parity.yaml \
    --run-records-out "$tmp_dir/stage5m-gematria-solved-fixture-cuda-run.yaml" \
    --out-dir "$tmp_dir/stage5m-gematria-solved-fixture-cuda" \
    --allow-warnings
"$python_bin" -m libreprimus.cli gematria-solved-fixture-cuda run-cuda-parity \
    --run-records "$tmp_dir/stage5m-gematria-solved-fixture-cuda-run.yaml" \
    --run-records-out "$tmp_dir/stage5m-gematria-solved-fixture-cuda-run.yaml" \
    --out-dir "$tmp_dir/stage5m-gematria-solved-fixture-cuda" \
    --build-dir "$tmp_dir/stage5m-cuda-build" \
    --skip-run \
    --allow-warnings
"$python_bin" -m libreprimus.cli gematria-solved-fixture-cuda build-parity-records \
    --run-records "$tmp_dir/stage5m-gematria-solved-fixture-cuda-run.yaml" \
    --parity-records-out "$tmp_dir/stage5m-gematria-solved-fixture-cuda-parity.yaml" \
    --out-dir "$tmp_dir/stage5m-gematria-solved-fixture-cuda" \
    --allow-warnings
"$python_bin" -m libreprimus.cli gematria-solved-fixture-cuda build-boundary-records \
    --run-records "$tmp_dir/stage5m-gematria-solved-fixture-cuda-run.yaml" \
    --boundaries-out "$tmp_dir/stage5m-gematria-solved-fixture-cuda-boundaries.yaml" \
    --out-dir "$tmp_dir/stage5m-gematria-solved-fixture-cuda" \
    --allow-warnings
"$python_bin" -m libreprimus.cli gematria-solved-fixture-cuda build-summary \
    --run-records "$tmp_dir/stage5m-gematria-solved-fixture-cuda-run.yaml" \
    --parity-records "$tmp_dir/stage5m-gematria-solved-fixture-cuda-parity.yaml" \
    --boundaries "$tmp_dir/stage5m-gematria-solved-fixture-cuda-boundaries.yaml" \
    --summary-out "$tmp_dir/stage5m-solved-fixture-cuda-parity-summary.yaml" \
    --out-dir "$tmp_dir/stage5m-gematria-solved-fixture-cuda" \
    --allow-warnings
"$python_bin" -m libreprimus.cli gematria-solved-fixture-cuda validate-stage5m \
    --run-records "$tmp_dir/stage5m-gematria-solved-fixture-cuda-run.yaml" \
    --parity-records "$tmp_dir/stage5m-gematria-solved-fixture-cuda-parity.yaml" \
    --boundaries "$tmp_dir/stage5m-gematria-solved-fixture-cuda-boundaries.yaml" \
    --summary "$tmp_dir/stage5m-solved-fixture-cuda-parity-summary.yaml" \
    --results-dir "$tmp_dir/stage5m-gematria-solved-fixture-cuda"

echo "Running Stage 5N solved-fixture Gematria CUDA reporting no-GPU-safe/temp output"
"$python_bin" -m libreprimus.cli gematria-solved-fixture-cuda-reporting build-parity-report \
    --stage5m-run-records data/cuda/stage5m-gematria-solved-fixture-cuda-run.yaml \
    --stage5m-parity-records data/cuda/stage5m-gematria-solved-fixture-cuda-parity.yaml \
    --stage5m-summary data/cuda/stage5m-solved-fixture-cuda-parity-summary.yaml \
    --parity-report-out "$tmp_dir/stage5n-gematria-solved-fixture-cuda-report.yaml" \
    --out-dir "$tmp_dir/stage5n-gematria-solved-fixture-cuda-reporting" \
    --allow-warnings
"$python_bin" -m libreprimus.cli gematria-solved-fixture-cuda-reporting build-controlled-expansion-gate \
    --controlled-expansion-gate-out "$tmp_dir/stage5n-gematria-controlled-expansion-gate.yaml" \
    --out-dir "$tmp_dir/stage5n-gematria-solved-fixture-cuda-reporting" \
    --allow-warnings
"$python_bin" -m libreprimus.cli gematria-solved-fixture-cuda-reporting build-boundary-review \
    --stage5m-summary data/cuda/stage5m-solved-fixture-cuda-parity-summary.yaml \
    --boundary-review-out "$tmp_dir/stage5n-gematria-cuda-boundary-review.yaml" \
    --out-dir "$tmp_dir/stage5n-gematria-solved-fixture-cuda-reporting" \
    --allow-warnings
"$python_bin" -m libreprimus.cli gematria-solved-fixture-cuda-reporting build-result-store-preflight \
    --stage4p-summary data/research/stage4p-result-store-score-summary-unification-summary.yaml \
    --result-store-preflight-out "$tmp_dir/stage5n-gematria-cuda-result-store-preflight.yaml" \
    --out-dir "$tmp_dir/stage5n-gematria-solved-fixture-cuda-reporting" \
    --allow-warnings
"$python_bin" -m libreprimus.cli gematria-solved-fixture-cuda-reporting build-no-unsolved-guardrail \
    --no-unsolved-guardrail-out "$tmp_dir/stage5n-gematria-no-unsolved-guardrail.yaml" \
    --out-dir "$tmp_dir/stage5n-gematria-solved-fixture-cuda-reporting" \
    --allow-warnings
"$python_bin" -m libreprimus.cli gematria-solved-fixture-cuda-reporting build-summary \
    --parity-report "$tmp_dir/stage5n-gematria-solved-fixture-cuda-report.yaml" \
    --controlled-expansion-gate "$tmp_dir/stage5n-gematria-controlled-expansion-gate.yaml" \
    --boundary-review "$tmp_dir/stage5n-gematria-cuda-boundary-review.yaml" \
    --result-store-preflight "$tmp_dir/stage5n-gematria-cuda-result-store-preflight.yaml" \
    --no-unsolved-guardrail "$tmp_dir/stage5n-gematria-no-unsolved-guardrail.yaml" \
    --stage5m-summary data/cuda/stage5m-solved-fixture-cuda-parity-summary.yaml \
    --summary-out "$tmp_dir/stage5n-solved-fixture-cuda-reporting-summary.yaml" \
    --out-dir "$tmp_dir/stage5n-gematria-solved-fixture-cuda-reporting" \
    --allow-warnings
"$python_bin" -m libreprimus.cli gematria-solved-fixture-cuda-reporting validate-stage5n \
    --parity-report "$tmp_dir/stage5n-gematria-solved-fixture-cuda-report.yaml" \
    --controlled-expansion-gate "$tmp_dir/stage5n-gematria-controlled-expansion-gate.yaml" \
    --boundary-review "$tmp_dir/stage5n-gematria-cuda-boundary-review.yaml" \
    --result-store-preflight "$tmp_dir/stage5n-gematria-cuda-result-store-preflight.yaml" \
    --no-unsolved-guardrail "$tmp_dir/stage5n-gematria-no-unsolved-guardrail.yaml" \
    --summary "$tmp_dir/stage5n-solved-fixture-cuda-reporting-summary.yaml" \
    --results-dir "$tmp_dir/stage5n-gematria-solved-fixture-cuda-reporting"

echo "Running Stage 5O solved-fixture Gematria CUDA repeat no-GPU-safe/temp output"
"$python_bin" -m libreprimus.cli gematria-solved-fixture-cuda-repeat build-repeat-run-records \
    --stage5m-run-records data/cuda/stage5m-gematria-solved-fixture-cuda-run.yaml \
    --stage5m-parity-records data/cuda/stage5m-gematria-solved-fixture-cuda-parity.yaml \
    --stage5l-native-parity data/cuda/stage5l-gematria-solved-fixture-native-parity.yaml \
    --repeat-run-out "$tmp_dir/stage5o-gematria-solved-fixture-cuda-repeat-run.yaml" \
    --out-dir "$tmp_dir/stage5o-gematria-solved-fixture-cuda-repeat" \
    --allow-warnings
"$python_bin" -m libreprimus.cli gematria-solved-fixture-cuda-repeat run-repeat-verification \
    --repeat-run "$tmp_dir/stage5o-gematria-solved-fixture-cuda-repeat-run.yaml" \
    --repeat-run-out "$tmp_dir/stage5o-gematria-solved-fixture-cuda-repeat-run.yaml" \
    --out-dir "$tmp_dir/stage5o-gematria-solved-fixture-cuda-repeat" \
    --build-dir "$tmp_dir/stage5o-cuda-build" \
    --skip-run \
    --allow-warnings
"$python_bin" -m libreprimus.cli gematria-solved-fixture-cuda-repeat build-repeat-parity-records \
    --repeat-run "$tmp_dir/stage5o-gematria-solved-fixture-cuda-repeat-run.yaml" \
    --repeat-parity-out "$tmp_dir/stage5o-gematria-solved-fixture-cuda-repeat-parity.yaml" \
    --out-dir "$tmp_dir/stage5o-gematria-solved-fixture-cuda-repeat" \
    --allow-warnings
"$python_bin" -m libreprimus.cli gematria-solved-fixture-cuda-repeat build-result-store-preflight \
    --repeat-parity "$tmp_dir/stage5o-gematria-solved-fixture-cuda-repeat-parity.yaml" \
    --stage4p-summary data/research/stage4p-result-store-score-summary-unification-summary.yaml \
    --result-store-preflight-out "$tmp_dir/stage5o-gematria-cuda-result-store-preflight.yaml" \
    --out-dir "$tmp_dir/stage5o-gematria-solved-fixture-cuda-repeat" \
    --allow-warnings
"$python_bin" -m libreprimus.cli gematria-solved-fixture-cuda-repeat build-score-summary-preflight \
    --repeat-parity "$tmp_dir/stage5o-gematria-solved-fixture-cuda-repeat-parity.yaml" \
    --score-summary-preflight-out "$tmp_dir/stage5o-gematria-cuda-score-summary-preflight.yaml" \
    --out-dir "$tmp_dir/stage5o-gematria-solved-fixture-cuda-repeat" \
    --allow-warnings
"$python_bin" -m libreprimus.cli gematria-solved-fixture-cuda-repeat build-expansion-decision \
    --repeat-parity "$tmp_dir/stage5o-gematria-solved-fixture-cuda-repeat-parity.yaml" \
    --result-store-preflight "$tmp_dir/stage5o-gematria-cuda-result-store-preflight.yaml" \
    --score-summary-preflight "$tmp_dir/stage5o-gematria-cuda-score-summary-preflight.yaml" \
    --expansion-decision-out "$tmp_dir/stage5o-gematria-cuda-expansion-decision.yaml" \
    --out-dir "$tmp_dir/stage5o-gematria-solved-fixture-cuda-repeat" \
    --allow-warnings
"$python_bin" -m libreprimus.cli gematria-solved-fixture-cuda-repeat build-summary \
    --repeat-run "$tmp_dir/stage5o-gematria-solved-fixture-cuda-repeat-run.yaml" \
    --repeat-parity "$tmp_dir/stage5o-gematria-solved-fixture-cuda-repeat-parity.yaml" \
    --result-store-preflight "$tmp_dir/stage5o-gematria-cuda-result-store-preflight.yaml" \
    --score-summary-preflight "$tmp_dir/stage5o-gematria-cuda-score-summary-preflight.yaml" \
    --expansion-decision "$tmp_dir/stage5o-gematria-cuda-expansion-decision.yaml" \
    --stage5m-summary data/cuda/stage5m-solved-fixture-cuda-parity-summary.yaml \
    --stage5n-summary data/cuda/stage5n-solved-fixture-cuda-reporting-summary.yaml \
    --summary-out "$tmp_dir/stage5o-repeat-verification-result-store-summary.yaml" \
    --out-dir "$tmp_dir/stage5o-gematria-solved-fixture-cuda-repeat" \
    --allow-warnings
"$python_bin" -m libreprimus.cli gematria-solved-fixture-cuda-repeat validate-stage5o \
    --repeat-run "$tmp_dir/stage5o-gematria-solved-fixture-cuda-repeat-run.yaml" \
    --repeat-parity "$tmp_dir/stage5o-gematria-solved-fixture-cuda-repeat-parity.yaml" \
    --result-store-preflight "$tmp_dir/stage5o-gematria-cuda-result-store-preflight.yaml" \
    --score-summary-preflight "$tmp_dir/stage5o-gematria-cuda-score-summary-preflight.yaml" \
    --expansion-decision "$tmp_dir/stage5o-gematria-cuda-expansion-decision.yaml" \
    --summary "$tmp_dir/stage5o-repeat-verification-result-store-summary.yaml" \
    --results-dir "$tmp_dir/stage5o-gematria-solved-fixture-cuda-repeat"

"$python_bin" -m libreprimus.cli gematria-cuda-result-store build-result-store-integration \
    --repeat-parity data/cuda/stage5o-gematria-solved-fixture-cuda-repeat-parity.yaml \
    --result-store-integration-out "$tmp_dir/stage5p-gematria-cuda-result-store-integration.yaml" \
    --out-dir "$tmp_dir/stage5p-gematria-cuda-result-store" \
    --allow-warnings
"$python_bin" -m libreprimus.cli gematria-cuda-result-store build-score-summary-integration \
    --result-store-integration "$tmp_dir/stage5p-gematria-cuda-result-store-integration.yaml" \
    --score-summary-integration-out "$tmp_dir/stage5p-gematria-cuda-score-summary-integration.yaml" \
    --out-dir "$tmp_dir/stage5p-gematria-cuda-result-store" \
    --allow-warnings
"$python_bin" -m libreprimus.cli gematria-cuda-result-store build-method-status-impact \
    --result-store-integration "$tmp_dir/stage5p-gematria-cuda-result-store-integration.yaml" \
    --method-status-impact-out "$tmp_dir/stage5p-gematria-cuda-method-status-impact.yaml" \
    --out-dir "$tmp_dir/stage5p-gematria-cuda-result-store" \
    --allow-warnings
"$python_bin" -m libreprimus.cli gematria-cuda-result-store build-generated-body-policy \
    --generated-body-policy-out "$tmp_dir/stage5p-gematria-cuda-generated-body-policy.yaml" \
    --out-dir "$tmp_dir/stage5p-gematria-cuda-result-store" \
    --allow-warnings
"$python_bin" -m libreprimus.cli gematria-cuda-result-store build-controlled-expansion-candidates \
    --controlled-expansion-candidates-out "$tmp_dir/stage5p-gematria-controlled-expansion-candidates.yaml" \
    --out-dir "$tmp_dir/stage5p-gematria-cuda-result-store" \
    --allow-warnings
"$python_bin" -m libreprimus.cli gematria-cuda-result-store build-summary \
    --result-store-integration "$tmp_dir/stage5p-gematria-cuda-result-store-integration.yaml" \
    --score-summary-integration "$tmp_dir/stage5p-gematria-cuda-score-summary-integration.yaml" \
    --method-status-impact "$tmp_dir/stage5p-gematria-cuda-method-status-impact.yaml" \
    --generated-body-policy "$tmp_dir/stage5p-gematria-cuda-generated-body-policy.yaml" \
    --controlled-expansion-candidates "$tmp_dir/stage5p-gematria-controlled-expansion-candidates.yaml" \
    --summary-out "$tmp_dir/stage5p-cuda-result-store-integration-summary.yaml" \
    --out-dir "$tmp_dir/stage5p-gematria-cuda-result-store" \
    --allow-warnings
"$python_bin" -m libreprimus.cli gematria-cuda-result-store validate-stage5p \
    --result-store-integration "$tmp_dir/stage5p-gematria-cuda-result-store-integration.yaml" \
    --score-summary-integration "$tmp_dir/stage5p-gematria-cuda-score-summary-integration.yaml" \
    --method-status-impact "$tmp_dir/stage5p-gematria-cuda-method-status-impact.yaml" \
    --generated-body-policy "$tmp_dir/stage5p-gematria-cuda-generated-body-policy.yaml" \
    --controlled-expansion-candidates "$tmp_dir/stage5p-gematria-controlled-expansion-candidates.yaml" \
    --summary "$tmp_dir/stage5p-cuda-result-store-integration-summary.yaml" \
    --results-dir "$tmp_dir/stage5p-gematria-cuda-result-store"

echo "Running Stage 5Q Gematria expansion candidate mapping no-GPU-safe/temp output"
"$python_bin" -m libreprimus.cli gematria-expansion-candidate-mapping build-candidate-inventory \
    --candidate-inventory-out "$tmp_dir/stage5q-gematria-expansion-candidate-inventory.yaml" \
    --out-dir "$tmp_dir/stage5q-gematria-expansion-candidate-mapping" \
    --allow-warnings
"$python_bin" -m libreprimus.cli gematria-expansion-candidate-mapping build-token-mapping \
    --candidate-inventory "$tmp_dir/stage5q-gematria-expansion-candidate-inventory.yaml" \
    --token-mapping-out "$tmp_dir/stage5q-gematria-expansion-token-mapping.yaml" \
    --out-dir "$tmp_dir/stage5q-gematria-expansion-candidate-mapping" \
    --allow-warnings
"$python_bin" -m libreprimus.cli gematria-expansion-candidate-mapping build-native-parity \
    --token-mapping "$tmp_dir/stage5q-gematria-expansion-token-mapping.yaml" \
    --native-parity-out "$tmp_dir/stage5q-gematria-expansion-native-parity.yaml" \
    --out-dir "$tmp_dir/stage5q-gematria-expansion-candidate-mapping" \
    --allow-warnings
"$python_bin" -m libreprimus.cli gematria-expansion-candidate-mapping build-result-store-preflight \
    --token-mapping "$tmp_dir/stage5q-gematria-expansion-token-mapping.yaml" \
    --native-parity "$tmp_dir/stage5q-gematria-expansion-native-parity.yaml" \
    --result-store-preflight-out "$tmp_dir/stage5q-gematria-expansion-result-store-preflight.yaml" \
    --out-dir "$tmp_dir/stage5q-gematria-expansion-candidate-mapping" \
    --allow-warnings
"$python_bin" -m libreprimus.cli gematria-expansion-candidate-mapping build-expansion-gate \
    --candidate-inventory "$tmp_dir/stage5q-gematria-expansion-candidate-inventory.yaml" \
    --token-mapping "$tmp_dir/stage5q-gematria-expansion-token-mapping.yaml" \
    --native-parity "$tmp_dir/stage5q-gematria-expansion-native-parity.yaml" \
    --result-store-preflight "$tmp_dir/stage5q-gematria-expansion-result-store-preflight.yaml" \
    --expansion-gate-out "$tmp_dir/stage5q-gematria-expansion-gate.yaml" \
    --out-dir "$tmp_dir/stage5q-gematria-expansion-candidate-mapping" \
    --allow-warnings
"$python_bin" -m libreprimus.cli gematria-expansion-candidate-mapping build-summary \
    --candidate-inventory "$tmp_dir/stage5q-gematria-expansion-candidate-inventory.yaml" \
    --token-mapping "$tmp_dir/stage5q-gematria-expansion-token-mapping.yaml" \
    --native-parity "$tmp_dir/stage5q-gematria-expansion-native-parity.yaml" \
    --result-store-preflight "$tmp_dir/stage5q-gematria-expansion-result-store-preflight.yaml" \
    --expansion-gate "$tmp_dir/stage5q-gematria-expansion-gate.yaml" \
    --summary-out "$tmp_dir/stage5q-expansion-candidate-mapping-summary.yaml" \
    --out-dir "$tmp_dir/stage5q-gematria-expansion-candidate-mapping" \
    --allow-warnings
"$python_bin" -m libreprimus.cli gematria-expansion-candidate-mapping validate-stage5q \
    --candidate-inventory "$tmp_dir/stage5q-gematria-expansion-candidate-inventory.yaml" \
    --token-mapping "$tmp_dir/stage5q-gematria-expansion-token-mapping.yaml" \
    --native-parity "$tmp_dir/stage5q-gematria-expansion-native-parity.yaml" \
    --result-store-preflight "$tmp_dir/stage5q-gematria-expansion-result-store-preflight.yaml" \
    --expansion-gate "$tmp_dir/stage5q-gematria-expansion-gate.yaml" \
    --summary "$tmp_dir/stage5q-expansion-candidate-mapping-summary.yaml" \
    --results-dir "$tmp_dir/stage5q-gematria-expansion-candidate-mapping"

echo "Running Stage 5R expanded solved-fixture CUDA parity no-GPU-safe/temp output"
"$python_bin" -m libreprimus.cli gematria-expanded-solved-fixture-cuda build-run-records \
    --run-records-out "$tmp_dir/stage5r-gematria-expanded-solved-fixture-cuda-run.yaml" \
    --out-dir "$tmp_dir/stage5r-gematria-expanded-solved-fixture-cuda" \
    --allow-warnings
"$python_bin" -m libreprimus.cli gematria-expanded-solved-fixture-cuda run-cuda-parity \
    --run-records "$tmp_dir/stage5r-gematria-expanded-solved-fixture-cuda-run.yaml" \
    --run-records-out "$tmp_dir/stage5r-gematria-expanded-solved-fixture-cuda-run.yaml" \
    --out-dir "$tmp_dir/stage5r-gematria-expanded-solved-fixture-cuda" \
    --build-dir "$tmp_dir/stage5r-cuda-build" \
    --skip-run \
    --allow-warnings
"$python_bin" -m libreprimus.cli gematria-expanded-solved-fixture-cuda build-parity-records \
    --run-records "$tmp_dir/stage5r-gematria-expanded-solved-fixture-cuda-run.yaml" \
    --parity-records-out "$tmp_dir/stage5r-gematria-expanded-solved-fixture-cuda-parity.yaml" \
    --out-dir "$tmp_dir/stage5r-gematria-expanded-solved-fixture-cuda" \
    --allow-warnings
"$python_bin" -m libreprimus.cli gematria-expanded-solved-fixture-cuda build-boundary-records \
    --run-records "$tmp_dir/stage5r-gematria-expanded-solved-fixture-cuda-run.yaml" \
    --parity-records "$tmp_dir/stage5r-gematria-expanded-solved-fixture-cuda-parity.yaml" \
    --boundaries-out "$tmp_dir/stage5r-gematria-expanded-solved-fixture-cuda-boundary.yaml" \
    --out-dir "$tmp_dir/stage5r-gematria-expanded-solved-fixture-cuda" \
    --allow-warnings
"$python_bin" -m libreprimus.cli gematria-expanded-solved-fixture-cuda build-result-store-preflight \
    --parity-records "$tmp_dir/stage5r-gematria-expanded-solved-fixture-cuda-parity.yaml" \
    --result-store-preflight-out "$tmp_dir/stage5r-gematria-expanded-solved-fixture-result-store-preflight.yaml" \
    --out-dir "$tmp_dir/stage5r-gematria-expanded-solved-fixture-cuda" \
    --allow-warnings
"$python_bin" -m libreprimus.cli gematria-expanded-solved-fixture-cuda build-score-summary-preflight \
    --parity-records "$tmp_dir/stage5r-gematria-expanded-solved-fixture-cuda-parity.yaml" \
    --score-summary-preflight-out "$tmp_dir/stage5r-gematria-expanded-solved-fixture-score-summary-preflight.yaml" \
    --out-dir "$tmp_dir/stage5r-gematria-expanded-solved-fixture-cuda" \
    --allow-warnings
"$python_bin" -m libreprimus.cli gematria-expanded-solved-fixture-cuda build-summary \
    --run-records "$tmp_dir/stage5r-gematria-expanded-solved-fixture-cuda-run.yaml" \
    --parity-records "$tmp_dir/stage5r-gematria-expanded-solved-fixture-cuda-parity.yaml" \
    --boundaries "$tmp_dir/stage5r-gematria-expanded-solved-fixture-cuda-boundary.yaml" \
    --result-store-preflight "$tmp_dir/stage5r-gematria-expanded-solved-fixture-result-store-preflight.yaml" \
    --score-summary-preflight "$tmp_dir/stage5r-gematria-expanded-solved-fixture-score-summary-preflight.yaml" \
    --summary-out "$tmp_dir/stage5r-expanded-solved-fixture-cuda-parity-summary.yaml" \
    --out-dir "$tmp_dir/stage5r-gematria-expanded-solved-fixture-cuda" \
    --allow-warnings
"$python_bin" -m libreprimus.cli gematria-expanded-solved-fixture-cuda validate-stage5r \
    --run-records "$tmp_dir/stage5r-gematria-expanded-solved-fixture-cuda-run.yaml" \
    --parity-records "$tmp_dir/stage5r-gematria-expanded-solved-fixture-cuda-parity.yaml" \
    --boundaries "$tmp_dir/stage5r-gematria-expanded-solved-fixture-cuda-boundary.yaml" \
    --result-store-preflight "$tmp_dir/stage5r-gematria-expanded-solved-fixture-result-store-preflight.yaml" \
    --score-summary-preflight "$tmp_dir/stage5r-gematria-expanded-solved-fixture-score-summary-preflight.yaml" \
    --summary "$tmp_dir/stage5r-expanded-solved-fixture-cuda-parity-summary.yaml" \
    --results-dir "$tmp_dir/stage5r-gematria-expanded-solved-fixture-cuda"

echo "Running Stage 5S expanded CUDA result-store integration temp output"
"$python_bin" -m libreprimus.cli gematria-expanded-cuda-result-store build-parity-report \
    --stage5r-parity "$tmp_dir/stage5r-gematria-expanded-solved-fixture-cuda-parity.yaml" \
    --stage5r-run "$tmp_dir/stage5r-gematria-expanded-solved-fixture-cuda-run.yaml" \
    --parity-report-out "$tmp_dir/stage5s-gematria-expanded-cuda-parity-report.yaml" \
    --out-dir "$tmp_dir/stage5s-gematria-expanded-cuda-result-store" \
    --allow-warnings
"$python_bin" -m libreprimus.cli gematria-expanded-cuda-result-store build-result-store-integration \
    --parity-report "$tmp_dir/stage5s-gematria-expanded-cuda-parity-report.yaml" \
    --result-store-integration-out "$tmp_dir/stage5s-gematria-expanded-cuda-result-store-integration.yaml" \
    --out-dir "$tmp_dir/stage5s-gematria-expanded-cuda-result-store" \
    --allow-warnings
"$python_bin" -m libreprimus.cli gematria-expanded-cuda-result-store build-score-summary-integration \
    --result-store-integration "$tmp_dir/stage5s-gematria-expanded-cuda-result-store-integration.yaml" \
    --score-summary-integration-out "$tmp_dir/stage5s-gematria-expanded-cuda-score-summary-integration.yaml" \
    --out-dir "$tmp_dir/stage5s-gematria-expanded-cuda-result-store" \
    --allow-warnings
"$python_bin" -m libreprimus.cli gematria-expanded-cuda-result-store build-method-status-impact \
    --method-status-impact-out "$tmp_dir/stage5s-gematria-expanded-cuda-method-status-impact.yaml" \
    --out-dir "$tmp_dir/stage5s-gematria-expanded-cuda-result-store" \
    --allow-warnings
"$python_bin" -m libreprimus.cli gematria-expanded-cuda-result-store build-generated-body-policy \
    --generated-body-policy-out "$tmp_dir/stage5s-gematria-expanded-cuda-generated-body-policy.yaml" \
    --out-dir "$tmp_dir/stage5s-gematria-expanded-cuda-result-store" \
    --allow-warnings
"$python_bin" -m libreprimus.cli gematria-expanded-cuda-result-store build-boundary-review \
    --boundary-review-out "$tmp_dir/stage5s-gematria-expanded-cuda-boundary-review.yaml" \
    --out-dir "$tmp_dir/stage5s-gematria-expanded-cuda-result-store" \
    --allow-warnings
"$python_bin" -m libreprimus.cli gematria-expanded-cuda-result-store build-next-step-decision \
    --next-step-decision-out "$tmp_dir/stage5s-gematria-expanded-cuda-next-step-decision.yaml" \
    --out-dir "$tmp_dir/stage5s-gematria-expanded-cuda-result-store" \
    --allow-warnings
"$python_bin" -m libreprimus.cli gematria-expanded-cuda-result-store build-summary \
    --parity-report "$tmp_dir/stage5s-gematria-expanded-cuda-parity-report.yaml" \
    --result-store-integration "$tmp_dir/stage5s-gematria-expanded-cuda-result-store-integration.yaml" \
    --score-summary-integration "$tmp_dir/stage5s-gematria-expanded-cuda-score-summary-integration.yaml" \
    --method-status-impact "$tmp_dir/stage5s-gematria-expanded-cuda-method-status-impact.yaml" \
    --generated-body-policy "$tmp_dir/stage5s-gematria-expanded-cuda-generated-body-policy.yaml" \
    --boundary-review "$tmp_dir/stage5s-gematria-expanded-cuda-boundary-review.yaml" \
    --next-step-decision "$tmp_dir/stage5s-gematria-expanded-cuda-next-step-decision.yaml" \
    --stage5r-summary "$tmp_dir/stage5r-expanded-solved-fixture-cuda-parity-summary.yaml" \
    --summary-out "$tmp_dir/stage5s-expanded-cuda-result-store-integration-summary.yaml" \
    --out-dir "$tmp_dir/stage5s-gematria-expanded-cuda-result-store" \
    --allow-warnings
"$python_bin" -m libreprimus.cli gematria-expanded-cuda-result-store validate-stage5s \
    --parity-report "$tmp_dir/stage5s-gematria-expanded-cuda-parity-report.yaml" \
    --result-store-integration "$tmp_dir/stage5s-gematria-expanded-cuda-result-store-integration.yaml" \
    --score-summary-integration "$tmp_dir/stage5s-gematria-expanded-cuda-score-summary-integration.yaml" \
    --method-status-impact "$tmp_dir/stage5s-gematria-expanded-cuda-method-status-impact.yaml" \
    --generated-body-policy "$tmp_dir/stage5s-gematria-expanded-cuda-generated-body-policy.yaml" \
    --boundary-review "$tmp_dir/stage5s-gematria-expanded-cuda-boundary-review.yaml" \
    --next-step-decision "$tmp_dir/stage5s-gematria-expanded-cuda-next-step-decision.yaml" \
    --summary "$tmp_dir/stage5s-expanded-cuda-result-store-integration-summary.yaml" \
    --results-dir "$tmp_dir/stage5s-gematria-expanded-cuda-result-store"

echo "Running Stage 5T CUDA solved-family readiness temp output"
"$python_bin" -m libreprimus.cli cuda-solved-family-readiness build-solved-family-inventory \
    --fixture-root data/fixtures \
    --solved-family-inventory-out "$tmp_dir/stage5t-solved-family-cuda-inventory.yaml" \
    --out-dir "$tmp_dir/stage5t-cuda-solved-family-readiness" \
    --allow-warnings
"$python_bin" -m libreprimus.cli cuda-solved-family-readiness build-parity-matrix \
    --solved-family-inventory "$tmp_dir/stage5t-solved-family-cuda-inventory.yaml" \
    --stage5m-summary "$tmp_dir/stage5m-solved-fixture-cuda-parity-summary.yaml" \
    --stage5r-summary "$tmp_dir/stage5r-expanded-solved-fixture-cuda-parity-summary.yaml" \
    --parity-matrix-out "$tmp_dir/stage5t-solved-family-cuda-parity-matrix.yaml" \
    --out-dir "$tmp_dir/stage5t-cuda-solved-family-readiness" \
    --allow-warnings
"$python_bin" -m libreprimus.cli cuda-solved-family-readiness build-kernel-readiness \
    --parity-matrix "$tmp_dir/stage5t-solved-family-cuda-parity-matrix.yaml" \
    --kernel-readiness-out "$tmp_dir/stage5t-cuda-kernel-readiness.yaml" \
    --out-dir "$tmp_dir/stage5t-cuda-solved-family-readiness" \
    --allow-warnings
"$python_bin" -m libreprimus.cli cuda-solved-family-readiness build-batch-abi-gaps \
    --batch-abi-gaps-out "$tmp_dir/stage5t-cuda-candidate-batch-abi-gaps.yaml" \
    --out-dir "$tmp_dir/stage5t-cuda-solved-family-readiness" \
    --allow-warnings
"$python_bin" -m libreprimus.cli cuda-solved-family-readiness build-benchmark-readiness \
    --benchmark-readiness-out "$tmp_dir/stage5t-cuda-benchmark-readiness.yaml" \
    --out-dir "$tmp_dir/stage5t-cuda-solved-family-readiness" \
    --allow-warnings
"$python_bin" -m libreprimus.cli cuda-solved-family-readiness build-no-unsolved-guardrail \
    --no-unsolved-guardrail-out "$tmp_dir/stage5t-cuda-no-unsolved-guardrail-review.yaml" \
    --out-dir "$tmp_dir/stage5t-cuda-solved-family-readiness" \
    --allow-warnings
"$python_bin" -m libreprimus.cli cuda-solved-family-readiness build-next-stage-decision \
    --batch-abi-gaps "$tmp_dir/stage5t-cuda-candidate-batch-abi-gaps.yaml" \
    --next-stage-decision-out "$tmp_dir/stage5t-cuda-next-stage-decision.yaml" \
    --out-dir "$tmp_dir/stage5t-cuda-solved-family-readiness" \
    --allow-warnings
"$python_bin" -m libreprimus.cli cuda-solved-family-readiness build-summary \
    --solved-family-inventory "$tmp_dir/stage5t-solved-family-cuda-inventory.yaml" \
    --parity-matrix "$tmp_dir/stage5t-solved-family-cuda-parity-matrix.yaml" \
    --kernel-readiness "$tmp_dir/stage5t-cuda-kernel-readiness.yaml" \
    --batch-abi-gaps "$tmp_dir/stage5t-cuda-candidate-batch-abi-gaps.yaml" \
    --benchmark-readiness "$tmp_dir/stage5t-cuda-benchmark-readiness.yaml" \
    --no-unsolved-guardrail "$tmp_dir/stage5t-cuda-no-unsolved-guardrail-review.yaml" \
    --next-stage-decision "$tmp_dir/stage5t-cuda-next-stage-decision.yaml" \
    --stage5s-summary "$tmp_dir/stage5s-expanded-cuda-result-store-integration-summary.yaml" \
    --summary-out "$tmp_dir/stage5t-cuda-solved-family-readiness-summary.yaml" \
    --out-dir "$tmp_dir/stage5t-cuda-solved-family-readiness" \
    --allow-warnings
"$python_bin" -m libreprimus.cli cuda-solved-family-readiness validate-stage5t \
    --solved-family-inventory "$tmp_dir/stage5t-solved-family-cuda-inventory.yaml" \
    --parity-matrix "$tmp_dir/stage5t-solved-family-cuda-parity-matrix.yaml" \
    --kernel-readiness "$tmp_dir/stage5t-cuda-kernel-readiness.yaml" \
    --batch-abi-gaps "$tmp_dir/stage5t-cuda-candidate-batch-abi-gaps.yaml" \
    --benchmark-readiness "$tmp_dir/stage5t-cuda-benchmark-readiness.yaml" \
    --no-unsolved-guardrail "$tmp_dir/stage5t-cuda-no-unsolved-guardrail-review.yaml" \
    --next-stage-decision "$tmp_dir/stage5t-cuda-next-stage-decision.yaml" \
    --summary "$tmp_dir/stage5t-cuda-solved-family-readiness-summary.yaml" \
    --results-dir "$tmp_dir/stage5t-cuda-solved-family-readiness"

echo "Running Stage 5U CUDA candidate batch ABI temp output"
"$python_bin" -m libreprimus.cli cuda-candidate-batch-abi build-candidate-batch-abi \
    --candidate-batch-abi-out "$tmp_dir/stage5u-candidate-batch-abi.yaml" \
    --out-dir "$tmp_dir/stage5u-cuda-candidate-batch-abi" \
    --allow-warnings
"$python_bin" -m libreprimus.cli cuda-candidate-batch-abi build-token-buffer-contract \
    --token-buffer-contract-out "$tmp_dir/stage5u-token-buffer-contract.yaml" \
    --out-dir "$tmp_dir/stage5u-cuda-candidate-batch-abi" \
    --allow-warnings
"$python_bin" -m libreprimus.cli cuda-candidate-batch-abi build-transform-parameter-contract \
    --transform-parameter-contract-out "$tmp_dir/stage5u-transform-parameter-contract.yaml" \
    --out-dir "$tmp_dir/stage5u-cuda-candidate-batch-abi" \
    --allow-warnings
"$python_bin" -m libreprimus.cli cuda-candidate-batch-abi build-key-schedule-contract \
    --key-schedule-contract-out "$tmp_dir/stage5u-key-schedule-contract.yaml" \
    --out-dir "$tmp_dir/stage5u-cuda-candidate-batch-abi" \
    --allow-warnings
"$python_bin" -m libreprimus.cli cuda-candidate-batch-abi build-stream-schedule-contract \
    --stream-schedule-contract-out "$tmp_dir/stage5u-stream-schedule-contract.yaml" \
    --out-dir "$tmp_dir/stage5u-cuda-candidate-batch-abi" \
    --allow-warnings
"$python_bin" -m libreprimus.cli cuda-candidate-batch-abi build-score-vector-contract \
    --score-vector-contract-out "$tmp_dir/stage5u-score-vector-contract.yaml" \
    --out-dir "$tmp_dir/stage5u-cuda-candidate-batch-abi" \
    --allow-warnings
"$python_bin" -m libreprimus.cli cuda-candidate-batch-abi build-topk-output-contract \
    --topk-output-contract-out "$tmp_dir/stage5u-topk-output-contract.yaml" \
    --out-dir "$tmp_dir/stage5u-cuda-candidate-batch-abi" \
    --allow-warnings
"$python_bin" -m libreprimus.cli cuda-candidate-batch-abi build-backend-surface-contract \
    --backend-surface-contract-out "$tmp_dir/stage5u-backend-surface-contract.yaml" \
    --out-dir "$tmp_dir/stage5u-cuda-candidate-batch-abi" \
    --allow-warnings
"$python_bin" -m libreprimus.cli cuda-candidate-batch-abi build-result-store-compatibility \
    --result-store-compatibility-out "$tmp_dir/stage5u-result-store-compatibility.yaml" \
    --out-dir "$tmp_dir/stage5u-cuda-candidate-batch-abi" \
    --allow-warnings
"$python_bin" -m libreprimus.cli cuda-candidate-batch-abi build-gap-closure \
    --stage5t-gaps "$tmp_dir/stage5t-cuda-candidate-batch-abi-gaps.yaml" \
    --gap-closure-out "$tmp_dir/stage5u-abi-gap-closure.yaml" \
    --out-dir "$tmp_dir/stage5u-cuda-candidate-batch-abi" \
    --allow-warnings
"$python_bin" -m libreprimus.cli cuda-candidate-batch-abi build-next-stage-decision \
    --gap-closure "$tmp_dir/stage5u-abi-gap-closure.yaml" \
    --next-stage-decision-out "$tmp_dir/stage5u-next-stage-decision.yaml" \
    --out-dir "$tmp_dir/stage5u-cuda-candidate-batch-abi" \
    --allow-warnings
"$python_bin" -m libreprimus.cli cuda-candidate-batch-abi build-summary \
    --candidate-batch-abi "$tmp_dir/stage5u-candidate-batch-abi.yaml" \
    --token-buffer-contract "$tmp_dir/stage5u-token-buffer-contract.yaml" \
    --transform-parameter-contract "$tmp_dir/stage5u-transform-parameter-contract.yaml" \
    --key-schedule-contract "$tmp_dir/stage5u-key-schedule-contract.yaml" \
    --stream-schedule-contract "$tmp_dir/stage5u-stream-schedule-contract.yaml" \
    --score-vector-contract "$tmp_dir/stage5u-score-vector-contract.yaml" \
    --topk-output-contract "$tmp_dir/stage5u-topk-output-contract.yaml" \
    --backend-surface-contract "$tmp_dir/stage5u-backend-surface-contract.yaml" \
    --result-store-compatibility "$tmp_dir/stage5u-result-store-compatibility.yaml" \
    --gap-closure "$tmp_dir/stage5u-abi-gap-closure.yaml" \
    --next-stage-decision "$tmp_dir/stage5u-next-stage-decision.yaml" \
    --stage5t-gaps "$tmp_dir/stage5t-cuda-candidate-batch-abi-gaps.yaml" \
    --stage5t-summary "$tmp_dir/stage5t-cuda-solved-family-readiness-summary.yaml" \
    --summary-out "$tmp_dir/stage5u-candidate-batch-abi-summary.yaml" \
    --out-dir "$tmp_dir/stage5u-cuda-candidate-batch-abi" \
    --allow-warnings
"$python_bin" -m libreprimus.cli cuda-candidate-batch-abi validate-stage5u \
    --candidate-batch-abi "$tmp_dir/stage5u-candidate-batch-abi.yaml" \
    --token-buffer-contract "$tmp_dir/stage5u-token-buffer-contract.yaml" \
    --transform-parameter-contract "$tmp_dir/stage5u-transform-parameter-contract.yaml" \
    --key-schedule-contract "$tmp_dir/stage5u-key-schedule-contract.yaml" \
    --stream-schedule-contract "$tmp_dir/stage5u-stream-schedule-contract.yaml" \
    --score-vector-contract "$tmp_dir/stage5u-score-vector-contract.yaml" \
    --topk-output-contract "$tmp_dir/stage5u-topk-output-contract.yaml" \
    --backend-surface-contract "$tmp_dir/stage5u-backend-surface-contract.yaml" \
    --result-store-compatibility "$tmp_dir/stage5u-result-store-compatibility.yaml" \
    --gap-closure "$tmp_dir/stage5u-abi-gap-closure.yaml" \
    --next-stage-decision "$tmp_dir/stage5u-next-stage-decision.yaml" \
    --summary "$tmp_dir/stage5u-candidate-batch-abi-summary.yaml" \
    --results-dir "$tmp_dir/stage5u-cuda-candidate-batch-abi"

echo "Running Stage 5V native Candidate Batch ABI conformance temp output"
"$python_bin" -m libreprimus.cli native-candidate-batch-conformance build-adapter-records \
    --adapter-records-out "$tmp_dir/stage5v-native-candidate-batch-adapter.yaml" \
    --out-dir "$tmp_dir/stage5v-native-candidate-batch-conformance" \
    --allow-warnings
"$python_bin" -m libreprimus.cli native-candidate-batch-conformance build-conformance-fixtures \
    --conformance-fixtures-out "$tmp_dir/stage5v-candidate-batch-conformance-fixtures.yaml" \
    --out-dir "$tmp_dir/stage5v-native-candidate-batch-conformance" \
    --allow-warnings
"$python_bin" -m libreprimus.cli native-candidate-batch-conformance run-native-conformance \
    --conformance-fixtures "$tmp_dir/stage5v-candidate-batch-conformance-fixtures.yaml" \
    --out-dir "$tmp_dir/stage5v-native-candidate-batch-conformance" \
    --allow-warnings
"$python_bin" -m libreprimus.cli native-candidate-batch-conformance build-token-buffer-conformance \
    --conformance-fixtures "$tmp_dir/stage5v-candidate-batch-conformance-fixtures.yaml" \
    --token-buffer-conformance-out "$tmp_dir/stage5v-token-buffer-conformance.yaml" \
    --out-dir "$tmp_dir/stage5v-native-candidate-batch-conformance" \
    --allow-warnings
"$python_bin" -m libreprimus.cli native-candidate-batch-conformance build-schedule-conformance \
    --schedule-conformance-out "$tmp_dir/stage5v-schedule-conformance.yaml" \
    --out-dir "$tmp_dir/stage5v-native-candidate-batch-conformance" \
    --allow-warnings
"$python_bin" -m libreprimus.cli native-candidate-batch-conformance build-score-vector-conformance \
    --score-vector-conformance-out "$tmp_dir/stage5v-score-vector-conformance.yaml" \
    --out-dir "$tmp_dir/stage5v-native-candidate-batch-conformance" \
    --allow-warnings
"$python_bin" -m libreprimus.cli native-candidate-batch-conformance build-topk-conformance \
    --topk-conformance-out "$tmp_dir/stage5v-topk-conformance.yaml" \
    --out-dir "$tmp_dir/stage5v-native-candidate-batch-conformance" \
    --allow-warnings
"$python_bin" -m libreprimus.cli native-candidate-batch-conformance build-result-store-conformance \
    --result-store-conformance-out "$tmp_dir/stage5v-native-conformance-result-store.yaml" \
    --out-dir "$tmp_dir/stage5v-native-candidate-batch-conformance" \
    --allow-warnings
"$python_bin" -m libreprimus.cli native-candidate-batch-conformance build-implementation-status \
    --implementation-status-out "$tmp_dir/stage5v-abi-implementation-status.yaml" \
    --out-dir "$tmp_dir/stage5v-native-candidate-batch-conformance" \
    --allow-warnings
"$python_bin" -m libreprimus.cli native-candidate-batch-conformance build-next-stage-decision \
    --next-stage-decision-out "$tmp_dir/stage5v-next-stage-decision.yaml" \
    --out-dir "$tmp_dir/stage5v-native-candidate-batch-conformance" \
    --allow-warnings
"$python_bin" -m libreprimus.cli native-candidate-batch-conformance build-summary \
    --adapter-records "$tmp_dir/stage5v-native-candidate-batch-adapter.yaml" \
    --conformance-fixtures "$tmp_dir/stage5v-candidate-batch-conformance-fixtures.yaml" \
    --token-buffer-conformance "$tmp_dir/stage5v-token-buffer-conformance.yaml" \
    --schedule-conformance "$tmp_dir/stage5v-schedule-conformance.yaml" \
    --score-vector-conformance "$tmp_dir/stage5v-score-vector-conformance.yaml" \
    --topk-conformance "$tmp_dir/stage5v-topk-conformance.yaml" \
    --result-store-conformance "$tmp_dir/stage5v-native-conformance-result-store.yaml" \
    --implementation-status "$tmp_dir/stage5v-abi-implementation-status.yaml" \
    --next-stage-decision "$tmp_dir/stage5v-next-stage-decision.yaml" \
    --summary-out "$tmp_dir/stage5v-native-candidate-batch-conformance-summary.yaml" \
    --out-dir "$tmp_dir/stage5v-native-candidate-batch-conformance" \
    --allow-warnings
"$python_bin" -m libreprimus.cli native-candidate-batch-conformance validate-stage5v \
    --adapter-records "$tmp_dir/stage5v-native-candidate-batch-adapter.yaml" \
    --conformance-fixtures "$tmp_dir/stage5v-candidate-batch-conformance-fixtures.yaml" \
    --token-buffer-conformance "$tmp_dir/stage5v-token-buffer-conformance.yaml" \
    --schedule-conformance "$tmp_dir/stage5v-schedule-conformance.yaml" \
    --score-vector-conformance "$tmp_dir/stage5v-score-vector-conformance.yaml" \
    --topk-conformance "$tmp_dir/stage5v-topk-conformance.yaml" \
    --result-store-conformance "$tmp_dir/stage5v-native-conformance-result-store.yaml" \
    --implementation-status "$tmp_dir/stage5v-abi-implementation-status.yaml" \
    --next-stage-decision "$tmp_dir/stage5v-next-stage-decision.yaml" \
    --summary "$tmp_dir/stage5v-native-candidate-batch-conformance-summary.yaml" \
    --results-dir "$tmp_dir/stage5v-native-candidate-batch-conformance"

echo "Running Stage 5W prime-minus-one native contract temp output"
"$python_bin" -m libreprimus.cli prime-minus-one-native-contract build-source-inventory \
    --source-inventory-out "$tmp_dir/stage5w-prime-minus-one-source-inventory.yaml" \
    --out-dir "$tmp_dir/stage5w-prime-minus-one-native-contract" \
    --allow-warnings
"$python_bin" -m libreprimus.cli prime-minus-one-native-contract build-stream-contract \
    --stream-contract-out "$tmp_dir/stage5w-prime-minus-one-stream-contract.yaml" \
    --out-dir "$tmp_dir/stage5w-prime-minus-one-native-contract" \
    --allow-warnings
"$python_bin" -m libreprimus.cli prime-minus-one-native-contract build-prime-schedule \
    --prime-schedule-out "$tmp_dir/stage5w-prime-minus-one-schedule.yaml" \
    --out-dir "$tmp_dir/stage5w-prime-minus-one-native-contract" \
    --allow-warnings
"$python_bin" -m libreprimus.cli prime-minus-one-native-contract build-candidate-batch-mapping \
    --candidate-batch-mapping-out "$tmp_dir/stage5w-prime-minus-one-candidate-batch-mapping.yaml" \
    --out-dir "$tmp_dir/stage5w-prime-minus-one-native-contract" \
    --allow-warnings
"$python_bin" -m libreprimus.cli prime-minus-one-native-contract build-native-parity-preparation \
    --native-parity-preparation-out "$tmp_dir/stage5w-prime-minus-one-native-parity-preparation.yaml" \
    --out-dir "$tmp_dir/stage5w-prime-minus-one-native-contract" \
    --allow-warnings
"$python_bin" -m libreprimus.cli prime-minus-one-native-contract build-result-store-preflight \
    --result-store-preflight-out "$tmp_dir/stage5w-prime-minus-one-result-store-preflight.yaml" \
    --out-dir "$tmp_dir/stage5w-prime-minus-one-native-contract" \
    --allow-warnings
"$python_bin" -m libreprimus.cli prime-minus-one-native-contract build-guardrails \
    --guardrail-out "$tmp_dir/stage5w-prime-minus-one-guardrail.yaml" \
    --out-dir "$tmp_dir/stage5w-prime-minus-one-native-contract" \
    --allow-warnings
"$python_bin" -m libreprimus.cli prime-minus-one-native-contract build-next-stage-decision \
    --next-stage-decision-out "$tmp_dir/stage5w-prime-minus-one-next-stage-decision.yaml" \
    --out-dir "$tmp_dir/stage5w-prime-minus-one-native-contract" \
    --allow-warnings
"$python_bin" -m libreprimus.cli prime-minus-one-native-contract build-summary \
    --source-inventory "$tmp_dir/stage5w-prime-minus-one-source-inventory.yaml" \
    --stream-contract "$tmp_dir/stage5w-prime-minus-one-stream-contract.yaml" \
    --prime-schedule "$tmp_dir/stage5w-prime-minus-one-schedule.yaml" \
    --candidate-batch-mapping "$tmp_dir/stage5w-prime-minus-one-candidate-batch-mapping.yaml" \
    --native-parity-preparation "$tmp_dir/stage5w-prime-minus-one-native-parity-preparation.yaml" \
    --result-store-preflight "$tmp_dir/stage5w-prime-minus-one-result-store-preflight.yaml" \
    --guardrail "$tmp_dir/stage5w-prime-minus-one-guardrail.yaml" \
    --next-stage-decision "$tmp_dir/stage5w-prime-minus-one-next-stage-decision.yaml" \
    --summary-out "$tmp_dir/stage5w-prime-minus-one-native-contract-summary.yaml" \
    --out-dir "$tmp_dir/stage5w-prime-minus-one-native-contract" \
    --allow-warnings
"$python_bin" -m libreprimus.cli prime-minus-one-native-contract validate-stage5w \
    --source-inventory "$tmp_dir/stage5w-prime-minus-one-source-inventory.yaml" \
    --stream-contract "$tmp_dir/stage5w-prime-minus-one-stream-contract.yaml" \
    --prime-schedule "$tmp_dir/stage5w-prime-minus-one-schedule.yaml" \
    --candidate-batch-mapping "$tmp_dir/stage5w-prime-minus-one-candidate-batch-mapping.yaml" \
    --native-parity-preparation "$tmp_dir/stage5w-prime-minus-one-native-parity-preparation.yaml" \
    --result-store-preflight "$tmp_dir/stage5w-prime-minus-one-result-store-preflight.yaml" \
    --guardrail "$tmp_dir/stage5w-prime-minus-one-guardrail.yaml" \
    --next-stage-decision "$tmp_dir/stage5w-prime-minus-one-next-stage-decision.yaml" \
    --summary "$tmp_dir/stage5w-prime-minus-one-native-contract-summary.yaml" \
    --results-dir "$tmp_dir/stage5w-prime-minus-one-native-contract"

echo "Running Stage 5X prime-minus-one native parity temp output"
"$python_bin" -m libreprimus.cli prime-minus-one-native-parity build-run-records \
    --native-run-out "$tmp_dir/stage5x-prime-minus-one-native-run.yaml" \
    --out-dir "$tmp_dir/stage5x-prime-minus-one-native-parity" \
    --allow-warnings
"$python_bin" -m libreprimus.cli prime-minus-one-native-parity build-parity-records \
    --native-run "$tmp_dir/stage5x-prime-minus-one-native-run.yaml" \
    --native-parity-out "$tmp_dir/stage5x-prime-minus-one-native-parity.yaml" \
    --out-dir "$tmp_dir/stage5x-prime-minus-one-native-parity" \
    --allow-warnings
"$python_bin" -m libreprimus.cli prime-minus-one-native-parity build-result-store-preflight \
    --native-parity "$tmp_dir/stage5x-prime-minus-one-native-parity.yaml" \
    --result-store-preflight-out "$tmp_dir/stage5x-prime-minus-one-native-result-store-preflight.yaml" \
    --out-dir "$tmp_dir/stage5x-prime-minus-one-native-parity" \
    --allow-warnings
"$python_bin" -m libreprimus.cli prime-minus-one-native-parity build-score-summary-preflight \
    --native-parity "$tmp_dir/stage5x-prime-minus-one-native-parity.yaml" \
    --score-summary-preflight-out "$tmp_dir/stage5x-prime-minus-one-native-score-summary-preflight.yaml" \
    --out-dir "$tmp_dir/stage5x-prime-minus-one-native-parity" \
    --allow-warnings
"$python_bin" -m libreprimus.cli prime-minus-one-native-parity build-full-p56-blocker \
    --full-p56-blocker-out "$tmp_dir/stage5x-prime-minus-one-full-p56-blocker.yaml" \
    --out-dir "$tmp_dir/stage5x-prime-minus-one-native-parity" \
    --allow-warnings
"$python_bin" -m libreprimus.cli prime-minus-one-native-parity build-guardrails \
    --guardrail-out "$tmp_dir/stage5x-prime-minus-one-native-guardrail.yaml" \
    --out-dir "$tmp_dir/stage5x-prime-minus-one-native-parity" \
    --allow-warnings
"$python_bin" -m libreprimus.cli prime-minus-one-native-parity build-next-stage-decision \
    --native-parity "$tmp_dir/stage5x-prime-minus-one-native-parity.yaml" \
    --next-stage-decision-out "$tmp_dir/stage5x-prime-minus-one-native-next-stage-decision.yaml" \
    --out-dir "$tmp_dir/stage5x-prime-minus-one-native-parity" \
    --allow-warnings
"$python_bin" -m libreprimus.cli prime-minus-one-native-parity build-summary \
    --native-run "$tmp_dir/stage5x-prime-minus-one-native-run.yaml" \
    --native-parity "$tmp_dir/stage5x-prime-minus-one-native-parity.yaml" \
    --result-store-preflight "$tmp_dir/stage5x-prime-minus-one-native-result-store-preflight.yaml" \
    --score-summary-preflight "$tmp_dir/stage5x-prime-minus-one-native-score-summary-preflight.yaml" \
    --full-p56-blocker "$tmp_dir/stage5x-prime-minus-one-full-p56-blocker.yaml" \
    --guardrail "$tmp_dir/stage5x-prime-minus-one-native-guardrail.yaml" \
    --next-stage-decision "$tmp_dir/stage5x-prime-minus-one-native-next-stage-decision.yaml" \
    --summary-out "$tmp_dir/stage5x-prime-minus-one-native-parity-summary.yaml" \
    --out-dir "$tmp_dir/stage5x-prime-minus-one-native-parity" \
    --allow-warnings
"$python_bin" -m libreprimus.cli prime-minus-one-native-parity validate-stage5x \
    --native-run "$tmp_dir/stage5x-prime-minus-one-native-run.yaml" \
    --native-parity "$tmp_dir/stage5x-prime-minus-one-native-parity.yaml" \
    --result-store-preflight "$tmp_dir/stage5x-prime-minus-one-native-result-store-preflight.yaml" \
    --score-summary-preflight "$tmp_dir/stage5x-prime-minus-one-native-score-summary-preflight.yaml" \
    --full-p56-blocker "$tmp_dir/stage5x-prime-minus-one-full-p56-blocker.yaml" \
    --guardrail "$tmp_dir/stage5x-prime-minus-one-native-guardrail.yaml" \
    --next-stage-decision "$tmp_dir/stage5x-prime-minus-one-native-next-stage-decision.yaml" \
    --summary "$tmp_dir/stage5x-prime-minus-one-native-parity-summary.yaml" \
    --results-dir "$tmp_dir/stage5x-prime-minus-one-native-parity"

echo "Running Stage 5Y prime-minus-one native reporting temp output"
"$python_bin" -m libreprimus.cli prime-minus-one-native-reporting build-parity-report \
    --parity-report-out "$tmp_dir/stage5y-prime-minus-one-native-parity-report.yaml" \
    --out-dir "$tmp_dir/stage5y-prime-minus-one-native-reporting" \
    --allow-warnings
"$python_bin" -m libreprimus.cli prime-minus-one-native-reporting build-result-store-integration \
    --parity-report "$tmp_dir/stage5y-prime-minus-one-native-parity-report.yaml" \
    --result-store-integration-out "$tmp_dir/stage5y-prime-minus-one-native-result-store-integration.yaml" \
    --out-dir "$tmp_dir/stage5y-prime-minus-one-native-reporting" \
    --allow-warnings
"$python_bin" -m libreprimus.cli prime-minus-one-native-reporting build-score-summary-integration \
    --parity-report "$tmp_dir/stage5y-prime-minus-one-native-parity-report.yaml" \
    --score-summary-integration-out "$tmp_dir/stage5y-prime-minus-one-native-score-summary-integration.yaml" \
    --out-dir "$tmp_dir/stage5y-prime-minus-one-native-reporting" \
    --allow-warnings
"$python_bin" -m libreprimus.cli prime-minus-one-native-reporting build-method-status-impact \
    --method-status-impact-out "$tmp_dir/stage5y-prime-minus-one-native-method-status-impact.yaml" \
    --out-dir "$tmp_dir/stage5y-prime-minus-one-native-reporting" \
    --allow-warnings
"$python_bin" -m libreprimus.cli prime-minus-one-native-reporting build-generated-body-policy \
    --generated-body-policy-out "$tmp_dir/stage5y-prime-minus-one-generated-body-policy.yaml" \
    --out-dir "$tmp_dir/stage5y-prime-minus-one-native-reporting" \
    --allow-warnings
"$python_bin" -m libreprimus.cli prime-minus-one-native-reporting build-full-p56-blocker-preservation \
    --full-p56-blocker-preservation-out "$tmp_dir/stage5y-prime-minus-one-full-p56-blocker-preservation.yaml" \
    --out-dir "$tmp_dir/stage5y-prime-minus-one-native-reporting" \
    --allow-warnings
"$python_bin" -m libreprimus.cli prime-minus-one-native-reporting build-cuda-contract-readiness-gate \
    --parity-report "$tmp_dir/stage5y-prime-minus-one-native-parity-report.yaml" \
    --result-store-integration "$tmp_dir/stage5y-prime-minus-one-native-result-store-integration.yaml" \
    --score-summary-integration "$tmp_dir/stage5y-prime-minus-one-native-score-summary-integration.yaml" \
    --cuda-contract-readiness-gate-out "$tmp_dir/stage5y-prime-minus-one-cuda-contract-readiness-gate.yaml" \
    --out-dir "$tmp_dir/stage5y-prime-minus-one-native-reporting" \
    --allow-warnings
"$python_bin" -m libreprimus.cli prime-minus-one-native-reporting build-scored-experiment-readiness \
    --scored-experiment-readiness-out "$tmp_dir/stage5y-bounded-scored-experiment-readiness.yaml" \
    --out-dir "$tmp_dir/stage5y-prime-minus-one-native-reporting" \
    --allow-warnings
"$python_bin" -m libreprimus.cli prime-minus-one-native-reporting build-guardrails \
    --guardrail-out "$tmp_dir/stage5y-prime-minus-one-native-reporting-guardrail.yaml" \
    --out-dir "$tmp_dir/stage5y-prime-minus-one-native-reporting" \
    --allow-warnings
"$python_bin" -m libreprimus.cli prime-minus-one-native-reporting build-next-stage-decision \
    --cuda-contract-readiness-gate "$tmp_dir/stage5y-prime-minus-one-cuda-contract-readiness-gate.yaml" \
    --next-stage-decision-out "$tmp_dir/stage5y-prime-minus-one-native-reporting-next-stage-decision.yaml" \
    --out-dir "$tmp_dir/stage5y-prime-minus-one-native-reporting" \
    --allow-warnings
"$python_bin" -m libreprimus.cli prime-minus-one-native-reporting build-summary \
    --parity-report "$tmp_dir/stage5y-prime-minus-one-native-parity-report.yaml" \
    --result-store-integration "$tmp_dir/stage5y-prime-minus-one-native-result-store-integration.yaml" \
    --score-summary-integration "$tmp_dir/stage5y-prime-minus-one-native-score-summary-integration.yaml" \
    --method-status-impact "$tmp_dir/stage5y-prime-minus-one-native-method-status-impact.yaml" \
    --generated-body-policy "$tmp_dir/stage5y-prime-minus-one-generated-body-policy.yaml" \
    --full-p56-blocker-preservation "$tmp_dir/stage5y-prime-minus-one-full-p56-blocker-preservation.yaml" \
    --cuda-contract-readiness-gate "$tmp_dir/stage5y-prime-minus-one-cuda-contract-readiness-gate.yaml" \
    --scored-experiment-readiness "$tmp_dir/stage5y-bounded-scored-experiment-readiness.yaml" \
    --guardrail "$tmp_dir/stage5y-prime-minus-one-native-reporting-guardrail.yaml" \
    --next-stage-decision "$tmp_dir/stage5y-prime-minus-one-native-reporting-next-stage-decision.yaml" \
    --summary-out "$tmp_dir/stage5y-prime-minus-one-native-reporting-summary.yaml" \
    --out-dir "$tmp_dir/stage5y-prime-minus-one-native-reporting" \
    --allow-warnings
"$python_bin" -m libreprimus.cli prime-minus-one-native-reporting validate-stage5y \
    --parity-report "$tmp_dir/stage5y-prime-minus-one-native-parity-report.yaml" \
    --result-store-integration "$tmp_dir/stage5y-prime-minus-one-native-result-store-integration.yaml" \
    --score-summary-integration "$tmp_dir/stage5y-prime-minus-one-native-score-summary-integration.yaml" \
    --method-status-impact "$tmp_dir/stage5y-prime-minus-one-native-method-status-impact.yaml" \
    --generated-body-policy "$tmp_dir/stage5y-prime-minus-one-generated-body-policy.yaml" \
    --full-p56-blocker-preservation "$tmp_dir/stage5y-prime-minus-one-full-p56-blocker-preservation.yaml" \
    --cuda-contract-readiness-gate "$tmp_dir/stage5y-prime-minus-one-cuda-contract-readiness-gate.yaml" \
    --scored-experiment-readiness "$tmp_dir/stage5y-bounded-scored-experiment-readiness.yaml" \
    --guardrail "$tmp_dir/stage5y-prime-minus-one-native-reporting-guardrail.yaml" \
    --next-stage-decision "$tmp_dir/stage5y-prime-minus-one-native-reporting-next-stage-decision.yaml" \
    --summary "$tmp_dir/stage5y-prime-minus-one-native-reporting-summary.yaml" \
    --results-dir "$tmp_dir/stage5y-prime-minus-one-native-reporting"

echo "Running Stage 5Z prime-minus-one CUDA contract temp output"
"$python_bin" -m libreprimus.cli prime-minus-one-cuda-contract build-contract-records \
    --cuda-contract-out "$tmp_dir/stage5z-prime-minus-one-cuda-contract.yaml" \
    --out-dir "$tmp_dir/stage5z-prime-minus-one-cuda-contract" \
    --allow-warnings
"$python_bin" -m libreprimus.cli prime-minus-one-cuda-contract build-kernel-abi \
    --kernel-abi-out "$tmp_dir/stage5z-prime-minus-one-cuda-kernel-abi.yaml" \
    --out-dir "$tmp_dir/stage5z-prime-minus-one-cuda-contract" \
    --allow-warnings
"$python_bin" -m libreprimus.cli prime-minus-one-cuda-contract build-host-runner-contract \
    --host-runner-contract-out "$tmp_dir/stage5z-prime-minus-one-cuda-host-runner-contract.yaml" \
    --out-dir "$tmp_dir/stage5z-prime-minus-one-cuda-contract" \
    --allow-warnings
"$python_bin" -m libreprimus.cli prime-minus-one-cuda-contract build-buffer-contract \
    --buffer-contract-out "$tmp_dir/stage5z-prime-minus-one-cuda-buffer-contract.yaml" \
    --out-dir "$tmp_dir/stage5z-prime-minus-one-cuda-contract" \
    --allow-warnings
"$python_bin" -m libreprimus.cli prime-minus-one-cuda-contract build-validation-vectors \
    --validation-vectors-out "$tmp_dir/stage5z-prime-minus-one-cuda-validation-vectors.yaml" \
    --out-dir "$tmp_dir/stage5z-prime-minus-one-cuda-contract" \
    --allow-warnings
"$python_bin" -m libreprimus.cli prime-minus-one-cuda-contract build-future-parity-plan \
    --future-parity-plan-out "$tmp_dir/stage5z-prime-minus-one-cuda-future-parity-plan.yaml" \
    --out-dir "$tmp_dir/stage5z-prime-minus-one-cuda-contract" \
    --allow-warnings
"$python_bin" -m libreprimus.cli prime-minus-one-cuda-contract build-result-store-compatibility \
    --result-store-compatibility-out "$tmp_dir/stage5z-prime-minus-one-cuda-result-store-compatibility.yaml" \
    --out-dir "$tmp_dir/stage5z-prime-minus-one-cuda-contract" \
    --allow-warnings
"$python_bin" -m libreprimus.cli prime-minus-one-cuda-contract build-full-p56-blocker \
    --full-p56-blocker-out "$tmp_dir/stage5z-prime-minus-one-cuda-full-p56-blocker.yaml" \
    --out-dir "$tmp_dir/stage5z-prime-minus-one-cuda-contract" \
    --allow-warnings
"$python_bin" -m libreprimus.cli prime-minus-one-cuda-contract build-scored-experiment-deferral \
    --scored-experiment-deferral-out "$tmp_dir/stage5z-prime-minus-one-scored-experiment-deferral.yaml" \
    --out-dir "$tmp_dir/stage5z-prime-minus-one-cuda-contract" \
    --allow-warnings
"$python_bin" -m libreprimus.cli prime-minus-one-cuda-contract build-implementation-readiness-gate \
    --implementation-readiness-out "$tmp_dir/stage5z-prime-minus-one-cuda-implementation-readiness-gate.yaml" \
    --out-dir "$tmp_dir/stage5z-prime-minus-one-cuda-contract" \
    --allow-warnings
"$python_bin" -m libreprimus.cli prime-minus-one-cuda-contract build-next-stage-decision \
    --next-stage-decision-out "$tmp_dir/stage5z-prime-minus-one-cuda-next-stage-decision.yaml" \
    --out-dir "$tmp_dir/stage5z-prime-minus-one-cuda-contract" \
    --allow-warnings
"$python_bin" -m libreprimus.cli prime-minus-one-cuda-contract build-summary \
    --cuda-contract "$tmp_dir/stage5z-prime-minus-one-cuda-contract.yaml" \
    --kernel-abi "$tmp_dir/stage5z-prime-minus-one-cuda-kernel-abi.yaml" \
    --host-runner-contract "$tmp_dir/stage5z-prime-minus-one-cuda-host-runner-contract.yaml" \
    --buffer-contract "$tmp_dir/stage5z-prime-minus-one-cuda-buffer-contract.yaml" \
    --validation-vectors "$tmp_dir/stage5z-prime-minus-one-cuda-validation-vectors.yaml" \
    --future-parity-plan "$tmp_dir/stage5z-prime-minus-one-cuda-future-parity-plan.yaml" \
    --result-store-compatibility "$tmp_dir/stage5z-prime-minus-one-cuda-result-store-compatibility.yaml" \
    --full-p56-blocker "$tmp_dir/stage5z-prime-minus-one-cuda-full-p56-blocker.yaml" \
    --scored-experiment-deferral "$tmp_dir/stage5z-prime-minus-one-scored-experiment-deferral.yaml" \
    --implementation-readiness-gate "$tmp_dir/stage5z-prime-minus-one-cuda-implementation-readiness-gate.yaml" \
    --next-stage-decision "$tmp_dir/stage5z-prime-minus-one-cuda-next-stage-decision.yaml" \
    --summary-out "$tmp_dir/stage5z-prime-minus-one-cuda-contract-summary.yaml" \
    --out-dir "$tmp_dir/stage5z-prime-minus-one-cuda-contract" \
    --allow-warnings
"$python_bin" -m libreprimus.cli prime-minus-one-cuda-contract validate-stage5z \
    --cuda-contract "$tmp_dir/stage5z-prime-minus-one-cuda-contract.yaml" \
    --kernel-abi "$tmp_dir/stage5z-prime-minus-one-cuda-kernel-abi.yaml" \
    --host-runner-contract "$tmp_dir/stage5z-prime-minus-one-cuda-host-runner-contract.yaml" \
    --buffer-contract "$tmp_dir/stage5z-prime-minus-one-cuda-buffer-contract.yaml" \
    --validation-vectors "$tmp_dir/stage5z-prime-minus-one-cuda-validation-vectors.yaml" \
    --future-parity-plan "$tmp_dir/stage5z-prime-minus-one-cuda-future-parity-plan.yaml" \
    --result-store-compatibility "$tmp_dir/stage5z-prime-minus-one-cuda-result-store-compatibility.yaml" \
    --full-p56-blocker "$tmp_dir/stage5z-prime-minus-one-cuda-full-p56-blocker.yaml" \
    --scored-experiment-deferral "$tmp_dir/stage5z-prime-minus-one-scored-experiment-deferral.yaml" \
    --implementation-readiness-gate "$tmp_dir/stage5z-prime-minus-one-cuda-implementation-readiness-gate.yaml" \
    --next-stage-decision "$tmp_dir/stage5z-prime-minus-one-cuda-next-stage-decision.yaml" \
    --summary "$tmp_dir/stage5z-prime-minus-one-cuda-contract-summary.yaml" \
    --results-dir "$tmp_dir/stage5z-prime-minus-one-cuda-contract"

echo "Running Stage 5AA prime-minus-one CUDA synthetic temp output"
"$python_bin" -m libreprimus.cli prime-minus-one-cuda-synthetic build-kernel-implementation-records \
    --kernel-implementation-out "$tmp_dir/stage5aa-prime-minus-one-cuda-synthetic-kernel-implementation.yaml" \
    --out-dir "$tmp_dir/stage5aa-prime-minus-one-cuda-synthetic" \
    --allow-warnings
"$python_bin" -m libreprimus.cli prime-minus-one-cuda-synthetic run-synthetic-cuda-parity \
    --cuda-run-out "$tmp_dir/stage5aa-prime-minus-one-cuda-synthetic-run.yaml" \
    --out-dir "$tmp_dir/stage5aa-prime-minus-one-cuda-synthetic" \
    --skip-cuda \
    --allow-warnings
"$python_bin" -m libreprimus.cli prime-minus-one-cuda-synthetic build-parity-records \
    --cuda-run "$tmp_dir/stage5aa-prime-minus-one-cuda-synthetic-run.yaml" \
    --parity-out "$tmp_dir/stage5aa-prime-minus-one-cuda-synthetic-parity.yaml" \
    --out-dir "$tmp_dir/stage5aa-prime-minus-one-cuda-synthetic" \
    --allow-warnings
"$python_bin" -m libreprimus.cli prime-minus-one-cuda-synthetic build-device-subset-audit \
    --device-subset-audit-out "$tmp_dir/stage5aa-prime-minus-one-cuda-device-subset-audit.yaml" \
    --out-dir "$tmp_dir/stage5aa-prime-minus-one-cuda-synthetic" \
    --allow-warnings
"$python_bin" -m libreprimus.cli prime-minus-one-cuda-synthetic build-result-store-preflight \
    --result-store-preflight-out "$tmp_dir/stage5aa-prime-minus-one-cuda-synthetic-result-store-preflight.yaml" \
    --out-dir "$tmp_dir/stage5aa-prime-minus-one-cuda-synthetic" \
    --allow-warnings
"$python_bin" -m libreprimus.cli prime-minus-one-cuda-synthetic build-p56-blocker \
    --p56-blocker-out "$tmp_dir/stage5aa-prime-minus-one-cuda-synthetic-p56-blocker.yaml" \
    --out-dir "$tmp_dir/stage5aa-prime-minus-one-cuda-synthetic" \
    --allow-warnings
"$python_bin" -m libreprimus.cli prime-minus-one-cuda-synthetic build-scored-experiment-deferral \
    --scored-experiment-deferral-out "$tmp_dir/stage5aa-prime-minus-one-cuda-synthetic-scored-experiment-deferral.yaml" \
    --out-dir "$tmp_dir/stage5aa-prime-minus-one-cuda-synthetic" \
    --allow-warnings
"$python_bin" -m libreprimus.cli prime-minus-one-cuda-synthetic build-next-stage-decision \
    --parity "$tmp_dir/stage5aa-prime-minus-one-cuda-synthetic-parity.yaml" \
    --next-stage-decision-out "$tmp_dir/stage5aa-prime-minus-one-cuda-synthetic-next-stage-decision.yaml" \
    --out-dir "$tmp_dir/stage5aa-prime-minus-one-cuda-synthetic" \
    --allow-warnings
"$python_bin" -m libreprimus.cli prime-minus-one-cuda-synthetic build-summary \
    --kernel-implementation "$tmp_dir/stage5aa-prime-minus-one-cuda-synthetic-kernel-implementation.yaml" \
    --cuda-run "$tmp_dir/stage5aa-prime-minus-one-cuda-synthetic-run.yaml" \
    --parity "$tmp_dir/stage5aa-prime-minus-one-cuda-synthetic-parity.yaml" \
    --device-subset-audit "$tmp_dir/stage5aa-prime-minus-one-cuda-device-subset-audit.yaml" \
    --result-store-preflight "$tmp_dir/stage5aa-prime-minus-one-cuda-synthetic-result-store-preflight.yaml" \
    --p56-blocker "$tmp_dir/stage5aa-prime-minus-one-cuda-synthetic-p56-blocker.yaml" \
    --scored-experiment-deferral "$tmp_dir/stage5aa-prime-minus-one-cuda-synthetic-scored-experiment-deferral.yaml" \
    --next-stage-decision "$tmp_dir/stage5aa-prime-minus-one-cuda-synthetic-next-stage-decision.yaml" \
    --summary-out "$tmp_dir/stage5aa-prime-minus-one-cuda-synthetic-summary.yaml" \
    --out-dir "$tmp_dir/stage5aa-prime-minus-one-cuda-synthetic" \
    --allow-warnings
"$python_bin" -m libreprimus.cli prime-minus-one-cuda-synthetic validate-stage5aa \
    --kernel-implementation "$tmp_dir/stage5aa-prime-minus-one-cuda-synthetic-kernel-implementation.yaml" \
    --cuda-run "$tmp_dir/stage5aa-prime-minus-one-cuda-synthetic-run.yaml" \
    --parity "$tmp_dir/stage5aa-prime-minus-one-cuda-synthetic-parity.yaml" \
    --device-subset-audit "$tmp_dir/stage5aa-prime-minus-one-cuda-device-subset-audit.yaml" \
    --result-store-preflight "$tmp_dir/stage5aa-prime-minus-one-cuda-synthetic-result-store-preflight.yaml" \
    --p56-blocker "$tmp_dir/stage5aa-prime-minus-one-cuda-synthetic-p56-blocker.yaml" \
    --scored-experiment-deferral "$tmp_dir/stage5aa-prime-minus-one-cuda-synthetic-scored-experiment-deferral.yaml" \
    --next-stage-decision "$tmp_dir/stage5aa-prime-minus-one-cuda-synthetic-next-stage-decision.yaml" \
    --summary "$tmp_dir/stage5aa-prime-minus-one-cuda-synthetic-summary.yaml" \
    --results-dir "$tmp_dir/stage5aa-prime-minus-one-cuda-synthetic"

echo "Running Stage 5AC prime-minus-one CUDA synthetic reporting temp output"
"$python_bin" -m libreprimus.cli prime-minus-one-cuda-synthetic-reporting build-parity-report \
    --parity-report-out "$tmp_dir/stage5ac-prime-minus-one-cuda-synthetic-parity-report.yaml" \
    --out-dir "$tmp_dir/stage5ac-prime-minus-one-cuda-synthetic-reporting" \
    --allow-warnings
"$python_bin" -m libreprimus.cli prime-minus-one-cuda-synthetic-reporting build-result-store-integration \
    --parity-report "$tmp_dir/stage5ac-prime-minus-one-cuda-synthetic-parity-report.yaml" \
    --result-store-integration-out "$tmp_dir/stage5ac-prime-minus-one-cuda-synthetic-result-store-integration.yaml" \
    --out-dir "$tmp_dir/stage5ac-prime-minus-one-cuda-synthetic-reporting" \
    --allow-warnings
"$python_bin" -m libreprimus.cli prime-minus-one-cuda-synthetic-reporting build-score-summary-integration \
    --parity-report "$tmp_dir/stage5ac-prime-minus-one-cuda-synthetic-parity-report.yaml" \
    --score-summary-integration-out "$tmp_dir/stage5ac-prime-minus-one-cuda-synthetic-score-summary-integration.yaml" \
    --out-dir "$tmp_dir/stage5ac-prime-minus-one-cuda-synthetic-reporting" \
    --allow-warnings
"$python_bin" -m libreprimus.cli prime-minus-one-cuda-synthetic-reporting build-method-status-impact \
    --method-status-impact-out "$tmp_dir/stage5ac-prime-minus-one-cuda-synthetic-method-status-impact.yaml" \
    --out-dir "$tmp_dir/stage5ac-prime-minus-one-cuda-synthetic-reporting" \
    --allow-warnings
"$python_bin" -m libreprimus.cli prime-minus-one-cuda-synthetic-reporting build-generated-body-policy \
    --generated-body-policy-out "$tmp_dir/stage5ac-prime-minus-one-cuda-synthetic-generated-body-policy.yaml" \
    --out-dir "$tmp_dir/stage5ac-prime-minus-one-cuda-synthetic-reporting" \
    --allow-warnings
"$python_bin" -m libreprimus.cli prime-minus-one-cuda-synthetic-reporting build-doc-staleness-validation \
    --doc-staleness-validation-out "$tmp_dir/stage5ac-prime-minus-one-cuda-synthetic-doc-staleness-validation.yaml" \
    --out-dir "$tmp_dir/stage5ac-prime-minus-one-cuda-synthetic-reporting" \
    --allow-warnings
"$python_bin" -m libreprimus.cli prime-minus-one-cuda-synthetic-reporting build-bounded-p56-preflight \
    --parity-report "$tmp_dir/stage5ac-prime-minus-one-cuda-synthetic-parity-report.yaml" \
    --doc-staleness-validation "$tmp_dir/stage5ac-prime-minus-one-cuda-synthetic-doc-staleness-validation.yaml" \
    --bounded-p56-preflight-out "$tmp_dir/stage5ac-bounded-p56-cuda-parity-preflight.yaml" \
    --out-dir "$tmp_dir/stage5ac-prime-minus-one-cuda-synthetic-reporting" \
    --allow-warnings
"$python_bin" -m libreprimus.cli prime-minus-one-cuda-synthetic-reporting build-full-p56-blocker \
    --full-p56-blocker-out "$tmp_dir/stage5ac-prime-minus-one-cuda-synthetic-full-p56-blocker.yaml" \
    --out-dir "$tmp_dir/stage5ac-prime-minus-one-cuda-synthetic-reporting" \
    --allow-warnings
"$python_bin" -m libreprimus.cli prime-minus-one-cuda-synthetic-reporting build-scored-experiment-deferral \
    --scored-experiment-deferral-out "$tmp_dir/stage5ac-prime-minus-one-cuda-synthetic-scored-experiment-deferral.yaml" \
    --out-dir "$tmp_dir/stage5ac-prime-minus-one-cuda-synthetic-reporting" \
    --allow-warnings
"$python_bin" -m libreprimus.cli prime-minus-one-cuda-synthetic-reporting build-next-stage-decision \
    --parity-report "$tmp_dir/stage5ac-prime-minus-one-cuda-synthetic-parity-report.yaml" \
    --bounded-p56-preflight "$tmp_dir/stage5ac-bounded-p56-cuda-parity-preflight.yaml" \
    --doc-staleness-validation "$tmp_dir/stage5ac-prime-minus-one-cuda-synthetic-doc-staleness-validation.yaml" \
    --next-stage-decision-out "$tmp_dir/stage5ac-prime-minus-one-cuda-synthetic-next-stage-decision.yaml" \
    --out-dir "$tmp_dir/stage5ac-prime-minus-one-cuda-synthetic-reporting" \
    --allow-warnings
"$python_bin" -m libreprimus.cli prime-minus-one-cuda-synthetic-reporting build-summary \
    --parity-report "$tmp_dir/stage5ac-prime-minus-one-cuda-synthetic-parity-report.yaml" \
    --result-store-integration "$tmp_dir/stage5ac-prime-minus-one-cuda-synthetic-result-store-integration.yaml" \
    --score-summary-integration "$tmp_dir/stage5ac-prime-minus-one-cuda-synthetic-score-summary-integration.yaml" \
    --method-status-impact "$tmp_dir/stage5ac-prime-minus-one-cuda-synthetic-method-status-impact.yaml" \
    --generated-body-policy "$tmp_dir/stage5ac-prime-minus-one-cuda-synthetic-generated-body-policy.yaml" \
    --bounded-p56-preflight "$tmp_dir/stage5ac-bounded-p56-cuda-parity-preflight.yaml" \
    --full-p56-blocker "$tmp_dir/stage5ac-prime-minus-one-cuda-synthetic-full-p56-blocker.yaml" \
    --scored-experiment-deferral "$tmp_dir/stage5ac-prime-minus-one-cuda-synthetic-scored-experiment-deferral.yaml" \
    --doc-staleness-validation "$tmp_dir/stage5ac-prime-minus-one-cuda-synthetic-doc-staleness-validation.yaml" \
    --next-stage-decision "$tmp_dir/stage5ac-prime-minus-one-cuda-synthetic-next-stage-decision.yaml" \
    --summary-out "$tmp_dir/stage5ac-prime-minus-one-cuda-synthetic-reporting-summary.yaml" \
    --out-dir "$tmp_dir/stage5ac-prime-minus-one-cuda-synthetic-reporting" \
    --allow-warnings
"$python_bin" -m libreprimus.cli prime-minus-one-cuda-synthetic-reporting validate-stage5ac \
    --parity-report "$tmp_dir/stage5ac-prime-minus-one-cuda-synthetic-parity-report.yaml" \
    --result-store-integration "$tmp_dir/stage5ac-prime-minus-one-cuda-synthetic-result-store-integration.yaml" \
    --score-summary-integration "$tmp_dir/stage5ac-prime-minus-one-cuda-synthetic-score-summary-integration.yaml" \
    --method-status-impact "$tmp_dir/stage5ac-prime-minus-one-cuda-synthetic-method-status-impact.yaml" \
    --generated-body-policy "$tmp_dir/stage5ac-prime-minus-one-cuda-synthetic-generated-body-policy.yaml" \
    --bounded-p56-preflight "$tmp_dir/stage5ac-bounded-p56-cuda-parity-preflight.yaml" \
    --full-p56-blocker "$tmp_dir/stage5ac-prime-minus-one-cuda-synthetic-full-p56-blocker.yaml" \
    --scored-experiment-deferral "$tmp_dir/stage5ac-prime-minus-one-cuda-synthetic-scored-experiment-deferral.yaml" \
    --doc-staleness-validation "$tmp_dir/stage5ac-prime-minus-one-cuda-synthetic-doc-staleness-validation.yaml" \
    --next-stage-decision "$tmp_dir/stage5ac-prime-minus-one-cuda-synthetic-next-stage-decision.yaml" \
    --summary "$tmp_dir/stage5ac-prime-minus-one-cuda-synthetic-reporting-summary.yaml" \
    --results-dir "$tmp_dir/stage5ac-prime-minus-one-cuda-synthetic-reporting"

echo "Running Stage 5AD bounded p56 CUDA parity skipped-CUDA temp output"
"$python_bin" -m libreprimus.cli bounded-p56-cuda-parity build-run-records \
    --cuda-run-out "$tmp_dir/stage5ad-bounded-p56-cuda-run.yaml" \
    --out-dir "$tmp_dir/stage5ad-bounded-p56-cuda-parity" \
    --allow-warnings
"$python_bin" -m libreprimus.cli bounded-p56-cuda-parity run-bounded-p56-cuda \
    --cuda-run-out "$tmp_dir/stage5ad-bounded-p56-cuda-run.yaml" \
    --out-dir "$tmp_dir/stage5ad-bounded-p56-cuda-parity" \
    --build-dir "$tmp_dir/stage5ad-bounded-p56-cuda-build" \
    --skip-cuda \
    --allow-warnings
"$python_bin" -m libreprimus.cli bounded-p56-cuda-parity build-parity-records \
    --cuda-run "$tmp_dir/stage5ad-bounded-p56-cuda-run.yaml" \
    --cuda-parity-out "$tmp_dir/stage5ad-bounded-p56-cuda-parity.yaml" \
    --out-dir "$tmp_dir/stage5ad-bounded-p56-cuda-parity" \
    --allow-warnings
"$python_bin" -m libreprimus.cli bounded-p56-cuda-parity build-result-store-preflight \
    --cuda-parity "$tmp_dir/stage5ad-bounded-p56-cuda-parity.yaml" \
    --result-store-preflight-out "$tmp_dir/stage5ad-bounded-p56-cuda-result-store-preflight.yaml" \
    --out-dir "$tmp_dir/stage5ad-bounded-p56-cuda-parity" \
    --allow-warnings
"$python_bin" -m libreprimus.cli bounded-p56-cuda-parity build-score-summary-preflight \
    --cuda-parity "$tmp_dir/stage5ad-bounded-p56-cuda-parity.yaml" \
    --score-summary-preflight-out "$tmp_dir/stage5ad-bounded-p56-cuda-score-summary-preflight.yaml" \
    --out-dir "$tmp_dir/stage5ad-bounded-p56-cuda-parity" \
    --allow-warnings
"$python_bin" -m libreprimus.cli bounded-p56-cuda-parity build-full-p56-blocker \
    --full-p56-blocker-out "$tmp_dir/stage5ad-bounded-p56-cuda-full-p56-blocker.yaml" \
    --out-dir "$tmp_dir/stage5ad-bounded-p56-cuda-parity" \
    --allow-warnings
"$python_bin" -m libreprimus.cli bounded-p56-cuda-parity build-scored-experiment-deferral \
    --scored-experiment-deferral-out "$tmp_dir/stage5ad-bounded-p56-cuda-scored-experiment-deferral.yaml" \
    --out-dir "$tmp_dir/stage5ad-bounded-p56-cuda-parity" \
    --allow-warnings
"$python_bin" -m libreprimus.cli bounded-p56-cuda-parity build-doc-staleness-validation \
    --doc-staleness-validation-out "$tmp_dir/stage5ad-bounded-p56-cuda-doc-staleness-validation.yaml" \
    --out-dir "$tmp_dir/stage5ad-bounded-p56-cuda-parity" \
    --allow-warnings
"$python_bin" -m libreprimus.cli bounded-p56-cuda-parity build-device-subset-audit \
    --device-subset-audit-out "$tmp_dir/stage5ad-bounded-p56-cuda-device-subset-audit.yaml" \
    --out-dir "$tmp_dir/stage5ad-bounded-p56-cuda-parity" \
    --allow-warnings
"$python_bin" -m libreprimus.cli bounded-p56-cuda-parity build-next-stage-decision \
    --cuda-parity "$tmp_dir/stage5ad-bounded-p56-cuda-parity.yaml" \
    --next-stage-decision-out "$tmp_dir/stage5ad-bounded-p56-cuda-next-stage-decision.yaml" \
    --out-dir "$tmp_dir/stage5ad-bounded-p56-cuda-parity" \
    --allow-warnings
"$python_bin" -m libreprimus.cli bounded-p56-cuda-parity build-summary \
    --cuda-run "$tmp_dir/stage5ad-bounded-p56-cuda-run.yaml" \
    --cuda-parity "$tmp_dir/stage5ad-bounded-p56-cuda-parity.yaml" \
    --result-store-preflight "$tmp_dir/stage5ad-bounded-p56-cuda-result-store-preflight.yaml" \
    --score-summary-preflight "$tmp_dir/stage5ad-bounded-p56-cuda-score-summary-preflight.yaml" \
    --full-p56-blocker "$tmp_dir/stage5ad-bounded-p56-cuda-full-p56-blocker.yaml" \
    --scored-experiment-deferral "$tmp_dir/stage5ad-bounded-p56-cuda-scored-experiment-deferral.yaml" \
    --doc-staleness-validation "$tmp_dir/stage5ad-bounded-p56-cuda-doc-staleness-validation.yaml" \
    --device-subset-audit "$tmp_dir/stage5ad-bounded-p56-cuda-device-subset-audit.yaml" \
    --next-stage-decision "$tmp_dir/stage5ad-bounded-p56-cuda-next-stage-decision.yaml" \
    --summary-out "$tmp_dir/stage5ad-bounded-p56-cuda-parity-summary.yaml" \
    --out-dir "$tmp_dir/stage5ad-bounded-p56-cuda-parity" \
    --allow-warnings
"$python_bin" -m libreprimus.cli bounded-p56-cuda-parity validate-stage5ad \
    --cuda-run "$tmp_dir/stage5ad-bounded-p56-cuda-run.yaml" \
    --cuda-parity "$tmp_dir/stage5ad-bounded-p56-cuda-parity.yaml" \
    --result-store-preflight "$tmp_dir/stage5ad-bounded-p56-cuda-result-store-preflight.yaml" \
    --score-summary-preflight "$tmp_dir/stage5ad-bounded-p56-cuda-score-summary-preflight.yaml" \
    --full-p56-blocker "$tmp_dir/stage5ad-bounded-p56-cuda-full-p56-blocker.yaml" \
    --scored-experiment-deferral "$tmp_dir/stage5ad-bounded-p56-cuda-scored-experiment-deferral.yaml" \
    --doc-staleness-validation "$tmp_dir/stage5ad-bounded-p56-cuda-doc-staleness-validation.yaml" \
    --device-subset-audit "$tmp_dir/stage5ad-bounded-p56-cuda-device-subset-audit.yaml" \
    --next-stage-decision "$tmp_dir/stage5ad-bounded-p56-cuda-next-stage-decision.yaml" \
    --summary "$tmp_dir/stage5ad-bounded-p56-cuda-parity-summary.yaml" \
    --results-dir "$tmp_dir/stage5ad-bounded-p56-cuda-parity"

echo "Running Stage 5AD-fix bounded p56 mismatch temp output"
"$python_bin" -m libreprimus.cli bounded-p56-mismatch build-hash-lineage \
    --hash-lineage-out "$tmp_dir/stage5ad-fix-bounded-p56-mismatch-hash-lineage.yaml" \
    --out-dir "$tmp_dir/stage5ad-fix-bounded-p56-mismatch" \
    --allow-warnings
"$python_bin" -m libreprimus.cli bounded-p56-mismatch build-token-trace \
    --token-trace-out "$tmp_dir/stage5ad-fix-bounded-p56-mismatch-token-trace.yaml" \
    --out-dir "$tmp_dir/stage5ad-fix-bounded-p56-mismatch" \
    --allow-warnings
"$python_bin" -m libreprimus.cli bounded-p56-mismatch build-stream-trace \
    --stream-trace-out "$tmp_dir/stage5ad-fix-bounded-p56-mismatch-stream-trace.yaml" \
    --out-dir "$tmp_dir/stage5ad-fix-bounded-p56-mismatch" \
    --allow-warnings
"$python_bin" -m libreprimus.cli bounded-p56-mismatch build-formula-trace \
    --formula-trace-out "$tmp_dir/stage5ad-fix-bounded-p56-mismatch-formula-trace.yaml" \
    --out-dir "$tmp_dir/stage5ad-fix-bounded-p56-mismatch" \
    --allow-warnings
"$python_bin" -m libreprimus.cli bounded-p56-mismatch build-hash-material-trace \
    --hash-material-out "$tmp_dir/stage5ad-fix-bounded-p56-mismatch-hash-material.yaml" \
    --out-dir "$tmp_dir/stage5ad-fix-bounded-p56-mismatch" \
    --allow-warnings
"$python_bin" -m libreprimus.cli bounded-p56-mismatch build-reference-contract \
    --reference-contract-out "$tmp_dir/stage5ad-fix-bounded-p56-mismatch-reference-contract.yaml" \
    --out-dir "$tmp_dir/stage5ad-fix-bounded-p56-mismatch" \
    --allow-warnings
"$python_bin" -m libreprimus.cli bounded-p56-mismatch build-root-cause \
    --root-cause-out "$tmp_dir/stage5ad-fix-bounded-p56-mismatch-root-cause.yaml" \
    --out-dir "$tmp_dir/stage5ad-fix-bounded-p56-mismatch" \
    --allow-warnings
"$python_bin" -m libreprimus.cli bounded-p56-mismatch build-repair-readiness \
    --repair-readiness-out "$tmp_dir/stage5ad-fix-bounded-p56-mismatch-repair-readiness.yaml" \
    --out-dir "$tmp_dir/stage5ad-fix-bounded-p56-mismatch" \
    --allow-warnings
"$python_bin" -m libreprimus.cli bounded-p56-mismatch build-guardrails \
    --guardrail-out "$tmp_dir/stage5ad-fix-bounded-p56-mismatch-guardrail.yaml" \
    --out-dir "$tmp_dir/stage5ad-fix-bounded-p56-mismatch" \
    --allow-warnings
"$python_bin" -m libreprimus.cli bounded-p56-mismatch build-next-stage-decision \
    --next-stage-decision-out "$tmp_dir/stage5ad-fix-bounded-p56-mismatch-next-stage-decision.yaml" \
    --out-dir "$tmp_dir/stage5ad-fix-bounded-p56-mismatch" \
    --allow-warnings
"$python_bin" -m libreprimus.cli bounded-p56-mismatch build-summary \
    --hash-lineage "$tmp_dir/stage5ad-fix-bounded-p56-mismatch-hash-lineage.yaml" \
    --token-trace "$tmp_dir/stage5ad-fix-bounded-p56-mismatch-token-trace.yaml" \
    --stream-trace "$tmp_dir/stage5ad-fix-bounded-p56-mismatch-stream-trace.yaml" \
    --formula-trace "$tmp_dir/stage5ad-fix-bounded-p56-mismatch-formula-trace.yaml" \
    --hash-material "$tmp_dir/stage5ad-fix-bounded-p56-mismatch-hash-material.yaml" \
    --reference-contract "$tmp_dir/stage5ad-fix-bounded-p56-mismatch-reference-contract.yaml" \
    --root-cause "$tmp_dir/stage5ad-fix-bounded-p56-mismatch-root-cause.yaml" \
    --repair-readiness "$tmp_dir/stage5ad-fix-bounded-p56-mismatch-repair-readiness.yaml" \
    --guardrail "$tmp_dir/stage5ad-fix-bounded-p56-mismatch-guardrail.yaml" \
    --next-stage-decision "$tmp_dir/stage5ad-fix-bounded-p56-mismatch-next-stage-decision.yaml" \
    --summary-out "$tmp_dir/stage5ad-fix-bounded-p56-mismatch-summary.yaml" \
    --out-dir "$tmp_dir/stage5ad-fix-bounded-p56-mismatch" \
    --allow-warnings
"$python_bin" -m libreprimus.cli bounded-p56-mismatch validate-stage5ad-fix \
    --hash-lineage "$tmp_dir/stage5ad-fix-bounded-p56-mismatch-hash-lineage.yaml" \
    --token-trace "$tmp_dir/stage5ad-fix-bounded-p56-mismatch-token-trace.yaml" \
    --stream-trace "$tmp_dir/stage5ad-fix-bounded-p56-mismatch-stream-trace.yaml" \
    --formula-trace "$tmp_dir/stage5ad-fix-bounded-p56-mismatch-formula-trace.yaml" \
    --hash-material "$tmp_dir/stage5ad-fix-bounded-p56-mismatch-hash-material.yaml" \
    --reference-contract "$tmp_dir/stage5ad-fix-bounded-p56-mismatch-reference-contract.yaml" \
    --root-cause "$tmp_dir/stage5ad-fix-bounded-p56-mismatch-root-cause.yaml" \
    --repair-readiness "$tmp_dir/stage5ad-fix-bounded-p56-mismatch-repair-readiness.yaml" \
    --guardrail "$tmp_dir/stage5ad-fix-bounded-p56-mismatch-guardrail.yaml" \
    --next-stage-decision "$tmp_dir/stage5ad-fix-bounded-p56-mismatch-next-stage-decision.yaml" \
    --summary "$tmp_dir/stage5ad-fix-bounded-p56-mismatch-summary.yaml" \
    --results-dir "$tmp_dir/stage5ad-fix-bounded-p56-mismatch"

echo "Running Stage 5AE corrected bounded p56 reporting temp output"
"$python_bin" -m libreprimus.cli corrected-bounded-p56-reporting build-formula-parity-report \
    --stage5ad-fix-summary "$tmp_dir/stage5ad-fix-bounded-p56-mismatch-summary.yaml" \
    --formula-parity-report-out "$tmp_dir/stage5ae-corrected-bounded-p56-formula-parity-report.yaml" \
    --out-dir "$tmp_dir/stage5ae-corrected-bounded-p56-reporting" \
    --allow-warnings
"$python_bin" -m libreprimus.cli corrected-bounded-p56-reporting build-reference-contract-repair \
    --reference-contract-repair-out "$tmp_dir/stage5ae-bounded-p56-reference-contract-repair.yaml" \
    --out-dir "$tmp_dir/stage5ae-corrected-bounded-p56-reporting" \
    --allow-warnings
"$python_bin" -m libreprimus.cli corrected-bounded-p56-reporting build-hash-material-policy \
    --hash-material-policy-out "$tmp_dir/stage5ae-hash-material-policy.yaml" \
    --out-dir "$tmp_dir/stage5ae-corrected-bounded-p56-reporting" \
    --allow-warnings
"$python_bin" -m libreprimus.cli corrected-bounded-p56-reporting build-result-store-integration \
    --result-store-integration-out "$tmp_dir/stage5ae-corrected-bounded-p56-result-store-integration.yaml" \
    --out-dir "$tmp_dir/stage5ae-corrected-bounded-p56-reporting" \
    --allow-warnings
"$python_bin" -m libreprimus.cli corrected-bounded-p56-reporting build-score-summary-integration \
    --score-summary-integration-out "$tmp_dir/stage5ae-corrected-bounded-p56-score-summary-integration.yaml" \
    --out-dir "$tmp_dir/stage5ae-corrected-bounded-p56-reporting" \
    --allow-warnings
"$python_bin" -m libreprimus.cli corrected-bounded-p56-reporting build-method-status-impact \
    --method-status-impact-out "$tmp_dir/stage5ae-corrected-bounded-p56-method-status-impact.yaml" \
    --out-dir "$tmp_dir/stage5ae-corrected-bounded-p56-reporting" \
    --allow-warnings
"$python_bin" -m libreprimus.cli corrected-bounded-p56-reporting build-generated-body-policy \
    --generated-body-policy-out "$tmp_dir/stage5ae-corrected-bounded-p56-generated-body-policy.yaml" \
    --out-dir "$tmp_dir/stage5ae-corrected-bounded-p56-reporting" \
    --allow-warnings
"$python_bin" -m libreprimus.cli corrected-bounded-p56-reporting build-full-p56-blocker \
    --full-p56-blocker-out "$tmp_dir/stage5ae-corrected-bounded-p56-full-p56-blocker.yaml" \
    --out-dir "$tmp_dir/stage5ae-corrected-bounded-p56-reporting" \
    --allow-warnings
"$python_bin" -m libreprimus.cli corrected-bounded-p56-reporting build-scored-experiment-deferral \
    --scored-experiment-deferral-out "$tmp_dir/stage5ae-corrected-bounded-p56-scored-experiment-deferral.yaml" \
    --out-dir "$tmp_dir/stage5ae-corrected-bounded-p56-reporting" \
    --allow-warnings
"$python_bin" -m libreprimus.cli corrected-bounded-p56-reporting build-archive-source-lock-deferral \
    --archive-source-lock-deferral-out "$tmp_dir/stage5ae-archive-source-lock-deferral.yaml" \
    --out-dir "$tmp_dir/stage5ae-corrected-bounded-p56-reporting" \
    --allow-warnings
"$python_bin" -m libreprimus.cli corrected-bounded-p56-reporting build-doc-staleness-validation \
    --doc-staleness-validation-out "$tmp_dir/stage5ae-corrected-bounded-p56-doc-staleness-validation.yaml" \
    --out-dir "$tmp_dir/stage5ae-corrected-bounded-p56-reporting" \
    --allow-warnings
"$python_bin" -m libreprimus.cli corrected-bounded-p56-reporting build-next-stage-decision \
    --next-stage-decision-out "$tmp_dir/stage5ae-corrected-bounded-p56-next-stage-decision.yaml" \
    --out-dir "$tmp_dir/stage5ae-corrected-bounded-p56-reporting" \
    --allow-warnings
"$python_bin" -m libreprimus.cli corrected-bounded-p56-reporting build-summary \
    --formula-parity-report "$tmp_dir/stage5ae-corrected-bounded-p56-formula-parity-report.yaml" \
    --reference-contract-repair "$tmp_dir/stage5ae-bounded-p56-reference-contract-repair.yaml" \
    --hash-material-policy "$tmp_dir/stage5ae-hash-material-policy.yaml" \
    --result-store-integration "$tmp_dir/stage5ae-corrected-bounded-p56-result-store-integration.yaml" \
    --score-summary-integration "$tmp_dir/stage5ae-corrected-bounded-p56-score-summary-integration.yaml" \
    --method-status-impact "$tmp_dir/stage5ae-corrected-bounded-p56-method-status-impact.yaml" \
    --generated-body-policy "$tmp_dir/stage5ae-corrected-bounded-p56-generated-body-policy.yaml" \
    --full-p56-blocker "$tmp_dir/stage5ae-corrected-bounded-p56-full-p56-blocker.yaml" \
    --scored-experiment-deferral "$tmp_dir/stage5ae-corrected-bounded-p56-scored-experiment-deferral.yaml" \
    --archive-source-lock-deferral "$tmp_dir/stage5ae-archive-source-lock-deferral.yaml" \
    --doc-staleness-validation "$tmp_dir/stage5ae-corrected-bounded-p56-doc-staleness-validation.yaml" \
    --next-stage-decision "$tmp_dir/stage5ae-corrected-bounded-p56-next-stage-decision.yaml" \
    --summary-out "$tmp_dir/stage5ae-corrected-bounded-p56-reporting-summary.yaml" \
    --out-dir "$tmp_dir/stage5ae-corrected-bounded-p56-reporting" \
    --allow-warnings
"$python_bin" -m libreprimus.cli corrected-bounded-p56-reporting validate-stage5ae \
    --formula-parity-report "$tmp_dir/stage5ae-corrected-bounded-p56-formula-parity-report.yaml" \
    --reference-contract-repair "$tmp_dir/stage5ae-bounded-p56-reference-contract-repair.yaml" \
    --hash-material-policy "$tmp_dir/stage5ae-hash-material-policy.yaml" \
    --result-store-integration "$tmp_dir/stage5ae-corrected-bounded-p56-result-store-integration.yaml" \
    --score-summary-integration "$tmp_dir/stage5ae-corrected-bounded-p56-score-summary-integration.yaml" \
    --method-status-impact "$tmp_dir/stage5ae-corrected-bounded-p56-method-status-impact.yaml" \
    --generated-body-policy "$tmp_dir/stage5ae-corrected-bounded-p56-generated-body-policy.yaml" \
    --full-p56-blocker "$tmp_dir/stage5ae-corrected-bounded-p56-full-p56-blocker.yaml" \
    --scored-experiment-deferral "$tmp_dir/stage5ae-corrected-bounded-p56-scored-experiment-deferral.yaml" \
    --archive-source-lock-deferral "$tmp_dir/stage5ae-archive-source-lock-deferral.yaml" \
    --doc-staleness-validation "$tmp_dir/stage5ae-corrected-bounded-p56-doc-staleness-validation.yaml" \
    --next-stage-decision "$tmp_dir/stage5ae-corrected-bounded-p56-next-stage-decision.yaml" \
    --summary "$tmp_dir/stage5ae-corrected-bounded-p56-reporting-summary.yaml" \
    --results-dir "$tmp_dir/stage5ae-corrected-bounded-p56-reporting"

echo "Running Stage 5AF source harvester temp output"
"$python_bin" -m libreprimus.cli source-harvester validate-manifest \
    --manifest data/source-harvester/stage5af-cicada-source-manifest.yaml \
    --out-dir "$tmp_dir/stage5af-source-harvester"
"$python_bin" -m libreprimus.cli source-harvester plan \
    --manifest data/source-harvester/stage5af-cicada-source-manifest.yaml \
    --out "$tmp_dir/stage5af-source-harvester/harvest_plan.json" \
    --dry-run-summary-out "$tmp_dir/stage5af-harvest-dry-run-summary.yaml" \
    --out-dir "$tmp_dir/stage5af-source-harvester"
"$python_bin" -m libreprimus.cli source-harvester build-bundles \
    --bundle-plan data/source-harvester/stage5af-research-bundle-plan.yaml \
    --out-root "$tmp_dir/stage5af-source-harvester/research_bundles_preview"
"$python_bin" -m libreprimus.cli source-harvester summarize \
    --manifest data/source-harvester/stage5af-cicada-source-manifest.yaml \
    --collection-priorities data/source-harvester/stage5af-source-collection-priorities.yaml \
    --clue-target-categories data/source-harvester/stage5af-clue-target-categories.yaml \
    --bundle-plan data/source-harvester/stage5af-research-bundle-plan.yaml \
    --tool-policy data/source-harvester/stage5af-harvest-tool-policy.yaml \
    --dry-run-summary "$tmp_dir/stage5af-harvest-dry-run-summary.yaml" \
    --next-stage-decision-out "$tmp_dir/stage5af-source-harvester-next-stage-decision.yaml" \
    --summary-out "$tmp_dir/stage5af-source-harvester-summary.yaml" \
    --out "$tmp_dir/stage5af-source-harvester/summary.json"
"$python_bin" -m libreprimus.cli source-harvester validate-stage5af \
    --source-manifest data/source-harvester/stage5af-cicada-source-manifest.yaml \
    --collection-priorities data/source-harvester/stage5af-source-collection-priorities.yaml \
    --clue-target-categories data/source-harvester/stage5af-clue-target-categories.yaml \
    --research-bundle-plan data/source-harvester/stage5af-research-bundle-plan.yaml \
    --tool-policy data/source-harvester/stage5af-harvest-tool-policy.yaml \
    --dry-run-summary "$tmp_dir/stage5af-harvest-dry-run-summary.yaml" \
    --next-stage-decision "$tmp_dir/stage5af-source-harvester-next-stage-decision.yaml" \
    --summary "$tmp_dir/stage5af-source-harvester-summary.yaml" \
    --results-dir "$tmp_dir/stage5af-source-harvester"

echo "Running Stage 5AG local source inventory temp output"
stage5ag_out="$tmp_dir/stage5ag-source-harvester-local"
stage5ag_root="third_party/__stage5ag_ci_missing__"
stage5ag_root_inventory="$tmp_dir/stage5ag-local-source-root-inventory.yaml"
stage5ag_file_summary="$tmp_dir/stage5ag-local-source-file-inventory-summary.yaml"
stage5ag_archive_summary="$tmp_dir/stage5ag-local-archive-inventory-summary.yaml"
stage5ag_hash_summary="$tmp_dir/stage5ag-local-source-hash-inventory-summary.yaml"
stage5ag_linkage="$tmp_dir/stage5ag-manifest-local-linkage.yaml"
stage5ag_extension="$tmp_dir/stage5ag-local-source-manifest-extension.yaml"
stage5ag_candidate="$tmp_dir/stage5ag-source-lock-candidate-summary.yaml"
stage5ag_gap="$tmp_dir/stage5ag-local-source-gap-report.yaml"
stage5ag_bundle="$tmp_dir/stage5ag-research-bundle-readiness.yaml"
stage5ag_guardrail="$tmp_dir/stage5ag-local-source-guardrail.yaml"
stage5ag_decision="$tmp_dir/stage5ag-source-harvester-next-stage-decision.yaml"
stage5ag_summary="$tmp_dir/stage5ag-source-harvester-summary.yaml"
"$python_bin" -m libreprimus.cli source-harvester inventory-local-sources \
    --manifest data/source-harvester/stage5af-cicada-source-manifest.yaml \
    --source-root "$stage5ag_root" \
    --results-dir "$stage5ag_out" \
    --out-root-inventory "$stage5ag_root_inventory" \
    --out-file-summary "$stage5ag_file_summary" \
    --out-archive-summary "$stage5ag_archive_summary" \
    --out-hash-summary "$stage5ag_hash_summary"
"$python_bin" -m libreprimus.cli source-harvester link-local-sources \
    --manifest data/source-harvester/stage5af-cicada-source-manifest.yaml \
    --source-root "$stage5ag_root" \
    --results-dir "$stage5ag_out" \
    --out "$stage5ag_linkage" \
    --out-extension "$stage5ag_extension"
"$python_bin" -m libreprimus.cli source-harvester build-source-lock-candidates \
    --manifest data/source-harvester/stage5af-cicada-source-manifest.yaml \
    --local-linkage "$stage5ag_linkage" \
    --out "$stage5ag_candidate" \
    --gap-report "$stage5ag_gap"
"$python_bin" -m libreprimus.cli source-harvester build-bundle-readiness \
    --bundle-plan data/source-harvester/stage5af-research-bundle-plan.yaml \
    --local-linkage "$stage5ag_linkage" \
    --out "$stage5ag_bundle" \
    --results-dir "$stage5ag_out"
"$python_bin" -m libreprimus.cli source-harvester build-stage5ag-guardrail \
    --source-root "$stage5ag_root" \
    --results-dir "$stage5ag_out" \
    --out "$stage5ag_guardrail"
"$python_bin" -m libreprimus.cli source-harvester build-stage5ag-next-stage-decision \
    --root-inventory "$stage5ag_root_inventory" \
    --local-linkage "$stage5ag_linkage" \
    --bundle-readiness "$stage5ag_bundle" \
    --out "$stage5ag_decision"
"$python_bin" -m libreprimus.cli source-harvester build-stage5ag-summary \
    --root-inventory "$stage5ag_root_inventory" \
    --file-summary "$stage5ag_file_summary" \
    --archive-summary "$stage5ag_archive_summary" \
    --hash-summary "$stage5ag_hash_summary" \
    --local-linkage "$stage5ag_linkage" \
    --candidate-summary "$stage5ag_candidate" \
    --gap-report "$stage5ag_gap" \
    --bundle-readiness "$stage5ag_bundle" \
    --guardrail "$stage5ag_guardrail" \
    --next-stage-decision "$stage5ag_decision" \
    --out "$stage5ag_summary" \
    --results-dir "$stage5ag_out"
"$python_bin" -m libreprimus.cli source-harvester validate-stage5ag \
    --root-inventory "$stage5ag_root_inventory" \
    --file-summary "$stage5ag_file_summary" \
    --archive-summary "$stage5ag_archive_summary" \
    --hash-summary "$stage5ag_hash_summary" \
    --local-linkage "$stage5ag_linkage" \
    --candidate-summary "$stage5ag_candidate" \
    --gap-report "$stage5ag_gap" \
    --bundle-readiness "$stage5ag_bundle" \
    --guardrail "$stage5ag_guardrail" \
    --next-stage-decision "$stage5ag_decision" \
    --summary "$stage5ag_summary" \
    --results-dir "$stage5ag_out"

if [[ -f research-inputs/stage5ai/master_manifest.yaml ]]; then
    echo "Validating Stage 5AI curated research bundle records"
    "$python_bin" -m libreprimus.cli source-harvester validate-stage5ai
else
    echo "Skipping Stage 5AI generated bundle validation; ignored local bundle bodies are absent"
fi
stage5ai_bundle_manifest="research-inputs/stage5ai/master_manifest.yaml"
stage5ai_generated_report="experiments""/results/research-bundles/stage5ai/summary.json"
git check-ignore -q "$stage5ai_bundle_manifest"
git check-ignore -q "$stage5ai_generated_report"

stage5aj_summary_report="experiments""/results/source-harvester-usefulfiles/stage5aj/summary.json"
if [[ -f "$stage5aj_summary_report" ]]; then
    echo "Validating Stage 5AJ UsefulFilesAndIdeas records"
    "$python_bin" -m libreprimus.cli source-harvester validate-stage5aj
else
    echo "Skipping Stage 5AJ generated UsefulFiles validation; ignored local reports are absent"
fi
stage5aj_bundle_manifest="research-inputs/stage5aj/master_manifest.yaml"
stage5aj_cell_index="experiments""/results/source-harvester-usefulfiles/stage5aj/xlsx_cell_metadata_index.jsonl"
stage5aj_important_links="experiments""/results/source-harvester-usefulfiles/stage5aj/important_links_url_index.json"
stage5aj_raw_workbook="third_party/UsefulFilesAndIdeas/LP Excel.xlsx"
git check-ignore -q "$stage5aj_bundle_manifest"
git check-ignore -q "$stage5aj_cell_index"
git check-ignore -q "$stage5aj_important_links"
git check-ignore -q "$stage5aj_raw_workbook"

stage5ak_results_dir="experiments""/results/source-harvester-community-facts/stage5ak"
stage5ak_summary_report="$stage5ak_results_dir/summary.json"
if [[ -f "$stage5ak_summary_report" ]]; then
    echo "Validating Stage 5AK community-facts records"
    "$python_bin" -m libreprimus.cli source-harvester validate-stage5ak \
        --inventory data/source-harvester/stage5ak-community-facts-local-inventory.yaml \
        --attachment-index data/source-harvester/stage5ak-community-facts-attachment-index.yaml \
        --source-card-summary data/source-harvester/stage5ak-community-facts-source-card-summary.yaml \
        --content-index-summary data/source-harvester/stage5ak-community-facts-content-index-summary.yaml \
        --clue-categories data/source-harvester/stage5ak-community-facts-clue-categories.yaml \
        --claim-policy data/source-harvester/stage5ak-community-claim-policy.yaml \
        --claim-records data/source-harvester/stage5ak-community-facts-claim-records.yaml \
        --correction-log data/source-harvester/stage5ak-community-facts-correction-log.yaml \
        --arithmetic-preflight data/source-harvester/stage5ak-community-facts-arithmetic-preflight.yaml \
        --website-update data/source-harvester/stage5ak-website-ingest-update-summary.yaml \
        --deep-research-update data/source-harvester/stage5ak-deep-research-pack-update-summary.yaml \
        --readiness data/source-harvester/stage5ak-research-bundle-readiness.yaml \
        --missing-source-plan data/source-harvester/stage5ak-missing-source-plan-update.yaml \
        --guardrail data/source-harvester/stage5ak-guardrail.yaml \
        --next-stage-decision data/source-harvester/stage5ak-next-stage-decision.yaml \
        --summary data/source-harvester/stage5ak-summary.yaml \
        --results-dir "$stage5ak_results_dir"
else
    echo "Skipping Stage 5AK generated community-facts validation; ignored local reports are absent"
fi
stage5ak_raw_text="third_party/UsefulFilesAndIdeas/community-facts/community-facts-collection.txt"
stage5ak_raw_image="third_party/UsefulFilesAndIdeas/community-facts/1.webp"
stage5ak_generated_claims="experiments""/results/source-harvester-community-facts/stage5ak/community_claim_records.jsonl"
stage5ak_bundle_claims="research-inputs/stage5ak/community_claim_records.jsonl"
stage5ak_handoff="codex-output/stage5ak-codex-completion.md"
git check-ignore -q "$stage5ak_raw_text"
git check-ignore -q "$stage5ak_raw_image"
git check-ignore -q "$stage5ak_generated_claims"
git check-ignore -q "$stage5ak_bundle_claims"
git check-ignore -q "$stage5ak_handoff"

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
