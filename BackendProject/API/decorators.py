from rest_framework.response import Response
from rest_framework import status

def students_only(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.user_type == "1":
            return view_func(request, *args, **kwargs)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)
    return wrapper_func


def examiners_only(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.user_type == "2":
            return view_func(request, *args, **kwargs)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)
    return wrapper_func