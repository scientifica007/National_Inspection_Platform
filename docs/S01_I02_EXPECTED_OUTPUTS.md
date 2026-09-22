# S01-I02 Expected Outputs

- Increment: **S01-I02 — Local Institutions**
- Status: **AUTHORIZED — NOT STARTED**
- Purpose: precise implementation/review contract for the second controlled increment.
- Precondition: S01-I01 is PASS and merged into `main`.

## Goal

Add the first business module, `institutions`, without broadening the slice.

An authorized inspector can create and manage **their own local Institution data**. Another inspector cannot borrow or mutate that ownership. An active Platform Admin has administrative visibility across institutions but does not gain professional/local ownership or mutation authority merely from Admin status.

Institution rows are current/master data, not immutable professional records. Historical meaning will later be preserved by Visit snapshots.

## Expected repository outputs

Likely new files include equivalents of:

```text
institutions/
  __init__.py
  apps.py
  models.py
  services.py
  selectors.py
  permissions.py        # only if useful; do not duplicate identity authority logic
  forms.py
  views.py
  urls.py
  migrations/
  tests/
  templates/institutions/

docs/IMPLEMENTATION_NOTES_S01_I02.md
docs/gates/S01-I02_GATE.md   # update evidence only; reviewer owns PASS
```

Existing files may be changed only where needed to register the app, route URLs, expose navigation, seed synthetic test setup, or extend tests.

Do **not** create `knowledge`, `visits`, `records`, `audit`, `missions`, `teams`, `reporting`, `geography`, or `organization` merely as placeholders.

## Institution model contract

Implement the accepted Slice 01 Institution shape:

```text
Institution
- id: UUID primary key
- name
- lifecycle: LOCAL_ACTIVE | ARCHIVED
- created_by_person_id -> identity.Person
- local_owner_person_id -> identity.Person
- created_at
- updated_at
- archived_at nullable
```

Requirements:
- default lifecycle is `LOCAL_ACTIVE`.
- `created_by_person` and `local_owner_person` are set from the **persisted acting Account's Person**, never supplied by an HTML form or caller-controlled owner field.
- Person references use history-safe relational behavior; deleting an Institution must never delete a Person.
- no hard-coded Institution registry or seed list.
- do not impose name uniqueness unless a canonical source explicitly requires it.
- lifecycle/archived timestamp consistency should be enforced cleanly in application/model rules; a simple DB constraint is acceptable when it reinforces the same rule.
- no ownership-transfer feature in S01-I02.

## Increment-specific authority contract

Use the already accepted S01-I01 authority foundation. Do not create a second authorization engine.

### Persisted actor
All authority decisions must inherit the persisted-actor protections from `identity.permissions`. Never trust caller-supplied Account flags, Person bindings, or copied PKs.

### Create
Creating a local Institution requires the existing professional capability:

`institution.create.local`

Creation is always for the real acting Person:
- `created_by_person = actor.person`
- `local_owner_person = actor.person`

No "create on behalf of" path exists.

### Owner read
Reading/listing one's own Institution requires:

`institution.read.own`

with OWN scope resolved against the Institution's stored `local_owner_person`.

### Owner mutation
For this bounded Slice 01 increment, do **not** invent a new institution mutation-capability taxonomy.

Edit/archive/hard-delete of a local Institution require:
- a genuine active persisted actor;
- stored local ownership by that actor's Person;
- the existing `institution.create.local` capability.

Ownership and lifecycle further restrict the action.

This is an increment-local policy that avoids prematurely adding `institution.update.*`, `institution.archive.*`, or `institution.delete.*` capability families before broader authority needs justify them.

### Platform Admin visibility
An active Platform Admin may:
- list all Institutions;
- view any Institution detail.

Admin status alone must **not** permit:
- changing the Institution name;
- archiving it;
- hard deleting it;
- reassigning ownership;
- performing an inspector action under another Person.

If the same real Person is both Platform Admin and a professional/local owner with the required capability, their legitimate owner action remains possible under their own identity.

### Other inspector
A different inspector without ownership/admin visibility:
- does not see the Institution in their list;
- cannot read its detail through an object-ID URL;
- cannot edit/archive/delete it.

Prefer 404/not-found behavior for unauthorized object discovery where consistent with the existing UI; do not leak another inspector's local data merely to return a more descriptive permission error.

## Lifecycle contract

S01-I02 implements:

```text
LOCAL_ACTIVE
  ├── edit by authorized owner
  ├── hard delete when retention permits
  └── archive ──> ARCHIVED
```

Rules:
- active local Institution is editable by authorized owner.
- archive is a one-way transition in this increment; do not invent unarchive/restore.
- archiving sets `archived_at`.
- an ARCHIVED Institution remains readable to its owner (with read authority) and to Platform Admin visibility.
- archived Institution is not editable.
- no use/selectability rules for Visits exist yet; that belongs to S01-I04.
- hard delete is an explicit destructive action and must be server-authorized.

## Hard-delete / retention contract

Canonical rule:
**hard delete is allowed only when no finalized historical record depends on the Institution.**

