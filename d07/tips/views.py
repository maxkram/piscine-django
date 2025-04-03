from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.conf import settings
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm, LoginForm, TipForm
from .models import Tip
from accounts.models import CustomUser
import random

def home(request):
    if request.user.is_authenticated:
        username = request.user.username
        if request.method == 'POST':
            form = TipForm(request.POST)
            if form.is_valid():
                tip = form.save(commit=False)
                tip.author = request.user
                tip.save()  # This will trigger reputation update
                return redirect('home')
        else:
            form = TipForm()
    else:
        if 'anonymous_name' not in request.session or request.session.get_expiry_age() <= 0:
            request.session['anonymous_name'] = random.choice(settings.ANONYMOUS_NAMES)
            request.session.set_expiry(42)
        username = request.session['anonymous_name']
        form = None

    tips = Tip.objects.all().order_by('-created_at')
    context = {
        'username': username,
        'form': form,
        'tips': tips
    }
    return render(request, 'home.html', context)

@login_required
def upvote_tip(request, tip_id):
    tip = Tip.objects.get(id=tip_id)
    if request.user in tip.downvotes.all():
        tip.downvotes.remove(request.user)
    if request.user in tip.upvotes.all():
        tip.upvotes.remove(request.user)
    else:
        tip.upvotes.add(request.user)
    tip.save()  # Trigger reputation update
    return redirect('home')

@login_required
def downvote_tip(request, tip_id):
    tip = Tip.objects.get(id=tip_id)
    if request.user == tip.author or request.user.has_perm('tips.can_downvote_tips'):
        if request.user in tip.upvotes.all():
            tip.upvotes.remove(request.user)
        if request.user in tip.downvotes.all():
            tip.downvotes.remove(request.user)
        else:
            tip.downvotes.add(request.user)
        tip.save()  # Trigger reputation update
    return redirect('home')

@login_required
def delete_tip(request, tip_id):
    tip = Tip.objects.get(id=tip_id)
    if request.user == tip.author or request.user.has_perm('tips.can_delete_tips'):
        tip.delete()  # This will trigger reputation update
    return redirect('home')

# Update forms to use CustomUser
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
    
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect('home')
    else:
        form = LoginForm()
    
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')