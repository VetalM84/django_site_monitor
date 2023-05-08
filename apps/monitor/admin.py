"""Backend admin page."""

from django.contrib import admin

from apps.monitor.models import Project, ProjectModule, ScrapResult


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    """Project model views on backend."""

    list_display = (
        "id",
        "name",
        "check_interval",
        "is_active",
        "user",
        "last_run",
        "date_created",
    )
    list_display_links = ("id", "name")
    ordering = ("-is_active", "name", "user")
    search_fields = ("name",)


@admin.register(ProjectModule)
class ProjectModuleAdmin(admin.ModelAdmin):
    """ProjectModule model views on backend."""

    list_display = ("id", "project", "is_active", "url", "pagination", "css_selector")
    list_display_links = ("id", "project")
    ordering = ("is_active", "project")
    search_fields = ("url", "css_selector")


@admin.register(ScrapResult)
class ScrapResultAdmin(admin.ModelAdmin):
    """ScrapResult model views on backend."""

    list_display = ("id", "module", "date_created", "status_code")
    list_display_links = ("id", "module")
    ordering = ("date_created", "module")
    search_fields = ("data",)
