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

