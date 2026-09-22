"""B-05 regression: automatic Person + Account creation is atomic.

The blocker was that the manager saved the automatic Person before the Account
row was written, so an Account failure left an orphaned Person behind.
"""

from __future__ import annotations

import pytest
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from identity.models import Account, Person

pytestmark = pytest.mark.django_db


def test_failed_account_creation_does_not_leave_an_orphan_person():
    """Regression: a duplicate username must not strand the automatic Person."""
    Account.objects.create_user(
        username="taken-username",
        password="synthetic-pass-01",
        display_name="الحساب الأول (بيانات اختبار)",
    )
    people_before = Person.objects.count()

    with pytest.raises(IntegrityError):
        Account.objects.create_user(
            username="taken-username",
            password="synthetic-pass-02",
            display_name="الحساب الفاشل (بيانات اختبار)",
        )

    assert Person.objects.count() == people_before
    assert not Person.objects.filter(display_name="الحساب الفاشل (بيانات اختبار)").exists()


def test_failed_creation_without_any_preexisting_person_leaves_no_rows():
    people_before = Person.objects.count()
    accounts_before = Account.objects.count()

    # An overlong username is rejected by AbstractUser.clean(), so the failure
    # happens after the automatic Person would have been written.
    with pytest.raises(ValidationError):
        Account.objects.create_user(username="x" * 300, password="synthetic-pass-01")

    assert Person.objects.count() == people_before
    assert Account.objects.count() == accounts_before


def test_successful_creation_still_persists_the_person():
    """The atomic block must not break the happy path."""
    account = Account.objects.create_user(
        username="atomic-ok",
        password="synthetic-pass-01",
        display_name="شخص ذرّي (بيانات اختبار)",
    )
    assert Person.objects.filter(pk=account.person_id).exists()
    assert account.person.display_name == "شخص ذرّي (بيانات اختبار)"


def test_preexisting_person_supplied_by_caller_is_not_deleted_on_failure():
    """Only the automatically-created Person is rolled back."""
    person = Person.objects.create(display_name="شخص موجود مسبقًا (بيانات اختبار)")
    Account.objects.create_user(
        username="caller-person", password="synthetic-pass-01", person=person
    )

    with pytest.raises(IntegrityError):
        Account.objects.create_user(
            username="caller-person", password="synthetic-pass-02", person=person
        )

    assert Person.objects.filter(pk=person.pk).exists()


def test_creation_uses_an_atomic_block():
    """The manager writes Person and Account under one transaction."""
    import inspect

    from identity.models import AccountManager

    source = inspect.getsource(AccountManager._create_user)
    assert "transaction.atomic()" in source
