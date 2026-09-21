"""Authentication and account-administration forms for the identity module."""

from __future__ import annotations

from django import forms
from django.contrib.auth.forms import (
    AdminUserCreationForm,
    AuthenticationForm,
    UserChangeForm,
)

from .models import Account


class RTLocalAuthenticationForm(AuthenticationForm):
    """Login form with Arabic-first labels and RTL-friendly widgets."""

    username = forms.CharField(
        label="اسم المستخدم",
        widget=forms.TextInput(
            attrs={"autocomplete": "username", "autofocus": True, "class": "field-input"}
        ),
    )
    password = forms.CharField(
        label="كلمة المرور",
        strip=False,
        widget=forms.PasswordInput(
            attrs={"autocomplete": "current-password", "class": "field-input"}
        ),
    )


class AccountCreationForm(AdminUserCreationForm):
    """Admin-side creation of an Account.

    Subclasses Django's admin creation form, which sets the password through
    ``set_password`` (hashing) rather than storing raw text, and which is what
    ``UserAdmin.add_form`` expects. ``person`` is declared here because it is
    required by the model: without it the admin add view would try to insert an
    Account with a null ``person`` and fail at the database.
    """

    class Meta(AdminUserCreationForm.Meta):
        model = Account
        fields = ("username", "person", "is_platform_admin")


class AccountChangeForm(UserChangeForm):
    """Admin-side editing of an Account.

    Django's change form renders the password as a read-only
    "change password" link, never as an editable raw text field.
    """

    class Meta(UserChangeForm.Meta):
        model = Account
        fields = "__all__"
