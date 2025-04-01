from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    password_confirm = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        model = User
        fields = ['username']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")
        username = cleaned_data.get("username")

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Passwords do not match.")
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already exists.")
        if not username or not password or not password_confirm:
            raise forms.ValidationError("All fields are required.")
        return cleaned_data

class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Username")
    password = forms.CharField(widget=forms.PasswordInput, label="Password")

    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data.get("username") or not cleaned_data.get("password"):
            raise forms.ValidationError("All fields are required.")
        return cleaned_data