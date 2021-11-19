from django import forms
from .models import Links
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class LinksForm(forms.ModelForm):
    original = forms.URLField(required=True, min_length=11)
    class Meta:
        model = Links
        fields = ["original"]

class UserForm(UserCreationForm):
    username = forms.CharField(min_length=8, max_length=150, help_text="8 characters or more. Letters, digits and @/./+/-/_ only.")
    email = forms.EmailField(max_length=254, help_text='Inform a valid email address.', required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', )