from django.contrib.auth.models import User
from django.db import models

from campstore.store.validators import validate_name, validate_name_length, validate_phone_number


class UserProfileModel(models.Model):
    user = models.OneToOneField(
        User,
        related_name='userprofile',
        on_delete=models.CASCADE
    )
    first_name = models.CharField(
        validators = [validate_name, validate_name_length],
        max_length=50,
        blank=True,
        null=True
    )
    last_name = models.CharField(
        validators=[validate_name, validate_name_length],
        max_length=50,
        blank=True,
        null=True
    )
    email = models.EmailField(
        unique=True,
        blank=True,
        null=True
    )
    profile_picture = models.ImageField(
        upload_to='uploads/profile_images',
        blank=True,
        null=True
    )
    address = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )
    post_code = models.IntegerField(blank=True,null=True)
    phone_number = models.CharField(
        validators=[validate_phone_number],
        max_length=15,
        blank=True,
        null=True)

    is_seller = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username