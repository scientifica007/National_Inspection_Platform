# S01-I01 — Project Skeleton + Identity/Authority Foundation

Status: **IMPLEMENTED — AWAITING INDEPENDENT REVIEW**
Branch: `build/slice-01`

This note records the implementation decisions taken while building S01-I01
that were not already fully specified by the accepted design documents.

## 1. Identity model shape

- `Person` carries a UUID primary key (business entity, `docs/VERTICAL_SLICE_01_DATA_MODEL.md`).
- `Account` is a custom Django user (`AUTH_USER_MODEL = "identity.Account"`) and
  keeps Django's default integer primary key. The concrete data model shows
  `Account.id` without a type annotation, and Django's authentication internals
  assume the standard key. `Person` ↔ `Account` is a one-to-one relation.
- `Account.person` uses `on_delete=PROTECT`: disabling or deleting an Account
  must never cascade into deleting the Person or their history
  (`docs/SECURITY_AND_DATA_GOVERNANCE.md` §2).
- `Account.is_platform_admin` is administrative authority only. It is never
  consulted by professional capability evaluation.

## 2. CapabilityGrant

Fields follow the accepted model: `capability_code`, `scope_kind`
(`OWN` | `ALL`), `valid_from`, `valid_until`, `delegable`,
`granted_by_account`, `revoked_at`.

Two additions that stay within the accepted semantics:

- A database `CheckConstraint` enforcing an ordered validity window. The model
  also validates this in `clean()`. The constraint reinforces the rule; it does
  not replace the application-level check.
- An index on `(account, capability_code)` for grant lookup.

No generic Scope engine, no `Delegation` model and no scope composition are
implemented: `OWN` and `ALL` are the only supported scope kinds, as required by
this increment.

## 3. Authority evaluation

`identity/permissions.py` is the single server-side evaluation point, free of
HTTP and templates so it can be tested independently
(`docs/ENGINEERING_CONVENTIONS.md`, `docs/TEST_STRATEGY.md` §1).

Two authority dimensions are kept strictly separate (ADR-0003):

1. Administrative — `is_platform_admin` satisfies only capabilities listed in
   `ADMINISTRATIVE_CAPABILITIES` (currently `account.manage`).
2. Professional — satisfied only by an active `CapabilityGrant`.

`evaluate_capability` returns an explainable `AuthorityDecision` carrying a
machine-readable reason, which keeps denial behaviour testable without leaking
internals to end users.

`subject_person` is the Person an action applies to. When a caller passes an
explicit Person, that Person is honoured exactly as given — no code path
substitutes it. An `OWN` grant authorises only when the subject is the
Account's own Person; a mismatch is denied with reason `scope_mismatch`.

## 4. Absence of impersonation

There is no impersonation helper, view, URL, form or service anywhere. The
dashboard reports the acting Account's real Person only. The account list is a
read-only administrative view and offers no "act as" action. Two automated
tests assert this absence structurally (no impersonation symbol in
`identity.permissions`, no impersonation route in the URL resolver).

## 5. Services and selectors

`identity/services.py` holds commands (`create_person`, `create_account`,
`grant_capability`, `revoke_capability`, `deactivate_account`) and owns
transaction boundaries. `identity/selectors.py` holds read-only queries.
Administrative commands require the primitives in `identity.permissions` —
specifically a real, active Platform Admin — so an inspector cannot escalate by
granting themselves capabilities. Since R2-B01 this includes `create_account`:
application account creation is an authorized mutation, not an open helper.

Revocation sets `revoked_at` instead of deleting the row, preserving grant
history.

## 6. Presentation

Arabic-first, RTL-native (`dir="rtl"`), semantic HTML with logical CSS
properties so DOM order stays meaningful. Design Tokens live in
`static/css/design-tokens.css`; layout and components consume them in
`static/css/app.css`. No business, permission or lifecycle rule appears in a
template, stylesheet or script.

## 7. Configuration

Environment-driven settings with explicit helpers rather than a configuration
framework. PostgreSQL is the only configured database backend; SQLite is
deliberately not offered, since designing for it first would hide
database-behaviour problems. `.env` is git-ignored and `.env.example` contains
placeholder values only.

## 8. System Operator vs Admin

