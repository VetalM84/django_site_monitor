from django.urls import path

from apps.monitor.views import (
    index,
    ProjectWizardView,
    get_project,
    get_all_unit_items,
)

urlpatterns = [
    path("", index, name="index"),
    path("new-project/", ProjectWizardView.as_view(), name="new-project"),
    path("project/<int:project_id>/", get_project, name="get-project"),
    path(
        "unit-items/<int:unit_id>/",
        get_all_unit_items,
        name="unit-items",
    ),
]
