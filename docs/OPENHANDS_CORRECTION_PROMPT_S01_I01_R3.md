# OpenHands Correction Prompt — S01-I01 Review Cycle 3

- Target executor: **OpenHands Cloud**
- PR: **#1**
- Branch: `build/slice-01`
- Reviewed head: `b94eb38b0ce61e6efed16cc26a9466e2ddd56f9c`
- Gate: **HOLD — CORRECTION REQUIRED (R3)**
- Authorization: **correction-only; S01-I02 remains forbidden**

## Prompt to paste into OpenHands

Continue the controlled correction cycle for **National Inspection Platform**.

Repository:
`scientifica007/National_Inspection_Platform`

PR:
`#1`

You are NOT authorized to start S01-I02.

### 1. Sync first

Fetch current `origin/main`, switch to `build/slice-01`, and merge current `origin/main` into the branch without rewriting/discarding existing implementation history.

Then read:
- `docs/DOCUMENTATION_INDEX.md`
- `docs/PROJECT_STATE.md`
- `docs/INVARIANTS.md`
- `docs/AUTHORITY_MODEL.md`
- `docs/SECURITY_AND_DATA_GOVERNANCE.md`
- `docs/REVIEW_AND_CHANGE_POLICY.md`
- `docs/gates/S01-I01_CORRECTION_R3.md`
- the latest independent review on PR #1.

### 2. Correct only R3-B01 through R3-B03

#### R3-B01 — make bootstrap Person+Account atomic

Current issue:
`identity.bootstrap.bootstrap_platform_admin` saves Person before Account creation. A later Account failure can leave an orphan Person.

Required:
- make the bootstrap operation atomic;
- preferably reuse `AccountManager`'s existing automatic Person creation path instead of duplicating Person creation;
- successful bootstrap still creates `is_platform_admin=True`;
- bootstrap must not grant professional capability.

Regression tests:
- duplicate/failing bootstrap leaves Person count unchanged;
- successful bootstrap creates exactly one linked Person and Account;
- no professional grant is created.

#### R3-B02 — authorize application Person creation

Current issue:
`identity.services.create_person` is an application mutation with no actor/authorization.

Required:
- either require an active real Platform Admin actor for standalone Person creation; OR
- remove/reclassify the command if no S01-I01 application use case requires standalone Person creation.

If retained, tests must prove:
1. non-admin denied;
2. inactive Platform Admin denied;
3. active Platform Admin allowed.

Do not add a new capability/delegation engine.

Update test factories/call sites cleanly so tests that merely need synthetic Persons do not misuse a gated product service.

#### R3-B03 — document first Platform Admin bootstrap

Current issue:
README tells operators to run `createsuperuser`, but Django superuser and application Platform Admin are deliberately distinct. R2 added a bootstrap boundary but the setup path does not explain how to create the first Platform Admin.

Required:
- clearly explain the difference between Django technical superuser and Platform Admin;
- document a safe operator-controlled first-Platform-Admin bootstrap procedure;
- no product HTTP route;
- no real password/secret in source or examples.

A small Django management command is acceptable if it stays in the technical/deployment boundary and does not broaden product scope. A documented operator procedure using the existing bootstrap module is also acceptable if safe and reproducible.

### 3. Do not broaden scope

Do NOT implement:
- S01-I02 institutions;
- product account-management UI;
- delegation engine;
- audit module;
- visits/checklists/missions/teams;
- future APIs/modules.

### 4. Verification

Run at minimum:
- `ruff check .`
- `ruff format --check .`
- `python manage.py check`
- `python manage.py makemigrations --check --dry-run`
- fresh PostgreSQL migration path;
- targeted R3 regression tests;
- full `pytest -q` against PostgreSQL;
- CI on the pushed head.

Inspect git status and confirm:
- no secrets/database artifacts;
- no future modules;
- PR remains draft/unmerged;
- auto-merge disabled.

### 5. Gate/docs

Update `docs/gates/S01-I01_GATE.md` and implementation notes with R3 evidence.

Do NOT claim PASS.

End state:
`HOLD — RE-REVIEW REQUIRED`

No PASS checkpoint.

### 6. Git/PR

Continue on the same `build/slice-01` branch and PR #1.

Do not merge.
Do not enable auto-merge.
Do not start S01-I02.

### 7. Final report

Report:
- current main SHA integrated;
- merge/sync commit;
- correction commit(s);
- final head SHA;
- exact change for R3-B01…R3-B03;
- migration state;
- new regression tests and total suite count;
- PostgreSQL/CI evidence;
- scope confirmation.

Then STOP and await independent re-review.
