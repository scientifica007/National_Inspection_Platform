# M0 Status

## Current phase

**M0 — Foundation / Domain Design**

## Completed design work

- Product vision draft.
- Conceptual domain model.
- Core invariants.
- Replaceable modular architecture principle.
- Domain fitness scenarios.
- Scenario Review 01.
- Minimal Stable Core.
- Authority model.
- Lifecycle semantics.
- lifecycle profiles for Visit / KnowledgeArtifact / Institution.
- Initial implementation scope.
- Vertical Slice 01.
- concrete data model draft for Vertical Slice 01.
- module dependency map.
- Test strategy.
- proposed initial stack.
- AI executor readiness gate.

## Findings from Scenario Review 01

The architecture remains viable. Four refinements were identified:

1. TeamCycle for recurring/seasonal team instances.
2. explicit Scope intersection semantics.
3. retention rule for local entities referenced by finalized history.
4. separation between Admin authority and professional authorship.

The first three have a proposed design. The fourth is an owner-level Domain decision.

## Open before handoff

1. Resolve the decisions in `docs/OPEN_DECISIONS.md`.
2. Accept/revise ADR-0002 initial stack.
3. Apply TeamCycle + Scope refinements to the main Domain Model.
4. Review the concrete Vertical Slice 01 data model for over-modeling and missing constraints.
5. Convert the accepted slice into an executor specification/prompt.
6. Run final contradiction/over-abstraction review.
7. Mark Product Vision/Invariants as accepted rather than draft.

## Handoff state

**NOT READY**

The design is approaching executor-ready state, but the remaining decisions affect permissions and implementation shape and should not be guessed by an executor.
