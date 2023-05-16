from django.shortcuts import render, redirect

from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required

from .models import *
from .forms import *

import requests
# Create your views here.


#View for homepage
def home(request):
    response = requests.get('http://api.weatherapi.com/v1/current.json?key=59208b37dbca49ae860121639231003&q=Guildford&aqi=no')
    weather = response.json()
    context = {'location':(weather['location']['name'] + ", " + weather['location']['country']),
               'condition':weather['current']['condition']['text'],
               'temp':weather['current']['temp_c'],
               'feelslike':weather['current']['feelslike_c'],
               }
    return render(request, 'homeapp/home.html', context)

#View to register a user
class RegisterUser(CreateView):
    model = User
    form_class = UserCreationWithEmailForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')

#View to update User record
@login_required
def updateUser(request):
    context={}
    user = request.user
    form = UserCreationWithEmailForm(request.POST or None, instance = user)
    if form.is_valid():
        #Overwrite existing record
        form.save()
        return redirect('/home')
    context["form"] = form
    return render(request, "registration/updateUser.html", context)

#View to delete User
@login_required
def deleteUser(request):
    context={}
    user = request.user
    if request.method == "POST":
        #Delete record
        user.delete()
        return redirect('/home')
    return render(request, "registration/deleteUser.html", context)

def breakfast(request):
    if request.method == 'POST':
        form = BreakfastForm(request.POST)
        if form.is_valid():
            breakfast_choice = form.cleaned_data['breakfast_choice']
            # Process the selected breakfast choice here
            return redirect('lunch_choices')  # Replace 'lunch_choices' with your actual URL name for the lunch choices page
    else:
        form = BreakfastForm()
    
    return render(request, 'breakfast.html', {'form': form})