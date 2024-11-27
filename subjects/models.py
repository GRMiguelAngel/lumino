from django.conf import settings
from django.db import models

# Create your models here.


class Subject(models.Model):
    code = models.CharField(max_length=3, unique=True)
    name = models.CharField(max_length=250)
    students = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='students',
    )
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='teacher'
    )


class Lesson(models.Model):
    title = models.CharField(max_length=250)
    content = models.TextField(blank=True)
    subject = models.ForeignKey(
        'subjects.Subject', related_name='subject_lesson', on_delete=models.CASCADE
    )
