from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.views.decorators.csrf import csrf_exempt

def account_view(request):
    if request.user.is_authenticated:
        return render(request, 'account/logged_in.html', {'user': request.user})
    return render(request, 'account/login.html', {'form': AuthenticationForm()})

@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({'status': 'success', 'username': user.username})
        return JsonResponse({'status': 'error', 'errors': 'Invalid credentials'})
    return JsonResponse({'status': 'error', 'errors': 'Invalid request'})

@csrf_exempt
def logout_view(request):
    if request.method == 'POST' and request.user.is_authenticated:
        logout(request)
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'})