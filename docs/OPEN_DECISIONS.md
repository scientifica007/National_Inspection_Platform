# Decisions Before AI Executor Handoff

All previously open owner-level decisions for the first implementation have now been resolved.

## OD-001 — Admin vs Professional Authorship

### Decision
**ACCEPTED — Admin authority does not itself grant professional authorship.**

Admin has the broadest administrative authority inside the application, but authoring/finalizing professional inspection findings requires an appropriate professional capability/position attached to the same real person.

One person may therefore be both:
- Admin for platform administration, and
- Inspector/Minister/etc. for professional acts.

Every action keeps its true actor and context.

Admin can create and manage missions, users, permissions, scopes, configuration and workflows, and can see application data according to the platform-wide administrative policy. Admin may not impersonate another professional or rewrite that person's finalized professional record.

**Approved by owner: 2026-09-21.**

---

## OD-002 — Initial Technical Stack

### Decision
**ACCEPTED.**

- Python 3.12
- Django 5.2 LTS
- PostgreSQL
- Django Templates
- CSS Design Tokens/components
- minimal JavaScript
- HTMX only when useful
- pytest/pytest-django
- Playwright for critical browser paths
- Ruff
- CI on PRs

**Approved by owner: 2026-09-21.**

---

## OD-003 — Amendment availability before production

### Decision
**ACCEPTED.**

Development and human acceptance with test data may proceed before Amendment UI exists.

No production/pilot using real official finalized records may begin until correction-by-amendment/addendum is implemented and tested.

**Approved by owner: 2026-09-21.**

---

## OD-004 — First Slice breadth

### Decision
**ACCEPTED.**

The first executor builds only **Solo Inspector Field Visit**.

Teams, Missions and Assignments remain architecturally planned but implementation-deferred.

**Approved by owner: 2026-09-21.**

## Result

There are no owner-level open decisions blocking implementation of Vertical Slice 01.
