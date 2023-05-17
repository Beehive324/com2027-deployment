"""healthoasis URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
import homeapp, homeapp.views

urlpatterns = [
    #Admin URL
    path('admin/', admin.site.urls),

    #Homepage URL
    path('home/', include('homeapp.urls')),
    #Redirect empty URL to home (127.0.0.1:8000/ -> 127.0.0.1:8000/home)
    path('', lambda reuqest: redirect('home/', permanent=False)),
    
    #Nutrition URL
    path('nutrition/', homeapp.views.nutrition, name='nutrition'),
    path('nutrition/search/', homeapp.views.search, name='search'),
    path('nutrition/search/results', homeapp.views.results, name='results'),

    #Chat websocket URLs
    path('chat/', include('chatapp.urls')),

    #Account related URLs:
    path('accounts/', include('django.contrib.auth.urls')), #Accounts, used to login (accounts/login)
    path('accounts/signup/', homeapp.views.RegisterUser.as_view(), name='signup_user'), #Signup page
    path('accounts/edit/', homeapp.views.updateUser, name="updateUser"),
    path('accounts/delete/', homeapp.views.deleteUser, name="deleteUser"),
    
    #Workout URLs
    path('workoutlog/', homeapp.views.workout2, name='workouts'),
    path('workoutlog/add', homeapp.views.addWorkout2, name='addWorkout'),
    path('workoutlog/edit', homeapp.views.editWorkout2, name='editWorkout'),
    path('workoutlog/delete', homeapp.views.deleteWorkout2, name='deleteWorkout'),
    
    #Workout URLs
    path('progress/', homeapp.views.progress, name='progress'),

    #about URL
    path('home/about', homeapp.views.about , name='about'),

    #Nutrition URLs pertaining to users.
    path('nutrition/log', homeapp.views.logUserNutrition, name = 'nutritionLog'),
]
