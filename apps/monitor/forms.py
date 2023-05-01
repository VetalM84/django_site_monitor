"""Forms management."""

from django import forms

from apps.monitor.models import Project, ProjectUnit, UnitItem


class ProjectForm(forms.ModelForm):
    """Project form."""

    name = forms.CharField(
        label="Project name", widget=forms.TextInput(attrs={"class": "form-control"})
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


class ProjectUnitForm(forms.ModelForm):
    """Project Unit form."""

    # project = forms.ModelChoiceField(
    #     required=False,
    #     queryset=Project.objects.all(),
    #     widget=forms.Select(attrs={"class": "form-select"}),
    # )
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
    container_html_tag = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "div, span, ul, etc."}
        ),
    )
    container_html_tag_class = forms.CharField(
        required=False, widget=forms.TextInput(attrs={"class": "form-control"})
    )
    container_selector = forms.CharField(
        required=False, widget=forms.TextInput(attrs={"class": "form-control"})
    )
    is_active = forms.BooleanField(
        required=False, widget=forms.CheckboxInput(attrs={"class": "form-check"})
    )

    class Meta:
        """Meta."""

        model = ProjectUnit
        fields = [
            "url",
            "pagination",
            "container_html_tag",
            "container_html_tag_class",
            "container_selector",
            "is_active",
        ]


class UnitItemForm(forms.ModelForm):
    """Unit Item form."""

    # project_unit = forms.ModelChoiceField(
    #     queryset=ItemsContainer.objects.all(),
    #     widget=forms.Select(attrs={"class": "form-select"}),
    # )
    html_tag = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "div, span, ul, ...."}
        ),
    )
    html_tag_class = forms.CharField(
        required=False, widget=forms.TextInput(attrs={"class": "form-control"})
    )
    selector = forms.CharField(
        required=False, widget=forms.TextInput(attrs={"class": "form-control"})
    )
    html_attr = forms.CharField(
        required=False, widget=forms.TextInput(attrs={"class": "form-control"})
    )
    extract_text = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(
            attrs={"class": "form-check", "placeholder": "href, data-id, ...."}
        ),
    )

    class Meta:
        """Meta."""

        model = UnitItem
        exclude = ["project_unit"]
