from __future__ import annotations

from django.http import Http404

from identity.models import Account
from identity.permissions import (
    Capability,
    has_capability,
    is_platform_admin,
    resolve_persisted_account,
)

from .models import Institution


def institutions_visible_to(actor: Account):
    queryset = Institution.objects.select_related(
        "created_by_person", "local_owner_person"
    ).order_by("name")

    stored, denial = resolve_persisted_account(actor)
    if denial is not None or stored is None or not stored.is_active:
        return queryset.none()
    if is_platform_admin(stored):
        return queryset
    if has_capability(
        stored,
        Capability.INSTITUTION_READ_OWN,
        subject_person=stored.person,
    ):
        return queryset.filter(local_owner_person=stored.person)
    return queryset.none()


def get_visible_institution_or_404(*, actor: Account, institution_id) -> Institution:
    try:
        return institutions_visible_to(actor).get(pk=institution_id)
    except Institution.DoesNotExist as exc:
        raise Http404("المؤسسة غير موجودة.") from exc
