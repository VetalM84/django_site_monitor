"""."""

import asyncio

from asgiref.sync import sync_to_async
from bs4 import BeautifulSoup
from django.contrib.auth.models import AnonymousUser
from django.http import (
    HttpRequest,
    HttpResponse,
    HttpResponseNotAllowed,
    HttpResponseServerError,
)
from django.shortcuts import render
from formtools.wizard.views import SessionWizardView

from ..accounts.models import User
from .forms import ProjectForm, ProjectModuleForm
from .models import Project, ProjectModule, ScrapResult
from .utils.url_request import URLRequest


class ProjectWizardView(SessionWizardView):
    """New Project Wizard form set."""

    form_list = [ProjectForm, ProjectModuleForm]
    template_name = "monitor/project_wizard.html"

    def done(self, form_list, **kwargs):
        """Save forms data to DB upon done."""
        project = form_list[0].save(commit=False)
        project.user = self.request.user
        project.save()
        project_module = form_list[1].save(commit=False)
        project_module.project = project
        project_module.save()
        return HttpResponse("Done")


# async def index(request):
#     """Index view."""
#     return render(request, "monitor/index.html", context={"projects": projects})


async def user_dashboard(request):
    projects = list(
        [project async for project in Project.objects.all().prefetch_related("modules")]
    )
    return render(request, "monitor/index.html", context={"projects": projects})


async def get_project(request, project_id: int):
    """Detailed project view with modules."""
    project: Project = await Project.objects.prefetch_related("modules").aget(
        pk=project_id
    )
    return render(request, "monitor/project.html", context={"project": project})


async def save_parsed_data(module, status_code):
    """Save parsed data to DB."""
    try:
        result = ScrapResult()
        # result.data = await parse_data()
        result.module = module
        result.status_code = status_code
        await result.asave()
    except Exception as e:
        print(e)
        return httpx.Response(status_code=500)


async def get_project_object(project_id: int):
    """Get project object."""
    try:
        return await Project.objects.aget(pk=project_id)
    except Exception as e:
        return HttpResponseServerError(f"Error: {e}")


@sync_to_async
def get_user_from_request(request: HttpRequest) -> User | AnonymousUser | None:
    """Async get user object from request."""
    return request.user if bool(request.user) else None


async def htmx_test_call_url(request):
    """Call url with HTMX request."""
    user = await get_user_from_request(request)
    client = URLRequest()

    if user.is_authenticated and request.method == "POST":
        # TODO: call_url with POST method
        module: ProjectModule = await ProjectModule.objects.aget(
            pk=request.POST.get("module_id")
        )

        response = await client.get_url_with_pagination(module)

        if response.status_code == 200:
            return HttpResponse(content="Page response OK")
        elif response.status_code in [301, 302]:
            return HttpResponse(content="Page redirected")
        elif response.status_code == 404:
            return HttpResponse(content="Page not found")
        else:
            # TODO: add errors list (elif error in errors[500,501,...])
            return HttpResponse(
                content=f"Error. Response code is {response.status_code}",
                status=response.status_code,
            )


async def htmx_get_project_to_edit(request, project_id: int):
    project: Project = await get_project_object(project_id=project_id)
    form = ProjectForm(instance=project)
    return render(
        request,
        "monitor/_edit_project.html",
        context={"project": project, "form": form},
    )


async def htmx_get_project(request, project_id: int):
    """Get project html data with HTMX request."""
    project: Project = await get_project_object(project_id=project_id)
    return render(
        request,
        "monitor/_project_data.html",
        context={"project": project},
    )


async def htmx_edit_project(request, project_id: int):
    """Edit project with HTMX request."""
    project: Project = await get_project_object(project_id=project_id)
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
    module: ProjectModule = await get_module_object(module_id=module_id)
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


async def htmx_add_module(request, project_id: int):
    """Add new module with HTMX request."""
    module_form = ProjectModuleForm(request.POST or None)
    project: Project = await Project.objects.filter(pk=project_id).afirst()
    context = {"form": module_form, "project": project}

    # render form to save new module
    if request.method == "GET":
        return render(request, "monitor/_add_module.html", context=context)

    # save new module upon form submission
    elif request.method == "POST":
        if module_form.is_valid():
            new_module = module_form.save(commit=False)
            new_module.project = project
            await sync_to_async(new_module.save)()
            return render(
                request,
                "monitor/_module_data.html",
                context={"module": new_module},
            )
        else:
            return render(request, "monitor/_add_module.html", context=context)


async def htmx_get_module(request, module_id: int):
    """Get project html data with HTMX request."""
    module: ProjectModule = await get_module_object(module_id=module_id)
    return render(request, "monitor/_module_data.html", context={"module": module})


async def htmx_delete_module(request, module_id: int):
    """Delete project form DB with HTMX request."""
    # TODO: add user check
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
    # TODO: add user check
    client = URLRequest()
    if request.method == "GET":
        try:
            module: ProjectModule = await ProjectModule.objects.aget(pk=module_id)
            response = await client.get_url_with_pagination(module=module)
            soup = BeautifulSoup(response.text, "lxml")
            selector = soup.select_one(module.css_selector)

            return HttpResponse(selector)
        except Exception as e:
            return HttpResponseServerError(f"Error: {e}")
    else:
        return HttpResponseNotAllowed("Error. Method not allowed.")
