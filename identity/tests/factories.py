"""Synthetic test data builders.

All data produced here is synthetic (docs/SECURITY_AND_DATA_GOVERNANCE.md).
No real person, inspection record or credential is represented.

``make_account`` writes an Account directly through the ORM. That is a
deliberate test-only bypass: the production paths are
``identity.services.create_account`` (which requires an acting Platform Admin,
R2-B01) and ``identity.bootstrap.bootstrap_platform_admin`` (the seed admin).
Most tests need a plain Account to observe behaviour rather than to exercise an
authorized mutation, so bypassing the service keeps each test focused. Tests
that *do* exercise the authorization go through the service explicitly.
"""

from __future__ import annotations

from identity.models import Account, Person

__all__ = ["make_account", "make_person"]


def make_account(
    *,
    username: str,
    password: str = "synthetic-test-pass-01",
    display_name: str | None = None,
    is_platform_admin: bool = False,
) -> Account:
    """Create a synthetic Account directly via the ORM (test setup only)."""
    return Account.objects.create_user(
        username=username,
        password=password,
        display_name=display_name,
        is_platform_admin=is_platform_admin,
    )


def make_person(*, display_name: str) -> Person:
    """Create a synthetic Person directly via the ORM (test setup only).

    The application path ``identity.services.create_person`` is an authorized
    mutation since R3-B02; tests that need a Person merely as data use this
    instead of pretending to be an admin.
    """
    person = Person(display_name=display_name)
    person.full_clean()
    person.save()
    return person
