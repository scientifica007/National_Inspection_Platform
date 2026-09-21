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
Administrative commands require `account.manage` through the same primitives,
so an inspector cannot escalate by granting themselves capabilities.

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
automatically hold application administrative authority (`account.manage`),
and never holds professional authorship. Conversely, `is_platform_admin` grants
`account.manage` but not `/admin/` access.

Known limitation for later increments: `/admin/` editing is not yet covered by
`AuditEvent`, because the `audit` module belongs to a later increment. Until
audit exists, technical-plane mutations are not traceable in application
history. This is recorded as a risk, not solved speculatively here.

## 9. Deliberately not implemented

No `institutions`, `knowledge`, `visits`, `records`, `audit`, `missions`,
`teams`, `geography`, `organization` or `reporting` app exists — not even as an
empty placeholder. A test asserts that neither `INSTALLED_APPS` nor the app
registry contains any deferred module.

