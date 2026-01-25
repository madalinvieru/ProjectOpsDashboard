from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .models import User

def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
             
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('main-page')
        else:
            return render(request, 'authentication/login.html', {
                'customStyles': ['auth.css'],
                'message': 'Invalid username or password'
            })

    if request.method == 'GET':
        return render(request, 'authentication/login.html', {
            'customStyles': ['auth.css']
        })