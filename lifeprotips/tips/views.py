from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from .forms import RegistrationForm, LoginForm
from django.conf import settings
import random
import time

def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegistrationForm()
    return render(request, 'tips/register.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.user
            login(request, user)
            return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'tips/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

def home(request):
    if request.user.is_authenticated:
        username = request.user.username
    elif not request.session.get('username') or time.time() > request.session.get('expiry', 0):
        request.session['username'] = random.choice(settings.RANDOM_NAMES)
        request.session['expiry'] = time.time() + 42
        username = request.session['username']
    else:
        username = request.session['username']
    return render(request, 'tips/home.html', {'username': username})