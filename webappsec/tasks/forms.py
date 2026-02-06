from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title']

    def clean_title(self):
        title = self.cleaned_data['title']
        if "hack" in title.lower():
            raise forms.ValidationError("Invalid input detected")
        return title


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "password1", "password2"]
