# Codex Executor Prompt — S01-I02 Local Institutions

You are the controlled implementation executor for **National Inspection Platform**.

Repository:
`scientifica007/National_Inspection_Platform`

Increment:
`S01-I02 — Local Institutions`

Dedicated branch:
`build/s01-i02`

You are replacing OpenHands **for this increment only** as a controlled executor experiment. Do not compare against OpenHands implementation history and do not change the review standard.

## 0. Mandatory starting state

Start only from the current accepted `main` baseline.

S01-I01 is already:
- independently reviewed;
- PASS;
- merged to `main`.

Do not continue from the old `build/slice-01` branch.

At the start:
1. fetch `origin/main`;
2. verify `build/s01-i02` starts from current `origin/main`;
3. record the exact main SHA you started from;
4. inspect the current implementation before editing.

Do not rewrite history.

## 1. Read source of truth before coding

Read in this order:

1. `docs/DOCUMENTATION_INDEX.md`
2. `docs/PROJECT_STATE.md`
3. `docs/INVARIANTS.md`
4. accepted ADRs in `decisions/`
5. `docs/PRODUCT_VISION.md`
6. `docs/AUTHORITY_MODEL.md`
7. `docs/DOMAIN_MODEL.md`
8. `docs/LIFECYCLE_SEMANTICS.md`
9. `docs/LIFECYCLE_PROFILES.md`
10. `docs/VERTICAL_SLICE_01.md`
11. `docs/VERTICAL_SLICE_01_DATA_MODEL.md`
12. `docs/VERTICAL_SLICE_01_DATA_MODEL_REVIEW.md`
13. `docs/MODULE_DEPENDENCY_MAP.md`
14. `docs/ENGINEERING_CONVENTIONS.md`
15. `docs/SECURITY_AND_DATA_GOVERNANCE.md`
16. `docs/REVIEW_AND_CHANGE_POLICY.md`
17. `docs/CONTROLLED_IMPLEMENTATION_CYCLE.md`
18. `docs/SLICE_01_INCREMENT_PLAN.md`
19. `docs/S01_I02_EXPECTED_OUTPUTS.md`
20. `docs/gates/S01-I02_GATE.md`

When documents appear to conflict, use the precedence in `DOCUMENTATION_INDEX.md`. If a true conflict remains, STOP and report it. Do not invent policy.

## 2. Clean-slate / independence rule

Never inspect, read, compare, copy, cherry-pick or import from:
- Inspector_Website_001
- Inspector_Website_002
- Inspector_Website_003
- Inspector_Website_004
- Inspector_Website_005

Do not use prior experimental screenshots, databases, migrations, architecture or tests.

The accepted `main` of **National_Inspection_Platform** is the only implementation baseline.

## 3. Scope — implement S01-I02 only

Build:
- `institutions` Django app.
- local Institution model/lifecycle.
- create/list/detail/edit/archive/delete application behavior.
- server-side object permissions.
- owner vs other-inspector vs Platform Admin read-visibility matrix.
- minimal Arabic RTL Institution UI.
- migration.
- tests.
- implementation notes/gate evidence.

Do not start S01-I03.

## 4. Institution model

Follow `docs/S01_I02_EXPECTED_OUTPUTS.md` exactly.

Expected shape:
- UUID PK.
- name.
- lifecycle `LOCAL_ACTIVE | ARCHIVED`.
- created_by_person.
- local_owner_person.
- created_at / updated_at.
- archived_at nullable.

No institution list in code/config.
No ownership transfer.
No shared/national registry workflow.

## 5. Authority — reuse, do not reinvent

The S01-I01 authority foundation is accepted and heavily regression-tested.

Use it.

Do not create a second actor resolver, permission engine, role hierarchy or policy framework.

The increment-specific permission contract is defined in:
`docs/S01_I02_EXPECTED_OUTPUTS.md`

Key rules:
- create: existing `institution.create.local` capability;
- owner read: existing `institution.read.own` capability;
- owner edit/archive/delete: persisted real actor + stored local ownership + existing `institution.create.local` capability;
- active Platform Admin: read visibility across Institutions;
- Platform Admin status alone: **no edit/archive/delete authority** over another Person's local Institution;
- no impersonation;
- created_by/local_owner come from the stored acting Person, never a form field.

Use the persisted actor/identity rules already implemented in `identity.permissions`.

