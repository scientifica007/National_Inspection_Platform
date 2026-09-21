# S01-I01 Residual Correction — R4.1

- Increment: `S01-I01`
- PR: `#1`
- Reviewed head: `ead46986a3d220ee69e3f18688339000ae7491a1`
- Decision: **HOLD — MINIMAL RESIDUAL CORRECTION REQUIRED (R4.1)**

## R4 re-review result

R4-B02 is closed.

R4-B01 is substantially corrected but has one residual case.

### Residual finding

| ID | Severity | Finding | Required correction |
|---|---|---|---|
| R4-B01-R | High | an unsaved `Account` may carry an explicit PK copied from a real Platform Admin; current code treats `pk != None` as sufficient before querying the privileged row | reject Django model instances still in unsaved/adding state even when an explicit PK is present; keep current-row active/admin lookup |

Why this matters:
- a fabricated unsaved Account can borrow the PK of a real admin;
- a service can then authorize the mutation and attribute provenance to the real admin's FK id;
- this violates Actor Always Known / Identity Cannot Be Borrowed.

## Evidence at review

- PR #1 draft/open/unmerged.
- head `ead4698`.
- current `main` is an ancestor.
- GitHub Actions green.
- PostgreSQL-backed suite: 218 passed.
- no S01-I02 module present.
- R4-B02 PR-summary correction is complete.

## Authorized action

One minimal residual correction pass only.

Prompt:
`docs/OPENHANDS_CORRECTION_PROMPT_S01_I01_R4_1.md`

## Exit condition

- gate remains `HOLD — RE-REVIEW REQUIRED`;
- independent reviewer rechecks the explicit-PK unsaved actor case;
- S01-I02 remains unauthorized.
