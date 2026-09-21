# S01-I01 Correction Cycle — Review 2

- Increment: `S01-I01`
- PR: `#1`
- Reviewed head: `0485d8cc6a0b4d4d673512774fbdcc6e0f709fac`
- Decision: **HOLD — CORRECTION REQUIRED (R2)**

## R1 closure

Original findings B-01…B-07 were re-reviewed. Their intended R1 corrections are substantially present and automated verification is green.

## New/residual blocking findings

| ID | Severity | Finding | Required correction |
|---|---|---|---|
| R2-B01 | Critical | `create_account` is an ungated application mutation and can create Platform Admins | require active Platform Admin actor for application account creation; keep technical bootstrap separate |
| R2-B02 | High | existing Account can be rebound to another Person via Django Admin | make Account→Person binding immutable after creation in supported admin/application path |
| R2-B03 | High | CapabilityGrant Django Admin exposes invalid/bypass-prone add/change/delete surface | make CapabilityGrant technical admin read-only for S01-I01 |
| R2-B04 | High | recipient Account deletion cascades away CapabilityGrant history | use history-preserving recipient deletion policy such as PROTECT |
| R2-B05 | Medium | implementation notes/PR body contain stale statements after R1 sync | update documentation/PR metadata to current truth |

## Evidence

- PR #1 remains draft/open.
- current correction head at review: `0485d8c`.
- branch is synchronized with current main at review time.
- GitHub Actions run `35625026357`: success.
- terminal evidence shows final PostgreSQL-backed suite: 111 passed.
- S01-I02 was not started.

## Authorized next action

OpenHands Cloud may perform a second **correction-only** pass on `build/slice-01`.

Prompt:
`docs/OPENHANDS_CORRECTION_PROMPT_S01_I01_R2.md`

## Exit condition

After correction:
- gate remains `HOLD — RE-REVIEW REQUIRED`;
- independent re-review is mandatory;
- S01-I02 remains unauthorized.
