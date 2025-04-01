from django.utils import timezone
import random
from django.conf import settings

class AnonymousUsernameMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated:
            if 'anonymous_name' not in request.session or timezone.now() > request.session.get('anonymous_name_expiry', timezone.now()):
                request.session['anonymous_name'] = random.choice(settings.ANONYMOUS_NAMES)
                request.session.set_expiry(42)
                request.session['anonymous_name_expiry'] = timezone.now() + timezone.timedelta(seconds=42)
        response = self.get_response(request)
        return response