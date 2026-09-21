"""Operator-controlled bootstrap of the very first Platform Admin.

This lives in the technical/deployment boundary (docs/AUTHORITY_MODEL.md), not
in the product surface. There is no HTTP route and no template that reaches it;
it must be invoked deliberately by an operator on the server.

Using ``createsuperuser`` instead would be wrong for this purpose: that creates
a *Django* technical superuser, which is a separate layer from the application's
Platform Admin (``Account.is_platform_admin``). Neither implies the other.
"""

from __future__ import annotations

import os

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from identity.bootstrap import bootstrap_platform_admin
from identity.models import Account


class Command(BaseCommand):
    help = (
        "Create the first application Platform Admin (technical bootstrap). "
        "This is not a Django superuser; see docs/AUTHORITY_MODEL.md."
    )

    def add_arguments(self, parser):
        parser.add_argument("--username", required=True, help="Account username.")
        parser.add_argument(
            "--display-name",
            default=None,
            help="Person display name. Defaults to the username.",
        )
        parser.add_argument("--email", default="", help="Optional email address.")
        parser.add_argument(
            "--password-env",
            default="NIP_BOOTSTRAP_PASSWORD",
            help=(
                "Name of the environment variable holding the password. "
                "Passing the password on the command line would leak it into "
                "shell history and the process list."
            ),
        )

    def handle(self, *args, **options):
        username = options["username"]
        if Account.objects.filter(username=username).exists():
            raise CommandError(f"An account named {username!r} already exists.")

        password_env = options["password_env"]
        password = os.environ.get(password_env)
        if not password:
            raise CommandError(
                f"Environment variable {password_env!r} is not set. "
                "Set it to a strong password for the bootstrap run, then unset it. "
                "The password is never stored in the repository."
            )

        try:
            with transaction.atomic():
                account = bootstrap_platform_admin(
                    username=username,
                    password=password,
                    display_name=options["display_name"],
                    email=options["email"],
                )
        except Exception as exc:  # noqa: BLE001 - reported as a command error
            raise CommandError(f"Bootstrap failed: {exc}") from exc

        self.stdout.write(
            self.style.SUCCESS(
                f"Created Platform Admin {account.username!r} "
                f"(person {account.person_id}). No professional capability was granted."
            )
        )
