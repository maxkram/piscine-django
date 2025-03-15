from django.shortcuts import render
from django.conf import settings
import random
from datetime import datetime, timedelta

def home(request):
    # Check if session has a name and expiry
    current_name = request.session.get('random_name')
    expiry_time = request.session.get('name_expiry')

    if not current_name or not expiry_time or datetime.now() > datetime.fromisoformat(expiry_time):
        # Assign new random name and set expiry
        current_name = random.choice(settings.RANDOM_NAMES)
        expiry_time = datetime.now() + timedelta(seconds=settings.NAME_EXPIRY_SECONDS)
        request.session['random_name'] = current_name
        request.session['name_expiry'] = expiry_time.isoformat()

    context = {'user_name': current_name}
    return render(request, 'ex00/home.html', context)