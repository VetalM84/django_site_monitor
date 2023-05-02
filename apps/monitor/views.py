import json

from asgiref.sync import sync_to_async
from django.http import HttpResponse
from django.shortcuts import render
from formtools.wizard.views import SessionWizardView

from .forms import ProjectForm, ProjectUnitForm, UnitItemForm
from .models import Project, ProjectUnit, UnitItem


class ProjectWizardView(SessionWizardView):
    """Project Wizard form set."""

    form_list = [ProjectForm, ProjectUnitForm, UnitItemForm]
    template_name = "monitor/project_wizard.html"

    def done(self, form_list, **kwargs):
        """Save forms data to DB upon done."""
        project = form_list[0].save()
        project_unit = form_list[1].save(commit=False)
        project_unit.project = project
        project_unit.save()
        unit_items = form_list[2].save(commit=False)
        unit_items.project_unit = project_unit
        unit_items.save()
        return HttpResponse("Done")


async def index(request):
    """Index view."""
    projects = list(
        [
            project
            async for project in Project.objects.all().prefetch_related("project_units")
        ]
    )
    # projects = Project.objects.prefetch_related("projects")
    return render(request, "monitor/index.html", context={"projects": projects})


async def get_project(request, project_id: int):
    """Project view."""
    project = await get_project_object(project_id=project_id)
    proj_units = list(
        [item async for item in project.project_units.filter(project_id=project_id)]
    )
    return render(
        request,
        "monitor/project.html",
        context={"project": project, "project_units": proj_units},
    )


async def htmx_get_project_to_edit(request, project_id: int):
    project = await get_project_object(project_id=project_id)
    form = ProjectForm(instance=project)
    return render(
        request,
        "monitor/_edit_project.html",
        context={"project": project, "form": form},
    )


async def get_project_object(project_id: int):
    """Get project object."""
    try:
        return await Project.objects.aget(pk=project_id)
    except Exception as e:
        return HttpResponse(f"Error: {e}")


async def htmx_get_project_data(request, project_id: int):
    """Get project html data with HTMX request."""
    project = await get_project_object(project_id=project_id)
    return render(
        request,
        "monitor/_project_data.html",
        context={"project": project},
    )


async def htmx_edit_project(request, project_id: int):
    """Edit project with HTMX request."""
    project = await get_project_object(project_id=project_id)
    project_form = ProjectForm(request.POST or None, instance=project)

    # get edit form with data
    if request.method == "GET":
        return render(
            request,
            "monitor/_edit_project.html",
            context={"project": project, "form": project_form},
        )
    # save form data
    elif request.method == "POST":
        if project_form.is_valid():
            await sync_to_async(project_form.save)()
        return render(
            request,
            "monitor/_project_data.html",
            context={"project": project, "form": project_form},
        )


async def get_all_unit_items(request, unit_id: int):
    """upon HTMX request."""
    if request.method == "POST":
        try:
            unit_items = list(
                [
                    item
                    async for item in UnitItem.objects.filter(project_unit_id=unit_id)
                ]
            )
            return render(
                request, "monitor/_unit_items.html", context={"unit_items": unit_items}
            )
        except Exception as e:
            return HttpResponse(f"Error: {e}")
    else:
        return HttpResponse("Error. Method not allowed.", status=405)
