from django.contrib import admin
from main import models


@admin.register(models.Request)
class RequestAdmin(admin.ModelAdmin):
	list_display = ('query', )

@admin.register(models.Video)
class VideoAdmin(admin.ModelAdmin):
	list_display = ('vid_id', 'name', 'link', 'iframe', 'date')

@admin.register(models.UserLikedList)
class UserLikedListAdmin(admin.ModelAdmin):
	list_display = ('user', 'video')

@admin.register(models.RequestVideo)
class RequestVideoAdmin(admin.ModelAdmin):
	list_display = ('request', 'video')