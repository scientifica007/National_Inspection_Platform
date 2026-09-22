# Codex Correction Prompt — S01-I02 Review Cycle R1

- Executor: **Codex**
- Increment: **S01-I02 — Local Institutions**
- PR: **#2**
- Branch: `build/s01-i02`
- Reviewed head: `d5db159a00e15349192e09c6d4be5bd52bd2c760`
- Gate: **HOLD — CORRECTION REQUIRED (R1)**
- Authorization: **correction-only; S01-I03 remains forbidden**

## 1. Sync first

Fetch current `origin/main` and merge it into `build/s01-i02` without rewriting or discarding implementation history.

Then read:
- `docs/DOCUMENTATION_INDEX.md`
- `docs/PROJECT_STATE.md`
- `docs/INVARIANTS.md`
- `docs/AUTHORITY_MODEL.md`
- `docs/LIFECYCLE_PROFILES.md`
- `docs/S01_I02_EXPECTED_OUTPUTS.md`
- `docs/gates/S01-I02_CORRECTION_R1.md`
- the latest independent review on PR #2.

## 2. Correct only S01-I02-R1-B01 and B02

### B01 — persisted Institution target must be authoritative

Current problem:
actor identity is re-resolved correctly, but Institution permission/mutation code trusts the caller-supplied Institution instance for ownership/lifecycle and then saves/deletes by its PK.

Required:
- add one narrow institutions-layer persisted-target resolver;
- reject non-Institution input;
- reject `pk=None`;
- reject Django unsaved/adding instances, including explicit borrowed PK;
- reject missing rows;
- re-read current stored Institution state;
- for update/archive/delete, resolve the row inside the transaction and use `select_for_update()` or an equivalently clear row-lock/current-state pattern;
- authorize stored ownership and current stored lifecycle;
- mutate/delete the stored row, never the caller instance;
- harden `can_read_institution` and `can_mutate_institution` against borrowed/stale Institution objects;
- keep the design local/simple; no generic repository/policy engine.

Regression tests must prove at minimum:
1. fabricated unsaved Institution borrowing another owner's PK cannot update;
2. cannot archive;
3. cannot delete;
4. victim row remains unchanged;
5. stale instance cannot update after stored row was archived;
6. stale instance cannot delete after stored row was archived;
7. caller-side owner field mutation cannot redirect authority;
8. missing/deleted row is denied cleanly;
9. genuine owner + genuine active stored Institution still succeeds.

Also test the read/mutation predicates themselves against a borrowed target object.

### B02 — Django admin must not bypass Institution domain services

Current problem:
plain `InstitutionAdmin` exposes add/change/delete and writable owner/creator/lifecycle fields.

Required:
- preferred: keep Institution registered as inspection-only;
- all Institution fields read-only in technical admin;
- `has_add_permission = False`;
- `has_change_permission = False`;
- `has_delete_permission = False`;
- alternatively unregister Institution entirely if simpler.

Add regression tests proving a Django superuser cannot add/change/delete Institution through ModelAdmin.

Do not build a new Platform Admin product UI.

## 3. Preserve everything already correct

Do not weaken:
- S01-I01 persisted-actor authority;
- owner/other/Admin visibility;
- Platform Admin read-only product visibility;
- lifecycle constraint;
- `ProtectedError -> InstitutionRetentionError`;
- no-unarchive rule;
- CSRF/POST mutation behavior.

The create-without-read redirect edge noted by the reviewer is **non-blocking**. Do not redefine capability implication during this correction.

## 4. No scope expansion

Do NOT:
- start S01-I03;
- add knowledge/checklists/visits/records/audit;
- add ownership transfer;
- add unarchive;
- add new capability taxonomy;
- add REST API/SPA/background jobs/microservices;
- add a generic object repository/policy framework.

No schema change is expected. If a migration appears, stop and explain why before proceeding.

## 5. Verification

Run:
- focused B01/B02 regression tests;
- full institutions tests;
- all S01-I01 regressions;
- `ruff check .`;
- `ruff format --check .`;
- `python manage.py check`;
- `python manage.py makemigrations --check --dry-run`;
- full `pytest -q` against PostgreSQL;
- fresh empty PostgreSQL migration chain;
- CI on exact pushed head.

## 6. Git / PR

Continue on:
`build/s01-i02`

Keep PR #2:
- draft;
- open;
- unmerged;
- auto-merge disabled.

Update:
- `docs/IMPLEMENTATION_NOTES_S01_I02.md`
- `docs/gates/S01-I02_GATE.md`
- PR body with correction evidence.

Do not edit reviewer-owned state to claim PASS.
Do not create a PASS checkpoint.
Do not authorize S01-I03.

End gate:

`HOLD — RE-REVIEW REQUIRED`

## 7. Final report

Report:
- current main SHA integrated;
- sync commit;
- correction commit(s);
- final head SHA;
- exact persisted-Institution design;
- exact Django-admin hardening;
- new regression tests;
- full suite count;
- PostgreSQL/fresh migration evidence;
- CI run/result;
- scope confirmation.

Then STOP for independent re-review.
