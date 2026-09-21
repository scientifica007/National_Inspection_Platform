"""Django admin registration for technical administration.

The Django admin is a technical control-plane tool, not the product UI. It is
intentionally limited: it offers no way to act as, or author records on behalf
of, another Person (ADR-0003).
"""

from __future__ import annotations

from django.contrib import admin

from .models import Account, CapabilityGrant, Person


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ("display_name", "active", "created_at")
    list_filter = ("active",)
    search_fields = ("display_name",)
    readonly_fields = ("id", "created_at")


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ("username", "person", "is_platform_admin", "is_active", "is_staff")
    list_filter = ("is_platform_admin", "is_active", "is_staff")
    search_fields = ("username", "person__display_name")
    readonly_fields = ("last_login", "date_joined")
    autocomplete_fields = ("person",)


@admin.register(CapabilityGrant)
class CapabilityGrantAdmin(admin.ModelAdmin):
    list_display = (
        "capability_code",
        "scope_kind",
        "account",
        "valid_from",
        "valid_until",
        "revoked_at",
        "delegable",
    )
    list_filter = ("scope_kind", "capability_code", "delegable")
    search_fields = ("capability_code", "account__username")
    autocomplete_fields = ("account", "granted_by_account")
