# Operations and Maintenance

- Status: **Design baseline; production details deferred**

## Maintenance objective

The platform should be repairable and evolvable without requiring broad rewrites for ordinary changes.

## Replaceable-part strategy

Change should remain localized:

- UI theme/layout → Presentation.
- page composition → Presentation/View Models.
- business process → Application/Domain with explicit decision.
- file backend → Storage adapter.
- export engine → Export adapter.
- external service → Integration adapter.
- dashboard query shape → reporting/query layer.

## Dependency hygiene

Maintenance reviews should detect:
- circular imports.
- cross-module direct mutations.
- duplicated permission logic.
- business rules inside templates.
- "utils.py" dumping grounds.
- generic abstractions without demonstrated use.

## Upgrade policy

For framework/dependency upgrades:
1. read release/security notes.
2. create bounded upgrade branch/increment.
3. run full relevant tests.
4. inspect deprecations/migrations.
5. human smoke test critical UI.
6. document upgrade decision if it changes architecture/behavior.

## Database maintenance

Before destructive/schema-significant production change:
- backup.
- verify restore path.
- document migration.
- test on representative copy.
- define rollback/forward-fix strategy.

Prefer additive, reversible migrations when practical.

## Observability

Before production, define:
- structured application logs.
- error reporting.
- health checks.
- audit-event retention.
- database/storage capacity monitoring.

Do not leak sensitive professional data into logs unnecessarily.

## Backup/recovery

Before production:
- database backup schedule.
- evidence/file storage backup.
- restore drill.
- recovery responsibility.
- retention window.

## Dependency minimization

Every dependency increases maintenance burden.

Add a package only when it provides clear value over a small internal implementation and is actively maintained.

## Documentation maintenance

At each milestone/checkpoint:
- update PROJECT_STATE.
- update CHANGELOG.
- update risk register if needed.
- update ADR/traceability if decisions changed.

## Maintenance success criterion

A routine change should affect the smallest plausible area and be testable without understanding the entire system.
