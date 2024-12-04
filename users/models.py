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

    def __str__(self):
        return self.role
