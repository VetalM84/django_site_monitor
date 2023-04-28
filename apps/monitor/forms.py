"""Forms management."""

from django import forms

from apps.monitor.models import Project, ProjectDetail, ItemsContainer, Item


class ProjectForm(forms.ModelForm):
    """Project form."""

    class Meta:
        """Meta."""

        model = Project
        fields = ("name", "check_interval", "is_active")


class ProjectDetailForm(forms.ModelForm):
    """Project Detail form."""

    class Meta:
        """Meta."""

        model = ProjectDetail
        fields = "__all__"


class ItemsContainerForm(forms.ModelForm):
    """Items Container form."""

    class Meta:
        """Meta."""

        model = ItemsContainer
        fields = "__all__"


class ItemForm(forms.ModelForm):
    """Item form."""

    class Meta:
        """Meta."""

        model = Item
        fields = "__all__"
