"""Authentication and access-control tests.

Covers required evidence items 3, 4 and 11-13.
"""

from __future__ import annotations

import pytest
from django.test import Client
from django.urls import reverse

from identity.models import Account, Person
from identity.services import create_account

pytestmark = pytest.mark.django_db


@pytest.fixture
def password():
    return "synthetic-login-pass-01"


@pytest.fixture
def active_account(password):
    return create_account(
        username="login-user",
        password=password,
        display_name="مستخدم الدخول (بيانات اختبار)",
    )


class TestAuthentication:
    """Requirement 3: authentication works."""

    def test_login_page_is_reachable(self, client):
        response = client.get(reverse("identity:login"))
        assert response.status_code == 200
        assert "text/html" in response["Content-Type"]

    def test_login_with_valid_credentials_succeeds(self, client, active_account, password):
        response = client.post(
            reverse("identity:login"),
            {"username": active_account.username, "password": password},
        )
        assert response.status_code == 302
        assert response.url == reverse("identity:dashboard")

    def test_session_is_authenticated_after_login(self, client, active_account, password):
        client.post(
            reverse("identity:login"),
            {"username": active_account.username, "password": password},
        )
        response = client.get(reverse("identity:dashboard"))
        assert response.status_code == 200
        assert response.context["account"].pk == active_account.pk

    def test_login_with_invalid_password_fails(self, client, active_account):
        response = client.post(
            reverse("identity:login"),
            {"username": active_account.username, "password": "wrong-password"},
        )
        assert response.status_code == 200
        assert response.context["form"].errors

    def test_inactive_account_cannot_authenticate(self, client, active_account, password):
        active_account.is_active = False
        active_account.save(update_fields=["is_active"])
        response = client.post(
            reverse("identity:login"),
            {"username": active_account.username, "password": password},
        )
        assert response.status_code == 200
        assert response.context["form"].errors

    def test_logout_requires_post_and_ends_session(self, client, active_account, password):
        client.post(
            reverse("identity:login"),
            {"username": active_account.username, "password": password},
        )
        response = client.post(reverse("identity:logout"))
        assert response.status_code == 302
        assert client.get(reverse("identity:dashboard")).status_code == 302

    def test_logout_via_get_is_not_allowed(self, client, active_account, password):
        """Mutations use POST; a GET logout must not succeed."""
        client.post(
            reverse("identity:login"),
            {"username": active_account.username, "password": password},
        )
        response = client.get(reverse("identity:logout"))
        assert response.status_code == 405


class TestProtectedAccess:
    """Requirement 4: unauthenticated protected access is rejected/redirected."""

    def test_dashboard_redirects_anonymous_user_to_login(self, client):
        response = client.get(reverse("identity:dashboard"))
        assert response.status_code == 302
        assert reverse("identity:login") in response.url

    def test_account_list_redirects_anonymous_user_to_login(self, client):
        response = client.get(reverse("identity:account-list"))
        assert response.status_code == 302
        assert reverse("identity:login") in response.url

    def test_login_redirect_preserves_next_target(self, client):
        response = client.get(reverse("identity:dashboard"))
        assert "next=" in response.url


class TestCsrfProtection:
    def test_login_post_without_csrf_token_is_rejected(self):
        """Requirement: CSRF protection remains enabled."""
        csrf_client = Client(enforce_csrf_checks=True)
        person = Person.objects.create(display_name="محاولة CSRF")
        Account.objects.create_user(
            username="csrf-target", password="synthetic-pass-01", person=person
        )
        response = csrf_client.post(
            reverse("identity:login"),
            {"username": "csrf-target", "password": "synthetic-pass-01"},
        )
        assert response.status_code == 403

    def test_dashboard_page_contains_csrf_token_for_logout_form(
        self, client, active_account, password
    ):
        client.post(
            reverse("identity:login"),
            {"username": active_account.username, "password": password},
        )
        response = client.get(reverse("identity:dashboard"))
        assert b"csrfmiddlewaretoken" in response.content


class TestRtlShell:
    """The presentation shell is Arabic-first RTL and carries design tokens."""

    def test_base_template_declares_rtl_direction(self, client, active_account, password):
        client.post(
            reverse("identity:login"),
            {"username": active_account.username, "password": password},
        )
        response = client.get(reverse("identity:dashboard"))
        content = response.content.decode()
        assert 'dir="rtl"' in content
        assert 'lang="ar"' in content

    def test_design_tokens_stylesheet_is_linked(self, client, active_account, password):
        client.post(
            reverse("identity:login"),
            {"username": active_account.username, "password": password},
        )
        response = client.get(reverse("identity:dashboard"))
        assert b"design-tokens.css" in response.content

    def test_login_page_is_rtl_too(self, client):
        response = client.get(reverse("identity:login"))
        assert 'dir="rtl"' in response.content.decode()


class TestAdminVisibility:
    """Admin sees accounts; it still cannot act as another Person."""

    def test_admin_can_list_accounts(self, client, admin_account):
        client.force_login(admin_account)
        response = client.get(reverse("identity:account-list"))
        assert response.status_code == 200

    def test_non_admin_only_sees_own_account(self, client, inspector_account):
        client.force_login(inspector_account)
        response = client.get(reverse("identity:account-list"))
        assert response.status_code == 200
        accounts = list(response.context["accounts"])
        assert [account.pk for account in accounts] == [inspector_account.pk]

    def test_no_account_switching_route_exists(self):
        """Requirement 9: no impersonation route is exposed over HTTP."""
        from django.urls import get_resolver

        resolver = get_resolver()
        route_names = {name for name in resolver.reverse_dict if isinstance(name, str)}
        forbidden_fragments = ("impersonate", "act-as", "act_as", "switch", "become")
        assert not any(fragment in name for name in route_names for fragment in forbidden_fragments)
