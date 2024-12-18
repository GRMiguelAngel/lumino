from django.conf import settings
from django.db import models
from django.urls import reverse

# Create your models here.


class Subject(models.Model):
    code = models.CharField(max_length=3, unique=True)
    name = models.CharField(max_length=250)
    students = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='subjects.Enrollment',
        related_name='student_subjects',
    )
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='teacher_subjects',
    )

    def get_absolute_url(self):
        return reverse('subject:subject-detail', kwargs={'code': self.code})

    def __str__(self):
        return self.code


class Lesson(models.Model):
    title = models.CharField(max_length=250)
    content = models.TextField(blank=True)
    subject = models.ForeignKey(
        'subjects.Subject', related_name='subject_lesson', on_delete=models.CASCADE
    )

    def __str__(self):
        return self.title


class Enrollment(models.Model):
    enrolled_at = models.DateField(auto_now_add=True)
    mark = models.PositiveSmallIntegerField(null=True)
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='student_enrollment'
    )
    subject = models.ForeignKey(
        'subjects.Subject', related_name='enrollment', on_delete=models.CASCADE
    )
