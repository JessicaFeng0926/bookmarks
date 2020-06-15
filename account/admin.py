from django.contrib import admin

from .models import Profile
# Register your models here.

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    '''这是用户档案的管理类'''
    list_display = ['user','date_of_birth','photo']