Django's `is_superuser`/`is_staff` remain the technical control-plane flag for
`/admin/`, and are deliberately **not** wired to `is_platform_admin`. This
mirrors the accepted model, where the System Operator/Developer is a technical
layer outside the functional hierarchy (`docs/AUTHORITY_MODEL.md`), separate
from the application's administrative authority.

Consequence worth recording: a Django superuser reaches `/admin/` but does not
automatically hold application administrative authority (`is_platform_admin`),
and never holds professional authorship. Conversely, `is_platform_admin` grants
application administrative authority but not `/admin/` access.

Known limitation for later increments: `/admin/` editing is not yet covered by
`AuditEvent`, because the `audit` module belongs to a later increment. Until
audit exists, technical-plane mutations are not traceable in application
history. This is recorded as a risk, not solved speculatively here.

## 9. Deliberately not implemented

No `institutions`, `knowledge`, `visits`, `records`, `audit`, `missions`,
`teams`, `geography`, `organization` or `reporting` app exists — not even as an
empty placeholder. A test asserts that neither `INSTALLED_APPS` nor the app
registry contains any deferred module.

## 10. Correction Cycle R1 (B-01 … B-07)

Independent review R1 decided **HOLD — CORRECTION REQUIRED**
(`docs/gates/S01-I01_CORRECTION_R1.md`). Current main (`ac7e01d`) was merged
into `build/slice-01` before any edit; the implementation commits were
preserved. The corrections are as follows.

### B-01 — administrative self-escalation (Critical)

`evaluate_capability` previously accepted an `account.manage` CapabilityGrant as
satisfying administrative authority. Combined with the service commands, a
non-admin holding that grant could grant itself any capability — bypassing scope
and delegable semantics.

The rule is now: an administrative capability is satisfied **only** by a real
`is_platform_admin` account. A new primitive,
`require_administrative_authority`, authorizes the mutating commands
(`grant_capability`, `revoke_capability`, `deactivate_account`) and is likewise
satisfied only by a real Platform Admin; a deactivated admin cannot mutate.

To avoid a confusing dual meaning, the two uses are kept explicitly apart:

- `evaluate_capability(..., ACCOUNT_MANAGE)` answers *"does this account hold
  administrative authority?"* — the query/display question.
- `require_administrative_authority` authorizes an actual mutation.

Both deliberately exclude grant-based administration, because explicit bounded
delegation is deferred (`docs/AUTHORITY_MODEL.md` §Delegation). Partially
implementing delegation here is exactly what produced the escalation path.

### B-02 — hashing-safe admin

`AccountAdmin` now extends `UserAdmin` with `AccountCreationForm`
(`AdminUserCreationForm` — the class `UserAdmin.add_form` expects) and
`AccountChangeForm` (`UserChangeForm`, whose password field is the read-only
`ReadOnlyPasswordHashField`). `person` and `is_platform_admin` appear in the
fieldsets/add_fieldsets. `CapabilityGrantAdmin` makes `granted_by_account` read-only,
so an existing grant's provenance cannot be rewritten.

Writing the test surfaced a real defect in the first attempt: the add form
declared only `username`, so the admin add view would have inserted an Account
with a null `person` and failed at the database. `person` is now declared on the
creation form.

### B-03 — secret key fails closed

`DJANGO_SECRET_KEY` is read first. If it is present it is used verbatim. If it is
absent or blank: with `DEBUG` enabled, a clearly labelled development-only
fallback is used; otherwise settings raise `ImproperlyConfigured` at import,
before the application can serve a request. The failure message says what to set
and never echoes a value. CI supplies `DJANGO_SECRET_KEY` with `DJANGO_DEBUG:
"False"`, so CI exercises the required-key path rather than the fallback.

### B-04 — grant provenance

`granted_by_account` is non-null with `on_delete=PROTECT`. A grant can no longer
exist without an issuer, and the issuer cannot be deleted while referenced, so
"actor always known" is enforced by the database and not only by convention.
Because the schema is still a development-only initial migration with no
production data, the initial migration was regenerated cleanly rather than
chained — per the correction prompt's migration discipline. No compatibility
migration was added.

### B-05 — atomic Person + Account creation

