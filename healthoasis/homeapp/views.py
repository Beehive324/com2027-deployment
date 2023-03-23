from django.shortcuts import render

from django.views.generic import CreateView
from django.urls import reverse_lazy

from .models import *
from .forms import *

import requests
# Create your views here.


#View for homepage
def home(request):
    response = requests.get('http://api.weatherapi.com/v1/current.json?key=59208b37dbca49ae860121639231003&q=London&aqi=no')
    weather = response.json()
    context = {'location':(weather['location']['name'] + ", " + weather['location']['country']),
               'condition':weather['current']['condition']['text']}
    return render(request, 'homeapp/home.html', context)

#View to register a user
class RegisterUser(CreateView):
    model = User
    form_class = UserCreationWithEmailForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')