from django import forms
from django.contrib.auth.models import User

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    password_confirm = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        model = User
        fields = ['username']
        labels = {'username': 'Username'}

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        # Check all fields are filled
        if not username or not password or not password_confirm:
            raise forms.ValidationError("All fields are required.")
        
        # Check if username is unique
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken.")
        
        # Check if passwords match
        if password != password_confirm:
            raise forms.ValidationError("Passwords do not match.")
        
        return cleaned_data

class LoginForm(forms.Form):
    username = forms.CharField(label="Username")
    password = forms.CharField(widget=forms.PasswordInput, label="Password")

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        # Check all fields are filled
        if not username or not password:
            raise forms.ValidationError("All fields are required.")
        
        return cleaned_data