`AccountManager._create_user` writes the automatic Person and the Account inside
one `transaction.atomic()` block. A failure anywhere in Account creation rolls
the automatic Person back. A Person supplied by the caller is never saved or
deleted by this path, because it was not created here.

Note on the shape of the fix: this deliberately uses an explicit atomic block
rather than `transaction.on_commit`, because in autocommit mode (notably under
`pytest-django`'s `TestCase`) `on_commit` runs immediately and would have left
the orphan exactly as before, while still appearing correct.

### B-06 / B-07 / N-01

- B-06: the `license = { text = "Proprietary" }` declaration was removed from
  `pyproject.toml`. Licensing stays undecided; no other licence was substituted.
- B-07: `CREATEROLE` was removed from the README. Only `CREATEDB` is granted,
  which is what pytest-django needs to create its test database, and the note
  states `CREATEROLE`/`SUPERUSER` are not granted.
- N-01: the unused, mis-typed `can_manage_accounts` context value and its
  now-unused import were removed from the dashboard view.

### Regression tests added

| Blocker | Test file | Count |
|---|---|---|
| B-01 | `identity/tests/test_administrative_mutations.py` | 16 |
| B-02 | `identity/tests/test_admin_configuration.py` | 12 |
| B-03 | `tests/test_settings_secret_key.py` | 11 |
| B-04 | `identity/tests/test_grant_provenance.py` | 11 |
| B-05 | `identity/tests/test_account_creation_atomicity.py` | 5 |

Total 55 new tests; the suite grew from 61 to 111.

The B-03 tests run the settings module in a subprocess with a controlled
environment, so the real import path and the real failure are exercised rather
than a re-implementation of the rule.

## 11. Correction Cycle R2 (R2-B01 … R2-B05)

Independent re-review R2 decided **HOLD — CORRECTION REQUIRED (R2)**
(`docs/gates/S01-I01_CORRECTION_R2.md`). The R1 findings were confirmed closed.
Current main (`73e1e9f`) was merged into `build/slice-01` before any edit, and
the S01-I01 implementation history was preserved.

### R2-B01 — application account creation is authorized

`identity.services.create_account` was ungated: it was reachable without an
actor and could set `is_platform_admin=True`, so any caller could mint a
Platform Admin. It now takes a required `actor` and calls
`require_administrative_authority`, so only an active real Platform Admin may
create an Account, whether ordinary or administrative.

The chicken-and-egg case of the *first* admin is deliberately handled outside
the service, in `identity.bootstrap.bootstrap_platform_admin`. That module is a
technical/deployment boundary (`docs/AUTHORITY_MODEL.md`), is not imported by
`services.py`, and grants no professional capability. Two tests assert the
separation structurally (AST-level import check, and no bootstrap attribute on
the services module). No product account-management UI was added.

### R2-B02 — the Account→Person binding is frozen

The Person is selectable at creation but not rebindable afterwards. The rule is
enforced in `Account.save`, not only in a form, so Django Admin, forms, a shell
session and future callers all obey it. The guard reads the *stored*
`person_id` rather than the instance, so assigning `account.person_id = ...`
directly cannot slip past it. `AccountChangeForm` additionally disables the
field, keeping the binding visible but not editable.

Residual path, documented rather than overstated: `QuerySet.update()` is raw SQL
and bypasses `save()`. It is not a supported application path; a test records
the boundary explicitly so the guard is not credited with more than it does.

### R2-B03 — CapabilityGrant admin is read-only

The technical admin exposed add/change/delete for grants. Adding a grant there
could not satisfy the required issuer, and change/delete would bypass the
service semantics (the real acting admin is recorded, revocation preserves
history instead of deleting). `CapabilityGrantAdmin` is now inspection-only:
every field is read-only and `has_add_permission`, `has_change_permission` and
`has_delete_permission` all return `False` for every actor, including a Django
superuser holding all permissions. Grant operations remain available only
through `identity.services`.

### R2-B04 — grant history survives recipient deletion

`CapabilityGrant.account` changed from `CASCADE` to `PROTECT`. Deleting a
recipient Account that has grant history is now refused at the database level,
so authorisation records are not silently cascaded away
(`docs/INVARIANTS.md` §1, §16). Account deactivation remains the normal
lifecycle operation: a deactivated Account stops authorizing but is still not
deletable while referenced. The initial migration was regenerated cleanly, as
in R1, because the schema is still development-only with no persistent data.

All three foreign keys out of `CapabilityGrant` (`account`, `granted_by_account`)
and into `Person` now use `PROTECT`, so no deletion path erases identity or
authority history.

### R2-B05 — documentation corrected

`docs/IMPLEMENTATION_NOTES_S01_I01.md` no longer states that mutations require
an `account.manage` grant; it points at the real rule (a real, active Platform
Admin). PR #1's body no longer claims `docs/S01_I01_EXPECTED_OUTPUTS.md` is
missing — that file exists and the note was stale. All R1 evidence is retained
and the R2 evidence is added beside it.

### Regression tests added (R2)

| Blocker | Test file | Count |
|---|---|---|
| R2-B01 | `identity/tests/test_account_creation_authorization.py` | 17 |
| R2-B02 | `identity/tests/test_person_binding_immutable.py` | 12 |
| R2-B03 | `identity/tests/test_grant_admin_readonly.py` | 12 |
| R2-B04 | `identity/tests/test_grant_history_preserved.py` | 10 |

The suite grew from 111 to 162 tests.

### Gate

The gate remains **HOLD — RE-REVIEW REQUIRED**. This executor does not
self-declare PASS; that outcome belongs to the independent reviewer.

## 12. Correction Cycle R3 (R3-B01 … R3-B03)

Third correction-only pass, on the same `build/slice-01` branch. No S01-I02 work
was started and no product surface was added.

### R3-B01 — bootstrap is atomic and reuses the manager path

`identity.bootstrap.bootstrap_platform_admin` previously constructed and saved
the Person itself, then created the Account:

```python
person = Person(display_name=display_name or username)
person.full_clean()
person.save()                       # committed here
return Account.objects.create_user(person=person, ...)
```

If Account creation failed — a duplicate `username` is the easy case — the
Person row survived, unreachable from any Account. The fix removes the
duplicated creation instead of adding a compensating delete:

```python
with transaction.atomic():
    return Account.objects.create_user(
        username=username,
        email=email,
        password=password,
        display_name=display_name or username,
        is_platform_admin=True,
    )
```

`AccountManager._create_user` detects the absent `person` and creates one inside
its own atomic block together with the Account (the R2-B05 mechanism). The
bootstrap therefore inherits an already-tested atomicity path rather than
re-implementing it, and the outer `transaction.atomic()` makes the operation
safe when a caller has not started one. The manager's deliberate contract is
preserved: a Person supplied by the caller is never saved or deleted by the
manager.

Bootstrap still creates `is_platform_admin=True` and still grants no
professional capability.

### R3-B02 — standalone Person creation is authorized

`identity.services.create_person` took only `display_name`. It is an identity
mutation, so it now requires an actor and applies the same narrow rule as the
other administrative commands:

```python
def create_person(*, actor: Account, display_name: str) -> Person:
    require_administrative_authority(actor, action="create_person")
```

`require_administrative_authority` is satisfied only by an active real Platform
Admin in S01-I01, so a non-admin — including an Account holding an
`account.manage` grant — and an inactive Platform Admin are both denied. No new
capability was added, no delegation intake was introduced, and
`ALL_CAPABILITIES` is unchanged.

The command was retained rather than removed because the authorized use case is
real: registering a human being before or independently of their Account. What
changed is that fixtures no longer misuse it. Tests that need a Person merely as
data call the test-only `identity.tests.factories.make_person`, which is
documented as a setup bypass in the same spirit as `make_account`. One existing
test that genuinely exercised the binding path now passes its admin actor
explicitly, so it drives the real gated service.

### R3-B03 — first Platform Admin bootstrap documented and reproducible

The README instructed operators to run `createsuperuser`. That creates a Django
*technical* superuser, which this project deliberately keeps distinct from the
application Platform Admin: `is_superuser`/`is_staff` are not wired to
`is_platform_admin`, so a superuser is not an application administrator, and a
Platform Admin has no `/admin/` access by virtue of that flag. Neither grants
professional authorship.

The README now documents the distinction in a table and gives an
operator-controlled procedure. A management command supplies the reproducible
step:

```bash
export NIP_BOOTSTRAP_PASSWORD='...'
python manage.py bootstrap_platform_admin --username admin --display-name "المدير الأول"
unset NIP_BOOTSTRAP_PASSWORD
```

`identity/management/commands/bootstrap_platform_admin.py` stays inside the
technical/deployment boundary:

- no HTTP route and no template reach it;
- it calls `identity.bootstrap.bootstrap_platform_admin`, the same atomic path
  as R3-B01, inside `transaction.atomic()`;
- the password is read only from an environment variable — it is never a
  command-line option, because that would leak into shell history and `ps`, and
  it is never written to source or committed;
- it refuses to run when the environment variable is unset or the username
  already exists, with the collision leaving no orphan Person.

`identity/services.py` does not import the bootstrap module and the bootstrap
module does not import `services`, so the service's authorization cannot be
weakened by the bootstrap bypass. A test asserts that import direction
structurally rather than by string match.

### Regression tests added (R3)

| Blocker | Test file | Count |
|---|---|---|
| R3-B01 | `identity/tests/test_bootstrap_atomicity.py` | 12 |
| R3-B02 | `identity/tests/test_person_creation_authorization.py` | 12 |
| R3-B03 | `identity/tests/test_bootstrap_management_command.py` | 13 |

The suite grew from 162 to 199 tests.

The R3-B01 tests were confirmed to detect the original defect: restoring the
pre-correction bootstrap made four of them fail (duplicate-username Person
count, orphan-Person absence, and the two structural checks that assert the
manager path is reused). The tests are therefore real regression tests, not
restatements of the current code.

### Gate

The gate remains **HOLD — RE-REVIEW REQUIRED**. Neither this pass nor any
previous one claims PASS; closing the findings and any `PASS — NEXT INCREMENT
ALLOWED` belong to the independent reviewer.

## 13. Correction Cycle R4 (R4-B01, R4-B02)

Fourth correction-only pass, on the same `build/slice-01` branch. No S01-I02
work was started and no product surface was added.

### R4-B01 — administrative authority requires a persisted actor

`identity.permissions.require_administrative_authority` read the actor through
`getattr`:

```python
if not getattr(actor, "is_platform_admin", False):
    ...
if not actor.is_active:
    ...
```

That trusted duck typing. A bare `object()` carrying no attributes was denied by
luck, but any object exposing `is_platform_admin = True` and `is_active = True`
passed — including a fabricated stand-in and an unsaved `Account` instance whose
row was never written. A stale instance whose row had since been deactivated or
demoted in the database also still passed, because only the in-memory flags were
consulted. In each case the mutation proceeded with no persisted acting identity
that actually held administrative authority.

The primitive now resolves the actor against the database:

```python
if not isinstance(actor, Account):
    raise PermissionDeniedError(...)  # fabricated / foreign object
if actor.pk is None:
    raise PermissionDeniedError(...)  # unsaved Account

stored = Account.objects.filter(pk=actor.pk).values_list("is_platform_admin", "is_active").first()
if stored is None:
    raise PermissionDeniedError(...)  # row no longer exists

is_admin, is_active = stored  # stored state decides
```

The stored row, not the caller's object, is authoritative. A caller holding a
stale instance is therefore denied once the row is deactivated or demoted, while
a legitimate current Platform Admin is still allowed. The two explicit checks
(`isinstance`, `pk is None`) give precise failures, and the `None` branch covers
a deleted row.

Deliberately unchanged: delegation is still not implemented; no new capability
or acceptance surface was added; Django's technical superuser layer is still not
consulted, so a technical superuser without the administrative flag remains
denied; and administrative authority still never grants professional authorship.
The query is one indexed primary-key lookup, so the per-mutation cost is
negligible.

### R4-B02 — stale PR verification summary corrected

PR #1's top verification table still showed the R2 totals (94 formatted files,
162 tests). It now reflects the R4 state (105 formatted files, 218 tests). The
historical R1/R2/R3 sections are retained unchanged, so the review trail stays
intact rather than being rewritten.

