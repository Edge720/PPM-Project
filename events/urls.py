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
    path('<year>-<month>-<day>/', views.day_events, name='day_events'),
    path('<year>-<month>-<day>/<event_id>/', views.event_details, name='event_details'),
    path('<year>-<month>-<day>/<event_id>/edit', views.event_edit, name='event_edit'),
    path('<year>-<month>-<day>/<event_id>/edit/done', views.event_edit_done, name='event_edit_done'),
    path('<year>-<month>-<day>/<event_id>/remove', views.event_remove, name='event_remove'),
    path('<year>-<month>-<day>/<event_id>/remove/done', views.event_remove_done, name='event_remove_done'),
    path('add-user/', views.add_user, name='add_user'),
    path('review/<event_id>', views.review_events, name='review_events'),
    path('review/done/<event_id>', views.review_done, name='review_done')

]
