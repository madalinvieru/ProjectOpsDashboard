from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required(login_url='login-page')
def mainPage(request):
    currentUser = request.user

    if currentUser.role == 'manager':
        return render(request, 'dashboard/manager-page.html', {
            'pageTitle': 'Manager Dashboard'
        })
    else:
        return render(request, 'dashboard/member-page.html', {
            'pageTitle': 'Member Dashboard'
        })