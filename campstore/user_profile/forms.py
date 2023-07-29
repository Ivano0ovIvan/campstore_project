from django import forms
from .models import UserProfileModel


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfileModel
        fields = [
            'first_name',
            'last_name',
            'email',
            'profile_picture',
            'address',
            'post_code',
            'phone_number',
            'is_seller'
        ]

