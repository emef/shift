from django.contrib import admin
from shift.jobs.models import Job, Shift

class ShiftInline(admin.StackedInline):
    model = Shift
    extra = 3

class JobAdmin(admin.ModelAdmin):
    inlines = [ShiftInline]
    
admin.site.register(Job, JobAdmin)
