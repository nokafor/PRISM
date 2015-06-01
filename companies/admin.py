from django.contrib import admin

from companies.models import Company, Member, Admin, Cast, Rehearsal, Choreographer
from profiles.models import Conflict

def unschedule_rehearsals(modeladmin, request, queryset):
    queryset.update(is_scheduled=False)
unschedule_rehearsals.short_description = "Unschedule Rehearsals"

def unschedule_casts(modeladmin, request, queryset):
    queryset.update(is_scheduled=False)
    queryset.update(rehearsal=None)
unschedule_casts.short_description = "Unschedule Casts"

# Register your models here.
class CompanyInline(admin.TabularInline):
    model = Member.company.through

class AdminInline(admin.TabularInline):
	model = Admin
	extra = 2

class ConflictInline(admin.TabularInline):
	model = Conflict
	extra = 2

class MemberAdmin(admin.ModelAdmin):
    search_fields=['first_name', 'last_name', 'netid']
    inlines = [CompanyInline, AdminInline, ConflictInline]
    list_filter = ['company']

class RehearsalAdmin(admin.ModelAdmin):
	list_display = ['day_of_week', 'start_time', 'place', 'is_scheduled']
	ordering = ['company', 'day_of_week', 'start_time']
	list_filter = ['company']
	actions = [unschedule_rehearsals]

class CastAdmin(admin.ModelAdmin):
	list_display = ['name', 'rehearsal', 'is_scheduled']
	ordering = ['company', 'name']
	list_filter = ['company']
	actions = [unschedule_casts]

admin.site.register(Company)
admin.site.register(Rehearsal, RehearsalAdmin)
admin.site.register(Cast, CastAdmin)
admin.site.register(Choreographer)
admin.site.register(Member, MemberAdmin)