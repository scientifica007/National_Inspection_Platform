# Changelog

This changelog records project-level architecture/delivery milestones, not every file edit.

## 2026-09-21 — M0 Foundation Complete

Established clean-slate National Inspection Platform design baseline.

Accepted:
- Stable Core / Flexible Reality / Immutable History / Progressive Complexity.
- replaceable-parts architecture.
- Modular Monolith.
- Admin authority separated from professional authorship.
- Django 5.2 LTS + Python 3.12 + PostgreSQL initial stack.
- controlled implementation cycle.
- Vertical Slice 01: Solo Inspector Field Visit.
- S01-I01 … S01-I07 increment plan.
- human acceptance after machine review/correction gates.

Created:
- domain/authority/lifecycle documentation.
- architecture and dependency map.
- first-slice concrete data model.
- test strategy.
- executor handoff/spec/prompt.
- risk/security/UI/maintenance/review governance docs.

State:
- M0 COMPLETE.
- Slice 01 READY FOR AI EXECUTOR — CONTROLLED IMPLEMENTATION.
- next authorized increment: S01-I01 only.


## 2026-09-21 — OpenHands Selected for S01-I01

Selected OpenHands Cloud as the controlled executor for the first increment.

Added:
- `docs/OPENHANDS_EXECUTOR_PROMPT_S01_I01.md`
- `docs/S01_I01_EXPECTED_OUTPUTS.md`

Execution remains restricted to S01-I01. OpenHands must stop after implementation/testing and may not continue to S01-I02 without an independent review gate PASS.


## 2026-09-21 — S01-I01 Independent Review R1

PR #1 was independently reviewed against the current main documentation baseline, actual diff, tests, CI and execution evidence.

Gate:
- `HOLD — CORRECTION REQUIRED`

Blocking findings:
- B-01 administrative self-escalation/delegation gap.
- B-02 unsafe plain ModelAdmin for custom Account.
- B-03 insecure SECRET_KEY fallback outside explicit debug.
- B-04 CapabilityGrant provenance can be null/erased.
- B-05 non-atomic auto Person+Account creation.
- B-06 unauthorized Proprietary license metadata.
- B-07 unnecessary PostgreSQL CREATEROLE privilege.

Added:
- `docs/OPENHANDS_CORRECTION_PROMPT_S01_I01_R1.md`
- `docs/gates/S01-I01_CORRECTION_R1.md`

S01-I02 remains unauthorized.


## 2026-09-21 — S01-I01 Independent Re-review R2

Re-reviewed PR #1 at head `0485d8c` after correction cycle R1.

R1 blockers B-01…B-07 were substantially closed, but the gate remains:
- `HOLD — CORRECTION REQUIRED (R2)`

New/residual blockers:
- R2-B01: ungated `create_account` application service can mint Platform Admins.
- R2-B02: Account→Person binding remains mutable through Django Admin.
- R2-B03: CapabilityGrant technical admin exposes invalid/bypass-prone mutation surface.
- R2-B04: grant recipient Account deletion can CASCADE away CapabilityGrant history.
- R2-B05: stale implementation/PR documentation after R1 sync.

Added:
- `docs/OPENHANDS_CORRECTION_PROMPT_S01_I01_R2.md`
- `docs/gates/S01-I01_CORRECTION_R2.md`

S01-I02 remains unauthorized.


## 2026-09-21 — S01-I01 Independent Re-review R3

Re-reviewed PR #1 at head `b94eb38` after correction cycle R2.

R2 blockers R2-B01…R2-B05 were closed. Gate remains:
- `HOLD — CORRECTION REQUIRED (R3)`

Remaining blockers:
- R3-B01: bootstrap Platform Admin creation can orphan a Person if Account creation fails.
- R3-B02: `identity.services.create_person` is an ungated application identity mutation.
- R3-B03: local setup docs distinguish neither Django superuser nor explain first Platform Admin bootstrap.

Added:
- `docs/OPENHANDS_CORRECTION_PROMPT_S01_I01_R3.md`
- `docs/gates/S01-I01_CORRECTION_R3.md`

S01-I02 remains unauthorized.


## 2026-09-21 — S01-I01 Independent Re-review R4

Re-reviewed PR #1 at head `cd58b81` after correction cycle R3.

R3 blockers R3-B01…R3-B03 were closed. Gate remains:
- `HOLD — CORRECTION REQUIRED (R4)`

Remaining blocker:
- R4-B01: `require_administrative_authority` trusts duck-typed/in-memory flags and can accept fabricated or unsaved actors instead of a real persisted Platform Admin.

Documentation cleanup:
- R4-B02: PR top verification summary still contains stale pre-R3 totals.

Operational security notice:
- an access-token-like GitHub credential appeared in the supplied execution transcript; it was not found in the repository diff. Treat it as exposed and rotate/revoke if still valid.

Added:
- `docs/OPENHANDS_CORRECTION_PROMPT_S01_I01_R4.md`
- `docs/gates/S01-I01_CORRECTION_R4.md`

S01-I02 remains unauthorized.


## 2026-09-21 — S01-I01 R4 Correction Re-review / Residual R4.1

Re-reviewed PR #1 at head `ead4698` after correction cycle R4.

