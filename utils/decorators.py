from functools import wraps
from django.shortcuts import redirect


def login_required(func):
    """
    This decorator will function ensure that, if the user logged_in then it will go to the respected view,
    otherwise redirect to the index/home page
    """

    @wraps(func)
    def wrapper(self, request, *args, **kwargs):
        logged_in = request.logged_in
        if not logged_in:
            return redirect('/')
        else:
            return func(self, request, *args, **kwargs)
    return wrapper
