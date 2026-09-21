# Review and Change Policy

- Status: **Accepted workflow baseline**

## Branching

- `main`: accepted baseline and reviewed increments only.
- implementation: dedicated bounded branch, e.g. `build/slice-01`.
- avoid long-lived speculative branches.

## Increment discipline

Each increment:
1. starts from documented scope.
2. changes only relevant modules.
3. includes tests.
4. receives review.
5. receives corrections.
6. is reverified.
7. records checkpoint.

No next increment before PASS.

## Review categories

Reviewer checks:
- functional correctness.
- invariants.
- permissions/security.
- data integrity.
- migrations.
- module boundaries.
- maintainability.
- unnecessary abstraction.
- UX dead ends.
- documentation drift.

## Blocking findings

Examples:
- invariant violation.
- privilege escalation.
- history rewrite.
- data-loss risk.
- migration inconsistency.
- incorrect snapshot semantics.
- architecture boundary violation causing systemic coupling.
- failure of required test path.

Blocking findings require correction before progression.

## Non-blocking findings

May be deferred only when:
- explicitly documented.
- does not violate current acceptance.
- has clear rationale/target milestone.

## Documentation change rule

If implementation introduces an accepted design decision:
- update the relevant canonical document.
- add/update ADR if architectural.
- update traceability/risk/state where materially affected.

Do not hide policy changes only in code comments or commit messages.

## Domain change rule

If code reveals the accepted domain model is wrong:
- STOP implementation.
- document the conflict.
- resolve design first.
- update specs/tests.
- then resume.

## Independent review

Prefer a reviewer distinct from the implementation pass.

If the same AI system reviews:
- start a separate review pass.
- read canonical docs first.
- inspect actual diff/tests.
- do not rely on executor summary as evidence.

## Merge rule

Merge to `main` only after:
- gate PASS.
- required CI green.
- blocking findings resolved.
- checkpoint recorded.
