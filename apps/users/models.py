from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class Organisation(models.Model):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        related_name='children',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    lavozim = models.CharField(max_length=255, blank=True, null=True)
    organisation = models.ForeignKey(Organisation, null=True, blank=True, on_delete=models.SET_NULL, related_name='users')

    def __str__(self):
        return f"{self.user.username} - {self.lavozim or 'No position'}"
