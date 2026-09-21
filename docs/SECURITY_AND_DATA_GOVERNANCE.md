# Security and Data Governance

- Status: **Baseline policy**
- Updated: 2026-09-21

## 1. Repository data policy

The GitHub repository is public.

Therefore:
- no real personal data.
- no official confidential operational data.
- no production database.
- no access tokens, API keys, bearer tokens, passwords or secrets.
- no uploaded evidence from real inspection cases.
- demo fixtures must be fictional/synthetic.

If real data is ever required for testing, it must be kept outside the public repository and governed explicitly.

## 2. Identity and authentication

- custom Django User/Account from day one.
- secure password handling through Django authentication primitives.
- no shared production accounts.
- Account represents access identity; Person represents the human.
- disabling an Account must not delete Person/business history.

## 3. Authorization

Authorization is server-side.

Rules:
- deny sensitive actions unless capability/scope permits.
- object-level authorization required.
- ownership, visibility and authority are distinct.
- Admin status does not imply professional authorship.
- no impersonation shortcut.
- no reliance on hidden buttons for enforcement.

## 4. Professional record integrity

Finalized professional records:
- cannot be destructively edited.
- cannot be deleted by ordinary/Admin application actions.
- later corrections use Amendment/Addendum.
- actor, author, timestamps and provenance are retained.

## 5. Audit vs business history

AuditEvent:
- append-only.
- captures important application/security actions.
- supports investigation.

Business history:
- FinalizedRecord/version/Amendment semantics.
- remains the canonical professional history.

Audit logs must not be treated as a substitute for domain history.

## 6. Secrets

- environment variables or secret manager for secrets.
- `.env` excluded from Git.
- `.env.example` may document variable names only, with fake values.
- secret exposure triggers immediate rotation/revocation and incident note.

## 7. Web security baseline

Do not disable framework protections for convenience:
- CSRF.
- secure session/cookie settings appropriate to deployment.
- host/origin configuration.
- output escaping.
- authentication/authorization middleware.

Mutations use POST/appropriate unsafe methods and server-side checks.

## 8. Files and evidence

Future uploaded files require:
- explicit ownership.
- access control.
- content/type/size validation.
- storage abstraction.
- retention policy.
- no public object URL by default for sensitive evidence.

## 9. Data minimization

Store only data required for the product purpose.

Do not collect sensitive personal fields merely because future analytics might use them.

## 10. Backups and recovery

Before production:
- documented database backup schedule.
- restore test.
- file/evidence backup strategy.
- point-in-time/recovery goals appropriate to deployment.
- no destructive migration without verified recovery path.

## 11. Production gate

No production use with official records before:
- Amendment/Addendum exists.
- security settings reviewed.
- data classification/retention is agreed.
- backup and restore are tested.
- human acceptance passes.
- deployment environment is documented.
