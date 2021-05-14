from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse

def students_only(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.user_type == "1":
            return view_func(request, *args, **kwargs)
        elif request.user.is_anonymous:
            return JsonResponse({'detail': 'Authentication credentials were not provided.'}, status=401)
        else:
            return JsonResponse({'detail':'only students allowed'}, status=403)
    return wrapper_func


def examiners_only(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_anonymous:
            return JsonResponse({'detail': 'Authentication credentials were not provided.'}, status=401)
        elif request.user.user_type == "2":
            return view_func(request, *args, **kwargs)
        else:
            return JsonResponse({'error':'only examiners allowed'} ,status=403)
    return wrapper_func