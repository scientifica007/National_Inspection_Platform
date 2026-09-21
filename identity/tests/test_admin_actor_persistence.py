"""R4-B01 regression: administrative authority requires a real persisted actor.

``require_administrative_authority`` used to trust the caller's in-memory flags
(``is_platform_admin`` and ``is_active``) through ``getattr``. A fabricated
object, an unsaved Account, or a stale instance whose row had since been
deactivated or demoted could therefore satisfy the primitive even though no
persisted acting identity held administrative authority.

The primitive now requires a real ``Account`` with a primary key, and re-reads
the stored row to confirm it is still active and still a Platform Admin. These
tests pin each of those requirements, and prove the services that depend on the
primitive inherit them.
"""

from __future__ import annotations

import pytest

from identity.models import Account
from identity.permissions import PermissionDeniedError, require_administrative_authority
from identity.services import deactivate_account, grant_capability
from identity.tests.factories import make_account

pytestmark = pytest.mark.django_db


class TestNonAccountActorsAreRejected:
    def test_plain_object_is_denied(self):
        with pytest.raises(PermissionDeniedError):
            require_administrative_authority(object(), action="test")

    def test_none_is_denied(self):
        with pytest.raises(PermissionDeniedError):
            require_administrative_authority(None, action="test")

    def test_fabricated_admin_like_object_is_denied(self):
        """Duck typing must not satisfy the primitive (the R4-B01 defect)."""

        class FabricatedAdmin:
            is_platform_admin = True
            is_active = True
            pk = 1

        with pytest.raises(PermissionDeniedError):
            require_administrative_authority(FabricatedAdmin(), action="test")

    def test_simple_namespace_admin_is_denied(self):
        from types import SimpleNamespace

        fake = SimpleNamespace(is_platform_admin=True, is_active=True, pk=1)
        with pytest.raises(PermissionDeniedError):
            require_administrative_authority(fake, action="test")


class TestUnsavedAccountsAreRejected:
    def test_unsaved_platform_admin_is_denied(self):
        """In-memory flags on a row that was never written must not authorize."""
        person = make_account(username="seed-owner").person
        unsaved = Account(
            username="unsaved-admin",
            person=person,
            is_platform_admin=True,
            is_active=True,
        )
        assert unsaved.pk is None
        with pytest.raises(PermissionDeniedError):
            require_administrative_authority(unsaved, action="test")

    def test_a_deleted_account_is_denied(self):
        """A pk that no longer resolves to a row must not authorize."""
        account = make_account(username="deleted-admin", is_platform_admin=True)
        pk = account.pk
        Account.objects.filter(pk=pk).delete()
        account.pk = pk
        with pytest.raises(PermissionDeniedError):
            require_administrative_authority(account, action="test")


class TestPersistedStateDecides:
    def test_persisted_ordinary_account_is_denied(self, inspector_account):
        with pytest.raises(PermissionDeniedError):
            require_administrative_authority(inspector_account, action="test")

    def test_persisted_active_platform_admin_is_allowed(self, grant_issuer):
        require_administrative_authority(grant_issuer, action="test")

    def test_persisted_inactive_platform_admin_is_denied(self, grant_issuer):
        grant_issuer.is_active = False
        grant_issuer.save(update_fields=["is_active"])
        with pytest.raises(PermissionDeniedError):
            require_administrative_authority(grant_issuer, action="test")


class TestStaleInMemoryActorIsDenied:
    def test_stale_actor_denied_after_its_row_is_deactivated(self, grant_issuer):
        """The in-memory object still says active; the database says otherwise."""
        stale = Account.objects.get(pk=grant_issuer.pk)
        assert stale.is_active is True

        Account.objects.filter(pk=grant_issuer.pk).update(is_active=False)

        stale.is_active = True  # flag the caller still believes
        with pytest.raises(PermissionDeniedError):
            require_administrative_authority(stale, action="test")

    def test_stale_actor_denied_after_its_row_is_demoted(self, grant_issuer):
        stale = Account.objects.get(pk=grant_issuer.pk)
        assert stale.is_platform_admin is True

        Account.objects.filter(pk=grant_issuer.pk).update(is_platform_admin=False)

        stale.is_platform_admin = True  # flag the caller still believes
        with pytest.raises(PermissionDeniedError):
            require_administrative_authority(stale, action="test")

    def test_stale_actor_allowed_while_its_row_stays_admin(self, grant_issuer):
        """Re-reading the row must not break the legitimate case."""
        stale = Account.objects.get(pk=grant_issuer.pk)
        require_administrative_authority(stale, action="test")


class TestTechnicalSuperuserIsStillDenied:
    def test_superuser_without_platform_admin_is_denied(self):
        """Django's superuser layer is not application administrative authority."""
        account = make_account(username="technical-superuser")
        account.is_superuser = True
        account.is_staff = True
        account.save(update_fields=["is_superuser", "is_staff"])
        assert account.is_superuser is True
        with pytest.raises(PermissionDeniedError):
            require_administrative_authority(account, action="test")

    def test_superuser_flag_alone_changes_nothing(self):
        """Toggling only the superuser flags must not alter the decision."""
        account = make_account(username="flag-matrix")
        for superuser, staff in ((False, False), (True, True)):
            account.is_superuser = superuser
            account.is_staff = staff
            account.save(update_fields=["is_superuser", "is_staff"])
            with pytest.raises(PermissionDeniedError):
                require_administrative_authority(account, action="test")

    def test_platform_admin_flag_alone_changes_the_decision(self):
        """The administrative flag the primitive owns is the one that matters."""
        account = make_account(username="admin-flag-matrix")
        with pytest.raises(PermissionDeniedError):
            require_administrative_authority(account, action="test")
        account.is_platform_admin = True
        account.save(update_fields=["is_platform_admin"])
        require_administrative_authority(account, action="test")


class TestMutationServicesInheritTheGate:
    def test_grant_capability_rejects_a_fabricated_actor(self, inspector_account):
        class FabricatedAdmin:
            is_platform_admin = True
            is_active = True
            pk = 1

        with pytest.raises(PermissionDeniedError):
            grant_capability(
                actor=FabricatedAdmin(),
                account=inspector_account,
                capability_code="visit.create",
            )

    def test_grant_capability_rejects_an_unsaved_actor(self, inspector_account):
        person = make_account(username="unsaved-actor-owner").person
        unsaved = Account(
            username="unsaved-actor",
            person=person,
            is_platform_admin=True,
            is_active=True,
        )
        with pytest.raises(PermissionDeniedError):
            grant_capability(
                actor=unsaved,
                account=inspector_account,
                capability_code="visit.create",
            )

    def test_deactivate_account_rejects_a_fabricated_actor(self, inspector_account):
        class FabricatedAdmin:
            is_platform_admin = True
            is_active = True
            pk = 1

        with pytest.raises(PermissionDeniedError):
            deactivate_account(actor=FabricatedAdmin(), account=inspector_account)

    def test_no_capability_was_created_by_a_rejected_grant(self, inspector_account):
        class FabricatedAdmin:
            is_platform_admin = True
            is_active = True
            pk = 1

        before = inspector_account.capability_grants.count()
        with pytest.raises(PermissionDeniedError):
            grant_capability(
                actor=FabricatedAdmin(),
                account=inspector_account,
                capability_code="visit.create",
            )
        assert inspector_account.capability_grants.count() == before
