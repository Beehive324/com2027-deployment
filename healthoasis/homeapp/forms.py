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

class UserNutritionForm(forms.ModelForm):
    class Meta:
        model = UserNutrition

        fields = ['calories', 'user']

        widgets = {
            'calories' : forms.NumberInput(attrs = {
                'placeholder' : 'kcals',
                'required' : True,
                'class' : 'formfield',
            }),
            'user': forms.HiddenInput(),
        }

class UserWorkout(forms.ModelForm):
    class Meta:
        model = Workout
        fields = ['user', 'workout', 'date', 'desc']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'formfield'}),
            'description': forms.Textarea(attrs={'class': 'formfield', 'rows': 5}),
            'date': forms.DateInput(attrs={'class': 'formfield', 'type': 'date'}),
            'exercises': forms.SelectMultiple(attrs={'class': 'formfield'}),
            'user': forms.HiddenInput(),
        }
 
 