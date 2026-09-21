"""Shared fixtures for identity-module tests.

All data is synthetic (docs/SECURITY_AND_DATA_GOVERNANCE.md). No fixture
represents a real person, inspection record or credential.
"""

from __future__ import annotations

import pytest

from identity.models import CapabilityGrant
from identity.permissions import Capability
from identity.services import create_person, grant_capability
from identity.tests.factories import make_account


@pytest.fixture
def grant_issuer(db):
    """An administrative Account used only to issue grants in tests."""
    return make_account(
        username="grant-issuer",
        display_name="مانح الصلاحيات (بيانات اختبار)",
        is_platform_admin=True,
    )


@pytest.fixture
def admin_account(grant_issuer):
    """A Person who also holds administrative authority."""
    return grant_issuer


@pytest.fixture
def inspector_account(db, grant_issuer):
    """An inspector Person with an OWN-scoped professional capability."""
    account = make_account(
        username="inspector-01",
        display_name="مفتش ميداني (بيانات اختبار)",
    )
    grant_capability(
        actor=grant_issuer,
        account=account,
        capability_code=Capability.VISIT_CREATE,
        scope_kind=CapabilityGrant.ScopeKind.OWN,
    )
    return account


@pytest.fixture
def other_person(db):
    """A second, unrelated Person for scope-mismatch tests."""
    return create_person(display_name="شخص آخر (بيانات اختبار)")
