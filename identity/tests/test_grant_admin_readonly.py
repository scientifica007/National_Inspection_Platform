"""R2-B03 regression: CapabilityGrant is read-only in the technical admin.

The admin previously exposed an add/change/delete surface. Adding a grant there
could not satisfy the required issuer, and change/delete would bypass the
service semantics (real acting admin, revocation preserves history). For
S01-I01 the admin is inspection-only.
"""

from __future__ import annotations

import pytest
from django.contrib.admin.sites import site
from django.contrib.auth.models import Permission
from django.test import RequestFactory

from identity.admin import CapabilityGrantAdmin
from identity.models import CapabilityGrant
from identity.services import grant_capability

pytestmark = pytest.mark.django_db


@pytest.fixture
def superuser_request(grant_issuer):
    """A request from a Django superuser — the strongest technical actor.

    Even this actor must not mutate grants through the admin, so the refusals
    are not merely "a weaker user cannot".
    """
    grant_issuer.is_staff = True
    grant_issuer.is_superuser = True
    grant_issuer.save(update_fields=["is_staff", "is_superuser"])
    request = RequestFactory().get("/admin/identity/capabilitygrant/")
    request.user = grant_issuer
    return request


class TestAdminIsRegisteredReadOnly:
    def test_admin_class_is_registered(self):
        assert isinstance(site._registry[CapabilityGrant], CapabilityGrantAdmin)

    def test_add_is_disabled(self, superuser_request):
        assert site._registry[CapabilityGrant].has_add_permission(superuser_request) is False

    def test_change_is_disabled(self, superuser_request):
        assert site._registry[CapabilityGrant].has_change_permission(superuser_request) is False

    def test_delete_is_disabled(self, superuser_request):
        assert site._registry[CapabilityGrant].has_delete_permission(superuser_request) is False

    def test_readonly_refusals_hold_even_for_a_user_with_all_permissions(
        self, superuser_request, grant_issuer
    ):
        grant_issuer.user_permissions.set(Permission.objects.all())
        admin = site._registry[CapabilityGrant]
        assert admin.has_add_permission(superuser_request) is False
        assert admin.has_change_permission(superuser_request) is False
        assert admin.has_delete_permission(superuser_request) is False


class TestAdminFieldsAreInspectionOnly:
    def test_every_grant_field_is_readonly(self):
        admin = site._registry[CapabilityGrant]
        model_fields = {field.name for field in CapabilityGrant._meta.get_fields()}
        expected = {
            "id",
            "account",
            "capability_code",
            "scope_kind",
            "valid_from",
            "valid_until",
            "delegable",
            "granted_by_account",
            "revoked_at",
            "created_at",
        }
        assert expected <= set(admin.readonly_fields)
        assert expected <= model_fields

    def test_issuer_and_recipient_are_not_editable_in_the_admin(self):
        admin = site._registry[CapabilityGrant]
        assert "granted_by_account" in admin.readonly_fields
        assert "account" in admin.readonly_fields

    def test_admin_exposes_no_editable_autocomplete_fields(self):
        admin = site._registry[CapabilityGrant]
        assert not getattr(admin, "autocomplete_fields", ())


class TestGrantsRemainInspectable:
    def test_list_display_covers_the_auditable_columns(self):
        admin = site._registry[CapabilityGrant]
        assert "granted_by_account" in admin.list_display
        assert "revoked_at" in admin.list_display

    def test_grants_can_still_be_filtered_and_searched(self):
        admin = site._registry[CapabilityGrant]
        assert "capability_code" in admin.list_filter
        assert "capability_code" in admin.search_fields


class TestServicePathIsTheOnlyMutationPath:
    def test_grant_created_through_the_service_is_visible_to_the_admin(
        self, grant_issuer, inspector_account
    ):
        grant = grant_capability(
            actor=grant_issuer,
            account=inspector_account,
            capability_code="visit.create",
        )
        assert CapabilityGrant.objects.filter(pk=grant.pk).exists()

    def test_admin_add_would_have_missed_the_required_issuer(self):
        """Why add is disabled: the issuer is required and cannot be defaulted."""
        field = CapabilityGrant._meta.get_field("granted_by_account")
        assert field.null is False
        assert field.blank is False
