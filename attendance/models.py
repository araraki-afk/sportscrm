from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
import uuid
from django.utils.timezone import now
import secrets
from django.db import models


class APIKey(models.Model):
    name = models.CharField(max_length=255, unique=True)  # Название ключа (например, "Мобильное приложение")
    key = models.CharField(max_length=64, unique=True, editable=False)  # Уникальный API-ключ
    created_at = models.DateTimeField(auto_now_add=True)  # Дата создания
    is_active = models.BooleanField(default=True)  # Возможность деактивации ключа

    def save(self, *args, **kwargs):
        if not self.key:  # Генерируем ключ только при первом создании
            self.key = secrets.token_hex(32)  # Генерация безопасного ключа
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({'Активен' if self.is_active else 'Отключен'})"


class CustomUser(AbstractUser):
    is_student = models.BooleanField(default=True)
    is_coach = models.BooleanField(default=False)

    groups = models.ManyToManyField(
        Group,
        related_name='customuser_set',
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_permissions_set',
        blank=True
    )

    def save(self, *args, **kwargs):
        # Если пользователь не является тренером, то он автоматически студент
        if not self.is_coach:
            self.is_student = True
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username


class Section(models.Model):
    name = models.CharField(max_length=100)
    coach = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, limit_choices_to={'is_coach': True})

    def __str__(self):
        return self.name


class SectionTime(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.section.name} ({self.start_time} - {self.end_time})"


class StudentSectionTime(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'is_student': True})
    section_time = models.ForeignKey(SectionTime, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.student.username} - {self.section_time}"


class QRCode(models.Model):
    section_time = models.ForeignKey(SectionTime, on_delete=models.CASCADE)
    qr_code = models.ImageField(upload_to='qr_codes/')
    valid_from = models.DateTimeField()
    valid_until = models.DateTimeField()

    def __str__(self):
        return f"QR для {self.section_time} с {self.valid_from} по {self.valid_until}"


class Attendance(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'is_student': True})
    section_time = models.ForeignKey(SectionTime, on_delete=models.CASCADE)
    qr_code = models.ForeignKey(QRCode, on_delete=models.SET_NULL, null=True)
    date_scanned = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.student.username} посетил {self.section_time} на {self.date_scanned}"
