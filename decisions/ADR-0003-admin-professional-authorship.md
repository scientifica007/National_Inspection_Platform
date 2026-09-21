# ADR-0003 — Administrative Authority and Professional Authorship

- Status: **Accepted**
- Date: 2026-09-21
- Owner approval: 2026-09-21

## Context

The platform needs an Admin with the broadest authority inside the application. At the same time, professional inspection findings must preserve authorship, independence and historical provenance.

## Decision

Administrative authority and professional authorship are independent dimensions.

An Admin may:
- manage accounts and permissions.
- configure application data and scopes.
- see application data under platform-wide administrative authority.
- create and manage Missions/Assignments when those modules are implemented.
- perform any administrative use case explicitly granted to Admin.

Admin status alone does **not** allow the account to:
- author a professional finding as another person.
- impersonate an inspector.
- rewrite or delete another person's finalized professional record.

If the same Person also holds a professional Position/Capability, that Person may perform professional work in that capacity. The actor remains the real Person and the action context records the professional capability used.

## Consequences

- One Person may simultaneously have administrative and professional capabilities.
- UI may expose different workspaces/actions based on context, but identity remains single and explicit.
- "higher authority can do lower-level professional work" is implemented through explicit professional capability profiles, not impersonation.
- immutable finalized records remain protected even from Admin destructive editing.
