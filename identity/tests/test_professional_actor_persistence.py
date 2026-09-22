"""R5-B01 — generic professional authority must not trust the caller's Account.

The administrative mutation primitive was hardened in R4/R4.1. The *generic*
professional evaluator still trusted the caller-supplied instance: it read
``is_active`` from the object and queried ``account.capability_grants`` through
the supplied primary key. An unsaved, fabricated Account could therefore copy a
real professional Account's ``pk`` and ``person_id`` and inherit its stored
grants.

These tests pin the closure: every professional authority evaluation and read
helper resolves the *persisted* Account row first and denies a fabricated,
unsaved, borrowed-PK, missing or stale actor (docs/INVARIANTS.md §Actor Always
Known, §Identity Cannot Be Borrowed).

All data is synthetic (docs/SECURITY_AND_DATA_GOVERNANCE.md).
"""

from __future__ import annotations

import pytest

from identity.models import Account, CapabilityGrant
from identity.permissions import (
    REASON_ACTOR_NOT_FOUND,
    REASON_ACTOR_NOT_PERSISTED,
    REASON_INVALID_ACTOR,
    Capability,
    PermissionDeniedError,
    can_perform_professional_work,
    evaluate_capability,
    has_capability,
    is_platform_admin,
    require_capability,
    resolve_persisted_account,
)
from identity.services import grant_capability
from identity.tests.factories import make_account

pytestmark = pytest.mark.django_db


def _borrowed_identity_of(account: Account, *, username: str = "borrowed") -> Account:
    """Build an unsaved Account carrying ``account``'s pk and Person binding.

    This is precisely the fabrication the finding describes: the object is not
    persisted and was never saved, yet it presents the real Account's primary
    key, Person id and a favourable in-memory active state.
    """
    imported = Account(
        username=username,
        person=account.person,
        is_active=True,
    )
    imported.pk = account.pk
    return imported


class TestProfessionalOwnGrantCannotBeBorrowed:
    """Requirement 1: borrowed pk + person_id cannot satisfy an OWN grant."""

    def test_borrowed_identity_is_denied(self, inspector_account):
        fabricated = _borrowed_identity_of(inspector_account)
        decision = evaluate_capability(fabricated, Capability.VISIT_CREATE)
        assert decision.allowed is False
        assert decision.reason == REASON_ACTOR_NOT_PERSISTED

    def test_borrowed_identity_has_no_professional_capability(self, inspector_account):
        fabricated = _borrowed_identity_of(inspector_account)
        assert has_capability(fabricated, Capability.VISIT_CREATE) is False

    def test_borrowed_identity_cannot_satisfy_own_scope_via_subject(self, inspector_account):
        """Even naming the real Person as the subject must not authorise it."""
        fabricated = _borrowed_identity_of(inspector_account)
        decision = evaluate_capability(
            fabricated,
            Capability.VISIT_CREATE,
            subject_person=inspector_account.person,
        )
        assert decision.allowed is False
        assert decision.reason == REASON_ACTOR_NOT_PERSISTED

    def test_unsaved_account_without_pk_is_denied(self, inspector_account):
        unsaved = Account(username="no-pk", person=inspector_account.person, is_active=True)
        assert evaluate_capability(unsaved, Capability.VISIT_CREATE).reason == (
            REASON_ACTOR_NOT_PERSISTED
        )

    def test_account_shaped_object_is_denied(self, inspector_account):
        class FabricatedAccount:
            pk = 1
            person_id = None
            is_active = True
            is_platform_admin = True
            capability_grants = None

        assert evaluate_capability(FabricatedAccount(), Capability.VISIT_CREATE).reason == (
            REASON_INVALID_ACTOR
        )

    def test_deleted_row_yields_actor_not_found(self, grant_issuer):
        """A row removed behind a loaded instance is caught by the lookup."""
        ghost = make_account(username="ghost-row")
        pk = ghost.pk
        Account.objects.filter(pk=pk).delete()
        decision = evaluate_capability(ghost, Capability.VISIT_CREATE)
        assert decision.allowed is False
        assert decision.reason in {REASON_ACTOR_NOT_PERSISTED, REASON_ACTOR_NOT_FOUND}


