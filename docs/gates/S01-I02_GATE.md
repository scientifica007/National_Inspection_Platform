# Increment Gate — S01-I02 Local Institutions

## Increment ID

`S01-I02`

## Status

`AUTHORIZED — IMPLEMENTATION PENDING`

## Goal

Introduce local Institution master data as the first business module while preserving:
- local inspector ownership;
- server-side object authority;
- Platform Admin visibility without identity borrowing;
- clean lifecycle/archive/delete semantics;
- future historical-retention compatibility.

## In Scope

- `institutions` Django app.
- Institution model per accepted Slice 01 data model.
- create/list/detail/edit/archive/delete rules.
- owner/other inspector/Admin visibility and mutation matrix.
- server-side authorization.
- Arabic RTL minimum UI.
- migration.
- automated tests.
- implementation notes.

## Out of Scope

- Checklist/knowledge.
- Visits/snapshots.
- Findings/Recommendations.
- AuditEvent.
- Missions/Teams.
- geography/organization engines.
- shared/national Institution registry.
- propose/approve/publish.
- ownership transfer.
- unarchive.
- new generic capability/delegation engine.
- REST API / SPA / microservices.

## Affected Modules

- new: `institutions`
- existing integration only: `config`, `identity`, base templates/navigation, test/CI support as needed.

## Invariants Exercised

- Actor Always Known.
- Identity Cannot Be Borrowed.
- Ownership vs Visibility vs Authority are distinct.
- Admin does not become another Person/owner.
- Freedom by Default, Constraint by Rule.
- Institution data is not hard-coded.
- current master data may evolve; immutable history is preserved later through snapshots.
- hard deletion must not destroy retained historical meaning.

## Acceptance Criteria

- [ ] Institution has UUID PK, name, lifecycle, creator, local owner, timestamps and archived_at.
- [ ] no hard-coded Institution registry/data.
- [ ] create derives creator/owner from persisted actor identity.
- [ ] `institution.create.local` controls local creation.
- [ ] owner read requires `institution.read.own`.
- [ ] owner edit/archive/delete requires stored ownership plus existing `institution.create.local`.
- [ ] active Platform Admin can list/view all Institutions.
- [ ] Platform Admin status alone cannot edit/archive/delete another Person's Institution.
- [ ] another inspector cannot discover/read/mutate another owner's Institution.
- [ ] archived Institution remains readable when visible but is not editable.
- [ ] archive is one-way in S01-I02; no unarchive.
- [ ] authorized unreferenced local Institution can be hard-deleted.
- [ ] protected-delete condition maps to an explicit retention/domain error; no silent cascade.
- [ ] no owner-transfer/impersonation path.
- [ ] forms do not expose creator/owner/lifecycle internals as writable fields.
- [ ] mutations are CSRF-protected and server-authorized.
- [ ] S01-I01 regression tests remain green.
- [ ] no S01-I03 or later module added.

## Required Automated Checks

- [ ] Ruff lint.
- [ ] Ruff format.
- [ ] Django system check.
- [ ] migration generation/review.
- [ ] `makemigrations --check --dry-run`.
- [ ] model/lifecycle tests.
- [ ] application service tests.
- [ ] owner / other inspector / Admin permission matrix.
- [ ] HTTP/authentication/CSRF tests.
- [ ] PostgreSQL full suite.
- [ ] fresh empty PostgreSQL migration path.
- [ ] no secrets/real data/future modules.

## Implementation Result

- branch: `build/s01-i02`
- starting main SHA:
- implementation commits:
- final head:
- draft PR:
- files/modules changed:
- migrations:
- test count:
- CI:
- notes:

## Review Findings

### Blocking

Pending independent review.

### Non-blocking

Pending independent review.

### Architecture/Domain observations

Pending independent review.

## Corrections

Pending.

## Re-verification

- [ ] all blocking findings resolved.
- [ ] regression tests added for review findings.
- [ ] relevant checks pass.

## Checkpoint Decision

Current:

`HOLD — IMPLEMENTATION / INDEPENDENT REVIEW REQUIRED`

Executor must leave this as:

`HOLD — RE-REVIEW REQUIRED`

after implementation.

Only the independent reviewer/maintainer may record:

`PASS — NEXT INCREMENT ALLOWED`

## Next Increment

Not authorized.

`S01-I03` remains forbidden until S01-I02 receives explicit PASS.
