from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib import messages
import calendar, datetime
import random

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .decorators import admin_only, check_if_logged_in

from .models import Event
from .models import UserProfile 
from .forms import DateForm, CreateUserForm

monthCount = 0
yearCount = 0

# Create your views here.
@login_required(login_url='events:login_page')
def index(request):
    global monthCount, yearCount
    monthAdd = 0
    if request.method == 'POST':
        if request.POST.get('next'):
            monthAdd = 1
        elif request.POST.get('prev'):
            monthAdd = -1
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
                user = event.event_user
                user_details = User.objects.get(username = user)
                event_list.append([event,event.pk,user_details])
            if len(event_list) != 0:
                c_list[temp_w_iter][temp_d_iter] = [day,event_list]
            else: c_list[temp_w_iter][temp_d_iter] = [day]
            temp_d_iter += 1
        temp_w_iter += 1
    del temp_d_iter, temp_w_iter
    today = timezone.now().day

    is_admin = 0
    if request.user.is_superuser:
        is_admin = 1

    context = {'c_list': c_list, 'year': timezone.now().year+yearCount, 'month': timezone.now().month+monthCount, 'today':today, 'is_admin': is_admin}
    return render(request, 'events/index.html', context)

@login_required(login_url='events:login_page')
def add(request):
    is_admin = 0
    if request.user.is_superuser:
        is_admin = 1

    context = {'form': DateForm(), 'is_admin': is_admin}
    return render(request, 'events/add.html', context)

@login_required(login_url='events:login_page')
def add_done(request):
    event = Event(event_name=request.POST['name'],event_date=request.POST['date'],event_desc=request.POST['description'],start_time=request.POST['start_time'],end_time=request.POST['end_time'], event_user = request.user)
    event.save()
    return HttpResponseRedirect(reverse('events:index'))

@login_required(login_url='events:login_page')
def day_events(request, year, month, day):
    time_events = []
    time = datetime.time(8, 0, 0)
    count_mins = 0
    count = 0
    print(time)
    while time < datetime.time(23, 0, 0):
        event_list = []
        event_set = Event.objects.filter(event_date__year=timezone.now().year + yearCount,
                                         event_date__month=timezone.now().month + monthCount, event_date__day=day,
                                         start_time=time)
        for event in event_set:
            user = event.event_user
            user_colour = User.objects.get(username = user)
            temptime = time
            time_slots = (event.end_time.hour - event.start_time.hour) * 2
            event_list.append([event, time_slots, user_colour])
        time_events.append([time, event_list])
        count_mins = count_mins + 30
        if count_mins == 60:
            count = count + 1
            count_mins = 0
        time = datetime.time(8+count, 0 + count_mins, 0)

    event = 0
    context = {'year': year, 'month': month, 'day': day, 'time_events': time_events}
    return render(request, 'events/day_event_layout.html', context)

@login_required(login_url='events:login_page')
def remove(request):
    events = Event.objects.all()

    context = {'events': events}
    return render(request, 'events/remove.html', context)

@login_required(login_url='events:login_page')
def remove_done(request):
    try:
        event = Event.objects.get(pk=request.POST['choice'])
        event.delete()
    except:
        print('Error in retrieving event!')

    return HttpResponseRedirect(reverse('events:index'))

@admin_only
@login_required(login_url='events:login_page')
def add_user(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user_saved = form.save()

            r = lambda: random.randint(0,255)
            code = ('#%02X%02X%02X' % (r(),r(),r()))
            
            user_profile = UserProfile(user = user_saved, hex_code = code)

            user_profile.save()
            
            messages.success(request, "Account created successfully!")

            return redirect('events:index')

    is_admin = 0
    if request.user.is_superuser:
        is_admin = 1

    context = {'form': form, 'is_admin': is_admin}
    return render(request, 'events/create_account.html', context)

@check_if_logged_in
def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('user')
        password = request.POST.get('pwd')

        user = authenticate(request, username=username, password=password)

        
        if user is not None:
            login(request, user)
            return redirect('events:index')
        else:
            messages.info(request, 'Username or Password incorrect!')

    context = {}
    return render(request,'events/login.html', context)

@login_required(login_url='events:login_page')
def logout_user(request):
    logout(request)
    return redirect('events:login_page')

@login_required(login_url='events:login_page')
def event_details(request,year,month,day,event):
    event = Event.objects.get(pk=event)
    user = event.event_user
    user_details = User.objects.get(username = user)

    can_change = 0
    if request.user.id == event.event_user.id or request.user.is_superuser:
        can_change = 1

    context = {'date':event.event_date, 'event':event, 'start':event.start_time, 'end':event.end_time, 'description':event.event_desc, 'user':user_details, 'can_change': can_change}
    return render(request, 'events/event_details.html',context)



    
