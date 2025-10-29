import logging
from functools import wraps
from django.shortcuts import redirect
from asgiref.sync import async_to_sync

from utils.constants.base import AUTH_TOKEN
from communication.auth_service_request import get_data_from_nats


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


def inject_user_info(func):
    """
    Retrieves user info from NATS based on access_token in cookies,
    and injects it into kwargs as `user`.
    """

    @wraps(func)
    def wrapper(self, request, *args, **kwargs):
        # retrieve the access token stored in COOKIES
        access_token: str = request.COOKIES.get(AUTH_TOKEN)
        if not access_token:
            redirect('/')

        try:
            # call the async NATS handler to fetch the user_information against the access token
            user_info = async_to_sync(get_data_from_nats)({
                "access_token": access_token
            })
            kwargs["user"] = user_info
        except Exception as exp:
            logging.exception("Getting error during fetch user info from NAT, %s", str(exp))
            redirect('/')
        return func(self, request, *args, **kwargs)
    return wrapper
