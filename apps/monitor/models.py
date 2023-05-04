"""Monitor models."""

from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse_lazy


class Project(models.Model):
    """Project Model."""

    name = models.CharField(max_length=50, blank=False, verbose_name="Project name")
    check_interval = models.IntegerField(
        default=24, verbose_name="Check interval in hours"
    )
    is_active = models.BooleanField(default=False, verbose_name="Is active")
    date_created = models.DateTimeField(auto_now_add=True, verbose_name="Date created")
    last_run = models.DateTimeField(null=True, blank=True, verbose_name="Last run")

    # user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="User")

    def __str__(self):
        """String representation of the model."""
        return self.name

    def get_absolute_url(self):
        return reverse_lazy("get-project", kwargs={"project_id": self.pk})

    class Meta:
        """Meta."""

        verbose_name = "Project"
        verbose_name_plural = "Projects"
        ordering = ["name", "-is_active"]
        # unique_together = ["user", "name"]


class ProjectModule(models.Model):
    """Project Module Model."""

    project = models.ForeignKey(
        Project,
        related_name="modules",
        on_delete=models.CASCADE,
        verbose_name="Project name",
    )
    is_active = models.BooleanField(default=True, verbose_name="Is Active")
    date_created = models.DateTimeField(auto_now_add=True, verbose_name="Date created")
    url = models.URLField(verbose_name="URL")
    pagination = models.IntegerField(default=0, verbose_name="Pagination count")
    container_html_tag = models.CharField(
        max_length=1024, blank=True, default="", verbose_name="HTML Tag"
    )
    container_html_tag_class = models.CharField(
        max_length=1024, blank=True, default="", verbose_name="HTML Tag class"
    )
    container_selector = models.CharField(
        max_length=1024, blank=True, default="", verbose_name="Selector"
    )

    def __str__(self):
        """String representation of the model."""
        return self.project.name + ", " + self.url[:50] + "..."

    def clean(self):
        """Validation for url, pagination."""
        # TODO: send request to url, check response status code
        if self.pagination and self.url.find("$page$") == -1:
            raise ValidationError("URL with pagination must have $page$ pattern")

        """Validation for tag, selector - one of them must be filled."""
        if (not self.container_html_tag and not self.container_selector) or (
            self.container_html_tag and self.container_selector
        ):
            raise ValidationError("Tag or Selector must be filled")

    class Meta:
        """Meta."""

        verbose_name = "Project module"
        verbose_name_plural = "Project modules"
        ordering = ["-is_active"]


class ModuleItem(models.Model):
    """Project Module Item Model."""

    project_unit = models.ForeignKey(
        ProjectModule,
        related_name="module_items",
        on_delete=models.CASCADE,
        verbose_name="Project unit",
    )
    html_tag = models.CharField(
        max_length=1024, blank=True, default="", verbose_name="HTML Tag"
    )
    html_tag_class = models.CharField(
        max_length=1024, blank=True, default="", verbose_name="HTML Tag class"
    )
    selector = models.CharField(
        max_length=1024, blank=True, default="", verbose_name="Selector"
    )
    html_attr = models.CharField(
        max_length=1024, blank=True, default="", verbose_name="HTML attribute"
    )
    extract_text = models.BooleanField(default=False, verbose_name="Extract text")

    class Meta:
        """Meta."""

        verbose_name = "Module item"
        verbose_name_plural = "Module items"
