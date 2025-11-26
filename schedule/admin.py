from django.contrib import admin
from .models import Category, SchedulePost

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')

class SchedulePostAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'title')
    list_display_links = ('id', 'user', 'title')

admin.site.register(Category, CategoryAdmin)
admin.site.register(SchedulePost, SchedulePostAdmin)