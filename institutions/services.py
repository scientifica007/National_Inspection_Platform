from __future__ import annotations

from django.db import transaction
from django.db.models import ProtectedError
from django.utils import timezone

from identity.models import Account
from identity.permissions import Capability, PermissionDeniedError, require_capability

from .models import Institution
from .permissions import can_mutate_institution, persisted_active_actor


class InstitutionError(Exception):
    """Base class for institution application/domain errors."""


class InstitutionPermissionDenied(PermissionDeniedError):
    """Raised when an actor is not allowed to perform an institution action."""


class InstitutionLifecycleError(InstitutionError):
    """Raised for invalid lifecycle transitions."""


class InstitutionRetentionError(InstitutionError):
    """Raised when hard delete is blocked by retained historical dependencies."""


def _require_mutation_authority(actor: Account, institution: Institution) -> None:
    if not can_mutate_institution(actor, institution):
        raise InstitutionPermissionDenied("لا تملك صلاحية تعديل هذه المؤسسة المحلية.")


def _require_active_lifecycle(institution: Institution, *, action: str) -> None:
    if institution.lifecycle != Institution.Lifecycle.LOCAL_ACTIVE:
        raise InstitutionLifecycleError(f"لا يمكن تنفيذ {action} على مؤسسة مؤرشفة.")


@transaction.atomic
def create_local_institution(*, actor: Account, name: str) -> Institution:
    stored_actor = persisted_active_actor(actor)
    require_capability(
        stored_actor,
        Capability.INSTITUTION_CREATE_LOCAL,
        subject_person=stored_actor.person,
    )
    institution = Institution(
        name=name,
        created_by_person=stored_actor.person,
        local_owner_person=stored_actor.person,
    )
    institution.full_clean()
    institution.save()
    return institution


@transaction.atomic
def update_local_institution(*, actor: Account, institution: Institution, name: str) -> Institution:
    _require_mutation_authority(actor, institution)
    _require_active_lifecycle(institution, action="التعديل")
    institution.name = name
    institution.full_clean()
    institution.save(update_fields=["name", "updated_at"])
    return institution


@transaction.atomic
def archive_local_institution(*, actor: Account, institution: Institution) -> Institution:
    _require_mutation_authority(actor, institution)
    _require_active_lifecycle(institution, action="الأرشفة")
    institution.lifecycle = Institution.Lifecycle.ARCHIVED
    institution.archived_at = timezone.now()
    institution.full_clean()
    institution.save(update_fields=["lifecycle", "archived_at", "updated_at"])
    return institution


@transaction.atomic
def delete_local_institution(*, actor: Account, institution: Institution) -> None:
    _require_mutation_authority(actor, institution)
    _require_active_lifecycle(institution, action="الحذف")
    try:
        institution.delete()
    except ProtectedError as exc:
        raise InstitutionRetentionError(
            "لا يمكن حذف المؤسسة لأن سجلًا تاريخيًا محفوظًا يعتمد عليها."
        ) from exc
