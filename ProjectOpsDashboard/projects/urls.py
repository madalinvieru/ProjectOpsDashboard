from django.urls import path
from . import views

urlpatterns = [
    path('', views.projectsMainPage, name='projects-page'),

    path('create/', views.createProject, name='create-project'),
    path('edit/<int:id>/', views.editProject, name='edit-project'),
    path('save/', views.saveProject, name='save-project'),
    path('view/<int:id>', views.viewProject, name='view-project'),

    path('task/create/<int:projectID>/', views.createTask, name='create-task'),
    path('task/edit/', views.editTask, name='edit-task'),
    path('task/save/', views.saveTask, name='save-task')
]