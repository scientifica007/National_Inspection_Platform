# Increment Gate — S01-I01

## Increment ID
`S01-I01`

## Goal
Project skeleton plus identity/authority foundation: a Django 5.2 LTS project
on PostgreSQL with a custom Account from day one, Person separation, minimal
CapabilityGrant (`OWN`/`ALL`), authentication, an Arabic RTL shell, and the
CI/lint/test foundation.

## In Scope
- Python 3.12 project, Django 5.2 LTS, PostgreSQL canonical.
- Environment-driven configuration, `.env.example`, `.gitignore`.
- `config/` project package; bounded `identity` app.
- `Person`, custom `Account` (`AUTH_USER_MODEL`), `CapabilityGrant`.
- Server-side authority primitives.
- Login, logout, protected dashboard shell, account list.
- Arabic RTL shell with design tokens and reusable components.
- pytest / pytest-django / Ruff / CI.

## Out of Scope
Institutions, checklists, visits, findings, recommendations, finalization,
snapshots, amendment, missions, teams, assignments, geography, organization
hierarchy, dashboards, reports, datasets, notifications, REST API, mobile,
AI features, generic workflow/rule engines, microservices.

## Affected Modules
- `identity` (new)
- `config` (new, presentation/configuration only)

## Invariants Exercised
- Invariant 1 — Actor Always Known.
- Invariant 2 — Identity Cannot Be Borrowed.
- Invariant 3 — Authority Has Scope (Capability ∩ Scope ∩ Time).
- Invariant 4 — Administrative Power Is Not Professional Authorship.

## Acceptance Criteria
- [x] Authentication works (login, logout, session).
- [x] Unauthenticated protected access is redirected to login.
- [x] Custom Account is Django's user model.
- [x] Person ↔ Account one-to-one works.
- [x] `OWN` and `ALL` capability evaluation work for supported cases.
- [x] Revoked/expired/not-yet-valid grants do not authorize.
- [x] Admin status does not create professional-authorship capability.
- [x] No impersonation helper, route or API exists.
- [x] Permission primitives are testable independently of presentation.
- [x] Django system checks pass.
- [x] Migrations are internally consistent.
- [x] No future business module implemented.

## Required Automated Checks
- [x] lint/static — `ruff check .` / `ruff format --check .`
- [x] domain/application tests — `pytest`
- [x] integration/database — PostgreSQL-backed `pytest`
- [x] permissions — `identity/tests/test_permissions.py`
- [x] migrations — `manage.py makemigrations --check --dry-run`
- [x] system check — `manage.py check`
- [ ] browser tests — not applicable to S01-I01

## Implementation Result
- branch: `build/slice-01`
- implementation commit: `2a8ff6e` (implementation), `00a4aab` (correction cycle R1)
- PR: draft #1 — https://github.com/scientifica007/National_Inspection_Platform/pull/1
- files/modules changed: `config/`, `identity/`, `templates/`, `static/`,
  `tests/`, `.github/workflows/ci.yml`, `manage.py`, `pyproject.toml`,
  `requirements*.txt`, `.gitignore`, `.env.example`, `README.md`,
  `docs/IMPLEMENTATION_NOTES_S01_I01.md`, this gate record
- migrations: `identity/migrations/0001_initial.py`
- notes: see `docs/IMPLEMENTATION_NOTES_S01_I01.md`

## Recorded Verification Evidence

| Check | Command | Result |
|---|---|---|
| Python | `.venv/bin/python --version` | Python 3.12.14 |
| Django | `python -c "import django; print(django.get_version())"` | Django 5.2.17 |
| Ruff lint | `ruff check .` | All checks passed |
| Ruff format | `ruff format --check .` | 108 files already formatted |
| Django check | `python manage.py check` | no issues (0 silenced) |
| Migration check | `python manage.py makemigrations --check --dry-run` | No changes detected |
| Migrations applied | `python manage.py showmigrations identity` | `[X] 0001_initial` |
| Fresh DB migration path | `POSTGRES_DB=<fresh> python manage.py migrate` | all migrations applied OK |
| Tests | `pytest -q` | 229 passed |
| PostgreSQL | `connection.vendor` | `postgresql` (PostgreSQL 17.11) |
| CI | GitHub Actions run on the pushed head | see PR #1 |

