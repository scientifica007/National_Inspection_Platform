# OpenHands Executor Prompt — S01-I01

- Target tool: **OpenHands Cloud**
- Authorized increment: **S01-I01 only**
- Repository: `scientifica007/National_Inspection_Platform`
- Base branch: `main`
- Required working branch: `build/slice-01`

## Prompt to paste into OpenHands

You are the controlled implementation agent for **National Inspection Platform**.

Repository:
`scientifica007/National_Inspection_Platform`

The repository is currently documentation-first and M0 is complete.

Your authorization is intentionally narrow:

**Implement S01-I01 — Project Skeleton + Identity/Authority Foundation only.**

Do NOT implement S01-I02 or any later increment.

### 1. Mandatory first actions

Before changing any file:

1. Confirm the repository is `scientifica007/National_Inspection_Platform`.
2. Confirm the starting branch is `main`.
3. Read:
   - `docs/DOCUMENTATION_INDEX.md`
   - `docs/PROJECT_STATE.md`
   - `docs/INVARIANTS.md`
   - `docs/PRODUCT_VISION.md`
   - `docs/DOMAIN_MODEL.md`
   - `docs/AUTHORITY_MODEL.md`
   - `docs/ARCHITECTURE_PRINCIPLES.md`
   - `docs/ENGINEERING_CONVENTIONS.md`
   - `docs/SECURITY_AND_DATA_GOVERNANCE.md`
   - `docs/REPOSITORY_GOVERNANCE.md`
   - `docs/CONTROLLED_IMPLEMENTATION_CYCLE.md`
   - `docs/SLICE_01_INCREMENT_PLAN.md`
   - `docs/AI_EXECUTOR_SPEC_01.md`
   - `decisions/ADR-0001-modular-monolith-replaceable-interfaces.md`
   - `decisions/ADR-0002-initial-stack.md`
   - `decisions/ADR-0003-admin-professional-authorship.md`
4. Create and switch to:
   `build/slice-01`
5. Do not make implementation commits on `main`.

If the branch already exists, verify its state before using it.

### 2. Clean-slate rule

Do not inspect, read, compare, copy, cherry-pick, import or reuse code, architecture, migrations, templates, tests, databases or implementation details from:

- Inspector_Website_001
- Inspector_Website_002
- Inspector_Website_003
- Inspector_Website_004
- Inspector_Website_005

Those repositories are outside the allowed source of truth.

### 3. Exact scope of S01-I01

Implement only:

#### Project foundation
- Python 3.12 compatible project.
- Django 5.2 LTS.
- PostgreSQL as canonical database configuration.
- environment-based database/settings configuration.
- safe `.env.example` with fake/non-secret values only.
- `.gitignore` suitable for Python/Django/local secrets.
- Django project/config package.

#### Identity
Create only the minimum identity foundation needed now:

- `Person`
- custom Django User/Account model from day one.
- one-to-one Person ↔ Account mapping for this slice.
- active/inactive semantics as documented.
- no Position hierarchy implementation yet unless strictly required by accepted S01-I01 docs.

#### Authority
Implement minimal `CapabilityGrant` for S01-I01:

- capability code.
- scope kind limited to:
  - `OWN`
  - `ALL`
- validity timestamps if required by the accepted data model.
- grant source / granted-by information as documented.
- revoked state/timestamp where specified.
- delegable field where specified.

Do NOT build the future generic scope engine.

#### Admin separation
Enforce the accepted rule:

**Admin authority does not itself grant professional authorship.**

Requirements:
- Admin may have broad administrative access.
- Admin must not gain an impersonation mechanism.
- Account identity and Person identity remain explicit.
- no "act as inspector" shortcut.
- no code path that treats `is_platform_admin` as proof of professional authorship.

#### Authentication
- login/logout.
- minimal authenticated landing/dashboard shell.
- unauthorized users redirected/denied appropriately.
- CSRF remains enabled.

#### Presentation shell
Build only a minimal reusable Arabic RTL shell:

- `dir="rtl"`.
- Arabic-first layout.
- basic navigation/header sufficient for S01-I01.
- central CSS Design Tokens using custom properties.
- reusable small components/partials where useful.
- semantic HTML.
- no large visual design exercise yet.
- no business rules implemented only in templates/JavaScript.

