# Generated by Django 5.1.3 on 2024-12-04 16:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('subjects', '0003_enrollment_alter_subject_students'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Enrollment',
        ),
    ]