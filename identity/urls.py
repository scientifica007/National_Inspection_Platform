"""URL routes for the identity module."""

from django.urls import path

from . import views

app_name = "identity"

urlpatterns = [
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("", views.dashboard, name="dashboard"),
    path("accounts/", views.account_list, name="account-list"),
]
