"""Technical bootstrap entry point for the very first Platform Admin.

The application service ``identity.services.create_account`` requires an
existing Platform Admin actor, which is correct for the product but leaves one
chicken-and-egg problem: the first administrative account cannot be created
through it. This module is that separate entry point.

It is deliberately **not** imported by the application service, so the service's
authorization can never be weakened by it. It represents the System Operator /
deployment boundary (`docs/AUTHORITY_MODEL.md`), not a product feature: it is
the single place where an Account is created without an acting admin, and it
should be reachable only from an operator-controlled context (deployment
runbook, CI seeding, tests) — never from an HTTP request or template.
"""

from __future__ import annotations

from .models import Account, Person

__all__ = ["bootstrap_platform_admin"]


def bootstrap_platform_admin(
    *,
    username: str,
    password: str,
    display_name: str | None = None,
    email: str = "",
) -> Account:
    """Create the seed Platform Admin Account and its Person.

    Administrative authority is all this grants. It creates no professional
    capability, so the bootstrapped Account is not an author of anything
    (ADR-0003). Professional authority must later be granted explicitly through
    ``identity.services.grant_capability``.
    """
    person = Person(display_name=display_name or username)
    person.full_clean()
    person.save()
    return Account.objects.create_user(
        username=username,
        email=email,
        password=password,
        person=person,
        is_platform_admin=True,
    )
