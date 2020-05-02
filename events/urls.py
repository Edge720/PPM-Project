from django.urls import path
from django.views.generic import RedirectView

from . import views

app_name = 'events'
urlpatterns = [
    path('', views.index, name='index'),
    path('add/', views.add, name='add'),
    path('events/login/', views.loginPage, name='loginPage'),
    path('login/', views.loginPage, name='loginPage'),
    path('logout/', views.logoutUser, name='logoutUser'),
    path('add/done/', views.add_done, name='add_done'),
    path('<year>-<month>-<day>/<event>/', views.event_details, name='event_details'),
    path('<year>-<month>-<day>/', views.day_events, name='day_events'),
    path('remove/', views.remove, name='remove'),
    path('remove/done', views.remove_done, name='remove_done'),
    path('create-account/', views.create_account, name='create_account'),
    path('admin', RedirectView.as_view(pattern_name='admin:index'))
]
