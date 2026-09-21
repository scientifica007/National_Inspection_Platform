# Open Decisions Before AI Executor Handoff

Only decisions that materially affect implementation belong here.

## OD-001 — Admin vs Professional Authorship

### Question
Does an account with Admin authority, **only because it is Admin**, have the right to author/finalize professional inspection findings?

### Recommended decision
**No.**

Admin should have the broadest administrative authority inside the application, but professional authorship should require a professional capability/position attached to the same real person.

Therefore one person may be both:
- Admin for platform administration, and
- Inspector/Minister/etc. for professional acts.

The same person can then perform both kinds of actions, but each action keeps its true actor/context.

### Reason
This preserves:
- professional independence.
- provenance.
- non-impersonation.
- clear audit semantics.

Admin can still create missions, manage users, configure scopes, see all permitted data, and manage workflows.

**Status: OPEN — owner approval required.**

---

## OD-002 — Initial Technical Stack

### Proposed
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

### Reason
Lowest useful complexity while keeping frontend replaceable and backend modular.

**Status: OPEN — owner approval required.**

---

## OD-003 — Amendment availability before production

Vertical Slice 01 proves immutability but does not yet expose Amendment UI.

### Recommended decision
No production/pilot with real official records until correction-by-amendment exists.

Development/human acceptance with test data can proceed without it, provided finalization warns that the test record is immutable.

**Status: RECOMMENDED — confirm before production planning.**

---

## OD-004 — First Slice breadth

### Proposed
The first executor builds only the Solo Inspector Field Visit slice.

Teams/Missions/Assignments stay deferred even though they are central to the final product.

### Reason
This verifies the architecture with the smallest meaningful end-to-end product before adding organizational complexity.

**Status: OPEN — owner approval required.**
