from django.urls import path
from . import views

urlpatterns = [
    path('', views.projectsMainPage, name='projects-page'),
    path('<int:id>/', views.createEditProject, name='create-edit-project'),
    path('save/', views.saveProject, name='save-project')
]