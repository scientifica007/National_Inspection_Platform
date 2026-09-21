"""Application services for the identity module.

These are command/use-case functions owning transaction boundaries
(docs/ENGINEERING_CONVENTIONS.md). They contain no HTTP or template logic.

Authorization for administrative commands is evaluated through
``identity.permissions`` so the rule stays server-side and reusable.
"""

from __future__ import annotations

from django.db import transaction
from django.utils import timezone

from .models import Account, CapabilityGrant, Person
from .permissions import (
    ADMINISTRATIVE_CAPABILITIES,
    ALL_CAPABILITIES,
    PermissionDeniedError,
    require_administrative_authority,
)


def create_person(*, display_name: str) -> Person:
    """Create a Person (the human being), independent of any Account."""
    person = Person(display_name=display_name)
    person.full_clean()
    person.save()
    return person


def create_account(
    *,
    username: str,
    password: str,
    display_name: str | None = None,
    person: Person | None = None,
    email: str = "",
    is_platform_admin: bool = False,
) -> Account:
    """Create an Account for a Person.

    ``is_platform_admin`` grants administrative authority only. It never
    creates a professional capability and never reuses another Person's
    identity.
    """
    return Account.objects.create_user(
        username=username,
        email=email,
        password=password,
        display_name=display_name,
        person=person,
        is_platform_admin=is_platform_admin,
    )


def grant_capability(
    *,
    actor: Account,
    account: Account,
    capability_code: str,
    scope_kind: str = CapabilityGrant.ScopeKind.OWN,
    valid_from=None,
    valid_until=None,
    delegable: bool = False,
) -> CapabilityGrant:
    """Grant a Capability to an Account.

    Only a real Platform Admin may grant capabilities. An ``account.manage``
    grant does not satisfy this check, so a non-admin cannot escalate by
    obtaining or issuing administrative capabilities. The issuing Account is
    recorded on the grant and preserved for the grant's lifetime.
    """
    require_administrative_authority(actor, action="grant_capability")

    if capability_code not in ALL_CAPABILITIES:
        raise ValueError(f"Unknown capability code: {capability_code!r}")
    if scope_kind not in CapabilityGrant.ScopeKind.values:
        raise ValueError(f"Unknown scope kind: {scope_kind!r}")

    grant = CapabilityGrant(
        account=account,
        capability_code=capability_code,
        scope_kind=scope_kind,
        valid_from=valid_from,
        valid_until=valid_until,
        delegable=delegable,
        granted_by_account=actor,
    )
    grant.full_clean()
    grant.save()
    return grant


@transaction.atomic
def revoke_capability(*, actor: Account, grant: CapabilityGrant) -> CapabilityGrant:
    """Revoke a grant without deleting history."""
    require_administrative_authority(actor, action="revoke_capability")
    if grant.revoked_at is None:
        grant.revoked_at = timezone.now()
        grant.save(update_fields=["revoked_at"])
    return grant


@transaction.atomic
def deactivate_account(*, actor: Account, account: Account) -> Account:
    """Disable an Account without deleting the Person or their history."""
    require_administrative_authority(actor, action="deactivate_account")
    if account.pk == actor.pk:
        raise PermissionDeniedError("لا يمكن لمدير المنصة تعطيل حسابه الخاص.")
    account.is_active = False
    account.save(update_fields=["is_active"])
    return account


def is_administrative_capability(capability_code: str) -> bool:
    """Whether a capability belongs to the administrative dimension."""
    return capability_code in ADMINISTRATIVE_CAPABILITIES
