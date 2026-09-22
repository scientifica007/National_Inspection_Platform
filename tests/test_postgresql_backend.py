from __future__ import annotations

import pytest
from django.db import connection


@pytest.mark.django_db
@pytest.mark.postgres
def test_test_database_backend_is_postgresql():
    assert connection.vendor == "postgresql"
