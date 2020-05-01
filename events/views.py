from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from django.utils import timezone
import calendar

from .models import Event
from .forms import DateForm

monthCount = 0
yearCount = 0

# Create your views here.
def index(request,monthAdd = 0):
    global monthCount,yearCount
    monthCount = monthCount + int(monthAdd)
    c = calendar.Calendar(calendar.MONDAY)
    if int(monthAdd) == 0:
        monthCount = 0
        yearCount = 0
    if timezone.now().month+monthCount == 13 :
        monthCount = - timezone.now().month+1
        yearCount = yearCount + 1
    if timezone.now().month+monthCount == 0 :
        monthCount = 12 - timezone.now().month
        yearCount = yearCount - 1
    c_list = c.monthdayscalendar(timezone.now().year+yearCount, timezone.now().month+monthCount)
    temp_w_iter = 0
    for week in c_list:
        temp_d_iter = 0
        for day in week:
            try:
                c_event = Event.objects.get(event_date__year=timezone.now().year+yearCount, event_date__month=timezone.now().month+monthCount, event_date__day=day)
            except:
                c_event = 0
            if c_event != 0:
                c_list[temp_w_iter][temp_d_iter] = [day,c_event]
            else: c_list[temp_w_iter][temp_d_iter] = [day]
            temp_d_iter += 1
        temp_w_iter += 1
    del temp_d_iter, temp_w_iter
    today = timezone.now().day   
    context = {'c_list': c_list, 'year': timezone.now().year+yearCount, 'month': timezone.now().month+monthCount, 'today':today}
    return render(request, 'events/index.html', context)

def add(request):
    form = DateForm()
    return render(request, 'events/add.html',{'form': form})

def add_done(request):
    print(request.POST['name'])
    new_name = request.POST['name']
    datetime_object = request.POST['date']
    
    print(datetime_object)
    event = Event(event_name=new_name,event_date="08-05-2020")
    event.save()
    return HttpResponseRedirect(reverse('events:index'))

def day_events(request):
    return render(request, 'events/Day.html')
