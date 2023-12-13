from django.contrib import admin
from .models import *

# Register your models here.

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
	list_display = ('id', 'user')

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id','title','is_active')
    readonly_fields = ('slug',)

@admin.register(ContactProfile)
class ContactAdmin(admin.ModelAdmin):
	list_display = ('id', 'timestamp', 'name',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'content',)