# OpenHands Correction Prompt — S01-I01 Review Cycle 1

- Target executor: **OpenHands Cloud**
- PR: **#1**
- Branch: `build/slice-01`
- Reviewed head: `0b3fe700997cfd607bce357f590c76cbde179ae8`
- Gate: **HOLD — CORRECTION REQUIRED**
- Authorization: **correction-only; S01-I02 remains forbidden**

## Prompt to paste into OpenHands

You are continuing the controlled implementation of:

**National Inspection Platform**

Repository:
`scientifica007/National_Inspection_Platform`

Pull Request:
`#1 — S01-I01 — Project Skeleton + Identity/Authority Foundation`

Current reviewed implementation head:
`0b3fe700997cfd607bce357f590c76cbde179ae8`

Independent review has completed.

Gate decision:

**HOLD — CORRECTION REQUIRED**

Your authorization is now:

**CORRECT S01-I01 ONLY.**

Do NOT start S01-I02.
Do NOT broaden scope.
Do NOT merge PR #1.
Do NOT enable auto-merge.

==================================================
1. FIRST: SYNC WITH CURRENT MAIN
==================================================

The implementation branch was created from an older main snapshot and is behind current main.

Before editing code:

1. fetch origin.
2. inspect current `origin/main`.
3. switch to `build/slice-01`.
4. integrate current `origin/main` into the branch WITHOUT discarding the existing S01-I01 implementation commits.

Prefer a normal merge from `origin/main` into `build/slice-01` to preserve auditability and avoid rewriting reviewed history.

If conflicts occur:
- preserve the current canonical documentation from main.
- preserve valid implementation-specific content from the branch.
- do not delete newer governance/review documents.
- do not weaken any invariant merely to resolve a conflict.

After syncing, re-read:
- `docs/DOCUMENTATION_INDEX.md`
- `docs/PROJECT_STATE.md`
- `docs/INVARIANTS.md`
- `docs/AUTHORITY_MODEL.md`
- `docs/SECURITY_AND_DATA_GOVERNANCE.md`
- `docs/ENGINEERING_CONVENTIONS.md`
- `docs/REVIEW_AND_CHANGE_POLICY.md`
- `docs/CORRECTION_CYCLE_TEMPLATE.md`
- `docs/S01_I01_EXPECTED_OUTPUTS.md`
- the independent review on PR #1.

==================================================
2. CORRECTION SCOPE
==================================================

Correct ONLY the blocking findings B-01 through B-07 from the independent review.

Also address N-01 if it is trivial and local.

Do NOT use this correction pass to add future features.

==================================================
3. B-01 — BLOCK ADMINISTRATIVE SELF-ESCALATION
==================================================

Severity: CRITICAL

Current problem:

A non-platform-admin Account can potentially receive a CapabilityGrant for:

`account.manage`

and then use the current service layer to grant itself or others arbitrary capabilities/scopes.

This bypasses:
- Scope semantics.
- delegable semantics.
- least privilege.
- accepted Delegation rules.

Advanced delegation is DEFERRED.

Therefore do NOT build a delegation engine now.

Required S01-I01 correction:

- only a real `is_platform_admin=True` account may perform S01-I01 account-management mutation commands:
  - grant_capability
  - revoke_capability
  - deactivate_account
  - any equivalent administrative mutation introduced in this increment.

- an `account.manage` CapabilityGrant on a non-admin account MUST NOT authorize those administrative mutation commands in S01-I01.

- preserve the broader conceptual model for future explicit delegation, but do not partially implement it now.

- do not let a non-admin self-escalate by receiving/granting account.manage.

Required regression tests at minimum:

1. non-admin + `account.manage` grant cannot grant itself a professional capability.
2. non-admin + `account.manage` grant cannot grant another account a capability.
3. non-admin + `account.manage` grant cannot revoke a grant.
4. non-admin + `account.manage` grant cannot deactivate another account.
5. platform admin can still perform the intended administrative mutations.
6. platform admin still does NOT gain professional authorship automatically.

