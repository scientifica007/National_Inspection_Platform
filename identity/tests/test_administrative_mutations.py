"""B-01 regression: administrative mutations cannot be self-escalated.

The blocker was that a non-admin Account holding an ``account.manage``
CapabilityGrant could call the administrative service commands and grant itself
or others arbitrary capabilities. These tests pin the corrected rule: only a
real Platform Admin may run administrative mutations, and an
``account.manage`` grant does not satisfy them.
"""

from __future__ import annotations

import pytest

from identity.models import CapabilityGrant
from identity.permissions import (
    ADMINISTRATIVE_CAPABILITIES,
    Capability,
    PermissionDeniedError,
    evaluate_capability,
    has_capability,
    require_administrative_authority,
)
from identity.services import (
    deactivate_account,
    grant_capability,
    revoke_capability,
)
from identity.tests.factories import make_account

pytestmark = pytest.mark.django_db


@pytest.fixture
def non_admin_with_account_manage(grant_issuer):
    """A non-admin Account that was granted ``account.manage`` directly.

    Seeding the grant directly (rather than through the service) models the
    escalation attempt at its strongest: the row exists in the database.
    """
    account = make_account(
        username="pseudo-admin",
        display_name="مسؤول غير حقيقي (بيانات اختبار)",
    )
    CapabilityGrant.objects.create(
        account=account,
        capability_code=Capability.ACCOUNT_MANAGE,
        scope_kind=CapabilityGrant.ScopeKind.ALL,
        granted_by_account=grant_issuer,
    )
    return account


@pytest.fixture
def victim_account(db):
    return make_account(
        username="target-account",
        display_name="حساب مستهدف (بيانات اختبار)",
    )


class TestNonAdminCannotEscalate:
    """Required regressions 1-4: an account.manage grant is not administrative power."""

    def test_cannot_grant_itself_a_professional_capability(self, non_admin_with_account_manage):
        """Regression 1."""
        with pytest.raises(PermissionDeniedError):
            grant_capability(
                actor=non_admin_with_account_manage,
                account=non_admin_with_account_manage,
                capability_code=Capability.VISIT_CREATE,
                scope_kind=CapabilityGrant.ScopeKind.OWN,
            )
        assert (
            non_admin_with_account_manage.capability_grants.filter(
                capability_code=Capability.VISIT_CREATE
            ).count()
            == 0
        )

    def test_cannot_grant_another_account_a_capability(
        self, non_admin_with_account_manage, victim_account
    ):
        """Regression 2."""
        with pytest.raises(PermissionDeniedError):
            grant_capability(
                actor=non_admin_with_account_manage,
                account=victim_account,
                capability_code=Capability.VISIT_READ_ALL,
                scope_kind=CapabilityGrant.ScopeKind.ALL,
            )
        assert victim_account.capability_grants.count() == 0

    def test_cannot_revoke_a_grant(self, non_admin_with_account_manage, inspector_account):
        """Regression 3."""
        grant = inspector_account.capability_grants.first()
        with pytest.raises(PermissionDeniedError):
            revoke_capability(actor=non_admin_with_account_manage, grant=grant)
        grant.refresh_from_db()
        assert grant.revoked_at is None

    def test_cannot_deactivate_another_account(self, non_admin_with_account_manage, victim_account):
        """Regression 4."""
        with pytest.raises(PermissionDeniedError):
            deactivate_account(actor=non_admin_with_account_manage, account=victim_account)
        victim_account.refresh_from_db()
        assert victim_account.is_active is True

    def test_account_manage_grant_does_not_satisfy_the_mutation_primitive(
        self, non_admin_with_account_manage
    ):
        with pytest.raises(PermissionDeniedError):
            require_administrative_authority(non_admin_with_account_manage)

    def test_account_manage_grant_does_not_report_administrative_authority(
        self, non_admin_with_account_manage
    ):
        """The query-side view agrees: the grant is not administrative power."""
        assert has_capability(non_admin_with_account_manage, Capability.ACCOUNT_MANAGE) is False
        decision = evaluate_capability(non_admin_with_account_manage, Capability.ACCOUNT_MANAGE)
        assert decision.reason == "not_platform_admin"

    def test_account_manage_grant_confers_no_professional_authority(
        self, non_admin_with_account_manage
    ):
        assert has_capability(non_admin_with_account_manage, Capability.VISIT_CREATE) is False


class TestPlatformAdminCanStillAdminister:
    """Regression 5: the intended administrative mutations keep working."""

    def test_platform_admin_can_grant(self, grant_issuer, victim_account):
        grant = grant_capability(
            actor=grant_issuer,
            account=victim_account,
            capability_code=Capability.VISIT_CREATE,
            scope_kind=CapabilityGrant.ScopeKind.OWN,
        )
        assert grant.pk is not None
        assert victim_account.capability_grants.filter(pk=grant.pk).exists()

    def test_platform_admin_can_revoke(self, grant_issuer, inspector_account):
        grant = inspector_account.capability_grants.first()
        revoke_capability(actor=grant_issuer, grant=grant)
        grant.refresh_from_db()
        assert grant.revoked_at is not None

    def test_platform_admin_can_deactivate(self, grant_issuer, victim_account):
        deactivate_account(actor=grant_issuer, account=victim_account)
        victim_account.refresh_from_db()
        assert victim_account.is_active is False

    def test_platform_admin_still_cannot_deactivate_itself(self, grant_issuer):
        with pytest.raises(PermissionDeniedError):
            deactivate_account(actor=grant_issuer, account=grant_issuer)


class TestAdminStatusIsNotProfessionalAuthorship:
    """Regression 6: administrative authority alone is never authorship."""

    def test_platform_admin_gaining_admin_power_does_not_make_it_an_author(self, grant_issuer):
        assert has_capability(grant_issuer, Capability.ACCOUNT_MANAGE) is True
        assert has_capability(grant_issuer, Capability.VISIT_CREATE) is False
        assert has_capability(grant_issuer, Capability.VISIT_FINALIZE_OWN) is False

    def test_mutation_primitive_does_not_imply_professional_work(self, grant_issuer):
        require_administrative_authority(grant_issuer)
        assert has_capability(grant_issuer, Capability.VISIT_CREATE) is False


class TestAdministrativeCapabilitySemantics:
    def test_administrative_capability_is_satisfied_only_by_platform_admin(
        self, grant_issuer, non_admin_with_account_manage
    ):
        assert has_capability(grant_issuer, Capability.ACCOUNT_MANAGE) is True
        assert has_capability(non_admin_with_account_manage, Capability.ACCOUNT_MANAGE) is False

    def test_inactive_platform_admin_cannot_run_mutations(self, grant_issuer):
        """Deactivation must remove administrative reach, not just login."""
        grant_issuer.is_active = False
        grant_issuer.save(update_fields=["is_active"])
        with pytest.raises(PermissionDeniedError):
            require_administrative_authority(grant_issuer)

    def test_administrative_capability_set_is_still_only_account_manage(self):
        assert ADMINISTRATIVE_CAPABILITIES == {Capability.ACCOUNT_MANAGE}
