"""System-level and scope-boundary tests.

Covers required evidence items 11, 12 and 13.
"""

from __future__ import annotations

import pytest
from django.apps import apps
from django.conf import settings
from django.core.management import call_command

#: Modules explicitly deferred beyond S01-I01. None may be installed yet.
DEFERRED_APPS = {
    "institutions",
    "knowledge",
    "visits",
    "records",
    "audit",
    "missions",
    "teams",
    "reporting",
    "organization",
    "geography",
}


def test_django_system_checks_pass():
    """Requirement 11: Django system checks pass."""
    call_command("check", verbosity=0)


@pytest.mark.django_db
def test_migrations_are_consistent():
    """Requirement 12: migrations are internally consistent."""
    call_command("makemigrations", "--check", "--dry-run", verbosity=0)


def test_no_deferred_business_module_is_installed():
    """Requirement 13: no future business module was implemented."""
    installed = set(settings.INSTALLED_APPS)
    app_labels = {config.label for config in apps.get_app_configs()}
    assert installed & DEFERRED_APPS == set()
    assert app_labels & DEFERRED_APPS == set()


def test_only_identity_application_module_exists():
    """Only the identity bounded module is added in this increment."""
    project_apps = [
        config.label for config in apps.get_app_configs() if not config.name.startswith("django.")
    ]
    assert project_apps == ["identity"]


def test_postgresql_is_the_configured_canonical_database():
    """PostgreSQL is canonical; the project is not designed SQLite-only."""
    assert settings.DATABASES["default"]["ENGINE"] == "django.db.backends.postgresql"


@pytest.mark.django_db
def test_identity_tables_exist_in_the_database():
    """The identity migration actually created its tables."""
    from django.db import connection

    table_names = set(connection.introspection.table_names())
    assert "identity_person" in table_names
    assert "identity_account" in table_names
    assert "identity_capabilitygrant" in table_names


@pytest.mark.django_db
def test_test_database_is_postgresql():
    """The suite runs against PostgreSQL, not SQLite.

    This is the evidence that database-behaviour tests exercise the canonical
    backend rather than a convenience substitute.
    """
    from django.db import connection

    assert connection.vendor == "postgresql"