If you change the semantics of `evaluate_capability(account.manage)`, keep the distinction clear between:
- product display/query of administrative authority, and
- mutation authorization.

Do not create confusing dual meanings.

==================================================
4. B-02 — USE HASHING-SAFE DJANGO USER ADMIN
==================================================

Severity: HIGH

Current problem:

`AccountAdmin` inherits from plain `admin.ModelAdmin`.

That is unsafe/inappropriate for a Django custom user because password creation/change must use hashing-aware UserAdmin forms.

Required correction:

- use Django `UserAdmin` for Account, or an equivalently safe custom admin implementation.
- include the custom fields:
  - person
  - is_platform_admin
  in appropriate fieldsets/add_fieldsets.
- preserve secure password hashing behavior.
- do not expose an ordinary raw password text field.

Add regression coverage if practical, preferably proving:
- admin user creation/change uses hashed password semantics or at least the configured admin class is UserAdmin-based with correct forms.

Do not overbuild a new product account-management UI in this pass.

==================================================
5. B-03 — SECRET_KEY MUST FAIL SAFE
==================================================

Severity: HIGH

Current problem:

When `DJANGO_SECRET_KEY` is absent, settings can use a fixed insecure fallback while `DEBUG=False`.

Required correction:

- in non-debug mode:
  - missing/blank `DJANGO_SECRET_KEY` MUST fail fast during settings startup with a clear configuration error.

- in explicitly debug/development mode:
  - a development-only fallback is acceptable if clearly labeled and impossible to confuse with production.

- CI must continue to pass with its explicit CI key.

Add tests for:
1. non-debug + missing secret key fails.
2. debug/development path behaves as documented.
3. explicit secret key works.

Do not log the secret.

==================================================
6. B-04 — PRESERVE CAPABILITY GRANT PROVENANCE
==================================================

Severity: HIGH

Current problem:

`granted_by_account` is nullable and uses `SET_NULL`.

This allows a sensitive CapabilityGrant to exist without an issuing actor or lose its issuer later.

This violates:

**Actor Always Known**

Required correction:

- ordinary CapabilityGrant creation must require a known granting Account.
- provenance must not silently disappear if that Account is later modified/deactivated/deleted.

Because this is still a clean initial migration and no production data exists, prefer correcting the initial schema cleanly instead of adding needless compatibility complexity.

A suitable baseline is:
- `granted_by_account` non-null.
- deletion behavior that preserves provenance, e.g. `PROTECT`.

If you identify a real bootstrap problem caused by this rule:
- STOP and report it rather than silently inventing a nullable bootstrap exception.

Required tests:
1. grant cannot be persisted without issuer.
2. issuer cannot be deleted while referenced, or equivalent provenance-preserving behavior.
3. revoke preserves original issuer.
4. existing service-created grant records the real admin actor.

==================================================
7. B-05 — PERSON + ACCOUNT CREATION MUST BE ATOMIC
==================================================

Severity: MEDIUM / DATA INTEGRITY

Current problem:

The Account manager may create/save Person before Account creation completes.
A later Account failure can leave an orphan Person.

Required correction:

- automatic Person + Account creation must be atomic.
- a failed Account creation must roll back the automatically-created Person.

Add regression test:
- arrange a failure such as duplicate username after auto-Person creation would have begun.
- assert Person count/state is unchanged after failure.

Do not delete deliberately pre-existing Person objects supplied by the caller.

==================================================
8. B-06 — REMOVE UNAUTHORIZED LICENSE DECISION
==================================================

Severity: MEDIUM / GOVERNANCE

Current problem:

`pyproject.toml` declares:

`license = { text = "Proprietary" }`

But the repository explicitly says licensing is not yet decided.

Required correction:

- remove that license declaration.
- do NOT replace it with MIT/GPL/Apache/Proprietary/All Rights Reserved or any other policy.
- leave licensing undecided until owner decision.

No other licensing changes are authorized.

==================================================
9. B-07 — REMOVE UNNECESSARY CREATEROLE PRIVILEGE
==================================================

