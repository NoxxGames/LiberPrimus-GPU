# Minimal CPU Transform Executor

Stage 3A adds the first bounded CPU executor for a real reviewable corpus-candidate slice. It is deliberately narrow: the executor enumerates Caesar shift mod 29 and affine mod 29 transforms for one queue item that passes the standing operator policy.

The executor reads index-29 token metadata from generated, ignored corpus-candidate records. It does not commit raw corpus text, activate a canonical corpus, finalize page boundaries, use CUDA, or make a solve claim.

## Inputs

- Policy: `experiments/policies/operator-policy-v0.yaml`
- Queue: `experiments/queues/stage2j-bounded-cpu-queue.yaml`
- Queue item: `stage2j-caesar-affine-first-reviewable-slice`
- Generated selector metadata: `data/normalized/corpus-candidates/rtkd-master-v0-candidate/`

The committed queue stores selector metadata only. The actual candidate-token metadata remains generated and ignored.

## Execution

The Stage 3A executor:

- loads a safe `index29` stream from a reviewable page-candidate selector;
- generates 29 Caesar candidates;
- generates 812 affine mod-29 candidates;
- writes 841 candidate records to ignored JSONL;
- applies deterministic minimal triage scoring;
- writes a summary and top-k lead records under `experiments/results/bounded-auto-runs/stage3a/`.

## Safety

Candidate outputs are generated experiment artifacts. They are not source evidence, not canonical corpus material, and not solve evidence. The committed repository records only code, schemas, manifests, docs, tests, and summary-level research notes.
