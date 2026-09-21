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
- commit: recorded in the PR after push
- files/modules changed: `config/`, `identity/`, `templates/`, `static/`,
  `tests/`, `.github/workflows/ci.yml`, `manage.py`, `pyproject.toml`,
  `requirements*.txt`, `.gitignore`, `.env.example`,
  `docs/IMPLEMENTATION_NOTES_S01_I01.md`, this gate record
- migrations: `identity/migrations/0001_initial.py`
- notes: see `docs/IMPLEMENTATION_NOTES_S01_I01.md`

## Review Findings

### Blocking
- Not yet reviewed. Independent review is the next required step
  (`docs/AI_REVIEWER_PROMPT_01.md`).

### Non-blocking
- To be recorded after review.

### Architecture/Domain observations
- To be recorded after review.

## Corrections
- None yet.

## Re-verification
- [ ] all blocking findings resolved
- [ ] regression tests added
- [ ] relevant checks pass

## Checkpoint Decision

`HOLD — REVIEW REQUIRED`

The increment is implemented and self-verified, but a checkpoint decision may
only be recorded after an independent review pass. No `PASS — NEXT INCREMENT
ALLOWED` decision is claimed here, and S01-I02 is not started.

## Next Increment
Not defined. `S01-I02` remains unauthorized until S01-I01 is explicitly marked
`PASS — NEXT INCREMENT ALLOWED` by the review/maintainer process.
