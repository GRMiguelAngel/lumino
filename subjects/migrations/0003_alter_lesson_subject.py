# Generated by Django 5.1.3 on 2025-01-13 18:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subjects', '0002_alter_enrollment_student'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lessons', to='subjects.subject'),
        ),
    ]