class TestProfessionalAllGrantCannotBeBorrowed:
    """Requirement 2: borrowed identity cannot satisfy an ALL grant."""

    @pytest.fixture
    def all_granted(self, grant_issuer):
        account = make_account(username="all-granted", display_name="نطاق عام (بيانات اختبار)")
        grant_capability(
            actor=grant_issuer,
            account=account,
            capability_code=Capability.VISIT_READ_ALL,
            scope_kind=CapabilityGrant.ScopeKind.ALL,
        )
        return account

    def test_borrowed_identity_is_denied(self, all_granted):
        fabricated = _borrowed_identity_of(all_granted)
        decision = evaluate_capability(fabricated, Capability.VISIT_READ_ALL)
        assert decision.allowed is False
        assert decision.reason == REASON_ACTOR_NOT_PERSISTED

    def test_borrowed_identity_cannot_read_all(self, all_granted, other_person):
        fabricated = _borrowed_identity_of(all_granted)
        assert (
            has_capability(fabricated, Capability.VISIT_READ_ALL, subject_person=other_person)
            is False
        )

    def test_borrowed_identity_has_no_professional_work(self, all_granted):
        assert can_perform_professional_work(_borrowed_identity_of(all_granted)) is False


class TestRequireCapabilityRaisesForFabricatedActor:
    """Requirement 3: require_capability raises for a fabricated actor."""

    def test_raises_for_borrowed_own_identity(self, inspector_account):
        fabricated = _borrowed_identity_of(inspector_account)
        with pytest.raises(PermissionDeniedError):
            require_capability(fabricated, Capability.VISIT_CREATE)

    def test_raises_for_account_shaped_object(self):
        class FabricatedAccount:
            pk = 1
            person_id = None
            is_active = True
            is_platform_admin = True

        with pytest.raises(PermissionDeniedError):
            require_capability(FabricatedAccount(), Capability.VISIT_CREATE)

    def test_passes_for_a_genuine_persisted_account(self, inspector_account):
        require_capability(inspector_account, Capability.VISIT_CREATE)


class TestStaleActorIsDenied:
    """Requirement 4: the stored row decides, not the caller's in-memory copy."""

    def test_stale_instance_denied_after_stored_deactivation(self, inspector_account):
        stale = inspector_account
        Account.objects.filter(pk=stale.pk).update(is_active=False)
        # The caller still believes the Account is active.
        assert stale.is_active is True
        decision = evaluate_capability(stale, Capability.VISIT_CREATE)
        assert decision.allowed is False
        assert decision.reason == "account_inactive"

    def test_stale_instance_cannot_claim_professional_work(self, inspector_account):
        Account.objects.filter(pk=inspector_account.pk).update(is_active=False)
        assert inspector_account.is_active is True
        assert can_perform_professional_work(inspector_account) is False

    def test_inactive_account_is_not_reported_as_platform_admin(self, admin_account):
        """Active state is part of administrative authority, not a separate flag.

        A deactivated admin must not read as an admin, or this helper would be a
        weaker gate than the mutation primitive it sits beside.
        """
        Account.objects.filter(pk=admin_account.pk).update(is_active=False)
        assert admin_account.is_active is True  # caller's stale belief
        assert is_platform_admin(admin_account) is False
        assert has_capability(admin_account, Capability.ACCOUNT_MANAGE) is False

    def test_borrowed_identity_cannot_claim_admin_status(self, admin_account):
        """A fabricated actor borrowing an admin's pk does not inherit the flag."""
        assert is_platform_admin(_borrowed_identity_of(admin_account)) is False

    def test_deactivation_also_denies_administrative_capability(self, admin_account):
        Account.objects.filter(pk=admin_account.pk).update(is_active=False)
        decision = evaluate_capability(admin_account, Capability.ACCOUNT_MANAGE)
        assert decision.allowed is False
        assert decision.reason == "account_inactive"


