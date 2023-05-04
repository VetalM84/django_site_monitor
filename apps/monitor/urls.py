from django.urls import path

from apps.monitor.views import (
    ProjectWizardView,
    get_project,
    htmx_call_url,
    htmx_delete_module,
    htmx_edit_module,
    htmx_edit_project,
    htmx_get_module,
    htmx_get_project,
    htmx_test_run_module,
    index,
)

urlpatterns = [
    path("", index, name="index"),
    path("new-project/", ProjectWizardView.as_view(), name="new-project"),
    path("project/<int:project_id>/", get_project, name="get-project"),
]
htmx_patterns = [
    path("call_url/", htmx_call_url, name="htmx-call-url"),
    path("project/<int:project_id>/edit/", htmx_edit_project, name="htmx-edit-project"),
    path("get-project/<int:project_id>/", htmx_get_project, name="htmx-get-project"),
    path("module/<int:module_id>/run/", htmx_test_run_module, name="htmx-test-module"),
    path(
        "module/<int:module_id>/delete/", htmx_delete_module, name="htmx-delete-module"
    ),
    path("module/<int:module_id>/edit/", htmx_edit_module, name="htmx-edit-module"),
    path("get-module/<int:module_id>/", htmx_get_module, name="htmx-get-module"),
]

urlpatterns += htmx_patterns
