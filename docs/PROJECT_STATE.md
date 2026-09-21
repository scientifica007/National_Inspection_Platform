# Project State

- Project: **National Inspection Platform**
- Repository: `scientifica007/National_Inspection_Platform`
- Date: 2026-09-21
- Canonical branch for design baseline: `main`

## Current milestone

**M0 — Foundation / Domain Design — COMPLETE**

## Documentation baseline

**DOCUMENTED AND INDEXED**

The repository now contains:
- product/domain/authority/lifecycle baseline.
- architecture/dependency/engineering baseline.
- security/data-governance baseline.
- UI/maintenance/repository-governance baseline.
- roadmap/risk/traceability/decision records.
- controlled executor/reviewer/correction/checkpoint protocols.
- human acceptance and release gates.

Canonical map:
`docs/DOCUMENTATION_INDEX.md`

## Current delivery readiness

**READY FOR AI EXECUTOR — CONTROLLED IMPLEMENTATION**

This readiness applies only to:

**Vertical Slice 01 — Solo Inspector Field Visit**

It does not authorize broad implementation of the complete national platform.

## Current implementation gate

**S01-I01 — HOLD — CORRECTION REQUIRED (R2)**

Independent re-review of PR #1 confirmed the R1 fixes but found residual/new blocking findings R2-B01 through R2-B05.

Active correction record:
`docs/gates/S01-I01_CORRECTION_R2.md`

Authorized correction prompt:
`docs/OPENHANDS_CORRECTION_PROMPT_S01_I01_R2.md`

## Next authorized action

Continue on implementation branch:

`build/slice-01`

Execute the **R2 correction-only pass for S01-I01**.

S01-I02 remains unauthorized.

Selected executor for this increment:
**OpenHands Cloud (free option), under controlled execution constraints.**

OpenHands-specific prompt:
`docs/OPENHANDS_EXECUTOR_PROMPT_S01_I01.md`

Expected outputs:
`docs/S01_I01_EXPECTED_OUTPUTS.md`

After correction:
- rerun verification.
- push corrections to PR #1.
- stop with `HOLD — RE-REVIEW REQUIRED`.
- independently re-review.
- correct further if needed.
- record checkpoint only after PASS.

No S01-I02 work starts before S01-I01 is explicitly marked:

`PASS — NEXT INCREMENT ALLOWED`

## Accepted architectural baseline

- clean-slate implementation.
- modular monolith.
- Django 5.2 LTS / Python 3.12 / PostgreSQL.
- server-rendered Arabic RTL UI first.
- Design Tokens/components for replaceable presentation.
- business logic outside templates/JavaScript.
- no microservices initially.
- no copying from previous Inspector_Website_* experiments.

## Accepted domain baseline

- Person is separate from Account, Position and temporary operational role.
- Capability + Scope + Time + Context determine authority.
- Admin is the highest administrative authority inside the application.
- Admin status alone does not grant professional authorship.
- professional identity cannot be borrowed or impersonated.
- Draft is mutable.
- Finalized professional history is immutable.
- correction adds history through Amendment/Addendum.
- local work remains possible.
- historical execution uses snapshots/versioned meaning.
- changing reality should be Data/Configuration whenever it is not a stable domain law.

## Repository-governance note

GitHub currently reports `main` as unprotected.  
This does not block S01-I01 design readiness, but branch-protection settings should be reviewed before routine implementation merges to `main`.

## Human review state

**NOT STARTED**

Human Acceptance is intentionally deferred until S01-I01 … S01-I07 pass automated verification, review and correction gates.

## Production state

**NOT PRODUCTION READY**

No real official finalized records may be used before:
- Amendment/Addendum correction flow is implemented and tested.
- deployment/security/backup controls are reviewed.
- human acceptance is passed for the relevant release.
