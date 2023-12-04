from django.contrib import admin

from .models import Video,Subscriber,Comment

admin.site.register(Video)
admin.site.register(Subscriber)
admin.site.register(Comment)