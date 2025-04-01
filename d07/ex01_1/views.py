from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .forms import RegistrationForm, LoginForm
import time
import random

def home(request):
    username = request.session.get('username')
    timestamp = request.session.get('timestamp', 0)
    current_time = time.time()

    if request.user.is_authenticated:
        username = request.user.username
    elif not username or (current_time - timestamp) > settings.NAME_VALIDITY_DURATION:
        username = random.choice(settings.RANDOM_NAMES)
        request.session['username'] = username
        request.session['timestamp'] = current_time

    return render(request, 'tips/home.html', {'username': username})

def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegistrationForm()
    return render(request, 'tips/register.html', {'form': form})

def user_login(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], 
                              password=form.cleaned_data['password'])
            if user:
                login(request, user)
                return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'tips/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('home')