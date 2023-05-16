from django import forms
from .models import *

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

#Form to create/edit a User object, with an additional field for email
class UserCreationWithEmailForm(UserCreationForm):
    email = forms.EmailField(required=True, label='email')
    class Meta:
        model = User
        fields = ("username", "email")


class BreakfastForm(forms.Form):
    BREAKFAST_CHOICES = [
        ('healthy', 'Option 1 (Healthy)'),
        ('medium', 'Option 2 (Medium Healthy)'),
        ('unhealthy', 'Option 3 (Unhealthy)'),
    ]

    breakfast_choice = forms.ChoiceField(
        label='Pick 1 of the 3 options for breakfast choices.',
        choices=BREAKFAST_CHOICES,
        widget=forms.RadioSelect
    )