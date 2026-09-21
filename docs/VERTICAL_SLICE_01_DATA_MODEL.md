# Vertical Slice 01 — Concrete Data Model

- Status: **Reviewed baseline for implementation**
- Review: `docs/VERTICAL_SLICE_01_DATA_MODEL_REVIEW.md`

## Conventions

- UUID primary keys for business entities.
- UTC timestamps in storage; presentation uses configured local timezone.
- explicit `created_at`, `updated_at` for mutable objects where useful.
- finalized timestamps are separate from ordinary update timestamps.
- actor/person IDs are explicit for important actions.
- no hard-coded institution/checklist lists.
- database constraints reinforce, but do not replace, application/domain authorization.

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

Custom Django User from day one.

```text
Account
- id
- person_id -> Person (1:1 for Slice 01)
- username
- authentication fields
- active
- is_platform_admin
```

`is_platform_admin` grants application administration, not professional authorship.

### CapabilityGrant

Slice 01 deliberately keeps scope small.

```text
CapabilityGrant
- id: UUID
- account_id
- capability_code
- scope_kind: OWN | ALL
- valid_from nullable
- valid_until nullable
- delegable boolean
- granted_by_account_id
- revoked_at nullable
```

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

Capability identifiers correspond to stable application use cases and may be code constants; grants are data.

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
- updated_at
- archived_at nullable
```

Hard delete is allowed only when no finalized historical record depends on the Institution.

## knowledge

### Checklist

```text
Checklist
- id: UUID
- title
- owner_person_id
- lifecycle: LOCAL_ACTIVE | ARCHIVED
- created_at
- archived_at nullable
```

### ChecklistVersion

```text
ChecklistVersion
- id: UUID
- checklist_id
- version_number
- status: DRAFT | ACTIVE | ARCHIVED
- created_by_person_id
- created_at
- activated_at nullable
```

Rules:
- DRAFT editable/deletable.
- ACTIVE immutable.
- editing an ACTIVE checklist creates a new DRAFT version.
- Visit may snapshot only ACTIVE version.
- uniqueness: `(checklist_id, version_number)`.
- default current version is the highest/explicitly current ACTIVE version according to the application rule.

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

ChecklistItem rows belonging to ACTIVE versions are immutable.

## visits

### Visit

```text
Visit
- id: UUID
- owner_person_id
- institution_id nullable
- institution_snapshot: JSON
- title
- purpose nullable
- planned_date nullable
- status: DRAFT | FINALIZED
- created_at
- updated_at
- finalized_at nullable
- finalized_by_person_id nullable
```

The Institution snapshot stores only the historical display identity required to understand the Visit.

### VisitChecklistSnapshot

```text
VisitChecklistSnapshot
- id: UUID
- visit_id (1:1 in Slice 01)
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

Snapshot rows are copies and are never updated because the source Checklist changes.

While Visit is DRAFT, the user may replace the selected Checklist/version only when doing so will not orphan node-linked draft professional records. Slice 01 blocks replacement if such records exist.

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

While Visit is DRAFT, authorized owner edits are allowed.

When Visit becomes FINALIZED:
- Finding/Recommendation are immutable.
- update/delete commands reject server-side.

Amendment UI is deferred from Slice 01 but required before real official production/pilot data.

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

AuditEvent is append-only and is not canonical business history.

## Finalize Visit transaction

```text
BEGIN
  authorize visit.finalize.own
  lock/read current Visit
  assert Visit.status == DRAFT
  validate snapshot consistency
  validate child-record consistency
  set Visit.status = FINALIZED
  set finalized_at
  set finalized_by_person_id
  append AuditEvent
COMMIT
```

All later mutation commands must reject FINALIZED state in application/service logic. UI hiding alone is insufficient.

## Not modeled in Slice 01

- Team / TeamCycle
- Mission
- Assignment
- Approval/Publish
- advanced Delegation
- advanced geographic scope
- Report
- Dataset
- Amendment UI

These are intentionally deferred without changing their conceptual place in the broader Domain.
