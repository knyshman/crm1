from django.contrib import admin
from .models import Company, CompanyEmail, CompanyManager, Phone, Project


class PhoneInline(admin.StackedInline):
    model = Phone


class CompanyEmailInline(admin.TabularInline):
    model = CompanyEmail


class CompanyManagerInline(admin.TabularInline):
    model = CompanyManager


class CompanyAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'address']
    fields = ['name', 'description', 'address']
    inlines = [CompanyManagerInline, PhoneInline, CompanyEmailInline]


admin.site.register(Company, CompanyAdmin)
admin.site.register(Project)