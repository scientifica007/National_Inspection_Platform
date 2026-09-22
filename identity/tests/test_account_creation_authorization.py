"""R2-B01 regression: application account creation is an authorized mutation.

``identity.services.create_account`` was an ungated application service: any
caller could create an Account and could set ``is_platform_admin=True``. It now
requires an active real Platform Admin actor. Seeding the first Platform Admin
is a separate technical concern (``identity.bootstrap``), which must not weaken
the application service.
"""

from __future__ import annotations

import ast

import pytest

from identity.bootstrap import bootstrap_platform_admin
from identity.models import Account, CapabilityGrant
from identity.permissions import Capability, PermissionDeniedError
from identity.services import create_account, create_person
from identity.tests.factories import make_account

pytestmark = pytest.mark.django_db


class TestNonAdminCannotCreateAccounts:
    def test_plain_account_cannot_create_an_account(self, inspector_account):
        before = Account.objects.count()
        with pytest.raises(PermissionDeniedError):
            create_account(
                actor=inspector_account,
                username="smuggled-account",
                password="synthetic-smuggled-pass",
            )
        assert Account.objects.count() == before

    def test_account_manage_grant_does_not_authorize_creation(
        self, grant_issuer, inspector_account
    ):
        """An ``account.manage`` grant is not administrative authority (R1-B01)."""
        CapabilityGrant.objects.create(
            account=inspector_account,
            capability_code=Capability.ACCOUNT_MANAGE,
            scope_kind=CapabilityGrant.ScopeKind.ALL,
            granted_by_account=grant_issuer,
        )
        with pytest.raises(PermissionDeniedError):
            create_account(
                actor=inspector_account,
                username="escalated-admin",
                password="synthetic-escalated-pass",
                is_platform_admin=True,
            )
        assert not Account.objects.filter(username="escalated-admin").exists()

    def test_non_admin_cannot_create_a_platform_admin(self, inspector_account):
        with pytest.raises(PermissionDeniedError):
            create_account(
                actor=inspector_account,
                username="new-admin",
                password="synthetic-new-admin-pass",
                is_platform_admin=True,
            )

    def test_inactive_platform_admin_cannot_create_an_account(self, grant_issuer):
        grant_issuer.is_active = False
        grant_issuer.save(update_fields=["is_active"])
        with pytest.raises(PermissionDeniedError):
            create_account(
                actor=grant_issuer,
                username="deferred-account",
                password="synthetic-deferred-pass",
            )


class TestActivePlatformAdminCanCreateAccounts:
    def test_admin_can_create_an_ordinary_account(self, grant_issuer):
        account = create_account(
            actor=grant_issuer,
            username="ordinary-created",
            password="synthetic-ordinary-pass",
            display_name="حساب عادي (بيانات اختبار)",
        )
        assert account.pk is not None
        assert account.is_platform_admin is False

    def test_admin_can_create_a_platform_admin_account(self, grant_issuer):
        account = create_account(
            actor=grant_issuer,
            username="second-admin",
            password="synthetic-second-admin-pass",
            is_platform_admin=True,
        )
        assert account.is_platform_admin is True

    def test_created_account_authenticates_with_its_password(self, grant_issuer):
        create_account(
            actor=grant_issuer,
            username="login-check",
            password="synthetic-login-check-pass",
        )
        account = Account.objects.get(username="login-check")
        assert account.check_password("synthetic-login-check-pass") is True

    def test_created_account_binds_the_explicitly_supplied_person(self, grant_issuer):
        person = create_person(actor=grant_issuer, display_name="شخص صريح (بيانات اختبار)")
        account = create_account(
            actor=grant_issuer,
            username="bound-account",
            password="synthetic-bound-pass",
            person=person,
        )
        assert account.person_id == person.pk

    def test_created_account_is_not_a_professional_author(self, grant_issuer):
        """Creating an admin Account must not confer professional authorship."""
        account = create_account(
            actor=grant_issuer,
            username="no-authorship",
            password="synthetic-no-authorship-pass",
            is_platform_admin=True,
        )
        assert account.capability_grants.count() == 0


class TestBootstrapIsSeparateAndNarrow:
    """The seed-admin path exists, but must not imply editorial authorship."""

    def test_bootstrap_creates_a_platform_admin(self):
        account = bootstrap_platform_admin(
            username="seeded-admin",
            password="synthetic-seeded-pass",
            display_name="مدير مبدئي (بيانات اختبار)",
        )
        assert account.is_platform_admin is True
        assert account.is_active is True

    def test_bootstrap_grants_no_professional_capability(self):
        account = bootstrap_platform_admin(
            username="seeded-admin-2",
            password="synthetic-seeded-pass-2",
        )
        assert account.capability_grants.count() == 0

    def test_bootstrap_creates_its_own_person(self):
        account = bootstrap_platform_admin(
            username="seeded-admin-3",
            password="synthetic-seeded-pass-3",
            display_name="مدير مبدئي ٣ (بيانات اختبار)",
        )
        assert account.person_id is not None
        assert account.person.display_name == "مدير مبدئي ٣ (بيانات اختبار)"

    def test_service_does_not_import_bootstrap(self):
        """The gated service must not be weakened by the bootstrap entry point."""
        import inspect

        from identity import services

        imported_names = {
            alias.name
            for node in ast.walk(ast.parse(inspect.getsource(services)))
            if isinstance(node, ast.ImportFrom)
            for alias in node.names
        } | {
            alias.name
            for node in ast.walk(ast.parse(inspect.getsource(services)))
            if isinstance(node, ast.Import)
            for alias in node.names
        }
        assert "bootstrap" not in imported_names
        assert "identity.bootstrap" not in imported_names

    def test_services_module_has_no_bootstrap_attribute(self):
        from identity import services

        assert not hasattr(services, "bootstrap_platform_admin")

    def test_bootstrapped_admin_can_then_create_accounts(self):
        admin = bootstrap_platform_admin(
            username="seed-then-create",
            password="synthetic-seed-then-create-pass",
        )
        created = create_account(
            actor=admin,
            username="created-by-seed-admin",
            password="synthetic-created-by-seed-pass",
        )
        assert created.pk is not None

    def test_make_account_factory_bypass_is_test_only(self):
        """Guard: the test factory is not exported from the application package."""
        import identity

        assert not hasattr(identity, "make_account")
        assert make_account(username="factory-check").pk is not None

    def test_permissions_module_has_no_creation_shortcut(self):
        import inspect

        from identity import permissions

        source = inspect.getsource(permissions)
        assert "is_superuser" not in source
