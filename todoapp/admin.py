from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *
# Register your models here.
class TaskAdmin(admin.ModelAdmin):
    filter_horizontal = ['completed']
admin.site.register(Task, TaskAdmin)

# class UserAdmin(admin.ModelAdmin):
#     list_display = ('username', 'first_name', 'last_name', 'email',) 

admin.site.register(User, UserAdmin)