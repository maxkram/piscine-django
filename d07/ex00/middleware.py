import random
from django.utils import timezone
from django.conf import settings

class AnonymousSessionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if 'username' not in request.session or 'username_expires' not in request.session:
            # Assign a new random username
            request.session['username'] = random.choice(settings.RANDOM_NAMES)
            request.session['username_expires'] = timezone.now().timestamp() + 42

        # Check if the username has expired
        if timezone.now().timestamp() > request.session['username_expires']:
            request.session['username'] = random.choice(settings.RANDOM_NAMES)
            request.session['username_expires'] = timezone.now().timestamp() + 42

        response = self.get_response(request)
        return response