S01-I02 has no Visit/finalized-history model yet. Therefore:
- implement the currently reachable case: an authorized owner's unreferenced local Institution can be hard-deleted;
- deletion must be explicit and must not cascade into Person/identity data;
- if database relational protection raises `ProtectedError`, map it to an explicit institution-retention/domain error rather than silently cascading or leaking an internal traceback;
- do not import or create a future `visits` module just to simulate finalized history;
- S01-I04/S01-I06 must add the concrete historical-dependency regression when Visit/finalization exists.

This is not permission to weaken future retention; it is a scoped implementation of the rule at the first point where the dependent history does not yet exist.

## Required application services

Names may vary, but the use cases should be explicit and testable, equivalent to:

- `create_local_institution`
- `update_local_institution`
- `archive_local_institution`
- `delete_local_institution`

Services own mutation rules and transaction boundaries.

Do not put ownership/lifecycle enforcement only in views/forms/templates.

## Required selectors

Equivalent read operations should cover:
- Institutions visible to the current actor.
- one Institution visible to the current actor.

Selectors must preserve:
- owner-only visibility for inspectors;
- Platform Admin read visibility;
- no borrowed-PK identity leakage.

Do not directly expose unrestricted `Institution.objects.all()` to inspector-facing views.

## Required UI

Minimum Arabic RTL product UI:
- navigation entry: **مؤسساتي** or equivalent clear Arabic label;
- Institution list with lifecycle/status visible;
- create form;
- detail page;
- edit action for authorized active owner;
- archive action;
- explicit hard-delete confirmation/action.

Forms should expose only fields the user may actually author. At minimum, the Institution form exposes `name`; it must not expose owner/creator/lifecycle timestamps as writable user fields.

Reuse the existing base layout/design tokens. Do not redesign the whole application in S01-I02.

## Required HTTP/security behavior

- authentication required.
- CSRF remains enabled.
- create/edit/archive/delete use POST or appropriate unsafe methods.
- object authorization is server-side.
- hiding buttons is supplementary only.
- no impersonation or "act as owner" route.
- no real personal/official data in fixtures.

## Required tests

At minimum, add regression coverage for:

### Model/lifecycle
- UUID business PK.
- default `LOCAL_ACTIVE`.
- correct owner/creator/timestamps.
- archive sets lifecycle and `archived_at`.
- archived edit rejected.
- no unarchive path.
- no hard-coded Institution data.

### Create
- active persisted inspector with `institution.create.local` creates own Institution.
- created_by/local_owner are the stored actor Person, not caller-supplied identity.
- missing capability denied.
- fabricated/unsaved/borrowed actor cannot create.

### Visibility/read matrix
For each sensitive read path:
- unauthenticated denied/redirected.
- owner inspector with `institution.read.own` allowed.
- other inspector denied / object hidden.
- active Platform Admin allowed to read.
- inactive Admin denied.
- borrowed/stale actor does not gain visibility.

### Edit/archive/delete matrix
- authorized owner succeeds while lifecycle permits.
- other inspector denied.
- Platform Admin status alone denied.
- owner without required capability denied.
- archived edit denied.
- repeated/invalid archive transition rejected explicitly.
- authorized unreferenced hard delete succeeds.
- retention/protected-delete failure maps to explicit domain/application error and does not silently cascade.

### Regression
- all S01-I01 identity/authority tests stay green.
- Admin remains distinct from professional/local ownership.
- no owner reassignment/impersonation path appears.

## Migration/DB expectations

- one small reviewable initial `institutions` migration is expected.
- PostgreSQL remains canonical.
- `makemigrations --check --dry-run` must be clean after committed migration.
- apply the complete migration chain to a fresh PostgreSQL database.
- no destructive migration.
- no SQLite fallback.

## Expected documentation/evidence

Executor should add:
- `docs/IMPLEMENTATION_NOTES_S01_I02.md`.
- implementation evidence into `docs/gates/S01-I02_GATE.md`.
- PR body with scope, migration and test evidence.

Executor must **not**:
- mark `PROJECT_STATE.md` PASS;
- create a PASS checkpoint;
- merge the PR;
- authorize S01-I03.

Those belong to independent review/maintainer closure.

## Explicit non-outputs

Review warning if any of these appear without a documented source-of-truth requirement:

- Checklist/ChecklistVersion/ChecklistItem.
- Visit or snapshots.
- Finding/Recommendation.
- AuditEvent.
- Mission/Assignment/Team.
- geography/organization engines.
- national/shared Institution registry.
- propose/approve/publish workflow.
- ownership transfer.
- unarchive/restore workflow.
- new generic capability engine.
- new generic repository/service abstraction.
- REST API.
- SPA/frontend framework.
- background jobs.
- microservices.

## Gate

Executor completion is not PASS.

After delivery:
`HOLD — RE-REVIEW REQUIRED`

Independent review must verify actual code, migration, tests, CI, permission matrix and scope before recording:

`PASS — NEXT INCREMENT ALLOWED`

Only then may S01-I03 begin.
