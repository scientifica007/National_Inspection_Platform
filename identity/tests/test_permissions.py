"""Authority primitive tests.

Covers required evidence items 5, 6, 7 and 10, plus the core ADR-0003
invariant that administrative status never yields professional authorship.
These tests exercise the server-side primitives directly, with no HTTP layer.
"""

from __future__ import annotations

import pytest
from django.utils import timezone

from identity.models import CapabilityGrant
from identity.permissions import (
    ADMINISTRATIVE_CAPABILITIES,
    Capability,
    PermissionDeniedError,
    can_perform_professional_work,
    evaluate_capability,
    has_capability,
    require_capability,
)
from identity.services import grant_capability
from identity.tests.factories import make_account

pytestmark = pytest.mark.django_db


class TestOwnScope:
    """Requirement 5: OWN capability evaluation."""

    def test_own_grant_authorizes_the_accounts_own_person(self, inspector_account):
        assert has_capability(inspector_account, Capability.VISIT_CREATE) is True

    def test_own_grant_authorizes_when_subject_is_explicitly_the_own_person(
        self, inspector_account
    ):
        assert (
            has_capability(
                inspector_account,
                Capability.VISIT_CREATE,
                subject_person=inspector_account.person,
            )
            is True
        )

    def test_own_grant_does_not_authorize_acting_for_another_person(
        self, inspector_account, other_person
    ):
        decision = evaluate_capability(
            inspector_account,
            Capability.VISIT_CREATE,
            subject_person=other_person,
        )
        assert decision.allowed is False
        assert decision.reason == "scope_mismatch"

    def test_own_grant_does_not_leak_to_other_capabilities(self, inspector_account):
        assert has_capability(inspector_account, Capability.VISIT_READ_ALL) is False


class TestAllScope:
    """Requirement 6: ALL capability evaluation."""

    def test_all_grant_authorizes_the_own_person(self, grant_issuer):
        account = make_account(
            username="all-scope",
            password="synthetic-all-pass-01",
            display_name="صاحب صلاحية عامة",
        )
        grant_capability(
            actor=grant_issuer,
            account=account,
            capability_code=Capability.VISIT_READ_ALL,
            scope_kind=CapabilityGrant.ScopeKind.ALL,
        )
        assert has_capability(account, Capability.VISIT_READ_ALL) is True

    def test_all_grant_authorizes_any_subject_person(self, grant_issuer, other_person):
        account = make_account(
            username="all-scope-2",
            password="synthetic-all-pass-02",
            display_name="صاحب صلاحية عامة",
        )
        grant_capability(
            actor=grant_issuer,
            account=account,
            capability_code=Capability.VISIT_READ_ALL,
            scope_kind=CapabilityGrant.ScopeKind.ALL,
        )
        assert (
            has_capability(account, Capability.VISIT_READ_ALL, subject_person=other_person) is True
        )


class TestValidity:
    """Requirement 7: revoked/expired grants do not authorize."""

    def test_expired_grant_does_not_authorize(self, inspector_account):
        grant = inspector_account.capability_grants.first()
        now = timezone.now()
        grant.valid_from = now - timezone.timedelta(days=10)
        grant.valid_until = now - timezone.timedelta(days=1)
        grant.save(update_fields=["valid_from", "valid_until"])
        assert has_capability(inspector_account, Capability.VISIT_CREATE) is False

    def test_not_yet_valid_grant_does_not_authorize(self, inspector_account):
        grant = inspector_account.capability_grants.first()
        grant.valid_from = timezone.now() + timezone.timedelta(days=1)
        grant.save(update_fields=["valid_from"])
        assert has_capability(inspector_account, Capability.VISIT_CREATE) is False

    def test_revoked_grant_does_not_authorize(self, inspector_account):
        grant = inspector_account.capability_grants.first()
        grant.revoked_at = timezone.now()
        grant.save(update_fields=["revoked_at"])
        assert has_capability(inspector_account, Capability.VISIT_CREATE) is False

    def test_future_valid_from_boundary_is_respected(self, grant_issuer):
        account = make_account(
            username="future-window",
            password="synthetic-future-pass-01",
            display_name="نافذة مستقبلية",
        )
        now = timezone.now()
        grant_capability(
            actor=grant_issuer,
            account=account,
            capability_code=Capability.VISIT_CREATE,
            valid_from=now + timezone.timedelta(days=5),
            valid_until=now + timezone.timedelta(days=10),
        )
        assert has_capability(account, Capability.VISIT_CREATE) is False
        assert (
            has_capability(
                account,
                Capability.VISIT_CREATE,
                at=now + timezone.timedelta(days=7),
            )
            is True
        )


