"""Read/query operations for the identity module.

Selectors never mutate state (docs/ENGINEERING_CONVENTIONS.md).
"""

from __future__ import annotations

from django.db.models import QuerySet

from .models import Account, CapabilityGrant


def accounts_visible_to(account: Account) -> QuerySet[Account]:
    """Accounts an acting Account may list.

    Administrative authority yields the whole account list; every other
    Account sees only itself. Visibility never implies the right to author or
    to act as another Person.
    """
    queryset = Account.objects.select_related("person").order_by("username")
    if account.is_platform_admin:
        return queryset
    return queryset.filter(pk=account.pk)


def grants_for(account: Account) -> QuerySet[CapabilityGrant]:
    """Grants belonging to an Account, newest first."""
    return account.capability_grants.select_related("account", "granted_by_account")
