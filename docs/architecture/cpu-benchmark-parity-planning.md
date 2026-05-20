# CPU Benchmark Parity Planning

Stage 4Q records the benchmark and parity-planning surface that future CUDA work must cite before it can start. It does not implement CUDA, run GPU benchmarks, make speedup claims, execute broad experiments, activate the canonical corpus, finalise page boundaries, or make solve claims.

The committed records are:

- `data/benchmarks/stage4q-cpu-benchmark-plan.yaml`
- `data/benchmarks/stage4q-cuda-parity-readiness.yaml`
- `data/research/stage4q-cpu-benchmark-parity-planning-summary.yaml`

Generated diagnostics remain ignored under `experiments/results/benchmarks/stage4q/`.

The Stage 4Q plan is intentionally conservative. It links Stage 4O CPU parity expectations and Stage 4P unified result surfaces to future parity gates, records blocked transform families explicitly, and keeps non-transform targets such as cookie, stego/audio, image, compression, and bigram work outside CUDA parity scope.

CPU smoke timings are diagnostic plumbing only. They are not performance measurements and must not be reported as evidence of speed or scalability.

Stage 5A uses Stage 4Q readiness records to plan CUDA parity scaffolds. It does not run GPU benchmarks, modify CUDA source, or claim performance.