### Regression tests added (R4)

`identity/tests/test_admin_actor_persistence.py` — 19 tests covering:

| # | Requirement | Test |
|---|---|---|
| 1 | plain object denied | `test_plain_object_is_denied`, `test_none_is_denied` |
| 2 | fabricated admin-like object denied | `test_fabricated_admin_like_object_is_denied`, `test_simple_namespace_admin_is_denied` |
| 3 | unsaved Account with the flag denied | `test_unsaved_platform_admin_is_denied` |
| — | deleted row denied | `test_a_deleted_account_is_denied` |
| 4 | persisted ordinary Account denied | `test_persisted_ordinary_account_is_denied` |
| 5 | persisted inactive Platform Admin denied | `test_persisted_inactive_platform_admin_is_denied` |
| 6 | persisted active Platform Admin allowed | `test_persisted_active_platform_admin_is_allowed` |
| 7 | stale actor denied after row deactivated | `test_stale_actor_denied_after_its_row_is_deactivated` |
| 8 | stale actor denied after row demoted | `test_stale_actor_denied_after_its_row_is_demoted` |
| 9 | technical superuser without the flag denied | `test_superuser_without_platform_admin_is_denied`, `test_superuser_flag_alone_changes_nothing` |
| 10 | mutation services cannot run with such an actor | `TestMutationServicesInheritTheGate` (4 tests, incl. no grant created) |

