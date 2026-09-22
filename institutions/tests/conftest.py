from __future__ import annotations

import pytest

from identity.models import CapabilityGrant
from identity.permissions import Capability
from identity.services import grant_capability
from identity.tests.factories import make_account


@pytest.fixture
def grant_issuer(db):
    return make_account(
        username="institution-grant-issuer",
        display_name="مانح صلاحيات المؤسسات (بيانات اختبار)",
        is_platform_admin=True,
    )


@pytest.fixture
def institution_owner(db, grant_issuer):
    account = make_account(
        username="institution-owner",
        display_name="مالك مؤسسة محلية (بيانات اختبار)",
    )
    grant_capability(
        actor=grant_issuer,
        account=account,
        capability_code=Capability.INSTITUTION_CREATE_LOCAL,
        scope_kind=CapabilityGrant.ScopeKind.OWN,
    )
    grant_capability(
        actor=grant_issuer,
        account=account,
        capability_code=Capability.INSTITUTION_READ_OWN,
        scope_kind=CapabilityGrant.ScopeKind.OWN,
    )
    return account


@pytest.fixture
def other_inspector(db, grant_issuer):
    account = make_account(
        username="other-institution-inspector",
        display_name="مفتش آخر (بيانات اختبار)",
    )
    grant_capability(
        actor=grant_issuer,
        account=account,
        capability_code=Capability.INSTITUTION_CREATE_LOCAL,
        scope_kind=CapabilityGrant.ScopeKind.OWN,
    )
    grant_capability(
        actor=grant_issuer,
        account=account,
        capability_code=Capability.INSTITUTION_READ_OWN,
        scope_kind=CapabilityGrant.ScopeKind.OWN,
    )
    return account


@pytest.fixture
def platform_admin(db):
    return make_account(
        username="institution-platform-admin",
        display_name="مدير منصة للمؤسسات (بيانات اختبار)",
        is_platform_admin=True,
    )
