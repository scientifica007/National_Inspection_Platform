"""Django admin registration for technical administration.

The Django admin is a technical control-plane tool, not the product UI. It is
intentionally limited: it offers no way to act as, or author records on behalf
of, another Person (ADR-0003).

``AccountAdmin`` extends Django's ``UserAdmin`` so password creation and
change keep using hashing-aware forms. A plain ``ModelAdmin`` would allow a raw
password text field and store it unhashed, which is unsafe for a user model.
"""

from __future__ import annotations

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import AccountChangeForm, AccountCreationForm
from .models import Account, CapabilityGrant, Person


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ("display_name", "active", "created_at")
    list_filter = ("active",)
    search_fields = ("display_name",)
    readonly_fields = ("id", "created_at")


@admin.register(Account)
class AccountAdmin(UserAdmin):
    """Account administration with Django's hashing-safe user forms."""

    form = AccountChangeForm
    add_form = AccountCreationForm

    list_display = ("username", "person", "is_platform_admin", "is_active", "is_staff")
    list_filter = ("is_platform_admin", "is_active", "is_staff")
    search_fields = ("username", "person__display_name")
    autocomplete_fields = ("person",)
    ordering = ("username",)

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("الشخص", {"fields": ("person",)}),
        (
            "السلطة الإدارية",
            {
                "fields": ("is_platform_admin",),
                "description": (
                    "سلطة إدارية داخل التطبيق. لا تمنح تأليفًا مهنيًا ولا تسمح بالتصرف باسم شخص آخر."
                ),
            },
        ),
        (
            "المعلومات الشخصية",
            {"fields": ("first_name", "last_name", "email")},
        ),
        (
            "الصلاحيات التقنية",
            {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")},
        ),
        ("تواريخ مهمة", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "usable_password", "password1", "password2"),
            },
        ),
        ("الشخص", {"fields": ("person",)}),
        ("السلطة الإدارية", {"fields": ("is_platform_admin",)}),
    )

    readonly_fields = ("last_login", "date_joined")


@admin.register(CapabilityGrant)
class CapabilityGrantAdmin(admin.ModelAdmin):
    list_display = (
        "capability_code",
        "scope_kind",
        "account",
        "granted_by_account",
        "valid_from",
        "valid_until",
        "revoked_at",
        "delegable",
    )
    list_filter = ("scope_kind", "capability_code", "delegable")
    search_fields = ("capability_code", "account__username")
    autocomplete_fields = ("account", "granted_by_account")
    # Provenance is immutable: an existing grant's issuer must not be rewritten.
    readonly_fields = ("granted_by_account",)
