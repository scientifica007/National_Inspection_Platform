# Risk Register

- Status: **Active**
- Updated: 2026-09-21

| ID | Risk | Impact | Current control | State |
|---|---|---|---|---|
| R-001 | Over-abstraction creates a generic framework instead of a useful inspection product | High | Minimal Stable Core; explicit models; no EAV/workflow engine | Controlled |
| R-002 | Modular Monolith degrades into tightly coupled monolith | High | dependency map; service boundaries; architecture review | Active |
| R-003 | Admin becomes impersonation/superuser shortcut for professional records | Critical | ADR-0003; server-side authority rules; permission matrix | Controlled |
| R-004 | UI permissions hide buttons but backend still permits forbidden actions | Critical | server-side enforcement; permission tests | Controlled |
| R-005 | Finalized history can be rewritten/deleted | Critical | immutability invariant; finalize transaction; regression tests | Controlled |
| R-006 | Source checklist/institution changes rewrite historical meaning | High | snapshots/versioning; retention rules | Controlled |
| R-007 | Frontend becomes coupled to business logic, blocking redesign | High | presentation separation; services/selectors; Design Tokens | Controlled |
| R-008 | Future features are pre-built speculatively and increase maintenance cost | High | bounded increments; explicit Deferred scope | Controlled |
| R-009 | AI executor silently invents domain policy | High | executor source precedence; STOP on contradiction | Controlled |
| R-010 | Same AI trusts its own implementation and misses defects | High | separate review pass; gate evidence; independent audit mindset | Active |
| R-011 | Real personal/official data enters public GitHub repository | Critical | no-real-data rule; security/data governance | Active |
| R-012 | SQLite-only success hides PostgreSQL behavior defects | Medium/High | PostgreSQL canonical tests | Controlled |
| R-013 | Migrations damage data/history | Critical | small reviewed migrations; backups/rollback reasoning before destructive change | Future control |
| R-014 | Human workflow is technically correct but practically rigid | High | human acceptance; freedom-by-default principle | Active |
| R-015 | Visual polishing consumes effort before workflow is coherent | Medium | visual refinement after functional increments; replaceable UI | Controlled |
| R-016 | Dashboard aggregates become detached from source facts | High | provenance invariant; drill-down requirement | Future control |
| R-017 | Geographic/organizational hard-coding becomes obsolete | High | versioned Data/Configuration design | Controlled conceptually |
| R-018 | Team hierarchy is encoded as legal permanent tree | High | contextual temporal membership/leadership model | Controlled conceptually |
| R-019 | Amendment is deferred too long and real records are used anyway | Critical | explicit production prohibition before Amendment | Active |
| R-020 | Documentation diverges from code | High | checkpoint docs; traceability; review requires documentation update | Active |

## Review rule

At every increment checkpoint:
- identify new risks.
- update changed risk state/control.
- do not mark a risk "closed" merely because implementation exists; evidence is required.
