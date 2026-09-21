# Project State

- Project: **National Inspection Platform**
- Repository: `scientifica007/National_Inspection_Platform`
- Date: 2026-09-21
- Canonical branch for design baseline: `main`

## Current milestone

**M0 — Foundation / Domain Design — COMPLETE**

## Current delivery readiness

**READY FOR AI EXECUTOR — CONTROLLED IMPLEMENTATION**

This readiness applies only to:

**Vertical Slice 01 — Solo Inspector Field Visit**

It does not authorize broad implementation of the complete national platform.

## Next authorized action

Create/use implementation branch:

`build/slice-01`

Then execute only:

**S01-I01 — Project Skeleton + Identity/Authority Foundation**

After implementation:
- verify.
- independently review.
- correct.
- reverify.
- record checkpoint.

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

## Human review state

**NOT STARTED**

Human Acceptance is intentionally deferred until S01-I01 … S01-I07 pass automated verification, review and correction gates.

## Production state

**NOT PRODUCTION READY**

No real official finalized records may be used before:
- Amendment/Addendum correction flow is implemented and tested.
- deployment/security/backup controls are reviewed.
- human acceptance is passed for the relevant release.
