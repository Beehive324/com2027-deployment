from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta, date
from random import choice
from homeapp.models import BreakfastOption
from .models import User, Exercise, UserWorkouts
from django.shortcuts import get_object_or_404, redirect, render
from .models import *
from .forms import *

import requests


BREAKFAST_OPTIONS_HEALTHY = [
    'Oatmeal', 'Whole Grain Bread', 'Boiled Eggs', 'Avocado', 'Apple'
]

BREAKFAST_OPTIONS_MEDIUM_HEALTHY = [
    'Bran Flakes', 'Sourdough Bread', 'Scrambled Tofu', 'Baked Beans', 'Greek Yoghurt'
]

BREAKFAST_OPTIONS_UNHEALTHY = [
    'Frosted Flakes', 'White Bread', 'Sausage', 'Bacon', 'Hot Chocolate'
]


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

               'burntCals':burntCals,
               'eType':type
    }
    return render(request, 'homeapp/home.html', context)

#View for nutrition search
@login_required
def search(request):
    if request.method == 'POST':
        #Get request
        query = request.POST.get('query', '')
        data = {'query': query}
        #Pass to API
        response = requests.post(nutritionEndPt, headers=headers, json=data)
        if response.status_code == 200: #If successful,
            results = response.json()   #convert to JSON and pass into template
            return render(request, 'nutrition/results.html', {'results': results})
    return render(request, 'nutrition/search.html')

#View for nutrition search results
@login_required
def results(request):
    return render(request, 'nutrition/results.html')

#View for exercise search
@login_required
def exerciseSearch(request):
    if request.method == 'POST':
        #Get request
        muscle = request.POST.get('query', '')
        difficulty = request.POST.get('difficulty', '')
        queryString = {"muscle":muscle, "difficulty":difficulty}
        #Pass to API
        url = 'https://api.api-ninjas.com/v1/exercises'
        response = requests.get(url, headers=APINinjaHeaders, params=queryString)
        if response.status_code == 200: #If successful,
            results = response.json()   #convert to JSON and pass into template
            print(results)
            return render(request, 'exerciseFinder/results.html', {'results': results})
    return render(request, 'exerciseFinder/search.html')

#View for exercise search results
@login_required
def exerciseResults(request):
    return render(request, 'exerciseFinder/results.html')

#View for nutrition page
@login_required
def nutrition(request):
    context = {}
    return render(request, 'nutrition/nutrition.html', context)

#View to register a user
class RegisterUser(CreateView):
    #Setup form
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
    #Get all objects, parse to template
    context["workoutlist"] = UserWorkouts.objects.filter(user = request.user.id)
    context["calorielist"] = UserNutrition.objects.filter(user = request.user.id)
    return render(request, 'progress/progress.html', context)

#View to add a workout
@login_required
def addWorkout(request):
    if request.method == 'POST':
        form = UserWorkout(request.POST)
        if form.is_valid():
            workout = form.save(commit=False)
            workout.date = date.today()
            workout.save()
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

    context = {'form': form, 'workout': workout}
    return render(request, 'workoutlog/edit.html', context)


#View to delete a workout
@login_required
def deleteWorkout(request):

    workout = get_object_or_404(Workout)

    if request.method == 'POST':
        workout.delete()
        return redirect('home')

    context = {'workout': workout}
    return render(request, 'workoutlog/delete.html', context)

def about(request):
    context = {}
    return render(request, 'homeapp/about.html', context)

#View with logic to Log User's weekly caloric intake.
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
                else:
                    existingCalorieEntry.calories = form.cleaned_data['calories']
                    existingCalorieEntry.save() 
                    messages.add_message(request, messages.SUCCESS, 'Weekly Caloric intake updated.')
            except UserNutrition.DoesNotExist:
                newEntry = UserNutrition(calories = form.cleaned_data['calories'], user = request.user)
                messages.add_message(request, messages.SUCCESS, 'Weekly Caloric intake Logged.')
                newEntry.save()
            return redirect('/nutrition')
        else:
            messages.add_message(request, messages.ERROR, 'Invalid Form Data; Nutrition not updated.')
    context['form']= form
    return render(request, "userNutrition/logUserNutrition.html", context)

@login_required  # Ensures that the user must be logged in to access this page
def questionnaire_page1(request):
    if request.method == 'POST':
        # Handle form submission
        # Retrieve the user's answers from the request.POST dictionary
        # Save the answers and redirect to the next page
        # You can use Django forms or manually handle the form data
        # Example code:
        height = request.POST['height']
        weight = request.POST['weight']
        date_of_birth = request.POST['date_of_birth']
        # Save the answers to the database or perform any necessary actions
        # Redirect to the next page of the questionnaire
        return redirect('questionnaire_page2')

    # If the request method is GET, render the questionnaire page template
    return render(request, 'homeapp/questionnaire_page1.html')


@login_required
def questionnaire_page2(request):
    if request.method == 'POST':
        # Handle form submission and redirect to the next page
        # Retrieve the selected breakfast option from the form
        selected_option = request.POST.get('breakfast_option')
        # Save the selected option and its health level to the database
        # Example code assuming you have a BreakfastOption model:
        breakfast_option = BreakfastOption.objects.create(
            user=request.user,
            option=selected_option,
            health_level=get_breakfast_health_level(selected_option)
        )
        # Redirect to the next page of the questionnaire
        return redirect('questionnaire_page3')

    # If the request method is GET, render the questionnaire page template
    # Generate a random breakfast option for each health level
    healthy_option = choice(BREAKFAST_OPTIONS_HEALTHY)
    medium_healthy_option = choice(BREAKFAST_OPTIONS_MEDIUM_HEALTHY)
    unhealthy_option = choice(BREAKFAST_OPTIONS_UNHEALTHY)

    context = {
        'healthy_option': healthy_option,
        'medium_healthy_option': medium_healthy_option,
        'unhealthy_option': unhealthy_option,
    }

    return render(request, 'homeapp/questionnaire_page2.html', context)

def get_breakfast_health_level(selected_option):
    if selected_option in BREAKFAST_OPTIONS_HEALTHY:
        return 'Healthy'
    elif selected_option in BREAKFAST_OPTIONS_MEDIUM_HEALTHY:
        return 'Medium Healthy'
    elif selected_option in BREAKFAST_OPTIONS_UNHEALTHY:
        return 'Unhealthy'
    else:
        return 'Unknown'
