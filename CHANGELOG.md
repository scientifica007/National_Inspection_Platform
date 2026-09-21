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
