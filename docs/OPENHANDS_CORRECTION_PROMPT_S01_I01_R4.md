# OpenHands Correction Prompt — S01-I01 Review Cycle 4

- Target executor: **OpenHands Cloud**
- PR: **#1**
- Branch: `build/slice-01`
- Reviewed head: `cd58b8107090abc1a68e3280e72f6bc6d2fcd10f`
- Gate: **HOLD — CORRECTION REQUIRED (R4)**
- Authorization: **minimal correction-only; S01-I02 remains forbidden**

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
- `docs/gates/S01-I01_CORRECTION_R4.md`
- the latest independent review on PR #1.

### 2. Correct R4-B01 only in code

#### R4-B01 — require a real persisted Platform Admin actor

Current issue:
`identity.permissions.require_administrative_authority` trusts duck-typed attributes:

`is_platform_admin` and `is_active`.

That means a fabricated object or unsaved Account carrying those attributes can satisfy the authorization primitive even though no persisted acting identity exists.

Required:
- reject non-`Account` actors;
- reject unsaved Account actors;
- verify the current persisted Account row is active and has `is_platform_admin=True`;
- do not trust only the caller object's in-memory flags;
- a Django technical superuser without `is_platform_admin` remains denied;
- preserve separation between Admin authority and professional authorship;
- do not implement delegation or a new generic auth engine.

Prefer a small explicit implementation at the existing authority primitive.

Regression tests must cover at minimum:
1. plain object denied;
2. fabricated admin-like object denied;
3. unsaved Account with `is_platform_admin=True` denied;
4. persisted ordinary Account denied;
5. persisted inactive Platform Admin denied;
6. persisted active Platform Admin allowed;
7. stale in-memory actor denied after its DB row is deactivated;
8. stale in-memory actor denied after its DB row is demoted from Platform Admin;
9. Django superuser without Platform Admin denied;
10. representative mutation services cannot execute with fabricated/unsaved actor.

Do not add a new capability or delegation surface.

### 3. R4-B02 — correct stale PR summary only

The top PR verification table still contains older R2 values.

Update the PR body so the current summary reflects the latest verified totals after R4.

Keep historical R1/R2/R3 sections intact.

### 4. Credential handling

The reviewer detected an access-token-like credential in the supplied terminal transcript.

Do NOT:
- reproduce that token in commits, PR text, docs, tests, or final reports;
- print authenticated remote URLs;
- include secret values in diagnostic output.

Use sanitized remote output only.

The repository itself must remain secret-free.

### 5. Do not broaden scope

Do NOT implement:
- S01-I02;
- product account-management UI;
- delegation;
- audit;
- future modules;
- unrelated refactors.

### 6. Verification

Run at minimum:
- `ruff check .`
- `ruff format --check .`
- `python manage.py check`
- `python manage.py makemigrations --check --dry-run`
- targeted R4 regression tests;
- full `pytest -q` against PostgreSQL;
- CI on pushed head.

No migration change is expected. If a migration appears, stop and explain why before proceeding.

### 7. Gate/docs

Update implementation notes and `docs/gates/S01-I01_GATE.md` with R4 evidence.

Do NOT claim PASS.

End state:
`HOLD — RE-REVIEW REQUIRED`

No PASS checkpoint.

### 8. Git/PR

Continue on the same `build/slice-01` branch and PR #1.

Do not merge.
Do not enable auto-merge.
Do not start S01-I02.

### 9. Final report

Report:
- current main SHA integrated;
- merge/sync commit;
- correction commit(s);
- final head SHA;
- exact R4-B01 correction;
- R4 regression tests;
- final full suite count;
- PostgreSQL/CI evidence;
- confirmation that no credential was reproduced;
- scope confirmation.

Then STOP and await independent re-review.
