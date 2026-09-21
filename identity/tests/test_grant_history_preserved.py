"""R2-B04 regression: grant history survives recipient Account deletion.

``CapabilityGrant.account`` used ``CASCADE``, so deleting a recipient Account
silently destroyed its authorisation history. It is now ``PROTECT``: an Account
referenced by grant history cannot be deleted through the normal ORM path.
Account deactivation remains the normal lifecycle operation.
"""

from __future__ import annotations

import pytest
from django.db.models import PROTECT, ProtectedError
from django.utils import timezone

from identity.models import CapabilityGrant
from identity.services import deactivate_account
from identity.tests.factories import make_account

pytestmark = pytest.mark.django_db


class TestRecipientDeletionIsProtected:
    def test_deleting_a_recipient_with_history_is_refused(self, grant_issuer, inspector_account):
        assert CapabilityGrant.objects.filter(account=inspector_account).exists()
        with pytest.raises(ProtectedError):
            inspector_account.delete()

    def test_the_history_is_still_present_after_the_refused_delete(
        self, grant_issuer, inspector_account
    ):
        before = CapabilityGrant.objects.filter(account=inspector_account).count()
        with pytest.raises(ProtectedError):
            inspector_account.delete()
        assert CapabilityGrant.objects.filter(account=inspector_account).count() == before

    def test_deletion_behaviour_is_protect_not_cascade(self):
        field = CapabilityGrant._meta.get_field("account")
        assert field.remote_field.on_delete is PROTECT

    def test_revoked_grants_also_protect_the_recipient(self, grant_issuer):
        """History is history even after revocation."""
        account = make_account(username="revoked-recipient")
        grant = CapabilityGrant.objects.create(
            account=account,
            capability_code="visit.create",
            granted_by_account=grant_issuer,
            revoked_at=timezone.now(),
        )
        assert grant.pk is not None
        with pytest.raises(ProtectedError):
            account.delete()


class TestAccountWithoutHistoryCanStillBeDeleted:
    def test_an_unreferenced_account_can_be_deleted(self):
        account = make_account(username="no-history-account")
        pk = account.pk
        account.delete()
        assert not type(account).objects.filter(pk=pk).exists()

    def test_account_remains_deletable_after_its_grants_are_removed(self, grant_issuer):
        account = make_account(username="history-removed")
        CapabilityGrant.objects.create(
            account=account,
            capability_code="visit.create",
            granted_by_account=grant_issuer,
        )
        CapabilityGrant.objects.filter(account=account).delete()
        account.delete()
        assert not type(account).objects.filter(pk=account.pk).exists()


class TestDeactivationIsTheNormalLifecycle:
    def test_admin_can_deactivate_a_recipient_that_has_history(
        self, grant_issuer, inspector_account
    ):
        deactivate_account(actor=grant_issuer, account=inspector_account)
        inspector_account.refresh_from_db()
        assert inspector_account.is_active is False

    def test_deactivation_preserves_the_grant_history(self, grant_issuer, inspector_account):
        before = CapabilityGrant.objects.filter(account=inspector_account).count()
        deactivate_account(actor=grant_issuer, account=inspector_account)
        assert CapabilityGrant.objects.filter(account=inspector_account).count() == before

    def test_deactivated_account_stops_authorizing_but_keeps_records(
        self, grant_issuer, inspector_account
    ):
        from identity.permissions import Capability, evaluate_capability

        deactivate_account(actor=grant_issuer, account=inspector_account)
        decision = evaluate_capability(inspector_account, Capability.VISIT_CREATE)
        assert decision.allowed is False
        assert CapabilityGrant.objects.filter(account=inspector_account).exists()

    def test_new_grant_targeting_a_deactivated_account_still_protects_it(
        self, grant_issuer, inspector_account
    ):
        """Deletion stays refused after deactivation; lifecycle is not deletion."""
        deactivate_account(actor=grant_issuer, account=inspector_account)
        with pytest.raises(ProtectedError):
            inspector_account.delete()