Severity: MEDIUM / LEAST PRIVILEGE

Current problem:

README local setup grants:

`CREATEDB CREATEROLE`

but the documented test need is only `CREATEDB`.

Required correction:

- remove `CREATEROLE`.
- document only the minimum PostgreSQL privilege actually required for the local test workflow.
- keep setup instructions accurate.

==================================================
10. N-01 — CLEAN UNUSED/MIS-TYPED VIEW CONTEXT
==================================================

Non-blocking, but fix now if local and trivial.

Current issue:

`can_manage_accounts` in `identity/views.py` is a capability string rather than a boolean and is currently unused.

Preferred correction:
- remove the unused context value now, OR
- evaluate it correctly as a boolean if the current UI genuinely needs it.

Do not add new Admin product UI just to use it.

==================================================
11. DO NOT ADDRESS N-02 IN THIS PASS
==================================================

N-02 notes that the Platform Admin product UI is still read-only.

This is NOT a blocking S01-I01 correction.

Do NOT expand this correction pass into:
- account-management forms.
- grant-management pages.
- new workflow UI.

Record/retain it for the appropriate future increment before Human Acceptance.

==================================================
12. MIGRATION DISCIPLINE
==================================================

Because the current implementation has only an initial development migration and no real production data:

- prefer a clean corrected initial migration if that is consistent with repository policy and branch history.
- ensure migration state matches models exactly.
- do not create unnecessary migration chains solely to preserve a development-only broken schema.

After correction run:
- `python manage.py makemigrations --check --dry-run`
- fresh database migration/test path under PostgreSQL.

==================================================
13. REQUIRED VERIFICATION
==================================================

After all corrections run at minimum:

- Python version.
- Django version.
- `ruff check .`
- `ruff format --check .`
- `python manage.py check`
- `python manage.py makemigrations --check --dry-run`
- full `pytest -q` against PostgreSQL.
- any targeted regression tests for B-01 through B-05.
- verify CI on the pushed head.

Also inspect:
- `git status`
- changed files
- repository for secrets/database artifacts.

==================================================
14. REQUIRED DOCUMENTATION UPDATE
==================================================

Update the S01-I01 gate/evidence so it accurately records:

- independent review decision was HOLD.
- B-01 … B-07.
- correction commit(s).
- regression tests added.
- re-verification evidence.

Do NOT mark:

`PASS — NEXT INCREMENT ALLOWED`

yourself.

The next status after your correction should remain:

`HOLD — RE-REVIEW REQUIRED`

or equivalent wording that clearly awaits independent re-review.

Do not create a PASS checkpoint.

==================================================
15. GIT / PR
==================================================

Continue using:

`build/slice-01`

Push correction commits to the same branch so PR #1 updates.

Do not:
- create a new feature PR.
- close PR #1.
- merge PR #1.
- enable auto-merge.
- start S01-I02.

==================================================
16. FINAL CORRECTION REPORT
==================================================

When corrections are complete, STOP and report:

SYNC
- origin/main SHA integrated.
- merge/sync commit SHA if applicable.

CORRECTIONS
For each:
- B-01 status and exact implementation.
- B-02 status and exact implementation.
- B-03 status and exact implementation.
- B-04 status and exact implementation.
- B-05 status and exact implementation.
- B-06 status.
- B-07 status.
- N-01 status.

COMMITS
- correction commit SHA(s).
- final branch HEAD SHA.

MIGRATIONS
- exact migration state/change.

REGRESSION TESTS
- tests added for each applicable blocker.

FULL VERIFICATION
- Ruff result.
- Django check result.
- migration check result.
- pytest count/result.
- PostgreSQL version/vendor.
- CI run/result.

SCOPE
Explicitly confirm:
- S01-I02 not started.
- no future module added.
- no merge performed.
- auto-merge still disabled.
- no previous Inspector_Website repository inspected/reused.
- no secrets/real sensitive data committed.

GATE
State:

`HOLD — RE-REVIEW REQUIRED`

Then STOP.

Do not self-authorize PASS or S01-I02.
