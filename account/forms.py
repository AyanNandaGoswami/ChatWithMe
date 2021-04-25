from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegistrationForm(UserCreationForm):

    email = forms.EmailField(help_text='Enter a valid email address.')

    class Meta:
        model = User
        fields = ('first_name', 'email', 'username', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data['email']

        try:
            user = User.objects.get(email=email)
            raise forms.ValidationError(f'Email {email} already in use.')
        except:
            return email

    def clean_username(self):
        username = self.cleaned_data['username']

        try:
            user = User.objects.get(username=username)
            raise forms.ValidationError(f'Username {username} already in use.')
        except:
            return username

