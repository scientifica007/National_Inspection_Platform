# S01-I02 Correction Cycle — Review R1

- Increment: `S01-I02 — Local Institutions`
- PR: `#2`
- Reviewed head: `d5db159a00e15349192e09c6d4be5bd52bd2c760`
- Executor: **Codex**
- Decision: **HOLD — CORRECTION REQUIRED (R1)**

## Positive findings

The first Codex delivery is substantially aligned:
- exact S01-I02 module scope;
- Institution model/migration match;
- actor identity reuses accepted persisted-account authority;
- owner/other/Admin read visibility is separated correctly;
- PostgreSQL CI is green with 312 tests;
- no S01-I03 module was added.

## Blocking findings

| ID | Severity | Finding | Required correction |
|---|---|---|---|
| S01-I02-R1-B01 | Critical | Institution permission/mutation logic trusts caller-supplied target object ownership/lifecycle; a fabricated or stale object with a borrowed PK can cross-owner mutate/archive/delete a real row | resolve current persisted Institution target inside the institutions layer; lock/current-read on mutations; authorize and mutate stored row; add regression tests |
| S01-I02-R1-B02 | High | plain Django InstitutionAdmin exposes add/change/delete and writable owner/creator/lifecycle fields, bypassing application ownership/lifecycle rules | make technical Institution admin inspection-only or unregister it; add admin regression tests |

## B01 root issue

S01-I01 established that authority must follow stored identity, not caller object state.

S01-I02 correctly applies that to the **actor** but not to the **target Institution**.

Current mutation predicates read caller-side:
- `local_owner_person_id`;
- lifecycle.

Services then save/delete using the caller object's PK. Therefore object identity/ownership can be borrowed at the target side even though actor identity is hardened.

## B02 root issue

The accepted product rule says:
- creator/owner derive from the real actor;
- no ownership transfer;
- archive is one-way;
- archived Institution is not editable;
- hard delete follows application retention/lifecycle rules.

A writable generic ModelAdmin bypasses all of these rules.

## Non-blocking observation

A create-capable account without `institution.read.own` can create but cannot follow the resulting detail redirect. This is documented but not part of R1 correction because capability-profile implication is not defined by this increment.

## Evidence

- PR #2: draft/open/unmerged.
- branch: 2 commits ahead, 0 behind starting main.
- GitHub Actions run `35725511709`: success.
- full PostgreSQL suite: 312 passed.
- no S01-I03+ module present.

## Authorized next action

Codex may execute one **R1 correction-only pass** on `build/s01-i02`.

Prompt:
`docs/CODEX_CORRECTION_PROMPT_S01_I02_R1.md`

## Exit condition

After correction:
- gate remains `HOLD — RE-REVIEW REQUIRED`;
- independent reviewer closes or reopens findings;
- S01-I03 remains unauthorized.
