from __future__ import annotations

from identity.models import Account
from identity.permissions import (
    Capability,
    PermissionDeniedError,
    has_capability,
    is_platform_admin,
    resolve_persisted_account,
)

from .models import Institution


def persisted_active_actor(actor: Account) -> Account:
    stored, denial = resolve_persisted_account(actor)
    if denial is not None or stored is None:
        raise PermissionDeniedError("يتطلب هذا الإجراء حسابًا حقيقيًا محفوظًا.")
    if not stored.is_active:
        raise PermissionDeniedError("الحساب المعطّل لا يمكنه تنفيذ هذا الإجراء.")
    return stored


def can_create_local_institution(actor: Account) -> bool:
    stored, denial = resolve_persisted_account(actor)
    if denial is not None or stored is None or not stored.is_active:
        return False
    return has_capability(
        stored,
        Capability.INSTITUTION_CREATE_LOCAL,
        subject_person=stored.person,
    )


def can_read_institution(actor: Account, institution: Institution) -> bool:
    stored, denial = resolve_persisted_account(actor)
    if denial is not None or stored is None or not stored.is_active:
        return False
    if is_platform_admin(stored):
        return True
    return has_capability(
        stored,
        Capability.INSTITUTION_READ_OWN,
        subject_person=institution.local_owner_person,
    )


def can_mutate_institution(actor: Account, institution: Institution) -> bool:
    stored, denial = resolve_persisted_account(actor)
    if denial is not None or stored is None or not stored.is_active:
        return False
    if institution.local_owner_person_id != stored.person_id:
        return False
    return has_capability(
        stored,
        Capability.INSTITUTION_CREATE_LOCAL,
        subject_person=stored.person,
    )
