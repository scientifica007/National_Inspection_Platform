"""Environment-driven Django settings for the National Inspection Platform.

Stack (ADR-0002):
- Python 3.12
- Django 5.2 LTS
- PostgreSQL is the canonical database

Settings read explicit environment variables through small helpers instead of
a generic configuration framework, so deployment behaviour stays auditable.
"""

from __future__ import annotations

import os
from pathlib import Path

from django.core.exceptions import ImproperlyConfigured

BASE_DIR = Path(__file__).resolve().parent.parent


def _env(name: str, default: str = "") -> str:
    return os.environ.get(name, default)


def _env_bool(name: str, default: bool = False) -> bool:
    raw = os.environ.get(name)
    if raw is None:
        return default
    return raw.strip().lower() in {"1", "true", "yes", "on"}


def _env_list(name: str, default: str = "") -> list[str]:
    return [item.strip() for item in os.environ.get(name, default).split(",") if item.strip()]


DEBUG = _env_bool("DJANGO_DEBUG", default=False)

# --- Secret key -----------------------------------------------------------
# A missing secret key must never silently fall back to a fixed value outside
# explicit development: that would make every such deployment share one public
# signing key. Fail fast instead, with a message that says what to set.
_DEVELOPMENT_SECRET_KEY = "insecure-development-only-key-not-for-production"

_secret_key = _env("DJANGO_SECRET_KEY").strip()
if _secret_key:
    SECRET_KEY = _secret_key
elif DEBUG:
    SECRET_KEY = _DEVELOPMENT_SECRET_KEY
else:
    raise ImproperlyConfigured(
        "DJANGO_SECRET_KEY is required when DJANGO_DEBUG is not enabled. "
        "Set it in the environment (or a local .env) to a long random string."
    )

ALLOWED_HOSTS = _env_list("DJANGO_ALLOWED_HOSTS", default="localhost,127.0.0.1")

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Bounded application modules for the controlled Slice 01 increments.
    "identity",
    "institutions",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"

# --- Database -------------------------------------------------------------
# PostgreSQL is canonical. SQLite is deliberately not an option: designing for
# SQLite first would hide database-behaviour problems until later.
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": _env("POSTGRES_DB", default="national_inspection"),
        "USER": _env("POSTGRES_USER", default="national_inspection"),
        "PASSWORD": _env("POSTGRES_PASSWORD"),
        "HOST": _env("POSTGRES_HOST", default="127.0.0.1"),
        "PORT": _env("POSTGRES_PORT", default="5432"),
        "CONN_MAX_AGE": 60,
    }
}

# --- Authentication -------------------------------------------------------
AUTH_USER_MODEL = "identity.Account"

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
]

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LOGIN_URL = "identity:login"
LOGIN_REDIRECT_URL = "identity:dashboard"
LOGOUT_REDIRECT_URL = "identity:login"

# --- Internationalisation -------------------------------------------------
LANGUAGE_CODE = "ar"
LANGUAGES = [
    ("ar", "العربية"),
    ("fr", "Français"),
    ("en", "English"),
]
TIME_ZONE = _env("DJANGO_TIME_ZONE", default="UTC")
USE_I18N = True
USE_TZ = True

# --- Static files ---------------------------------------------------------
STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# --- Security -------------------------------------------------------------
# Secure defaults, adjustable per deployment. Framework protections (CSRF,
# output escaping, authentication middleware) are never switched off for
# convenience.
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = "Lax"
# Readable by the browser so the template can emit the CSRF form token.
CSRF_COOKIE_HTTPONLY = False
CSRF_COOKIE_SAMESITE = "Lax"
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_REFERRER_POLICY = "same-origin"
X_FRAME_OPTIONS = "DENY"

if not DEBUG:
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_SSL_REDIRECT = _env_bool("DJANGO_SECURE_SSL_REDIRECT", default=False)
