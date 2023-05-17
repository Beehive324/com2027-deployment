from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta, date

from .models import User, Exercise, UserWorkouts

from django.shortcuts import get_object_or_404, redirect, render



from .models import *
from .forms import *

import requests

#WeatherAPI direction dictionary
dir = {
    'NW':'North-West',
    'N':'North',
    'NE':'North-East',
    'E':'East',
    'SE':'South-East',
    'S':'South',
    'SW':'South-West',
    'W':'West'
}

#Nutrition API variables
nutritionAppID = '3cb0640e'
nutritionKey = 'c3fb87d22654be6672e1b78518bd7028'
headers = {'x-app-id':nutritionAppID,
           'x-app-key':nutritionKey,
           'content-type':'application/json'}
nutritionEndPt = 'https://trackapi.nutritionix.com/v2/natural/nutrients'
exerciseEndPt = 'https://trackapi.nutritionix.com/v2/natural/exercise'

#APINinja exercise API variables
APINinjaKey = 'f7INLmwM1qteGEeuhO1HwQ==ZjyRFWgA4YkQouxM'
APINinjaHeaders = {'X-Api-Key' : APINinjaKey}
APINinjaEndPt = 'https://api.api-ninjas.com/v1/exercises?muscle='

#View for homepage
def home(request):
    #WeatherAPI data getter
    weatherResponse = requests.get('http://api.weatherapi.com/v1/current.json?key=59208b37dbca49ae860121639231003&q=Guildford&aqi=no')
    weather = weatherResponse.json()

    try:    #Try to format wind direction nicely
        windDir = dir[weather['current']['wind_dir']]
    except: #Not in pre-def dictionary? Keep as-is
        windDir = weather['current']['wind_dir']

    '''#NutritionAPI data getter
    nQuery = {
        "query":"big mac"
    }
    nutritionResponse = requests.post(nutritionEndPt, headers=headers, json=nQuery)
    nutrition = nutritionResponse.json()
    #Extract info from request
    for food in nutrition['foods']:
        name = food['food_name']
        cals = round(food['nf_calories'])
        fat = food['nf_saturated_fat']
        photo = food['photo']['highres']

    eQuery = {
        'query':'ran 5 miles',
        'gender':'male',
        'weight_kg':'85',
        'height_cm':'175',
        'age':20
    }
    exerciseResponse = requests.post(exerciseEndPt, headers=headers, json=eQuery)
    exercise = exerciseResponse.json()
    #Extract info from request
    print(exercise)
    for e in exercise['exercises']:
        type = e['user_input']
        burntCals = e['nf_calories']

    #Pass context into template
    context = {'location':(weather['location']['name'] + ", " + weather['location']['country']),
               'condition':weather['current']['condition']['text'],
               'temp':weather['current']['temp_c'],
               'feelslike':weather['current']['feelslike_c'],
               'wind_mph':weather['current']['wind_mph'],
                'wind_dir':windDir,
               'vis':weather['current']['vis_miles'],

               'nName':name,
               'nCals':cals,
               'nFat':fat,
               'nImg':photo,

               'burntCals':burntCals,
               'eType':type
    }'''
    context = {}
    return render(request, 'homeapp/home.html', context)

def search(request):
    if request.method == 'POST':
        query = request.POST.get('query', '')
        data = {'query': query}
        response = requests.post(nutritionEndPt, headers=headers, json=data)
        if response.status_code == 200:
            results = response.json()
            return render(request, 'nutrition/results.html', {'results': results})
    return render(request, 'nutrition/search.html')

def results(request):
    return render(request, 'nutrition/results.html')

def exerciseSearch(request):
    if request.method == 'POST':
        muscle = request.POST.get('query', '')
        difficulty = request.POST.get('difficulty', '')
        queryString = {"muscle":muscle, "difficulty":difficulty}
        url = 'https://api.api-ninjas.com/v1/exercises'
        response = requests.get(url, headers=APINinjaHeaders, params=queryString)
        if response.status_code == 200:
            results = response.json()
            print(results)
            return render(request, 'exerciseFinder/results.html', {'results': results})
    return render(request, 'exerciseFinder/search.html')

