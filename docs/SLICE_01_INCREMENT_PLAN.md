# Vertical Slice 01 — Controlled Increment Plan

The first human review is intentionally delayed until several small machine-reviewed increments form a coherent workflow.

## S01-I01 — Project Skeleton + Identity/Authority Foundation

Build:
- Django project.
- PostgreSQL configuration.
- custom Account/User from day one.
- Person.
- minimal CapabilityGrant with OWN/ALL.
- authentication.
- Admin vs professional authorship separation.
- basic Arabic RTL shell and design tokens.
- CI/lint/test foundation.

Gate:
- authentication works.
- permission primitives tested.
- Admin cannot impersonate professional identity.
- no future modules added.

## S01-I02 — Local Institutions

Build:
- local Institution model/lifecycle.
- inspector create/list/detail/edit/archive/delete rules.
- server-side object permissions.
- Admin visibility.

Gate:
- hard-delete/retention behavior tested.
- owner vs other inspector vs Admin matrix passes.
- no Institution data hard-coded.

## S01-I03 — Local Checklist + Versioning

Build:
- Checklist.
- ChecklistVersion DRAFT/ACTIVE/ARCHIVED.
- ChecklistItem hierarchy.
- activation.
- new-version flow.

Gate:
- ACTIVE version immutable.
- changing active content requires new DRAFT version.
- permissions and ownership tested.

## S01-I04 — Draft Visit + Frozen Snapshot

Build:
- Visit DRAFT.
- Institution snapshot.
- ACTIVE Checklist selection.
- VisitChecklistSnapshot + VisitSnapshotNode.
- checklist replacement rule.

Gate:
- source edits never alter existing snapshot.
- replacement blocked when it would orphan linked records.
- draft visit edit/delete tested.

## S01-I05 — Findings + Recommendations

Build:
- draft Finding.
- draft Recommendation.
- node-linked and visit-level records.
- edit/delete while Visit DRAFT.

Gate:
- authorship/provenance correct.
- another inspector cannot mutate.
- Admin can inspect but not author as inspector.

## S01-I06 — Finalization + Immutability

Build:
- finalize transaction.
- finalization confirmation.
- immutable Visit/Findings/Recommendations.
- audit event.
- finalized read-only views.

Gate:
- server-side mutation/delete attempts rejected.
- transaction and concurrency-sensitive behavior tested.
- no UI-only enforcement.

## S01-I07 — UX/Integration Hardening

Build/fix only what is needed to make the complete slice coherent:
- navigation.
- empty states.
- validation/error clarity.
- unsaved-change behavior.
- RTL/mobile usability.
- demo/test data command.
- run/setup documentation.
- critical Playwright path.

Gate:
- complete end-to-end browser workflow passes.
- desktop/mobile smoke checks pass.
- no known blocker remains.

## Human Acceptance Gate

Only after S01-I01 through S01-I07 are PASS.

The owner then evaluates the full Solo Inspector Field Visit workflow visually and practically.

Human acceptance findings are not mixed casually into a future feature branch; they become explicit correction increments.
