from django.urls import path

from . import views

app_name = "institutions"

urlpatterns = [
    path("", views.institution_list, name="list"),
    path("new/", views.institution_create, name="create"),
    path("<uuid:institution_id>/", views.institution_detail, name="detail"),
    path("<uuid:institution_id>/edit/", views.institution_edit, name="edit"),
    path("<uuid:institution_id>/archive/", views.institution_archive, name="archive"),
    path("<uuid:institution_id>/delete/", views.institution_delete, name="delete"),
]
