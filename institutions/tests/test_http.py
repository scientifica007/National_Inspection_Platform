from __future__ import annotations

import pytest
from django.test import Client
from django.urls import reverse

from institutions.forms import InstitutionForm
from institutions.models import Institution
from institutions.services import archive_local_institution, create_local_institution

pytestmark = pytest.mark.django_db


def test_list_redirects_anonymous_user(client):
    response = client.get(reverse("institutions:list"))

    assert response.status_code == 302
    assert reverse("identity:login") in response.url


def test_nav_contains_my_institutions_link(client, institution_owner):
    client.force_login(institution_owner)

    response = client.get(reverse("identity:dashboard"))

    assert "مؤسساتي" in response.content.decode()


def test_owner_list_shows_own_institution_not_other(client, institution_owner, other_inspector):
    own = create_local_institution(actor=institution_owner, name="ظاهرة للمالك")
    other = create_local_institution(actor=other_inspector, name="مخفية عن المالك")
    client.force_login(institution_owner)

    response = client.get(reverse("institutions:list"))

    content = response.content.decode()
    assert response.status_code == 200
    assert own.name in content
    assert other.name not in content


def test_other_inspector_gets_not_found_for_detail(client, institution_owner, other_inspector):
    institution = create_local_institution(actor=institution_owner, name="تفصيل مخفي")
    client.force_login(other_inspector)

    response = client.get(reverse("institutions:detail", args=[institution.pk]))

    assert response.status_code == 404


def test_platform_admin_can_read_detail(client, institution_owner, platform_admin):
    institution = create_local_institution(actor=institution_owner, name="تفصيل إداري")
    client.force_login(platform_admin)

    response = client.get(reverse("institutions:detail", args=[institution.pk]))

    assert response.status_code == 200
    assert institution.name in response.content.decode()


def test_platform_admin_status_alone_cannot_post_edit(client, institution_owner, platform_admin):
    institution = create_local_institution(actor=institution_owner, name="قبل محاولة الإدارة")
    client.force_login(platform_admin)

    response = client.post(
        reverse("institutions:edit", args=[institution.pk]),
        {"name": "تعديل غير مسموح"},
    )

    assert response.status_code == 403
    institution.refresh_from_db()
    assert institution.name == "قبل محاولة الإدارة"


def test_owner_can_create_from_form(client, institution_owner):
    client.force_login(institution_owner)

    response = client.post(reverse("institutions:create"), {"name": "من الواجهة"})

    assert response.status_code == 302
    institution = Institution.objects.get(name="من الواجهة")
    assert institution.local_owner_person == institution_owner.person
    assert institution.created_by_person == institution_owner.person


def test_create_post_without_csrf_is_rejected(institution_owner):
    csrf_client = Client(enforce_csrf_checks=True)
    csrf_client.force_login(institution_owner)

    response = csrf_client.post(reverse("institutions:create"), {"name": "محاولة CSRF"})

    assert response.status_code == 403


def test_institution_form_exposes_only_name():
    assert list(InstitutionForm().fields) == ["name"]


def test_archive_requires_post(client, institution_owner):
    institution = create_local_institution(actor=institution_owner, name="أرشفة HTTP")
    client.force_login(institution_owner)

    response = client.get(reverse("institutions:archive", args=[institution.pk]))

    assert response.status_code == 405


def test_owner_can_archive_via_post(client, institution_owner):
    institution = create_local_institution(actor=institution_owner, name="أرشفة من الواجهة")
    client.force_login(institution_owner)

    response = client.post(reverse("institutions:archive", args=[institution.pk]))

    assert response.status_code == 302
    institution.refresh_from_db()
    assert institution.lifecycle == Institution.Lifecycle.ARCHIVED


def test_archived_edit_is_rejected_in_form_flow(client, institution_owner):
    institution = create_local_institution(actor=institution_owner, name="مؤسسة مؤرشفة")
    archive_local_institution(actor=institution_owner, institution=institution)
    client.force_login(institution_owner)

    response = client.post(
        reverse("institutions:edit", args=[institution.pk]),
        {"name": "غير مقبول"},
    )

    assert response.status_code == 200
    assert "مؤرشفة" in response.content.decode()
    institution.refresh_from_db()
    assert institution.name == "مؤسسة مؤرشفة"


def test_delete_confirmation_and_post_delete(client, institution_owner):
    institution = create_local_institution(actor=institution_owner, name="حذف من الواجهة")
    client.force_login(institution_owner)

    get_response = client.get(reverse("institutions:delete", args=[institution.pk]))
    post_response = client.post(reverse("institutions:delete", args=[institution.pk]))

    assert get_response.status_code == 200
    assert post_response.status_code == 302
    assert not Institution.objects.filter(pk=institution.pk).exists()


def test_other_inspector_delete_is_not_found(client, institution_owner, other_inspector):
    institution = create_local_institution(actor=institution_owner, name="حذف مخفي")
    client.force_login(other_inspector)

    response = client.post(reverse("institutions:delete", args=[institution.pk]))

    assert response.status_code == 404
    assert Institution.objects.filter(pk=institution.pk).exists()
