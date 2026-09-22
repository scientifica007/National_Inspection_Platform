"""R3-B01 regression: first Platform Admin bootstrap is atomic.

``bootstrap_platform_admin`` previously saved the Person and *then* created the
Account, so an Account failure (a duplicate username, for example) left an
orphan Person behind. It now reuses ``AccountManager``'s automatic Person path,
which writes both rows in one atomic block (the R2-B05 mechanism), so a failed
bootstrap leaves nothing behind.
"""

from __future__ import annotations

import pytest
from django.db import IntegrityError, transaction

from identity.bootstrap import bootstrap_platform_admin
from identity.models import Account, Person

pytestmark = pytest.mark.django_db


class TestSuccessfulBootstrap:
    def test_creates_exactly_one_account_and_one_person(self):
        accounts_before = Account.objects.count()
        persons_before = Person.objects.count()

        account = bootstrap_platform_admin(
            username="atomic-admin",
            password="synthetic-atomic-pass",
            display_name="مدير ذري (بيانات اختبار)",
        )

        assert Account.objects.count() == accounts_before + 1
        assert Person.objects.count() == persons_before + 1
        assert account.person_id is not None

    def test_the_person_is_linked_to_the_account(self):
        account = bootstrap_platform_admin(
            username="linked-admin",
            password="synthetic-linked-pass",
            display_name="مدير مرتبط (بيانات اختبار)",
        )
        assert account.person.account.pk == account.pk
        assert account.person.display_name == "مدير مرتبط (بيانات اختبار)"

    def test_the_account_is_a_platform_admin(self):
        account = bootstrap_platform_admin(
            username="admin-flag", password="synthetic-admin-flag-pass"
        )
        assert account.is_platform_admin is True
        assert account.is_active is True

    def test_display_name_defaults_to_the_username(self):
        account = bootstrap_platform_admin(
            username="default-name-admin", password="synthetic-default-name-pass"
        )
        assert account.person.display_name == "default-name-admin"

    def test_no_professional_capability_is_created(self):
        account = bootstrap_platform_admin(
            username="no-grant-admin", password="synthetic-no-grant-pass"
        )
        assert account.capability_grants.count() == 0

    def test_password_is_hashed_and_usable(self):
        account = bootstrap_platform_admin(
            username="hashed-admin", password="synthetic-hashed-pass"
        )
        assert account.password != "synthetic-hashed-pass"
        assert account.check_password("synthetic-hashed-pass") is True


class TestFailedBootstrapLeavesNoOrphan:
    def test_duplicate_username_leaves_person_count_unchanged(self):
        bootstrap_platform_admin(username="duplicate-admin", password="synthetic-first-pass")
        persons_after_first = Person.objects.count()

        with pytest.raises(IntegrityError):
            bootstrap_platform_admin(username="duplicate-admin", password="synthetic-second-pass")

        assert Person.objects.count() == persons_after_first

    def test_duplicate_username_leaves_account_count_unchanged(self):
        bootstrap_platform_admin(username="duplicate-admin-2", password="synthetic-first-pass")
        accounts_after_first = Account.objects.count()

        with pytest.raises(IntegrityError):
            bootstrap_platform_admin(username="duplicate-admin-2", password="synthetic-second-pass")

        assert Account.objects.count() == accounts_after_first

    def test_no_orphan_person_exists_after_a_refused_bootstrap(self):
        """The orphan is the specific regression R3-B01 raised."""
        bootstrap_platform_admin(username="orphan-check-admin", password="synthetic-first-pass")
        with pytest.raises(IntegrityError):
            bootstrap_platform_admin(
                username="orphan-check-admin", password="synthetic-second-pass"
            )
        # Every Person must still be reachable from an Account.
        unreachable = Person.objects.filter(account__isnull=True)
        assert not unreachable.exists()

    def test_failure_inside_an_outer_atomic_block_still_rolls_back(self):
        """A caller wrapping the bootstrap in its own transaction is safe too."""
        persons_before = Person.objects.count()

        class Marker(Exception):
            pass

        with pytest.raises(Marker):
            with transaction.atomic():
                bootstrap_platform_admin(
                    username="outer-rollback-admin",
                    password="synthetic-outer-rollback-pass",
                )
                raise Marker

        assert Person.objects.count() == persons_before
        assert not Account.objects.filter(username="outer-rollback-admin").exists()


class TestBootstrapReusesTheManagerPath:
    def test_bootstrap_does_not_construct_a_person_directly(self):
        """It must delegate Person creation to AccountManager, not duplicate it."""
        import ast
        import inspect

        from identity import bootstrap

        tree = ast.parse(inspect.getsource(bootstrap))
        calls = [
            node.func.attr if isinstance(node.func, ast.Attribute) else getattr(node.func, "id", "")
            for node in ast.walk(tree)
            if isinstance(node, ast.Call)
        ]
        assert "save" not in calls
        assert "Person" not in calls

    def test_bootstrap_is_atomic(self):
        import inspect

        from identity import bootstrap

        source = inspect.getsource(bootstrap)
        assert "transaction.atomic" in source
