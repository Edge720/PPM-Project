from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from django.utils import timezone
import calendar

from .models import Event

# Create your views here.
def index(request):
    c = calendar.Calendar(calendar.MONDAY)
    c_list = c.monthdayscalendar(timezone.now().year, timezone.now().month)
    temp_w_iter = 0
    for week in c_list:
        temp_d_iter = 0
        for day in week:
            try:
                c_event = Event.objects.get(event_date__year=timezone.now().year, event_date__month=timezone.now().month, event_date__day=day)
            except:
                c_event = 0
            if c_event != 0:
                c_list[temp_w_iter][temp_d_iter] = [day, c_event]
            temp_d_iter += 1
        temp_w_iter += 1
    del temp_d_iter, temp_w_iter
    today = timezone.now().day

    context = {'c_list': c_list, 'year': timezone.now().year, 'month': timezone.now().month, 'today':today}
    return render(request, 'events/index.html', context)

def add(request):
    return render(request, 'events/add.html')

def add_done(request):
    try:
        event = Event(event_name=request.POST['name'],event_date=request.POST['date'])
        event.save()
    except:
        print("Didn't get data!")


    return HttpResponseRedirect(reverse('events:index'))