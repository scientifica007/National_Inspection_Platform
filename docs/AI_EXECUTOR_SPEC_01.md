# AI Executor Specification — Vertical Slice 01

## Project

**National Inspection Platform**

Repository:
`scientifica007/National_Inspection_Platform`

Implementation branch:
`build/slice-01`

## Mission

Build only the first end-to-end slice:

**Solo Inspector Field Visit**

Do not implement the complete national platform.

## Source of truth order

When implementation questions arise, use this order:

1. `docs/INVARIANTS.md`
2. `docs/PRODUCT_VISION.md`
3. `docs/AUTHORITY_MODEL.md`
4. `docs/LIFECYCLE_SEMANTICS.md`
5. `docs/LIFECYCLE_PROFILES.md`
6. `docs/MINIMAL_STABLE_CORE.md`
7. `docs/VERTICAL_SLICE_01.md`
8. `docs/VERTICAL_SLICE_01_DATA_MODEL.md`
9. `docs/ENGINEERING_CONVENTIONS.md`
10. accepted ADRs

If documents truly conflict, stop and report the contradiction. Do not silently choose a new policy.

## Independence

This is a clean-slate build.

Do not inspect, read, copy, compare, cherry-pick or import code/architecture/migrations/templates/tests/databases from:
- Inspector_Website_001
- Inspector_Website_002
- Inspector_Website_003
- Inspector_Website_004
- Inspector_Website_005

## Stack

Follow ADR-0002:
- Python 3.12
- Django 5.2 LTS
- PostgreSQL canonical
- Django Templates
- CSS Design Tokens / reusable components
- minimal JavaScript
- HTMX only if clearly useful
- pytest + pytest-django
- Ruff
- Playwright for critical browser path when practical
- CI

## Required modules for this slice

Only:
- identity
- institutions
- knowledge
- visits
- records
- audit

Do not create empty future modules as placeholders.

## Required user behavior

### Inspector
Must be able to:
1. authenticate.
2. see a simple personal dashboard.
3. create a local Institution.
4. create a local Checklist and activate a version.
5. create a Draft Visit.
6. select Institution.
7. select an ACTIVE ChecklistVersion.
8. obtain a frozen Visit snapshot.
9. create/edit/delete draft Findings and Recommendations.
10. edit/delete Draft Visit.
11. finalize Visit with an explicit confirmation.
12. view the finalized Visit read-only.

### Admin
Must be able to:
- authenticate.
- manage the minimum account/capability setup required for the slice.
- see Inspector Visits.
- inspect provenance.
- NOT rewrite/delete Inspector finalized Findings/Recommendations.
- NOT impersonate Inspector for professional authorship.

## Required invariants

Server-side enforcement is mandatory:
- actor known.
- identity not borrowed.
- capability/scope checked.
- Draft mutable.
- Finalized immutable.
- active ChecklistVersion immutable.
- Visit snapshot unaffected by later source changes.
- historical dependency survives source archival.
- Admin power does not bypass professional record immutability.

A hidden button is not enforcement.

## Snapshot rule

A Visit snapshots the selected ACTIVE ChecklistVersion.

Changing the source later must not change existing VisitSnapshotNodes.

While Visit is Draft, replacement of the checklist snapshot is allowed only if it does not orphan node-linked records. For Slice 01, block replacement when linked draft Findings/Recommendations exist.

## UX requirements

- Arabic RTL first.
- mobile-friendly.
- clear page hierarchy.
- comfortable, restrained visual design.
- no rigid wizard unless necessary.
- explicit status.
- actionable empty states.
- clear error messages.
- `dd/mm/yyyy` display/input strategy where browser implementation allows it unambiguously.
- no dead-end page with required empty choice lists.
- unsaved-change behavior must not produce misleading warnings after a successful save.

The exact appearance is intentionally replaceable and may evolve after human review.

## Acceptance

All acceptance criteria in `docs/VERTICAL_SLICE_01.md` are mandatory.

Additionally:
- PostgreSQL test path passes.
- permission matrix includes unauthenticated / owner inspector / other inspector / admin.
- changing an ACTIVE Checklist requires creating a new DRAFT version.
- finalized objects reject direct ORM/service-level mutation through public application commands.
- no business invariant exists only in JavaScript/template logic.

## Execution cadence

Implementation MUST follow `docs/CONTROLLED_IMPLEMENTATION_CYCLE.md` and `docs/SLICE_01_INCREMENT_PLAN.md`.

Do not implement the whole slice in one uncontrolled pass.

For each increment:
1. implement only that increment.
2. run required verification.
3. submit the increment for review.
4. correct review findings.
5. re-run verification.
6. record a checkpoint.
7. proceed only after `PASS — NEXT INCREMENT ALLOWED`.

Human acceptance starts only after all Slice 01 increments have passed their machine review/correction gates.

## Deliverables

- working application.
- migrations.
- tests.
- CI.
- README setup/run instructions.
- demo/test data creation command that is idempotent and clearly non-production.
- architecture note for any implementation decision not already covered.
- Human Acceptance checklist for the owner.

## Stop conditions

Stop and surface the issue if:
- a requirement conflicts with an invariant.
- implementing the slice requires changing the accepted Domain meaning.
- a destructive data decision is needed.
- a future feature appears necessary only because of speculative design.

Do not broaden scope to "help".
