from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect
from .views import CustomLoginView

urlpatterns = [
    # Перенаправление на страницу входа
    path('', lambda request: redirect('login'), name='home'),

    # Аутентификация
path('login/', CustomLoginView.as_view(template_name='attendance/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', views.register, name='register'),

    # Главная страница
    path('dashboard/', views.dashboard, name='dashboard'),

    # Секции и посещаемость
    path('register-section/', views.register_section, name='register_section'),
    path('section/<int:section_time_id>/', views.section_detail, name='section_detail'),
    path('generate-qrcode/<int:section_time_id>/', views.generate_qr, name='generate_qr'),
    path('scan-qrcode/<str:token>/<int:section_time_id>/', views.scan_qr, name='scan_qr'),
    path('view-attendance/', views.view_attendance, name='view_attendance'),

# Сканирование QR-кода студентом
    path('scan-qr-page/<int:section_time_id>/', views.scan_qr_page, name='scan_qr_page'),

    # Дополнительно для тренеров
    path('coach-dashboard/', views.coach_dashboard, name='coach_dashboard'),
]
