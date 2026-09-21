# Human Acceptance Protocol

- Status: **Required before closing a usable slice**

## Entry gate

Human Acceptance starts only after:
- all planned machine increments for the slice are PASS.
- no blocking automated failures.
- no unresolved critical permission/invariant defects.
- app setup/run instructions work.
- demo/test data path is available.
- end-to-end browser workflow is complete.

## Review dimensions

Human acceptance is intentionally broader than automated testing.

### Visual
Evaluate:
- comfort.
- balance.
- hierarchy.
- typography.
- colors.
- density.
- consistency.
- RTL quality.

### Practical workflow
Evaluate:
- can the user understand what to do next?
- is useful freedom preserved?
- are unnecessary steps imposed?
- do pages expose expected actions?
- are dead ends present?
- is terminology natural to real work?

### Domain fit
Evaluate:
- does the workflow match actual inspection practice?
- does the application force a false hierarchy?
- does it preserve professional independence?
- does it support individual work correctly?

### Information quality
Evaluate:
- overview usefulness.
- drill-down clarity.
- source/provenance visibility.
- status clarity.
- meaningful totals/detail.

### Devices
At minimum:
- desktop.
- mobile portrait.
- mobile landscape where the workflow materially uses it.

## Finding classification

Each human finding is classified as one of:

- BUG — implemented behavior contradicts accepted requirement.
- DOMAIN GAP — accepted model is insufficient/wrong.
- PERMISSION/SECURITY — authority/integrity issue.
- UX WORKFLOW — function exists but flow is unclear/inefficient.
- VISUAL — appearance/spacing/hierarchy.
- TERMINOLOGY — wording does not match domain language.
- ENHANCEMENT — optional improvement outside current acceptance.

## Correction rule

Findings do not get patched casually during review.

For each relevant finding:
1. classify.
2. decide whether domain/design decision is required.
3. create bounded correction increment.
4. implement.
5. automated verification.
6. review.
7. human re-test when relevant.

## Acceptance decision

Possible outcomes:
- PASS — slice accepted.
- CONDITIONAL PASS — only explicitly documented non-blocking items remain.
- HOLD — correction required.
- STOP — domain redesign required.

## Evidence

Record:
- date.
- version/commit tested.
- device/browser.
- test account/profile.
- findings.
- resolution status.
- final decision.
