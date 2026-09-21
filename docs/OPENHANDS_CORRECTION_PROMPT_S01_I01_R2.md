# OpenHands Correction Prompt — S01-I01 Review Cycle 2

- Target executor: **OpenHands Cloud**
- PR: **#1**
- Branch: `build/slice-01`
- Reviewed head: `0485d8cc6a0b4d4d673512774fbdcc6e0f709fac`
- Gate: **HOLD — CORRECTION REQUIRED (R2)**
- Authorization: **correction-only; S01-I02 remains forbidden**

## Prompt to paste into OpenHands

Continue the controlled correction cycle for **National Inspection Platform**.

Repository:
`scientifica007/National_Inspection_Platform`

PR:
`#1`

You are NOT authorized to start S01-I02.

### 1. Sync first

Fetch current `origin/main`, switch to `build/slice-01`, and merge current `origin/main` into the branch without rewriting/discarding the existing implementation history.

Then read:
- `docs/DOCUMENTATION_INDEX.md`
- `docs/PROJECT_STATE.md`
- `docs/INVARIANTS.md`
- `docs/AUTHORITY_MODEL.md`
- `docs/SECURITY_AND_DATA_GOVERNANCE.md`
- `docs/REVIEW_AND_CHANGE_POLICY.md`
- `docs/gates/S01-I01_CORRECTION_R2.md`
- the latest independent review on PR #1.

### 2. Correct only R2-B01 through R2-B05

#### R2-B01 — authorize application account creation
`identity/services.py::create_account` is currently an ungated application service and can set `is_platform_admin=True`.

Required:
- product/application account creation must require an active real Platform Admin actor;
- non-admin cannot create ordinary accounts or Platform Admin accounts through this service;
- inactive Platform Admin cannot create accounts;
- active Platform Admin may create ordinary or Platform Admin accounts;
- bootstrap/system-operator mechanics must remain separate and must not weaken the application service.

Do not create a product account-management UI in this pass.

Add regression tests.

#### R2-B02 — freeze Account → Person binding after creation
The Person may be selected at Account creation, but an existing Account must not be routinely rebound to another Person through Django Admin/application forms.

Required:
- keep `person` available in the add form;
- make it read-only/immutable in the change path;
- add regression coverage.

Do not build a generic identity-history mechanism now.

#### R2-B03 — make CapabilityGrant Django Admin read-only
The technical admin currently exposes an add/change/delete surface that is either invalid with the required readonly issuer or bypasses service/history semantics.

For S01-I01:
- allow list/detail inspection;
- disable add;
- disable domain changes;
- disable delete.

Do not build a new grant-management product UI.

Add tests for admin permissions.

#### R2-B04 — preserve grant history when recipient account is deleted
`CapabilityGrant.account` currently uses CASCADE.

Required:
- change to a history-preserving policy such as PROTECT;
- update the clean initial migration consistently;
- add tests proving an Account with grant history cannot be deleted through the normal ORM delete path while referenced.

Account deactivation remains the normal lifecycle operation.

#### R2-B05 — correct stale documentation
Update:
- `docs/IMPLEMENTATION_NOTES_S01_I01.md` so it no longer says mutations require an `account.manage` grant;
- PR #1 body so it no longer claims `docs/S01_I01_EXPECTED_OUTPUTS.md` is missing.

Keep all current R1 evidence and accurately add R2 evidence.

### 3. Do not broaden scope

Do NOT implement:
- S01-I02 institutions;
- new product Admin UI;
- delegation engine;
- audit module;
- missions/teams/visits/checklists;
- future modules or APIs.

### 4. Verification

Run at minimum:
- `ruff check .`
- `ruff format --check .`
- `python manage.py check`
- `python manage.py makemigrations --check --dry-run`
- full `pytest -q` against PostgreSQL;
- fresh migration path on PostgreSQL;
- targeted regression tests for all R2 blockers;
- CI on pushed head.

Inspect:
- git status;
- no secrets/database artifacts;
- no future modules.

### 5. Gate/docs

Update `docs/gates/S01-I01_GATE.md` with R2 correction evidence.

Do NOT claim PASS.

End state must be:

`HOLD — RE-REVIEW REQUIRED`

No PASS checkpoint.

### 6. Git/PR

Continue on the same `build/slice-01` branch and same draft PR #1.

Do not merge.
Do not enable auto-merge.
Do not start S01-I02.

### 7. Final report

Report:
- current main SHA integrated;
- merge/sync commit;
- correction commit(s);
- final head SHA;
- exact change for R2-B01…R2-B05;
- migration state;
- new tests and full test count;
- PostgreSQL/CI results;
- scope confirmation.

Then STOP and await independent re-review.