A further test confirms the legitimate case is not broken by the extra lookup
(`test_stale_actor_allowed_while_its_row_stays_admin`), and
`test_platform_admin_flag_alone_changes_the_decision` pins that the
administrative flag the primitive owns is the one that decides.

The suite grew from 199 to 218 tests.

The tests were confirmed to detect the original defect: restoring the
duck-typed primitive made **10 of the 19 fail**, including every fabricated,
unsaved, deleted-row and stale-actor case. They are genuine regression tests.

### A pre-existing guard required a one-line docstring wording change

`identity/tests/test_account_creation_authorization.py::test_permissions_module_has_no_creation_shortcut`
asserts that `inspect.getsource(identity.permissions)` does not contain the
substring `is_superuser`. My first R4 docstring explained the layer separation
using that identifier, which the guard flagged. The behavioural guarantee is now
asserted properly instead — `test_superuser_flag_alone_changes_nothing` toggles
the flags and requires denial — and the docstring was reworded to describe the
layer without naming the field. The guard itself was left untouched. This is the
only change outside the R4 findings, and it is confined to a comment.

### Verification (R4)

| Check | Command | Result |
|---|---|---|
| Ruff lint | `ruff check .` | All checks passed |
| Ruff format | `ruff format --check .` | 105 files already formatted |
| Django check | `python manage.py check` | no issues (0 silenced) |
| Migration check | `makemigrations --check --dry-run` | No changes detected |
| Fresh-DB path | `POSTGRES_DB=nip_r4 manage.py migrate` | full chain applied OK |
| Tests | `pytest -q` | 218 passed |
| PostgreSQL | `connection.vendor` | `postgresql` |

