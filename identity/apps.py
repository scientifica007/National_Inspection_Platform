"""Application configuration for the identity module.

The identity module owns Person, Account and CapabilityGrant. It must not
depend on business modules (documents/MODULE_DEPENDENCY_MAP.md).
"""

from django.apps import AppConfig


class IdentityConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "identity"
    verbose_name = "الهوية والصلاحيات"
