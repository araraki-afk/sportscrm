from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Section, SectionTime, StudentSectionTime, Attendance


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('is_student', 'is_coach')}),
    )
    list_display = ['username', 'is_student', 'is_coach']


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Section)
admin.site.register(SectionTime)
admin.site.register(StudentSectionTime)
admin.site.register(Attendance)
