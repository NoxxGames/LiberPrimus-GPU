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
