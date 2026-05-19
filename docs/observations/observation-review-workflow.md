# Observation Review Workflow

Stage 4J defines the review-to-promotion lifecycle for observation records.
Observations are leads until reviewed; review does not make them canonical and
does not prove plaintext.

The lifecycle is:

1. Create an observation from a committed source, annotation, fixture, or
   negative-control record.
2. Assign a review state.
3. Apply promotion gates.
4. Preserve blocked observations as deferred, rejected, quarantined, or
   negative-control records.
5. Promote only by explicit review decision and manifest policy.

Review-only observations keep `usable_as_experiment_seed=false`. Visual
observations require page/image evidence and coordinates before seed promotion.
Cuneiform and dot observations also require accepted readings and ambiguity
resolution.
