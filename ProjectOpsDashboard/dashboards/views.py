from django.shortcuts import render

users = ['manager', 'member']

def mainPage(request):
    currentUser = users[0]

    if currentUser == 'manager':
        return render(request, 'dashboard/manager-page.html', {
            'pageTitle': 'Manager Dashboard'
        })
    else:
        return render(request, 'dashboard/member-page.html')