from django import forms

class TextForm(forms.Form):
    text = forms.CharField(label='Enter text', max_length=100)