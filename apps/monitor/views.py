from asgiref.sync import sync_to_async
from django.shortcuts import render
from formtools.wizard.views import SessionWizardView

from .forms import ProjectForm, ProjectUnitForm, UnitItemForm
from django.http import HttpResponse

from .models import Project, ProjectUnit, UnitItem


class ProjectWizardView(SessionWizardView):
    """Project Wizard form set."""

    form_list = [ProjectForm, ProjectUnitForm]
    template_name = "monitor/project_wizard.html"

    def done(self, form_list, **kwargs):
        """Save forms data to DB upon done."""
        project = form_list[0].save()
        project_unit = form_list[1].save(commit=False)
        project_unit.project = project
        project_unit.save()
        # items_container = form_list[2].save(commit=False)
        # items_container.project_unit = project_unit
        # items_container.save()
        return HttpResponse("Done")


async def index(request):
    """Index view."""
    projects = list([project async for project in Project.objects.all()])
    # projects = Project.objects.prefetch_related("projects")
    return render(request, "monitor/index.html", context={"projects": projects})


async def get_project(request, project_id: int):
    """Project view."""
    project = await Project.objects.aget(pk=project_id)
    proj_units = list(
        [item async for item in project.project_units.filter(project_id=project_id)]
    )
    return render(
        request,
        "monitor/project.html",
        context={"project": project, "project_units": proj_units},
    )


async def get_all_unit_items(request, unit_id: int):
    """upon HTMX request."""
    if request.method == "GET":
        try:
            unit_items = list(
                [
                    item
                    async for item in UnitItem.objects.filter(project_unit_id=unit_id)
                ]
            )
            print(unit_items)
            return HttpResponse(unit_items)
        except Exception as e:
            return HttpResponse(f"Error: {e}")
    else:
        return HttpResponse("Error. Method not allowed.", status=405)
