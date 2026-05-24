Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$RepoRoot = Resolve-Path (Join-Path $PSScriptRoot "..\..")
Set-Location $RepoRoot

$Python = if ($env:PYTHON) { $env:PYTHON } elseif (Test-Path ".\.venv\Scripts\python.exe") { ".\.venv\Scripts\python.exe" } else { "python" }
$TempDir = Join-Path ([System.IO.Path]::GetTempPath()) ("libreprimus-consistency-" + [System.Guid]::NewGuid().ToString("N"))
New-Item -ItemType Directory -Path $TempDir | Out-Null

try {
    Write-Host "Running full consistency suite"
    & $Python -m libreprimus.cli consistency check-all --allow-warnings

    Write-Host "Running state-drift consistency checks"
    & $Python -m libreprimus.cli consistency check-state-drift

    Write-Host "Running document staleness checks"
    & $Python -m libreprimus.cli consistency check-doc-staleness `
        --source-of-truth data/project-state/stage5ah-doc-staleness-source-of-truth.yaml `
        --strict

    Write-Host "Running Stage 5AH doc-staleness coverage checks"
    $Stage5AHOut = Join-Path $TempDir "stage5ah-doc-staleness"
    New-Item -ItemType Directory -Path $Stage5AHOut | Out-Null
    & $Python -m libreprimus.cli consistency check-stage-ledger-staleness `
        --expected-latest-stage "Stage 5AK" `
        --expected-next-stage "Stage 5AL" `
        --out (Join-Path $Stage5AHOut "stale_stage_ledger_report.json")
    & $Python -m libreprimus.cli consistency check-operational-file-map-coverage `
        --out (Join-Path $Stage5AHOut "operational_file_map_coverage_report.json")
    & $Python -m libreprimus.cli consistency check-current-next-stage-consistency `
        --expected-latest-stage "Stage 5AK" `
        --expected-next-stage "Stage 5AL" `
        --out (Join-Path $Stage5AHOut "current_next_stage_report.json")
@"
import json
from pathlib import Path
import yaml
from libreprimus.doc_staleness.stage_ledger import stage_ledger_findings_for_text

out = Path(r"$Stage5AHOut")
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
"@ | & $Python -
    & $Python -m libreprimus.cli consistency validate-stage5ah-doc-staleness `
        --source-of-truth data/project-state/stage5ah-doc-staleness-source-of-truth.yaml `
        --findings data/project-state/stage5ah-doc-staleness-findings.yaml `
        --stage-ledger-coverage data/project-state/stage5ah-stage-ledger-coverage.yaml `
        --operational-file-map-coverage data/project-state/stage5ah-operational-file-map-coverage.yaml `
        --next-stage-decision data/project-state/stage5ah-next-stage-decision.yaml `
        --summary data/project-state/stage5ah-doc-staleness-summary.yaml `
        --results-dir $Stage5AHOut

    Write-Host "Validating Stage 3Y research synthesis records"
    & $Python -m libreprimus.cli research-synthesis validate --data-dir data/research --staged-plan docs/roadmap/staged-plan.md

    Write-Host "Validating Stage 4B source-lock triage records"
    & $Python -m libreprimus.cli source-lock-triage validate `
        --promoted-sources data/observations/archive/stage4b-promoted-source-records.yaml `
        --source-health data/locks/third-party/stage4b-source-health-records.yaml `
        --visual-observations data/observations/visual/stage4b-visual-observation-records.yaml `
        --negative-controls data/observations/research/stage4b-negative-control-records.yaml `
        --cookie-source-records data/observations/web/stage4b-cookie-candidate-source-records.yaml `
        --manifest-dir experiments/manifests/stage4b-disabled

    Write-Host "Validating Stage 4C visual annotation records"
    & $Python -m libreprimus.cli visual-annotation validate `
        --task data/observations/visual/stage4c-visual-annotation-tasks.yaml `
        --cuneiform data/observations/visual/stage4c-cuneiform-reading-candidates.yaml `
        --dot data/observations/visual/stage4c-dot-pattern-annotation-tasks.yaml `
        --delimiter data/observations/visual/stage4c-delimiter-annotation-tasks.yaml `
        --negative data/observations/visual/stage4c-visual-negative-control-annotation-tasks.yaml `
        --summary data/observations/visual/stage4c-annotation-pack-summary.yaml

    Write-Host "Running Stage 4D bounded numeric verifier synthetic/temp output"
    $Stage4DOut = Join-Path $TempDir "stage4d-bounded-numeric"
    & $Python -m libreprimus.cli bounded-numeric run `
        --manifest-dir experiments/manifests/stage4b-disabled `
        --stage4b-visual data/observations/visual/stage4b-visual-observation-records.yaml `
        --stage4c-tasks data/observations/visual/stage4c-visual-annotation-tasks.yaml `
        --stage4c-cuneiform data/observations/visual/stage4c-cuneiform-reading-candidates.yaml `
        --stage4c-dot data/observations/visual/stage4c-dot-pattern-annotation-tasks.yaml `
        --stage4c-delimiter data/observations/visual/stage4c-delimiter-annotation-tasks.yaml `
        --stage4c-negative data/observations/visual/stage4c-visual-negative-control-annotation-tasks.yaml `
        --out-dir $Stage4DOut `
        --allow-warnings
    & $Python -m libreprimus.cli bounded-numeric validate --results-dir $Stage4DOut

    Write-Host "Validating Stage 4E source-delta audit records"
    & $Python -m libreprimus.cli source-delta-audit validate `
        --source-delta data/observations/archive/stage4e-cicada-solvers-iddqd-source-delta.yaml `
        --source-health data/locks/third-party/stage4e-cicada-solvers-iddqd-source-health.yaml `
        --image-artifact data/observations/visual/stage4e-image-compression-artifact-observations.yaml `
        --manifest-dir experiments/manifests/stage4e-disabled

    Write-Host "Validating Stage 4F stego/audio fixture records"
    & $Python -m libreprimus.cli stego-fixtures validate `
        --outguess-fixtures data/observations/stego/stage4f-outguess-fixture-source-records.yaml `
        --audio-fixtures data/observations/stego/stage4f-audio-fixture-source-records.yaml `
        --source-health data/locks/third-party/stage4f-stego-fixture-source-health.yaml `
        --toolchain data/observations/stego/stage4f-toolchain-requirements.yaml `
        --manifest-dir experiments/manifests/stego/stage4f-disabled

    Write-Host "Running Stage 4G cookie refresh synthetic/temp output"
    $Stage4GOut = Join-Path $TempDir "stage4g-cookie-refresh"
    $Stage4GSummary = Join-Path $TempDir "stage4g-cookie-refresh-summary.yaml"
    & $Python -m libreprimus.cli cookie-refresh run `
        --manifest experiments/manifests/stage4b-disabled/exp_stage4b_cookie_pack_v2.yaml `
        --candidate-sources data/observations/web/stage4b-cookie-candidate-source-records.yaml `
        --cookie-targets data/observations/web/cookie-hash-records-v0.yaml `
        --out-dir $Stage4GOut `
        --summary-out $Stage4GSummary `
        --allow-warnings
    & $Python -m libreprimus.cli cookie-refresh validate --results-dir $Stage4GOut --summary $Stage4GSummary

    Write-Host "Running Stage 4H CPU batch synthetic/temp output"
    $Stage4HOut = Join-Path $TempDir "stage4h-cpu-batch"
    & $Python -m libreprimus.cli cpu-batch validate-manifest `
        --manifest experiments/manifests/cpu-batch/stage4h-synthetic-smoke-batch.yaml
    & $Python -m libreprimus.cli cpu-batch run `
        --manifest experiments/manifests/cpu-batch/stage4h-synthetic-smoke-batch.yaml `
        --out-dir $Stage4HOut `
        --allow-warnings
    & $Python -m libreprimus.cli cpu-batch adapter-coverage `
        --registry data/transform-registry/cpu-reference-transforms-v0.json `
        --out-dir $Stage4HOut `
        --allow-warnings
    & $Python -m libreprimus.cli cpu-batch validate-results --results-dir $Stage4HOut

    Write-Host "Validating Stage 4I scoring consolidation records"
    $Stage4IOut = Join-Path $TempDir "stage4i-scoring"
    $Stage4IData = Join-Path $TempDir "stage4i-scoring-data"
    & $Python -m libreprimus.cli scoring consolidate `
        --out-dir $Stage4IOut `
        --data-dir $Stage4IData `
        --allow-warnings
    & $Python -m libreprimus.cli scoring validate --data-dir data/scoring
    & $Python -m libreprimus.cli scoring check-cpu-batch-compatibility `
        --cpu-batch-summary data/research/stage4h-cpu-batch-api-summary.yaml `
        --data-dir data/scoring `
        --allow-warnings

    Write-Host "Validating Stage 4J observation review workflow records"
    & $Python -m libreprimus.cli observation-review validate `
        --policy data/observations/review/stage4j-observation-review-policy.yaml `
        --decisions data/observations/review/stage4j-observation-review-decisions.yaml `
        --promotions data/observations/review/stage4j-observation-promotion-records.yaml `
        --quarantine data/observations/review/stage4j-observation-quarantine-records.yaml `
        --summary data/observations/review/stage4j-observation-review-summary.yaml
    & $Python -m libreprimus.cli observation-review check-paths --repo-root .

    Write-Host "Validating Stage 4K source-lock snapshot records"
    & $Python -m libreprimus.cli source-lock-snapshots validate `
        --snapshot-records data/locks/third-party/source-snapshots/stage4k-source-lock-snapshot-records.yaml `
        --fetch-records data/locks/third-party/source-snapshots/stage4k-source-fetch-records.yaml `
        --copyright-records data/locks/third-party/source-snapshots/stage4k-source-copyright-policy-records.yaml `
        --summary data/locks/third-party/source-snapshots/stage4k-source-lock-summary.yaml

    Write-Host "Validating Stage 4L observation promotion records"
    & $Python -m libreprimus.cli observation-promotion validate `
        --ledger data/observations/review/stage4l-reviewed-observation-promotion-ledger.yaml `
        --readiness data/observations/review/stage4l-observation-promotion-readiness-records.yaml `
        --blockers data/observations/review/stage4l-observation-promotion-blocker-records.yaml `
        --manifest-readiness data/observations/review/stage4l-manifest-readiness-records.yaml `
        --summary data/observations/review/stage4l-reviewed-observation-promotion-summary.yaml

    Write-Host "Validating Stage 4M image preflight records"
    & $Python -m libreprimus.cli image-preflight validate `
        --source-variant data/observations/visual/stage4m-image-source-variant-preflight-records.yaml `
        --compression data/observations/visual/stage4m-image-compression-preflight-records.yaml `
        --artifact-candidates data/observations/visual/stage4m-image-artifact-review-candidates.yaml `
        --summary data/observations/visual/stage4m-image-preflight-summary.yaml `
        --bigram-readiness data/observations/review/stage4m-bigram-frequency-pattern-readiness.yaml

    Write-Host "Validating Stage 4N stego/audio positive-control records"
    & $Python -m libreprimus.cli stego-positive-controls validate `
        --outguess-readiness data/observations/stego/stage4n-outguess-positive-control-readiness.yaml `
        --audio-readiness data/observations/stego/stage4n-audio-positive-control-readiness.yaml `
        --fixture-cache data/observations/stego/stage4n-fixture-cache-records.yaml `
        --expected-output data/observations/stego/stage4n-expected-output-records.yaml `
        --toolchain data/observations/stego/stage4n-toolchain-readiness.yaml `
        --summary data/observations/stego/stage4n-positive-control-summary.yaml

    Write-Host "Running Stage 4O CPU batch adapter expansion synthetic/temp output"
    $Stage4OOut = Join-Path $TempDir "stage4o-cpu-batch"
    $Stage4OSummary = Join-Path $TempDir "stage4o-cpu-batch-summary.yaml"
    & $Python -m libreprimus.cli cpu-batch solved-fixture-parity `
        --manifest experiments/manifests/cpu-batch/stage4o-solved-fixture-parity-batch.yaml `
        --out-dir $Stage4OOut `
        --allow-warnings
    & $Python -m libreprimus.cli cpu-batch adapter-expansion `
        --manifest experiments/manifests/cpu-batch/stage4o-adapter-expansion-smoke-batch.yaml `
        --registry data/transform-registry/cpu-reference-transforms-v0.json `
        --out-dir $Stage4OOut `
        --allow-warnings
    & $Python -m libreprimus.cli cpu-batch parity-readiness `
        --manifest experiments/manifests/cpu-batch/stage4o-cpu-cuda-parity-readiness.yaml `
        --out-dir $Stage4OOut `
        --summary-out $Stage4OSummary `
        --allow-warnings
    & $Python -m libreprimus.cli cpu-batch validate-stage4o `
        --results-dir $Stage4OOut `
        --summary $Stage4OSummary

    Write-Host "Running Stage 4P result-store unification synthetic/temp output"
    $Stage4POut = Join-Path $TempDir "stage4p-result-store-unification"
    $Stage4PSummary = Join-Path $TempDir "stage4p-result-store-score-summary-unification-summary.yaml"
    & $Python -m libreprimus.cli result-store build-source-inventory `
        --manifest experiments/manifests/result-store/stage4p-result-source-inventory.yaml `
        --out-dir $Stage4POut `
        --allow-warnings
    & $Python -m libreprimus.cli result-store unify-score-summaries `
        --manifest experiments/manifests/result-store/stage4p-score-summary-unification.yaml `
        --out-dir $Stage4POut `
        --allow-warnings
    & $Python -m libreprimus.cli result-store build-cross-stage-report `
        --manifest experiments/manifests/result-store/stage4p-cross-stage-report.yaml `
        --out-dir $Stage4POut `
        --summary-out $Stage4PSummary `
        --allow-warnings
    & $Python -m libreprimus.cli result-store validate-stage4p `
        --results-dir $Stage4POut `
        --summary $Stage4PSummary

    Write-Host "Running Stage 4Q benchmark planning synthetic/temp output"
    $Stage4QOut = Join-Path $TempDir "stage4q-benchmark-planning"
    $Stage4QPlan = Join-Path $TempDir "stage4q-cpu-benchmark-plan.yaml"
    $Stage4QReadiness = Join-Path $TempDir "stage4q-cuda-parity-readiness.yaml"
    $Stage4QSummary = Join-Path $TempDir "stage4q-cpu-benchmark-parity-planning-summary.yaml"
    & $Python -m libreprimus.cli benchmark-planning environment `
        --manifest experiments/manifests/benchmarks/stage4q-benchmark-environment.yaml `
        --out-dir $Stage4QOut `
        --allow-warnings
    & $Python -m libreprimus.cli benchmark-planning cpu-smoke `
        --manifest experiments/manifests/benchmarks/stage4q-cpu-benchmark-smoke.yaml `
        --out-dir $Stage4QOut `
        --allow-warnings
    & $Python -m libreprimus.cli benchmark-planning build-plan `
        --manifest experiments/manifests/benchmarks/stage4q-cuda-parity-readiness.yaml `
        --plan-out $Stage4QPlan `
        --readiness-out $Stage4QReadiness `
        --summary-out $Stage4QSummary `
        --out-dir $Stage4QOut `
        --allow-warnings
    & $Python -m libreprimus.cli benchmark-planning validate-stage4q `
        --results-dir $Stage4QOut `
        --plan $Stage4QPlan `
        --readiness $Stage4QReadiness `
        --summary $Stage4QSummary

    Write-Host "Running Stage 5A CUDA planning synthetic/temp output"
    $Stage5AOut = Join-Path $TempDir "stage5a-cuda-planning"
    $Stage5ATargetPlan = Join-Path $TempDir "stage5a-cuda-target-plan.yaml"
    $Stage5ANonTargets = Join-Path $TempDir "stage5a-cuda-non-targets.yaml"
    $Stage5AParityScaffold = Join-Path $TempDir "stage5a-cuda-parity-scaffold.yaml"
    $Stage5AGates = Join-Path $TempDir "stage5a-cuda-implementation-gates.yaml"
    $Stage5ASummary = Join-Path $TempDir "stage5a-cuda-planning-summary.yaml"
    & $Python -m libreprimus.cli cuda-planning build-target-plan `
        --manifest experiments/manifests/cuda/stage5a-cuda-target-plan.yaml `
        --out-dir $Stage5AOut `
        --target-plan-out $Stage5ATargetPlan `
        --non-targets-out $Stage5ANonTargets `
        --allow-warnings
    & $Python -m libreprimus.cli cuda-planning build-parity-scaffold `
        --manifest experiments/manifests/cuda/stage5a-cuda-parity-scaffold.yaml `
        --out-dir $Stage5AOut `
        --parity-scaffold-out $Stage5AParityScaffold `
        --allow-warnings
    & $Python -m libreprimus.cli cuda-planning build-implementation-gates `
        --manifest experiments/manifests/cuda/stage5a-cuda-implementation-gates.yaml `
        --out-dir $Stage5AOut `
        --implementation-gates-out $Stage5AGates `
        --summary-out $Stage5ASummary `
        --allow-warnings
    & $Python -m libreprimus.cli cuda-planning validate-stage5a `
        --target-plan $Stage5ATargetPlan `
        --parity-scaffold $Stage5AParityScaffold `
        --implementation-gates $Stage5AGates `
        --non-targets $Stage5ANonTargets `
        --summary $Stage5ASummary `
        --results-dir $Stage5AOut

    Write-Host "Running Stage 5B CUDA parity harness synthetic/temp output"
    $Stage5BOut = Join-Path $TempDir "stage5b-cuda-parity"
    $Stage5BHarness = Join-Path $TempDir "stage5b-cuda-parity-harness-plan.yaml"
    $Stage5BFixtures = Join-Path $TempDir "stage5b-cuda-parity-fixtures.yaml"
    $Stage5BBackend = Join-Path $TempDir "stage5b-cuda-backend-capability.yaml"
    $Stage5BMatrix = Join-Path $TempDir "stage5b-future-kernel-parity-matrix.yaml"
    $Stage5BSummary = Join-Path $TempDir "stage5b-cuda-parity-harness-summary.yaml"
    & $Python -m libreprimus.cli cuda-parity build-harness-plan `
        --manifest experiments/manifests/cuda/stage5b-cuda-parity-harness-plan.yaml `
        --target-plan data/cuda/stage5a-cuda-target-plan.yaml `
        --parity-scaffold data/cuda/stage5a-cuda-parity-scaffold.yaml `
        --implementation-gates data/cuda/stage5a-cuda-implementation-gates.yaml `
        --non-targets data/cuda/stage5a-cuda-non-targets.yaml `
        --stage5a-summary data/cuda/stage5a-cuda-planning-summary.yaml `
        --stage4q-readiness data/benchmarks/stage4q-cuda-parity-readiness.yaml `
        --stage4q-summary data/research/stage4q-cpu-benchmark-parity-planning-summary.yaml `
        --stage4o-summary data/research/stage4o-cpu-batch-adapter-expansion-summary.yaml `
        --stage4p-summary data/research/stage4p-result-store-score-summary-unification-summary.yaml `
        --out-dir $Stage5BOut `
        --harness-plan-out $Stage5BHarness `
        --parity-fixtures-out $Stage5BFixtures `
        --summary-out $Stage5BSummary `
        --allow-warnings
    & $Python -m libreprimus.cli cuda-parity build-backend-capability `
        --manifest experiments/manifests/cuda/stage5b-cuda-backend-capability.yaml `
        --out-dir $Stage5BOut `
        --backend-capability-out $Stage5BBackend `
        --allow-missing-cuda `
        --allow-warnings
    & $Python -m libreprimus.cli cuda-parity build-future-kernel-matrix `
        --manifest experiments/manifests/cuda/stage5b-future-kernel-parity-matrix.yaml `
        --target-plan data/cuda/stage5a-cuda-target-plan.yaml `
        --harness-plan $Stage5BHarness `
        --parity-fixtures $Stage5BFixtures `
        --backend-capability $Stage5BBackend `
        --out-dir $Stage5BOut `
        --future-kernel-matrix-out $Stage5BMatrix `
        --summary-out $Stage5BSummary `
        --allow-warnings
    & $Python -m libreprimus.cli cuda-parity validate-stage5b `
        --harness-plan $Stage5BHarness `
        --parity-fixtures $Stage5BFixtures `
        --backend-capability $Stage5BBackend `
        --future-kernel-matrix $Stage5BMatrix `
        --summary $Stage5BSummary `
        --results-dir $Stage5BOut

    Write-Host "Running Stage 5C CUDA build/device detection synthetic/temp output"
    $Stage5COut = Join-Path $TempDir "stage5c-cuda-build"
    $Stage5CProfiles = Join-Path $TempDir "stage5c-cuda-build-profiles.yaml"
    $Stage5CToolchain = Join-Path $TempDir "stage5c-cuda-toolchain-detection.yaml"
    $Stage5CDevices = Join-Path $TempDir "stage5c-cuda-device-detection.yaml"
    $Stage5CSmoke = Join-Path $TempDir "stage5c-cuda-smoke-build-records.yaml"
    $Stage5CSummary = Join-Path $TempDir "stage5c-cuda-build-device-summary.yaml"
    & $Python -m libreprimus.cli cuda-build profile-toolchain `
        --manifest experiments/manifests/cuda/stage5c-cuda-build-device-detection.yaml `
        --out-dir $Stage5COut `
        --profiles-out $Stage5CProfiles `
        --toolchain-out $Stage5CToolchain `
        --allow-missing-cuda `
        --allow-warnings
    & $Python -m libreprimus.cli cuda-build detect-device `
        --manifest experiments/manifests/cuda/stage5c-cuda-build-device-detection.yaml `
        --out-dir $Stage5COut `
        --devices-out $Stage5CDevices `
        --allow-no-gpu `
        --allow-warnings
    & $Python -m libreprimus.cli cuda-build smoke-build `
        --manifest experiments/manifests/cuda/stage5c-cuda-no-gpu-ci-profile.yaml `
        --out-dir $Stage5COut `
        --smoke-build-out $Stage5CSmoke `
        --allow-missing-cuda `
        --allow-no-gpu `
        --allow-warnings
    & $Python -m libreprimus.cli cuda-build build-summary `
        --profiles $Stage5CProfiles `
        --toolchain $Stage5CToolchain `
        --devices $Stage5CDevices `
        --smoke-build $Stage5CSmoke `
        --summary-out $Stage5CSummary `
        --out-dir $Stage5COut `
        --allow-warnings
    & $Python -m libreprimus.cli cuda-build validate-stage5c `
        --profiles $Stage5CProfiles `
        --toolchain $Stage5CToolchain `
        --devices $Stage5CDevices `
        --smoke-build $Stage5CSmoke `
        --summary $Stage5CSummary `
        --results-dir $Stage5COut

    Write-Host "Running Stage 5D native CPU backend synthetic/temp output"
    $Stage5DOut = Join-Path $TempDir "stage5d-native-cpu"
    $Stage5DFakeNative = Join-Path $TempDir "stage5d-fake-native.py"
    $Stage5DCapabilities = Join-Path $TempDir "stage5d-native-cpu-backend-capabilities.yaml"
    $Stage5DThreading = Join-Path $TempDir "stage5d-native-cpu-threading-records.yaml"
    $Stage5DParity = Join-Path $TempDir "stage5d-native-cpu-parity-records.yaml"
    $Stage5DDiagnostics = Join-Path $TempDir "stage5d-native-cpu-diagnostic-records.yaml"
    $Stage5DSummary = Join-Path $TempDir "stage5d-native-cpu-summary.yaml"
    @"
import json
import sys
from libreprimus.native_cpu.runner import python_reference_run
thread_count = 1
for index, arg in enumerate(sys.argv):
    if arg == "--threads" and index + 1 < len(sys.argv):
        thread_count = int(sys.argv[index + 1])
json.dump(python_reference_run(threads=thread_count), sys.stdout, sort_keys=True)
"@ | Set-Content -Encoding UTF8 $Stage5DFakeNative
    & $Python -m libreprimus.cli native-cpu run-smoke `
        --native-executable $Stage5DFakeNative `
        --manifest experiments/manifests/native-cpu/stage5d-native-cpu-smoke.yaml `
        --out-dir $Stage5DOut `
        --capabilities-out $Stage5DCapabilities `
        --diagnostics-out $Stage5DDiagnostics `
        --allow-warnings
    & $Python -m libreprimus.cli native-cpu check-threading-parity `
        --native-executable $Stage5DFakeNative `
        --manifest experiments/manifests/native-cpu/stage5d-native-cpu-threading-parity.yaml `
        --out-dir $Stage5DOut `
        --threading-out $Stage5DThreading `
        --thread-counts 1,2,4 `
        --allow-warnings
    & $Python -m libreprimus.cli native-cpu check-python-parity `
        --native-executable $Stage5DFakeNative `
        --manifest experiments/manifests/native-cpu/stage5d-native-python-parity.yaml `
        --out-dir $Stage5DOut `
        --parity-out $Stage5DParity `
        --allow-warnings
    & $Python -m libreprimus.cli native-cpu build-summary `
        --capabilities $Stage5DCapabilities `
        --threading $Stage5DThreading `
        --parity $Stage5DParity `
        --diagnostics $Stage5DDiagnostics `
        --summary-out $Stage5DSummary `
        --out-dir $Stage5DOut `
        --allow-warnings
    & $Python -m libreprimus.cli native-cpu validate-stage5d `
        --capabilities $Stage5DCapabilities `
        --threading $Stage5DThreading `
        --parity $Stage5DParity `
        --diagnostics $Stage5DDiagnostics `
        --summary $Stage5DSummary `
        --results-dir $Stage5DOut

    Write-Host "Running Stage 5E CUDA kernel contract synthetic/temp output"
    $Stage5EOut = Join-Path $TempDir "stage5e-cuda-kernel-contract"
    $Stage5EContract = Join-Path $TempDir "stage5e-first-kernel-contract.yaml"
    $Stage5EAdapter = Join-Path $TempDir "stage5e-cuda-adapter-selection.yaml"
    $Stage5ENative = Join-Path $TempDir "stage5e-native-parity-adapter-map.yaml"
    $Stage5EReadiness = Join-Path $TempDir "stage5e-implementation-readiness.yaml"
    $Stage5ESummary = Join-Path $TempDir "stage5e-first-kernel-contract-summary.yaml"
    & $Python -m libreprimus.cli cuda-kernel-contract select-first-kernel `
        --manifest experiments/manifests/cuda/stage5e-first-kernel-contract.yaml `
        --out-dir $Stage5EOut `
        --contract-out $Stage5EContract `
        --adapter-selection-out $Stage5EAdapter `
        --allow-warnings
    & $Python -m libreprimus.cli cuda-kernel-contract build-native-parity-map `
        --manifest experiments/manifests/cuda/stage5e-adapter-selection.yaml `
        --contract $Stage5EContract `
        --out-dir $Stage5EOut `
        --native-parity-out $Stage5ENative `
        --allow-warnings
    & $Python -m libreprimus.cli cuda-kernel-contract build-readiness `
        --manifest experiments/manifests/cuda/stage5e-implementation-readiness.yaml `
        --contract $Stage5EContract `
        --native-parity $Stage5ENative `
        --out-dir $Stage5EOut `
        --readiness-out $Stage5EReadiness `
        --allow-warnings
    & $Python -m libreprimus.cli cuda-kernel-contract build-summary `
        --contract $Stage5EContract `
        --adapter-selection $Stage5EAdapter `
        --native-parity $Stage5ENative `
        --readiness $Stage5EReadiness `
        --out-dir $Stage5EOut `
        --summary-out $Stage5ESummary `
        --allow-warnings
    & $Python -m libreprimus.cli cuda-kernel-contract validate-stage5e `
        --contract $Stage5EContract `
        --adapter-selection $Stage5EAdapter `
        --native-parity $Stage5ENative `
        --readiness $Stage5EReadiness `
        --summary $Stage5ESummary `
        --results-dir $Stage5EOut

    Write-Host "Running Stage 5F synthetic CUDA kernel no-GPU-safe/temp output"
    $Stage5FOut = Join-Path $TempDir "stage5f-cuda-kernel"
    $Stage5FImplementation = Join-Path $TempDir "stage5f-cuda-synthetic-kernel-implementation.yaml"
    $Stage5FBuild = Join-Path $TempDir "stage5f-cuda-kernel-build-records.yaml"
    $Stage5FParity = Join-Path $TempDir "stage5f-cuda-synthetic-parity-records.yaml"
    $Stage5FSummary = Join-Path $TempDir "stage5f-cuda-synthetic-kernel-summary.yaml"
    $Stage5FBuildDir = Join-Path $TempDir "stage5f-cuda-build"
    & $Python -m libreprimus.cli cuda-kernel build-implementation-records `
        --manifest experiments/manifests/cuda/stage5f-shift-score-synthetic-parity.yaml `
        --out-dir $Stage5FOut `
        --implementation-out $Stage5FImplementation `
        --allow-warnings
    & $Python -m libreprimus.cli cuda-kernel attempt-build `
        --manifest experiments/manifests/cuda/stage5f-cuda-no-gpu-ci-skip.yaml `
        --out-dir $Stage5FOut `
        --build-records-out $Stage5FBuild `
        --build-dir $Stage5FBuildDir `
        --skip-build `
        --allow-warnings
    & $Python -m libreprimus.cli cuda-kernel run-synthetic-parity `
        --manifest experiments/manifests/cuda/stage5f-shift-score-synthetic-parity.yaml `
        --build-records $Stage5FBuild `
        --out-dir $Stage5FOut `
        --parity-records-out $Stage5FParity `
        --build-dir $Stage5FBuildDir `
        --allow-warnings
    & $Python -m libreprimus.cli cuda-kernel build-summary `
        --implementation $Stage5FImplementation `
        --build-records $Stage5FBuild `
        --parity-records $Stage5FParity `
        --summary-out $Stage5FSummary `
        --out-dir $Stage5FOut `
        --allow-warnings
    & $Python -m libreprimus.cli cuda-kernel validate-stage5f `
        --implementation $Stage5FImplementation `
        --build-records $Stage5FBuild `
        --parity-records $Stage5FParity `
        --summary $Stage5FSummary `
        --results-dir $Stage5FOut

    Write-Host "Running Stage 5G CUDA parity reporting no-GPU-safe/temp output"
    $Stage5GOut = Join-Path $TempDir "stage5g-cuda-parity-reporting"
    $Stage5GParityReport = Join-Path $TempDir "stage5g-shift-score-parity-report.yaml"
    $Stage5GDeviceAudit = Join-Path $TempDir "stage5g-cuda-device-code-subset-audit.yaml"
    $Stage5GPreflight = Join-Path $TempDir "stage5g-solved-fixture-safe-adapter-preflight.yaml"
    $Stage5GSummary = Join-Path $TempDir "stage5g-cuda-parity-reporting-summary.yaml"
    & $Python -m libreprimus.cli cuda-parity-reporting build-parity-report `
        --manifest experiments/manifests/cuda/stage5g-shift-score-parity-reporting.yaml `
        --out-dir $Stage5GOut `
        --parity-report-out $Stage5GParityReport `
        --allow-warnings
    & $Python -m libreprimus.cli cuda-parity-reporting audit-device-code-subset `
        --manifest experiments/manifests/cuda/stage5g-device-code-subset-audit.yaml `
        --out-dir $Stage5GOut `
        --device-code-audit-out $Stage5GDeviceAudit `
        --allow-warnings
    & $Python -m libreprimus.cli cuda-parity-reporting build-solved-fixture-preflight `
        --manifest experiments/manifests/cuda/stage5g-solved-fixture-safe-adapter-preflight.yaml `
        --out-dir $Stage5GOut `
        --preflight-out $Stage5GPreflight `
        --allow-warnings
    & $Python -m libreprimus.cli cuda-parity-reporting build-summary `
        --parity-report $Stage5GParityReport `
        --device-code-audit $Stage5GDeviceAudit `
        --preflight $Stage5GPreflight `
        --summary-out $Stage5GSummary `
        --out-dir $Stage5GOut `
        --allow-warnings
    & $Python -m libreprimus.cli cuda-parity-reporting validate-stage5g `
        --parity-report $Stage5GParityReport `
        --device-code-audit $Stage5GDeviceAudit `
        --preflight $Stage5GPreflight `
        --summary $Stage5GSummary `
        --results-dir $Stage5GOut

    Write-Host "Running Stage 5H Gematria shift contract no-GPU-safe/temp output"
    $Stage5HOut = Join-Path $TempDir "stage5h-gematria-shift-contract"
    $Stage5HContract = Join-Path $TempDir "stage5h-gematria-shift-score-contract.yaml"
    $Stage5HFixtures = Join-Path $TempDir "stage5h-gematria-native-parity-fixtures.yaml"
    $Stage5HMapping = Join-Path $TempDir "stage5h-gematria-solved-fixture-safe-mapping.yaml"
    $Stage5HScorePlan = Join-Path $TempDir "stage5h-gematria-score-summary-parity-plan.yaml"
    $Stage5HSummary = Join-Path $TempDir "stage5h-gematria-shift-contract-summary.yaml"
    & $Python -m libreprimus.cli gematria-shift-contract build-contract `
        --manifest experiments/manifests/cuda/stage5h-gematria-shift-score-contract.yaml `
        --out-dir $Stage5HOut `
        --contract-out $Stage5HContract `
        --allow-warnings
    & $Python -m libreprimus.cli gematria-shift-contract build-native-fixtures `
        --manifest experiments/manifests/cuda/stage5h-gematria-native-parity-fixtures.yaml `
        --out-dir $Stage5HOut `
        --fixtures-out $Stage5HFixtures `
        --allow-warnings
    & $Python -m libreprimus.cli gematria-shift-contract build-solved-fixture-mapping `
        --manifest experiments/manifests/cuda/stage5h-solved-fixture-safe-mapping.yaml `
        --source-manifest experiments/manifests/cpu-batch/stage4o-solved-fixture-parity-batch.yaml `
        --out-dir $Stage5HOut `
        --mapping-out $Stage5HMapping `
        --allow-warnings
    & $Python -m libreprimus.cli gematria-shift-contract build-score-summary-plan `
        --manifest experiments/manifests/cuda/stage5h-gematria-shift-score-contract.yaml `
        --out-dir $Stage5HOut `
        --score-summary-plan-out $Stage5HScorePlan `
        --allow-warnings
    & $Python -m libreprimus.cli gematria-shift-contract build-summary `
        --contract $Stage5HContract `
        --fixtures $Stage5HFixtures `
        --mapping $Stage5HMapping `
        --score-summary-plan $Stage5HScorePlan `
        --summary-out $Stage5HSummary `
        --out-dir $Stage5HOut `
        --allow-warnings
    & $Python -m libreprimus.cli gematria-shift-contract validate-stage5h `
        --contract $Stage5HContract `
        --fixtures $Stage5HFixtures `
        --mapping $Stage5HMapping `
        --score-summary-plan $Stage5HScorePlan `
        --summary $Stage5HSummary `
        --results-dir $Stage5HOut

    Write-Host "Running Stage 5I Gematria CUDA preparation no-GPU-safe/temp output"
    $Stage5IOut = Join-Path $TempDir "stage5i-gematria-cuda-prep"
    $Stage5IPreparation = Join-Path $TempDir "stage5i-gematria-cuda-kernel-preparation.yaml"
    $Stage5IAbi = Join-Path $TempDir "stage5i-gematria-cuda-abi-plan.yaml"
    $Stage5IVectors = Join-Path $TempDir "stage5i-gematria-cuda-validation-vectors.yaml"
    $Stage5IChecklist = Join-Path $TempDir "stage5i-gematria-cuda-implementation-checklist.yaml"
    $Stage5ISummary = Join-Path $TempDir "stage5i-gematria-cuda-preparation-summary.yaml"
    & $Python -m libreprimus.cli gematria-cuda-prep build-kernel-preparation `
        --manifest experiments/manifests/cuda/stage5i-gematria-cuda-kernel-preparation.yaml `
        --out-dir $Stage5IOut `
        --preparation-out $Stage5IPreparation `
        --allow-warnings
    & $Python -m libreprimus.cli gematria-cuda-prep build-abi-plan `
        --manifest experiments/manifests/cuda/stage5i-gematria-cuda-abi-plan.yaml `
        --out-dir $Stage5IOut `
        --abi-plan-out $Stage5IAbi `
        --allow-warnings
    & $Python -m libreprimus.cli gematria-cuda-prep build-validation-vectors `
        --manifest experiments/manifests/cuda/stage5i-gematria-cuda-validation-vectors.yaml `
        --out-dir $Stage5IOut `
        --validation-vectors-out $Stage5IVectors `
        --allow-warnings
    & $Python -m libreprimus.cli gematria-cuda-prep build-implementation-checklist `
        --out-dir $Stage5IOut `
        --implementation-checklist-out $Stage5IChecklist `
        --allow-warnings
    & $Python -m libreprimus.cli gematria-cuda-prep build-summary `
        --preparation $Stage5IPreparation `
        --abi-plan $Stage5IAbi `
        --validation-vectors $Stage5IVectors `
        --implementation-checklist $Stage5IChecklist `
        --summary-out $Stage5ISummary `
        --out-dir $Stage5IOut `
        --allow-warnings
    & $Python -m libreprimus.cli gematria-cuda-prep validate-stage5i `
        --preparation $Stage5IPreparation `
        --abi-plan $Stage5IAbi `
        --validation-vectors $Stage5IVectors `
        --implementation-checklist $Stage5IChecklist `
        --summary $Stage5ISummary `
        --results-dir $Stage5IOut

    Write-Host "Running Stage 5J Gematria CUDA kernel no-GPU-safe/temp output"
    $Stage5JOut = Join-Path $TempDir "stage5j-gematria-cuda-kernel"
    $Stage5JImplementation = Join-Path $TempDir "stage5j-gematria-cuda-kernel-implementation.yaml"
    $Stage5JBuild = Join-Path $TempDir "stage5j-gematria-cuda-kernel-build-records.yaml"
    $Stage5JParity = Join-Path $TempDir "stage5j-gematria-cuda-synthetic-parity-records.yaml"
    $Stage5JSummary = Join-Path $TempDir "stage5j-gematria-cuda-kernel-summary.yaml"
    $Stage5JBuildDir = Join-Path $TempDir "stage5j-cuda-build"
    & $Python -m libreprimus.cli gematria-cuda-kernel build-implementation-records `
        --manifest experiments/manifests/cuda/stage5j-gematria-cuda-kernel.yaml `
        --out-dir $Stage5JOut `
        --implementation-out $Stage5JImplementation `
        --allow-warnings
    & $Python -m libreprimus.cli gematria-cuda-kernel attempt-build `
        --manifest experiments/manifests/cuda/stage5j-gematria-cuda-no-gpu-ci-skip.yaml `
        --out-dir $Stage5JOut `
        --build-records-out $Stage5JBuild `
        --build-dir $Stage5JBuildDir `
        --skip-build `
        --allow-warnings
    & $Python -m libreprimus.cli gematria-cuda-kernel run-synthetic-parity `
        --manifest experiments/manifests/cuda/stage5j-gematria-cuda-kernel.yaml `
        --build-records $Stage5JBuild `
        --out-dir $Stage5JOut `
        --parity-records-out $Stage5JParity `
        --build-dir $Stage5JBuildDir `
        --allow-warnings
    & $Python -m libreprimus.cli gematria-cuda-kernel build-summary `
        --implementation $Stage5JImplementation `
        --build-records $Stage5JBuild `
        --parity-records $Stage5JParity `
        --summary-out $Stage5JSummary `
        --out-dir $Stage5JOut `
        --allow-warnings
    & $Python -m libreprimus.cli gematria-cuda-kernel validate-stage5j `
        --implementation $Stage5JImplementation `
        --build-records $Stage5JBuild `
        --parity-records $Stage5JParity `
        --summary $Stage5JSummary `
        --results-dir $Stage5JOut

    Write-Host "Running Stage 5K Gematria CUDA parity reporting no-GPU-safe/temp output"
    $Stage5KOut = Join-Path $TempDir "stage5k-gematria-cuda-parity-reporting"
    $Stage5KParity = Join-Path $TempDir "stage5k-gematria-cuda-parity-report.yaml"
    $Stage5KAudit = Join-Path $TempDir "stage5k-gematria-cuda-device-code-audit.yaml"
    $Stage5KPreflight = Join-Path $TempDir "stage5k-gematria-solved-fixture-safe-preflight.yaml"
    $Stage5KScore = Join-Path $TempDir "stage5k-gematria-cuda-score-summary-preflight.yaml"
    $Stage5KSummary = Join-Path $TempDir "stage5k-gematria-cuda-parity-reporting-summary.yaml"
    & $Python -m libreprimus.cli gematria-cuda-parity-reporting build-parity-report `
        --manifest experiments/manifests/cuda/stage5k-gematria-cuda-parity-reporting.yaml `
        --out-dir $Stage5KOut `
        --parity-report-out $Stage5KParity `
        --allow-warnings
    & $Python -m libreprimus.cli gematria-cuda-parity-reporting audit-device-code `
        --manifest experiments/manifests/cuda/stage5k-gematria-device-code-audit.yaml `
        --out-dir $Stage5KOut `
        --device-code-audit-out $Stage5KAudit `
        --allow-warnings
    & $Python -m libreprimus.cli gematria-cuda-parity-reporting build-solved-fixture-preflight `
        --manifest experiments/manifests/cuda/stage5k-solved-fixture-safe-preflight.yaml `
        --out-dir $Stage5KOut `
        --preflight-out $Stage5KPreflight `
        --allow-warnings
    & $Python -m libreprimus.cli gematria-cuda-parity-reporting build-score-summary-preflight `
        --manifest experiments/manifests/cuda/stage5k-solved-fixture-safe-preflight.yaml `
        --out-dir $Stage5KOut `
        --score-summary-preflight-out $Stage5KScore `
        --allow-warnings
    & $Python -m libreprimus.cli gematria-cuda-parity-reporting build-summary `
        --parity-report $Stage5KParity `
        --device-code-audit $Stage5KAudit `
        --preflight $Stage5KPreflight `
        --score-summary-preflight $Stage5KScore `
        --summary-out $Stage5KSummary `
        --out-dir $Stage5KOut `
        --allow-warnings
    & $Python -m libreprimus.cli gematria-cuda-parity-reporting validate-stage5k `
        --parity-report $Stage5KParity `
        --device-code-audit $Stage5KAudit `
        --preflight $Stage5KPreflight `
        --score-summary-preflight $Stage5KScore `
        --summary $Stage5KSummary `
        --results-dir $Stage5KOut

    Write-Host "Running Stage 5L solved-fixture Gematria token mapping no-GPU-safe/temp output"
    $Stage5LOut = Join-Path $TempDir "stage5l-gematria-solved-fixture-mapping"
    $Stage5LTokenMapping = Join-Path $TempDir "stage5l-gematria-solved-fixture-token-mapping.yaml"
    $Stage5LNativeParity = Join-Path $TempDir "stage5l-gematria-solved-fixture-native-parity.yaml"
    $Stage5LOutputHash = Join-Path $TempDir "stage5l-gematria-solved-fixture-output-hash-contract.yaml"
    $Stage5LScoreShape = Join-Path $TempDir "stage5l-gematria-solved-fixture-score-summary-shape.yaml"
    $Stage5LSummary = Join-Path $TempDir "stage5l-solved-fixture-token-mapping-summary.yaml"
    & $Python -m libreprimus.cli gematria-solved-fixture-mapping build-token-mapping `
        --manifest experiments/manifests/cuda/stage5l-solved-fixture-token-mapping.yaml `
        --preflight data/cuda/stage5k-gematria-solved-fixture-safe-preflight.yaml `
        --out-dir $Stage5LOut `
        --token-mapping-out $Stage5LTokenMapping `
        --allow-warnings
    & $Python -m libreprimus.cli gematria-solved-fixture-mapping build-native-parity `
        --token-mapping $Stage5LTokenMapping `
        --out-dir $Stage5LOut `
        --native-parity-out $Stage5LNativeParity `
        --allow-warnings
    & $Python -m libreprimus.cli gematria-solved-fixture-mapping build-output-hash-contract `
        --native-parity $Stage5LNativeParity `
        --out-dir $Stage5LOut `
        --output-hash-contract-out $Stage5LOutputHash `
        --allow-warnings
    & $Python -m libreprimus.cli gematria-solved-fixture-mapping build-score-summary-shape `
        --out-dir $Stage5LOut `
        --score-summary-shape-out $Stage5LScoreShape `
        --allow-warnings
    & $Python -m libreprimus.cli gematria-solved-fixture-mapping build-summary `
        --token-mapping $Stage5LTokenMapping `
        --native-parity $Stage5LNativeParity `
        --output-hash-contract $Stage5LOutputHash `
        --score-summary-shape $Stage5LScoreShape `
        --summary-out $Stage5LSummary `
        --out-dir $Stage5LOut `
        --allow-warnings
    & $Python -m libreprimus.cli gematria-solved-fixture-mapping validate-stage5l `
        --token-mapping $Stage5LTokenMapping `
        --native-parity $Stage5LNativeParity `
        --output-hash-contract $Stage5LOutputHash `
        --score-summary-shape $Stage5LScoreShape `
        --summary $Stage5LSummary `
        --results-dir $Stage5LOut

    Write-Host "Running Stage 5M solved-fixture Gematria CUDA parity no-GPU-safe/temp output"
    $Stage5MOut = Join-Path $TempDir "stage5m-gematria-solved-fixture-cuda"
    $Stage5MRunRecords = Join-Path $TempDir "stage5m-gematria-solved-fixture-cuda-run.yaml"
    $Stage5MParityRecords = Join-Path $TempDir "stage5m-gematria-solved-fixture-cuda-parity.yaml"
    $Stage5MBoundaries = Join-Path $TempDir "stage5m-gematria-solved-fixture-cuda-boundaries.yaml"
    $Stage5MSummary = Join-Path $TempDir "stage5m-solved-fixture-cuda-parity-summary.yaml"
    & $Python -m libreprimus.cli gematria-solved-fixture-cuda build-run-records `
        --token-mapping data/cuda/stage5l-gematria-solved-fixture-token-mapping.yaml `
        --native-parity data/cuda/stage5l-gematria-solved-fixture-native-parity.yaml `
        --run-records-out $Stage5MRunRecords `
        --out-dir $Stage5MOut `
        --allow-warnings
    & $Python -m libreprimus.cli gematria-solved-fixture-cuda run-cuda-parity `
        --run-records $Stage5MRunRecords `
        --run-records-out $Stage5MRunRecords `
        --out-dir $Stage5MOut `
        --build-dir (Join-Path $TempDir "stage5m-cuda-build") `
        --skip-run `
        --allow-warnings
    & $Python -m libreprimus.cli gematria-solved-fixture-cuda build-parity-records `
        --run-records $Stage5MRunRecords `
        --parity-records-out $Stage5MParityRecords `
        --out-dir $Stage5MOut `
        --allow-warnings
    & $Python -m libreprimus.cli gematria-solved-fixture-cuda build-boundary-records `
        --run-records $Stage5MRunRecords `
        --boundaries-out $Stage5MBoundaries `
        --out-dir $Stage5MOut `
        --allow-warnings
    & $Python -m libreprimus.cli gematria-solved-fixture-cuda build-summary `
        --run-records $Stage5MRunRecords `
        --parity-records $Stage5MParityRecords `
        --boundaries $Stage5MBoundaries `
        --summary-out $Stage5MSummary `
        --out-dir $Stage5MOut `
        --allow-warnings
    & $Python -m libreprimus.cli gematria-solved-fixture-cuda validate-stage5m `
        --run-records $Stage5MRunRecords `
        --parity-records $Stage5MParityRecords `
        --boundaries $Stage5MBoundaries `
        --summary $Stage5MSummary `
        --results-dir $Stage5MOut

    Write-Host "Running Stage 5N solved-fixture Gematria CUDA reporting no-GPU-safe/temp output"
    $Stage5NOut = Join-Path $TempDir "stage5n-gematria-solved-fixture-cuda-reporting"
    $Stage5NParityReport = Join-Path $TempDir "stage5n-gematria-solved-fixture-cuda-report.yaml"
    $Stage5NGate = Join-Path $TempDir "stage5n-gematria-controlled-expansion-gate.yaml"
    $Stage5NBoundary = Join-Path $TempDir "stage5n-gematria-cuda-boundary-review.yaml"
    $Stage5NPreflight = Join-Path $TempDir "stage5n-gematria-cuda-result-store-preflight.yaml"
    $Stage5NGuardrail = Join-Path $TempDir "stage5n-gematria-no-unsolved-guardrail.yaml"
    $Stage5NSummary = Join-Path $TempDir "stage5n-solved-fixture-cuda-reporting-summary.yaml"
    & $Python -m libreprimus.cli gematria-solved-fixture-cuda-reporting build-parity-report `
        --stage5m-run-records data/cuda/stage5m-gematria-solved-fixture-cuda-run.yaml `
        --stage5m-parity-records data/cuda/stage5m-gematria-solved-fixture-cuda-parity.yaml `
        --stage5m-summary data/cuda/stage5m-solved-fixture-cuda-parity-summary.yaml `
        --parity-report-out $Stage5NParityReport `
        --out-dir $Stage5NOut `
        --allow-warnings
    & $Python -m libreprimus.cli gematria-solved-fixture-cuda-reporting build-controlled-expansion-gate `
        --controlled-expansion-gate-out $Stage5NGate `
        --out-dir $Stage5NOut `
        --allow-warnings
    & $Python -m libreprimus.cli gematria-solved-fixture-cuda-reporting build-boundary-review `
        --stage5m-summary data/cuda/stage5m-solved-fixture-cuda-parity-summary.yaml `
        --boundary-review-out $Stage5NBoundary `
        --out-dir $Stage5NOut `
        --allow-warnings
    & $Python -m libreprimus.cli gematria-solved-fixture-cuda-reporting build-result-store-preflight `
        --stage4p-summary data/research/stage4p-result-store-score-summary-unification-summary.yaml `
        --result-store-preflight-out $Stage5NPreflight `
        --out-dir $Stage5NOut `
        --allow-warnings
    & $Python -m libreprimus.cli gematria-solved-fixture-cuda-reporting build-no-unsolved-guardrail `
        --no-unsolved-guardrail-out $Stage5NGuardrail `
        --out-dir $Stage5NOut `
        --allow-warnings
    & $Python -m libreprimus.cli gematria-solved-fixture-cuda-reporting build-summary `
        --parity-report $Stage5NParityReport `
        --controlled-expansion-gate $Stage5NGate `
        --boundary-review $Stage5NBoundary `
        --result-store-preflight $Stage5NPreflight `
        --no-unsolved-guardrail $Stage5NGuardrail `
        --stage5m-summary data/cuda/stage5m-solved-fixture-cuda-parity-summary.yaml `
        --summary-out $Stage5NSummary `
        --out-dir $Stage5NOut `
        --allow-warnings
    & $Python -m libreprimus.cli gematria-solved-fixture-cuda-reporting validate-stage5n `
        --parity-report $Stage5NParityReport `
        --controlled-expansion-gate $Stage5NGate `
        --boundary-review $Stage5NBoundary `
        --result-store-preflight $Stage5NPreflight `
        --no-unsolved-guardrail $Stage5NGuardrail `
        --summary $Stage5NSummary `
        --results-dir $Stage5NOut

    Write-Host "Running Stage 5O solved-fixture Gematria CUDA repeat no-GPU-safe/temp output"
    $Stage5OOut = Join-Path $TempDir "stage5o-gematria-solved-fixture-cuda-repeat"
    $Stage5ORun = Join-Path $TempDir "stage5o-gematria-solved-fixture-cuda-repeat-run.yaml"
    $Stage5OParity = Join-Path $TempDir "stage5o-gematria-solved-fixture-cuda-repeat-parity.yaml"
    $Stage5OResultStore = Join-Path $TempDir "stage5o-gematria-cuda-result-store-preflight.yaml"
    $Stage5OScore = Join-Path $TempDir "stage5o-gematria-cuda-score-summary-preflight.yaml"
    $Stage5ODecision = Join-Path $TempDir "stage5o-gematria-cuda-expansion-decision.yaml"
    $Stage5OSummary = Join-Path $TempDir "stage5o-repeat-verification-result-store-summary.yaml"
    & $Python -m libreprimus.cli gematria-solved-fixture-cuda-repeat build-repeat-run-records `
        --stage5m-run-records data/cuda/stage5m-gematria-solved-fixture-cuda-run.yaml `
        --stage5m-parity-records data/cuda/stage5m-gematria-solved-fixture-cuda-parity.yaml `
        --stage5l-native-parity data/cuda/stage5l-gematria-solved-fixture-native-parity.yaml `
        --repeat-run-out $Stage5ORun `
        --out-dir $Stage5OOut `
        --allow-warnings
    & $Python -m libreprimus.cli gematria-solved-fixture-cuda-repeat run-repeat-verification `
        --repeat-run $Stage5ORun `
        --repeat-run-out $Stage5ORun `
        --out-dir $Stage5OOut `
        --build-dir (Join-Path $TempDir "stage5o-cuda-build") `
        --skip-run `
        --allow-warnings
    & $Python -m libreprimus.cli gematria-solved-fixture-cuda-repeat build-repeat-parity-records `
        --repeat-run $Stage5ORun `
        --repeat-parity-out $Stage5OParity `
        --out-dir $Stage5OOut `
        --allow-warnings
    & $Python -m libreprimus.cli gematria-solved-fixture-cuda-repeat build-result-store-preflight `
        --repeat-parity $Stage5OParity `
        --stage4p-summary data/research/stage4p-result-store-score-summary-unification-summary.yaml `
        --result-store-preflight-out $Stage5OResultStore `
        --out-dir $Stage5OOut `
        --allow-warnings
    & $Python -m libreprimus.cli gematria-solved-fixture-cuda-repeat build-score-summary-preflight `
        --repeat-parity $Stage5OParity `
        --score-summary-preflight-out $Stage5OScore `
        --out-dir $Stage5OOut `
        --allow-warnings
    & $Python -m libreprimus.cli gematria-solved-fixture-cuda-repeat build-expansion-decision `
        --repeat-parity $Stage5OParity `
        --result-store-preflight $Stage5OResultStore `
        --score-summary-preflight $Stage5OScore `
        --expansion-decision-out $Stage5ODecision `
        --out-dir $Stage5OOut `
        --allow-warnings
    & $Python -m libreprimus.cli gematria-solved-fixture-cuda-repeat build-summary `
        --repeat-run $Stage5ORun `
        --repeat-parity $Stage5OParity `
        --result-store-preflight $Stage5OResultStore `
        --score-summary-preflight $Stage5OScore `
        --expansion-decision $Stage5ODecision `
        --stage5m-summary data/cuda/stage5m-solved-fixture-cuda-parity-summary.yaml `
        --stage5n-summary data/cuda/stage5n-solved-fixture-cuda-reporting-summary.yaml `
        --summary-out $Stage5OSummary `
        --out-dir $Stage5OOut `
        --allow-warnings
    & $Python -m libreprimus.cli gematria-solved-fixture-cuda-repeat validate-stage5o `
        --repeat-run $Stage5ORun `
        --repeat-parity $Stage5OParity `
        --result-store-preflight $Stage5OResultStore `
        --score-summary-preflight $Stage5OScore `
        --expansion-decision $Stage5ODecision `
        --summary $Stage5OSummary `
        --results-dir $Stage5OOut

    $Stage5POut = Join-Path $TempDir "stage5p-gematria-cuda-result-store"
    $Stage5PResultStore = Join-Path $TempDir "stage5p-gematria-cuda-result-store-integration.yaml"
    $Stage5PScore = Join-Path $TempDir "stage5p-gematria-cuda-score-summary-integration.yaml"
    $Stage5PMethod = Join-Path $TempDir "stage5p-gematria-cuda-method-status-impact.yaml"
    $Stage5PPolicy = Join-Path $TempDir "stage5p-gematria-cuda-generated-body-policy.yaml"
    $Stage5PCandidates = Join-Path $TempDir "stage5p-gematria-controlled-expansion-candidates.yaml"
    $Stage5PSummary = Join-Path $TempDir "stage5p-cuda-result-store-integration-summary.yaml"
    & $Python -m libreprimus.cli gematria-cuda-result-store build-result-store-integration `
        --repeat-parity data/cuda/stage5o-gematria-solved-fixture-cuda-repeat-parity.yaml `
        --result-store-integration-out $Stage5PResultStore `
        --out-dir $Stage5POut `
        --allow-warnings
    & $Python -m libreprimus.cli gematria-cuda-result-store build-score-summary-integration `
        --result-store-integration $Stage5PResultStore `
        --score-summary-integration-out $Stage5PScore `
        --out-dir $Stage5POut `
        --allow-warnings
    & $Python -m libreprimus.cli gematria-cuda-result-store build-method-status-impact `
        --result-store-integration $Stage5PResultStore `
        --method-status-impact-out $Stage5PMethod `
        --out-dir $Stage5POut `
        --allow-warnings
    & $Python -m libreprimus.cli gematria-cuda-result-store build-generated-body-policy `
        --generated-body-policy-out $Stage5PPolicy `
        --out-dir $Stage5POut `
        --allow-warnings
    & $Python -m libreprimus.cli gematria-cuda-result-store build-controlled-expansion-candidates `
        --controlled-expansion-candidates-out $Stage5PCandidates `
        --out-dir $Stage5POut `
        --allow-warnings
    & $Python -m libreprimus.cli gematria-cuda-result-store build-summary `
        --result-store-integration $Stage5PResultStore `
        --score-summary-integration $Stage5PScore `
        --method-status-impact $Stage5PMethod `
        --generated-body-policy $Stage5PPolicy `
        --controlled-expansion-candidates $Stage5PCandidates `
        --summary-out $Stage5PSummary `
        --out-dir $Stage5POut `
        --allow-warnings
    & $Python -m libreprimus.cli gematria-cuda-result-store validate-stage5p `
        --result-store-integration $Stage5PResultStore `
        --score-summary-integration $Stage5PScore `
        --method-status-impact $Stage5PMethod `
        --generated-body-policy $Stage5PPolicy `
        --controlled-expansion-candidates $Stage5PCandidates `
        --summary $Stage5PSummary `
        --results-dir $Stage5POut

    Write-Host "Running Stage 5Q Gematria expansion candidate mapping no-GPU-safe/temp output"
    $Stage5QOut = Join-Path $TempDir "stage5q-gematria-expansion-candidate-mapping"
    $Stage5QInventory = Join-Path $TempDir "stage5q-gematria-expansion-candidate-inventory.yaml"
    $Stage5QMapping = Join-Path $TempDir "stage5q-gematria-expansion-token-mapping.yaml"
    $Stage5QNative = Join-Path $TempDir "stage5q-gematria-expansion-native-parity.yaml"
    $Stage5QPreflight = Join-Path $TempDir "stage5q-gematria-expansion-result-store-preflight.yaml"
    $Stage5QGate = Join-Path $TempDir "stage5q-gematria-expansion-gate.yaml"
    $Stage5QSummary = Join-Path $TempDir "stage5q-expansion-candidate-mapping-summary.yaml"
    & $Python -m libreprimus.cli gematria-expansion-candidate-mapping build-candidate-inventory `
        --candidate-inventory-out $Stage5QInventory `
        --out-dir $Stage5QOut `
        --allow-warnings
    & $Python -m libreprimus.cli gematria-expansion-candidate-mapping build-token-mapping `
        --candidate-inventory $Stage5QInventory `
        --token-mapping-out $Stage5QMapping `
        --out-dir $Stage5QOut `
        --allow-warnings
    & $Python -m libreprimus.cli gematria-expansion-candidate-mapping build-native-parity `
        --token-mapping $Stage5QMapping `
        --native-parity-out $Stage5QNative `
        --out-dir $Stage5QOut `
        --allow-warnings
    & $Python -m libreprimus.cli gematria-expansion-candidate-mapping build-result-store-preflight `
        --token-mapping $Stage5QMapping `
        --native-parity $Stage5QNative `
        --result-store-preflight-out $Stage5QPreflight `
        --out-dir $Stage5QOut `
        --allow-warnings
    & $Python -m libreprimus.cli gematria-expansion-candidate-mapping build-expansion-gate `
        --candidate-inventory $Stage5QInventory `
        --token-mapping $Stage5QMapping `
        --native-parity $Stage5QNative `
        --result-store-preflight $Stage5QPreflight `
        --expansion-gate-out $Stage5QGate `
        --out-dir $Stage5QOut `
        --allow-warnings
    & $Python -m libreprimus.cli gematria-expansion-candidate-mapping build-summary `
        --candidate-inventory $Stage5QInventory `
        --token-mapping $Stage5QMapping `
        --native-parity $Stage5QNative `
        --result-store-preflight $Stage5QPreflight `
        --expansion-gate $Stage5QGate `
        --summary-out $Stage5QSummary `
        --out-dir $Stage5QOut `
        --allow-warnings
    & $Python -m libreprimus.cli gematria-expansion-candidate-mapping validate-stage5q `
        --candidate-inventory $Stage5QInventory `
        --token-mapping $Stage5QMapping `
        --native-parity $Stage5QNative `
        --result-store-preflight $Stage5QPreflight `
        --expansion-gate $Stage5QGate `
        --summary $Stage5QSummary `
        --results-dir $Stage5QOut

    Write-Host "Running Stage 5R expanded solved-fixture CUDA parity no-GPU-safe/temp output"
    $Stage5ROut = Join-Path $TempDir "stage5r-gematria-expanded-solved-fixture-cuda"
    $Stage5RRun = Join-Path $TempDir "stage5r-gematria-expanded-solved-fixture-cuda-run.yaml"
    $Stage5RParity = Join-Path $TempDir "stage5r-gematria-expanded-solved-fixture-cuda-parity.yaml"
    $Stage5RBoundary = Join-Path $TempDir "stage5r-gematria-expanded-solved-fixture-cuda-boundary.yaml"
    $Stage5RResultStore = Join-Path $TempDir "stage5r-gematria-expanded-solved-fixture-result-store-preflight.yaml"
    $Stage5RScore = Join-Path $TempDir "stage5r-gematria-expanded-solved-fixture-score-summary-preflight.yaml"
    $Stage5RSummary = Join-Path $TempDir "stage5r-expanded-solved-fixture-cuda-parity-summary.yaml"
    $Stage5RBuild = Join-Path $TempDir "stage5r-cuda-build"
    & $Python -m libreprimus.cli gematria-expanded-solved-fixture-cuda build-run-records `
        --run-records-out $Stage5RRun `
        --out-dir $Stage5ROut `
        --allow-warnings
    & $Python -m libreprimus.cli gematria-expanded-solved-fixture-cuda run-cuda-parity `
        --run-records $Stage5RRun `
        --run-records-out $Stage5RRun `
        --out-dir $Stage5ROut `
        --build-dir $Stage5RBuild `
        --skip-run `
        --allow-warnings
    & $Python -m libreprimus.cli gematria-expanded-solved-fixture-cuda build-parity-records `
        --run-records $Stage5RRun `
        --parity-records-out $Stage5RParity `
        --out-dir $Stage5ROut `
        --allow-warnings
    & $Python -m libreprimus.cli gematria-expanded-solved-fixture-cuda build-boundary-records `
        --run-records $Stage5RRun `
        --parity-records $Stage5RParity `
        --boundaries-out $Stage5RBoundary `
        --out-dir $Stage5ROut `
        --allow-warnings
    & $Python -m libreprimus.cli gematria-expanded-solved-fixture-cuda build-result-store-preflight `
        --parity-records $Stage5RParity `
        --result-store-preflight-out $Stage5RResultStore `
        --out-dir $Stage5ROut `
        --allow-warnings
    & $Python -m libreprimus.cli gematria-expanded-solved-fixture-cuda build-score-summary-preflight `
        --parity-records $Stage5RParity `
        --score-summary-preflight-out $Stage5RScore `
        --out-dir $Stage5ROut `
        --allow-warnings
    & $Python -m libreprimus.cli gematria-expanded-solved-fixture-cuda build-summary `
        --run-records $Stage5RRun `
        --parity-records $Stage5RParity `
        --boundaries $Stage5RBoundary `
        --result-store-preflight $Stage5RResultStore `
        --score-summary-preflight $Stage5RScore `
        --summary-out $Stage5RSummary `
        --out-dir $Stage5ROut `
        --allow-warnings
    & $Python -m libreprimus.cli gematria-expanded-solved-fixture-cuda validate-stage5r `
        --run-records $Stage5RRun `
        --parity-records $Stage5RParity `
        --boundaries $Stage5RBoundary `
        --result-store-preflight $Stage5RResultStore `
        --score-summary-preflight $Stage5RScore `
        --summary $Stage5RSummary `
        --results-dir $Stage5ROut

    Write-Host "Running Stage 5S expanded CUDA result-store integration temp output"
    $Stage5SOut = Join-Path $TempDir "stage5s-gematria-expanded-cuda-result-store"
    $Stage5SParity = Join-Path $TempDir "stage5s-gematria-expanded-cuda-parity-report.yaml"
    $Stage5SResultStore = Join-Path $TempDir "stage5s-gematria-expanded-cuda-result-store-integration.yaml"
    $Stage5SScore = Join-Path $TempDir "stage5s-gematria-expanded-cuda-score-summary-integration.yaml"
    $Stage5SMethod = Join-Path $TempDir "stage5s-gematria-expanded-cuda-method-status-impact.yaml"
    $Stage5SPolicy = Join-Path $TempDir "stage5s-gematria-expanded-cuda-generated-body-policy.yaml"
    $Stage5SBoundary = Join-Path $TempDir "stage5s-gematria-expanded-cuda-boundary-review.yaml"
    $Stage5SDecision = Join-Path $TempDir "stage5s-gematria-expanded-cuda-next-step-decision.yaml"
    $Stage5SSummary = Join-Path $TempDir "stage5s-expanded-cuda-result-store-integration-summary.yaml"
    & $Python -m libreprimus.cli gematria-expanded-cuda-result-store build-parity-report `
        --stage5r-parity $Stage5RParity `
        --stage5r-run $Stage5RRun `
        --parity-report-out $Stage5SParity `
        --out-dir $Stage5SOut `
        --allow-warnings
    & $Python -m libreprimus.cli gematria-expanded-cuda-result-store build-result-store-integration `
        --parity-report $Stage5SParity `
        --result-store-integration-out $Stage5SResultStore `
        --out-dir $Stage5SOut `
        --allow-warnings
    & $Python -m libreprimus.cli gematria-expanded-cuda-result-store build-score-summary-integration `
        --result-store-integration $Stage5SResultStore `
        --score-summary-integration-out $Stage5SScore `
        --out-dir $Stage5SOut `
        --allow-warnings
    & $Python -m libreprimus.cli gematria-expanded-cuda-result-store build-method-status-impact `
        --method-status-impact-out $Stage5SMethod `
        --out-dir $Stage5SOut `
        --allow-warnings
    & $Python -m libreprimus.cli gematria-expanded-cuda-result-store build-generated-body-policy `
        --generated-body-policy-out $Stage5SPolicy `
        --out-dir $Stage5SOut `
        --allow-warnings
    & $Python -m libreprimus.cli gematria-expanded-cuda-result-store build-boundary-review `
        --boundary-review-out $Stage5SBoundary `
        --out-dir $Stage5SOut `
        --allow-warnings
    & $Python -m libreprimus.cli gematria-expanded-cuda-result-store build-next-step-decision `
        --next-step-decision-out $Stage5SDecision `
        --out-dir $Stage5SOut `
        --allow-warnings
    & $Python -m libreprimus.cli gematria-expanded-cuda-result-store build-summary `
        --parity-report $Stage5SParity `
        --result-store-integration $Stage5SResultStore `
        --score-summary-integration $Stage5SScore `
        --method-status-impact $Stage5SMethod `
        --generated-body-policy $Stage5SPolicy `
        --boundary-review $Stage5SBoundary `
        --next-step-decision $Stage5SDecision `
        --stage5r-summary $Stage5RSummary `
        --summary-out $Stage5SSummary `
        --out-dir $Stage5SOut `
        --allow-warnings
    & $Python -m libreprimus.cli gematria-expanded-cuda-result-store validate-stage5s `
        --parity-report $Stage5SParity `
        --result-store-integration $Stage5SResultStore `
        --score-summary-integration $Stage5SScore `
        --method-status-impact $Stage5SMethod `
        --generated-body-policy $Stage5SPolicy `
        --boundary-review $Stage5SBoundary `
        --next-step-decision $Stage5SDecision `
        --summary $Stage5SSummary `
        --results-dir $Stage5SOut

    Write-Host "Running Stage 5T CUDA solved-family readiness temp output"
    $Stage5TOut = Join-Path $TempDir "stage5t-cuda-solved-family-readiness"
    $Stage5TInventory = Join-Path $TempDir "stage5t-solved-family-cuda-inventory.yaml"
    $Stage5TMatrix = Join-Path $TempDir "stage5t-solved-family-cuda-parity-matrix.yaml"
    $Stage5TKernel = Join-Path $TempDir "stage5t-cuda-kernel-readiness.yaml"
    $Stage5TAbi = Join-Path $TempDir "stage5t-cuda-candidate-batch-abi-gaps.yaml"
    $Stage5TBenchmark = Join-Path $TempDir "stage5t-cuda-benchmark-readiness.yaml"
    $Stage5TGuardrail = Join-Path $TempDir "stage5t-cuda-no-unsolved-guardrail-review.yaml"
    $Stage5TDecision = Join-Path $TempDir "stage5t-cuda-next-stage-decision.yaml"
    $Stage5TSummary = Join-Path $TempDir "stage5t-cuda-solved-family-readiness-summary.yaml"
    & $Python -m libreprimus.cli cuda-solved-family-readiness build-solved-family-inventory `
        --fixture-root data/fixtures `
        --solved-family-inventory-out $Stage5TInventory `
        --out-dir $Stage5TOut `
        --allow-warnings
    & $Python -m libreprimus.cli cuda-solved-family-readiness build-parity-matrix `
        --solved-family-inventory $Stage5TInventory `
        --stage5m-summary $Stage5MSummary `
        --stage5r-summary $Stage5RSummary `
        --parity-matrix-out $Stage5TMatrix `
        --out-dir $Stage5TOut `
        --allow-warnings
    & $Python -m libreprimus.cli cuda-solved-family-readiness build-kernel-readiness `
        --parity-matrix $Stage5TMatrix `
        --kernel-readiness-out $Stage5TKernel `
        --out-dir $Stage5TOut `
        --allow-warnings
    & $Python -m libreprimus.cli cuda-solved-family-readiness build-batch-abi-gaps `
        --batch-abi-gaps-out $Stage5TAbi `
        --out-dir $Stage5TOut `
        --allow-warnings
    & $Python -m libreprimus.cli cuda-solved-family-readiness build-benchmark-readiness `
        --benchmark-readiness-out $Stage5TBenchmark `
        --out-dir $Stage5TOut `
        --allow-warnings
    & $Python -m libreprimus.cli cuda-solved-family-readiness build-no-unsolved-guardrail `
        --no-unsolved-guardrail-out $Stage5TGuardrail `
        --out-dir $Stage5TOut `
        --allow-warnings
    & $Python -m libreprimus.cli cuda-solved-family-readiness build-next-stage-decision `
        --batch-abi-gaps $Stage5TAbi `
        --next-stage-decision-out $Stage5TDecision `
        --out-dir $Stage5TOut `
        --allow-warnings
    & $Python -m libreprimus.cli cuda-solved-family-readiness build-summary `
        --solved-family-inventory $Stage5TInventory `
        --parity-matrix $Stage5TMatrix `
        --kernel-readiness $Stage5TKernel `
        --batch-abi-gaps $Stage5TAbi `
        --benchmark-readiness $Stage5TBenchmark `
        --no-unsolved-guardrail $Stage5TGuardrail `
        --next-stage-decision $Stage5TDecision `
        --stage5s-summary $Stage5SSummary `
        --summary-out $Stage5TSummary `
        --out-dir $Stage5TOut `
        --allow-warnings
    & $Python -m libreprimus.cli cuda-solved-family-readiness validate-stage5t `
        --solved-family-inventory $Stage5TInventory `
        --parity-matrix $Stage5TMatrix `
        --kernel-readiness $Stage5TKernel `
        --batch-abi-gaps $Stage5TAbi `
        --benchmark-readiness $Stage5TBenchmark `
        --no-unsolved-guardrail $Stage5TGuardrail `
        --next-stage-decision $Stage5TDecision `
        --summary $Stage5TSummary `
        --results-dir $Stage5TOut

    Write-Host "Running Stage 5U CUDA candidate batch ABI temp output"
    $Stage5UOut = Join-Path $TempDir "stage5u-cuda-candidate-batch-abi"
    $Stage5UAbi = Join-Path $TempDir "stage5u-candidate-batch-abi.yaml"
    $Stage5UToken = Join-Path $TempDir "stage5u-token-buffer-contract.yaml"
    $Stage5UTransform = Join-Path $TempDir "stage5u-transform-parameter-contract.yaml"
    $Stage5UKey = Join-Path $TempDir "stage5u-key-schedule-contract.yaml"
    $Stage5UStream = Join-Path $TempDir "stage5u-stream-schedule-contract.yaml"
    $Stage5UScore = Join-Path $TempDir "stage5u-score-vector-contract.yaml"
    $Stage5UTopk = Join-Path $TempDir "stage5u-topk-output-contract.yaml"
    $Stage5UBackend = Join-Path $TempDir "stage5u-backend-surface-contract.yaml"
    $Stage5UCompat = Join-Path $TempDir "stage5u-result-store-compatibility.yaml"
    $Stage5UGapClosure = Join-Path $TempDir "stage5u-abi-gap-closure.yaml"
    $Stage5UDecision = Join-Path $TempDir "stage5u-next-stage-decision.yaml"
    $Stage5USummary = Join-Path $TempDir "stage5u-candidate-batch-abi-summary.yaml"
    & $Python -m libreprimus.cli cuda-candidate-batch-abi build-candidate-batch-abi --candidate-batch-abi-out $Stage5UAbi --out-dir $Stage5UOut --allow-warnings
    & $Python -m libreprimus.cli cuda-candidate-batch-abi build-token-buffer-contract --token-buffer-contract-out $Stage5UToken --out-dir $Stage5UOut --allow-warnings
    & $Python -m libreprimus.cli cuda-candidate-batch-abi build-transform-parameter-contract --transform-parameter-contract-out $Stage5UTransform --out-dir $Stage5UOut --allow-warnings
    & $Python -m libreprimus.cli cuda-candidate-batch-abi build-key-schedule-contract --key-schedule-contract-out $Stage5UKey --out-dir $Stage5UOut --allow-warnings
    & $Python -m libreprimus.cli cuda-candidate-batch-abi build-stream-schedule-contract --stream-schedule-contract-out $Stage5UStream --out-dir $Stage5UOut --allow-warnings
    & $Python -m libreprimus.cli cuda-candidate-batch-abi build-score-vector-contract --score-vector-contract-out $Stage5UScore --out-dir $Stage5UOut --allow-warnings
    & $Python -m libreprimus.cli cuda-candidate-batch-abi build-topk-output-contract --topk-output-contract-out $Stage5UTopk --out-dir $Stage5UOut --allow-warnings
    & $Python -m libreprimus.cli cuda-candidate-batch-abi build-backend-surface-contract --backend-surface-contract-out $Stage5UBackend --out-dir $Stage5UOut --allow-warnings
    & $Python -m libreprimus.cli cuda-candidate-batch-abi build-result-store-compatibility --result-store-compatibility-out $Stage5UCompat --out-dir $Stage5UOut --allow-warnings
    & $Python -m libreprimus.cli cuda-candidate-batch-abi build-gap-closure --stage5t-gaps $Stage5TAbi --gap-closure-out $Stage5UGapClosure --out-dir $Stage5UOut --allow-warnings
    & $Python -m libreprimus.cli cuda-candidate-batch-abi build-next-stage-decision --gap-closure $Stage5UGapClosure --next-stage-decision-out $Stage5UDecision --out-dir $Stage5UOut --allow-warnings
    & $Python -m libreprimus.cli cuda-candidate-batch-abi build-summary `
        --candidate-batch-abi $Stage5UAbi `
        --token-buffer-contract $Stage5UToken `
        --transform-parameter-contract $Stage5UTransform `
        --key-schedule-contract $Stage5UKey `
        --stream-schedule-contract $Stage5UStream `
        --score-vector-contract $Stage5UScore `
        --topk-output-contract $Stage5UTopk `
        --backend-surface-contract $Stage5UBackend `
        --result-store-compatibility $Stage5UCompat `
        --gap-closure $Stage5UGapClosure `
        --next-stage-decision $Stage5UDecision `
        --stage5t-gaps $Stage5TAbi `
        --stage5t-summary $Stage5TSummary `
        --summary-out $Stage5USummary `
        --out-dir $Stage5UOut `
        --allow-warnings
    & $Python -m libreprimus.cli cuda-candidate-batch-abi validate-stage5u `
        --candidate-batch-abi $Stage5UAbi `
        --token-buffer-contract $Stage5UToken `
        --transform-parameter-contract $Stage5UTransform `
        --key-schedule-contract $Stage5UKey `
        --stream-schedule-contract $Stage5UStream `
        --score-vector-contract $Stage5UScore `
        --topk-output-contract $Stage5UTopk `
        --backend-surface-contract $Stage5UBackend `
        --result-store-compatibility $Stage5UCompat `
        --gap-closure $Stage5UGapClosure `
        --next-stage-decision $Stage5UDecision `
        --summary $Stage5USummary `
        --results-dir $Stage5UOut

    Write-Host "Running Stage 5V native Candidate Batch ABI conformance temp output"
    $Stage5VOut = Join-Path $TempDir "stage5v-native-candidate-batch-conformance"
    $Stage5VAdapter = Join-Path $TempDir "stage5v-native-candidate-batch-adapter.yaml"
    $Stage5VFixtures = Join-Path $TempDir "stage5v-candidate-batch-conformance-fixtures.yaml"
    $Stage5VToken = Join-Path $TempDir "stage5v-token-buffer-conformance.yaml"
    $Stage5VSchedule = Join-Path $TempDir "stage5v-schedule-conformance.yaml"
    $Stage5VScore = Join-Path $TempDir "stage5v-score-vector-conformance.yaml"
    $Stage5VTopk = Join-Path $TempDir "stage5v-topk-conformance.yaml"
    $Stage5VResultStore = Join-Path $TempDir "stage5v-native-conformance-result-store.yaml"
    $Stage5VStatus = Join-Path $TempDir "stage5v-abi-implementation-status.yaml"
    $Stage5VDecision = Join-Path $TempDir "stage5v-next-stage-decision.yaml"
    $Stage5VSummary = Join-Path $TempDir "stage5v-native-candidate-batch-conformance-summary.yaml"
    & $Python -m libreprimus.cli native-candidate-batch-conformance build-adapter-records --adapter-records-out $Stage5VAdapter --out-dir $Stage5VOut --allow-warnings
    & $Python -m libreprimus.cli native-candidate-batch-conformance build-conformance-fixtures --conformance-fixtures-out $Stage5VFixtures --out-dir $Stage5VOut --allow-warnings
    & $Python -m libreprimus.cli native-candidate-batch-conformance run-native-conformance --conformance-fixtures $Stage5VFixtures --out-dir $Stage5VOut --allow-warnings
    & $Python -m libreprimus.cli native-candidate-batch-conformance build-token-buffer-conformance --conformance-fixtures $Stage5VFixtures --token-buffer-conformance-out $Stage5VToken --out-dir $Stage5VOut --allow-warnings
    & $Python -m libreprimus.cli native-candidate-batch-conformance build-schedule-conformance --schedule-conformance-out $Stage5VSchedule --out-dir $Stage5VOut --allow-warnings
    & $Python -m libreprimus.cli native-candidate-batch-conformance build-score-vector-conformance --score-vector-conformance-out $Stage5VScore --out-dir $Stage5VOut --allow-warnings
    & $Python -m libreprimus.cli native-candidate-batch-conformance build-topk-conformance --topk-conformance-out $Stage5VTopk --out-dir $Stage5VOut --allow-warnings
    & $Python -m libreprimus.cli native-candidate-batch-conformance build-result-store-conformance --result-store-conformance-out $Stage5VResultStore --out-dir $Stage5VOut --allow-warnings
    & $Python -m libreprimus.cli native-candidate-batch-conformance build-implementation-status --implementation-status-out $Stage5VStatus --out-dir $Stage5VOut --allow-warnings
    & $Python -m libreprimus.cli native-candidate-batch-conformance build-next-stage-decision --next-stage-decision-out $Stage5VDecision --out-dir $Stage5VOut --allow-warnings
    & $Python -m libreprimus.cli native-candidate-batch-conformance build-summary `
        --adapter-records $Stage5VAdapter `
        --conformance-fixtures $Stage5VFixtures `
        --token-buffer-conformance $Stage5VToken `
        --schedule-conformance $Stage5VSchedule `
        --score-vector-conformance $Stage5VScore `
        --topk-conformance $Stage5VTopk `
        --result-store-conformance $Stage5VResultStore `
        --implementation-status $Stage5VStatus `
        --next-stage-decision $Stage5VDecision `
        --summary-out $Stage5VSummary `
        --out-dir $Stage5VOut `
        --allow-warnings
    & $Python -m libreprimus.cli native-candidate-batch-conformance validate-stage5v `
        --adapter-records $Stage5VAdapter `
        --conformance-fixtures $Stage5VFixtures `
        --token-buffer-conformance $Stage5VToken `
        --schedule-conformance $Stage5VSchedule `
        --score-vector-conformance $Stage5VScore `
        --topk-conformance $Stage5VTopk `
        --result-store-conformance $Stage5VResultStore `
        --implementation-status $Stage5VStatus `
        --next-stage-decision $Stage5VDecision `
        --summary $Stage5VSummary `
        --results-dir $Stage5VOut

    Write-Host "Running Stage 5W prime-minus-one native contract temp output"
    $Stage5WOut = Join-Path $TempDir "stage5w-prime-minus-one-native-contract"
    $Stage5WSourceInventory = Join-Path $TempDir "stage5w-prime-minus-one-source-inventory.yaml"
    $Stage5WStreamContract = Join-Path $TempDir "stage5w-prime-minus-one-stream-contract.yaml"
    $Stage5WPrimeSchedule = Join-Path $TempDir "stage5w-prime-minus-one-schedule.yaml"
    $Stage5WMapping = Join-Path $TempDir "stage5w-prime-minus-one-candidate-batch-mapping.yaml"
    $Stage5WPreparation = Join-Path $TempDir "stage5w-prime-minus-one-native-parity-preparation.yaml"
    $Stage5WResultStore = Join-Path $TempDir "stage5w-prime-minus-one-result-store-preflight.yaml"
    $Stage5WGuardrail = Join-Path $TempDir "stage5w-prime-minus-one-guardrail.yaml"
    $Stage5WDecision = Join-Path $TempDir "stage5w-prime-minus-one-next-stage-decision.yaml"
    $Stage5WSummary = Join-Path $TempDir "stage5w-prime-minus-one-native-contract-summary.yaml"
    & $Python -m libreprimus.cli prime-minus-one-native-contract build-source-inventory --source-inventory-out $Stage5WSourceInventory --out-dir $Stage5WOut --allow-warnings
    & $Python -m libreprimus.cli prime-minus-one-native-contract build-stream-contract --stream-contract-out $Stage5WStreamContract --out-dir $Stage5WOut --allow-warnings
    & $Python -m libreprimus.cli prime-minus-one-native-contract build-prime-schedule --prime-schedule-out $Stage5WPrimeSchedule --out-dir $Stage5WOut --allow-warnings
    & $Python -m libreprimus.cli prime-minus-one-native-contract build-candidate-batch-mapping --candidate-batch-mapping-out $Stage5WMapping --out-dir $Stage5WOut --allow-warnings
    & $Python -m libreprimus.cli prime-minus-one-native-contract build-native-parity-preparation --native-parity-preparation-out $Stage5WPreparation --out-dir $Stage5WOut --allow-warnings
    & $Python -m libreprimus.cli prime-minus-one-native-contract build-result-store-preflight --result-store-preflight-out $Stage5WResultStore --out-dir $Stage5WOut --allow-warnings
    & $Python -m libreprimus.cli prime-minus-one-native-contract build-guardrails --guardrail-out $Stage5WGuardrail --out-dir $Stage5WOut --allow-warnings
    & $Python -m libreprimus.cli prime-minus-one-native-contract build-next-stage-decision --next-stage-decision-out $Stage5WDecision --out-dir $Stage5WOut --allow-warnings
    & $Python -m libreprimus.cli prime-minus-one-native-contract build-summary `
        --source-inventory $Stage5WSourceInventory `
        --stream-contract $Stage5WStreamContract `
        --prime-schedule $Stage5WPrimeSchedule `
        --candidate-batch-mapping $Stage5WMapping `
        --native-parity-preparation $Stage5WPreparation `
        --result-store-preflight $Stage5WResultStore `
        --guardrail $Stage5WGuardrail `
        --next-stage-decision $Stage5WDecision `
        --summary-out $Stage5WSummary `
        --out-dir $Stage5WOut `
        --allow-warnings
    & $Python -m libreprimus.cli prime-minus-one-native-contract validate-stage5w `
        --source-inventory $Stage5WSourceInventory `
        --stream-contract $Stage5WStreamContract `
        --prime-schedule $Stage5WPrimeSchedule `
        --candidate-batch-mapping $Stage5WMapping `
        --native-parity-preparation $Stage5WPreparation `
        --result-store-preflight $Stage5WResultStore `
        --guardrail $Stage5WGuardrail `
        --next-stage-decision $Stage5WDecision `
        --summary $Stage5WSummary `
        --results-dir $Stage5WOut

    Write-Host "Running Stage 5X prime-minus-one native parity temp output"
    $Stage5XOut = Join-Path $TempDir "stage5x-prime-minus-one-native-parity"
    $Stage5XRun = Join-Path $TempDir "stage5x-prime-minus-one-native-run.yaml"
    $Stage5XParity = Join-Path $TempDir "stage5x-prime-minus-one-native-parity.yaml"
    $Stage5XResultStore = Join-Path $TempDir "stage5x-prime-minus-one-native-result-store-preflight.yaml"
    $Stage5XScore = Join-Path $TempDir "stage5x-prime-minus-one-native-score-summary-preflight.yaml"
    $Stage5XBlocker = Join-Path $TempDir "stage5x-prime-minus-one-full-p56-blocker.yaml"
    $Stage5XGuardrail = Join-Path $TempDir "stage5x-prime-minus-one-native-guardrail.yaml"
    $Stage5XDecision = Join-Path $TempDir "stage5x-prime-minus-one-native-next-stage-decision.yaml"
    $Stage5XSummary = Join-Path $TempDir "stage5x-prime-minus-one-native-parity-summary.yaml"
    & $Python -m libreprimus.cli prime-minus-one-native-parity build-run-records --native-run-out $Stage5XRun --out-dir $Stage5XOut --allow-warnings
    & $Python -m libreprimus.cli prime-minus-one-native-parity build-parity-records --native-run $Stage5XRun --native-parity-out $Stage5XParity --out-dir $Stage5XOut --allow-warnings
    & $Python -m libreprimus.cli prime-minus-one-native-parity build-result-store-preflight --native-parity $Stage5XParity --result-store-preflight-out $Stage5XResultStore --out-dir $Stage5XOut --allow-warnings
    & $Python -m libreprimus.cli prime-minus-one-native-parity build-score-summary-preflight --native-parity $Stage5XParity --score-summary-preflight-out $Stage5XScore --out-dir $Stage5XOut --allow-warnings
    & $Python -m libreprimus.cli prime-minus-one-native-parity build-full-p56-blocker --full-p56-blocker-out $Stage5XBlocker --out-dir $Stage5XOut --allow-warnings
    & $Python -m libreprimus.cli prime-minus-one-native-parity build-guardrails --guardrail-out $Stage5XGuardrail --out-dir $Stage5XOut --allow-warnings
    & $Python -m libreprimus.cli prime-minus-one-native-parity build-next-stage-decision --native-parity $Stage5XParity --next-stage-decision-out $Stage5XDecision --out-dir $Stage5XOut --allow-warnings
    & $Python -m libreprimus.cli prime-minus-one-native-parity build-summary `
        --native-run $Stage5XRun `
        --native-parity $Stage5XParity `
        --result-store-preflight $Stage5XResultStore `
        --score-summary-preflight $Stage5XScore `
        --full-p56-blocker $Stage5XBlocker `
        --guardrail $Stage5XGuardrail `
        --next-stage-decision $Stage5XDecision `
        --summary-out $Stage5XSummary `
        --out-dir $Stage5XOut `
        --allow-warnings
    & $Python -m libreprimus.cli prime-minus-one-native-parity validate-stage5x `
        --native-run $Stage5XRun `
        --native-parity $Stage5XParity `
        --result-store-preflight $Stage5XResultStore `
        --score-summary-preflight $Stage5XScore `
        --full-p56-blocker $Stage5XBlocker `
        --guardrail $Stage5XGuardrail `
        --next-stage-decision $Stage5XDecision `
        --summary $Stage5XSummary `
        --results-dir $Stage5XOut

    Write-Host "Running Stage 5Y prime-minus-one native reporting temp output"
    $Stage5YOut = Join-Path $TempDir "stage5y-prime-minus-one-native-reporting"
    $Stage5YParity = Join-Path $TempDir "stage5y-prime-minus-one-native-parity-report.yaml"
    $Stage5YResultStore = Join-Path $TempDir "stage5y-prime-minus-one-native-result-store-integration.yaml"
    $Stage5YScore = Join-Path $TempDir "stage5y-prime-minus-one-native-score-summary-integration.yaml"
    $Stage5YMethod = Join-Path $TempDir "stage5y-prime-minus-one-native-method-status-impact.yaml"
    $Stage5YPolicy = Join-Path $TempDir "stage5y-prime-minus-one-generated-body-policy.yaml"
    $Stage5YBlocker = Join-Path $TempDir "stage5y-prime-minus-one-full-p56-blocker-preservation.yaml"
    $Stage5YGate = Join-Path $TempDir "stage5y-prime-minus-one-cuda-contract-readiness-gate.yaml"
    $Stage5YScored = Join-Path $TempDir "stage5y-bounded-scored-experiment-readiness.yaml"
    $Stage5YGuardrail = Join-Path $TempDir "stage5y-prime-minus-one-native-reporting-guardrail.yaml"
    $Stage5YDecision = Join-Path $TempDir "stage5y-prime-minus-one-native-reporting-next-stage-decision.yaml"
    $Stage5YSummary = Join-Path $TempDir "stage5y-prime-minus-one-native-reporting-summary.yaml"
    & $Python -m libreprimus.cli prime-minus-one-native-reporting build-parity-report --parity-report-out $Stage5YParity --out-dir $Stage5YOut --allow-warnings
    & $Python -m libreprimus.cli prime-minus-one-native-reporting build-result-store-integration --parity-report $Stage5YParity --result-store-integration-out $Stage5YResultStore --out-dir $Stage5YOut --allow-warnings
    & $Python -m libreprimus.cli prime-minus-one-native-reporting build-score-summary-integration --parity-report $Stage5YParity --score-summary-integration-out $Stage5YScore --out-dir $Stage5YOut --allow-warnings
    & $Python -m libreprimus.cli prime-minus-one-native-reporting build-method-status-impact --method-status-impact-out $Stage5YMethod --out-dir $Stage5YOut --allow-warnings
    & $Python -m libreprimus.cli prime-minus-one-native-reporting build-generated-body-policy --generated-body-policy-out $Stage5YPolicy --out-dir $Stage5YOut --allow-warnings
    & $Python -m libreprimus.cli prime-minus-one-native-reporting build-full-p56-blocker-preservation --full-p56-blocker-preservation-out $Stage5YBlocker --out-dir $Stage5YOut --allow-warnings
    & $Python -m libreprimus.cli prime-minus-one-native-reporting build-cuda-contract-readiness-gate --parity-report $Stage5YParity --result-store-integration $Stage5YResultStore --score-summary-integration $Stage5YScore --cuda-contract-readiness-gate-out $Stage5YGate --out-dir $Stage5YOut --allow-warnings
    & $Python -m libreprimus.cli prime-minus-one-native-reporting build-scored-experiment-readiness --scored-experiment-readiness-out $Stage5YScored --out-dir $Stage5YOut --allow-warnings
    & $Python -m libreprimus.cli prime-minus-one-native-reporting build-guardrails --guardrail-out $Stage5YGuardrail --out-dir $Stage5YOut --allow-warnings
    & $Python -m libreprimus.cli prime-minus-one-native-reporting build-next-stage-decision --cuda-contract-readiness-gate $Stage5YGate --next-stage-decision-out $Stage5YDecision --out-dir $Stage5YOut --allow-warnings
    & $Python -m libreprimus.cli prime-minus-one-native-reporting build-summary `
        --parity-report $Stage5YParity `
        --result-store-integration $Stage5YResultStore `
        --score-summary-integration $Stage5YScore `
        --method-status-impact $Stage5YMethod `
        --generated-body-policy $Stage5YPolicy `
        --full-p56-blocker-preservation $Stage5YBlocker `
        --cuda-contract-readiness-gate $Stage5YGate `
        --scored-experiment-readiness $Stage5YScored `
        --guardrail $Stage5YGuardrail `
        --next-stage-decision $Stage5YDecision `
        --summary-out $Stage5YSummary `
        --out-dir $Stage5YOut `
        --allow-warnings
    & $Python -m libreprimus.cli prime-minus-one-native-reporting validate-stage5y `
        --parity-report $Stage5YParity `
        --result-store-integration $Stage5YResultStore `
        --score-summary-integration $Stage5YScore `
        --method-status-impact $Stage5YMethod `
        --generated-body-policy $Stage5YPolicy `
        --full-p56-blocker-preservation $Stage5YBlocker `
        --cuda-contract-readiness-gate $Stage5YGate `
        --scored-experiment-readiness $Stage5YScored `
        --guardrail $Stage5YGuardrail `
        --next-stage-decision $Stage5YDecision `
        --summary $Stage5YSummary `
        --results-dir $Stage5YOut

    Write-Host "Running Stage 5Z prime-minus-one CUDA contract temp output"
    $Stage5ZOut = Join-Path $TempDir "stage5z-prime-minus-one-cuda-contract"
    $Stage5ZContract = Join-Path $TempDir "stage5z-prime-minus-one-cuda-contract.yaml"
    $Stage5ZKernel = Join-Path $TempDir "stage5z-prime-minus-one-cuda-kernel-abi.yaml"
    $Stage5ZHost = Join-Path $TempDir "stage5z-prime-minus-one-cuda-host-runner-contract.yaml"
    $Stage5ZBuffer = Join-Path $TempDir "stage5z-prime-minus-one-cuda-buffer-contract.yaml"
    $Stage5ZVectors = Join-Path $TempDir "stage5z-prime-minus-one-cuda-validation-vectors.yaml"
    $Stage5ZFuture = Join-Path $TempDir "stage5z-prime-minus-one-cuda-future-parity-plan.yaml"
    $Stage5ZResult = Join-Path $TempDir "stage5z-prime-minus-one-cuda-result-store-compatibility.yaml"
    $Stage5ZBlocker = Join-Path $TempDir "stage5z-prime-minus-one-cuda-full-p56-blocker.yaml"
    $Stage5ZScored = Join-Path $TempDir "stage5z-prime-minus-one-scored-experiment-deferral.yaml"
    $Stage5ZGate = Join-Path $TempDir "stage5z-prime-minus-one-cuda-implementation-readiness-gate.yaml"
    $Stage5ZDecision = Join-Path $TempDir "stage5z-prime-minus-one-cuda-next-stage-decision.yaml"
    $Stage5ZSummary = Join-Path $TempDir "stage5z-prime-minus-one-cuda-contract-summary.yaml"
    & $Python -m libreprimus.cli prime-minus-one-cuda-contract build-contract-records `
        --cuda-contract-out $Stage5ZContract --out-dir $Stage5ZOut --allow-warnings
    & $Python -m libreprimus.cli prime-minus-one-cuda-contract build-kernel-abi `
        --kernel-abi-out $Stage5ZKernel --out-dir $Stage5ZOut --allow-warnings
    & $Python -m libreprimus.cli prime-minus-one-cuda-contract build-host-runner-contract `
        --host-runner-contract-out $Stage5ZHost --out-dir $Stage5ZOut --allow-warnings
    & $Python -m libreprimus.cli prime-minus-one-cuda-contract build-buffer-contract `
        --buffer-contract-out $Stage5ZBuffer --out-dir $Stage5ZOut --allow-warnings
    & $Python -m libreprimus.cli prime-minus-one-cuda-contract build-validation-vectors `
        --validation-vectors-out $Stage5ZVectors --out-dir $Stage5ZOut --allow-warnings
    & $Python -m libreprimus.cli prime-minus-one-cuda-contract build-future-parity-plan `
        --future-parity-plan-out $Stage5ZFuture --out-dir $Stage5ZOut --allow-warnings
    & $Python -m libreprimus.cli prime-minus-one-cuda-contract build-result-store-compatibility `
        --result-store-compatibility-out $Stage5ZResult --out-dir $Stage5ZOut --allow-warnings
    & $Python -m libreprimus.cli prime-minus-one-cuda-contract build-full-p56-blocker `
        --full-p56-blocker-out $Stage5ZBlocker --out-dir $Stage5ZOut --allow-warnings
    & $Python -m libreprimus.cli prime-minus-one-cuda-contract build-scored-experiment-deferral `
        --scored-experiment-deferral-out $Stage5ZScored --out-dir $Stage5ZOut --allow-warnings
    & $Python -m libreprimus.cli prime-minus-one-cuda-contract build-implementation-readiness-gate `
        --implementation-readiness-out $Stage5ZGate --out-dir $Stage5ZOut --allow-warnings
    & $Python -m libreprimus.cli prime-minus-one-cuda-contract build-next-stage-decision `
        --next-stage-decision-out $Stage5ZDecision --out-dir $Stage5ZOut --allow-warnings
    & $Python -m libreprimus.cli prime-minus-one-cuda-contract build-summary `
        --cuda-contract $Stage5ZContract `
        --kernel-abi $Stage5ZKernel `
        --host-runner-contract $Stage5ZHost `
        --buffer-contract $Stage5ZBuffer `
        --validation-vectors $Stage5ZVectors `
        --future-parity-plan $Stage5ZFuture `
        --result-store-compatibility $Stage5ZResult `
        --full-p56-blocker $Stage5ZBlocker `
        --scored-experiment-deferral $Stage5ZScored `
        --implementation-readiness-gate $Stage5ZGate `
        --next-stage-decision $Stage5ZDecision `
        --summary-out $Stage5ZSummary `
        --out-dir $Stage5ZOut `
        --allow-warnings
    & $Python -m libreprimus.cli prime-minus-one-cuda-contract validate-stage5z `
        --cuda-contract $Stage5ZContract `
        --kernel-abi $Stage5ZKernel `
        --host-runner-contract $Stage5ZHost `
        --buffer-contract $Stage5ZBuffer `
        --validation-vectors $Stage5ZVectors `
        --future-parity-plan $Stage5ZFuture `
        --result-store-compatibility $Stage5ZResult `
        --full-p56-blocker $Stage5ZBlocker `
        --scored-experiment-deferral $Stage5ZScored `
        --implementation-readiness-gate $Stage5ZGate `
        --next-stage-decision $Stage5ZDecision `
        --summary $Stage5ZSummary `
        --results-dir $Stage5ZOut

    Write-Host "Running Stage 5AA prime-minus-one CUDA synthetic temp output"
    $Stage5AAOut = Join-Path $TempDir "stage5aa-prime-minus-one-cuda-synthetic"
    $Stage5AAKernel = Join-Path $TempDir "stage5aa-prime-minus-one-cuda-synthetic-kernel-implementation.yaml"
    $Stage5AARun = Join-Path $TempDir "stage5aa-prime-minus-one-cuda-synthetic-run.yaml"
    $Stage5AAParity = Join-Path $TempDir "stage5aa-prime-minus-one-cuda-synthetic-parity.yaml"
    $Stage5AAAudit = Join-Path $TempDir "stage5aa-prime-minus-one-cuda-device-subset-audit.yaml"
    $Stage5AAResult = Join-Path $TempDir "stage5aa-prime-minus-one-cuda-synthetic-result-store-preflight.yaml"
    $Stage5AABlocker = Join-Path $TempDir "stage5aa-prime-minus-one-cuda-synthetic-p56-blocker.yaml"
    $Stage5AAScored = Join-Path $TempDir "stage5aa-prime-minus-one-cuda-synthetic-scored-experiment-deferral.yaml"
    $Stage5AADecision = Join-Path $TempDir "stage5aa-prime-minus-one-cuda-synthetic-next-stage-decision.yaml"
    $Stage5AASummary = Join-Path $TempDir "stage5aa-prime-minus-one-cuda-synthetic-summary.yaml"
    & $Python -m libreprimus.cli prime-minus-one-cuda-synthetic build-kernel-implementation-records `
        --kernel-implementation-out $Stage5AAKernel --out-dir $Stage5AAOut --allow-warnings
    & $Python -m libreprimus.cli prime-minus-one-cuda-synthetic run-synthetic-cuda-parity `
        --cuda-run-out $Stage5AARun --out-dir $Stage5AAOut --skip-cuda --allow-warnings
    & $Python -m libreprimus.cli prime-minus-one-cuda-synthetic build-parity-records `
        --cuda-run $Stage5AARun --parity-out $Stage5AAParity --out-dir $Stage5AAOut --allow-warnings
    & $Python -m libreprimus.cli prime-minus-one-cuda-synthetic build-device-subset-audit `
        --device-subset-audit-out $Stage5AAAudit --out-dir $Stage5AAOut --allow-warnings
    & $Python -m libreprimus.cli prime-minus-one-cuda-synthetic build-result-store-preflight `
        --result-store-preflight-out $Stage5AAResult --out-dir $Stage5AAOut --allow-warnings
    & $Python -m libreprimus.cli prime-minus-one-cuda-synthetic build-p56-blocker `
        --p56-blocker-out $Stage5AABlocker --out-dir $Stage5AAOut --allow-warnings
    & $Python -m libreprimus.cli prime-minus-one-cuda-synthetic build-scored-experiment-deferral `
        --scored-experiment-deferral-out $Stage5AAScored --out-dir $Stage5AAOut --allow-warnings
    & $Python -m libreprimus.cli prime-minus-one-cuda-synthetic build-next-stage-decision `
        --parity $Stage5AAParity --next-stage-decision-out $Stage5AADecision --out-dir $Stage5AAOut --allow-warnings
    & $Python -m libreprimus.cli prime-minus-one-cuda-synthetic build-summary `
        --kernel-implementation $Stage5AAKernel `
        --cuda-run $Stage5AARun `
        --parity $Stage5AAParity `
        --device-subset-audit $Stage5AAAudit `
        --result-store-preflight $Stage5AAResult `
        --p56-blocker $Stage5AABlocker `
        --scored-experiment-deferral $Stage5AAScored `
        --next-stage-decision $Stage5AADecision `
        --summary-out $Stage5AASummary `
        --out-dir $Stage5AAOut `
        --allow-warnings
    & $Python -m libreprimus.cli prime-minus-one-cuda-synthetic validate-stage5aa `
        --kernel-implementation $Stage5AAKernel `
        --cuda-run $Stage5AARun `
        --parity $Stage5AAParity `
        --device-subset-audit $Stage5AAAudit `
        --result-store-preflight $Stage5AAResult `
        --p56-blocker $Stage5AABlocker `
        --scored-experiment-deferral $Stage5AAScored `
        --next-stage-decision $Stage5AADecision `
        --summary $Stage5AASummary `
        --results-dir $Stage5AAOut

    Write-Host "Running Stage 5AC prime-minus-one CUDA synthetic reporting temp output"
    $Stage5ACOut = Join-Path $TempDir "stage5ac-prime-minus-one-cuda-synthetic-reporting"
    $Stage5ACParity = Join-Path $TempDir "stage5ac-prime-minus-one-cuda-synthetic-parity-report.yaml"
    $Stage5ACResult = Join-Path $TempDir "stage5ac-prime-minus-one-cuda-synthetic-result-store-integration.yaml"
    $Stage5ACScore = Join-Path $TempDir "stage5ac-prime-minus-one-cuda-synthetic-score-summary-integration.yaml"
    $Stage5ACMethod = Join-Path $TempDir "stage5ac-prime-minus-one-cuda-synthetic-method-status-impact.yaml"
    $Stage5ACPolicy = Join-Path $TempDir "stage5ac-prime-minus-one-cuda-synthetic-generated-body-policy.yaml"
    $Stage5ACBounded = Join-Path $TempDir "stage5ac-bounded-p56-cuda-parity-preflight.yaml"
    $Stage5ACFull = Join-Path $TempDir "stage5ac-prime-minus-one-cuda-synthetic-full-p56-blocker.yaml"
    $Stage5ACScored = Join-Path $TempDir "stage5ac-prime-minus-one-cuda-synthetic-scored-experiment-deferral.yaml"
    $Stage5ACDocs = Join-Path $TempDir "stage5ac-prime-minus-one-cuda-synthetic-doc-staleness-validation.yaml"
    $Stage5ACDecision = Join-Path $TempDir "stage5ac-prime-minus-one-cuda-synthetic-next-stage-decision.yaml"
    $Stage5ACSummary = Join-Path $TempDir "stage5ac-prime-minus-one-cuda-synthetic-reporting-summary.yaml"
    & $Python -m libreprimus.cli prime-minus-one-cuda-synthetic-reporting build-parity-report `
        --parity-report-out $Stage5ACParity --out-dir $Stage5ACOut --allow-warnings
    & $Python -m libreprimus.cli prime-minus-one-cuda-synthetic-reporting build-result-store-integration `
        --parity-report $Stage5ACParity --result-store-integration-out $Stage5ACResult --out-dir $Stage5ACOut --allow-warnings
    & $Python -m libreprimus.cli prime-minus-one-cuda-synthetic-reporting build-score-summary-integration `
        --parity-report $Stage5ACParity --score-summary-integration-out $Stage5ACScore --out-dir $Stage5ACOut --allow-warnings
    & $Python -m libreprimus.cli prime-minus-one-cuda-synthetic-reporting build-method-status-impact `
        --method-status-impact-out $Stage5ACMethod --out-dir $Stage5ACOut --allow-warnings
    & $Python -m libreprimus.cli prime-minus-one-cuda-synthetic-reporting build-generated-body-policy `
        --generated-body-policy-out $Stage5ACPolicy --out-dir $Stage5ACOut --allow-warnings
    & $Python -m libreprimus.cli prime-minus-one-cuda-synthetic-reporting build-doc-staleness-validation `
        --doc-staleness-validation-out $Stage5ACDocs --out-dir $Stage5ACOut --allow-warnings
    & $Python -m libreprimus.cli prime-minus-one-cuda-synthetic-reporting build-bounded-p56-preflight `
        --parity-report $Stage5ACParity `
        --doc-staleness-validation $Stage5ACDocs `
        --bounded-p56-preflight-out $Stage5ACBounded `
        --out-dir $Stage5ACOut `
        --allow-warnings
    & $Python -m libreprimus.cli prime-minus-one-cuda-synthetic-reporting build-full-p56-blocker `
        --full-p56-blocker-out $Stage5ACFull --out-dir $Stage5ACOut --allow-warnings
    & $Python -m libreprimus.cli prime-minus-one-cuda-synthetic-reporting build-scored-experiment-deferral `
        --scored-experiment-deferral-out $Stage5ACScored --out-dir $Stage5ACOut --allow-warnings
    & $Python -m libreprimus.cli prime-minus-one-cuda-synthetic-reporting build-next-stage-decision `
        --parity-report $Stage5ACParity `
        --bounded-p56-preflight $Stage5ACBounded `
        --doc-staleness-validation $Stage5ACDocs `
        --next-stage-decision-out $Stage5ACDecision `
        --out-dir $Stage5ACOut `
        --allow-warnings
    & $Python -m libreprimus.cli prime-minus-one-cuda-synthetic-reporting build-summary `
        --parity-report $Stage5ACParity `
        --result-store-integration $Stage5ACResult `
        --score-summary-integration $Stage5ACScore `
        --method-status-impact $Stage5ACMethod `
        --generated-body-policy $Stage5ACPolicy `
        --bounded-p56-preflight $Stage5ACBounded `
        --full-p56-blocker $Stage5ACFull `
        --scored-experiment-deferral $Stage5ACScored `
        --doc-staleness-validation $Stage5ACDocs `
        --next-stage-decision $Stage5ACDecision `
        --summary-out $Stage5ACSummary `
        --out-dir $Stage5ACOut `
        --allow-warnings
    & $Python -m libreprimus.cli prime-minus-one-cuda-synthetic-reporting validate-stage5ac `
        --parity-report $Stage5ACParity `
        --result-store-integration $Stage5ACResult `
        --score-summary-integration $Stage5ACScore `
        --method-status-impact $Stage5ACMethod `
        --generated-body-policy $Stage5ACPolicy `
        --bounded-p56-preflight $Stage5ACBounded `
        --full-p56-blocker $Stage5ACFull `
        --scored-experiment-deferral $Stage5ACScored `
        --doc-staleness-validation $Stage5ACDocs `
        --next-stage-decision $Stage5ACDecision `
        --summary $Stage5ACSummary `
        --results-dir $Stage5ACOut

    Write-Host "Running Stage 5AD bounded p56 CUDA parity skipped-CUDA temp output"
    $Stage5ADOut = Join-Path $TempDir "stage5ad-bounded-p56-cuda-parity"
    $Stage5ADBuild = Join-Path $TempDir "stage5ad-bounded-p56-cuda-build"
    $Stage5ADRun = Join-Path $TempDir "stage5ad-bounded-p56-cuda-run.yaml"
    $Stage5ADParity = Join-Path $TempDir "stage5ad-bounded-p56-cuda-parity.yaml"
    $Stage5ADResult = Join-Path $TempDir "stage5ad-bounded-p56-cuda-result-store-preflight.yaml"
    $Stage5ADScore = Join-Path $TempDir "stage5ad-bounded-p56-cuda-score-summary-preflight.yaml"
    $Stage5ADFull = Join-Path $TempDir "stage5ad-bounded-p56-cuda-full-p56-blocker.yaml"
    $Stage5ADScored = Join-Path $TempDir "stage5ad-bounded-p56-cuda-scored-experiment-deferral.yaml"
    $Stage5ADDocs = Join-Path $TempDir "stage5ad-bounded-p56-cuda-doc-staleness-validation.yaml"
    $Stage5ADAudit = Join-Path $TempDir "stage5ad-bounded-p56-cuda-device-subset-audit.yaml"
    $Stage5ADDecision = Join-Path $TempDir "stage5ad-bounded-p56-cuda-next-stage-decision.yaml"
    $Stage5ADSummary = Join-Path $TempDir "stage5ad-bounded-p56-cuda-parity-summary.yaml"
    & $Python -m libreprimus.cli bounded-p56-cuda-parity build-run-records `
        --cuda-run-out $Stage5ADRun --out-dir $Stage5ADOut --allow-warnings
    & $Python -m libreprimus.cli bounded-p56-cuda-parity run-bounded-p56-cuda `
        --cuda-run-out $Stage5ADRun --out-dir $Stage5ADOut --build-dir $Stage5ADBuild --skip-cuda --allow-warnings
    & $Python -m libreprimus.cli bounded-p56-cuda-parity build-parity-records `
        --cuda-run $Stage5ADRun --cuda-parity-out $Stage5ADParity --out-dir $Stage5ADOut --allow-warnings
    & $Python -m libreprimus.cli bounded-p56-cuda-parity build-result-store-preflight `
        --cuda-parity $Stage5ADParity --result-store-preflight-out $Stage5ADResult --out-dir $Stage5ADOut --allow-warnings
    & $Python -m libreprimus.cli bounded-p56-cuda-parity build-score-summary-preflight `
        --cuda-parity $Stage5ADParity --score-summary-preflight-out $Stage5ADScore --out-dir $Stage5ADOut --allow-warnings
    & $Python -m libreprimus.cli bounded-p56-cuda-parity build-full-p56-blocker `
        --full-p56-blocker-out $Stage5ADFull --out-dir $Stage5ADOut --allow-warnings
    & $Python -m libreprimus.cli bounded-p56-cuda-parity build-scored-experiment-deferral `
        --scored-experiment-deferral-out $Stage5ADScored --out-dir $Stage5ADOut --allow-warnings
    & $Python -m libreprimus.cli bounded-p56-cuda-parity build-doc-staleness-validation `
        --doc-staleness-validation-out $Stage5ADDocs --out-dir $Stage5ADOut --allow-warnings
    & $Python -m libreprimus.cli bounded-p56-cuda-parity build-device-subset-audit `
        --device-subset-audit-out $Stage5ADAudit --out-dir $Stage5ADOut --allow-warnings
    & $Python -m libreprimus.cli bounded-p56-cuda-parity build-next-stage-decision `
        --cuda-parity $Stage5ADParity --next-stage-decision-out $Stage5ADDecision --out-dir $Stage5ADOut --allow-warnings
    & $Python -m libreprimus.cli bounded-p56-cuda-parity build-summary `
        --cuda-run $Stage5ADRun `
        --cuda-parity $Stage5ADParity `
        --result-store-preflight $Stage5ADResult `
        --score-summary-preflight $Stage5ADScore `
        --full-p56-blocker $Stage5ADFull `
        --scored-experiment-deferral $Stage5ADScored `
        --doc-staleness-validation $Stage5ADDocs `
        --device-subset-audit $Stage5ADAudit `
        --next-stage-decision $Stage5ADDecision `
        --summary-out $Stage5ADSummary `
        --out-dir $Stage5ADOut `
        --allow-warnings
    & $Python -m libreprimus.cli bounded-p56-cuda-parity validate-stage5ad `
        --cuda-run $Stage5ADRun `
        --cuda-parity $Stage5ADParity `
        --result-store-preflight $Stage5ADResult `
        --score-summary-preflight $Stage5ADScore `
        --full-p56-blocker $Stage5ADFull `
        --scored-experiment-deferral $Stage5ADScored `
        --doc-staleness-validation $Stage5ADDocs `
        --device-subset-audit $Stage5ADAudit `
        --next-stage-decision $Stage5ADDecision `
        --summary $Stage5ADSummary `
        --results-dir $Stage5ADOut

    Write-Host "Running Stage 5AD-fix bounded p56 mismatch temp output"
    $Stage5ADFixOut = Join-Path $TempDir "stage5ad-fix-bounded-p56-mismatch"
    $Stage5ADFixHash = Join-Path $TempDir "stage5ad-fix-bounded-p56-mismatch-hash-lineage.yaml"
    $Stage5ADFixToken = Join-Path $TempDir "stage5ad-fix-bounded-p56-mismatch-token-trace.yaml"
    $Stage5ADFixStream = Join-Path $TempDir "stage5ad-fix-bounded-p56-mismatch-stream-trace.yaml"
    $Stage5ADFixFormula = Join-Path $TempDir "stage5ad-fix-bounded-p56-mismatch-formula-trace.yaml"
    $Stage5ADFixMaterial = Join-Path $TempDir "stage5ad-fix-bounded-p56-mismatch-hash-material.yaml"
    $Stage5ADFixContract = Join-Path $TempDir "stage5ad-fix-bounded-p56-mismatch-reference-contract.yaml"
    $Stage5ADFixRoot = Join-Path $TempDir "stage5ad-fix-bounded-p56-mismatch-root-cause.yaml"
    $Stage5ADFixRepair = Join-Path $TempDir "stage5ad-fix-bounded-p56-mismatch-repair-readiness.yaml"
    $Stage5ADFixGuardrail = Join-Path $TempDir "stage5ad-fix-bounded-p56-mismatch-guardrail.yaml"
    $Stage5ADFixDecision = Join-Path $TempDir "stage5ad-fix-bounded-p56-mismatch-next-stage-decision.yaml"
    $Stage5ADFixSummary = Join-Path $TempDir "stage5ad-fix-bounded-p56-mismatch-summary.yaml"
    & $Python -m libreprimus.cli bounded-p56-mismatch build-hash-lineage `
        --hash-lineage-out $Stage5ADFixHash --out-dir $Stage5ADFixOut --allow-warnings
    & $Python -m libreprimus.cli bounded-p56-mismatch build-token-trace `
        --token-trace-out $Stage5ADFixToken --out-dir $Stage5ADFixOut --allow-warnings
    & $Python -m libreprimus.cli bounded-p56-mismatch build-stream-trace `
        --stream-trace-out $Stage5ADFixStream --out-dir $Stage5ADFixOut --allow-warnings
    & $Python -m libreprimus.cli bounded-p56-mismatch build-formula-trace `
        --formula-trace-out $Stage5ADFixFormula --out-dir $Stage5ADFixOut --allow-warnings
    & $Python -m libreprimus.cli bounded-p56-mismatch build-hash-material-trace `
        --hash-material-out $Stage5ADFixMaterial --out-dir $Stage5ADFixOut --allow-warnings
    & $Python -m libreprimus.cli bounded-p56-mismatch build-reference-contract `
        --reference-contract-out $Stage5ADFixContract --out-dir $Stage5ADFixOut --allow-warnings
    & $Python -m libreprimus.cli bounded-p56-mismatch build-root-cause `
        --root-cause-out $Stage5ADFixRoot --out-dir $Stage5ADFixOut --allow-warnings
    & $Python -m libreprimus.cli bounded-p56-mismatch build-repair-readiness `
        --repair-readiness-out $Stage5ADFixRepair --out-dir $Stage5ADFixOut --allow-warnings
    & $Python -m libreprimus.cli bounded-p56-mismatch build-guardrails `
        --guardrail-out $Stage5ADFixGuardrail --out-dir $Stage5ADFixOut --allow-warnings
    & $Python -m libreprimus.cli bounded-p56-mismatch build-next-stage-decision `
        --next-stage-decision-out $Stage5ADFixDecision --out-dir $Stage5ADFixOut --allow-warnings
    & $Python -m libreprimus.cli bounded-p56-mismatch build-summary `
        --hash-lineage $Stage5ADFixHash `
        --token-trace $Stage5ADFixToken `
        --stream-trace $Stage5ADFixStream `
        --formula-trace $Stage5ADFixFormula `
        --hash-material $Stage5ADFixMaterial `
        --reference-contract $Stage5ADFixContract `
        --root-cause $Stage5ADFixRoot `
        --repair-readiness $Stage5ADFixRepair `
        --guardrail $Stage5ADFixGuardrail `
        --next-stage-decision $Stage5ADFixDecision `
        --summary-out $Stage5ADFixSummary `
        --out-dir $Stage5ADFixOut `
        --allow-warnings
    & $Python -m libreprimus.cli bounded-p56-mismatch validate-stage5ad-fix `
        --hash-lineage $Stage5ADFixHash `
        --token-trace $Stage5ADFixToken `
        --stream-trace $Stage5ADFixStream `
        --formula-trace $Stage5ADFixFormula `
        --hash-material $Stage5ADFixMaterial `
        --reference-contract $Stage5ADFixContract `
        --root-cause $Stage5ADFixRoot `
        --repair-readiness $Stage5ADFixRepair `
        --guardrail $Stage5ADFixGuardrail `
        --next-stage-decision $Stage5ADFixDecision `
        --summary $Stage5ADFixSummary `
        --results-dir $Stage5ADFixOut

    Write-Host "Running Stage 5AE corrected bounded p56 reporting temp output"
    $Stage5AEOut = Join-Path $TempDir "stage5ae-corrected-bounded-p56-reporting"
    $Stage5AEFormula = Join-Path $TempDir "stage5ae-corrected-bounded-p56-formula-parity-report.yaml"
    $Stage5AEContract = Join-Path $TempDir "stage5ae-bounded-p56-reference-contract-repair.yaml"
    $Stage5AEPolicy = Join-Path $TempDir "stage5ae-hash-material-policy.yaml"
    $Stage5AEResult = Join-Path $TempDir "stage5ae-corrected-bounded-p56-result-store-integration.yaml"
    $Stage5AEScore = Join-Path $TempDir "stage5ae-corrected-bounded-p56-score-summary-integration.yaml"
    $Stage5AEMethod = Join-Path $TempDir "stage5ae-corrected-bounded-p56-method-status-impact.yaml"
    $Stage5AEBody = Join-Path $TempDir "stage5ae-corrected-bounded-p56-generated-body-policy.yaml"
    $Stage5AEFull = Join-Path $TempDir "stage5ae-corrected-bounded-p56-full-p56-blocker.yaml"
    $Stage5AEScored = Join-Path $TempDir "stage5ae-corrected-bounded-p56-scored-experiment-deferral.yaml"
    $Stage5AEArchive = Join-Path $TempDir "stage5ae-archive-source-lock-deferral.yaml"
    $Stage5AEDocs = Join-Path $TempDir "stage5ae-corrected-bounded-p56-doc-staleness-validation.yaml"
    $Stage5AEDecision = Join-Path $TempDir "stage5ae-corrected-bounded-p56-next-stage-decision.yaml"
    $Stage5AESummary = Join-Path $TempDir "stage5ae-corrected-bounded-p56-reporting-summary.yaml"
    & $Python -m libreprimus.cli corrected-bounded-p56-reporting build-formula-parity-report `
        --stage5ad-fix-summary $Stage5ADFixSummary --formula-parity-report-out $Stage5AEFormula --out-dir $Stage5AEOut --allow-warnings
    & $Python -m libreprimus.cli corrected-bounded-p56-reporting build-reference-contract-repair `
        --reference-contract-repair-out $Stage5AEContract --out-dir $Stage5AEOut --allow-warnings
    & $Python -m libreprimus.cli corrected-bounded-p56-reporting build-hash-material-policy `
        --hash-material-policy-out $Stage5AEPolicy --out-dir $Stage5AEOut --allow-warnings
    & $Python -m libreprimus.cli corrected-bounded-p56-reporting build-result-store-integration `
        --result-store-integration-out $Stage5AEResult --out-dir $Stage5AEOut --allow-warnings
    & $Python -m libreprimus.cli corrected-bounded-p56-reporting build-score-summary-integration `
        --score-summary-integration-out $Stage5AEScore --out-dir $Stage5AEOut --allow-warnings
    & $Python -m libreprimus.cli corrected-bounded-p56-reporting build-method-status-impact `
        --method-status-impact-out $Stage5AEMethod --out-dir $Stage5AEOut --allow-warnings
    & $Python -m libreprimus.cli corrected-bounded-p56-reporting build-generated-body-policy `
        --generated-body-policy-out $Stage5AEBody --out-dir $Stage5AEOut --allow-warnings
    & $Python -m libreprimus.cli corrected-bounded-p56-reporting build-full-p56-blocker `
        --full-p56-blocker-out $Stage5AEFull --out-dir $Stage5AEOut --allow-warnings
    & $Python -m libreprimus.cli corrected-bounded-p56-reporting build-scored-experiment-deferral `
        --scored-experiment-deferral-out $Stage5AEScored --out-dir $Stage5AEOut --allow-warnings
    & $Python -m libreprimus.cli corrected-bounded-p56-reporting build-archive-source-lock-deferral `
        --archive-source-lock-deferral-out $Stage5AEArchive --out-dir $Stage5AEOut --allow-warnings
    & $Python -m libreprimus.cli corrected-bounded-p56-reporting build-doc-staleness-validation `
        --doc-staleness-validation-out $Stage5AEDocs --out-dir $Stage5AEOut --allow-warnings
    & $Python -m libreprimus.cli corrected-bounded-p56-reporting build-next-stage-decision `
        --next-stage-decision-out $Stage5AEDecision --out-dir $Stage5AEOut --allow-warnings
    & $Python -m libreprimus.cli corrected-bounded-p56-reporting build-summary `
        --formula-parity-report $Stage5AEFormula `
        --reference-contract-repair $Stage5AEContract `
        --hash-material-policy $Stage5AEPolicy `
        --result-store-integration $Stage5AEResult `
        --score-summary-integration $Stage5AEScore `
        --method-status-impact $Stage5AEMethod `
        --generated-body-policy $Stage5AEBody `
        --full-p56-blocker $Stage5AEFull `
        --scored-experiment-deferral $Stage5AEScored `
        --archive-source-lock-deferral $Stage5AEArchive `
        --doc-staleness-validation $Stage5AEDocs `
        --next-stage-decision $Stage5AEDecision `
        --summary-out $Stage5AESummary `
        --out-dir $Stage5AEOut `
        --allow-warnings
    & $Python -m libreprimus.cli corrected-bounded-p56-reporting validate-stage5ae `
        --formula-parity-report $Stage5AEFormula `
        --reference-contract-repair $Stage5AEContract `
        --hash-material-policy $Stage5AEPolicy `
        --result-store-integration $Stage5AEResult `
        --score-summary-integration $Stage5AEScore `
        --method-status-impact $Stage5AEMethod `
        --generated-body-policy $Stage5AEBody `
        --full-p56-blocker $Stage5AEFull `
        --scored-experiment-deferral $Stage5AEScored `
        --archive-source-lock-deferral $Stage5AEArchive `
        --doc-staleness-validation $Stage5AEDocs `
        --next-stage-decision $Stage5AEDecision `
        --summary $Stage5AESummary `
        --results-dir $Stage5AEOut

    Write-Host "Running Stage 5AF source harvester temp output"
    $Stage5AFOut = Join-Path $TempDir "stage5af-source-harvester"
    $Stage5AFPlan = Join-Path $Stage5AFOut "harvest_plan.json"
    $Stage5AFDryRun = Join-Path $TempDir "stage5af-harvest-dry-run-summary.yaml"
    $Stage5AFDecision = Join-Path $TempDir "stage5af-source-harvester-next-stage-decision.yaml"
    $Stage5AFSummary = Join-Path $TempDir "stage5af-source-harvester-summary.yaml"
    & $Python -m libreprimus.cli source-harvester validate-manifest `
        --manifest data/source-harvester/stage5af-cicada-source-manifest.yaml `
        --out-dir $Stage5AFOut
    & $Python -m libreprimus.cli source-harvester plan `
        --manifest data/source-harvester/stage5af-cicada-source-manifest.yaml `
        --out $Stage5AFPlan `
        --dry-run-summary-out $Stage5AFDryRun `
        --out-dir $Stage5AFOut
    & $Python -m libreprimus.cli source-harvester build-bundles `
        --bundle-plan data/source-harvester/stage5af-research-bundle-plan.yaml `
        --out-root (Join-Path $Stage5AFOut "research_bundles_preview")
    & $Python -m libreprimus.cli source-harvester summarize `
        --manifest data/source-harvester/stage5af-cicada-source-manifest.yaml `
        --collection-priorities data/source-harvester/stage5af-source-collection-priorities.yaml `
        --clue-target-categories data/source-harvester/stage5af-clue-target-categories.yaml `
        --bundle-plan data/source-harvester/stage5af-research-bundle-plan.yaml `
        --tool-policy data/source-harvester/stage5af-harvest-tool-policy.yaml `
        --dry-run-summary $Stage5AFDryRun `
        --next-stage-decision-out $Stage5AFDecision `
        --summary-out $Stage5AFSummary `
        --out (Join-Path $Stage5AFOut "summary.json")
    & $Python -m libreprimus.cli source-harvester validate-stage5af `
        --source-manifest data/source-harvester/stage5af-cicada-source-manifest.yaml `
        --collection-priorities data/source-harvester/stage5af-source-collection-priorities.yaml `
        --clue-target-categories data/source-harvester/stage5af-clue-target-categories.yaml `
        --research-bundle-plan data/source-harvester/stage5af-research-bundle-plan.yaml `
        --tool-policy data/source-harvester/stage5af-harvest-tool-policy.yaml `
        --dry-run-summary $Stage5AFDryRun `
        --next-stage-decision $Stage5AFDecision `
        --summary $Stage5AFSummary `
        --results-dir $Stage5AFOut

    Write-Host "Running Stage 5AG local source inventory temp output"
    $Stage5AGOut = Join-Path $TempDir "stage5ag-source-harvester-local"
    $Stage5AGRoot = Join-Path "third_party" "__stage5ag_ci_missing__"
    $Stage5AGRootInventory = Join-Path $TempDir "stage5ag-local-source-root-inventory.yaml"
    $Stage5AGFileSummary = Join-Path $TempDir "stage5ag-local-source-file-inventory-summary.yaml"
    $Stage5AGArchiveSummary = Join-Path $TempDir "stage5ag-local-archive-inventory-summary.yaml"
    $Stage5AGHashSummary = Join-Path $TempDir "stage5ag-local-source-hash-inventory-summary.yaml"
    $Stage5AGLinkage = Join-Path $TempDir "stage5ag-manifest-local-linkage.yaml"
    $Stage5AGExtension = Join-Path $TempDir "stage5ag-local-source-manifest-extension.yaml"
    $Stage5AGCandidate = Join-Path $TempDir "stage5ag-source-lock-candidate-summary.yaml"
    $Stage5AGGap = Join-Path $TempDir "stage5ag-local-source-gap-report.yaml"
    $Stage5AGBundle = Join-Path $TempDir "stage5ag-research-bundle-readiness.yaml"
    $Stage5AGGuardrail = Join-Path $TempDir "stage5ag-local-source-guardrail.yaml"
    $Stage5AGDecision = Join-Path $TempDir "stage5ag-source-harvester-next-stage-decision.yaml"
    $Stage5AGSummary = Join-Path $TempDir "stage5ag-source-harvester-summary.yaml"
    & $Python -m libreprimus.cli source-harvester inventory-local-sources `
        --manifest data/source-harvester/stage5af-cicada-source-manifest.yaml `
        --source-root $Stage5AGRoot `
        --results-dir $Stage5AGOut `
        --out-root-inventory $Stage5AGRootInventory `
        --out-file-summary $Stage5AGFileSummary `
        --out-archive-summary $Stage5AGArchiveSummary `
        --out-hash-summary $Stage5AGHashSummary
    & $Python -m libreprimus.cli source-harvester link-local-sources `
        --manifest data/source-harvester/stage5af-cicada-source-manifest.yaml `
        --source-root $Stage5AGRoot `
        --results-dir $Stage5AGOut `
        --out $Stage5AGLinkage `
        --out-extension $Stage5AGExtension
    & $Python -m libreprimus.cli source-harvester build-source-lock-candidates `
        --manifest data/source-harvester/stage5af-cicada-source-manifest.yaml `
        --local-linkage $Stage5AGLinkage `
        --out $Stage5AGCandidate `
        --gap-report $Stage5AGGap
    & $Python -m libreprimus.cli source-harvester build-bundle-readiness `
        --bundle-plan data/source-harvester/stage5af-research-bundle-plan.yaml `
        --local-linkage $Stage5AGLinkage `
        --out $Stage5AGBundle `
        --results-dir $Stage5AGOut
    & $Python -m libreprimus.cli source-harvester build-stage5ag-guardrail `
        --source-root $Stage5AGRoot `
        --results-dir $Stage5AGOut `
        --out $Stage5AGGuardrail
    & $Python -m libreprimus.cli source-harvester build-stage5ag-next-stage-decision `
        --root-inventory $Stage5AGRootInventory `
        --local-linkage $Stage5AGLinkage `
        --bundle-readiness $Stage5AGBundle `
        --out $Stage5AGDecision
    & $Python -m libreprimus.cli source-harvester build-stage5ag-summary `
        --root-inventory $Stage5AGRootInventory `
        --file-summary $Stage5AGFileSummary `
        --archive-summary $Stage5AGArchiveSummary `
        --hash-summary $Stage5AGHashSummary `
        --local-linkage $Stage5AGLinkage `
        --candidate-summary $Stage5AGCandidate `
        --gap-report $Stage5AGGap `
        --bundle-readiness $Stage5AGBundle `
        --guardrail $Stage5AGGuardrail `
        --next-stage-decision $Stage5AGDecision `
        --out $Stage5AGSummary `
        --results-dir $Stage5AGOut
    & $Python -m libreprimus.cli source-harvester validate-stage5ag `
        --root-inventory $Stage5AGRootInventory `
        --file-summary $Stage5AGFileSummary `
        --archive-summary $Stage5AGArchiveSummary `
        --hash-summary $Stage5AGHashSummary `
        --local-linkage $Stage5AGLinkage `
        --candidate-summary $Stage5AGCandidate `
        --gap-report $Stage5AGGap `
        --bundle-readiness $Stage5AGBundle `
        --guardrail $Stage5AGGuardrail `
        --next-stage-decision $Stage5AGDecision `
        --summary $Stage5AGSummary `
        --results-dir $Stage5AGOut

    if (Test-Path "research-inputs\stage5ai\master_manifest.yaml") {
        Write-Host "Validating Stage 5AI curated research bundle records"
        & $Python -m libreprimus.cli source-harvester validate-stage5ai
    } else {
        Write-Host "Skipping Stage 5AI generated bundle validation; ignored local bundle bodies are absent"
    }
    $Stage5AIBundleManifest = "research-inputs/stage5ai/master_manifest.yaml"
    $Stage5AIGeneratedReport = Join-Path (Join-Path (Join-Path "experiments" "results") "research-bundles") "stage5ai\summary.json"
    git check-ignore -q $Stage5AIBundleManifest
    git check-ignore -q $Stage5AIGeneratedReport

    $Stage5AJSummaryReport = Join-Path (Join-Path (Join-Path "experiments" "results") "source-harvester-usefulfiles") "stage5aj\summary.json"
    if (Test-Path $Stage5AJSummaryReport) {
        Write-Host "Validating Stage 5AJ UsefulFilesAndIdeas records"
        & $Python -m libreprimus.cli source-harvester validate-stage5aj
    } else {
        Write-Host "Skipping Stage 5AJ generated UsefulFiles validation; ignored local reports are absent"
    }
    $Stage5AJBundleManifest = "research-inputs/stage5aj/master_manifest.yaml"
    $Stage5AJCellIndex = Join-Path (Join-Path (Join-Path "experiments" "results") "source-harvester-usefulfiles") "stage5aj\xlsx_cell_metadata_index.jsonl"
    $Stage5AJImportantLinks = Join-Path (Join-Path (Join-Path "experiments" "results") "source-harvester-usefulfiles") "stage5aj\important_links_url_index.json"
    $Stage5AJRawWorkbook = "third_party/UsefulFilesAndIdeas/LP Excel.xlsx"
    git check-ignore -q $Stage5AJBundleManifest
    git check-ignore -q $Stage5AJCellIndex
    git check-ignore -q $Stage5AJImportantLinks
    git check-ignore -q $Stage5AJRawWorkbook

    $Stage5AKGeneratedDir = Join-Path (Join-Path (Join-Path "experiments" "results") "source-harvester-community-facts") "stage5ak"
    $Stage5AKSummaryReport = Join-Path $Stage5AKGeneratedDir "summary.json"
    if (Test-Path $Stage5AKSummaryReport) {
        Write-Host "Validating Stage 5AK community-facts records"
        & $Python -m libreprimus.cli source-harvester validate-stage5ak `
            --inventory data/source-harvester/stage5ak-community-facts-local-inventory.yaml `
            --attachment-index data/source-harvester/stage5ak-community-facts-attachment-index.yaml `
            --source-card-summary data/source-harvester/stage5ak-community-facts-source-card-summary.yaml `
            --content-index-summary data/source-harvester/stage5ak-community-facts-content-index-summary.yaml `
            --clue-categories data/source-harvester/stage5ak-community-facts-clue-categories.yaml `
            --claim-policy data/source-harvester/stage5ak-community-claim-policy.yaml `
            --claim-records data/source-harvester/stage5ak-community-facts-claim-records.yaml `
            --correction-log data/source-harvester/stage5ak-community-facts-correction-log.yaml `
            --arithmetic-preflight data/source-harvester/stage5ak-community-facts-arithmetic-preflight.yaml `
            --website-update data/source-harvester/stage5ak-website-ingest-update-summary.yaml `
            --deep-research-update data/source-harvester/stage5ak-deep-research-pack-update-summary.yaml `
            --readiness data/source-harvester/stage5ak-research-bundle-readiness.yaml `
            --missing-source-plan data/source-harvester/stage5ak-missing-source-plan-update.yaml `
            --guardrail data/source-harvester/stage5ak-guardrail.yaml `
            --next-stage-decision data/source-harvester/stage5ak-next-stage-decision.yaml `
            --summary data/source-harvester/stage5ak-summary.yaml `
            --results-dir $Stage5AKGeneratedDir
    } else {
        Write-Host "Skipping Stage 5AK generated community-facts validation; ignored local reports are absent"
    }
    $Stage5AKRawText = "third_party/UsefulFilesAndIdeas/community-facts/community-facts-collection.txt"
    $Stage5AKRawImage = "third_party/UsefulFilesAndIdeas/community-facts/1.webp"
    $Stage5AKGeneratedClaims = Join-Path (Join-Path (Join-Path "experiments" "results") "source-harvester-community-facts") "stage5ak\community_claim_records.jsonl"
    $Stage5AKBundleClaims = "research-inputs/stage5ak/community_claim_records.jsonl"
    $Stage5AKHandoff = "codex-output/stage5ak-codex-completion.md"
    git check-ignore -q $Stage5AKRawText
    git check-ignore -q $Stage5AKRawImage
    git check-ignore -q $Stage5AKGeneratedClaims
    git check-ignore -q $Stage5AKBundleClaims
    git check-ignore -q $Stage5AKHandoff

    Write-Host "Running result-store consistency suite"
    & $Python -m libreprimus.cli consistency check-result-store --allow-missing-generated --allow-warnings

    Write-Host "Exporting consistency summary to temp"
    & $Python -m libreprimus.cli consistency check-all --out (Join-Path $TempDir "consistency_summary.json") --allow-warnings

    Write-Host "Validating Stage 3K archive and observation registries"
    & $Python -m libreprimus.cli archive validate-sources --records data/observations/archive/source-archive-records-v0.yaml
    & $Python -m libreprimus.cli archive validate-image-locks --locks data/locks/third-party/liber-primus-pages/liber-primus-page-image-locks-v0.jsonl --artifacts data/observations/visual/liber-primus-page-image-artifacts-v0.jsonl --allow-empty
    & $Python -m libreprimus.cli observation validate-visual --records data/observations/visual/visual-numeric-observations-v0.yaml
    & $Python -m libreprimus.cli observation validate-cookies --records data/observations/web/cookie-hash-records-v0.yaml

    Write-Host "Validating Stage 3L hash preimage candidate packs"
    & $Python -m libreprimus.cli hash-preimage validate-packs --pack-dir data/observations/web/hash-preimage-candidate-packs

    Write-Host "Validating Stage 3M deterministic image-analysis raw-data-free mode"
    & $Python -m libreprimus.cli image-analysis validate-results --results-dir (Join-Path $TempDir "stage3m-image-analysis") --allow-missing

    Write-Host "Validating Stage 3P deterministic image-transform raw-data-free mode"
    & $Python -m libreprimus.cli image-transform validate-results --results-dir (Join-Path $TempDir "stage3p-image-transforms") --allow-missing

    Write-Host "Validating Stage 3N Discord ingestion raw-log-free mode"
    & $Python -m libreprimus.cli discord-ingest scan --source-dir (Join-Path $TempDir "missing-discord") --out-dir (Join-Path $TempDir "stage3n-discord") --allow-missing --allow-warnings
    & $Python -m libreprimus.cli discord-ingest validate-results --results-dir (Join-Path $TempDir "stage3n-discord") --allow-missing

    Write-Host "Validating Stage 3O Discord promotion and Wiki mirror"
    & $Python -m libreprimus.cli discord-promote validate-promoted --links data/observations/discord/promoted-public-source-links-stage3o.yaml --methods data/observations/discord/promoted-method-claim-candidates-stage3o.yaml --numerics data/observations/discord/promoted-numeric-observation-candidates-stage3o.yaml --allow-empty
    & .\scripts\github\validate-wiki-source.ps1

    Write-Host "Validating Stage 3Q Discord review-bundle raw-log-free mode"
    $Stage3QOut = Join-Path $TempDir "stage3q-discord-review"
    $Stage3QAggregate = Join-Path $TempDir "stage3q-discord-review-aggregate.yaml"
    & $Python -m libreprimus.cli discord-review build-bundles --ingestion-dir (Join-Path $TempDir "missing-stage3n") --promotion-dir (Join-Path $TempDir "missing-stage3o") --raw-dir (Join-Path $TempDir "missing-discord") --out-dir $Stage3QOut --aggregate-out $Stage3QAggregate --allow-missing --allow-warnings
    & $Python -m libreprimus.cli discord-review validate-bundles --results-dir $Stage3QOut --aggregate $Stage3QAggregate --allow-missing

    Write-Host "Validating Stage 4A Discord full-review synthetic build"
    $Stage4ADiscord = Join-Path $TempDir "stage4a-discord"
    $Stage4APages = Join-Path $TempDir "stage4a-pages"
    $Stage4AOut = Join-Path $TempDir "stage4a-full-review"
    New-Item -ItemType Directory -Path $Stage4ADiscord, $Stage4APages | Out-Null
    @"
from pathlib import Path
from PIL import Image
discord = Path(r"$Stage4ADiscord")
pages = Path(r"$Stage4APages")
(discord / "CicadaSolvers - Cicada - ci-test [123456789012345678].html").write_text(
    '<div class="chatlog__message"><span class="chatlog__author-name">User</span>'
    '<div class="chatlog__content">cuneiform base60 onion 7 https://example.org/source '
    'https://cdn.discordapp.com/attachments/1/2/test.png?secret=1</div></div>',
    encoding="utf-8",
)
Image.new("RGB", (32, 32), "white").save(pages / "page001.jpg")
"@ | & $Python -
    & $Python -m libreprimus.cli discord-full-review build --discord-dir $Stage4ADiscord --lp-pages-dir $Stage4APages --out-dir $Stage4AOut --privacy-mode redacted_public --include-lp-page-gallery --allow-warnings
    & $Python -m libreprimus.cli discord-full-review validate --results-dir $Stage4AOut

    Write-Host "Validating Stage 3R Discord lead promotion records and disabled manifests"
    & $Python -m libreprimus.cli discord-leads validate --promoted-sources data/observations/discord/stage3r-promoted-source-records.yaml --promoted-observations data/observations/discord/stage3r-promoted-observation-records.yaml --negative-controls data/observations/discord/stage3r-negative-control-records.yaml --manifest-dir experiments/manifests/post-discord --allow-empty

    Write-Host "Validating Stage 3S post-Discord Onion 7 manifest"
    & $Python -m libreprimus.cli post-discord validate-manifest --manifest experiments/manifests/post-discord/EXP-3R-003-onion7-raw-prime-order-seed-pack-a.yaml

    Write-Host "Validating Stage 3T GP/rune claim verifier manifest"
    & $Python -m libreprimus.cli post-discord validate-gp-rune-manifest --manifest experiments/manifests/post-discord/EXP-3R-004-gp-rune-claim-verifier-a.yaml

    Write-Host "Validating Stage 3U cookie signed-variant manifest"
    & $Python -m libreprimus.cli post-discord validate-cookie-manifest --manifest experiments/manifests/post-discord/EXP-3R-001-cookie-sha256-signed-variants-a.yaml

    Write-Host "Validating Stage 3V OutGuess regression manifest and missing-tool-safe detection"
    & $Python -m libreprimus.cli stego outguess-validate-manifest --manifest experiments/manifests/stego/outguess-regression-v1.yaml --artifacts data/observations/stego/outguess-artifacts-v0.yaml
    & $Python -m libreprimus.cli stego outguess-detect --out-dir (Join-Path $TempDir "stage3v-outguess") --allow-missing-tool

    Write-Host "Validating Stage 2E exploratory manifests"
    & $Python -m libreprimus.cli experiment validate-exploratory --manifest experiments/manifests/exploratory/stage2e-caesar-preview-dry-run.yaml
    & $Python -m libreprimus.cli experiment validate-exploratory --manifest experiments/manifests/exploratory/stage2e-affine-preview-dry-run.yaml

    Write-Host "Dry-running Stage 2E Caesar preview to temp"
    & $Python -m libreprimus.cli experiment dry-run --manifest experiments/manifests/exploratory/stage2e-caesar-preview-dry-run.yaml --out-dir (Join-Path $TempDir "stage2e-dry-run") --allow-warnings

    Write-Host "Validating Stage 2F CPU execution manifests"
    & $Python -m libreprimus.cli execution validate --manifest experiments/manifests/cpu-execution/stage2f-synthetic-direct-execution.yaml
    & $Python -m libreprimus.cli execution validate --manifest experiments/manifests/cpu-execution/stage2f-solved-baseline-replay.yaml

    Write-Host "Running Stage 2F synthetic direct execution"
    & $Python -m libreprimus.cli execution run --manifest experiments/manifests/cpu-execution/stage2f-synthetic-direct-execution.yaml --out-dir experiments/results/cpu-execution/stage2f --allow-warnings

    Write-Host "Validating Stage 2G proposals and approval gates"
    & $Python -m libreprimus.cli proposal validate --proposal experiments/proposals/stage2g/stage2g-caesar-page-candidate-proposal.yaml
    & $Python -m libreprimus.cli proposal check-approval --proposal experiments/proposals/stage2g/stage2g-caesar-page-candidate-proposal.yaml --approval experiments/proposals/stage2g/approval-records/stage2g-example-pending-approval.yaml

    Write-Host "Generating Stage 2G review packet to temp"
    & $Python -m libreprimus.cli proposal review-packet --proposal experiments/proposals/stage2g/stage2g-caesar-page-candidate-proposal.yaml --out-dir (Join-Path $TempDir "stage2g-review") --allow-warnings

    Write-Host "Validating Stage 2H approval-gated requests"
    & $Python -m libreprimus.cli approval-execution validate --request experiments/proposals/stage2h/stage2h-approved-synthetic-direct-request.yaml
    & $Python -m libreprimus.cli approval-execution validate --request experiments/proposals/stage2h/stage2h-noop-real-request.yaml

    Write-Host "Running Stage 2H approved synthetic request to temp"
    & $Python -m libreprimus.cli approval-execution run --request experiments/proposals/stage2h/stage2h-approved-synthetic-direct-request.yaml --out-dir (Join-Path $TempDir "stage2h-approval-execution") --allow-warnings

    Write-Host "Validating Stage 2I approval-readiness proposal"
    & $Python -m libreprimus.cli approval-readiness validate --proposal experiments/proposals/stage2i/stage2i-first-bounded-caesar-affine-review.yaml --approval experiments/proposals/stage2i/approval-records/stage2i-first-bounded-caesar-affine-pending-approval.yaml

    Write-Host "Generating Stage 2I readiness packet to temp"
    & $Python -m libreprimus.cli approval-readiness packet --proposal experiments/proposals/stage2i/stage2i-first-bounded-caesar-affine-review.yaml --approval experiments/proposals/stage2i/approval-records/stage2i-first-bounded-caesar-affine-pending-approval.yaml --out-dir (Join-Path $TempDir "stage2i-readiness") --allow-warnings

    Write-Host "Validating Stage 2J bounded operator policy and queue"
    & $Python -m libreprimus.cli bounded-experiment validate-policy --policy experiments/policies/operator-policy-v0.yaml
    & $Python -m libreprimus.cli bounded-experiment validate-queue --queue experiments/queues/stage2j-bounded-cpu-queue.yaml
    & $Python -m libreprimus.cli bounded-experiment check-queue --policy experiments/policies/operator-policy-v0.yaml --queue experiments/queues/stage2j-bounded-cpu-queue.yaml

    Write-Host "Running Stage 2J bounded queue to temp"
    & $Python -m libreprimus.cli bounded-experiment run-all --policy experiments/policies/operator-policy-v0.yaml --queue experiments/queues/stage2j-bounded-cpu-queue.yaml --out-dir (Join-Path $TempDir "stage2j-bounded") --allow-warnings
} finally {
    if (Test-Path $TempDir) {
        Remove-Item -LiteralPath $TempDir -Recurse -Force
    }
}
