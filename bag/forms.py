from django import forms
from .models import BagItem

class BagItemForm(forms.ModelForm):
    class Meta:
        model = BagItem
        fields = ['quantity']
