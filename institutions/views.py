from __future__ import annotations

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, HttpResponseForbidden
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods, require_POST

from identity.permissions import PermissionDeniedError, is_platform_admin

from .forms import InstitutionForm
from .models import Institution
from .permissions import can_create_local_institution, can_mutate_institution
from .selectors import get_visible_institution_or_404, institutions_visible_to
from .services import (
    InstitutionError,
    InstitutionPermissionDenied,
    archive_local_institution,
    create_local_institution,
    delete_local_institution,
    update_local_institution,
)


def _base_context(request: HttpRequest) -> dict:
    return {"is_platform_admin": is_platform_admin(request.user)}


def _forbidden_response(message: str) -> HttpResponse:
    return HttpResponseForbidden(message)


@login_required
@require_http_methods(["GET"])
def institution_list(request: HttpRequest) -> HttpResponse:
    context = _base_context(request)
    context.update(
        {
            "institutions": institutions_visible_to(request.user),
            "can_create": can_create_local_institution(request.user),
        }
    )
    return render(request, "institutions/institution_list.html", context)


@login_required
@require_http_methods(["GET", "POST"])
def institution_create(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = InstitutionForm(request.POST)
        if form.is_valid():
            try:
                institution = create_local_institution(
                    actor=request.user,
                    name=form.cleaned_data["name"],
                )
            except PermissionDeniedError as exc:
                return _forbidden_response(str(exc))
            messages.success(request, "تم إنشاء المؤسسة.")
            return redirect("institutions:detail", institution_id=institution.pk)
    else:
        form = InstitutionForm()

    context = _base_context(request)
    context["form"] = form
    return render(request, "institutions/institution_form.html", context)


@login_required
@require_http_methods(["GET"])
def institution_detail(request: HttpRequest, institution_id) -> HttpResponse:
    institution = get_visible_institution_or_404(
        actor=request.user,
        institution_id=institution_id,
    )
    context = _base_context(request)
    context.update(
        {
            "institution": institution,
            "can_mutate": can_mutate_institution(request.user, institution)
            and institution.lifecycle == Institution.Lifecycle.LOCAL_ACTIVE,
        }
    )
    return render(request, "institutions/institution_detail.html", context)


@login_required
@require_http_methods(["GET", "POST"])
def institution_edit(request: HttpRequest, institution_id) -> HttpResponse:
    institution = get_visible_institution_or_404(
        actor=request.user,
        institution_id=institution_id,
    )
    if not can_mutate_institution(request.user, institution):
        return _forbidden_response("لا تملك صلاحية تعديل هذه المؤسسة.")

    if request.method == "POST":
        form = InstitutionForm(request.POST, instance=institution)
        if form.is_valid():
            try:
                update_local_institution(
                    actor=request.user,
                    institution=institution,
                    name=form.cleaned_data["name"],
                )
            except InstitutionError as exc:
                form.add_error(None, str(exc))
            else:
                messages.success(request, "تم تحديث المؤسسة.")
                return redirect("institutions:detail", institution_id=institution.pk)
    else:
        form = InstitutionForm(instance=institution)

    context = _base_context(request)
    context.update({"form": form, "institution": institution, "mode": "edit"})
    return render(request, "institutions/institution_form.html", context)


@login_required
@require_POST
def institution_archive(request: HttpRequest, institution_id) -> HttpResponse:
    institution = get_visible_institution_or_404(
        actor=request.user,
        institution_id=institution_id,
    )
    try:
        archive_local_institution(actor=request.user, institution=institution)
    except InstitutionPermissionDenied as exc:
        return _forbidden_response(str(exc))
    except InstitutionError as exc:
        messages.error(request, str(exc))
        return redirect("institutions:detail", institution_id=institution.pk)
    messages.success(request, "تمت أرشفة المؤسسة.")
    return redirect("institutions:detail", institution_id=institution.pk)


@login_required
@require_http_methods(["GET", "POST"])
def institution_delete(request: HttpRequest, institution_id) -> HttpResponse:
    institution = get_visible_institution_or_404(
        actor=request.user,
        institution_id=institution_id,
    )
    if not can_mutate_institution(request.user, institution):
        return _forbidden_response("لا تملك صلاحية حذف هذه المؤسسة.")

    if request.method == "POST":
        try:
            delete_local_institution(actor=request.user, institution=institution)
        except InstitutionError as exc:
            messages.error(request, str(exc))
            return redirect("institutions:detail", institution_id=institution.pk)
        messages.success(request, "تم حذف المؤسسة.")
        return redirect("institutions:list")

    context = _base_context(request)
    context["institution"] = institution
    return render(request, "institutions/institution_confirm_delete.html", context)
