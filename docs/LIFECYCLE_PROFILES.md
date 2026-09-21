# Lifecycle Profiles — First Domain Specialization

## الهدف

تطبيق Lifecycle Semantics العامة على ثلاثة مفاهيم مختلفة دون افتراض أن لكل شيء workflow واحدًا.

## Visit

```text
DRAFT
  └── FINALIZE ──> FINALIZED
```

DRAFT:
- editable/deletable by authorized owner.
- may change institution/purpose/scope.
- findings/recommendations editable.

FINALIZED:
- read-only historical execution.
- no destructive update/delete.
- later correction via Amendment (future slice).

No APPROVE is required merely for an inspector to own his professional observation.

## KnowledgeArtifact / Checklist

Conceptual lifecycle:

```text
LOCAL_DRAFT
  ├── delete
  └── ACTIVATE_LOCAL ──> LOCAL_ACTIVE
                         ├── new version
                         ├── archive
                         └── PROPOSE ──> PROPOSED
                                          ├── reject
                                          └── approve/publish by scope
```

Slice 01 implements only local creation/use and version snapshot behavior. Proposal/approval/publish are deferred.

## Institution

Conceptual lifecycle:

```text
LOCAL_ACTIVE
  ├── edit while not historically frozen
  ├── propose for shared registry
  └── archive
```

An Institution is not a professional observation. Its name/details may evolve.

Historical Visits therefore store institution snapshot data needed to preserve historical meaning.

Hard deletion is allowed only while no finalized historical dependency exists.

## Key distinction

"Immutable history" applies to historical execution records and snapshots, not to every master-data row forever.

We preserve:
- historical meaning through snapshots/versioning.
- current reality through editable/versioned master data.
