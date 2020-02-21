from django.shortcuts import render
from django.utils import timezone
import calendar

# Create your views here.
def index(request):
    c = calendar.Calendar(calendar.MONDAY)
    c_list = c.monthdayscalendar(timezone.now().year, timezone.now().month)
    today = timezone.now().day

    context = {'c_list': c_list, 'year': timezone.now().year, 'month': timezone.now().month, 'today':today}
    return render(request, 'events/index.html', context)