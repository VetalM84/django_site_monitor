from django.urls import path

from apps.monitor.views import (
    ProjectWizardView,
    diff_view,
    get_module_reports,
    get_project,
    get_single_report,
    htmx_add_module,
    htmx_delete_module,
    htmx_edit_module,
    htmx_edit_project,
    htmx_get_module,
    htmx_get_project,
    htmx_test_call_url,
    htmx_test_run_module,
    user_dashboard,
    scap_save,
)

urlpatterns = [
    path("", user_dashboard, name="user-dashboard"),
    path("new-project/", ProjectWizardView.as_view(), name="new-project"),
    path("project/<int:project_id>/", get_project, name="project"),
    path("diff-view/", diff_view, name="diff-view"),
    path("report/<int:report_id>/", get_single_report, name="report"),
    path("module/<int:module_id>/reports/", get_module_reports, name="module-reports"),
    path("r/", scap_save, name="r"),
]
htmx_patterns = [
    path("call_url/", htmx_test_call_url, name="htmx-call-url"),
    path("project/<int:project_id>/edit/", htmx_edit_project, name="htmx-edit-project"),
    path("project/<int:project_id>/get/", htmx_get_project, name="htmx-get-project"),
    path("module/<int:project_id>/add/", htmx_add_module, name="htmx-add-module"),
    path("module/<int:module_id>/", htmx_get_module, name="htmx-get-module"),
    path("module/<int:module_id>/run/", htmx_test_run_module, name="htmx-test-module"),
    path(
        "module/<int:module_id>/delete/", htmx_delete_module, name="htmx-delete-module"
    ),
    path("module/<int:module_id>/edit/", htmx_edit_module, name="htmx-edit-module"),
]

urlpatterns += htmx_patterns