Verified separately that `git status` is clean, `.env` is git-ignored and
unstaged, and no `db.sqlite3`, dump or token file exists in the tree.

## Environmental Limitations
- None blocking. A local PostgreSQL 17.11 server was available, so the
  PostgreSQL test path was fully exercised rather than waived.
- The execution container was recycled during each correction pass (the
  PostgreSQL server, the uv-managed Python 3.12 and the virtualenv were
  reinstalled and the suite re-run). The evidence above reflects a completed
  run on the final tree, not a cached one.


## Review Findings

### Blocking — Correction Cycle R1

Independent review R1 (`docs/gates/S01-I01_CORRECTION_R1.md`) decided
**HOLD — CORRECTION REQUIRED**. All seven blockers were corrected; see
`docs/IMPLEMENTATION_NOTES_S01_I01.md` for the implementation detail.

| ID | Severity | Status | Correction |
|---|---|---|---|
| B-01 | Critical | corrected | Administrative mutation commands are satisfied only by a real `is_platform_admin` account. An `account.manage` grant no longer authorizes them, so a non-admin cannot self-escalate. New primitive `require_administrative_authority` keeps mutation authorization distinct from the query/display meaning of `evaluate_capability(ACCOUNT_MANAGE)`. |
| B-02 | High | corrected | `AccountAdmin` now extends Django `UserAdmin` with `AdminUserCreationForm` / `UserChangeForm`, so password handling stays hashing-aware and no raw password field is exposed. |
| B-03 | High | corrected | `DJANGO_SECRET_KEY` is required when `DEBUG` is not enabled; settings raise `ImproperlyConfigured` at import. In debug a labelled development-only fallback remains. |
| B-04 | High | corrected | `granted_by_account` is non-null with `on_delete=PROTECT`. Provenance cannot be absent and cannot be silently erased. Corrected in the initial migration (no compatibility migration chain). |
| B-05 | Medium | corrected | Automatic Person + Account creation happens inside one `transaction.atomic()` block, so an Account failure rolls the automatic Person back. |
| B-06 | Medium | corrected | The `license = { text = "Proprietary" }` declaration was removed from `pyproject.toml`. Licensing is left undecided; no other licence was substituted. |
| B-07 | Medium | corrected | `CREATEROLE` was removed from the README setup; only `CREATEDB` is granted and the note states `CREATEROLE`/`SUPERUSER` are not granted. |

### Non-blocking
- N-01 (corrected): the unused, mis-typed `can_manage_accounts` context value was
  removed from the dashboard view along with its now-unused import.
- N-02 (deferred, as instructed): the Platform Admin product UI remains
  read-only. Retained for a future increment before Human Acceptance.

### Architecture/Domain observations
- The correction preserves the broader delegation model in
  `docs/AUTHORITY_MODEL.md` without partially implementing it. Explicit,
  bounded delegation remains future work; B-01 only removes the unsafe shortcut.

## Corrections
- Correction cycle R1: B-01 … B-07 corrected, N-01 cleaned.
- Correction commit: `00a4aab` (all B-01..B-07 code and test corrections). This gate record is updated in the commit that follows it.
- Correction cycle R2: R2-B01 … R2-B05 corrected. See
  `docs/gates/S01-I01_CORRECTION_R2.md` and
  `docs/IMPLEMENTATION_NOTES_S01_I01.md` §11 for the implementation detail.

### Blocking — Correction Cycle R2

Independent re-review R2 decided **HOLD — CORRECTION REQUIRED (R2)**. The R1
findings were confirmed closed; five further blockers were raised and corrected.

