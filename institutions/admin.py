from django.contrib import admin

from .models import Institution


@admin.register(Institution)
class InstitutionAdmin(admin.ModelAdmin):
    list_display = ("name", "lifecycle", "local_owner_person", "created_at", "archived_at")
    list_filter = ("lifecycle",)
    search_fields = ("name", "local_owner_person__display_name")
    readonly_fields = ("created_at", "updated_at")
