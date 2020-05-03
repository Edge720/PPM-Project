"""PPM_Project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', RedirectView.as_view(pattern_name='events:index')),
    path('events/', include('events.urls')),
    path('admin/', admin.site.urls),
    path('reset-password', auth_views.PasswordResetView.as_view(template_name='events/password_reset.html'), name='reset_password'),
    path('reset-password/done', auth_views.PasswordResetDoneView.as_view(template_name='events/password_reset_sent.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='events/password_reset_form.html'), name='password_reset_confirm'),
    path('reset-password/complete', auth_views.PasswordResetCompleteView.as_view(template_name='events/password_reset_done.html'), name='password_reset_complete')
]
