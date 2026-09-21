# Controlled Implementation Cycle

- Status: **Accepted**
- Owner approval: 2026-09-21

## Principle

Implementation proceeds through repeated controlled loops:

```text
Design-ready increment
      ↓
Controlled implementation
      ↓
Automated verification
      ↓
Architecture/domain review
      ↓
Defect correction
      ↓
Re-verification
      ↓
Next controlled increment
      ↓
...
      ↓
Human acceptance
```

The project must not jump directly from design to a broad implementation followed only by human testing.

## Cycle phases

### 1. PLAN
Define one bounded increment only.

Each increment must have:
- scope.
- affected modules.
- acceptance criteria.
- invariants involved.
- explicitly deferred items.
- expected tests.
- rollback/recovery considerations when data changes.

### 2. IMPLEMENT
The executor changes only what belongs to the increment.

Rules:
- no speculative future features.
- no unrelated refactors.
- no silent domain decisions.
- no weakening of accepted invariants.
- no borrowing from previous experimental repositories.

### 3. VERIFY
Run automated verification appropriate to the increment:

- lint/static checks.
- domain/application tests.
- integration/database tests.
- permission matrix.
- migration checks.
- Django system checks.
- browser tests where relevant.
- PostgreSQL path where database behavior matters.

### 4. REVIEW
A separate review pass evaluates:

- correctness against acceptance criteria.
- Domain invariants.
- authority/security behavior.
- module boundaries.
- data integrity.
- historical integrity.
- maintainability.
- unnecessary abstraction.
- unnecessary coupling.
- UX dead ends visible from implementation.
- migration safety.

Review must not assume that "tests pass" means "design is correct".

### 5. CORRECT
Any defect found by review is fixed before starting the next increment.

Rules:
- defect gets a regression test when automatable.
- architecture/domain defects are fixed at the correct layer, not patched only in UI.
- permission defects are fixed server-side.
- data integrity defects require explicit migration/data handling.

### 6. RE-VERIFY
After correction, rerun the relevant checks.

An increment is not closed until:
- required tests pass.
- review findings are resolved or explicitly deferred with justification.
- documentation reflects any accepted decision.

### 7. CHECKPOINT
Record:
- branch/commit.
- completed scope.
- tests/results.
- unresolved risks.
- next increment.

Only then may the next controlled implementation increment start.

## Human Acceptance Gate

Human review happens only after the machine-controlled implementation/review/correction loops have produced a coherent usable slice.

Before Human Acceptance:
- no known blocking automated-test failure.
- no unresolved critical permission/invariant defect.
- migrations are coherent.
- setup/run instructions work.
- demo/test data path exists.
- the intended browser workflow is complete.

Human Acceptance then evaluates areas automation cannot decide well:
- visual comfort.
- clarity.
- practical workflow.
- terminology.
- discoverability.
- perceived rigidity/freedom.
- real-world usefulness.
- desktop/mobile behavior.

## After Human Acceptance

Human findings enter another controlled loop:

```text
Human finding
  ↓
classify: UX / domain / permission / defect / preference
  ↓
design decision if needed
  ↓
controlled implementation
  ↓
automated verification
  ↓
review
  ↓
correction
  ↓
human re-test when relevant
```

## Rule of progression

**No next increment on top of a known broken foundation.**

A later feature must not be used to hide or compensate for an unresolved defect in an earlier layer.

## Independence of reviewer

Where practical, implementation and review should be separated logically:
- executor builds.
- reviewer/auditor examines diffs, tests and architecture independently.
- corrections return to executor.
- reviewer verifies closure.

The same AI system may perform both roles only if the review is run as a distinct pass from source-of-truth documents rather than trusting its own implementation narrative.
