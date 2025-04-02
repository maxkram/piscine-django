from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from .forms import CustomUserCreationForm, CustomAuthenticationForm, TipForm
from .models import Tip, Vote

def index(request):
    tips = Tip.objects.all().order_by('-date')
    user_votes = {}
    if request.user.is_authenticated:
        user_votes = {vote.tip.id: vote.vote_type for vote in Vote.objects.filter(user=request.user)}
    return render(request, 'home.html', {'tips': tips, 'user_votes': user_votes})

def register(request):
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
        else:
            return render(request, 'register.html', {'form': form})
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('index')
        else:
            return render(request, 'login.html', {'form': form})
    else:
        form = CustomAuthenticationForm()
    return render(request, 'login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('index')

@login_required
def create_tip(request):
    if request.method == 'POST':
        form = TipForm(request.POST)
        if form.is_valid():
            tip = form.save(commit=False)
            tip.author = request.user
            tip.save()
            return redirect('index')
    else:
        form = TipForm()
    return render(request, 'create_tip.html', {'form': form})

@login_required
def vote(request, tip_id, vote_type):
    tip = get_object_or_404(Tip, id=tip_id)
    if vote_type == 'downvote' and tip.author != request.user and not request.user.has_perm('myapp.downvote_tip'):
        raise PermissionDenied("You don't have permission to downvote this tip.")
    existing_vote = Vote.objects.filter(tip=tip, user=request.user).first()
    if existing_vote:
        if existing_vote.vote_type == vote_type:
            existing_vote.delete()
        else:
            existing_vote.vote_type = vote_type
            existing_vote.save()
    else:
        Vote.objects.create(tip=tip, user=request.user, vote_type=vote_type)
    return redirect('index')

@login_required
def can_delete_tip(request, tip_id):
    tip = get_object_or_404(Tip, id=tip_id)
    if tip.author == request.user or request.user.has_perm('myapp.can_delete_tip'):
        tip.delete()
    else:
        raise PermissionDenied("You don't have permission to delete this tip.")
    return redirect('index')