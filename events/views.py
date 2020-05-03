from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib import messages
import calendar, datetime, random
from django.db.models import F
from django.core.mail import send_mail

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


from .decorators import admin_only, check_if_logged_in, admin_or_creator_only

from .models import Event, UserProfile, Review
from .forms import DateForm, CreateUserForm

# Create your views here.
@login_required(login_url='events:login_page')
def index(request):
    if 'monthCount' in request.session:
        monthCount = request.session['monthCount']
    else:
        monthCount = 0
        request.session['monthCount'] = monthCount

    if 'yearCount' in request.session:
        yearCount = request.session['yearCount']
    else:
        yearCount = 0
        request.session['yearCount'] = yearCount

    if request.method == 'POST':
        if request.POST.get('next'):
            monthCount += 1
            request.session['monthCount'] = request.session['monthCount'] + 1
        elif request.POST.get('prev'):
            monthCount -= 1
            request.session['monthCount'] = request.session['monthCount'] - 1
        else:
            monthCount = 0
            yearCount = 0
            request.session['monthCount'] = 0
            request.session['yearCount'] = 0
    if timezone.now().month+monthCount == 13 :
        monthCount = - timezone.now().month+1
        yearCount = yearCount + 1
    if timezone.now().month+monthCount == 0 :
        monthCount = 12 - timezone.now().month
        yearCount = yearCount - 1
    c = calendar.Calendar(calendar.MONDAY)
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
    current_month = timezone.now().month
    event_review_set = Event.objects.filter(event_date__range=["2011-01-01", timezone.now()], event_user = request.user, event_reviewed = False)
    event_reviews = []
    for event in event_review_set :
        event_reviews.append(event)
        print(event)

    event_review_set = Event.objects.filter(event_date__range=["2011-01-01", timezone.now()], event_user=request.user,
                                            event_reviewed=False)
    event_reviews = []
    for event in event_review_set:
        event_reviews.append(event)
        print(event)

    is_admin = 0
    if request.user.is_superuser:
        is_admin = 1

    context = {'c_list': c_list, 'year': timezone.now().year+yearCount, 'month': timezone.now().month+monthCount, 'today': today, 'current_month':current_month, 'is_admin': is_admin, 'event_review':event_reviews}
    return render(request, 'events/index.html', context)

@login_required(login_url='events:login_page')
def add(request):
    is_admin = 0
    if request.user.is_superuser:
        is_admin = 1

    users = UserProfile.objects.all()

    context = {'form': DateForm(), 'is_admin': is_admin, 'users': users}
    return render(request, 'events/add.html', context)

@login_required(login_url='events:login_page')
def add_done(request):
    if request.user.is_superuser:
        user = User.objects.get(pk=request.POST.get('users'))
    else:
        user = request.user
    event = Event(event_name=request.POST['name'],event_date=request.POST['date'],event_desc=request.POST['description'],start_time=request.POST['start_time'],end_time=request.POST['end_time'], event_location=request.POST['event_location'], event_user = user)
    event.save()

    email_message = "You have been assigned to an event: " + event.event_name + "\nDate: " + event.event_date + "\n" + event.start_time + "-" + event.end_time 

    account_email = user.email

    send_mail('Event Assigned', email_message , account_email, [account_email], fail_silently = False)

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

            email_message = 'Account successfully Created:' + user_saved.username

            account_email = user_saved.email

            send_mail('Account  Created', email_message, account_email, [account_email] ,fail_silently = False)

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
            today = datetime.date.today()
            week_ago = today - datetime.timedelta(days=7)
            email_message = 'Events Require Reviewing: '
            eventset = Event.objects.filter(event_user_id = user.id, event_reviewed = False, event_date__range=["2011-01-01", week_ago] )
            if eventset.count() != 0:
                for event in eventset:
                     email_message = email_message+ event.event_name + "\n"
                email_message = email_message + "These events are over a week old, please review them."
                account_email = user.email
                send_mail('Event Requires Reviewing', email_message, account_email, [account_email] ,fail_silently = False)
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
def event_details(request, year, month, day, event_id):
    event = Event.objects.get(pk=event_id)
    user = event.event_user
    review = None
    user_details = User.objects.get(username = user)
    if (event.event_reviewed == True):
        review = Review.objects.get(event_reviewed = event_id)
    can_change = 0
    if request.user.id == event.event_user.id or request.user.is_superuser:
        can_change = 1

    context = {'date':event.event_date, 'event':event, 'start':event.start_time, 'end':event.end_time, 'description':event.event_desc, 'user':user_details, 'can_change': can_change, 'year': year, 'month':month, 'day':day,'location':event.event_location, 'event_id':event_id,'review':review}
    return render(request, 'events/event_details.html',context)

@admin_or_creator_only
@login_required(login_url='events:login_page')
def event_edit(request, year, month, day, event_id):
    event = Event.objects.get(pk=event_id)

    is_admin = 0
    if request.user.is_superuser:
        is_admin = 1

    users = UserProfile.objects.all()

    start_time_hour = "%02d" % event.start_time.hour
    start_time_min = "%02d" % event.start_time.minute
    end_time_hour = "%02d" % event.end_time.hour
    end_time_min = "%02d" % event.end_time.minute

    context = {'year': year, 'month':month, 'day':day, 'event_id':event_id, 'event': event, 'is_admin': is_admin, 'users': users, 'start_time_hour':start_time_hour, 'end_time_hour': end_time_hour, 'start_time_min':start_time_min, 'end_time_min': end_time_min}
    return render(request, 'events/event_edit.html', context)

@admin_or_creator_only
@login_required(login_url='events:login_page')
def event_edit_done(request, year, month, day, event_id):
    try:
        event = Event.objects.get(pk=event_id)
    except:
        print('Error in retrieving event!')

    if request.user.is_superuser:
        user = User.objects.get(pk=request.POST.get('users'))
    else:
        user = request.user

    event.event_name = request.POST['name']
    event.event_user = user
    event.event_desc = request.POST['description']
    event.start_time = request.POST['start_time']
    event.end_time=request.POST['end_time']
    event.save()

    return redirect('events:event_details',year, month, day, event_id)

@admin_or_creator_only
@login_required(login_url='events:login_page')
def event_remove(request, year, month, day, event_id):
    try:
        event = Event.objects.get(pk=event_id)
    except:
        print('Error in retrieving event!')

    context = {'event_name': event.event_name, 'year': year, 'month':month, 'day':day, 'event_id':event_id}
    return render(request, 'events/remove.html', context)

@admin_or_creator_only
@login_required(login_url='events:login_page')
def event_remove_done(request, year, month, day, event_id):
    try:
        event = Event.objects.get(pk=event_id)
        event.delete()
    except:
        print('Error in retrieving event!')

    return HttpResponse('<script type="text/javascript">window.close();</script>')

@admin_or_creator_only
@login_required(login_url='events:login_page')
def review_events(request, event_id):
    event = Event.objects.get(pk=event_id)
    context = {'event':event}
    return render(request, 'events/review.html',context)

@admin_or_creator_only
@login_required(login_url='events:login_page')
def review_done(request,event_id):
    if (request.POST['attended'] == "on"):
        value = True
    else: value = False
    event = Event.objects.get(pk=event_id)
    event_review = Review(event_reviewed=event,review=request.POST['description'],attended=value,attendance=request.POST['quantity'],rating=request.POST['rating'])
    event_review.save()
    event.event_reviewed = True
    event.save()

    return HttpResponseRedirect(reverse('events:index'))



