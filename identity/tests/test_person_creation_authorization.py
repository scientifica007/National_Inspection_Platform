"""R3-B02 regression: standalone Person creation is authorized.

``identity.services.create_person`` was an application identity mutation with
no actor and no authorization. It now requires an active real Platform Admin,
the same narrow rule the other administrative commands use. A Person created as
mere test/seed *data* bypasses this deliberately through the test factory; the
product path is gated.
"""

from __future__ import annotations

import pytest

from identity.models import CapabilityGrant, Person
from identity.permissions import Capability, PermissionDeniedError
from identity.services import create_person
from identity.tests.factories import make_account

pytestmark = pytest.mark.django_db


class TestNonAdminIsDenied:
    def test_plain_account_cannot_create_a_person(self, inspector_account):
        before = Person.objects.count()
        with pytest.raises(PermissionDeniedError):
            create_person(actor=inspector_account, display_name="شخص مرفوض (بيانات اختبار)")
        assert Person.objects.count() == before

    def test_account_manage_grant_does_not_authorize_person_creation(
        self, grant_issuer, inspector_account
    ):
        CapabilityGrant.objects.create(
            account=inspector_account,
            capability_code=Capability.ACCOUNT_MANAGE,
            scope_kind=CapabilityGrant.ScopeKind.ALL,
            granted_by_account=grant_issuer,
        )
        with pytest.raises(PermissionDeniedError):
            create_person(
                actor=inspector_account,
                display_name="شخص بتصريح إداري (بيانات اختبار)",
            )

    def test_no_person_is_created_on_denial(self, inspector_account):
        with pytest.raises(PermissionDeniedError):
            create_person(actor=inspector_account, display_name="لن يُنشأ")
        assert not Person.objects.filter(display_name="لن يُنشأ").exists()

    def test_an_arbitrary_object_is_not_an_actor(self, db):
        """A non-Account actor must not slip through the authority check."""
        with pytest.raises(PermissionDeniedError):
            create_person(actor=object(), display_name="كائن وهمي")


class TestInactivePlatformAdminIsDenied:
    def test_inactive_admin_cannot_create_a_person(self, grant_issuer):
        grant_issuer.is_active = False
        grant_issuer.save(update_fields=["is_active"])
        before = Person.objects.count()
        with pytest.raises(PermissionDeniedError):
            create_person(actor=grant_issuer, display_name="شخص لحساب معطّل")
        assert Person.objects.count() == before


class TestActivePlatformAdminIsAllowed:
    def test_active_admin_can_create_a_person(self, grant_issuer):
        person = create_person(actor=grant_issuer, display_name="شخص مصرّح (بيانات اختبار)")
        assert person.pk is not None
        assert person.display_name == "شخص مصرّح (بيانات اختبار)"

    def test_created_person_has_no_account_and_no_capability(self, grant_issuer):
        person = create_person(actor=grant_issuer, display_name="شخص بلا حساب (بيانات اختبار)")
        assert not hasattr(person, "account")
        assert CapabilityGrant.objects.filter(account__person=person).count() == 0

    def test_created_person_is_persisted(self, grant_issuer):
        person = create_person(actor=grant_issuer, display_name="شخص محفوظ")
        assert Person.objects.filter(pk=person.pk).exists()

    def test_create_person_requires_an_actor_keyword(self):
        """The gate is unreachable-by-omission: no default actor exists."""
        import inspect

        from identity.services import create_person

        parameters = inspect.signature(create_person).parameters
        assert "actor" in parameters
        assert parameters["actor"].default is inspect.Parameter.empty

    def test_no_delegation_intake_was_added_to_the_person_services(self):
        """R3-B02 forbids adding a delegation engine for this correction."""
        from identity.permissions import (
            ADMINISTRATIVE_CAPABILITIES,
            ALL_CAPABILITIES,
            Capability,
        )

        assert set(ALL_CAPABILITIES) == {
            Capability.INSTITUTION_CREATE_LOCAL,
            Capability.INSTITUTION_READ_OWN,
            Capability.KNOWLEDGE_CREATE_LOCAL,
            Capability.KNOWLEDGE_READ_OWN,
            Capability.VISIT_CREATE,
            Capability.VISIT_READ_OWN,
            Capability.VISIT_UPDATE_OWN_DRAFT,
            Capability.VISIT_FINALIZE_OWN,
            Capability.VISIT_READ_ALL,
            Capability.ACCOUNT_MANAGE,
        }
        assert ADMINISTRATIVE_CAPABILITIES == {Capability.ACCOUNT_MANAGE}

    def test_created_person_can_later_receive_an_account(self, grant_issuer):
        """The authorized use case: register a human, bind them later."""
        person = create_person(actor=grant_issuer, display_name="شخص ثم حساب")
        from identity.services import create_account

        account = create_account(
            actor=grant_issuer,
            username="person-then-account",
            password="synthetic-person-then-account-pass",
            person=person,
        )
        assert account.person_id == person.pk

    def test_factory_person_bypass_is_test_only(self):
        from identity.tests.factories import make_person

        assert make_person(display_name="شخص مصنع").pk is not None

    def test_make_account_still_creates_its_own_person(self):
        account = make_account(username="factory-owner")
        assert account.person_id is not None
