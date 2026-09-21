"""Identity model tests.

Covers required evidence items 1, 2 and the model-side of item 7.
"""

from __future__ import annotations

import pytest
from django.apps import apps
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.db.models import ProtectedError
from django.utils import timezone

from identity.models import Account, CapabilityGrant, Person

pytestmark = pytest.mark.django_db


def test_custom_account_is_the_configured_user_model():
    """Requirement 1: the custom Account is Django's user model from day one."""
    assert settings.AUTH_USER_MODEL == "identity.Account"
    assert get_user_model() is Account
    assert Account._meta.pk.name == "id"


def test_person_and_account_are_one_to_one():
    """Requirement 2: Person <-> Account relationship works."""
    person = Person.objects.create(display_name="أحمد التجريبي")
    account = Account.objects.create_user(
        username="one-to-one", password="synthetic-pass-01", person=person
    )

    assert account.person == person
    assert person.account == account

    with pytest.raises(IntegrityError):
        Account.objects.create_user(username="duplicate-person", password="x", person=person)


def test_account_creation_creates_its_own_person_when_none_given():
    account = Account.objects.create_user(
        username="auto-person", password="synthetic-pass-01", display_name="شخص تلقائي"
    )
    assert account.person.display_name == "شخص تلقائي"
    assert Person.objects.filter(account=account).count() == 1


def test_account_person_cannot_be_shared_across_accounts():
    person = Person.objects.create(display_name="شخص واحد")
    Account.objects.create_user(username="first", password="synthetic-pass-01", person=person)
    with pytest.raises(IntegrityError):
        Account.objects.create_user(username="second", password="synthetic-pass-01", person=person)


def test_person_deletion_is_protected_while_account_exists():
    """Disabling/deleting an Account must not silently drop the Person."""
    person = Person.objects.create(display_name="شخص محمي")
    account = Account.objects.create_user(
        username="protected", password="synthetic-pass-01", person=person
    )
    with pytest.raises(ProtectedError):
        person.delete()
    assert Account.objects.filter(pk=account.pk).exists()


class TestCapabilityGrantValidity:
    """Requirement 7: revoked/expired grants do not authorize."""

    def _grant(self, account, **kwargs):
        return CapabilityGrant.objects.create(
            account=account, capability_code="visit.create", **kwargs
        )

    def test_unbounded_grant_is_valid(self, inspector_account):
        grant = self._grant(inspector_account, scope_kind=CapabilityGrant.ScopeKind.OWN)
        assert grant.is_valid_at() is True
        assert grant.is_revoked is False

    def test_expired_grant_is_not_valid(self, inspector_account):
        now = timezone.now()
        grant = self._grant(
            inspector_account,
            valid_from=now - timezone.timedelta(days=10),
            valid_until=now - timezone.timedelta(days=1),
        )
        assert grant.is_valid_at() is False

    def test_not_yet_started_grant_is_not_valid(self, inspector_account):
        now = timezone.now()
        grant = self._grant(inspector_account, valid_from=now + timezone.timedelta(days=1))
        assert grant.is_valid_at() is False

    def test_revoked_grant_is_not_valid(self, inspector_account):
        grant = self._grant(inspector_account, revoked_at=timezone.now())
        assert grant.is_revoked is True
        assert grant.is_valid_at() is False

    def test_scope_kind_is_limited_to_own_and_all(self):
        """Slice 01 supports OWN and ALL only; no generic scope engine."""
        assert set(CapabilityGrant.ScopeKind.values) == {"OWN", "ALL"}

    def test_invalid_validity_window_is_rejected_by_clean(self, inspector_account):
        now = timezone.now()
        grant = CapabilityGrant(
            account=inspector_account,
            capability_code="visit.create",
            valid_from=now,
            valid_until=now - timezone.timedelta(days=1),
        )
        with pytest.raises(ValidationError):
            grant.full_clean()

    def test_validity_window_order_is_enforced_by_database(self, inspector_account):
        now = timezone.now()
        with pytest.raises(IntegrityError):
            CapabilityGrant.objects.create(
                account=inspector_account,
                capability_code="visit.create",
                valid_from=now,
                valid_until=now - timezone.timedelta(days=1),
            )


def test_identity_app_owns_only_identity_concepts():
    """The identity module models Person, Account and CapabilityGrant only."""
    model_names = {model.__name__ for model in apps.get_app_config("identity").get_models()}
    assert model_names == {"Person", "Account", "CapabilityGrant"}
