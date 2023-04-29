from django.urls import path

from apps.monitor.views import index, ProjectWizardView

urlpatterns = [
    # path("", index, name="index"),
    path("", ProjectWizardView.as_view(), name="project"),
]
