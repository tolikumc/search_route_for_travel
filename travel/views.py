from .forms import UserLoginForm
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect


def login_view(request):
    form = UserLoginForm(request.POST)
    next = request.GET.get('next')
    if form.is_valid():
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username.strip(), password=password.strip())

        login(request, user)
        next_post = request.POST.get('next')
        redirect_path = next or next_post or '/'
        return redirect(redirect_path)
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('/')