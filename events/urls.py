from django.urls import path
from django.views.generic import RedirectView

from . import views

app_name = 'events'
urlpatterns = [
    path('', views.index, name='index'),
    path('add/', views.add, name='add'),
    path('events/login/', views.login_page, name='login_page'),
    path('login/', views.login_page, name='login_page'),
    path('logout/', views.logout_user, name='logout_user'),
    path('add/done/', views.add_done, name='add_done'),
    path('<year>-<month>-<day>/<event>/', views.event_details, name='event_details'),
    path('<year>-<month>-<day>/', views.day_events, name='day_events'),
    path('remove/', views.remove, name='remove'),
    path('remove/done', views.remove_done, name='remove_done'),
    path('add-user/', views.add_user, name='add_user')

]
