"""B-04 regression: a CapabilityGrant always has a known issuer.

The blocker was a nullable ``granted_by_account`` with ``SET_NULL``, which let a
sensitive grant exist without provenance, or lose its issuer later. The
corrected model requires the issuer and protects it from deletion.
"""

from __future__ import annotations

import pytest
from django.db import IntegrityError
from django.db.models import ProtectedError

from identity.models import CapabilityGrant
from identity.permissions import Capability
from identity.services import grant_capability, revoke_capability
from identity.tests.factories import make_account

pytestmark = pytest.mark.django_db


class TestIssuerIsRequired:
    """Regression 1: a grant cannot be persisted without an issuer."""

    def test_grant_without_issuer_is_rejected_by_the_database(self, inspector_account):
        with pytest.raises(IntegrityError):
            CapabilityGrant.objects.create(
                account=inspector_account,
                capability_code=Capability.VISIT_CREATE,
            )

    def test_grant_without_issuer_is_rejected_by_validation(self, inspector_account):
        from django.core.exceptions import ValidationError

        grant = CapabilityGrant(
            account=inspector_account,
            capability_code=Capability.VISIT_CREATE,
        )
        with pytest.raises(ValidationError) as excinfo:
            grant.full_clean()
        assert "granted_by_account" in excinfo.value.message_dict

    def test_issuer_field_is_not_nullable(self):
        field = CapabilityGrant._meta.get_field("granted_by_account")
        assert field.null is False
        assert field.blank is False


class TestIssuerProvenanceIsPreserved:
    """Regression 2: the issuer cannot be deleted while it issued grants."""

    def test_issuer_deletion_is_protected(self, grant_issuer, inspector_account):
        assert CapabilityGrant.objects.filter(granted_by_account=grant_issuer).exists()
        with pytest.raises(ProtectedError):
            grant_issuer.delete()
        assert CapabilityGrant.objects.filter(granted_by_account=grant_issuer).exists()

    def test_deletion_behaviour_is_protect_not_set_null(self):
        field = CapabilityGrant._meta.get_field("granted_by_account")
        from django.db.models import PROTECT

        assert field.remote_field.on_delete is PROTECT


class TestRevocationKeepsHistory:
    """Regression 3: revoking does not rewrite who issued the grant."""

    def test_revoke_preserves_original_issuer(self, grant_issuer, inspector_account):
        grant = inspector_account.capability_grants.first()
        original_issuer_id = grant.granted_by_account_id

        revoke_capability(actor=grant_issuer, grant=grant)

        grant.refresh_from_db()
        assert grant.revoked_at is not None
        assert grant.granted_by_account_id == original_issuer_id


class TestServiceRecordsTheRealActor:
    """Regression 4: a service-created grant records the actual admin."""

    def test_grant_records_the_real_admin_actor(self, grant_issuer):
        account = make_account(
            username="grant-recipient",
            password="synthetic-recipient-pass",
            display_name="مستلم المنحة (بيانات اختبار)",
        )
        grant = grant_capability(
            actor=grant_issuer,
            account=account,
            capability_code=Capability.VISIT_CREATE,
        )
        assert grant.granted_by_account_id == grant_issuer.pk

    def test_issued_grants_are_traceable_from_the_actor(self, grant_issuer):
        account = make_account(
            username="grant-recipient-2",
            password="synthetic-recipient-pass-2",
            display_name="مستلم المنحة ٢ (بيانات اختبار)",
        )
        grant = grant_capability(
            actor=grant_issuer,
            account=account,
            capability_code=Capability.VISIT_CREATE,
        )
        assert grant in grant_issuer.grants_issued.all()

    def test_no_grant_anywhere_lacks_an_issuer(self, grant_issuer, inspector_account):
        """The invariant across all rows, not just the one just created."""
        assert CapabilityGrant.objects.filter(granted_by_account__isnull=True).count() == 0
