# Stage 4D Bounded Numeric Verifier Pack

Stage 4D turns the Stage 4B disabled numeric backlog into bounded audit outputs. It runs only the parts that have enough source-backed input and records explicit skip/defer states for everything else.

## Scope

- GP/rune batch002: exact-span verification only; skipped when no exact new claims are present.
- Delimiter handedness: metadata audit only; no reset-boundary or cipher meaning is inferred.
- Dot ambiguity: counts ambiguity and uniqueness only; `13` and `31` remain unforced.
- Number-square routes: fixed no-fudge routes only; skipped until raw values are source-locked.
- Visual negative controls: ambiguity metrics only.
- Cookie pack v2 and cuneiform reading pack v1: deferred.

## No-Fudge Rules

Raw values stay separate from derived values. Every derived value must record a formula and source.

Forbidden in Stage 4D:

- nearest-prime adjustments;
- arbitrary `+/-n` changes;
- post-hoc row or column arithmetic;
- route expansion beyond the manifest;
- fuzzy numeric matching;
- broad number-theory search.

## Generated Outputs

Generated results are written under:

```text
experiments/results/bounded-numeric/stage4d/
```

These files are ignored and must not be committed.

## Local Run

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli bounded-numeric run `
  --manifest-dir experiments/manifests/stage4b-disabled `
  --stage4b-visual data/observations/visual/stage4b-visual-observation-records.yaml `
  --stage4c-tasks data/observations/visual/stage4c-visual-annotation-tasks.yaml `
  --stage4c-cuneiform data/observations/visual/stage4c-cuneiform-reading-candidates.yaml `
  --stage4c-dot data/observations/visual/stage4c-dot-pattern-annotation-tasks.yaml `
  --stage4c-delimiter data/observations/visual/stage4c-delimiter-annotation-tasks.yaml `
  --stage4c-negative data/observations/visual/stage4c-visual-negative-control-annotation-tasks.yaml `
  --out-dir experiments/results/bounded-numeric/stage4d `
  --allow-warnings
```

## Stage 4D Result

The local run discovered `7` manifests, audited `3`, deferred or skipped `4`, verified `0` GP/rune claims because no exact new claims were present, audited `2` delimiter observations, skipped number-square route execution because raw values are pending source-lock, audited `10` visual negative controls, deferred cuneiform seed execution, and deferred cookie pack v2.

No solve claim, CUDA work, canonical corpus activation, or page-boundary finalization was made.
