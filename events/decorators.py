from django.http import HttpResponse
from django.shortcuts import redirect

from events.models import Event


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

def admin_or_creator_only(view_func):
    def wrapper_func(request, year, month, day, event_id, *args, **kwargs):
        event = Event.objects.get(pk=event_id)
        if request.user.is_superuser or request.user.id == event.event_user.id:
            return view_func(request, year, month, day, event_id, *args, **kwargs)
        else:
            return HttpResponse('<script type="text/javascript">window.close();</script>')

    return wrapper_func

def admin_or_creator_only_review(view_func):
    def wrapper_func(request, event_id, *args, **kwargs):
        event = Event.objects.get(pk=event_id)
        if request.user.is_superuser or request.user.id == event.event_user.id:
            return view_func(request, event_id, *args, **kwargs)
        else:
            return HttpResponse('<script type="text/javascript">window.close();</script>')

    return wrapper_func
