from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Section, SectionTime, StudentSectionTime, QRCode, Attendance
from django.contrib.auth import get_user_model
from .forms import CustomUserCreationForm
import qrcode
from django.http import HttpResponse
from django.utils import timezone
from datetime import timedelta
import uuid

CustomUser = get_user_model()  # Получаем текущую модель пользователя


def register(request):
    """
    Регистрация нового пользователя с ролью "студент".
    """
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_student = True  # Устанавливаем роль "студент" по умолчанию
            user.save()
            return redirect('dashboard')
    else:
        form = CustomUserCreationForm()
    return render(request, 'attendance/register.html', {'form': form})


@login_required
def dashboard(request):
    """
    Главная страница (dashboard) для тренеров и студентов.
    """
    if request.user.is_coach:
        # Для тренера: секции, которые он ведет
        section_times = SectionTime.objects.filter(section__coach=request.user)
        return render(request, 'attendance/coach_dashboard.html', {'section_times': section_times})
    elif request.user.is_student:
        # Для студента: секции, на которые он записан
        student_sections = StudentSectionTime.objects.filter(student=request.user)
        section_times = [student_section.section_time for student_section in student_sections]
        return render(request, 'attendance/student_dashboard.html', {'section_times': section_times})
    else:
        return redirect('login')



@login_required
def generate_qr(request, section_time_id):
    """
    Генерация динамического QR-кода для секции, действующего в течение 10 секунд.
    """
    section_time = get_object_or_404(SectionTime, id=section_time_id)

    # Уникальный токен для QR-кода
    token = str(uuid.uuid4())
    valid_from = timezone.now()
    valid_until = valid_from + timedelta(seconds=10)

    # Генерация данных для QR-кода
    qr_data = f"https://example.com/scan_qr/{token}/{section_time.id}"  # Замените на ваш домен
    qr_img = qrcode.make(qr_data)

    # Сохранение QR-кода в базе данных
    QRCode.objects.create(
        section_time=section_time,
        valid_from=valid_from,
        valid_until=valid_until
    )

    # Отправка QR-кода в виде изображения
    response = HttpResponse(content_type="image/png")
    qr_img.save(response, "PNG")
    return response


@login_required
def scan_qr(request, token, section_time_id):
    """
    Сканирование QR-кода студентом для отметки посещаемости.
    """
    try:
        qr_code = QRCode.objects.get(
            section_time_id=section_time_id,
            valid_from__lte=timezone.now(),
            valid_until__gte=timezone.now()
        )
    except QRCode.DoesNotExist:
        return HttpResponse("QR-код недействителен или время его действия истекло")

    # Запись посещаемости
    Attendance.objects.create(
        student=request.user,
        section_time=qr_code.section_time,
        qr_code=qr_code
    )
    return redirect('dashboard')


@login_required
def section_detail(request, section_time_id):
    """
    Отображение информации о секции:
    - QR-код для посещаемости
    - Таблица с записями посещаемости.
    """
    section_time = get_object_or_404(SectionTime, id=section_time_id)

    if request.user.is_coach and section_time.section.coach == request.user:
        # Получаем записи посещаемости для секции
        attendance_records = Attendance.objects.filter(section_time=section_time).order_by('-date_scanned')

        return render(request, 'attendance/section_detail.html', {
            'section_time': section_time,
            'attendance_records': attendance_records
        })
    else:
        return redirect('dashboard')


@login_required
def register_section(request):
    """
    Регистрация студента на секцию.
    """
    if request.method == 'POST':
        section_time_id = request.POST.get('section_time')
        section_time = get_object_or_404(SectionTime, id=section_time_id)
        StudentSectionTime.objects.get_or_create(student=request.user, section_time=section_time)
        return redirect('dashboard')
    else:
        section_times = SectionTime.objects.all()
        return render(request, 'attendance/register_section.html', {'section_times': section_times})


@login_required
def coach_dashboard(request):
    """
    Отображение панели тренера, включающей секции и студентов.
    """
    if request.user.is_coach:
        # Секции, которые ведет тренер
        section_times = SectionTime.objects.filter(section__coach=request.user)

        # Список студентов, зарегистрированных на секции тренера
        student_section_times = StudentSectionTime.objects.filter(section_time__in=section_times)
        students = CustomUser.objects.filter(id__in=[sst.student.id for sst in student_section_times])

        return render(request, 'attendance/coach_dashboard.html', {
            'section_times': section_times,
            'students': students
        })
    else:
        return redirect('dashboard')


@login_required
def view_attendance(request):
    """
    Отображение посещаемости для текущего пользователя.
    """
    attendance_records = Attendance.objects.filter(student=request.user)
    return render(request, 'attendance/view_attendance.html', {'attendance_records': attendance_records})


@login_required
def scan_qr_page(request, section_time_id):
    """
    Страница для сканирования QR-кода студентом.
    """
    section_time = get_object_or_404(SectionTime, id=section_time_id)

    # Убедимся, что студент записан на эту секцию
    if not StudentSectionTime.objects.filter(student=request.user, section_time=section_time).exists():
        return HttpResponse("Вы не записаны на эту секцию.")

    return render(request, 'attendance/scan_qr_page.html', {
        'section_time': section_time
    })