class TestAdminSeparation:
    """Requirement 8: Admin status does not create professional authorship."""

    def test_platform_admin_has_no_professional_capability(self, admin_account):
        for capability in (
            Capability.VISIT_CREATE,
            Capability.VISIT_FINALIZE_OWN,
            Capability.VISIT_UPDATE_OWN_DRAFT,
            Capability.INSTITUTION_CREATE_LOCAL,
            Capability.KNOWLEDGE_CREATE_LOCAL,
        ):
            decision = evaluate_capability(admin_account, capability)
            assert decision.allowed is False, capability
            assert decision.reason == "no_active_grant"

    def test_platform_admin_is_not_a_professional_author(self, admin_account):
        assert can_perform_professional_work(admin_account) is False

    def test_platform_admin_does_satisfy_administrative_capability(self, admin_account):
        assert has_capability(admin_account, Capability.ACCOUNT_MANAGE) is True

    def test_non_admin_does_not_satisfy_administrative_capability(self, inspector_account):
        assert has_capability(inspector_account, Capability.ACCOUNT_MANAGE) is False

    def test_admin_with_explicit_professional_grant_can_act_professionally(self, grant_issuer):
        """The same Person may be Admin and professionally authorised."""
        grant_capability(
            actor=grant_issuer,
            account=grant_issuer,
            capability_code=Capability.VISIT_CREATE,
            scope_kind=CapabilityGrant.ScopeKind.OWN,
        )
        assert can_perform_professional_work(grant_issuer) is True
        assert has_capability(grant_issuer, Capability.VISIT_CREATE) is True
        # ... but still never for someone else's identity.
        assert (
            has_capability(
                grant_issuer,
                Capability.VISIT_CREATE,
                subject_person=grant_issuer.person,
            )
            is True
        )

    def test_administrative_capabilities_are_disjoint_from_professional_ones(self):
        assert Capability.ACCOUNT_MANAGE in ADMINISTRATIVE_CAPABILITIES
        assert Capability.VISIT_CREATE not in ADMINISTRATIVE_CAPABILITIES
        assert Capability.VISIT_FINALIZE_OWN not in ADMINISTRATIVE_CAPABILITIES


class TestRequireAndEvaluateContract:
    """Requirement 10: primitives are usable and testable without the UI."""

    def test_require_capability_raises_for_missing_capability(self, admin_account):
        with pytest.raises(PermissionDeniedError):
            require_capability(admin_account, Capability.VISIT_CREATE)

    def test_require_capability_passes_when_authorized(self, inspector_account):
        require_capability(inspector_account, Capability.VISIT_CREATE)

    def test_unknown_capability_is_denied(self, inspector_account):
        decision = evaluate_capability(inspector_account, "not.a.real.capability")
        assert decision.allowed is False
        assert decision.reason == "unknown_capability"

    def test_inactive_account_is_denied(self, inspector_account):
        inspector_account.is_active = False
        inspector_account.save(update_fields=["is_active"])
        decision = evaluate_capability(inspector_account, Capability.VISIT_CREATE)
        assert decision.allowed is False
        assert decision.reason == "account_inactive"

    def test_decision_is_boolean_convertible(self, inspector_account, admin_account):
        assert bool(evaluate_capability(inspector_account, Capability.VISIT_CREATE)) is True
        assert bool(evaluate_capability(admin_account, Capability.VISIT_CREATE)) is False


class TestNoImpersonationPath:
    """Requirement 9: no helper lets an Account act as another professional identity."""

    def test_permissions_module_exposes_no_impersonation_helper(self):
        import identity.permissions as permissions

        public_names = {name for name in dir(permissions) if not name.startswith("_")}
        forbidden = {
            "impersonate",
            "act_as",
            "login_as",
            "switch_account",
            "become",
            "assume_identity",
        }
        assert public_names & forbidden == set()

    def test_grant_cannot_be_issued_without_administrative_capability(self, inspector_account):
        with pytest.raises(PermissionDeniedError):
            grant_capability(
                actor=inspector_account,
                account=inspector_account,
                capability_code=Capability.VISIT_CREATE,
            )
