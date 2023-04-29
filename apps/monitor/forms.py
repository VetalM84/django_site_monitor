"""Forms management."""

from django import forms

from apps.monitor.models import Item, ItemsContainer, Project, ProjectDetail


class ProjectForm(forms.ModelForm):
    """Project form."""

    name = forms.CharField(
        label="Project name", widget=forms.TextInput(attrs={"class": "form-control"})
    )
    check_interval = forms.IntegerField(
        label="Check Interval in hours", initial=12, min_value=1, max_value=744, widget=forms.NumberInput(attrs={"class": "form-control"})
    )
    is_active = forms.BooleanField(
        required=False, widget=forms.CheckboxInput(attrs={"class": "form-check"})
    )

    class Meta:
        """Meta."""

        model = Project
        fields = "__all__"


class ProjectDetailForm(forms.ModelForm):
    """Project Detail form."""

    # project = forms.ModelChoiceField(
    #     required=False,
    #     queryset=Project.objects.all(),
    #     widget=forms.Select(attrs={"class": "form-select"}),
    # )
    url = forms.URLField(label="Url (with pagination pattern if any)", widget=forms.URLInput(attrs={"class": "form-control"}))
    pagination = forms.IntegerField(
        label="Pagination count", initial=0, required=False, widget=forms.NumberInput(attrs={"class": "form-control"})
    )
    is_active = forms.BooleanField(
        required=False, widget=forms.CheckboxInput(attrs={"class": "form-check"})
    )

    class Meta:
        """Meta."""

        model = ProjectDetail
        fields = ["url", "pagination", "is_active"]


class ItemsContainerForm(forms.ModelForm):
    """Items Container form."""

    # project_detail = forms.ModelChoiceField(
    #     required=False,
    #     queryset=ProjectDetail.objects.all(),
    #     widget=forms.Select(attrs={"class": "form-select"}),
    # )
    html_tag = forms.CharField(
        required=False, widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "div, span, ul, etc."})
    )
    html_tag_class = forms.CharField(
        required=False, widget=forms.TextInput(attrs={"class": "form-control"})
    )
    selector = forms.CharField(
        required=False, widget=forms.TextInput(attrs={"class": "form-control"})
    )

    class Meta:
        """Meta."""

        model = ItemsContainer
        fields = ["html_tag", "html_tag_class", "selector"]


class ItemForm(forms.ModelForm):
    """Item form."""

    # items_container = forms.ModelChoiceField(
    #     queryset=ItemsContainer.objects.all(),
    #     widget=forms.Select(attrs={"class": "form-select"}),
    # )
    html_tag = forms.CharField(
        required=False, widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "div, span, ul, etc."})
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
    text = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={"class": "form-check"}))

    class Meta:
        """Meta."""

        model = Item
        # fields = "__all__"
        exclude = ["items_container"]
