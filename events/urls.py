from django.urls import path

from . import views

app_name = 'events'
urlpatterns = [
    path('', views.index, name='index'),
    path('add/', views.add, name='add'),
    path('add/done/', views.add_done, name='add_done'),
    path('day/', views.day, name='Day'),
    path('<monthAdd>/', views.index, name='newMonth'),
    path('-1/add/', views.add, name='add'),
    path('1/add/', views.add, name='add')
]
