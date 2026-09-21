# Traceability Matrix

- Status: **Baseline**
- Updated: 2026-09-21

| Need / Principle | Design source | First implementation evidence |
|---|---|---|
| Admin has broad application authority but cannot impersonate professional author | ADR-0003, AUTHORITY_MODEL | S01-I01 permission tests; S01-I05/I06 mutation tests |
| Person/account/position are distinct | DOMAIN_MODEL, AUTHORITY_MODEL | S01-I01 models/services |
| Inspector can work independently | PRODUCT_VISION, VERTICAL_SLICE_01 | complete Slice 01 happy path |
| Institutions are data, not hard-coded | INVARIANTS, data model | S01-I02 tests |
| Checklist is locally creatable/versioned | knowledge model | S01-I03 tests |
| Historical meaning is frozen | INVARIANTS | S01-I04 snapshot regression tests |
| Draft can change/delete | lifecycle docs | S01-I02/I03/I04/I05 tests |
| Finalized records immutable | INVARIANTS | S01-I06 server-side mutation/delete rejection |
| Correction adds history | INVARIANTS | Deferred to M2; production blocked until implemented |
| UI can be redesigned without backend rewrite | ADR-0001, UI_DESIGN_PRINCIPLES | architecture review + unchanged domain/application tests |
| Arabic RTL/mobile usability | UI principles | S01-I07 + Human Acceptance |
| No UI-only permissions | security/engineering | permission matrix each relevant increment |
| Controlled implementation loops | CONTROLLED_IMPLEMENTATION_CYCLE | increment checkpoints |
| Human review after machine review/correction | HUMAN_ACCEPTANCE_PROTOCOL | Human Acceptance 01 |
| Teams flexible/contextual | DOMAIN_MODEL | future Team slice design gate |
| Missions optional/mandatory | DOMAIN_MODEL | future Mission slice design gate |
| Geography changes over time | DOMAIN_MODEL | future Geography slice design gate |
| Dashboards support zoom/drill-down | PRODUCT_VISION | future Dashboard slice |
| Aggregates preserve provenance | INVARIANTS | future Reporting/Dashboard tests |
| Public repo contains no real sensitive data | SECURITY_AND_DATA_GOVERNANCE | fixtures/review/secret scanning discipline |

## Rule

Every new accepted requirement must be traceable to:
- a design/domain source, and
- planned or implemented verification evidence.

If a requirement has neither, it is not yet controlled.
