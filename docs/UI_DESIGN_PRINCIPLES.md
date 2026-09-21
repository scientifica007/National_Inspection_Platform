# UI Design Principles

- Status: **Accepted design baseline**

## Goal

The interface must remain easy to redesign without destabilizing the backend/domain.

Visual acceptance is iterative: the first implementation is not expected to be the final visual design.

## Principles

### 1. Arabic/RTL first
- native RTL layout.
- semantic DOM order.
- readable Arabic typography.
- unambiguous dates, defaulting to `dd/mm/yyyy`.
- no visual hacks that break keyboard/screen-reader order.

### 2. Calm visual hierarchy
Prefer:
- restrained surfaces.
- clear grouping.
- predictable spacing.
- low visual noise.
- deliberate emphasis only for important actions/status.

Avoid:
- decorative complexity.
- excessive cards/badges.
- inconsistent colors.
- controls competing for attention.

### 3. Overview → Drill-down → Zoom
Dashboards and lists should offer:
- concise overview.
- clickable totals/categories.
- progressive disclosure.
- ability to reach source records.

Do not force all detail onto the first screen.

### 4. Freedom without ambiguity
Users should be free to choose legitimate workflows, while the interface clearly explains:
- what is optional.
- what is required.
- what is final.
- what cannot be undone.

### 5. Action discoverability
A page should not look operational while hiding all real actions elsewhere.

If an action exists:
- make its location predictable.
- show disabled/restricted state with reason when helpful.
- avoid silent disappearance when that creates confusion.

### 6. Empty states are part of the workflow
No required select/list should become a dead end without explanation.

Empty states must explain:
- why empty.
- what the user can do.
- whether they lack permission or prerequisites.

### 7. Draft vs Finalized must be visually unmistakable
Finalization must:
- explain consequences.
- require explicit confirmation.
- lead to clearly read-only presentation.

### 8. Componentized presentation
Use:
- Design Tokens.
- reusable components/partials.
- layout primitives.
- semantic status components.

Do not duplicate page-specific CSS patterns unnecessarily.

### 9. Business logic stays out of presentation
Templates/JavaScript may assist interaction, but:
- do not own authority rules.
- do not own lifecycle rules.
- do not own immutability.

### 10. Human acceptance controls final UX
Automated tests can verify behavior.  
The owner/user decides whether the interface is practically clear, comfortable and efficient.

## Replaceability test

A significant redesign passes the architecture test when:
- domain/application tests do not change.
- service contracts remain valid.
- no migration is needed solely for visual changes.
- only presentation/query-view-model adjustments are required unless the new UX introduces a real domain requirement.
