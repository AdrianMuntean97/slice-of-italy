from django import forms
from .models import UserProfile

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['phone_number', 'address', 'postal_code']
        labels = {
            'phone_number': 'Phone Number',
            'address': 'Address',
            'postal_code': 'Postal Code',
        }
        widgets = {
            'phone_number': forms.TextInput(attrs={'placeholder': 'Enter your phone number'}),
            'address': forms.TextInput(attrs={'placeholder': 'Enter your address'}),
            'postal_code': forms.TextInput(attrs={'placeholder': 'Enter your postal code'}),
        }
