# Generated by Django 5.1.3 on 2024-11-20 15:33

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attendance',
            name='date',
        ),
        migrations.RemoveField(
            model_name='attendance',
            name='is_present',
        ),
        migrations.AddField(
            model_name='attendance',
            name='date_scanned',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.CreateModel(
            name='QRCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qr_code', models.ImageField(upload_to='qr_codes/')),
                ('valid_from', models.DateTimeField()),
                ('valid_until', models.DateTimeField()),
                ('section_time', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='attendance.sectiontime')),
            ],
        ),
        migrations.AddField(
            model_name='attendance',
            name='qr_code',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='attendance.qrcode'),
        ),
    ]
