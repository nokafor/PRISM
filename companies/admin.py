from django.contrib import admin

from companies.models import Company, Member, Admin
from profiles.models import Conflict

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

admin.site.register(Company)
admin.site.register(Member, MemberAdmin)