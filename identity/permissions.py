"""Server-side authority primitives for the identity module.

This module is the single place where Capability + Scope + Time are evaluated.
It is deliberately free of HTTP, templates and JavaScript so the authority
rules can be tested on their own (docs/TEST_STRATEGY.md).

Two independent authority dimensions are kept apart (ADR-0003):

1. Administrative authority — expressed by ``Account.is_platform_admin``.
2. Professional authority — expressed only by ``CapabilityGrant`` rows.

Admin status therefore never produces professional authorship, and there is no
helper anywhere that lets an Account act as another Person. Where professional
authorship is required, callers must pass the subject Person explicitly; the
recorded actor is always the real acting Account/Person.

Administrative mutation authority is deliberately narrow in S01-I01: only a
real Platform Admin (``is_platform_admin``) may run account-management
mutations. An ``account.manage`` grant does **not** satisfy them, because
explicit, bounded delegation is deferred to a later increment
(docs/AUTHORITY_MODEL.md §Delegation). Partially implementing it here would let
a non-admin escalate to arbitrary capabilities. The broader delegation model
remains intact for the increment that owns it.
"""

from __future__ import annotations

from dataclasses import dataclass

from django.utils import timezone

from .models import Account, CapabilityGrant, Person


class AuthorityError(Exception):
    """Base class for authority-related domain errors."""


class PermissionDeniedError(AuthorityError):
    """Raised when an Account lacks the capability/scope for an action."""


class Capability:
    """Stable capability identifiers for application use cases.

    Capability *identifiers* are code constants; the *grants* are data.
    """

    # institutions (S01-I02 and later)
    INSTITUTION_CREATE_LOCAL = "institution.create.local"
    INSTITUTION_READ_OWN = "institution.read.own"

    # knowledge (S01-I03 and later)
    KNOWLEDGE_CREATE_LOCAL = "knowledge.create.local"
    KNOWLEDGE_READ_OWN = "knowledge.read.own"

    # visits (S01-I04 and later)
    VISIT_CREATE = "visit.create"
    VISIT_READ_OWN = "visit.read.own"
    VISIT_UPDATE_OWN_DRAFT = "visit.update.own_draft"
    VISIT_FINALIZE_OWN = "visit.finalize.own"
    VISIT_READ_ALL = "visit.read.all"

    # administration
    ACCOUNT_MANAGE = "account.manage"


#: Capabilities that express application administration rather than
#: professional work. They are the only ones ``is_platform_admin`` satisfies.
ADMINISTRATIVE_CAPABILITIES: frozenset[str] = frozenset({Capability.ACCOUNT_MANAGE})

