from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Section, SectionTime, StudentSectionTime, Attendance, QRCode
from django.contrib import admin
from .models import APIKey


@admin.register(APIKey)
class APIKeyAdmin(admin.ModelAdmin):
    list_display = ('name', 'key', 'is_active', 'created_at')
    readonly_fields = ('key', 'created_at')  # Чтобы ключ нельзя было редактировать


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
admin.site.register(QRCode)