The shell should be clean and usable, but visual perfection is deferred.

#### Quality foundation
- pytest + pytest-django.
- Ruff.
- CI workflow for lint/tests.
- Django system checks.
- PostgreSQL test path where practical in CI.
- migrations.
- tests required by the S01-I01 gate.

### 4. Required S01-I01 tests

At minimum test:

1. custom Account/User is actually the configured Django user model.
2. Person and Account relation works.
3. authentication works.
4. unauthenticated protected access is rejected/redirected.
5. capability evaluation for `OWN` and `ALL` works for the minimal supported use cases.
6. expired/revoked grants do not authorize when those fields are implemented.
7. Admin administrative status does not create a professional-authorship capability.
8. there is no impersonation path/API/helper.
9. server-side permission primitives are testable independently of the UI.
10. Django system checks pass.
11. migrations are consistent.
12. no future modules such as missions/teams/reporting are created.

### 5. Architecture constraints

Follow the accepted Modular Monolith.

For this increment, create only what is necessary.

Likely bounded code area:
- `config/`
- `identity/`
- shared `templates/`
- shared `static/`
- tests/CI/config files

Do NOT create empty placeholder apps for:
- institutions
- knowledge
- visits
- records
- audit
- missions
- teams
- reporting

unless a current S01-I01 requirement absolutely requires one. S01-I01 should remain minimal.

Keep:
- HTTP/view logic thin.
- permission logic explicit and reusable.
- domain/application rules outside templates/JavaScript.
- no circular dependencies.
- no speculative generic framework.

### 6. Database rules

- PostgreSQL is canonical.
- SQLite-only success is insufficient as final evidence.
- create small, reviewable migrations.
- do not create destructive migrations.
- do not commit any database file.

If OpenHands environment cannot run PostgreSQL locally:
- still configure the project correctly for PostgreSQL,
- run every other available test,
- clearly report the exact limitation,
- do not falsely claim PostgreSQL verification passed.

### 7. Security/data rules

This repository is public.

Do not commit:
- real names/data from inspection work.
- real credentials.
- API keys/tokens.
- production secrets.
- real evidence/documents.
- database dumps.

Use only synthetic demo/test data.

### 8. Explicitly out of scope

Do NOT implement:

- Institutions.
- Checklists.
- Visits.
- Findings.
- Recommendations.
- Finalization.
- Snapshots.
- Amendment.
- Missions.
- Assignments.
- Teams.
- Geography.
- Minister dashboard.
- national dashboard.
- reports/datasets.
- notifications.
- REST API.
- mobile native app.
- AI features.
- generic workflow/rule engine.
- microservices.

These belong to later controlled increments.

### 9. Verification before stopping

Run and report exact commands/results for all applicable checks, including:

- Python/Django version.
- Ruff.
- pytest.
- Django `check`.
- migration consistency check.
- PostgreSQL-backed tests if environment supports them.

Inspect `git status` and confirm no secrets/database artifacts are present.

### 10. Git/PR behavior

When S01-I01 is complete:

1. commit the implementation on `build/slice-01`.
2. push the branch.
3. if OpenHands has permission, open a **DRAFT pull request** from `build/slice-01` to `main`.
4. DO NOT merge it.
5. DO NOT enable auto-merge.
6. DO NOT start S01-I02.

The PR title should clearly contain:

`S01-I01 — Project Skeleton + Identity/Authority Foundation`

### 11. Required final report

Stop after S01-I01 and provide a concise evidence report containing exactly:

- branch name.
- final commit SHA.
- draft PR URL/number if created.
- files/apps created.
- migrations created.
- implemented capabilities.
- exact tests/checks run and results.
- PostgreSQL verification status.
- any deviations from the spec.
- any unresolved risks/limitations.
- confirmation that no S01-I02 work was performed.
- confirmation that no previous Inspector_Website repository was inspected/reused.

Then stop and wait for independent review.

Do not self-authorize the next increment.

### 12. Stop conditions

Stop implementation and report the issue instead of guessing if:

- repository documents truly conflict.
- a required domain policy is missing.
- an implementation choice would weaken an invariant.
- a destructive data decision becomes necessary.
- you believe a future feature must be implemented to complete S01-I01.

The correct outcome in such a case is a documented question, not speculative code.