No migration change was produced or required: the correction is confined to a
Python authority primitive, so the schema is untouched.

### Gate

The gate remains **HOLD — RE-REVIEW REQUIRED**. As in R1–R3, this executor does
not self-declare PASS.

## 14. Residual Correction Cycle R4.1 (R4-B01-R)

One residual case remained after R4 and is corrected here. No S01-I02 work was
started, no migration was produced, and no product surface was added.

### R4-B01-R — an unsaved Account could borrow a real Platform Admin's `pk`

R4 established that the actor must be a real `Account`, must have a `pk`, must
have a row, and must be an active Platform Admin in the *stored* row. One shape
slipped through:

```python
borrowed = Account(username="x", is_platform_admin=True, is_active=True)
borrowed.pk = real_admin.pk  # explicit PK, copied
```

`pk is not None` cannot distinguish "this instance is persisted" from "this
instance merely carries a primary key value". The `pk` check passed, the
database lookup then resolved to the genuine privileged row, and the mutation
was authorized — while the actor handed to the services was never a persisted
identity. Because services write provenance from the actor
(`granted_by_account=actor`), a fabricated instance could attribute its mutation
to the real admin's FK. This violates Actor Always Known and Identity Cannot Be
Borrowed.

The primitive now also requires the instance to be actually saved:

```python
if actor._state.adding:
    raise PermissionDeniedError(...)  # unsaved, even with an explicit pk
```

