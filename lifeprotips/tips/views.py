from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User  # Add this import
from django.conf import settings
import random
from datetime import datetime, timedelta
from .forms import RegistrationForm, LoginForm

def home(request):
    if not request.user.is_authenticated:
        if 'username' not in request.session or 'name_time' not in request.session or \
           datetime.now() > datetime.fromisoformat(request.session['name_time']) + timedelta(seconds=42):
            request.session['username'] = random.choice(settings.RANDOM_NAMES)
            request.session['name_time'] = datetime.now().isoformat()
        username = request.session['username']
    else:
        username = request.user.username
    return render(request, 'tips/home.html', {'username': username})

def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
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
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                form.add_error(None, "Invalid username or password.")
    else:
        form = LoginForm()
    return render(request, 'tips/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('home')