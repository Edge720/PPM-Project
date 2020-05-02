from django.http import HttpResponse
from django.shortcuts import redirect

def check_if_logged_in(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('events:index')
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func

def admin_only(view_func):
    def wrapper_func(request, *args, **kwargs):
        if not request.user.is_superuser:
            return redirect('events:index')
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func
