# Module Dependency Map

## الهدف

الحفاظ على Modular Monolith حقيقي بدل مجلدات منفصلة شكليًا تتشابك داخليًا.

## Modules

```text
identity
geography
organization
institutions
knowledge
missions
visits
records
reporting
audit
```

## Dependency direction

```text
identity      geography
   │             │
   ├──────┐      │
   ▼      ▼      ▼
organization   institutions
   │             │
   └──────┬──────┘
          ▼
       missions  ◄──── knowledge
          │             │
          └──────┬──────┘
                 ▼
               visits
                 │
                 ▼
               records
                 │
                 ▼
              reporting

audit receives events from application use-cases and must not become a source of business truth.
```

## Rules

### identity
May not depend on business modules.

### geography
May not depend on identity or work modules.

### organization
May depend on identity and geography for membership/placement semantics.

### institutions
May depend on geography and organization; creator/owner IDs come from identity contracts.

### knowledge
May depend on identity for authorship/ownership. It should not depend on visits.

### missions
May depend on identity, organization, geography, institutions, and knowledge contracts.

### visits
May depend on identity, institutions, knowledge snapshots, and optionally mission identifiers/contracts.

A Visit must also exist without Mission.

### records
May depend on visits and identity. It owns professional finalized records and amendment rules.

### reporting
Is downstream/read-oriented. It consumes public query contracts/read models and must not mutate upstream domain state.

### audit
Stores technical/application audit events. It does not decide business lifecycle and is not a replacement for Record history.

## Cross-module interaction

Preferred order:

1. Application service calls public service/use-case of another module.
2. Stable identifiers may cross module boundaries.
3. Read projections may join across modules in a dedicated query layer when this materially simplifies dashboards.
4. Direct mutation of another module's tables is forbidden.
5. Cross-module ORM imports are minimized and documented; stable foreign keys are allowed where the relationship is fundamental and extraction is not a present goal.

## No circular dependencies

If A depends on B, B must not import/use A's application/domain layer.

When a two-way business interaction appears:
- move orchestration to application layer, or
- emit a domain/application event, or
- extract the truly shared concept.

Do not solve cycles by hidden service locators or global imports.

## Presentation

Presentation depends on Application/query contracts only.

```text
Web UI ─┐
API    ─┼──> Application / Queries ──> Domain modules
Future ─┘
```

No Domain module depends on Django templates, CSS, HTMX, REST serializers, or browser-specific code.
