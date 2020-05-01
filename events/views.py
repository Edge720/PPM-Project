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
    int_month = int(monthAdd)
    monthCount = monthCount + int_month
    c = calendar.Calendar(calendar.MONDAY)
    if int_month == 0:
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
            event_list = []
            event_set = Event.objects.filter(event_date__year=timezone.now().year+yearCount, event_date__month=timezone.now().month+monthCount, event_date__day=day)
            for event in event_set:
                event_list.append(event)
                print(event)
            if len(event_list) != 0:
                c_list[temp_w_iter][temp_d_iter] = [day,event_list]
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
    event = Event(event_name=request.POST['name'],event_date=request.POST['date'])
    event.save()
    return HttpResponseRedirect(reverse('events:index'))

def day_events(request, year, month, day):
    try:
        event = Event.objects.get(event_dateyear=timezone.now().year + yearCount,event_datemonth=timezone.now().month + monthCount, event_date__day=day) #,start_time=request.POST['start_time'],end_time=request.POST['end_time']
    except:
        event = 0
    context={'year':year, 'month':month, 'day':day, 'event':event}
    return render(request, 'events/day_events.html', context)


def remove(request):
    events = Event.objects.all()

    context = {'events':events}
    return render(request, 'events/remove.html', context)

def remove_done(request):
    try:
        event = Event.objects.get(pk=request.POST['choice'])
        event.delete()
    except:
        print('Error in retrieving event!')

    return HttpResponseRedirect(reverse('events:index'))


def login(request,email ="",password = ""):
    return render(request,'events/login.html')



    
