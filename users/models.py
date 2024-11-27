from django.conf import settings
from django.db import models

# Create your models here.


class Enrollment(models.Model):
    enrolled_at = models.DateField(auto_now_add=True)
    mark = models.IntegerField(blank=True)
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='student'
    )
    subject = models.ForeignKey(
        'subjects.Subject', related_name='subject', on_delete=models.CASCADE
    )


class Profile(models.Model):
    TEACHER = 'T'
    STUDENT = 'S'
    ROLE_CHOICES = {
        TEACHER: 'Teacher',
        STUDENT: 'Student',
    }

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user'
    )
    role = models.CharField(
        max_length=1,
        choices=ROLE_CHOICES,
        default=STUDENT,
    )
    bio = models.TextField(blank=True)
    avatar = models.ImageField(
        blank=True,
        null=True,
        upload_to='avatars',
        default='avatars/noavatar.png',
    )
