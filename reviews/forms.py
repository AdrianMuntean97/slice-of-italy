from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']

    rating = forms.ChoiceField(choices=[(i, i) for i in range(1, 6)], widget=forms.RadioSelect)