"""Read/query operations for the identity module.

Selectors never mutate state (docs/ENGINEERING_CONVENTIONS.md).

Every selector resolves the persisted Account first (R5-B01). "What may this
actor see?" is an authority question, so the answer rests on the stored row, not
on the instance a caller passes in. A fabricated, unsaved, borrowed-``pk`` or
stale actor gets nothing: returning an own-scoped result would still leak
whatever row its borrowed primary key names.
"""

from __future__ import annotations

from django.db.models import QuerySet

from .models import Account, CapabilityGrant
from .permissions import resolve_persisted_account


def accounts_visible_to(account: Account) -> QuerySet[Account]:
    """Accounts an acting Account may list.

    Administrative authority yields the whole account list; every other Account
    sees only itself. Visibility never implies the right to author or to act as
    another Person.

    An actor that is not a genuine persisted Account — or whose stored row is
    inactive — sees nothing at all.
    """
    queryset = Account.objects.select_related("person").order_by("username")

    stored, denial = resolve_persisted_account(account)
    if denial is not None or not stored.is_active:
        return queryset.none()
    if stored.is_platform_admin:
        return queryset
    return queryset.filter(pk=stored.pk)


def grants_for(account: Account) -> QuerySet[CapabilityGrant]:
    """Grants belonging to an Account, newest first.

    The grants returned are the stored row's, so a fabricated actor borrowing a
    real Account's primary key cannot enumerate that Account's authorisations.
    """
    queryset = CapabilityGrant.objects.select_related("account", "granted_by_account")

    stored, denial = resolve_persisted_account(account)
    if denial is not None:
        return queryset.none()
    return queryset.filter(account=stored)
