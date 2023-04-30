"""Monitor models."""

from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse_lazy


class Project(models.Model):
    """Project Model."""

    name = models.CharField(max_length=50, blank=False, verbose_name="Project name")
    check_interval = models.IntegerField(
        default=24, verbose_name="Check Interval in hours"
    )
    is_active = models.BooleanField(default=False, verbose_name="Is Active")

    # user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="User")

    def __str__(self):
        """String representation of the model."""
        return self.name

    def get_absolute_url(self):
        return reverse_lazy("get-project", kwargs={"project_id": self.pk})

    class Meta:
        """Meta."""

        db_table = "monitor_project"
        verbose_name = "Project"
        verbose_name_plural = "Projects"
        ordering = ["name", "is_active"]
        # unique_together = ["user", "name"]


class ProjectUnit(models.Model):
    """Project Unit Model."""

    project = models.ForeignKey(
        Project,
        related_name="project_units",
        on_delete=models.CASCADE,
        verbose_name="Project name",
    )
    is_active = models.BooleanField(default=True, verbose_name="Is Active")
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

    def get_absolute_url(self):
        return reverse_lazy("unit-items", kwargs={"unit_id": self.pk})

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

        db_table = "monitor_project_unit"
        verbose_name = "Project unit"
        verbose_name_plural = "Project units"
        ordering = ["is_active"]


class UnitItem(models.Model):
    """Project Unit Item Model."""

    project_unit = models.ForeignKey(
        ProjectUnit,
        related_name="unit_items",
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

        db_table = "monitor_unit_item"
        verbose_name = "Unit item"
        verbose_name_plural = "Unit items"
