from django import forms
from .models import *

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

#Form to create/edit a User object, with an additional field for email
class UserCreationWithEmailForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Email')
    class Meta:
        model = User
        fields = ("username", "email")


class UserNutritionFormCreate(forms.ModelForm):
    class Meta:
        model = UserNutrition

        fields = ['calories', 'user']

        widgets = {
            'calories' : forms.NumberInput(attrs = {
                'placeholder' : 'Calories',
                'required' : True,
                'class' : 'formfield'
            }),
            'user': forms.HiddenInput(),
        }