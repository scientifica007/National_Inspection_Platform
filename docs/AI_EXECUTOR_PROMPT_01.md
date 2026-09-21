# AI Executor Prompt — Vertical Slice 01

You are the implementation agent for **National Inspection Platform**.

Repository: `scientifica007/National_Inspection_Platform`

Create and work only on branch:

`build/slice-01`

Your job is to implement **Vertical Slice 01 — Solo Inspector Field Visit** and nothing beyond that scope.

Before writing code, read all current repository documentation, especially:

- `docs/INVARIANTS.md`
- `docs/PRODUCT_VISION.md`
- `docs/AUTHORITY_MODEL.md`
- `docs/LIFECYCLE_SEMANTICS.md`
- `docs/LIFECYCLE_PROFILES.md`
- `docs/MINIMAL_STABLE_CORE.md`
- `docs/VERTICAL_SLICE_01.md`
- `docs/VERTICAL_SLICE_01_DATA_MODEL.md`
- `docs/ENGINEERING_CONVENTIONS.md`
- `docs/AI_EXECUTOR_SPEC_01.md`
- accepted ADRs in `decisions/`

## Clean-slate rule

Do not inspect, read, copy, compare, cherry-pick or import from any previous Inspector_Website_* repository.

## Required behavior

Build the app, migrations, tests, CI and a usable Arabic RTL interface.

Implement only the modules required by the slice:
- identity
- institutions
- knowledge
- visits
- records
- audit

Do not pre-build Teams, Missions, Assignments, national dashboards, generic workflow engines, microservices, APIs, AI features or other deferred capabilities.

## Quality rules

- business rules enforced server-side.
- PostgreSQL canonical.
- Django 5.2 LTS / Python 3.12.
- no business logic hidden in templates or JavaScript.
- frontend built with replaceable Design Tokens/components.
- no impersonation shortcut for Admin.
- finalized professional records immutable.
- checklist/visit snapshot semantics fully tested.
- permissions tested for unauthenticated, owner inspector, another inspector and Admin.
- run tests and lint before completion.

## Execution process

Do NOT implement the complete slice in one pass.

Follow:
- `docs/CONTROLLED_IMPLEMENTATION_CYCLE.md`
- `docs/SLICE_01_INCREMENT_PLAN.md`
- `docs/INCREMENT_GATE_TEMPLATE.md`

Start with **S01-I01 only**.

After each increment:
- run its automated checks.
- provide the exact commit and test evidence.
- stop for an independent review pass.
- fix all blocking findings.
- rerun checks.
- continue only after the increment checkpoint is marked `PASS — NEXT INCREMENT ALLOWED`.

Do not enter Human Acceptance until all planned Slice 01 increments have passed review and correction.

## Completion

Do not stop at scaffolding or a prototype.

The slice is complete only when all acceptance criteria and tests in repository documentation pass and the app can be run locally for human acceptance.

If a repository document has a real contradiction, stop and report it instead of inventing a policy.
