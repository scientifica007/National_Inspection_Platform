# Correction Cycle Template

Use after a reviewer returns `HOLD — CORRECTION REQUIRED`.

## Increment
- ID:
- reviewed commit:

## Blocking findings to correct

| Finding ID | Root cause | Correct layer | Planned fix | Regression test |
|---|---|---|---|---|
| | | | | |

## Correction rules

- fix the root cause, not only the visible symptom.
- permission defects are fixed server-side.
- domain defects are fixed in domain/application layer.
- UI may communicate a rule but must not be its sole enforcement.
- migration/data defects require explicit safety treatment.
- no unrelated cleanup/refactor unless required to fix the finding.

## Re-verification

Record:
- lint/static result.
- targeted regression tests.
- full relevant test suite.
- PostgreSQL result where applicable.
- Django system/migration checks.
- browser/system checks where applicable.

## Reviewer closure

Each original blocking finding must be marked:
- RESOLVED, with evidence; or
- NOT RESOLVED.

No new increment starts until reviewer returns:

`PASS — NEXT INCREMENT ALLOWED`
