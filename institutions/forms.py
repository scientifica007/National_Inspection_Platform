from __future__ import annotations

from django import forms

from .models import Institution


class InstitutionForm(forms.ModelForm):
    class Meta:
        model = Institution
        fields = ("name",)
        labels = {"name": "اسم المؤسسة"}
        widgets = {"name": forms.TextInput(attrs={"class": "field-input", "autofocus": True})}
