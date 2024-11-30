from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser
from django import forms
from django.core.exceptions import ValidationError

class CustomUserCreationForm(UserCreationForm):
        class Meta(UserCreationForm.Meta):
            model = CustomUser
            fields = ("email",)

class CustomUserChangeForm(UserChangeForm):
        class Meta:
            model = CustomUser
            fields = ("email",)

