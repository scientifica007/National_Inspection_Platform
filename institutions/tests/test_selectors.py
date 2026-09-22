from __future__ import annotations

import pytest

from identity.permissions import Capability
from identity.services import grant_capability
from identity.tests.factories import make_account
from institutions.selectors import institutions_visible_to
from institutions.services import create_local_institution

pytestmark = pytest.mark.django_db


def test_owner_with_read_own_sees_own_institution_only(institution_owner, other_inspector):
    own = create_local_institution(actor=institution_owner, name="مؤسسة المالك")
    other = create_local_institution(actor=other_inspector, name="مؤسسة أخرى")

    visible_ids = {institution.pk for institution in institutions_visible_to(institution_owner)}

    assert own.pk in visible_ids
    assert other.pk not in visible_ids


def test_owner_without_read_own_does_not_see_own_institution(grant_issuer):
    account = make_account(
        username="create-without-read",
        display_name="إنشاء دون قراءة",
    )
    grant_capability(
        actor=grant_issuer,
        account=account,
        capability_code=Capability.INSTITUTION_CREATE_LOCAL,
    )
    institution = create_local_institution(actor=account, name="مخفية بلا قراءة")

    assert institution not in list(institutions_visible_to(account))


def test_other_inspector_cannot_discover_institution(institution_owner, other_inspector):
    create_local_institution(actor=institution_owner, name="مؤسسة مخفية")

    assert list(institutions_visible_to(other_inspector)) == []


def test_active_platform_admin_can_see_all_institutions(
    institution_owner, other_inspector, platform_admin
):
    first = create_local_institution(actor=institution_owner, name="الأولى")
    second = create_local_institution(actor=other_inspector, name="الثانية")

    visible_ids = {institution.pk for institution in institutions_visible_to(platform_admin)}

    assert visible_ids == {first.pk, second.pk}


def test_inactive_platform_admin_sees_nothing(institution_owner, platform_admin):
    create_local_institution(actor=institution_owner, name="لا تظهر للمعطل")
    platform_admin.is_active = False
    platform_admin.save(update_fields=["is_active"])

    assert list(institutions_visible_to(platform_admin)) == []


def test_borrowed_unsaved_actor_does_not_gain_visibility(institution_owner):
    create_local_institution(actor=institution_owner, name="لا تُستعار")
    borrowed = type(institution_owner)(
        pk=institution_owner.pk,
        username="borrowed-visibility",
        person=institution_owner.person,
    )

    assert list(institutions_visible_to(borrowed)) == []


def test_stale_admin_object_does_not_gain_visibility_after_demotion(
    institution_owner, platform_admin
):
    create_local_institution(actor=institution_owner, name="بعد العزل")
    stale_admin = platform_admin
    type(platform_admin).objects.filter(pk=platform_admin.pk).update(is_platform_admin=False)

    assert list(institutions_visible_to(stale_admin)) == []
