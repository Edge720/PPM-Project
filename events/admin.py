from django.contrib import admin

from .models import Event, UserProfile, Review

# Register your models here.

admin.site.register(Event)
admin.site.register(Review)
admin.site.register(UserProfile)