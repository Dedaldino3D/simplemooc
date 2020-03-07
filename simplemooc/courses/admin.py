from django.contrib import admin

from .models import Course, Comment, Announcement


# Register your models here.

class CourseAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'start_date', 'created_at']
    search_fields = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Course, CourseAdmin)
admin.site.register(Comment)
admin.site.register(Announcement)
