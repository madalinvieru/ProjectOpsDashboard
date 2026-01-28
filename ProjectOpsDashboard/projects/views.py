from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Project, Task
from core import constants
from .forms import ProjectForm, TaskForm
from accounts.models import User

# ======== PROJECTS ========

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
def createProject(request):
    if request.user.role == 'manager':
        return render(request, 'projects/create-edit-project.html', {
            'pageTitle': 'Create Project',
            'edit': False,
            'project': None,
            'constants': constants
        })
    else:
        return render(request, '403.html', {
            'pageTitle': 'Restricted Access'
        })

@login_required(login_url='login-page')
def editProject(request, id):
    if request.user.role == 'manager':
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
                        reason=form.cleaned_data.get('reason', ''),
                        created_by=request.user
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
        return render(request, '403.html', {
            'pageTitle': 'Restricted Access'
        })

@login_required(login_url='login-page')
def viewProject(request, id):
    if request.user.role == 'member':
        # Test if the member has access to the project (at least one task assigned to him).
        allowed = Project.objects.filter(
            id=id,
            tasks__assigned_to=request.user
        ).exists()

        if not allowed:
            return render(request, '403.html', {
                'pageTitle': 'Restricted Access'
            })
        
    # Get the project.
    project = get_object_or_404(Project, id=id)

    # Get the project's tasks.
    tasks = Task.objects.filter(project_id=id)

    return render(request, 'projects/view-project.html', {
        'customStyles': ['css/projects/projects-page.css'],
        'pageTitle': 'View Project',
        'project': project,
        'tasks': tasks
    })

# ======== TASKS ========

@login_required(login_url='login-page')
def createTask(request, projectID):
    project = get_object_or_404(Project, id=projectID)

    if request.user.role == 'member':
        # Test if the user has access on the project.
        if not project.tasks.filter(
            assigned_to=request.user
        ).exists():
            return render(request, '403.html', {
                'pageTitle': 'Restricted Access'
            })
    
    users = User.objects.all()

    return render(request, 'tasks/create-edit-task.html', {
        'pageTitle': 'Create Task',
        'edit': False,
        'task': None,
        'constants': constants,
        'projectID': projectID,
        'users': users
    })

@login_required(login_url='login-page')
def editTask(request, id):
    task = get_object_or_404(Task, id=id)

    if request.user.role == 'member':
        # Test if the user has access on the task to edit it.
        if not task.assigned_to != request.user:
            return render(request, '403.html', {
                'pageTitle': 'Restricted Access'
            })
    
    users = User.objects.all()

    return render(request, 'tasks/create-edit-task.html', {
        'pageTitle': 'Edit Task',
        'edit': True,
        'task': task,
        'constants': constants,
        'projectID': task.project.id,
        'users': users
    })

@login_required(login_url='login-page')
def saveTask(request):
    taskID = request.POST.get('id', None)

    form = TaskForm(request.POST, task_status=constants.TASK_STATUS, task_priority=constants.TASK_PRIORITY)

    if form.is_valid():
        if taskID:
            try:
                # UPDATE
                rowsUpdated = Task.objects.filter(
                    id=taskID
                ).update(
                    title=form.cleaned_data['title'],
                    description=form.cleaned_data.get('description'),
                    project_id=request.POST.get('projectID'),
                    assigned_to_id=form.cleaned_data.get('assigned_to').id if form.cleaned_data.get('assigned_to') else None,
                    start_date=form.cleaned_data.get('start_date'),
                    end_date=form.cleaned_data.get('end_date'),
                    status=form.cleaned_data.get('status'),
                    priority=form.cleaned_data.get('priority'),
                    parent_id=form.cleaned_data.get('parent')
                )

                updateProjectStatus(request.POST.get('projectID'))

                if rowsUpdated:
                    return JsonResponse({ "message": "SUCCESS" })
                else:
                    return JsonResponse({ "message": "ERROR_UPDATE" })
            except Exception as e:
                print("Error in editing an existing task:", e)
                return JsonResponse({ "message": "ERROR_UPDATE" })
        else:
            # CREATE
            try:
                newTask = Task.objects.create(
                    title=form.cleaned_data['title'],
                    description=form.cleaned_data.get('description'),
                    project_id=request.POST.get('projectID'),
                    assigned_to=form.cleaned_data.get('assigned_to'),
                    start_date=form.cleaned_data.get('start_date'),
                    end_date=form.cleaned_data.get('end_date'),
                    status=form.cleaned_data.get('status') or 'pending',
                    priority=form.cleaned_data.get('priority') or 'none',
                    parent_id=form.cleaned_data.get('parent'),
                    created_by=request.user
                )

                updateProjectStatus(request.POST.get('projectID'))

                return JsonResponse({ "message": "SUCCESS" })
            except Exception as e:
                print("Error in creating a new task:", e)
                return JsonResponse({ "message": "ERROR_CREATE" })
    else:
        return JsonResponse({
            "message": "INVALID_DATA",
            "errors": form.errors
        })

def updateProjectStatus(project_id):
    try:
        project = Project.objects.get(id=project_id)
        
        # Get all top-level tasks (tasks without parent).
        tasks = project.tasks.filter(parent__isnull=True)
        
        if not tasks.exists():
            # Keep the current status of the project.
            return
        
        # Check if all tasks are completed.
        allCompleted = all(task.is_completed() for task in tasks)
        
        if allCompleted:
            project.status = 'finished'
        else:
            # Don't override 'blocked' or 'rejected' statuses.
            if project.status in ['pending', 'finished']:
                project.status = 'in_progress'
        
        project.save()
        
    except Project.DoesNotExist:
        print(f"Project with ID {project_id} does not exist")
    except Exception as e:
        print(f"Error updating project status: {e}")