| ID | Severity | Status | Correction |
|---|---|---|---|
| R2-B01 | Critical | corrected | `identity.services.create_account` was ungated and could mint `is_platform_admin=True` accounts. It now requires an active real Platform Admin actor. Seeding the first admin is separated into `identity.bootstrap`, which the service does not import. |
| R2-B02 | High | corrected | An existing Account could be rebound to another Person through Django Admin. `Account.save` now refuses a `person` change for a persisted Account (reading the stored value, so a direct `person_id` assignment cannot bypass it), and `AccountChangeForm` disables the field. |
| R2-B03 | High | corrected | `CapabilityGrant` admin exposed add/change/delete that bypassed service and issuer semantics. `CapabilityGrantAdmin` is now inspection-only: all fields read-only, add/change/delete disabled for every actor including a superuser with all permissions. |
| R2-B04 | High | corrected | `CapabilityGrant.account` used `CASCADE`, so deleting a recipient destroyed its authorisation history. Changed to `PROTECT`; deactivation remains the lifecycle operation. |
| R2-B05 | Medium | corrected | Stale documentation: the notes no longer claim mutations require an `account.manage` grant, and PR #1 no longer claims `docs/S01_I01_EXPECTED_OUTPUTS.md` is missing. |

### Non-blocking (R2)
- N-02 (still deferred, as instructed): the Platform Admin product UI remains
  read-only.

## Corrections — Cycle R3

Correction cycle R3: `R3-B01` … `R3-B03` corrected. See
`docs/gates/S01-I01_CORRECTION_R3.md` and
`docs/IMPLEMENTATION_NOTES_S01_I01.md` §12 for the implementation detail.

### Blocking — Correction Cycle R3

Independent re-review R3 decided **HOLD — CORRECTION REQUIRED (R3)**. The R2
findings were confirmed closed; three further blockers were raised and
corrected.

| ID | Severity | Status | Correction |
|---|---|---|---|
| R3-B01 | High | corrected | `identity.bootstrap.bootstrap_platform_admin` saved the Person *before* creating the Account, so a later Account failure (a duplicate username, for example) left an orphan Person. It now delegates Person creation to `AccountManager`, which already writes the automatic Person and the Account in one atomic block (the R2-B05 mechanism), and wraps the call in `transaction.atomic()`. A refused bootstrap now leaves the Person count unchanged with no unreachable Person. |
| R3-B02 | High | corrected | `identity.services.create_person` was an application identity mutation with no actor. It now requires an active real Platform Admin actor through the same `require_administrative_authority` primitive, so a non-admin (including one holding an `account.manage` grant) and an inactive Platform Admin are both denied. No new capability or delegation surface was added. Tests that need a Person as *data* now use the test-only `make_person` factory instead of misusing the gated product service. |
| R3-B03 | Medium | corrected | The README pointed operators at `createsuperuser`, which creates a Django *technical* superuser — a deliberately separate layer from the application Platform Admin. The README now explains the distinction in a table and documents an operator-controlled first-Platform-Admin bootstrap. A management command `identity.management.commands.bootstrap_platform_admin` provides a reproducible procedure that stays inside the technical/deployment boundary: no HTTP route, no template, and the password is read from an environment variable only, never stored in source. |

### Non-blocking (R3)
- The raw `QuerySet.update()` Person-binding bypass remains explicitly
  unsupported, as accepted in R2.
- The product Platform Admin management UI remains deferred.
- `AuditEvent` coverage remains deferred to the audit increment.

## Corrections — Cycle R4

Correction cycle R4: `R4-B01` (code) and `R4-B02` (PR summary) corrected. See
`docs/gates/S01-I01_CORRECTION_R4.md` and
`docs/IMPLEMENTATION_NOTES_S01_I01.md` §13 for the implementation detail.

### Blocking — Correction Cycle R4

Independent re-review R4 confirmed R3-B01…R3-B03 closed and raised one further
blocking finding plus one documentation finding.