def exerciseResults(request):
    return render(request, 'exerciseFinder/results.html')

@login_required
def nutrition(request):
    context = {}
    return render(request, 'nutrition/nutrition.html', context)

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
#_____________________________________________________________________
#View to add a workout(added this just to see the workouts pages -Obi)
def workout2(request):
    return render(request, 'workoutlog/workouts.html')

def addWorkout2(request):
    return render(request, 'workoutlog/add.html')

def editWorkout2(request):
    return render(request, 'workoutlog/edit.html')

def deleteWorkout2(request):
    return render(request, 'workoutlog/delete.html')
#_____________________________________________________________________

@login_required
#View to see progress
def progress(request):
    context = {}
    context["workoutlist"] = UserWorkouts.objects.filter(user = request.user.id)
    return render(request, 'progress/progress.html')

#View to add a workout
@login_required
def addWorkout(request):
    if request.method == 'POST':
        form = UserWorkout(request.POST)
        if form.is_valid():
            # Create a new Workout object with form data
            workout = form.save(commit=False)
            workout.date = date.today()
            # You can also associate the workout with the current user
            # workout.user = request.user
            workout.save()

            # Redirect to a success page or any other desired action
            return redirect('home')
    else:
        form = UserWorkout()

    context = {'form': form}
    return render(request, 'workoutlog/add.html', context)

#View to edit a workout
@login_required
def editWorkout(request):
    workout = get_object_or_404(Workout)

    if request.method == 'POST':
        form = UserWorkout(request.POST, instance=workout)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = UserWorkout(instance=workout)

    context = {'form': form}
    return render(request, 'workoutlog/edit.html', context)


#View to delete a workout
@login_required
def deleteWorkout(request):
    # Retrieve the existing workout object from the database
    workout = get_object_or_404(Workout)

    if request.method == 'POST':
        workout.delete()
        return redirect('home')

    context = {'workout': workout}
    return render(request, 'workoutlog/delete.html', context)

def about(request):
    context = {}
    return render(request, 'homeapp/about.html', context)

@login_required
def logUserNutrition(request):
    context ={}
    currentUser = get_object_or_404(User, id = request.user.id)
    form = UserNutritionForm(request.POST or None)
    if(request.method == 'GET'):
        try:
            currentUser = UserNutrition.objects.get(user = currentUser)
            context['currentUserWeeklyIntake'] =  currentUser
            messages.add_message(request, messages.ERROR, 'You already have your Weekly Caloric Intake saved, entering in a new value will update you current Weekly Caloric Intake.')
        except UserNutrition.DoesNotExist:
            pass
    elif(request.method == 'POST'):
        if form.is_valid():
            try:
                existingCalorieEntry = UserNutrition.objects.get(user = currentUser)
                if(existingCalorieEntry.time_since_creation() < 7):
                    messages.add_message(request, messages.ERROR, 'Cannot update Current Caloric intake; Has not yet been a week.')
                    return redirect('/nutrition')
                else:
                    existingCalorieEntry.calories = form.cleaned_data['calories']
                    existingCalorieEntry.save() 
                    messages.add_message(request, messages.SUCCESS, 'Weekly Caloric intake updated.')
            except UserNutrition.DoesNotExist:
                form = UserNutrition(calories = form.cleaned_data['calories'], user = request.user)
                messages.add_message(request, messages.SUCCESS, 'Weekly Caloric intake Logged.')
                form.save()
            return redirect('/nutrition')
        else:
            messages.add_message(request, messages.ERROR, 'Invalid Form Data; Nutrition not updated.')
    context['form']= form
    return render(request, "userNutrition/logUserNutrition.html", context)