# Vertical Slice 01 — Data Model Review

- Status: **Passed with refinements**
- Date: 2026-09-21

## Review question

هل النموذج المقترح لأول Vertical Slice صغير بما يكفي للبناء والصيانة، وقوي بما يكفي لحماية القواعد الأساسية دون Over-modeling؟

## Result

**PASS WITH REFINEMENTS**

No additional Aggregate Root is required.

## Accepted simplifications

### Capability scope
Vertical Slice 01 implements only:
- `OWN`
- `ALL`

No generic polymorphic scope reference is implemented yet. The broader Scope model remains conceptual until Missions/Teams/Geography need it.

### No generic Record table
Slice 01 may use explicit `Finding` and `Recommendation` models.

The conceptual `Record` is a domain category, not a requirement to create a generic database table.

### No generic KnowledgeArtifact table
Slice 01 uses explicit `Checklist` / `ChecklistVersion`.

A common Knowledge abstraction can be introduced when a second or third knowledge type proves the shared lifecycle is real.

This avoids premature inheritance.

## Required refinements

### 1. Checklist versions are immutable once activated

Use:

```text
Checklist
  └── ChecklistVersion
        status = DRAFT | ACTIVE | ARCHIVED
        └── ChecklistItem
```

Rules:
- DRAFT version editable/deletable.
- ACTIVE version immutable.
- editing an active checklist creates a new DRAFT version.
- a Visit can snapshot only an ACTIVE version.
- only one current ACTIVE version is exposed as the default per Checklist.
- old active versions remain readable for provenance.

### 2. Visit snapshot replacement

While Visit is DRAFT:
- user may intentionally replace the selected checklist/version.
- replacement rebuilds the Visit snapshot transactionally.
- any draft Finding/Recommendation attached to removed snapshot nodes must not be silently remapped.
- implementation must block replacement when it would orphan draft records, or require explicit deletion/reconciliation.

For Slice 01, safest implementation:
**block replacement if node-linked draft records already exist.**

### 3. Institution snapshot

When a Visit selects an Institution, store a small historical snapshot at least containing:
- institution id at time of selection.
- display name.
- any stable local identifier exposed to the user.

Do not copy every Institution field.

### 4. Finalization transaction

Finalization must atomically:
- authorize.
- validate Visit is DRAFT.
- validate snapshot consistency.
- lock the Visit row as appropriate.
- set FINALIZED + finalized metadata.
- make child professional records immutable by rule.
- append audit event.

### 5. Deletion policy

Hard delete:
- Draft Visit: yes, by authorized owner.
- Draft ChecklistVersion: yes if unused.
- Institution: only if no finalized history depends on it.
- Active ChecklistVersion: no; archive/retire semantics.
- Finalized Visit/Finding/Recommendation: no.

## Conclusion

The Slice 01 model is neither missing a foundational entity nor requiring a generic framework.

Proceed with explicit Django models plus application services and strong server-side invariant checks.
