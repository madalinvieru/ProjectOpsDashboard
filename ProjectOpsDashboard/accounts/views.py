from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from core import constants
from .models import User
from .forms import SignUpForm

def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
             
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)    # Adds the session in the database and the browser.
            return redirect('main-page')
        else:
            return render(request, 'authentication/login.html', {
                'customStyles': ['css/auth.css'],
                'message': 'Invalid username or password'
            })

    if request.method == 'GET':
        return render(request, 'authentication/login.html', {
            'customStyles': ['css/auth.css']
        })

def signupPage(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST, user_roles=constants.USER_ROLE)

        if form.is_valid():
            User.objects.create_user(
                last_name=form.cleaned_data.get('lastname', ''),
                first_name=form.cleaned_data.get('firstname', ''),  # Returns empty string if the field does not exist.
                username=form.cleaned_data['username'], # Used with dictionary indexing (throws error if not exists).
                email=form.cleaned_data.get('email'),   # 'Get' returns 'None' if the field does not exist (optional field).
                password=form.cleaned_data['password'],
                role=form.cleaned_data['role']
            )
            return redirect('login-page')
        else:
            return render(request, 'authentication/signup.html', {
                'customStyles': ['css/auth.css'],
                'userRoles': constants.USER_ROLE,
                'errors': form.errors
            })

    if request.method == 'GET':
        return render(request, 'authentication/signup.html', {
            'customStyles': ['css/auth.css'],
            'userRoles': constants.USER_ROLE
        })

def logoutUser(request):
    logout(request)
    return redirect('login-page')