| ID | Severity | Status | Correction |
|---|---|---|---|
| R4-B01 | High | corrected | `identity.permissions.require_administrative_authority` read the actor through `getattr(actor, "is_platform_admin", False)` plus `actor.is_active`, so it trusted duck typing. A fabricated object exposing those two attributes, or an unsaved `Account`, satisfied the primitive with no persisted acting identity; a stale instance whose row had since been deactivated or demoted also still passed. It now rejects non-`Account` actors and unsaved Accounts, and re-reads the stored row (`values_list("is_platform_admin", "is_active")`), so the current persisted state decides. A missing row is denied. Django's technical superuser layer is still not consulted and delegation is still not implemented, so no new capability or acceptance surface was added. |
| R4-B02 | Low | corrected | The top of PR #1's verification summary still showed R2 totals (94 formatted files, 162 tests). It now reflects R4 (105 formatted files, 218 tests) while the historical R1/R2/R3 sections are retained unchanged. |

### Non-blocking (R4)
- The raw `QuerySet.update()` Person-binding bypass remains unsupported, as
  accepted in R2 scope.
- The product Platform Admin management UI remains deferred.
- `AuditEvent` coverage remains deferred to the audit increment.

### Operational security notice (R4)

Independent review R4 recorded that the execution transcript supplied with the
earlier pass exposed an access-token-like GitHub credential in terminal output
before sanitization. It was not present in the repository diff. No such value
appears in any commit, document, test or report from this correction pass, and
remote output was inspected with the credential sanitized. The credential is
treated as exposed and its rotation is the maintainer's action, not this
executor's.

## Corrections — Cycle R4.1 (residual)

Correction cycle R4.1: `R4-B01-R` corrected. See
`docs/gates/S01-I01_CORRECTION_R4_1.md` and
`docs/IMPLEMENTATION_NOTES_S01_I01.md` §14 for the implementation detail.

### Blocking — Correction Cycle R4.1

Independent re-review R4 closed `R4-B02` and confirmed `R4-B01` substantially
corrected, with one residual case.

| ID | Severity | Status | Correction |
|---|---|---|---|
| R4-B01-R | High | corrected | An unsaved `Account` could carry an explicit `pk` copied from a real Platform Admin. `pk is not None` cannot distinguish "persisted" from "carries a PK value", so the check passed and the subsequent stored-row lookup resolved to the genuine privileged row, authorizing the mutation. The actor handed to the services was never a persisted identity, and because provenance is written from the actor (`granted_by_account=actor`), the mutation could be attributed to the real admin's FK — violating Actor Always Known and Identity Cannot Be Borrowed. The primitive now also rejects any instance still in Django's unsaved state (`actor._state.adding`) before the lookup. The current-row active/admin lookup is unchanged, so stale deactivated/demoted actors are still caught by stored state. No authentication redesign, no delegation, no capability types, no migration. |

Reproduction before the fix confirmed the defect was real: a borrowed-`pk`
instance was allowed through `require_administrative_authority`, and
`grant_capability` with it created a grant recording the real admin as issuer.

### Non-blocking (R4.1)
- The raw `QuerySet.update()` Person-binding bypass remains unsupported, as
  accepted in R2 scope.
- The product Platform Admin management UI remains deferred.
- `AuditEvent` coverage remains deferred to the audit increment.

## Re-verification
- [x] all blocking findings resolved (R1, R2, R3, R4 and R4.1)
- [x] regression tests added (110 across R1/R2; 37 in R3; 19 in R4; 11 in R4.1)
- [x] relevant checks pass (229 tests, Ruff, Django check, migration check, fresh-DB migration path, CI)
- [x] new R3 tests confirmed to fail against the pre-correction implementation
- [x] new R4 tests confirmed to fail against the pre-correction implementation (10 of 19)
- [x] new R4.1 tests confirmed to fail against the pre-correction implementation (5 of 11)

## Checkpoint Decision

`HOLD — RE-REVIEW REQUIRED`

Correction cycles R1 through R4.1 are complete: every blocking finding was
corrected and regression-tested, and the full suite passes against PostgreSQL
with CI green. This record does **not** claim PASS. Closing each blocker, and any
subsequent `PASS — NEXT INCREMENT ALLOWED`, is reserved for the independent
reviewer or maintainer. S01-I02 is not started.

## Next Increment
Not defined. `S01-I02` remains unauthorized until S01-I01 is explicitly marked
`PASS — NEXT INCREMENT ALLOWED` by the review/maintainer process.
