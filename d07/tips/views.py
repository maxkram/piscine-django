from django.shortcuts import render
from django.conf import settings
import random

def home(request):
    # Check if anonymous_name exists and is still valid
    if 'anonymous_name' not in request.session or request.session.get_expiry_age() <= 0:
        # Set new random name with 42-second expiry
        request.session['anonymous_name'] = random.choice(settings.ANONYMOUS_NAMES)
        request.session.set_expiry(42)
    
    context = {
        'username': request.session['anonymous_name']
    }
    return render(request, 'home.html', context)