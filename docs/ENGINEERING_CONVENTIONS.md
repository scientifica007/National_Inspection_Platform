# Engineering Conventions — Initial Implementation

- Status: **Accepted baseline for executor**

## Repository discipline

- `main` remains stable.
- Executor works on `build/slice-01` (or an equivalent dedicated implementation branch).
- Changes reach `main` through review/PR.
- Do not import/copy code, architecture, migrations, templates, databases or tests from Inspector_Website_001/002/003/004/005.
- Previous experiments are lessons, not code dependencies.

## Django project shape

Use one Django project/config package plus bounded apps:

```text
config/
identity/
institutions/
knowledge/
visits/
records/
audit/
templates/
static/
tests/   # optional shared end-to-end tests only
```

Do not create `missions`, `teams`, `reporting` yet merely because they exist in the long-term design.

## Inside a bounded app

Prefer boring, discoverable structure:

```text
models.py
services.py
selectors.py
permissions.py
forms.py
views.py
urls.py
tests/
templates/<app>/
```

Split files only when size/cohesion justifies it.

### services.py
Commands/use cases and transaction boundaries.

Examples:
- create_local_institution
- create_checklist_version
- activate_checklist_version
- create_visit
- attach_checklist_snapshot
- finalize_visit

### selectors.py
Read/query operations that do not mutate state.

### permissions.py
Capability/scope decisions and reusable authorization predicates.

### views.py
HTTP orchestration only:
- parse request.
- call application service/query.
- map result/errors to response.

No important business rule may exist only in a view/template/JavaScript branch.

## Dependency rule

Presentation -> services/selectors -> models/domain rules.

Cross-app mutation goes through the owning app's service interface where practical.

Avoid circular imports and "utility" modules that secretly own domain logic.

## Frontend

### Design tokens
Central CSS variables for:
- typography.
- spacing.
- radii.
- surfaces.
- semantic colors.
- focus/error/success states.

### Components
Use reusable partials/components for:
- buttons/actions.
- forms/field errors.
- cards.
- tables/lists.
- status badges.
- page headers.
- confirmation dialogs.

### Replaceability rule
Templates may change dramatically without changing service behavior or tests of domain/application rules.

Do not encode permissions only through hidden buttons.

## Arabic / RTL

- `dir="rtl"` and Arabic-first layouts from the first page.
- semantic HTML order must remain sensible, not visually reversed hacks.
- dates displayed in a clear unambiguous format, initially `dd/mm/yyyy`.
- keyboard focus and error messaging must work in RTL.

## Error handling

Domain/application services raise explicit expected errors for:
- permission denied.
- invalid lifecycle transition.
- immutable record.
- snapshot conflict.
- validation failure.

Do not expose internal tracebacks to users.

## Database

- PostgreSQL is canonical.
- migrations are small and reviewable.
- no destructive migration without explicit migration/rollback reasoning.
- use transactions for lifecycle transitions.
- constraints for uniqueness and relational integrity.
- do not use database triggers for core business rules in Slice 01 unless a rule cannot be safely enforced otherwise.

## Tests

Every business rule gets a regression test.

At minimum before PR:
- Ruff.
- unit/domain/application tests.
- integration tests.
- permission matrix.
- Django system check.
- PostgreSQL test run.
- critical Playwright path when browser automation is introduced.

## Security

- CSRF protection remains enabled.
- POST/appropriate unsafe methods for mutations.
- object-level authorization server-side.
- no secrets committed.
- secure defaults documented for deployment.
- Admin authority must not create an impersonation shortcut.

## Simplicity rule

When two implementations satisfy the same invariant, prefer the one with:
- fewer moving parts.
- clearer ownership.
- easier testing.
- lower coupling.

Do not create abstraction solely because a future feature might need it.
