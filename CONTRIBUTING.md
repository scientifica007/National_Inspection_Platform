# Contributing / Executor Rules

This repository uses controlled implementation rather than open-ended feature development.

## Before changing code

Read:
1. `docs/DOCUMENTATION_INDEX.md`
2. `docs/PROJECT_STATE.md`
3. current increment specification/gate.

Do not implement deferred features.

## Clean-slate rule

Do not inspect, copy, compare, cherry-pick, import migrations/templates/tests/databases from previous `Inspector_Website_*` experiments unless the owner explicitly authorizes it in a documented decision.

## Change workflow

```text
bounded increment
→ implementation
→ automated verification
→ review
→ correction
→ re-verification
→ checkpoint
→ next increment
```

## Domain rule

If an implementation question requires inventing business policy:
- stop.
- document the ambiguity.
- request/obtain design resolution.

## Quality

Before an increment can pass:
- required tests pass.
- permission checks are server-side.
- no known blocking finding remains.
- docs reflect accepted changes.
- no secrets/real sensitive data are committed.

## Scope rule

"Future-proofing" is not permission to implement future features.

Prefer the smallest design that:
- satisfies current invariants.
- has clear extension seams.
- remains easy to maintain.

## Commit messages

Use clear intent-oriented messages, e.g.:
- `feat(identity): add person/account foundation`
- `test(visits): cover finalized mutation rejection`
- `fix(permissions): enforce object scope server-side`
- `docs: record S01-I01 checkpoint`

## Human acceptance

Do not claim product acceptance based only on automated tests.  
Human acceptance is a separate mandatory gate documented in `docs/HUMAN_ACCEPTANCE_PROTOCOL.md`.
