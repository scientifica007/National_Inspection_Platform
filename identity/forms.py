"""Authentication forms for the identity module."""

from __future__ import annotations

from django import forms
from django.contrib.auth.forms import AuthenticationForm


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