`_state.adding` is Django's own persisted/unsaved marker and is `True` on a
newly constructed instance regardless of any assigned `pk`. The existing
current-row lookup is kept unchanged, so stale deactivated/demoted actors are
still caught by stored state. Order matters: the `adding` check runs before the
lookup, so an unsaved instance never reaches authorization.

Confirmed at reproduction time, before the fix, that the defect was real and not
theoretical: a borrowed-`pk` instance was **allowed** through
`require_administrative_authority`, and `grant_capability` with it **created a
grant and recorded the real admin as `granted_by_account`**.

### Regression tests added (R4.1)

`identity/tests/test_unsaved_actor_explicit_pk.py` — 11 tests:

| Requirement | Test |
|---|---|
| 1–3 unsaved instance with the real admin's `pk` is denied | `test_borrowed_pk_instance_is_denied` |
| — same with matching flags/superuser/staff | `test_borrowed_pk_instance_is_denied_even_when_flags_match` |
| — unsaved instance without `pk` still denied | `test_unsaved_account_without_pk_is_denied` |
| — unsaved instance borrowing an ordinary account's `pk` denied | `test_unsaved_instance_with_borrowed_pk_of_ordinary_account_is_denied` |
| — unsaved instance borrowing a deactivated admin's `pk` denied | `test_unsaved_instance_borrowing_pk_of_deactivated_admin_is_denied` |
| 4 service `grant_capability` must not mutate | `test_grant_capability_rejects_a_borrowed_pk_actor` |
| 4 provenance must not name the real admin | `test_grant_capability_does_not_record_the_real_admin_as_issuer` |
| 4 service `create_person` must not mutate | `test_create_person_rejects_a_borrowed_pk_actor` |
| 5 genuine loaded admin still succeeds | `test_genuine_loaded_platform_admin_still_succeeds` |
| 5 genuine admin services still work end to end | `test_services_still_work_for_a_genuine_admin` |
| — a row-loaded instance modified in memory still passes | `test_detached_reload_is_not_treated_as_unsaved` |

The last two guard against over-tightening: the check targets Django's unsaved
state, not "the object is not the exact instance last saved".

The suite grew from 218 to 229 tests.

The tests were confirmed to detect the residual defect: removing the
`_state.adding` check made **5 of the 11 fail** — the denial test, the
flags-match variant, and all three service-mutation tests. They are genuine
regression tests.

### Verification (R4.1)

| Check | Command | Result |
|---|---|---|
| Ruff lint | `ruff check .` | All checks passed |
| Ruff format | `ruff format --check .` | 108 files already formatted |
| Django check | `python manage.py check` | no issues (0 silenced) |
| Migration check | `makemigrations --check --dry-run` | No changes detected |
| Fresh-DB path | `POSTGRES_DB=nip_r41 manage.py migrate` | full chain applied OK |
| Tests | `pytest -q` | 229 passed |
| PostgreSQL | `connection.vendor` / server version | `postgresql` / 17.11 |

No migration was produced or required: the residual correction is one Python
authority check, so the schema is untouched.

### Gate

The gate remains **HOLD — RE-REVIEW REQUIRED**. This executor does not
self-declare PASS.

## 15. Authority Closure — Correction Cycle R5 (R5-B01)

R4/R4.1 hardened the *administrative mutation* primitive. R5 closed the same
actor-identity class in the *generic professional* authority surface, which was a
pre-existing defect in the original permission foundation rather than a
regression from R4.1.

### R5-B01 — professional evaluation trusted the caller-supplied Account

`evaluate_capability` read `is_active` from the object it was handed and queried
`account.capability_grants` through that object's primary key. An unsaved
Account could copy a real professional Account's `pk` and `person_id` and
therefore:

```python
borrowed = Account(username="x", person=real_inspector.person, is_active=True)
borrowed.pk = real_inspector.pk
```

be evaluated against the real Account's stored grants — satisfying an OWN grant
(`granted_own`) or an ALL grant (`granted_all`). Confirmed at reproduction time
before the fix: both decisions came back **allowed**. The defect also reached the
inherited `has_capability` / `require_capability`, `can_perform_professional_work`,
`is_platform_admin`, and the identity read selectors `grants_for` /
`accounts_visible_to`.

### Correction — one persisted-actor resolver

