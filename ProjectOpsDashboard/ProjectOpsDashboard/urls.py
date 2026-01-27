from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from accounts import views as accountsViews

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', accountsViews.loginPage, name='login-page'),
    path('signup/', accountsViews.signupPage, name='signup-page'),
    path('logout/', accountsViews.logoutUser, name='logout'),

    path('', include('dashboards.urls')),
    path('projects/', include('projects.urls'))
]
