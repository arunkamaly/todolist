from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from userauth.forms import LoginForm, RegistrationForm
from home.forms import TodoForm
import pdb

def login_view(request):
    if request.method == 'POST':
        # pdb.set_trace()
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=request.POST['username'],
                password=request.POST['password']
            )
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('home:index')
        else:
            return render(request, 'userauth/login.html', {'form': form})
    else:
        return render(request, 'userauth/login.html', {'form': LoginForm()})

    return redirect('home:index')


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            try:
                User.objects.create_user(
                    username=request.POST['username'],
                    email=request.POST['email'],
                    password=request.POST['password']
                )
                return redirect('userauth:login')
            except:
                return render(request, 'userauth/register.html', {'form': form})
        else:
            return render(request, 'userauth/register.html', {'form': form})
    else:
        return render(
            request, 'userauth/register.html', {'form': RegistrationForm()}
        )


def logout_view(request):
    logout(request)
    return redirect('home:index')
