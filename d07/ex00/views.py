from django.shortcuts import render

def home(request):
    username = request.session.get('username', 'Guest')
    return render(request, 'home.html', {'username': username})