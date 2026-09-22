# OpenHands Correction Prompt — S01-I01 Review Cycle 5 / Authority Closure

- Target executor: **OpenHands Cloud**
- PR: **#1**
- Branch: `build/slice-01`
- Reviewed head: `6db196d50ff7e4965144d6db238729b498419c88`
- Gate: **HOLD — CORRECTION REQUIRED (R5)**
- Authorization: **authority-foundation correction only; S01-I02 remains forbidden**

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
- `docs/S01_I01_EXPECTED_OUTPUTS.md`
- `docs/gates/S01-I01_CORRECTION_R5.md`
- the latest independent review on PR #1.

### 2. Correct R5-B01 only

#### R5-B01 — close actor-identity borrowing in generic professional authority evaluation

The administrative mutation primitive is now hardened.

However the generic professional capability evaluator still trusts the caller-supplied Account instance and queries grants through its PK.

An unsaved/fabricated Account can borrow a real professional Account's:
- primary key;
- Person id;
- active state;

and may cause `evaluate_capability` / `has_capability` / `require_capability` to evaluate the real Account's stored grants.

This is a pre-existing authority-foundation defect. It was not introduced by R4.1.

Required correction:

1. Introduce one small internal persisted-actor resolver/validator in the identity permission layer.
2. Reject/deny:
   - non-Account input;
   - `pk is None`;
   - Django unsaved/adding Account even with explicit PK;
   - missing database row.
3. Resolve the current stored Account row and use the stored identity state for capability evaluation:
   - current `is_active`;
   - current `is_platform_admin` where administrative query evaluation needs it;
   - stored `person_id`;
   - CapabilityGrant relation/query.
4. `evaluate_capability`, `has_capability`, and `require_capability` must inherit the hardened behavior.
5. Harden `can_perform_professional_work` against the same fabricated/unsaved/stale actor class.
6. Preserve `require_administrative_authority` semantics. Refactor to reuse the persisted actor resolver only if doing so makes the rule clearer and does not weaken any R1-R4 regression.
7. Do NOT introduce delegation, a generic policy engine, middleware redesign, authentication redesign, or new capabilities.

Prefer one explicit helper and a narrow diff over duplicated checks.

### 3. Required regression tests

At minimum prove:

1. fabricated unsaved Account borrowing a real inspector's `pk` and `person_id` cannot satisfy an OWN professional grant;
2. fabricated unsaved Account borrowing a real ALL-granted Account's identity cannot satisfy the ALL grant;
3. `require_capability` raises for the fabricated actor;
4. stale in-memory professional actor is denied after the stored row is deactivated;
5. caller-side modification of `person_id` cannot change OWN-scope identity; stored Person binding decides;
6. genuine persisted professional Account still succeeds;
7. genuine Platform Admin without a professional grant still fails professional capability;
8. `can_perform_professional_work` is false for fabricated/unsaved/inactive actors;
9. `can_perform_professional_work` is true for a genuine active Account with a valid professional grant;
10. all R1-R4.1 authority regression tests remain green.

If the evaluator returns a denial decision for malformed actors, use stable reason codes and test them.

### 4. Final authority-closure inspection

Before stopping, inspect all current identity authority/read helpers for the same root assumption:
- `evaluate_capability`
- `has_capability`
- `require_capability`
- `is_platform_admin`
- `can_perform_professional_work`
- identity selectors used by the current authenticated UI

Do not broaden product scope. If a helper only receives authenticated `request.user` and is safe by construction, document that rather than inventing infrastructure.

The goal is to avoid another one-by-one discovery of the same actor-identity class.

### 5. No migrations expected

No schema change is expected.

If a migration appears:
- STOP;
- explain why;
- do not proceed automatically.

### 6. Verification

Run:
- focused R5 tests;
- all authority/identity tests;
- `ruff check .`;
- `ruff format --check .`;
- `python manage.py check`;
- `python manage.py makemigrations --check --dry-run`;
- full `pytest -q` against PostgreSQL;
- CI on pushed head.

Keep PR #1 draft/open.

### 7. Scope prohibitions

Do NOT:
- start S01-I02;
- merge PR #1;
- enable auto-merge;
- add institutions/checklists/visits;
- add product account-management UI;
- build delegation/audit;
- self-declare PASS.

### 8. Security

Do not output or commit authenticated Git remotes, access tokens, secrets, or real data.

### 9. Gate

Update executor-owned implementation/gate evidence only.

End state:
`HOLD — RE-REVIEW REQUIRED`

No PASS checkpoint.

### 10. Final report

Report:
- current main SHA integrated;
- sync commit;
- correction commit;
- final head SHA;
- exact persisted-actor design;
- exact R5 tests;
- final test count;
- PostgreSQL + CI evidence;
- final authority-helper inspection result;
- scope confirmation.

Then STOP and await independent review.
