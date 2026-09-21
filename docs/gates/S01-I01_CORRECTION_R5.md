# S01-I01 Correction Cycle — Review 5 / Authority Closure

- Increment: `S01-I01`
- PR: `#1`
- Reviewed head: `6db196d50ff7e4965144d6db238729b498419c88`
- Decision: **HOLD — CORRECTION REQUIRED (R5)**

## R4.1 closure

The explicit-PK unsaved Platform Admin residual is closed as requested.

Evidence:
- unsaved/adding actor check occurs before stored-row lookup;
- focused R4.1 tests reproduce the original defect when the check is removed;
- PostgreSQL-backed full suite: 229 passed;
- CI green.

## Blocking finding

| ID | Severity | Finding | Required correction |
|---|---|---|---|
| R5-B01 | High | generic professional capability evaluation still trusts caller Account identity and can query a real Account's grants through a borrowed PK/person binding | resolve and use a genuine persisted Account for all professional capability evaluation; deny fabricated/unsaved/stale actors; add regression tests |

### Root cause

`evaluate_capability` currently:
- trusts caller `is_active` / `is_platform_admin` / `person_id`;
- queries `account.capability_grants` from the supplied primary key.

Therefore an unsaved fabricated Account can copy a real professional Account's PK/Person id and borrow its stored grants.

This is a **pre-existing** defect in the original permission foundation, not a regression introduced by R4.1.

## Required closure scope

Harden:
- `evaluate_capability`;
- inherited `has_capability` / `require_capability`;
- `can_perform_professional_work`.

Inspect current `is_platform_admin` and identity selectors for the same root assumption and either harden them narrowly or document why the authenticated current path is safe.

Do not add future product features.

## Authorized executor

OpenHands Cloud may perform one R5 **authority-closure correction-only pass**.

Prompt:
`docs/OPENHANDS_CORRECTION_PROMPT_S01_I01_R5.md`

## Exit condition

After correction:
- `HOLD — RE-REVIEW REQUIRED`;
- independent review must close R5-B01;
- no S01-I02 work before explicit PASS.
