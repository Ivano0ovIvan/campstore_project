from django.contrib.auth.models import User
from django.db import models


class UserProfileModel(models.Model):
    user = models.OneToOneField(
        User,
        related_name='userprofile',
        on_delete=models.CASCADE
    )

    is_seller = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username