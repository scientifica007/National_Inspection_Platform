from __future__ import annotations

import uuid

import pytest
from django.core.exceptions import ValidationError
from django.db.models import ProtectedError
from django.utils import timezone

from identity.permissions import Capability, PermissionDeniedError
from identity.services import grant_capability
from identity.tests.factories import make_account
from institutions.models import Institution
from institutions.services import (
    InstitutionLifecycleError,
    InstitutionPermissionDenied,
    InstitutionRetentionError,
    archive_local_institution,
    create_local_institution,
    delete_local_institution,
    update_local_institution,
)

pytestmark = pytest.mark.django_db


def test_institution_uses_uuid_primary_key(institution_owner):
    institution = create_local_institution(actor=institution_owner, name="مؤسسة تدريبية")

    assert isinstance(institution.pk, uuid.UUID)


def test_default_lifecycle_owner_creator_and_timestamps(institution_owner):
    institution = create_local_institution(actor=institution_owner, name="مركز اختبار")

    assert institution.lifecycle == Institution.Lifecycle.LOCAL_ACTIVE
    assert institution.archived_at is None
    assert institution.created_by_person == institution_owner.person
    assert institution.local_owner_person == institution_owner.person
    assert institution.created_at is not None
    assert institution.updated_at is not None


def test_model_rejects_archive_timestamp_on_active_institution(institution_owner):
    institution = Institution(
        name="مؤسسة غير متسقة",
        created_by_person=institution_owner.person,
        local_owner_person=institution_owner.person,
        archived_at="2026-09-22T00:00:00Z",
    )

    with pytest.raises(ValidationError):
        institution.full_clean()


def test_model_rejects_blank_name_after_trimming(institution_owner):
    institution = Institution(
        name="   ",
        created_by_person=institution_owner.person,
        local_owner_person=institution_owner.person,
    )

    with pytest.raises(ValidationError):
        institution.full_clean()


def test_archive_sets_lifecycle_and_timestamp(institution_owner):
    institution = create_local_institution(actor=institution_owner, name="مؤسسة للأرشفة")

    archived = archive_local_institution(actor=institution_owner, institution=institution)

    assert archived.lifecycle == Institution.Lifecycle.ARCHIVED
    assert archived.archived_at is not None


def test_archived_institution_cannot_be_edited(institution_owner):
    institution = create_local_institution(actor=institution_owner, name="اسم أول")
    archive_local_institution(actor=institution_owner, institution=institution)

    with pytest.raises(InstitutionLifecycleError):
        update_local_institution(
            actor=institution_owner,
            institution=institution,
            name="اسم جديد",
        )


def test_repeated_archive_transition_is_rejected(institution_owner):
    institution = create_local_institution(actor=institution_owner, name="أرشفة مكررة")
    archive_local_institution(actor=institution_owner, institution=institution)

    with pytest.raises(InstitutionLifecycleError):
        archive_local_institution(actor=institution_owner, institution=institution)


def test_archived_institution_cannot_be_hard_deleted(institution_owner):
    institution = create_local_institution(actor=institution_owner, name="حذف مؤرشف")
    archive_local_institution(actor=institution_owner, institution=institution)

    with pytest.raises(InstitutionLifecycleError):
        delete_local_institution(actor=institution_owner, institution=institution)


def test_no_unarchive_service_or_route_exists():
    from django.urls import get_resolver

    import institutions.services as services

    assert not hasattr(services, "unarchive_local_institution")
    route_names = {name for name in get_resolver().reverse_dict if isinstance(name, str)}
    assert not any("unarchive" in name or "restore" in name for name in route_names)


def test_create_requires_institution_create_capability(db):
    account = make_account(
        username="institution-no-create",
        display_name="بلا صلاحية إنشاء مؤسسة",
    )

    with pytest.raises(PermissionDeniedError):
        create_local_institution(actor=account, name="مؤسسة مرفوضة")


def test_create_uses_stored_actor_person_not_caller_supplied_person(
    institution_owner, other_inspector
):
    institution_owner.person = other_inspector.person

    institution = create_local_institution(actor=institution_owner, name="هوية محفوظة")

    assert institution.created_by_person_id != other_inspector.person_id
    assert institution.local_owner_person_id != other_inspector.person_id
    institution_owner.refresh_from_db()
    assert institution.created_by_person_id == institution_owner.person_id
    assert institution.local_owner_person_id == institution_owner.person_id


def test_fabricated_unsaved_actor_cannot_create(institution_owner):
    fabricated = type(institution_owner)(
        pk=institution_owner.pk,
        username="fabricated-institution-owner",
        person=institution_owner.person,
    )

    with pytest.raises(PermissionDeniedError):
        create_local_institution(actor=fabricated, name="مؤسسة مزيفة")


def test_owner_can_update_active_institution(institution_owner):
    institution = create_local_institution(actor=institution_owner, name="قديم")

    update_local_institution(actor=institution_owner, institution=institution, name="جديد")

    institution.refresh_from_db()
    assert institution.name == "جديد"


def test_other_inspector_cannot_update_owner_institution(institution_owner, other_inspector):
    institution = create_local_institution(actor=institution_owner, name="مؤسسة المالك")

    with pytest.raises(InstitutionPermissionDenied):
        update_local_institution(actor=other_inspector, institution=institution, name="تعديل مرفوض")


def test_platform_admin_status_alone_cannot_update_owner_institution(
    institution_owner, platform_admin
):
    institution = create_local_institution(actor=institution_owner, name="مؤسسة مهنية")

    with pytest.raises(InstitutionPermissionDenied):
        update_local_institution(actor=platform_admin, institution=institution, name="تعديل إداري")


def test_owner_without_create_capability_cannot_update_or_delete(grant_issuer):
    account = make_account(
        username="institution-read-only-owner",
        display_name="مالك قراءة فقط",
    )
    grant_capability(
        actor=grant_issuer,
        account=account,
        capability_code=Capability.INSTITUTION_CREATE_LOCAL,
    )
    institution = create_local_institution(actor=account, name="مؤسسة قبل سحب الصلاحية")
    for grant in account.capability_grants.all():
        grant.revoked_at = timezone.now()
        grant.save(update_fields=["revoked_at"])

    with pytest.raises(InstitutionPermissionDenied):
        update_local_institution(actor=account, institution=institution, name="مرفوض")
    with pytest.raises(InstitutionPermissionDenied):
        delete_local_institution(actor=account, institution=institution)


def test_authorized_unrefenced_hard_delete_succeeds(institution_owner):
    institution = create_local_institution(actor=institution_owner, name="قابلة للحذف")
    institution_id = institution.pk

    delete_local_institution(actor=institution_owner, institution=institution)

    assert not Institution.objects.filter(pk=institution_id).exists()


def test_protected_delete_maps_to_retention_error(monkeypatch, institution_owner):
    institution = create_local_institution(actor=institution_owner, name="مرتبطة تاريخيًا")

    def raise_protected_error(*args, **kwargs):
        raise ProtectedError("protected", protected_objects=[])

    monkeypatch.setattr(institution, "delete", raise_protected_error)

    with pytest.raises(InstitutionRetentionError):
        delete_local_institution(actor=institution_owner, institution=institution)
    assert Institution.objects.filter(pk=institution.pk).exists()


def test_no_hard_coded_institution_data_after_migrations():
    assert Institution.objects.count() == 0
