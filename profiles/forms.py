from django import forms
from .models import UserProfile
from django_countries.fields import CountryField


from django import forms
from .models import UserProfile

from django import forms
from django_countries.fields import CountryField
from .models import UserProfile

class UserProfileForm(forms.ModelForm):

    default_country = forms.ChoiceField(choices=[('', 'Select a country')] + list(CountryField().choices), required=False)

    class Meta:
        model = UserProfile
        exclude = ('user',) 

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholders = {
            'default_phone_number': 'Phone Number',
            'default_postcode': 'Postal Code',
            'default_town_or_city': 'Town or City',
            'default_street_address1': 'Street Address 1',
            'default_street_address2': 'Street Address 2',
            'default_county': 'County, State or Locality',
            'default_country': 'Country',  
        }

        self.fields['default_phone_number'].widget.attrs['autofocus'] = True
        for field in self.fields:
            if field in placeholders:
                self.fields[field].widget.attrs['placeholder'] = placeholders[field]
                self.fields[field].widget.attrs['class'] = 'border-black rounded-0 profile-form-input'
                self.fields[field].label = False

        if 'instance' in kwargs and kwargs['instance'].default_country:
            self.fields['default_country'].initial = kwargs['instance'].default_country

