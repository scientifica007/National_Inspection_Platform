"""HTTP orchestration for the identity module.

Views stay thin: parse the request, call a service/selector, map the result to
a response. No authority or lifecycle rule is implemented here; those live in
``identity.permissions`` and ``identity.services``.
"""

from __future__ import annotations

from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.decorators.http import require_http_methods

from .forms import RTLocalAuthenticationForm
from .permissions import can_perform_professional_work, is_platform_admin
from .selectors import accounts_visible_to, grants_for


class LoginView(auth_views.LoginView):
    """Authentication entry point."""

    template_name = "identity/login.html"
    authentication_form = RTLocalAuthenticationForm
    redirect_authenticated_user = True


class LogoutView(auth_views.LogoutView):
    """Logout. Django 5 refuses GET logout, so the UI posts a CSRF token."""

    next_page = reverse_lazy("identity:login")


@login_required
@require_http_methods(["GET"])
def dashboard(request: HttpRequest) -> HttpResponse:
    """Authenticated landing/dashboard shell.

    The shell reports the real identity only. It deliberately offers no way to
    switch, borrow or impersonate another Person.
    """
    account = request.user
    context = {
        "account": account,
        "person": account.person,
        "is_platform_admin": is_platform_admin(account),
        "has_professional_authority": can_perform_professional_work(account),
        "grants": grants_for(account),
    }
    return render(request, "identity/dashboard.html", context)


@login_required
@require_http_methods(["GET"])
def account_list(request: HttpRequest) -> HttpResponse:
    """Accounts visible to the acting Account.

    Administrative authority allows listing accounts. This page cannot be used
    to act on behalf of any listed Person.
    """
    context = {
        "accounts": accounts_visible_to(request.user),
        "is_platform_admin": is_platform_admin(request.user),
    }
    return render(request, "identity/account_list.html", context)
