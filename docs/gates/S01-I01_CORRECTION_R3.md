# S01-I01 Correction Cycle — Review 3

- Increment: `S01-I01`
- PR: `#1`
- Reviewed head: `b94eb38b0ce61e6efed16cc26a9466e2ddd56f9c`
- Decision: **HOLD — CORRECTION REQUIRED (R3)**

## R2 closure

R2-B01…R2-B05 were independently re-reviewed and are closed as intended.

Evidence:
- PR remains draft/open.
- current head at review: `b94eb38`.
- current main is an ancestor of the branch.
- GitHub Actions run `35628657953`: success.
- PostgreSQL-backed suite: 162 passed.
- no S01-I02 module present.

## Blocking findings

| ID | Severity | Finding | Required correction |
|---|---|---|---|
| R3-B01 | High | bootstrap Platform Admin saves Person before Account and can orphan Person on failure | make bootstrap creation atomic/reuse AccountManager auto-Person path; add regression tests |
| R3-B02 | High | `create_person` is an ungated application identity mutation | require active Platform Admin actor or remove/reclassify from application service; test denial/allow paths |
| R3-B03 | Medium | README setup creates Django superuser but does not document first Platform Admin bootstrap | document safe technical bootstrap and distinction between superuser and Platform Admin |

## Non-blocking

- raw `QuerySet.update()` Person-binding bypass remains explicitly unsupported, as accepted in R2.
- product Platform Admin management UI remains deferred.
- AuditEvent coverage remains deferred to the audit increment.

## Authorized next action

OpenHands Cloud may perform a third **correction-only** pass on `build/slice-01`.

Prompt:
`docs/OPENHANDS_CORRECTION_PROMPT_S01_I01_R3.md`

## Exit condition

After correction:
- status remains `HOLD — RE-REVIEW REQUIRED`;
- independent review must close R3 findings;
- S01-I02 remains unauthorized.
