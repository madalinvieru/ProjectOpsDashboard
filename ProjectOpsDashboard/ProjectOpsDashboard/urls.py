from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from accounts import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.loginPage, name='login-page'),
    path('signup/', views.signupPage, name='signup-page'),
    path('logout/', views.logoutUser, name='logout'),
    path('', include('dashboards.urls'))
]
