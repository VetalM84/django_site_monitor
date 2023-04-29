from asgiref.sync import sync_to_async
from django.shortcuts import render
from formtools.wizard.views import SessionWizardView

from .forms import ProjectForm, ProjectDetailForm, ItemsContainerForm, ItemForm
from django.http import HttpResponse, HttpResponseBadRequest


class ProjectWizardView(SessionWizardView):
    """Project Wizard form set."""

    form_list = (ProjectForm, ProjectDetailForm, ItemsContainerForm)
    template_name = "monitor/project_wizard.html"

    def done(self, form_list, **kwargs):
        """Save forms data to DB upon done."""
        project = form_list[0].save()
        project_detail = form_list[1].save(commit=False)
        project_detail.project = project
        project_detail.save()
        items_container = form_list[2].save(commit=False)
        items_container.project_detail = project_detail
        items_container.save()
        return HttpResponse("Done")


def index(request):
    """Index view."""
    project_form = ProjectForm(data=request.POST or None)
    project_detail_form = ProjectDetailForm(data=request.POST or None)
    # items_container_form = ItemsContainerForm()
    # item_form = ItemForm()
    if request.method == "POST":
        try:
            if project_form.is_valid():
                project_form.save()
                return render(
                    request,
                    "monitor/project_wizard.html",
                    context={"project_detail_form": project_detail_form},
                )
        except Exception as e:
            return HttpResponse(f"Error: {e}")
    # context = {
    #     "project_form": project_form,
    #     "project_detail_form": project_detail_form,
    #     # "items_container_form": items_container_form,
    #     # "item_form": item_form,
    # }
    return render(request, "monitor/index.html", context={"project_form": project_form})


async def new_project(request):
    """Create a new project upon HTMX request, return JSONResponse."""
    if request.method == "POST":
        try:
            project = ProjectForm(request.POST)
            if project.is_valid():
                await sync_to_async(project.save)()
            # project = Project(
            #     name=request.POST.get("name"),
            #     check_interval=request.POST.get("check_interval"),
            #     # TODO: is_active "on" is not working
            #     is_active=request.POST.get("is_active", False),
            # )
            # await project.asave()
            return render(
                request,
                "monitor/project_wizard.html",
                context={"project_detail_form": project},
            )
        except Exception as e:
            return HttpResponse(f"Error: {e}")
    else:
        return HttpResponse("Error. Method not allowed.", status=405)
