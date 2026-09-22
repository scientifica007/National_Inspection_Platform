# Documentation Index

- Status: **Canonical documentation map**
- Updated: 2026-09-22

This file explains where each class of project truth lives and how an implementer/reviewer should resolve ambiguity.

## Source-of-truth precedence

When two documents appear to conflict, use this order:

1. `docs/INVARIANTS.md`
2. accepted ADRs in `decisions/`
3. `docs/PRODUCT_VISION.md`
4. `docs/AUTHORITY_MODEL.md`
5. `docs/DOMAIN_MODEL.md`
6. lifecycle documents
7. current slice specification/data model
8. engineering/security/repository-governance conventions
9. roadmap/status/checkpoint documents
10. implementation notes

If a true conflict remains after applying this order, implementation must stop and the conflict must be documented and resolved explicitly.

## Project direction

- `PRODUCT_VISION.md` — product purpose and operating philosophy.
- `INVARIANTS.md` — non-negotiable domain rules.
- `DOMAIN_MODEL.md` — conceptual domain baseline.
- `MINIMAL_STABLE_CORE.md` — smallest stable conceptual core.
- `GLOSSARY.md` — agreed terminology.
- `ROADMAP.md` — staged evolution of the platform.

## Authority, security and history

- `AUTHORITY_MODEL.md` — Person/Position/Capability/Scope/Context model.
- `LIFECYCLE_SEMANTICS.md` — Save/Submit/Finalize/Approve/Publish meanings.
- `LIFECYCLE_PROFILES.md` — lifecycle specialization by domain object.
- `SECURITY_AND_DATA_GOVERNANCE.md` — security, real-data, privacy and audit rules.
- `LEGAL_AND_LICENSING.md` — public-repo licensing/content-rights note.

## Architecture and maintainability

- `ARCHITECTURE_PRINCIPLES.md` — modular monolith and replaceability.
- `MODULE_DEPENDENCY_MAP.md` — allowed dependency direction.
- `ENGINEERING_CONVENTIONS.md` — implementation structure/conventions.
- `UI_DESIGN_PRINCIPLES.md` — replaceable interface and UX principles.
- `OPERATIONS_AND_MAINTENANCE.md` — maintenance/upgrade/backup discipline.
- `REPOSITORY_GOVERNANCE.md` — branches, PRs and repository controls.
- accepted ADRs in `../decisions/`.

## Controlled implementation

- `CONTROLLED_IMPLEMENTATION_CYCLE.md` — implement → verify → review → correct → reverify.
- `INCREMENT_GATE_TEMPLATE.md` — mandatory increment gate.
- `gates/S01-I01_CORRECTION_R1.md` — correction record for S01-I01 review cycle 1.
- `gates/S01-I01_CORRECTION_R2.md` — correction record for S01-I01 review cycle 2.
- `gates/S01-I01_CORRECTION_R3.md` — correction record for S01-I01 review cycle 3.
- `gates/S01-I01_CORRECTION_R4.md` — correction record for S01-I01 review cycle 4.
- `gates/S01-I01_CORRECTION_R4_1.md` — residual correction record after R4 re-review.
- `gates/S01-I01_CORRECTION_R5.md` — final authority-closure correction record.
- `gates/S01-I02_GATE.md` — active implementation/review gate for S01-I02.
- `checkpoints/S01-I01_PASS_2026-09-22.md` — accepted S01-I01 PASS checkpoint.
- `CHECKPOINT_RECORD_TEMPLATE.md` — persisted checkpoint evidence.
- `CORRECTION_CYCLE_TEMPLATE.md` — correction/re-verification record.
- `SLICE_01_INCREMENT_PLAN.md` — increments S01-I01 … S01-I07.
- `TEST_STRATEGY.md` — automated and human test layers.
- `REVIEW_AND_CHANGE_POLICY.md` — review/correction/change-control policy.
- `RELEASE_GATES.md` — Design → Increment → Slice → Human → Pilot → Production gates.

## Vertical Slice 01

- `VERTICAL_SLICE_01.md` — behavior and acceptance criteria.
- `VERTICAL_SLICE_01_DATA_MODEL.md` — concrete first-slice data model.
- `VERTICAL_SLICE_01_DATA_MODEL_REVIEW.md` — review conclusions.
- `INITIAL_IMPLEMENTATION_SCOPE.md` — in/out boundaries.
- `AI_EXECUTOR_SPEC_01.md` — controlled implementation specification.
- `AI_EXECUTOR_PROMPT_01.md` — generic executor prompt.
- `OPENHANDS_EXECUTOR_PROMPT_S01_I01.md` — OpenHands-specific prompt for initial S01-I01 implementation.
- `OPENHANDS_CORRECTION_PROMPT_S01_I01_R1.md` — correction-only OpenHands prompt after independent review R1.
- `OPENHANDS_CORRECTION_PROMPT_S01_I01_R2.md` — correction-only OpenHands prompt after independent re-review R2.
- `OPENHANDS_CORRECTION_PROMPT_S01_I01_R3.md` — correction-only OpenHands prompt after independent re-review R3.
- `OPENHANDS_CORRECTION_PROMPT_S01_I01_R4.md` — minimal correction-only OpenHands prompt after independent re-review R4.
- `OPENHANDS_CORRECTION_PROMPT_S01_I01_R4_1.md` — one-residual-fix OpenHands prompt after R4 correction re-review.
- `OPENHANDS_CORRECTION_PROMPT_S01_I01_R5.md` — authority-closure OpenHands prompt after final S01-I01 permission audit.
- `S01_I01_EXPECTED_OUTPUTS.md` — precise expected outputs/non-outputs for S01-I01.
- `S01_I02_EXPECTED_OUTPUTS.md` — precise expected outputs/non-outputs and authority contract for S01-I02.
- `CODEX_EXECUTOR_PROMPT_S01_I02.md` — Codex-specific controlled executor prompt for S01-I02.
- `AI_REVIEWER_PROMPT_01.md` — independent reviewer/auditor prompt.

## Reviews and readiness

- `SCENARIO_TESTS.md` — domain fitness scenarios.
- `SCENARIO_REVIEW_01.md` — first scenario review.
- `FINAL_ARCHITECTURE_REVIEW.md` — M0 architecture review.
- `AI_EXECUTOR_HANDOFF.md` — executor readiness gate.
- `HUMAN_ACCEPTANCE_PROTOCOL.md` — owner review protocol.
- `TRACEABILITY_MATRIX.md` — requirement-to-design/test traceability.
- `RISK_REGISTER.md` — known project risks and controls.

## State and history

- `PROJECT_STATE.md` — current canonical project state.
- `M0_STATUS.md` — M0 completion record.
- `DECISION_REGISTER.md` — current summarized decisions.
- `OPEN_DECISIONS.md` — historical handoff decision file; currently resolved.
- `checkpoints/` — accepted implementation/checkpoint records.
- root `CHANGELOG.md` — high-level project evolution.

## Contributor entry points

- root `README.md` — project landing page.
- root `CONTRIBUTING.md` — executor/contributor workflow.

## Rule

A document is not considered implemented merely because it exists.  
Implementation truth requires code + tests + review evidence + passed increment gate.