class TestCallerPersonRebindingCannotChangeOwnScope:
    """Requirement 5: stored Person binding decides OWN-scope identity."""

    def test_caller_side_person_id_mutation_cannot_extend_scope(
        self, inspector_account, other_person
    ):
        """Rebinding a stale instance at another Person must not widen scope.

        The instance keeps the inspector's pk, so it resolves to the inspector's
        stored row and its stored Person binding. The caller's in-memory
        ``person_id`` now names an unrelated Person; that must never let the OWN
        grant apply to that other Person.
        """
        stale = Account.objects.get(pk=inspector_account.pk)
        stale.person_id = other_person.pk

        decision = evaluate_capability(stale, Capability.VISIT_CREATE, subject_person=other_person)
        assert decision.allowed is False
        assert decision.reason == "scope_mismatch"

    def test_stored_binding_still_authorises_own_person(self, inspector_account):
        """The resolver's stored binding keeps the legitimate OWN grant intact."""
        reloaded = Account.objects.get(pk=inspector_account.pk)
        assert has_capability(reloaded, Capability.VISIT_CREATE) is True

    def test_in_memory_rebinding_does_not_widen_the_stored_binding(
        self, inspector_account, other_person
    ):
        """Mutating a loaded instance cannot change which Person OWN applies to."""
        stale = Account.objects.get(pk=inspector_account.pk)
        stale.person_id = other_person.pk

        decision = evaluate_capability(stale, Capability.VISIT_CREATE)
        assert decision.allowed is True
        # Authorised as the *stored* Person, never the caller-assigned one.
        assert decision.reason == "granted_own"
        stored, _ = resolve_persisted_account(stale)
        assert stored.person_id == inspector_account.person_id
        assert stored.person_id != other_person.pk


class TestGenuineAccountsStillWork:
    """Requirement 6: genuine persisted Accounts are unaffected."""

    def test_genuine_own_grant_still_authorises(self, inspector_account):
        assert has_capability(inspector_account, Capability.VISIT_CREATE) is True
        assert (
            evaluate_capability(inspector_account, Capability.VISIT_CREATE).reason == "granted_own"
        )

    def test_genuine_admin_administrative_capability_intact(self, admin_account):
        assert is_platform_admin(admin_account) is True
        assert has_capability(admin_account, Capability.ACCOUNT_MANAGE) is True

    def test_resolver_returns_the_stored_row(self, inspector_account):
        stored, denial = resolve_persisted_account(inspector_account)
        assert denial is None
        assert stored.pk == inspector_account.pk
        assert stored.person_id == inspector_account.person_id


class TestAdminStatusIsStillNotProfessionalAuthorship:
    """Requirement 7: an admin with no professional grant still fails."""

    def test_admin_without_grant_fails_professional_capability(self, admin_account):
        for capability in (
            Capability.VISIT_CREATE,
            Capability.VISIT_READ_OWN,
            Capability.VISIT_READ_ALL,
        ):
            decision = evaluate_capability(admin_account, capability)
            assert decision.allowed is False
            assert decision.reason == "no_active_grant"

    def test_admin_without_grant_has_no_professional_work(self, admin_account):
        assert can_perform_professional_work(admin_account) is False

    def test_admin_borrowing_a_granted_identity_is_still_denied(self, admin_account):
        """Admin status does not licence borrowing a professional identity."""
        fabricated = _borrowed_identity_of(admin_account)
        assert has_capability(fabricated, Capability.VISIT_CREATE) is False


class TestCanPerformProfessionalWork:
    """Requirements 8 and 9."""

    def test_false_for_fabricated_unsaved_and_inactive(self, inspector_account):
        assert can_perform_professional_work(_borrowed_identity_of(inspector_account)) is False
        unsaved = Account(username="unsaved-work", person=inspector_account.person)
        assert can_perform_professional_work(unsaved) is False

        class FabricatedAccount:
            pk = 1
            person_id = None
            is_active = True
            is_platform_admin = True
            capability_grants = None

        assert can_perform_professional_work(FabricatedAccount()) is False

        Account.objects.filter(pk=inspector_account.pk).update(is_active=False)
        assert can_perform_professional_work(inspector_account) is False

    def test_true_for_genuine_active_account_with_valid_grant(self, inspector_account):
        assert can_perform_professional_work(inspector_account) is True

    def test_administrative_grant_alone_is_not_professional_work(self, grant_issuer):
        account = make_account(username="admin-grant-only")
        grant_capability(
            actor=grant_issuer,
            account=account,
            capability_code=Capability.ACCOUNT_MANAGE,
            scope_kind=CapabilityGrant.ScopeKind.ALL,
        )
        assert can_perform_professional_work(account) is False

    def test_revoked_grant_is_not_professional_work(self, inspector_account):
        grant = inspector_account.capability_grants.get()
        grant.revoked_at = grant.created_at
        grant.save(update_fields=["revoked_at"])
        assert can_perform_professional_work(inspector_account) is False


