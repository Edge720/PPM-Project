from django.urls import path

from . import views

app_name = 'events'
urlpatterns = [
    path('', views.index, name='index'),
    path('add/', views.add, name='add'),
    path('login/', views.login, name='login'),
    path('add/done/', views.add_done, name='add_done'),
    path('-1/<year>-<month>-<day>-<event>/', views.event_details, name='event_details'),
    path('1/<year>-<month>-<day>-<event>/', views.event_details, name='event_details'),
    path('<year>-<month>-<day>-<event>/', views.event_details, name='event_details'),
    path('-1/<year>-<month>-<day>/', views.day_events, name='day_events'),
    path('1/<year>-<month>-<day>/', views.day_events, name='day_events'),
    path('<year>-<month>-<day>/', views.day_events, name='day_events'),
    path('<monthAdd>/', views.index, name='newMonth'),
    path('-1/add/', views.add, name='add'),
    path('1/add/', views.add, name='add'),
    path('1/login/', views.login, name='login'),
    path('-1/login/', views.login, name='login'),
    path('-1/remove/', views.remove, name='remove'),
    path('1/remove/', views.remove, name='remove'),
    path('remove/', views.remove, name='remove')   
]
