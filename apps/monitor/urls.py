from django.urls import path

from apps.monitor.views import (
    ProjectWizardView,
    get_all_unit_items,
    get_project,
    htmx_edit_project,
    htmx_get_project_data,
    index,
    call_url,
    htmx_call_url,
)

urlpatterns = [
    path("", index, name="index"),
    path("new-project/", ProjectWizardView.as_view(), name="new-project"),
    path("project/<int:project_id>/", get_project, name="get-project"),
]
htmx_patterns = [
    path("call_url", htmx_call_url, name="htmx-call-url"),
    path("project/<int:project_id>/edit/", htmx_edit_project, name="htmx-edit-project"),
    path(
        "get-project-data/<int:project_id>/",
        htmx_get_project_data,
        name="htmx-get-project-data",
    ),
    path(
        "unit-items/<int:unit_id>/",
        get_all_unit_items,
        name="htmx-unit-items",
    ),
]

urlpatterns += htmx_patterns
