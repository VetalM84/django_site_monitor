"""Monitor models."""

from django.core.exceptions import ValidationError
from django.db import models


class Project(models.Model):
    """Project Model."""

    name = models.CharField(max_length=50, verbose_name="Project name")
    check_interval = models.IntegerField(
        default=24, verbose_name="Check Interval in hours"
    )
    is_active = models.BooleanField(default=False, verbose_name="Is Active")

    # user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="User")

    def __str__(self):
        """String representation of the model."""
        return self.name

    class Meta:
        """Meta."""

        db_table = "project"
        verbose_name = "Project"
        verbose_name_plural = "Projects"
        ordering = ["name", "is_active"]


class ProjectDetail(models.Model):
    """Project Detail Model."""

    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, verbose_name="Project"
    )
    url = models.URLField(verbose_name="URL")
    pagination = models.IntegerField(default=0, verbose_name="Pagination count")
    # single_item_container = models.CharField(
    #     max_length=1024, blank=True, default=None, verbose_name="Single item container"
    # )
    is_active = models.BooleanField(default=True, verbose_name="Is Active")

    def __str__(self):
        """String representation of the model."""
        return self.project.name, self.url[:50], "..."

    class Meta:
        """Meta."""

        db_table = "project_detail"
        verbose_name = "Project Detail"
        verbose_name_plural = "Projects Details"
        ordering = ["is_active"]


class ItemsContainer(models.Model):
    """Items Container Model."""

    project_detail = models.OneToOneField(
        ProjectDetail, on_delete=models.CASCADE, verbose_name="Project Detail"
    )
    html_tag = models.CharField(
        max_length=1024, blank=True, default=None, verbose_name="HTML Tag"
    )
    html_tag_class = models.CharField(
        max_length=1024, blank=True, default=None, verbose_name="HTML Tag class"
    )
    selector = models.CharField(
        max_length=1024, blank=True, default=None, verbose_name="Selector"
    )

    def __str__(self):
        """String representation of the model."""
        return self.project_detail.project.name, self.project_detail.url[:50], "..."

    def clean(self):
        """Validation for tag, selector - one of them must be filled."""
        if (not self.html_tag and not self.selector) or (
            self.html_tag and self.selector
        ):
            raise ValidationError("Tag or Selector must be filled")

    class Meta:
        """Meta."""

        db_table = "items_container"
        verbose_name = "Items Container"
        verbose_name_plural = "Items Containers"


class Item(models.Model):
    """Item Model."""

    items_container = models.ForeignKey(
        ItemsContainer, on_delete=models.CASCADE, verbose_name="Items Container"
    )
    html_tag = models.CharField(
        max_length=1024, blank=True, default=None, verbose_name="HTML Tag"
    )
    html_tag_class = models.CharField(
        max_length=1024, blank=True, default=None, verbose_name="HTML Tag class"
    )
    selector = models.CharField(
        max_length=1024, blank=True, default=None, verbose_name="Selector"
    )
    html_attr = models.CharField(
        max_length=1024, default=None, blank=True, verbose_name="HTML attribute"
    )
    text = models.BooleanField(default=False, verbose_name="Extract text")

    class Meta:
        """Meta."""

        db_table = "item"
        verbose_name = "Item"
        verbose_name_plural = "Items"
