"""Forms management."""

from django import forms

from apps.monitor.models import Project, ProjectModule


class ProjectForm(forms.ModelForm):
    """Project form."""

    name = forms.CharField(
        label="Project name",
        max_length=50,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    check_interval = forms.IntegerField(
        label="Check Interval in hours",
        initial=12,
        min_value=1,
        max_value=744,
        widget=forms.NumberInput(attrs={"class": "form-control"}),
    )
    is_active = forms.BooleanField(
        required=False, widget=forms.CheckboxInput(attrs={"class": "form-check"})
    )

    class Meta:
        """Meta."""

        model = Project
        fields = ["name", "check_interval", "is_active"]


class ProjectModuleForm(forms.ModelForm):
    """Project Unit form."""

    url = forms.URLField(
        label="Url (with pagination pattern if any)",
        widget=forms.URLInput(
            attrs={
                "class": "form-control",
                "placeholder": "replace page number with $page$",
            }
        ),
    )
    pagination = forms.IntegerField(
        label="Pagination count",
        initial=0,
        required=False,
        widget=forms.NumberInput(attrs={"class": "form-control"}),
    )
    css_selector = forms.CharField(
        required=False, widget=forms.TextInput(attrs={"class": "form-control"})
    )
    is_active = forms.BooleanField(
        required=False, widget=forms.CheckboxInput(attrs={"class": "form-check"})
    )

    class Meta:
        """Meta."""

        model = ProjectModule
        fields = [
            "url",
            "pagination",
            "css_selector",
            "is_active",
        ]
