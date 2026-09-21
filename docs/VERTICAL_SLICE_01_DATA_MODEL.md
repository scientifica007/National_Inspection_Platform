# Vertical Slice 01 — Concrete Data Model Draft

## Status

**DESIGN DRAFT — no migrations yet**

The purpose is to remove implementation ambiguity before an executor writes code.

## Conventions

- UUID primary keys for business entities.
- UTC timestamps in storage; presentation uses configured local timezone.
- explicit `created_at`, `updated_at` for mutable drafts where useful.
- finalized timestamps are separate from ordinary update timestamps.
- actor IDs are stored explicitly for important actions.
- no hard-coded institution/checklist lists.

## identity

### Person

```text
Person
- id: UUID
- display_name
- active
- created_at
```

### Account

For Django implementation this is expected to be a custom User model from day one.

```text
Account
- id
- person_id -> Person
- username
- authentication fields
- active
- is_platform_admin
```

`is_platform_admin` is administrative access, not professional authorship.

### CapabilityGrant

```text
CapabilityGrant
- id: UUID
- account_id
- capability_code
- scope_kind
- scope_id nullable
- valid_from nullable
- valid_until nullable
- delegable boolean
- granted_by_account_id
- revoked_at nullable
```

For Slice 01, scope kinds may be only:
- OWN
- ALL

Do not build the full scope engine yet.

Example capability codes:
- institution.create.local
- institution.read.own
- knowledge.create.local
- knowledge.read.own
- visit.create
- visit.read.own
- visit.update.own_draft
- visit.finalize.own
- visit.read.all
- account.manage

Capability identifiers correspond to real use cases and therefore may be code constants; grants are data.

## institutions

### Institution

```text
Institution
- id: UUID
- name
- lifecycle: LOCAL_ACTIVE | ARCHIVED
- created_by_person_id
- local_owner_person_id
- created_at
- archived_at nullable
```

No national institution registry is required in Slice 01.

Hard delete is allowed only if no finalized historical record depends on it. If historical dependency exists, archive/tombstone instead.

## knowledge

### Checklist

```text
Checklist
- id: UUID
- title
- owner_person_id
- lifecycle: LOCAL_ACTIVE | ARCHIVED
- current_version_number
- created_at
```

### ChecklistVersion

```text
ChecklistVersion
- id: UUID
- checklist_id
- version_number
- created_by_person_id
- created_at
- frozen boolean
```

A version used by a Visit snapshot is never rewritten.

### ChecklistItem

```text
ChecklistItem
- id: UUID
- version_id
- stable_item_key: UUID
- parent_item_id nullable
- kind: SECTION | ITEM
- label
- position
```

Hierarchy is supported without forcing it on the first UI.

## visits

### Visit

```text
Visit
- id: UUID
- owner_person_id
- institution_id nullable
- institution_snapshot: JSON
- title/purpose
- planned_date nullable
- status: DRAFT | FINALIZED
- created_at
- finalized_at nullable
- finalized_by_person_id nullable
```

The institution snapshot stores at least immutable display identity needed to understand the historical visit even if the local source is later archived.

### VisitChecklistSnapshot

```text
VisitChecklistSnapshot
- id: UUID
- visit_id
- source_checklist_id nullable
- source_version_id nullable
- title_snapshot
- created_at
```

### VisitSnapshotNode

```text
VisitSnapshotNode
- id: UUID
- snapshot_id
- source_item_key nullable
- parent_node_id nullable
- kind
- label
- position
```

These rows are immutable once created except while the Visit is still in a creation transaction before exposure to the user. Updating the source Checklist never updates these nodes.

## records

### Finding

```text
Finding
- id: UUID
- visit_id
- snapshot_node_id nullable
- author_person_id
- text
- created_at
- updated_at
```

### Recommendation

```text
Recommendation
- id: UUID
- visit_id
- snapshot_node_id nullable
- author_person_id
- text
- created_at
- updated_at
```

While Visit is DRAFT, owner-authorized edits are allowed.

When Visit becomes FINALIZED:
- Finding/Recommendation are immutable.
- update/delete commands reject server-side.

Amendment is intentionally deferred from UI in Slice 01; the first slice therefore warns clearly before finalization. The generic correction mechanism is introduced before production use.

## audit

### AuditEvent

```text
AuditEvent
- id: UUID
- actor_account_id nullable
- actor_person_id nullable
- action_code
- target_type
- target_id
- occurred_at
- metadata: JSON
```

AuditEvent is append-only and is not the canonical business history.

## Transaction: finalize visit

```text
BEGIN
  authorize visit.finalize.own
  assert Visit.status == DRAFT
  validate required internal consistency
  set Visit.status = FINALIZED
  set finalized_at
  set finalized_by_person_id
  append AuditEvent
COMMIT
```

All subsequent mutation commands must check status in the application/domain layer.

## Not modeled yet

- Team
- Mission
- Assignment
- Approval/Publish
- Delegation UI
- advanced geographic scope
- Report
- Dataset
- Amendment UI

These remain part of the broader Domain Model but are deliberately outside Slice 01.
