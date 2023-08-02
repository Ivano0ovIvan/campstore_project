from django import forms
from .models import UserProfileModel, ContactMessage


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


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['subject', 'message']


class SellerReplyForm(forms.Form):
    reply_message = forms.CharField(widget=forms.Textarea(attrs={'rows': 4}))
