from django.conf import settings
from django.db import models

# Create your models here.


class Profile(models.Model):
    class Role(models.TextChoices):
        TEACHER = 'T', 'Teacher'
        STUDENT = 'S', 'Student'

    role = models.CharField(
        max_length=1,
        choices=Role,
        default=Role.STUDENT,
    )

    bio = models.TextField(blank=True)
    avatar = models.ImageField(
        blank=True,
        null=True,
        upload_to='avatars',
        default='avatars/noavatar.png',
    )

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def is_teacher(self):
        return self.role == Profile.Role.TEACHER

    def is_student(self):
        return self.role == Profile.Role.STUDENT

    def __str__(self):
        return self.role
