# Project State

- Project: **National Inspection Platform**
- Repository: `scientifica007/National_Inspection_Platform`
- Date: 2026-09-22
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

**S01-I01 — PASS — NEXT INCREMENT ALLOWED**

Independent closure review verified the final R5 authority correction at code head:

`7938ba8f133f2814cd8b2172140a2284d4d23a01`

Reviewer-owned gate closure was recorded on the implementation branch at:

`6ecaa621cd57696cc27e7ea4ce0343783f0835f5`

Evidence:
- R1 through R5 blocking findings resolved.
- R5 PostgreSQL CI run `35675070386`: **271 passed**.
- reviewer gate-only CI run `35703589536`: **success**.
- no future S01-I02 module present.
- accepted non-blocking deferrals remain documented.

Accepted checkpoint:
`docs/checkpoints/S01-I01_PASS_2026-09-22.md`

## Merge state

PR #1 was marked ready and merged into `main` on 2026-09-22.

Merge commit:

`72e156d4e285b334f83f7918068d6803d1b7f141`

Fresh read after merge confirms that `main` contains:
- the accepted S01-I01 implementation;
- the reviewer-owned PASS gate;
- the S01-I01 PASS checkpoint;
- the R1–R5 review/correction history.

The CI workflow runs on `build/**` pushes and pull requests targeting `main`; it does not run on direct `main` pushes/merge commits. The accepted reviewer-head CI had already passed before merge.

## Next authorized action

**S01-I02 — Local Institutions**

Status:

**HOLD — CORRECTION REQUIRED (R1)**

The next increment must start from the current accepted `main` baseline and remain bounded to:
- local Institution model/lifecycle;
- inspector create/list/detail/edit/archive/delete rules;
- server-side object permissions;
- Admin visibility;
- tests for hard-delete/retention and owner/other-inspector/Admin matrix.

No S01-I03 or later work is authorized.

S01-I01 executor:
**OpenHands Cloud**, under the controlled executor/reviewer/correction cycle.

S01-I02 selected executor:
**Codex**, as a controlled executor switch for this increment.

Prepared control documents:
- `docs/S01_I02_EXPECTED_OUTPUTS.md`
- `docs/CODEX_EXECUTOR_PROMPT_S01_I02.md`
- `docs/gates/S01-I02_GATE.md`

Dedicated implementation branch:
`build/s01-i02`

Codex completed the first S01-I02 implementation in draft PR #2. Independent review found two blocking issues: target-Institution state is not re-resolved before authorization/mutation, and Django InstitutionAdmin bypasses application ownership/lifecycle rules.

Active correction record:
- `docs/gates/S01-I02_CORRECTION_R1.md`

Authorized correction prompt:
- `docs/CODEX_CORRECTION_PROMPT_S01_I02_R1.md`

Codex may perform the R1 correction-only pass on `build/s01-i02`, then must stop at `HOLD — RE-REVIEW REQUIRED`. S01-I03 remains unauthorized.

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
