"""."""

import asyncio

import httpx
from asgiref.sync import sync_to_async
from bs4 import BeautifulSoup
from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseServerError
from django.shortcuts import render
from formtools.wizard.views import SessionWizardView

from .forms import ProjectForm, ProjectModuleForm
from .models import Project, ProjectModule


class ProjectWizardView(SessionWizardView):
    """New Project Wizard form set."""

    form_list = [ProjectForm, ProjectModuleForm]
    template_name = "monitor/project_wizard.html"

    def done(self, form_list, **kwargs):
        """Save forms data to DB upon done."""
        project = form_list[0].save()
        project_unit = form_list[1].save(commit=False)
        project_unit.project = project
        project_unit.save()
        return HttpResponse("Done")


# async def index(request):
#     """Index view."""
#     projects = list(
#         [
#             project
#             async for project in Project.objects.all().prefetch_related("project_units")
#         ]
#     )
#     return render(request, "monitor/index.html", context={"projects": projects})


async def index(request):
    # TODO: replace with user's dashboard
    projects = list(
        [project async for project in Project.objects.all().prefetch_related("modules")]
    )
    return render(request, "monitor/index.html", context={"projects": projects})


async def get_project(request, project_id: int):
    """Detailed project view with modules."""
    project = await Project.objects.prefetch_related("modules").aget(pk=project_id)
    return render(
        request,
        "monitor/project.html",
        context={"project": project, "call_url": call_url},
    )


async def call_url(url: str):
    """Make a request to an external url."""
    # TODO: move to class
    # TODO: add headers to aiohttp.ClientSession
    # TODO: add timeout to aiohttp.ClientSession
    try:
        async with httpx.AsyncClient() as client:
            response = client.get(url=url)
            return await response
    except Exception as e:
        print(e)
        return httpx.Response(status_code=500)


async def get_project_object(project_id: int):
    """Get project object."""
    try:
        return await Project.objects.aget(pk=project_id)
    except Exception as e:
        return HttpResponseServerError(f"Error: {e}")


async def htmx_call_url(request):
    """Call url with HTMX request."""
    # TODO: add user check
    if request.method == "POST":
        response = await call_url(url=request.POST.get("url"))
        if response.status_code == 200:
            return HttpResponse(content="Page response OK")
        elif response.status_code == 404:
            return HttpResponse(content="Page not found")
        else:
            # TODO: add errors list (elif error in errors[500,501,...])
            return HttpResponse(
                content=f"Error. Response code is {response.status_code}",
                status=response.status_code,
            )


async def htmx_get_project_to_edit(request, project_id: int):
    project = await get_project_object(project_id=project_id)
    form = ProjectForm(instance=project)
    return render(
        request,
        "monitor/_edit_project.html",
        context={"project": project, "form": form},
    )


async def htmx_get_project(request, project_id: int):
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


async def get_module_object(module_id: int):
    """Get module object."""
    try:
        return await ProjectModule.objects.aget(pk=module_id)
    except Exception as e:
        return HttpResponseServerError(f"Error: {e}")


async def htmx_edit_module(request, module_id: int):
    """Edit module with HTMX request."""
    module = await get_module_object(module_id=module_id)
    module_form = ProjectModuleForm(request.POST or None, instance=module)
    context = {"module": module, "form": module_form}

    # get edit form with data
    if request.method == "GET":
        return render(request, "monitor/_edit_module.html", context=context)
    # save form data
    elif request.method == "POST":
        if module_form.is_valid():
            await sync_to_async(module_form.save)()
            return render(request, "monitor/_module_data.html", context=context)
        else:
            return render(request, "monitor/_edit_module.html", context=context)


async def htmx_get_module(request, module_id: int):
    """Get project html data with HTMX request."""
    module = await get_module_object(module_id=module_id)
    return render(request, "monitor/_module_data.html", context={"module": module})


async def htmx_delete_module(request, module_id: int):
    """Delete project form DB with HTMX request."""
    if request.method == "POST":
        try:
            await ProjectModule.objects.filter(pk=module_id).adelete()
            return HttpResponse(content="Module deleted")
        except Exception as e:
            return HttpResponseServerError(f"Error: {e}")
    else:
        return HttpResponseNotAllowed("Error. Method not allowed.")


async def htmx_test_run_module(request, module_id: int):
    """Test run module with HTMX request."""
    if request.method == "GET":
        try:
            module_coroutine = ProjectModule.objects.aget(pk=module_id)
            module = await module_coroutine
            response = await call_url(url=module.url)
            soup = BeautifulSoup(response.text, "lxml")
            selector = soup.select_one(module.css_selector)

            return HttpResponse(selector)
        except Exception as e:
            return HttpResponseServerError(f"Error: {e}")
    else:
        return HttpResponseNotAllowed("Error. Method not allowed.")
