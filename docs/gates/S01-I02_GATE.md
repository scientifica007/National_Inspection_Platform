# Increment Gate — S01-I02 Local Institutions

## Increment ID

`S01-I02`

## Status

`IMPLEMENTED — AWAITING INDEPENDENT RE-REVIEW`

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

- [x] Institution has UUID PK, name, lifecycle, creator, local owner, timestamps and archived_at.
- [x] no hard-coded Institution registry/data.
- [x] create derives creator/owner from persisted actor identity.
- [x] `institution.create.local` controls local creation.
- [x] owner read requires `institution.read.own`.
- [x] owner edit/archive/delete requires stored ownership plus existing `institution.create.local`.
- [x] active Platform Admin can list/view all Institutions.
- [x] Platform Admin status alone cannot edit/archive/delete another Person's Institution.
- [x] another inspector cannot discover/read/mutate another owner's Institution.
- [x] archived Institution remains readable when visible but is not editable.
- [x] archive is one-way in S01-I02; no unarchive.
- [x] authorized unreferenced local Institution can be hard-deleted.
- [x] protected-delete condition maps to an explicit retention/domain error; no silent cascade.
- [x] no owner-transfer/impersonation path.
- [x] forms do not expose creator/owner/lifecycle internals as writable fields.
- [x] mutations are CSRF-protected and server-authorized.
- [x] S01-I01 regression tests remain green.
- [x] no S01-I03 or later module added.

## Required Automated Checks

- [x] Ruff lint.
- [x] Ruff format.
- [x] Django system check.
- [x] migration generation/review.
- [x] `makemigrations --check --dry-run`.
- [x] model/lifecycle tests.
- [x] application service tests.
- [x] owner / other inspector / Admin permission matrix.
- [x] HTTP/authentication/CSRF tests.
- [x] PostgreSQL full suite.
- [x] fresh empty PostgreSQL migration path.
- [x] no secrets/real data/future modules.

## Implementation Result

- branch: `build/s01-i02`
- starting main SHA: `dd2a17dbb161f342631c7e468223ce02197622d8`
- implementation commits: recorded in Git history for `build/s01-i02`; exact final head recorded in the PR/final executor report.
- final head: recorded in the PR/final executor report after the final evidence push.
- draft PR: pending creation.
- files/modules changed:
  - new `institutions` app.
  - `config` app registration and URL routing.
  - base navigation and existing CSS components.
  - project scope/PostgreSQL tests.
  - S01-I02 implementation notes/gate evidence.
- migrations: `institutions/migrations/0001_initial.py`
- test count: `312 passed`
- CI: pending after draft PR/final push.
- notes: PostgreSQL 16.15 local verification completed; no SQLite fallback used; no S01-I03+ module added.

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

`HOLD — RE-REVIEW REQUIRED`

Executor must leave this as:

`HOLD — RE-REVIEW REQUIRED`

after implementation.

Only the independent reviewer/maintainer may record:

`PASS — NEXT INCREMENT ALLOWED`

## Next Increment

Not authorized.

`S01-I03` remains forbidden until S01-I02 receives explicit PASS.
