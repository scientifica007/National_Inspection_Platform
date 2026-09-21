"""R3-B03 regression: operator bootstrap of the first Platform Admin.

The README previously pointed operators at ``createsuperuser``, which creates a
Django *technical* superuser and is a deliberately separate layer from the
application's Platform Admin. The management command tested here is the
operator-controlled bootstrap path. It stays in the technical/deployment
boundary: no HTTP route, no template, and no password in source.
"""

from __future__ import annotations

import pytest
from django.core.management import call_command
from django.core.management.base import CommandError

from identity.models import Account, Person

pytestmark = pytest.mark.django_db

PASSWORD_ENV = "NIP_TEST_BOOTSTRAP_PASSWORD"


class TestSuccessfulOperatorBootstrap:
    def test_command_creates_a_platform_admin(self, monkeypatch):
        monkeypatch.setenv(PASSWORD_ENV, "synthetic-operator-pass")
        call_command(
            "bootstrap_platform_admin",
            username="operator-admin",
            display_name="مدير تشغيل (بيانات اختبار)",
            password_env=PASSWORD_ENV,
        )
        account = Account.objects.get(username="operator-admin")
        assert account.is_platform_admin is True

    def test_command_does_not_create_a_django_superuser(self, monkeypatch):
        """The two layers stay distinct (the core of R3-B03)."""
        monkeypatch.setenv(PASSWORD_ENV, "synthetic-operator-pass")
        call_command(
            "bootstrap_platform_admin",
            username="not-a-superuser",
            password_env=PASSWORD_ENV,
        )
        account = Account.objects.get(username="not-a-superuser")
        assert account.is_superuser is False
        assert account.is_staff is False

    def test_command_links_a_person(self, monkeypatch):
        monkeypatch.setenv(PASSWORD_ENV, "synthetic-operator-pass")
        call_command(
            "bootstrap_platform_admin",
            username="operator-linked",
            display_name="مرتبط (بيانات اختبار)",
            password_env=PASSWORD_ENV,
        )
        account = Account.objects.get(username="operator-linked")
        assert account.person.account.pk == account.pk

    def test_command_grants_no_professional_capability(self, monkeypatch):
        monkeypatch.setenv(PASSWORD_ENV, "synthetic-operator-pass")
        call_command(
            "bootstrap_platform_admin",
            username="operator-no-grant",
            password_env=PASSWORD_ENV,
        )
        account = Account.objects.get(username="operator-no-grant")
        assert account.capability_grants.count() == 0

    def test_command_reports_success(self, monkeypatch, capsys):
        monkeypatch.setenv(PASSWORD_ENV, "synthetic-operator-pass")
        call_command(
            "bootstrap_platform_admin",
            username="operator-reported",
            password_env=PASSWORD_ENV,
        )
        assert "operator-reported" in capsys.readouterr().out


class TestOperatorBootstrapGuards:
    def test_missing_password_env_is_refused(self, monkeypatch):
        monkeypatch.delenv(PASSWORD_ENV, raising=False)
        with pytest.raises(CommandError):
            call_command(
                "bootstrap_platform_admin",
                username="no-password-admin",
                password_env=PASSWORD_ENV,
            )
        assert not Account.objects.filter(username="no-password-admin").exists()

    def test_collision_with_an_existing_account_is_refused(self, monkeypatch):
        monkeypatch.setenv(PASSWORD_ENV, "synthetic-operator-pass")
        call_command(
            "bootstrap_platform_admin",
            username="already-here",
            password_env=PASSWORD_ENV,
        )
        with pytest.raises(CommandError):
            call_command(
                "bootstrap_platform_admin",
                username="already-here",
                password_env=PASSWORD_ENV,
            )
        assert Account.objects.filter(username="already-here").count() == 1

    def test_refused_collision_leaves_no_orphan_person(self, monkeypatch):
        monkeypatch.setenv(PASSWORD_ENV, "synthetic-operator-pass")
        call_command(
            "bootstrap_platform_admin",
            username="collision-orphan",
            password_env=PASSWORD_ENV,
        )
        with pytest.raises(CommandError):
            call_command(
                "bootstrap_platform_admin",
                username="collision-orphan",
                password_env=PASSWORD_ENV,
            )
        assert not Person.objects.filter(account__isnull=True).exists()

    def test_password_is_not_accepted_as_a_command_line_option(self):
        """A password argument would leak into shell history and `ps`."""
        from django.core.management import get_commands, load_command_class

        assert get_commands()["bootstrap_platform_admin"] == "identity"
        command = load_command_class("identity", "bootstrap_platform_admin")
        parser = command.create_parser("manage.py", "bootstrap_platform_admin")
        option_strings = {option for action in parser._actions for option in action.option_strings}
        assert "--password" not in option_strings
        assert "--password-env" in option_strings


class TestBootstrapStaysTechnical:
    def test_no_http_route_reaches_the_bootstrap(self):
        from django.urls import get_resolver

        patterns = [str(pattern.pattern) for pattern in get_resolver().url_patterns]
        joined = " ".join(patterns)
        assert "bootstrap" not in joined

    def test_services_does_not_import_the_bootstrap_module(self):
        """The application service must never depend on the bootstrap bypass."""
        import ast
        import inspect

        from identity import services

        imported = {
            node.module
            for node in ast.walk(ast.parse(inspect.getsource(services)))
            if isinstance(node, ast.ImportFrom)
        }
        assert not any(module and "bootstrap" in module for module in imported)

    def test_bootstrap_module_does_not_import_services(self):
        import ast
        import inspect

        from identity import bootstrap

        imported = {
            node.module
            for node in ast.walk(ast.parse(inspect.getsource(bootstrap)))
            if isinstance(node, ast.ImportFrom)
        }
        assert not any(module and "services" in module for module in imported)
