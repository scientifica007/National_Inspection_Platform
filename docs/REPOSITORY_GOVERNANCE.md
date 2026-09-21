# Repository Governance

- Status: **Baseline**
- Updated: 2026-09-21

## Branch roles

### main
Accepted design baseline and reviewed implementation checkpoints.

Direct uncontrolled feature development on `main` is not allowed by project policy.

### build/slice-01
Authorized implementation branch for Vertical Slice 01.

The executor starts with S01-I01 only.

Future slices receive their own bounded branch/gate.

## Pull requests

Implementation changes should enter `main` through a reviewed PR once code exists.

A PR should include:
- increment ID.
- scope.
- tests/evidence.
- migrations.
- review findings and correction status.
- checkpoint decision.

## Main branch protection

At the time this document was written, GitHub reports `main` as **not protected**.

Before routine implementation merges begin, repository settings should be reviewed to consider:
- require pull request before merge.
- require passing CI/status checks.
- prevent force pushes.
- prevent branch deletion.
- preserve owner emergency access only if deliberately chosen.

This is a repository governance action, not a Domain requirement.

## Merge policy

Merge only after:
- increment gate PASS.
- required CI green.
- blocking review findings resolved.
- documentation/checkpoint updated.

Preferred merge style may be chosen when implementation begins, but history must remain auditable.

## Tags/releases

Use tags/releases only for meaningful accepted checkpoints, not every commit.

Suggested future pattern:
- `slice-01-human-acceptance`
- `pilot-v0.1`
- `v1.0.0`

## Repository contents

Public repository must contain:
- source.
- tests.
- synthetic fixtures.
- architecture/docs.
- safe examples.

It must not contain:
- production secrets.
- real confidential inspection evidence.
- production database dumps.
- unredacted personal datasets.

## Automation permissions

CI/workflows should receive minimum permissions required.

Do not grant write tokens broadly when read/test permissions are sufficient.
