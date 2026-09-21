# OpenHands Correction Prompt — S01-I01 Residual R4.1

- Target executor: **OpenHands Cloud**
- PR: **#1**
- Branch: `build/slice-01`
- Reviewed head: `ead46986a3d220ee69e3f18688339000ae7491a1`
- Gate: **HOLD — MINIMAL RESIDUAL CORRECTION REQUIRED (R4.1)**
- Authorization: **one residual authority fix only; S01-I02 remains forbidden**

## Prompt to paste into OpenHands

Continue the controlled correction cycle for **National Inspection Platform**.

Repository:
`scientifica007/National_Inspection_Platform`

PR:
`#1`

You are NOT authorized to start S01-I02.

### 1. Sync first

Fetch current `origin/main`, switch to `build/slice-01`, and merge current `origin/main` without rewriting or discarding existing history.

Then read:
- `docs/INVARIANTS.md`
- `docs/AUTHORITY_MODEL.md`
- `docs/SECURITY_AND_DATA_GOVERNANCE.md`
- `docs/gates/S01-I01_CORRECTION_R4_1.md`
- the latest independent review on PR #1.

### 2. Correct the residual R4-B01 case only

Current R4 code rejects non-Accounts, `pk=None`, missing rows, inactive rows, and demoted rows.

Residual defect:
an **unsaved Account with an explicit PK copied from a real Platform Admin** is still unsaved, but passes the current `pk is not None` check and then authorizes because the database lookup finds the real admin row.

Required:
- reject Account instances that are still in Django's unsaved/adding model state even when an explicit PK is present;
- keep the existing current-row lookup for stale deactivated/demoted actors;
- do not redesign authentication;
- do not add delegation, capability types, or generic auth abstractions.

Focused regression tests:
1. persisted active Platform Admin exists;
2. construct a *different unsaved Account instance* with `pk=real_admin.pk`;
3. `require_administrative_authority` must deny it;
4. a representative service (e.g. `grant_capability` or `create_person`) must not mutate using it;
5. a genuine normally loaded Platform Admin still succeeds.

Use a simple explicit check. A Django model instance with copied PK must not be treated as the authenticated persisted actor merely because that PK resolves to a privileged row.

### 3. Scope

Do NOT:
- start S01-I02;
- change migrations;
- add UI;
- add delegation/audit/future modules;
- refactor unrelated code;
- weaken the current persisted-state checks.

If a migration appears, stop and report.

### 4. Verification

Run:
- focused R4.1 tests;
- `ruff check .`;
- `ruff format --check .`;
- `python manage.py check`;
- `python manage.py makemigrations --check --dry-run`;
- full PostgreSQL `pytest -q`;
- CI on pushed head.

### 5. Gate

Update the implementation/gate evidence only.

Do NOT self-declare PASS.

End state:
`HOLD — RE-REVIEW REQUIRED`

No PASS checkpoint.

### 6. Security

Do not print or reproduce authenticated remote URLs, tokens, or secret values.

### 7. Final report

Report:
- main SHA integrated;
- sync commit;
- correction commit;
- final head SHA;
- exact explicit-PK-unsaved fix;
- focused test names;
- final suite count;
- PostgreSQL/CI evidence;
- scope confirmation.

Then STOP for independent re-review.
