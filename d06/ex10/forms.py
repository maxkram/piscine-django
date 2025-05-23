from django import forms
from .models import People

class CharacterFilterForm(forms.Form):
    min_date = forms.DateField(
        label="Movies minimum release date",
        required=True,
        widget=forms.DateInput(
            format=('%Y-%m-%d'),
            attrs={'placeholder': 'Select a date', 'type': 'date'}
        )
    )
    max_date = forms.DateField(
        label="Movies maximum release date",
        required=True,
        widget=forms.DateInput(
            format=('%Y-%m-%d'),
            attrs={'placeholder': 'Select a date', 'type': 'date'}
        )
    )
    diameter = forms.IntegerField(
        label="Planet diameter greater than",
        required=True
    )
    gender = forms.ChoiceField(
        label="Character gender",
        choices=[],
        required=True
    )

    def __init__(self, *args, **kwargs):
        super(CharacterFilterForm, self).__init__(*args, **kwargs)
        self.fields['gender'].choices = [
            (gender['gender'], gender['gender']) 
            for gender in People.objects.values('gender').distinct()
        ]
