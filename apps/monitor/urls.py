from django.urls import path

from apps.monitor.views import ProjectWizardView, get_all_unit_items, get_project, index

urlpatterns = [
    path("", index, name="index"),
    path("new-project/", ProjectWizardView.as_view(), name="new-project"),
    path("project/<int:project_id>/", get_project, name="get-project"),
]
htmx_patterns = [
    path(
        "unit-items/<int:unit_id>/",
        get_all_unit_items,
        name="unit-items",
    ),
]

urlpatterns += htmx_patterns
