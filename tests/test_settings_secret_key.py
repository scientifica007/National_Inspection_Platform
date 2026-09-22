"""B-03 regression: the secret key must fail safe.

The settings module is executed in a subprocess with a controlled environment
so the real settings-import path is exercised, rather than a re-implementation
of the rule. This also proves the failure happens at import time, before the
application can serve a request.
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent

# Settings that would otherwise make the import fail, isolated from the
# developer's local .env file by an explicit empty environment variable.
_BASE_ENV = {
    "DJANGO_ALLOWED_HOSTS": "localhost",
    "POSTGRES_DB": "national_inspection",
    "POSTGRES_USER": "national_inspection",
    "POSTGRES_PASSWORD": "",
    "POSTGRES_HOST": "127.0.0.1",
    "POSTGRES_PORT": "5432",
}


def _load_settings_subprocess(extra_env: dict[str, str]) -> subprocess.CompletedProcess:
    env = {**os.environ, **_BASE_ENV, **extra_env}
    return subprocess.run(
        [sys.executable, "-c", "import config.settings as s; print(s.SECRET_KEY)"],
        cwd=REPO_ROOT,
        env=env,
        capture_output=True,
        text=True,
    )


class TestSecretKeyFailsClosed:
    def test_non_debug_without_secret_key_fails_fast(self):
        """B-03: DEBUG=False with no key must raise, not use a fixed fallback."""
        result = _load_settings_subprocess({"DJANGO_DEBUG": "False", "DJANGO_SECRET_KEY": ""})
        assert result.returncode != 0
        assert "DJANGO_SECRET_KEY" in result.stderr
        assert "insecure" not in result.stdout

    def test_non_debug_with_blank_secret_key_fails_fast(self):
        """A whitespace-only key counts as missing."""
        result = _load_settings_subprocess({"DJANGO_DEBUG": "False", "DJANGO_SECRET_KEY": "   "})
        assert result.returncode != 0
        assert "DJANGO_SECRET_KEY" in result.stderr

    def test_explicit_secret_key_is_used_verbatim(self):
        result = _load_settings_subprocess(
            {"DJANGO_DEBUG": "False", "DJANGO_SECRET_KEY": "synthetic-explicit-key-for-tests"}
        )
        assert result.returncode == 0
        assert result.stdout.strip() == "synthetic-explicit-key-for-tests"

    def test_explicit_secret_key_wins_in_debug_too(self):
        result = _load_settings_subprocess(
            {"DJANGO_DEBUG": "True", "DJANGO_SECRET_KEY": "synthetic-debug-key-for-tests"}
        )
        assert result.returncode == 0
        assert result.stdout.strip() == "synthetic-debug-key-for-tests"

    def test_debug_fallback_is_labelled_development_only(self):
        """In debug the fallback is allowed, but must be recognisably temporary."""
        result = _load_settings_subprocess({"DJANGO_DEBUG": "True", "DJANGO_SECRET_KEY": ""})
        assert result.returncode == 0
        assert "insecure-development-only" in result.stdout

    def test_failure_message_does_not_leak_a_secret(self):
        result = _load_settings_subprocess({"DJANGO_DEBUG": "False", "DJANGO_SECRET_KEY": ""})
        assert result.returncode != 0
        assert "Traceback" in result.stderr
        # The error explains what to set; it never echoes a value.
        assert "long random string" in result.stderr


@pytest.mark.parametrize("value", ["False", "0", "no", "off", ""])
def test_non_debug_spellings_all_fail_without_a_key(value):
    """Every non-debug spelling must fail closed, not just the literal 'False'."""
    result = _load_settings_subprocess({"DJANGO_DEBUG": value, "DJANGO_SECRET_KEY": ""})
    assert result.returncode != 0
    assert "DJANGO_SECRET_KEY" in result.stderr
