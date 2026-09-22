# S01-I02 — Local Institutions

Status: **IMPLEMENTED — AWAITING INDEPENDENT RE-REVIEW**
Branch: `build/s01-i02`
Starting main SHA: `dd2a17dbb161f342631c7e468223ce02197622d8`

This note records the bounded implementation choices for S01-I02. It does not
claim PASS and does not authorize S01-I03.

## 1. Scope implemented

S01-I02 adds the first business module, `institutions`, with:

- `Institution` model and initial migration.
- local create/list/detail/edit/archive/delete product flow.
- service-owned mutation rules and transaction boundaries.
- selector-owned read visibility.
- server-side object authorization.
- minimal Arabic RTL templates integrated into the existing shell.
- regression tests for model/lifecycle, services, selectors, HTTP/CSRF, and
  scope boundaries.

No `knowledge`, `visits`, `records`, `audit`, `missions`, `teams`,
`geography`, `organization`, shared registry, ownership transfer, unarchive,
REST API, SPA, background job, or microservice work was started.

## 2. Institution model

`institutions.models.Institution` implements the accepted shape:

- UUID primary key.
- `name`.
- `lifecycle`: `LOCAL_ACTIVE` or `ARCHIVED`.
- `created_by_person` -> `identity.Person` with `PROTECT`.
- `local_owner_person` -> `identity.Person` with `PROTECT`.
- `created_at`, `updated_at`, `archived_at`.

The default lifecycle is `LOCAL_ACTIVE`. `created_by_person` and
`local_owner_person` are not form fields and are set only by the create service
from the persisted acting Account's stored Person.

A model clean rule and database check constraint keep lifecycle and
`archived_at` consistent:

- `LOCAL_ACTIVE` requires `archived_at is NULL`.
- `ARCHIVED` requires `archived_at is NOT NULL`.

No name uniqueness is imposed, and no institution registry/seed list exists.

## 3. Authority and visibility

The implementation reuses `identity.permissions`; it does not add a second
actor resolver, permission engine, role hierarchy, or delegation framework.

Permission matrix:

| Actor | List/detail visibility | Create | Edit/archive/delete |
|---|---|---|---|
| Owner inspector with `institution.read.own` | own Institutions | requires `institution.create.local` | requires stored ownership + `institution.create.local` + active lifecycle |
| Other inspector | hidden / object URL returns not found | only for their own new Institution if separately granted | denied |
| Active Platform Admin | all Institutions | not implied by Admin status | denied unless the same real Person is also the local owner with required professional grant |
| Inactive Admin | denied | denied | denied |
| Fabricated/unsaved/borrowed actor | denied | denied | denied |

The read selectors use `resolve_persisted_account`, `is_platform_admin`, and
`has_capability`. Mutation predicates also require stored local ownership by
the persisted actor's Person. Admin visibility remains separate from local
ownership and mutation authority.

## 4. Lifecycle and delete behavior

Implemented lifecycle:

```text
LOCAL_ACTIVE
  ├── edit
  ├── hard delete when retention permits
  └── archive -> ARCHIVED
```

There is no unarchive path. Archived Institutions remain readable to visible
actors but cannot be edited, archived again, or hard-deleted in this increment.

Hard delete is explicit and owner-authorized. Because S01-I02 has no Visit or
finalized-history module yet, the reachable case is an authorized owner's
unreferenced local Institution. If relational protection raises
`ProtectedError`, the service maps it to `InstitutionRetentionError` rather
than cascading or leaking the internal exception.

## 5. UI and HTTP behavior

The UI adds:

- navigation entry: `مؤسساتي`.
- list with lifecycle/status.
- create form.
- detail page.
- edit form.
- archive POST action.
- explicit hard-delete confirmation and POST action.

Forms expose only `name`. Creator, owner, lifecycle internals, timestamps, and
`archived_at` are not writable form fields. Mutations use POST where unsafe and
retain Django CSRF protection. Server-side services/selectors enforce the real
rules; hidden buttons are supplementary only.

## 6. Migration

Migration added:

- `institutions/migrations/0001_initial.py`

The migration creates only the `Institution` table and the lifecycle/archive
consistency constraint. It depends on `identity.0001_initial` and is
non-destructive.

## 7. Tests

New/updated coverage includes:

- UUID PK/default lifecycle/owner/creator/timestamps.
- lifecycle/archive consistency.
- archived mutation rejection and absence of unarchive route/service.
- create authorization and persisted actor identity.
- fabricated/unsaved actor denial.
- owner/other/Admin visibility matrix.
- inactive/stale/borrowed actor visibility denial.
- owner/other/Admin mutation matrix.
- missing capability denial.
- authorized hard-delete success.
- `ProtectedError` to retention-domain error mapping.
- no hard-coded Institution data.
- HTTP authentication, 404 object hiding, CSRF, POST-only archive, form fields.
- project scope guard updated to allow `institutions` and continue forbidding
  S01-I03+ modules.
- PostgreSQL backend assertion.

Full suite result on PostgreSQL:

```text
312 passed in 591.79s (0:09:51)
```

## 8. Verification evidence

Local checks run from `build/s01-i02`:

```text
ruff check .
All checks passed!

ruff format --check .
131 files already formatted

python manage.py check
System check identified no issues (0 silenced).

python manage.py makemigrations --check --dry-run
No changes detected

python manage.py migrate --noinput
Applied full migration chain on a fresh empty PostgreSQL database:
admin, auth, contenttypes, identity, institutions, sessions.

pytest -q
312 passed in 591.79s (0:09:51)
```

PostgreSQL evidence:

- Temporary PostgreSQL 16.15 cluster started locally on `127.0.0.1:55432`.
- Django settings used `django.db.backends.postgresql`.
- Test suite included a `connection.vendor == "postgresql"` assertion.

No SQLite fallback was used.

## 9. Data and security

No secrets, database dumps, real personal data, or official inspection data were
added. Test names and records are synthetic.

## 10. Known limitations

- CI result is recorded in the PR/final executor report after the final pushed
  head runs on GitHub Actions.
- Future finalized-history retention is not implemented because Visits and
  snapshots are explicitly out of S01-I02 scope. The service is prepared to map
  relational `ProtectedError` when future protected dependencies exist.

## 11. Stop state

Executor stop state:

`HOLD — RE-REVIEW REQUIRED`

Only the independent reviewer/maintainer may record PASS or authorize S01-I03.
