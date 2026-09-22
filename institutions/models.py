from __future__ import annotations

import uuid

from django.core.exceptions import ValidationError
from django.db import models

from identity.models import Person


class Institution(models.Model):
    class Lifecycle(models.TextChoices):
        LOCAL_ACTIVE = "LOCAL_ACTIVE", "نشطة محليًا"
        ARCHIVED = "ARCHIVED", "مؤرشفة"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField("اسم المؤسسة", max_length=255)
    lifecycle = models.CharField(
        "الحالة",
        max_length=20,
        choices=Lifecycle.choices,
        default=Lifecycle.LOCAL_ACTIVE,
    )
    created_by_person = models.ForeignKey(
        Person,
        on_delete=models.PROTECT,
        related_name="institutions_created",
        verbose_name="أنشئت بواسطة",
    )
    local_owner_person = models.ForeignKey(
        Person,
        on_delete=models.PROTECT,
        related_name="local_institutions",
        verbose_name="المالك المحلي",
    )
    created_at = models.DateTimeField("تاريخ الإنشاء", auto_now_add=True)
    updated_at = models.DateTimeField("تاريخ التحديث", auto_now=True)
    archived_at = models.DateTimeField("تاريخ الأرشفة", null=True, blank=True)

    class Meta:
        verbose_name = "مؤسسة"
        verbose_name_plural = "المؤسسات"
        ordering = ("name",)
        constraints = [
            models.CheckConstraint(
                condition=(
                    models.Q(lifecycle="LOCAL_ACTIVE", archived_at__isnull=True)
                    | models.Q(lifecycle="ARCHIVED", archived_at__isnull=False)
                ),
                name="institution_lifecycle_archive_consistent",
            )
        ]

    def __str__(self) -> str:
        return self.name

    def clean(self) -> None:
        super().clean()
        self.name = self.name.strip()
        if not self.name:
            raise ValidationError({"name": "اسم المؤسسة مطلوب."})
        if self.lifecycle == self.Lifecycle.LOCAL_ACTIVE and self.archived_at is not None:
            raise ValidationError({"archived_at": "المؤسسة النشطة لا تحمل تاريخ أرشفة."})
        if self.lifecycle == self.Lifecycle.ARCHIVED and self.archived_at is None:
            raise ValidationError({"archived_at": "المؤسسة المؤرشفة تحتاج تاريخ أرشفة."})
