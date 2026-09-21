"""B-02 regression: Account administration uses hashing-safe Django forms.

Plain ``ModelAdmin`` would have rendered the raw ``password`` column as an
editable text field and stored it unhashed. The corrected admin extends
Django's ``UserAdmin``.
"""

from __future__ import annotations

import pytest
from django.contrib.admin.sites import site
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import (
    AdminUserCreationForm,
    UserChangeForm,
    UserCreationForm,
)

from identity.admin import AccountAdmin
from identity.forms import AccountChangeForm, AccountCreationForm
from identity.models import Account, Person

pytestmark = pytest.mark.django_db


class TestAccountAdminIsUserAdminBased:
    def test_admin_class_extends_user_admin(self):
        assert issubclass(AccountAdmin, UserAdmin)

    def test_registered_admin_is_the_hashing_safe_class(self):
        assert isinstance(site._registry[Account], AccountAdmin)

    def test_uses_a_creation_form_and_a_change_form(self):
        assert issubclass(AccountAdmin.add_form, UserCreationForm)
        assert issubclass(AccountAdmin.form, UserChangeForm)

    def test_forms_target_the_custom_account_model(self):
        assert AccountCreationForm._meta.model is Account
        assert AccountChangeForm._meta.model is Account

    def test_add_form_is_the_admin_creation_form(self):
        """Keeps the ``usable_password`` affordance Django's admin add view expects."""
        assert issubclass(AccountCreationForm, AdminUserCreationForm)

    def test_admin_renders_the_password_field_as_a_hash_widget(self):
        """The change form must never expose an editable raw password value."""
        form = AccountChangeForm()
        password_field = form.fields["password"]
        # ``ReadOnlyPasswordHashField`` is Django's read-only hash display.
        assert password_field.__class__.__name__ == "ReadOnlyPasswordHashField"
        assert password_field.disabled is True

    def test_admin_registers_the_custom_fields(self):
        flat_fields = {
            name for _, options in AccountAdmin.fieldsets for name in (options.get("fields") or ())
        }
        assert "person" in flat_fields
        assert "is_platform_admin" in flat_fields


class TestAdminPasswordHashing:
    def test_admin_creation_form_hashes_the_password(self):
        """The password is hashed, and never stored as the submitted text."""
        person = Person.objects.create(display_name="شخص للحساب الإداري (بيانات اختبار)")
        form = AccountCreationForm(
            data={
                "username": "admin-created",
                "person": str(person.pk),
                "password1": "synthetic-admin-pass-01",
                "password2": "synthetic-admin-pass-01",
            }
        )
        assert form.is_valid(), form.errors
        account = form.save()
        assert account.password != "synthetic-admin-pass-01"
        assert account.password.startswith(("pbkdf2_", "argon2", "bcrypt", "scrypt"))
        assert account.check_password("synthetic-admin-pass-01") is True

    def test_admin_change_form_keeps_the_existing_hash(self, inspector_account):
        """Saving through the change form must not clobber the stored hash."""
        original_hash = inspector_account.password
        form = AccountChangeForm(
            data={
                "username": inspector_account.username,
                "person": str(inspector_account.person_id),
                "email": inspector_account.email,
                "is_active": True,
                "is_staff": False,
                "is_superuser": False,
                "date_joined": inspector_account.date_joined.strftime("%Y-%m-%d %H:%M:%S"),
                "password": original_hash,
            },
            instance=inspector_account,
        )
        assert form.is_valid(), form.errors
        saved = form.save()
        assert saved.password == original_hash
