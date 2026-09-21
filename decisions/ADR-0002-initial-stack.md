# ADR-0002 — Initial Implementation Stack

- Status: **Accepted**
- Date: 2026-09-21
- Owner approval: 2026-09-21

## Context

The first implementation must optimize for:
- maintainability.
- straightforward local development on Ubuntu.
- strong server-side permissions and transactions.
- Arabic RTL.
- repeated visual redesign without rewriting domain rules.
- easy handoff to coding agents.
- low operational complexity.

## Decision

### Backend
- Python 3.12
- Django 5.2 LTS
- PostgreSQL for canonical deployment/database behavior
- SQLite may be used only for lightweight local smoke work if tests also run against PostgreSQL where database behavior matters.

### Presentation
- Django Templates for the initial web UI.
- semantic HTML.
- CSS custom properties / Design Tokens.
- small reusable template components.
- minimal vanilla JavaScript.
- HTMX only where it materially simplifies interaction; it is not mandatory infrastructure.

### Testing
- pytest + pytest-django.
- browser/system tests only for critical user paths.
- Playwright as the preferred browser automation tool when introduced.
- permission matrix tests at application/request level.

### Quality
- Ruff for lint/format.
- type hints in application/domain services.
- CI on pull requests.

## Why server-rendered first?

A SPA is not required to make the frontend replaceable.

Replaceability comes from:
- domain/application independence.
- query/view-model contracts.
- componentized presentation.
- no business logic in templates.
- explicit HTTP/use-case boundaries.

Server-rendering keeps the first implementation smaller, easier to debug, and easier to maintain. A REST/JSON API or alternate frontend can be added later as a new Presentation Adapter.

## Why Django?

- mature authentication/security ecosystem.
- strong ORM and transaction support.
- admin tooling can assist technical administration without becoming the product UI.
- well suited to a modular monolith.
- lowers implementation and maintenance cost for the expected product shape.

## Why not a frontend framework now?

React/Vue/etc. would add build/tooling and state-management complexity before the UX requires it.

They remain valid future Presentation Adapters if later UX needs justify them.
