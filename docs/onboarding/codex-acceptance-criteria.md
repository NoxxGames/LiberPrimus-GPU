# Codex Acceptance Criteria

## Purpose
Future Codex stages must finish with coherent repository state, not just new records. Current mirrors, handoffs, validation evidence, ignored-output policy, and guardrails must agree.

## Edited-document integrity
When a stage edits a current-facing document, review the whole final file. Check that current sections match `data/project-state/current-stage-state.yaml`, avoid repeated generated phrases, and remove stale handoff paths.

## Current-mirror consistency
Current mirrors include README, AGENTS, STATUS, ROADMAP, TESTING, staged plan, onboarding maps, token-block CLI docs, ChatGPT context, current-stage state, and stage-summary records. Latest and next-stage wording must match the state file.

## ChatGPT context quality
The context file must separate current truth from historical summaries. Historical Stage 6C, 6D, 6E, and 6F material should remain durable, but old routing must not masquerade as current routing.

## Source-lock evidence and gap semantics
Source-lock records must cite committed source paths or record explicit gaps. Chat-only observations can be backlog blockers, but they are not source truth or proof.

## Number-fact and arithmetic quality
Arithmetic records need exact input labels, exact integer checks, source paths, and risk notes. Approximate geometry or discussion aliases must be marked as such.

## Probe traceability quality
Every future probe or manifest input row needs source records or an explicit source gap, controls, output archive policy, and disabled execution flags.

## Hook and preflight quality
Hooks must be report-only and exit zero by default. Strict mode must be explicit, tested separately, and never inferred from an inherited environment.

## Doc-staleness quality
Stale-current scanners must not be weakened. Fix legitimate current drift, classify warning-domain findings, and keep historical examples in clearly historical sections.

## Source Browser and overlay quality
Source Browser records and overlays must validate without widening schemas just to force fragile records. Review-only overlays must not become proof, route seeds, or activation decisions.

## CI-safe ignored-file policy
Tests may assert ignored paths are ignored, but clean CI must not require ignored completion summaries, local reports, or ignored third-party roots to exist.

## Completion summary quality
Ignored completion summaries must be written locally with actual final values after the final commit, push, and CI. They must not contain pending placeholders.

## Noncommit policy
Do not stage raw data, generated experiment outputs, `codex-output/**`, ignored reports, databases, archives, binaries, or protected local operator state.

## Bad vs good Codex instruction examples
Bad instruction:
"Update AGENTS.md."

Good instruction:
"Update AGENTS.md as a whole final file, then verify its current section matches current-stage-state.yaml, contains no repeated generated phrases, contains no stale latest/next-stage claims, and contains no stale completion-summary path."

## Final self-review checklist
- Current-stage state and current docs agree.
- ChatGPT context has current/historical boundaries.
- Stale-current strict errors are zero.
- Source Browser validates.
- Hook status is stated without overclaiming actual runner behavior.
- No Stage 7 manifest, archive, probe execution, route stream, byte stream, target selection, or solve claim was created unless explicitly authorized.
