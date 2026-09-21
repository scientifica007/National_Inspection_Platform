"""Identity module: Person, Account and CapabilityGrant.

Domain separation (docs/DOMAIN_MODEL.md, docs/MINIMAL_STABLE_CORE.md):

- ``Person`` is the real human being.
- ``Account`` is an access identity bound to a Person; it is NOT a professional
  position or an operational role.
- ``CapabilityGrant`` records what an Account may do, on which scope, and for
  how long.

Administrative authority is a separate dimension from professional authorship
(ADR-0003): ``Account.is_platform_admin`` never grants professional capability.
"""

from __future__ import annotations

import uuid

from django.contrib.auth.models import AbstractUser, UserManager
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class Person(models.Model):
    """The real human being represented in the platform.

    A Person survives account changes: disabling or replacing an Account must
    not delete the Person or the history attributed to them.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    display_name = models.CharField("الاسم المعروض", max_length=255)
    active = models.BooleanField("نشط", default=True)
    created_at = models.DateTimeField("تاريخ الإنشاء", auto_now_add=True)

    class Meta:
        verbose_name = "شخص"
        verbose_name_plural = "الأشخاص"
        ordering = ("display_name",)

    def __str__(self) -> str:
        return self.display_name


class AccountManager(UserManager):
    """Creates an Account together with the Person it represents.

    Identity stays explicit: an Account always resolves to exactly one Person.
    When no Person is supplied, one is created in the same operation as a
    convenience for administrative setup; the caller can never attach an
    unrelated existing Person implicitly.
    """

    use_in_migrations = True

    def _create_user(self, username, email, password, **extra_fields):
        person = extra_fields.pop("person", None)
        display_name = extra_fields.pop("display_name", None) or username
        if person is None:
            person = Person(display_name=display_name)
            person.full_clean()
            person.save()
        extra_fields["person"] = person
        return super()._create_user(username, email, password, **extra_fields)


class Account(AbstractUser):
    """Authentication identity bound one-to-one to a Person.

    ``is_platform_admin`` expresses administrative authority inside the
    application. It does not grant professional authorship, does not allow
    acting as another Person, and is never consulted by professional capability
    evaluation (see ``identity.permissions``).
    """

    person = models.OneToOneField(
        Person,
        on_delete=models.PROTECT,
        related_name="account",
        verbose_name="الشخص",
    )
    is_platform_admin = models.BooleanField(
        "مدير المنصة",
        default=False,
        help_text="سلطة إدارية داخل التطبيق؛ لا تمنح تأليفًا مهنيًا.",
    )

    objects = AccountManager()

    class Meta:
        verbose_name = "حساب"
        verbose_name_plural = "الحسابات"

    def __str__(self) -> str:
        return self.username


class CapabilityGrant(models.Model):
    """A time-bounded authorisation of a Capability on a Scope.

    Grants are data, not code (docs/AUTHORITY_MODEL.md). Scope is a semantic
    value: Slice 01 implements only ``OWN`` and ``ALL`` and deliberately does
    not build the future generic scope engine.
    """

    class ScopeKind(models.TextChoices):
        # Applies only where the acting subject is the Account's own Person.
        OWN = "OWN", "خاص (OWN)"
        # Applies platform-wide, regardless of the subject Person.
        ALL = "ALL", "عام (ALL)"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    account = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name="capability_grants",
        verbose_name="الحساب",
    )
    capability_code = models.CharField("رمز الصلاحية", max_length=100)
    scope_kind = models.CharField(
        "نطاق الصلاحية",
        max_length=8,
        choices=ScopeKind.choices,
        default=ScopeKind.OWN,
    )
    valid_from = models.DateTimeField("صالحة من", null=True, blank=True)
    valid_until = models.DateTimeField("صالحة إلى", null=True, blank=True)
    delegable = models.BooleanField("قابلة للتفويض", default=False)
    granted_by_account = models.ForeignKey(
        Account,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="grants_issued",
        verbose_name="مُنحت بواسطة",
    )
    revoked_at = models.DateTimeField("تاريخ الإلغاء", null=True, blank=True)
    created_at = models.DateTimeField("تاريخ الإنشاء", auto_now_add=True)

    class Meta:
        verbose_name = "منحة صلاحية"
        verbose_name_plural = "منح الصلاحيات"
        ordering = ("-created_at",)
        indexes = [
            models.Index(fields=("account", "capability_code"), name="grant_account_cap_idx"),
        ]
        constraints = [
            models.CheckConstraint(
                condition=(
                    models.Q(valid_from__isnull=True)
                    | models.Q(valid_until__isnull=True)
                    | models.Q(valid_until__gte=models.F("valid_from"))
                ),
                name="grant_validity_window_ordered",
            ),
        ]

    def __str__(self) -> str:
        return f"{self.capability_code} [{self.scope_kind}] -> {self.account_id}"

    def clean(self) -> None:
        super().clean()
        if self.valid_from and self.valid_until and self.valid_until < self.valid_from:
            raise ValidationError({"valid_until": "تاريخ الانتهاء يجب أن يكون بعد تاريخ البدء."})

    @property
    def is_revoked(self) -> bool:
        return self.revoked_at is not None

    def is_valid_at(self, at=None) -> bool:
        """Whether the grant authorises at ``at`` (defaults to now)."""
        at = at or timezone.now()
        if self.revoked_at is not None and self.revoked_at <= at:
            return False
        if self.valid_from is not None and self.valid_from > at:
            return False
        if self.valid_until is not None and self.valid_until < at:
            return False
        return True
