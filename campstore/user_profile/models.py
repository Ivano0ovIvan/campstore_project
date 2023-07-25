from django.contrib.auth.models import User
from django.db import models


class UserProfileModel(models.Model):
    user = models.OneToOneField(
        User,
        related_name='userprofile',
        on_delete=models.CASCADE
    )
    first_name = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )
    last_name = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )
    profile_picture = models.URLField(
        blank=True,
        null=True
    )
    address = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )
    post_code = models.IntegerField(blank=True,null=True)
    phone_number = models.IntegerField(blank=True,null=True)

    is_seller = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username