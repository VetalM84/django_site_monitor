from django.urls import path

from apps.monitor.views import index

urlpatterns = [
    path("", index, name="index"),
]