## 6. Lifecycle

Implement only:

```text
LOCAL_ACTIVE
  ├── edit
  ├── hard delete when retention permits
  └── archive -> ARCHIVED
```

No unarchive.

Archived:
- readable when visibility permits;
- not editable.

Hard delete:
- explicit, owner-authorized;
- allowed for currently unreferenced local Institution;
- map relational `ProtectedError` to an explicit retention/domain error;
- do not create `visits` just to model future finalized dependencies.

## 7. Application structure

Keep the boring bounded-app structure preferred by engineering conventions:

```text
institutions/
  models.py
  services.py
  selectors.py
  forms.py
  views.py
  urls.py
  tests/
  templates/institutions/
```

A small `permissions.py` is acceptable only for Institution-specific predicates; it must delegate identity/capability truth to `identity.permissions`.

Mutation business rules belong in services/domain logic, not only views/forms/templates.

Selectors are read-only.

Presentation must not directly mutate models.

## 8. UI

Add a minimal usable Arabic RTL flow:
- My Institutions list.
- create.
- detail.
- edit.
- archive.
- hard-delete confirmation/action.

Reuse existing layout, design tokens and components.

Do not perform a broad visual redesign.

Forms must not expose:
- owner;
- creator;
- lifecycle internals;
- archived_at;
- timestamps.

All destructive actions must be explicit and CSRF-protected.

## 9. Test before claiming completion

Implement the full matrix in `docs/S01_I02_EXPECTED_OUTPUTS.md`.

At minimum test:
- model/lifecycle.
- owner/other/Admin visibility.
- owner/other/Admin mutation denial/allow behavior.
- missing capability.
- inactive/fabricated/borrowed/stale actors where relevant.
- archived mutation rejection.
- hard-delete success.
- protected-delete/retention error mapping.
- no hard-coded Institution data.
- S01-I01 regression suite remains green.

Do not count tests as proof by themselves; inspect whether they actually fail against the defect they are meant to guard.

## 10. Verification

Run at minimum:

```text
ruff check .
ruff format --check .
python manage.py check
python manage.py makemigrations --check --dry-run
pytest -q
```

Requirements:
- full suite against PostgreSQL.
- apply the full migration chain to a freshly created empty PostgreSQL database.
- confirm the test backend is PostgreSQL.
- no migration drift.
- no secrets/DB dumps/real data.
- CI green on the exact final pushed head.

If PostgreSQL is unavailable, restore/provision it if the environment permits. Do not silently substitute SQLite.

## 11. Git / PR

Work only on:
`build/s01-i02`

Use small coherent commits.

Create a **draft PR** targeting `main` after implementation is ready for review.

PR title:
`S01-I02 — Local Institutions`

PR body must state:
- starting main SHA;
- scope implemented;
- migration;
- permission matrix;
- exact verification results;
- test count;
- deviations, if any;
- risks/limitations;
- explicit confirmation that S01-I03 was not started.

Do not merge.
Do not enable auto-merge.

## 12. Executor-owned docs

Create/update:
- `docs/IMPLEMENTATION_NOTES_S01_I02.md`
- `docs/gates/S01-I02_GATE.md` implementation evidence

Do not modify reviewer/maintainer state to claim PASS:
- do not mark `docs/PROJECT_STATE.md` PASS for S01-I02;
- do not create a PASS checkpoint;
- do not authorize S01-I03.

End gate must be:

`HOLD — RE-REVIEW REQUIRED`

## 13. Stop conditions

STOP rather than improvising if:
- a source-of-truth conflict changes Institution ownership/lifecycle meaning;
- implementing retention requires inventing Visit/finalization semantics;
- a destructive migration becomes necessary;
- a new capability taxonomy appears necessary beyond the explicit S01-I02 contract;
- a future module seems necessary only to make this increment work.

## 14. Final report

When finished, report:
- starting `main` SHA;
- branch;
- commits;
- final head SHA;
- changed modules/files;
- exact Institution lifecycle behavior;
- exact permission/visibility matrix;
- migration file(s);
- new tests and full suite count;
- fresh PostgreSQL migration evidence;
- CI run/result;
- no-secret/no-real-data check;
- scope confirmation;
- draft PR number/link.

Then STOP.

Do not start S01-I03 and do not self-declare PASS.