#: All capabilities known to the application. Professional capabilities must be
#: granted explicitly and are never implied by administrative status.
ALL_CAPABILITIES: frozenset[str] = frozenset(
    {
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
)


@dataclass(frozen=True)
class AuthorityDecision:
    """Explainable outcome of an authority evaluation.

    Returning the reason keeps denial messages honest and testable without
    leaking internal detail to end users.
    """

    allowed: bool
    capability_code: str
    reason: str

    def __bool__(self) -> bool:  # pragma: no cover - trivial
        return self.allowed


def _subject_for(account: Account, subject_person: Person | None) -> Person | None:
    """Resolve the Person an action would apply to.

    ``None`` means "the Account's own Person", which keeps ordinary call sites
    short without inventing an implicit identity switch.
    """
    return subject_person if subject_person is not None else account.person


def _active_grants(account: Account, capability_code: str, at) -> list[CapabilityGrant]:
    return [
        grant
        for grant in account.capability_grants.filter(capability_code=capability_code)
        if grant.is_valid_at(at)
    ]


def evaluate_capability(
    account: Account,
    capability_code: str,
    *,
    subject_person: Person | None = None,
    at=None,
) -> AuthorityDecision:
    """Evaluate Capability ∩ Scope ∩ Validity for ``account``.

    ``subject_person`` is the Person the action applies to. When omitted it is
    the Account's own Person. A subject Person supplied by a caller is always
    honoured as given: no code path silently substitutes another identity.
    """
    if capability_code not in ALL_CAPABILITIES:
        return AuthorityDecision(False, capability_code, "unknown_capability")

    if not account.is_active:
        return AuthorityDecision(False, capability_code, "account_inactive")

    now = at or timezone.now()
    subject = _subject_for(account, subject_person)

    # Administrative capability: satisfied by administrative authority only.
    #
    # A CapabilityGrant must NOT satisfy it in S01-I01. Accepting one here would
    # let a non-admin granted `account.manage` then grant itself or others
    # arbitrary capabilities, bypassing scope and delegable semantics. Explicit
    # delegation is deferred, so the rule is simply: real Platform Admin only.
    if capability_code in ADMINISTRATIVE_CAPABILITIES:
        if account.is_platform_admin:
            return AuthorityDecision(True, capability_code, "platform_admin")
        return AuthorityDecision(False, capability_code, "not_platform_admin")

    # Professional capability: never satisfied by administrative status.
    grants = _active_grants(account, capability_code, now)
    if not grants:
        return AuthorityDecision(False, capability_code, "no_active_grant")

    for grant in grants:
        if grant.scope_kind == CapabilityGrant.ScopeKind.ALL:
            return AuthorityDecision(True, capability_code, "granted_all")
        if grant.scope_kind == CapabilityGrant.ScopeKind.OWN and (
            subject is not None and subject.pk == account.person_id
        ):
            return AuthorityDecision(True, capability_code, "granted_own")

    return AuthorityDecision(False, capability_code, "scope_mismatch")


def has_capability(
    account: Account,
    capability_code: str,
    *,
    subject_person: Person | None = None,
    at=None,
) -> bool:
    """Boolean form of :func:`evaluate_capability`."""
    return evaluate_capability(
        account, capability_code, subject_person=subject_person, at=at
    ).allowed


def require_capability(
    account: Account,
    capability_code: str,
    *,
    subject_person: Person | None = None,
    at=None,
) -> None:
    """Raise :class:`PermissionDeniedError` unless the action is authorised."""
    decision = evaluate_capability(account, capability_code, subject_person=subject_person, at=at)
    if not decision.allowed:
        raise PermissionDeniedError(
            f"الصلاحية {capability_code!r} غير متوفرة (السبب: {decision.reason})."
        )


def is_platform_admin(account: Account) -> bool:
    """Whether the Account holds administrative authority."""
    return bool(account.is_platform_admin)


def require_administrative_authority(
    actor: Account, *, action: str = "administrative action"
) -> None:
    """Authorise an account-management *mutation*.

    This is the mutation-side primitive, deliberately separate from
    ``evaluate_capability(ACCOUNT_MANAGE)`` so the two meanings never blur:

    - ``evaluate_capability(..., ACCOUNT_MANAGE)`` answers "does this Account
      hold administrative authority?" — used for display/query decisions.
    - ``require_administrative_authority`` authorises an actual mutation and is
      satisfied only by a real Platform Admin in S01-I01.

    An ``account.manage`` CapabilityGrant does not satisfy this. Implementing
    partial delegation here would let a non-admin escalate; explicit, bounded
    delegation is deferred (docs/AUTHORITY_MODEL.md §Delegation).
    """
    if not getattr(actor, "is_platform_admin", False):
        raise PermissionDeniedError(f"هذا الفعل الإداري ({action}) متاح لمدير المنصة فقط.")
    if not actor.is_active:
        raise PermissionDeniedError(f"الحساب المعطّل لا يمكنه تنفيذ فعل إداري ({action}).")


def can_perform_professional_work(account: Account) -> bool:
    """Whether the Account holds at least one currently valid professional grant.

    Administrative status alone never makes this true.
    """
    now = timezone.now()
    for grant in account.capability_grants.all():
        if grant.capability_code in ADMINISTRATIVE_CAPABILITIES:
            continue
        if grant.is_valid_at(now):
            return True
    return False