Results:
- R4-B02: closed.
- R4-B01: substantially corrected but not fully closed.

Residual:
- an unsaved Django `Account` may be constructed with an explicit PK copied from a real Platform Admin.
- because the R4 primitive checks only `pk is not None` before querying that PK, the fabricated unsaved instance can still borrow the real admin's stored authority.

Gate:
- `HOLD — MINIMAL RESIDUAL CORRECTION REQUIRED (R4.1)`

Added:
- `docs/OPENHANDS_CORRECTION_PROMPT_S01_I01_R4_1.md`
- `docs/gates/S01-I01_CORRECTION_R4_1.md`

S01-I02 remains unauthorized.


## 2026-09-21 — S01-I01 R4.1 Re-review / R5 Authority Closure

Re-reviewed PR #1 at head `6db196d`.

R4.1 result:
- explicit-PK unsaved Platform Admin residual: closed.
- PostgreSQL-backed suite: 229 passed.
- CI green.

Final permission-surface closure audit found one pre-existing blocker:
- R5-B01: generic professional capability evaluation trusts the caller Account object's identity state and can query a real Account's persisted grants through a borrowed PK/person binding.

This was present in the original permission foundation; it was not introduced by R4.1.

Gate:
- `HOLD — CORRECTION REQUIRED (R5 / AUTHORITY CLOSURE)`

Added:
- `docs/OPENHANDS_CORRECTION_PROMPT_S01_I01_R5.md`
- `docs/gates/S01-I01_CORRECTION_R5.md`

S01-I02 remains unauthorized.


## 2026-09-22 — S01-I01 PASS

Independent closure review completed for PR #1 after correction cycle R5.

Reviewed implementation:
- code head: `7938ba8f133f2814cd8b2172140a2284d4d23a01`
- reviewer gate commit: `6ecaa621cd57696cc27e7ea4ce0343783f0835f5`

Verification:
- R5 PostgreSQL CI run `35675070386`: success, 271 tests passed.
- reviewer gate-only CI run `35703589536`: success.
- Ruff, format, Django system check and migration check green.
- no S01-I02 module present.

Review outcome:
- all R1–R5 blocking findings resolved.
- persisted-actor authority is shared across professional and administrative evaluation surfaces.
- accepted non-blocking deferrals remain documented.

Checkpoint:
- `docs/checkpoints/S01-I01_PASS_2026-09-22.md`

Gate:
- `PASS — NEXT INCREMENT ALLOWED`

Next required operation:
- merge PR #1 into `main`;
- only then begin the bounded S01-I02 — Local Institutions increment.


## 2026-09-22 — S01-I01 Merged to Main

PR #1 was marked ready for review and merged after the independent PASS gate.

Merge:
- PR: #1 — S01-I01 Project Skeleton + Identity/Authority Foundation.
- merge commit: `72e156d4e285b334f83f7918068d6803d1b7f141`.
- merge method: merge commit.

Post-merge fresh read confirms that `main` contains:
- accepted S01-I01 implementation;
- PASS gate;
- S01-I01 checkpoint;
- full R1–R5 review/correction history.

The repository CI workflow does not trigger on `main` pushes; the final reviewer-head CI run `35703589536` had already passed before merge.

Next authorized increment:
- `S01-I02 — Local Institutions`.
- status: AUTHORIZED — NOT STARTED.


## 2026-09-22 — Codex Selected for S01-I02

Selected Codex as the controlled executor for:
- `S01-I02 — Local Institutions`.

This is an intentional executor switch after S01-I01 was completed by OpenHands and merged.

Prepared:
- `docs/S01_I02_EXPECTED_OUTPUTS.md`
- `docs/CODEX_EXECUTOR_PROMPT_S01_I02.md`
- `docs/gates/S01-I02_GATE.md`

Execution constraints:
- branch: `build/s01-i02`.
- start from current accepted `main`.
- implement S01-I02 only.
- create a draft PR.
- stop at `HOLD — RE-REVIEW REQUIRED`.
- no S01-I03 work before independent PASS.

The review standard is unchanged from S01-I01: implementation quality, authority, lifecycle, data integrity, scope, PostgreSQL verification and CI remain independently reviewed.


## 2026-09-22 — S01-I02 Independent Review R1

Reviewed Codex draft PR #2 at head `d5db159a00e15349192e09c6d4be5bd52bd2c760`.

Positive:
- S01-I02 scope discipline was strong.
- Institution model/migration aligned with the accepted contract.
- actor identity reused the accepted S01-I01 persisted-account authority.
- PostgreSQL CI passed with 312 tests.
- no S01-I03 module was added.

Gate:
- `HOLD — CORRECTION REQUIRED (R1)`

Blocking findings:
- S01-I02-R1-B01 (Critical): Institution permission/mutation logic trusts the caller-supplied target Institution object. A fabricated or stale target carrying a real row's PK can bypass stored ownership/lifecycle and mutate/archive/delete that row.
- S01-I02-R1-B02 (High): Django InstitutionAdmin exposes add/change/delete and writable owner/creator/lifecycle fields, bypassing application service rules.

Added:
- `docs/CODEX_CORRECTION_PROMPT_S01_I02_R1.md`
- `docs/gates/S01-I02_CORRECTION_R1.md`

S01-I03 remains unauthorized.
