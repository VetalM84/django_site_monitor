"""Site change monitor models."""

from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse_lazy

from apps.accounts.models import User


class Project(models.Model):
    """Project Model."""

    name = models.CharField(max_length=50, blank=False, verbose_name="Project name")
    check_interval = models.IntegerField(
        default=24, verbose_name="Check interval in hours"
    )
    is_active = models.BooleanField(default=False, verbose_name="Is active")
    date_created = models.DateTimeField(auto_now_add=True, verbose_name="Date created")
    last_run = models.DateTimeField(null=True, blank=True, verbose_name="Last run")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="User")

    def __str__(self):
        """String representation of the model."""
        return self.name

    def get_absolute_url(self):
        """Get absolute url."""
        return reverse_lazy("project", kwargs={"project_id": self.pk})

    class Meta:
        """Meta."""

        verbose_name = "Project"
        verbose_name_plural = "Projects"
        ordering = ["name", "-is_active"]
        unique_together = ["user", "name"]


class ProjectModule(models.Model):
    """Project Module Model."""

    project = models.ForeignKey(
        Project,
        related_name="modules",
        on_delete=models.CASCADE,
        verbose_name="Project name",
    )
    is_active = models.BooleanField(default=True, verbose_name="Is Active")
    url = models.URLField(verbose_name="URL")
    pagination = models.IntegerField(default=0, verbose_name="Pagination count")
    css_selector = models.CharField(
        max_length=1024, blank=False, verbose_name="CSS selector"
    )

    def __str__(self):
        """String representation of the model."""
        return self.project.name + ", " + self.url[:50] + "..."

    # def save(self, *args, **kwargs):
    #     """Save method."""
    #     super().save()
    #     # TODO: send request to url, save response status code, scrap data

    def clean(self):
        """Validation for url, pagination."""
        if self.pagination and self.url.find("$page$") == -1:
            raise ValidationError("URL with pagination must have $page$ pattern")

    class Meta:
        """Meta."""

        verbose_name = "Project module"
        verbose_name_plural = "Project modules"
        ordering = ["-is_active"]


class ScrapResult(models.Model):
    """Scrap result model."""

    module = models.ForeignKey(
        ProjectModule,
        related_name="scrap_results",
        on_delete=models.CASCADE,
        verbose_name="Project module",
    )
    url = models.URLField(blank=True, verbose_name="URL")
    data = models.TextField(blank=True, verbose_name="Data")
    date_created = models.DateTimeField(auto_now_add=True, verbose_name="Date created")
    status_code = models.IntegerField(verbose_name="Status code")

    def __str__(self):
        """String representation of the model."""
        return self.module.project.name + ", " + self.module.url[:50] + "..."

    class Meta:
        """Meta."""

        verbose_name = "Scrap result"
        verbose_name_plural = "Scrap results"
        ordering = ["-date_created", "module"]
