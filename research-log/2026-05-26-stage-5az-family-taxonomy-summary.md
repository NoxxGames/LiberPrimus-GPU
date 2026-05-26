# Stage 5AZ Family Taxonomy Summary

The Stage 5AY design policy intentionally allowed `unresolved_as_current_only` to participate in both baseline-family reasoning and unresolved-policy reasoning. The problem was not the taxonomy overlap; it was the duplicate flat `family_id` records in the bounded variant-family manifest.

Stage 5AZ records this explicitly:

- Duplicate taxonomy memberships are allowed.
- Duplicate family records are not allowed.
- Family count semantics are unique family records.
- Taxonomy membership count semantics are memberships across unique family records.

The repaired manifest now has:

- Unique variant family records: `10`
- Taxonomy memberships: `11`
- Duplicate family IDs after repair: `0`

This is metadata repair only. It does not alter token values, branch semantics, source locks, branch budgets, DWH policy, or execution authorization.
