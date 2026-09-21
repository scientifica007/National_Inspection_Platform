# S01-I01 Correction Cycle — Review 1

- Increment: `S01-I01`
- PR: `#1`
- Reviewed implementation head: `0b3fe700997cfd607bce357f590c76cbde179ae8`
- Independent review date: 2026-09-21
- Decision: **HOLD — CORRECTION REQUIRED**

## Blocking findings

| ID | Severity | Root issue | Required correction |
|---|---|---|---|
| B-01 | Critical | administrative grant can permit self-escalation / ignores deferred delegation semantics | restrict S01-I01 administrative mutations to real Platform Admin; add regression tests |
| B-02 | High | custom Account uses plain ModelAdmin | use hashing-safe UserAdmin configuration |
| B-03 | High | fixed SECRET_KEY fallback possible with DEBUG=False | fail fast outside explicit debug/development |
| B-04 | High | CapabilityGrant issuer can be null/erased | require and preserve granting actor |
| B-05 | Medium | Person can be orphaned if Account creation fails | make auto Person+Account creation atomic |
| B-06 | Medium | package metadata invents Proprietary license | remove license decision |
| B-07 | Medium | README grants unnecessary PostgreSQL CREATEROLE | reduce to minimum privilege |

## Non-blocking

- N-01: remove or correctly evaluate unused `can_manage_accounts` context.
- N-02: product Admin management UI remains future work; do not expand correction scope.

## Synchronization requirement

The reviewed branch was behind current `main`. The correction pass must first integrate the current canonical documentation baseline without discarding the implementation commits.

## Authorized correction executor

OpenHands Cloud may perform a **correction-only pass** on `build/slice-01`.

Prompt:
`docs/OPENHANDS_CORRECTION_PROMPT_S01_I01_R1.md`

## Exit condition

After correction and CI:
- status remains **HOLD — RE-REVIEW REQUIRED**.
- independent reviewer must close each blocker.
- only reviewer/maintainer may set `PASS — NEXT INCREMENT ALLOWED`.

S01-I02 remains unauthorized.
