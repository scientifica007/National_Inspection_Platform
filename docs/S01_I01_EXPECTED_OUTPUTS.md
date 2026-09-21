# S01-I01 Expected Outputs

- Increment: **S01-I01 — Project Skeleton + Identity/Authority Foundation**
- Purpose: precise reviewer expectations; not a mandate to overbuild.

## Expected repository-level outputs

Likely new implementation files include equivalents of:

```text
manage.py
config/
identity/
templates/
static/
pyproject.toml and/or requirements files
pytest configuration
.env.example
.gitignore
.github/workflows/...
```

Exact file names may vary when justified.

## Expected Django outputs

### config
- settings suitable for environment-driven PostgreSQL.
- root URL configuration.
- WSGI/ASGI entry points.
- custom user model configured before first project migration.

### identity
Expected concepts:
- Person.
- Account/User.
- CapabilityGrant.
- minimal OWN/ALL authority evaluation.
- authentication views/forms or framework-supported equivalents.
- reusable permission/application logic.
- migrations.
- tests.

No institution/visit/mission models should exist yet.

## Expected UI

At this increment only:
- Arabic RTL base layout.
- login screen.
- authenticated landing/dashboard shell.
- logout path.
- minimum role/account context display where useful.
- design token stylesheet.
- basic responsive behavior.

No full product dashboard is expected.

## Expected tests/evidence

At minimum evidence should cover:
- custom user configured.
- Person/Account relation.
- authentication.
- unauthenticated denial.
- OWN/ALL capability evaluation.
- revoked/expired grant semantics if included in model.
- Admin != professional author.
- no impersonation behavior.
- system check.
- migration check.
- lint.
- PostgreSQL path or explicit environment limitation.

## Expected non-outputs

The following appearing in S01-I01 is a review warning unless clearly required:

- Institution model.
- Checklist model.
- Visit model.
- Finding/Recommendation.
- Mission/Assignment/Team.
- national dashboards.
- REST API.
- generic event bus.
- generic workflow engine.
- generic repository abstraction layer.
- microservice setup.
- large JavaScript frontend framework.

## Gate result

Completion by the executor is not PASS by itself.

After executor delivery the project enters:
**Independent Review**

Possible gate outcomes:
- `PASS — NEXT INCREMENT ALLOWED`
- `HOLD — CORRECTION REQUIRED`
- `STOP — DOMAIN DECISION REQUIRED`

S01-I02 is forbidden until the first outcome is explicitly recorded.
