from django import forms
from .models import Attendance
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    """
    Форма для создания нового пользователя с использованием кастомной модели CustomUser.
    """
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']  # Поля для регистрации

    def __init__(self, *args, **kwargs):
        """
        Инициализация формы с добавлением пользовательских атрибутов.
        """
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Имя пользователя'})
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Электронная почта'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Пароль'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Подтвердите пароль'})


class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['student', 'section_time']  # Поля, которые должны быть в форме

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Настройка виджетов формы, если необходимо
        self.fields['student'].widget.attrs.update({'class': 'form-control'})
        self.fields['section_time'].widget.attrs.update({'class': 'form-control'})