`resolve_persisted_account(account) -> (Account | None, reason | None)` is now the
single authority source. It rejects, in order:

| Input | Reason code |
|---|---|
| not an `Account` instance | `invalid_actor` |
| `pk is None` **or** Django unsaved state (`_state.adding`) | `actor_not_persisted` |
| no matching database row | `actor_not_found` |

and otherwise returns the **current stored row** (`select_related("person")`).
Every authority helper and read selector routes through it:

- `evaluate_capability` evaluates the stored row's `is_active`,
  `is_platform_admin`, `person_id` and grants. A denial from the resolver is
  returned as an explainable `AuthorityDecision` with the stable reason code.
- `has_capability` and `require_capability` inherit this unchanged.
- `can_perform_professional_work` returns `False` for any malformed or inactive
  actor and enumerates the stored row's grants.
- `is_platform_admin` reports whether the stored row currently holds
  administrative authority — the flag **and** active state — and `False` for any
  malformed actor. Active state is included deliberately: reporting the raw flag
  would make this helper a weaker gate than `evaluate_capability(ACCOUNT_MANAGE)`
  and `require_administrative_authority`, inviting its misuse as an
  authorization check.
- `grants_for` / `accounts_visible_to` return empty querysets for a malformed
  actor instead of resolving rows through a borrowed primary key.
- `require_administrative_authority` now reuses the same resolver while
  **preserving its exact R1–R4.1 semantics** (same rejection conditions, same
  denial branches, same Arabic messages, same ordering guarantee that an unsaved
  actor never reaches the lookup).

The requested OWN-scope identity is still judged against the **stored**
`person_id`, so a caller mutating a loaded instance's `person_id` cannot widen or
redirect the scope. No delegation, no policy engine, no middleware or
authentication redesign, and no new capability was introduced.

### Regression tests added (R5)

`identity/tests/test_professional_actor_persistence.py` — **42 tests**:

| Requirement | Coverage |
|---|---|
| 1 borrowed `pk`+`person_id` cannot satisfy an OWN grant | `TestProfessionalOwnGrantCannotBeBorrowed` (6) |
| 2 borrowed identity cannot satisfy an ALL grant | `TestProfessionalAllGrantCannotBeBorrowed` (3) |
| 3 `require_capability` raises for a fabricated actor | `TestRequireCapabilityRaisesForFabricatedActor` (3) |
| 4 stale actor denied after stored deactivation | `TestStaleActorIsDenied` (5) |
| 5 caller-side `person_id` mutation cannot change OWN scope | `TestCallerPersonRebindingCannotChangeOwnScope` (3) |
| 6 genuine persisted Account still succeeds | `TestGenuineAccountsStillWork` (3) |
| 7 admin without a professional grant still fails | `TestAdminStatusIsStillNotProfessionalAuthorship` (3) |
| 8/9 `can_perform_professional_work` false/true cases | `TestCanPerformProfessionalWork` (4) |
| resolver contract and stable reason codes | `TestResolverContract` (4) |
| read selectors resolve the persisted identity | `TestSelectorsResolvePersistedIdentity` (7) |
| 10 all R1–R4.1 authority regressions remain green | full suite |

Suite grew from 229 to **271** tests.

Revert-proof: restoring the pre-fix primitive (trusting the caller-supplied
instance) failed **19 of the 42** new tests, including the explicit OWN and ALL
borrowing cases which then returned `allowed=True`. They are genuine regression
tests.

### Verification (R5)

| Check | Command | Result |
|---|---|---|
| Ruff lint | `ruff check .` | All checks passed |
| Ruff format | `ruff format --check .` | 111 files already formatted |
| Django check | `python manage.py check` | no issues (0 silenced) |
| Migration check | `makemigrations --check --dry-run` | No changes detected |
| Fresh-DB path | `POSTGRES_DB=nip_r5 manage.py migrate` | full chain applied OK |
| Tests | `pytest -q` | 271 passed |
| PostgreSQL | `connection.vendor` / server version | `postgresql` / 17.11 |

No migration was produced or required: the correction is confined to Python
authority primitives, so the schema is untouched.

### Gate

The gate remains **HOLD — RE-REVIEW REQUIRED**. This executor does not
self-declare PASS.

