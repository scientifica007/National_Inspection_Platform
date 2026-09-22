"""R4.1 residual regression: an unsaved Account must not borrow a real PK.

R4-B01 was corrected by rejecting non-``Account`` actors, ``pk is None``,
missing rows, inactive rows and demoted rows, and by re-reading the stored row.
One residual case survived that pass: an *unsaved* ``Account`` instance given an
explicit ``pk`` copied from a real Platform Admin.

``pk is not None`` cannot distinguish "this instance is persisted" from "this
instance merely carries a primary key value". The database lookup then resolved
to the genuine privileged row and authorized the mutation, while the actor
object handed to the services was never the persisted identity. Because
provenance (``granted_by_account``) is written from the actor, that let a
fabricated instance attribute its mutation to the real admin's FK.

The primitive now requires the actor to be an actually-saved instance
(``_state.adding`` is False) *and* the stored row to be the current active
Platform Admin. These tests pin both halves.
"""

from __future__ import annotations

import pytest

from identity.models import Account
from identity.permissions import PermissionDeniedError, require_administrative_authority
from identity.services import create_person, grant_capability
from identity.tests.factories import make_account

pytestmark = pytest.mark.django_db


def _unsaved_account_with_borrowed_pk(real_admin: Account, username: str) -> Account:
    """A distinct, unsaved instance carrying a real admin's primary key."""
    borrowed = Account(
        username=username,
        is_platform_admin=True,
        is_active=True,
    )
    borrowed.pk = real_admin.pk
    assert borrowed._state.adding is True
    return borrowed


class TestUnsavedAccountWithExplicitPk:
    def test_borrowed_pk_instance_is_denied(self, grant_issuer):
        """The exact R4.1 residual: unsaved instance, real admin's pk."""
        assert grant_issuer.is_platform_admin is True
        assert grant_issuer.is_active is True

        borrowed = _unsaved_account_with_borrowed_pk(grant_issuer, "borrowed-pk")

        with pytest.raises(PermissionDeniedError):
            require_administrative_authority(borrowed, action="test")

    def test_genuine_loaded_platform_admin_still_succeeds(self, grant_issuer):
        """The legitimate persisted actor is unaffected by the tightening."""
        genuine = Account.objects.get(pk=grant_issuer.pk)
        assert genuine._state.adding is False
        require_administrative_authority(genuine, action="test")

    def test_borrowed_pk_instance_is_denied_even_when_flags_match(self, grant_issuer):
        """Matching the admin's own flags must not help an unsaved instance."""
        borrowed = Account(username="flags-match", is_platform_admin=True, is_active=True)
        borrowed.pk = grant_issuer.pk
        borrowed.is_superuser = True
        borrowed.is_staff = True
        with pytest.raises(PermissionDeniedError):
            require_administrative_authority(borrowed, action="test")

    def test_detached_reload_is_not_treated_as_unsaved(self, grant_issuer):
        """A row-loaded instance that was then modified in memory still passes.

        Tightening must target the unsaved state, not merely "the object is not
        the exact instance that was last saved".
        """
        reloaded = Account.objects.get(pk=grant_issuer.pk)
        reloaded.email = "changed-in-memory@example.invalid"
        require_administrative_authority(reloaded, action="test")


class TestMutationServicesRejectBorrowedPkActors:
    def test_grant_capability_rejects_a_borrowed_pk_actor(self, grant_issuer, inspector_account):
        borrowed = _unsaved_account_with_borrowed_pk(grant_issuer, "borrowed-grant")
        before = inspector_account.capability_grants.count()

        with pytest.raises(PermissionDeniedError):
            grant_capability(
                actor=borrowed,
                account=inspector_account,
                capability_code="visit.create",
            )

        assert inspector_account.capability_grants.count() == before

    def test_grant_capability_does_not_record_the_real_admin_as_issuer(
        self, grant_issuer, inspector_account
    ):
        """No new grant may appear, so provenance cannot name the real admin."""
        from identity.models import CapabilityGrant
        from identity.permissions import Capability

        borrowed = _unsaved_account_with_borrowed_pk(grant_issuer, "borrowed-provenance")
        before = CapabilityGrant.objects.filter(
            granted_by_account=grant_issuer,
            capability_code=Capability.KNOWLEDGE_CREATE_LOCAL,
        ).count()

        with pytest.raises(PermissionDeniedError):
            grant_capability(
                actor=borrowed,
                account=inspector_account,
                capability_code=Capability.KNOWLEDGE_CREATE_LOCAL,
            )

        after = CapabilityGrant.objects.filter(
            granted_by_account=grant_issuer,
            capability_code=Capability.KNOWLEDGE_CREATE_LOCAL,
        ).count()
        assert after == before

    def test_create_person_rejects_a_borrowed_pk_actor(self, grant_issuer):
        from identity.models import Person

        borrowed = _unsaved_account_with_borrowed_pk(grant_issuer, "borrowed-person")
        before = Person.objects.count()

        with pytest.raises(PermissionDeniedError):
            create_person(actor=borrowed, display_name="شخص غير مصرّح")

        assert Person.objects.count() == before

    def test_services_still_work_for_a_genuine_admin(self, grant_issuer, inspector_account):
        """The tightening must not break the authorized path end to end."""
        genuine = Account.objects.get(pk=grant_issuer.pk)
        created = create_person(actor=genuine, display_name="شخص مصرّح")
        assert created.pk is not None


class TestOtherUnsavedShapesRemainDenied:
    def test_unsaved_account_without_pk_is_denied(self, grant_issuer):
        unsaved = Account(
            username="no-pk",
            person=make_account(username="no-pk-owner").person,
            is_platform_admin=True,
            is_active=True,
        )
        assert unsaved.pk is None
        with pytest.raises(PermissionDeniedError):
            require_administrative_authority(unsaved, action="test")

    def test_unsaved_instance_with_borrowed_pk_of_ordinary_account_is_denied(self):
        ordinary = make_account(username="ordinary-peer")
        borrowed = Account(username="peer-borrow", is_platform_admin=True, is_active=True)
        borrowed.pk = ordinary.pk
        assert borrowed._state.adding is True
        with pytest.raises(PermissionDeniedError):
            require_administrative_authority(borrowed, action="test")

    def test_unsaved_instance_borrowing_pk_of_deactivated_admin_is_denied(self, grant_issuer):
        Account.objects.filter(pk=grant_issuer.pk).update(is_active=False)

        borrowed = Account(username="borrow-deactivated", is_platform_admin=True, is_active=True)
        borrowed.pk = grant_issuer.pk
        with pytest.raises(PermissionDeniedError):
            require_administrative_authority(borrowed, action="test")
