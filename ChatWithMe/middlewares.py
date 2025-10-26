import time
from django.shortcuts import redirect


class SessionTimeoutMiddleware:
    """
    Middleware to expire session data after 10 minutes (600 seconds).
    If expired, user is redirected to /login.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        session_key = 'authToken'

        session_data = request.session.get(session_key)

        if session_data:
            timestamp = session_data.get('timestamp')

            # check if timestamp exists and is valid
            if timestamp and (time.time() - timestamp > 600):
                # Expired: remove key and redirect
                del request.session[session_key]
                request.logged_in = False
            else:
                request.logged_in = True
        else:
            request.logged_in = False
        response = self.get_response(request)
        return response
