# Decision Register

- Updated: 2026-09-21

## Accepted architecture decisions

### ADR-0001 — Modular Monolith with Replaceable Interfaces
Status: Accepted.

Key effect:
- domain/application isolated from presentation/infrastructure.
- no microservices initially.
- replaceability comes from boundaries/contracts.

### ADR-0002 — Initial Implementation Stack
Status: Accepted.

Stack:
- Python 3.12.
- Django 5.2 LTS.
- PostgreSQL.
- Django Templates.
- Design Tokens/components.
- minimal JS / optional HTMX.
- pytest/pytest-django.
- Playwright for critical browser flows.
- Ruff + CI.

### ADR-0003 — Administrative Authority and Professional Authorship
Status: Accepted.

Key effect:
- Admin has broad administrative power.
- Admin is not automatically a professional author.
- no impersonation.
- the same Person may hold Admin and professional capabilities concurrently.

## Accepted delivery decisions

- M0 complete.
- Vertical Slice 01 is the first implementation target.
- Slice 01 is split into S01-I01 … S01-I07.
- every increment uses implement → verify → review → correct → reverify.
- Human Acceptance occurs only after machine gates pass.
- no official real-record production before Amendment/Addendum exists.

## Accepted independence rule

The new platform is a clean-slate implementation.

Previous Inspector_Website_* repositories:
- may inform lessons already captured in these docs.
- must not be inspected/copied/cherry-picked by the executor unless a future explicit owner decision changes this rule.

## Open decisions

No owner-level decision currently blocks **S01-I01**.

Future milestones will create new design gates and decisions when they become active.

## Historical note

`OPEN_DECISIONS.md` records the questions that were open before the 2026-09-21 owner approval. It is retained as historical context; this file is the current summary.