class TestResolverContract:
    """The resolver is the single authority source; its reasons are stable."""

    def test_reasons_are_distinct_and_stable(self):
        assert REASON_INVALID_ACTOR == "invalid_actor"
        assert REASON_ACTOR_NOT_PERSISTED == "actor_not_persisted"
        assert REASON_ACTOR_NOT_FOUND == "actor_not_found"

    def test_none_is_an_invalid_actor(self):
        assert resolve_persisted_account(None) == (None, REASON_INVALID_ACTOR)

    def test_borrowed_pk_is_not_persisted(self, inspector_account):
        fabricated = _borrowed_identity_of(inspector_account)
        assert resolve_persisted_account(fabricated) == (None, REASON_ACTOR_NOT_PERSISTED)

    def test_unknown_pk_is_actor_not_found(self, grant_issuer):
        """A persisted-then-removed row is caught by the resolver's lookup."""
        temp = make_account(username="temp-row")
        Account.objects.filter(pk=temp.pk).delete()
        # ``temp`` still holds its pk and is not in the adding state, so the
        # row lookup is what rejects it.
        assert resolve_persisted_account(temp) == (None, REASON_ACTOR_NOT_FOUND)

    def test_model_delete_clears_pk_and_is_not_persisted(self, grant_issuer):
        """``Model.delete()`` blanks the pk, which the resolver also rejects."""
        temp = make_account(username="temp-row-2")
        temp.delete()
        assert resolve_persisted_account(temp) == (None, REASON_ACTOR_NOT_PERSISTED)


class TestSelectorsResolvePersistedIdentity:
    """Read helpers must not enumerate grants through a fabricated actor."""

    def test_grants_for_returns_stored_accounts_grants(self, inspector_account):
        from identity.selectors import grants_for

        grants = grants_for(inspector_account)
        assert [grant.pk for grant in grants] == [
            grant.pk for grant in inspector_account.capability_grants.all()
        ]

    def test_grants_for_returns_nothing_for_a_borrowed_identity(self, inspector_account):
        """A fabricated actor must not enumerate the real Account's grants."""
        from identity.selectors import grants_for

        fabricated = _borrowed_identity_of(inspector_account)
        assert list(grants_for(fabricated)) == []

    def test_grants_for_returns_nothing_for_an_account_shaped_object(self):
        from identity.selectors import grants_for

        class FabricatedAccount:
            pk = 1
            person_id = None
            is_active = True
            is_platform_admin = True

        assert list(grants_for(FabricatedAccount())) == []

    def test_accounts_visible_to_returns_nothing_for_a_borrowed_identity(self, admin_account):
        from identity.selectors import accounts_visible_to

        fabricated = _borrowed_identity_of(admin_account)
        assert list(accounts_visible_to(fabricated)) == []

    def test_accounts_visible_to_returns_nothing_for_an_inactive_actor(self, admin_account):
        from identity.selectors import accounts_visible_to

        Account.objects.filter(pk=admin_account.pk).update(is_active=False)
        assert list(accounts_visible_to(admin_account)) == []

    def test_accounts_visible_to_still_works_for_a_genuine_admin(self, admin_account):
        from identity.selectors import accounts_visible_to

        assert accounts_visible_to(admin_account).count() >= 1

    def test_no_test_person_is_used_as_real_data(self):
        """Guard: the synthetic dataset here contains no real identities."""
        assert Account.objects.filter(username__startswith="real-").count() == 0
