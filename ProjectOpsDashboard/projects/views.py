from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Project
from core import constants
from .forms import ProjectForm

@login_required(login_url='login-page')
def projectsMainPage(request):
    user = request.user

    if user.role == 'manager':
        projectsList = Project.objects.all()
    elif user.role == 'member':
        projectsList = Project.objects.filter(
            tasks__assigned_to=user
        ).distinct()

    return render(request, 'projects/projects-page.html', {
        'customStyles': ['css/projects/projects-page.css'],
        'pageTitle': 'Projects',
        'projectsList': projectsList
    })

@login_required(login_url='login-page')
def createEditProject(request, id):
    if request.user.role == 'manager':
        if id == 0:
            return render(request, 'projects/create-edit-project.html', {
                'pageTitle': 'Create Project',
                'edit': False,
                'project': None,
                'constants': constants
            })
        else:
            project = get_object_or_404(Project, id=id)

            return render(request, 'projects/create-edit-project.html', {
                'pageTitle': 'Edit Project',
                'edit': True,
                'project': project,
                'constants': constants
            })
    else:
        return render(request, '403.html', {
            'pageTitle': 'Restricted Access'
        })

@login_required(login_url='login-page')
def saveProject(request):
    if request.user.role == 'manager':
        requestID = request.POST.get('id', None)

        form = ProjectForm(request.POST, project_status=constants.PROJECT_STATUS)

        if form.is_valid():
            if requestID:
                # UPDATE
                rowsUpdated = Project.objects.filter(
                    id=requestID
                ).update(
                    name=form.cleaned_data['name'],
                    description=form.cleaned_data.get('description', ''),
                    location=form.cleaned_data.get('location', ''),
                    type=form.cleaned_data.get('type', ''),
                    start_date=form.cleaned_data.get('start_date', ''),
                    end_date=form.cleaned_data.get('end_date', ''),
                    status=form.cleaned_data.get('status', ''),
                    reason=form.cleaned_data.get('reason', '')
                )

                if rowsUpdated:
                    return JsonResponse({ "message": "SUCCESS" })
                else:
                    return JsonResponse({ "message": "ERROR_UPDATE" })
            else:
                # CREATE
                try:
                    newProject = Project.objects.create(
                        name=form.cleaned_data['name'],
                        description=form.cleaned_data.get('description', ''),
                        location=form.cleaned_data.get('location', ''),
                        type=form.cleaned_data.get('type', ''),
                        start_date=form.cleaned_data.get('start_date', ''),
                        end_date=form.cleaned_data.get('end_date', ''),
                        status=form.cleaned_data.get('status', 'pending') or 'pending',
                        reason=form.cleaned_data.get('reason', '')
                    )

                    return JsonResponse({ "message": "SUCCESS" })
                except Exception as e:
                    print("Error in creating a new project:", e)
                    return JsonResponse({ "message": "ERROR_CREATE" })
        else:
            return JsonResponse({
                "message": "INVALID_DATA",
                "errors": form.errors
            })
    else:
        return render('403.html', {
            'pageTitle': 'Restricted Access'
        })