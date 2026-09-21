"""R2-B02 regression: the Account→Person binding is frozen after creation.

The Person may be chosen when the Account is created, but an existing Account
must not be routinely rebound to another Person. Rebinding would let
administrative access silently redirect professional identity, which violates
"Identity Cannot Be Borrowed" (docs/INVARIANTS.md §2).
"""

from __future__ import annotations

import pytest
from django.core.exceptions import ValidationError

from identity.forms import AccountChangeForm, AccountCreationForm
from identity.models import Account
from identity.tests.factories import make_account, make_person

pytestmark = pytest.mark.django_db


class TestPersonRemainsSelectableAtCreation:
    def test_add_form_exposes_the_person_field(self):
        assert "person" in AccountCreationForm().fields

    def test_add_form_person_field_is_editable(self):
        assert AccountCreationForm().fields["person"].disabled is False

    def test_creation_can_bind_an_explicit_person(self):
        person = make_person(display_name="شخص عند الإنشاء (بيانات اختبار)")
        form = AccountCreationForm(
            data={
                "username": "created-with-person",
                "person": str(person.pk),
                "password1": "synthetic-create-pass-01",
                "password2": "synthetic-create-pass-01",
            }
        )
        assert form.is_valid(), form.errors
        assert form.save().person_id == person.pk


class TestModelRefusesRebinding:
    def test_reassigning_person_on_save_is_rejected(self):
        account = make_account(username="rebind-target")
        other = make_person(display_name="شخص آخر (بيانات اختبار)")
        account.person = other
        with pytest.raises(ValidationError) as excinfo:
            account.save()
        assert "person" in excinfo.value.message_dict

    def test_rejected_rebind_leaves_the_stored_binding_intact(self):
        account = make_account(username="rebind-target-2")
        original_person_id = account.person_id
        other = make_person(display_name="شخص آخر ٢ (بيانات اختبار)")
        account.person = other
        with pytest.raises(ValidationError):
            account.save()
        assert Account.objects.get(pk=account.pk).person_id == original_person_id

    def test_rebinding_via_direct_person_id_assignment_is_rejected(self):
        """The check reads the stored value, so it cannot be bypassed by a raw id."""
        account = make_account(username="rebind-target-3")
        other = make_person(display_name="شخص آخر ٣ (بيانات اختبار)")
        account.person_id = other.pk
        with pytest.raises(ValidationError):
            account.save()

    def test_update_query_bypass_is_not_the_supported_path(self):
        """``QuerySet.update`` is raw SQL and numbered as a known residual path.

        This test documents the boundary rather than pretending the guard covers
        it: the supported paths are ``save()`` and the admin/application forms.
        """
        account = make_account(username="rebind-target-4")
        other = make_person(display_name="شخص آخر ٤ (بيانات اختبار)")
        Account.objects.filter(pk=account.pk).update(person=other)
        assert Account.objects.get(pk=account.pk).person_id == other.pk

    def test_saving_without_changing_person_still_works(self):
        account = make_account(username="unchanged-person")
        account.email = "synthetic@example.invalid"
        account.save(update_fields=["email"])
        assert account.pk is not None

    def test_other_fields_remain_editable(self, inspector_account):
        inspector_account.first_name = "اسم"
        inspector_account.save(update_fields=["first_name"])
        assert Account.objects.get(pk=inspector_account.pk).first_name == "اسم"


class TestChangeFormFreezesThePersonField:
    def test_change_form_disables_the_person_field(self, inspector_account):
        form = AccountChangeForm(instance=inspector_account)
        assert form.fields["person"].disabled is True

    def test_change_form_explains_why_it_is_frozen(self, inspector_account):
        form = AccountChangeForm(instance=inspector_account)
        assert "ثابت" in form.fields["person"].help_text

    def test_change_form_frozen_field_cannot_move_the_binding(self, inspector_account):
        """Even a forged POST value cannot move the binding through the form."""
        other = make_person(display_name="شخص مُدس (بيانات اختبار)")
        form = AccountChangeForm(
            data={
                "username": inspector_account.username,
                "person": str(other.pk),
                "email": inspector_account.email,
                "is_active": True,
                "is_staff": False,
                "is_superuser": False,
                "date_joined": inspector_account.date_joined.strftime("%Y-%m-%d %H:%M:%S"),
                "password": inspector_account.password,
            },
            instance=inspector_account,
        )
        assert form.is_valid(), form.errors
        saved = form.save()
        assert saved.person_id == inspector_account.person_id
