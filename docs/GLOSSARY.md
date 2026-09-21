# Glossary

- Status: **Canonical terminology baseline**

## Person
The real human being represented in the platform.

## Account
Authentication identity used to access the platform. An Account is not a professional Position.

## Position
Formal/professional position held by a Person, potentially time-bound.

Examples: Minister, Inspector General, Central Inspector, Field Inspector.

## Operational Role
Contextual temporary responsibility inside a Team/Mission.

Examples: leader, coordinator, rapporteur, field lead, reviewer.

## Capability
An action the subject may perform.

Examples: create institution, finalize own visit, assign mission, approve reference.

## Scope
The domain boundary within which a Capability applies.

Examples: OWN, NATIONAL, GEOGRAPHY(id), TEAM(id), INSTITUTION(id).

## Context
The Team, Mission, Organization or other business situation giving a role/authority its meaning.

## Admin
Highest administrative authority inside the application.  
Admin is not, by Admin status alone, a professional author of inspection findings.

## System Operator / Developer
Technical control-plane actor managing code, deployment, backups and technical configuration outside ordinary business hierarchy.

## Team
A work-group identity independent of its current members.

## TeamCycle
A time-bounded operational cycle of a recurring/seasonal Team.

## Mission
Work requested, proposed, opened or assigned. It describes what should be achieved and under what constraints.

## Assignment
A formal allocation of Mission responsibility to a Person/Team.

## Activity
Actual performed work. It may or may not originate from a Mission.

## Visit
A field-oriented Activity representing actual inspection/field execution.

## Knowledge Artifact
Conceptual category for versioned reusable knowledge such as checklists, references, indicators and guides. It does not require one generic database table.

## Checklist
Versioned structured inspection aid containing sections/items.

## Snapshot
Frozen copy/meaning captured for historical execution so later source changes cannot rewrite history.

## Finding
Professional observed fact/assessment recorded during work.

## Recommendation
Professional proposed action or improvement related to findings/work.

## Decision
Formal decision recorded in context where the actor has authority.

## Draft
Mutable, generally deletable pre-final state.

## Submit
Send to another workflow participant/review process; not automatically finalization.

## Finalize
Freeze a professional/business record into immutable history.

## Approve
Decision by authorized authority regarding acceptance of an item/proposal/version.

## Publish
Make an allowed/approved version usable/visible within an explicit scope.

## Archive
Retire from active use without destroying history.

## Amendment / Addendum
New historical record correcting/completing a finalized record without rewriting the original.

## Provenance
Ability to trace information to its author, source, time, version and context.

## Audit Event
Append-only technical/application trace of an action. It is not a substitute for business history.

## Semantic Zoom
Ability to move from overview/aggregate to detailed/source information and back, across different lenses.

## Vertical Slice
A small end-to-end usable product path crossing all needed layers, rather than building one technical layer in isolation.

## Increment
A bounded implementation unit inside a Vertical Slice that must pass verify/review/correct/reverify gates.

## Human Acceptance
Owner/user evaluation of practical usefulness, clarity, visual quality, freedom/rigidity and real workflow after machine quality gates pass.
