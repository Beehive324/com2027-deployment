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
    path('admin/', admin.site.urls),
    path('', lambda reuqest: redirect('home/', permanent=False)),   #redirect empty URL to home
    path('home/', include('homeapp.urls')), #
    
    path('chat/', include('chatapp.urls')),


    #Account related URLs:
    path('accounts/', include('django.contrib.auth.urls')), #Accounts, used to login (accounts/login)
    path('accounts/signup/', homeapp.views.RegisterUser.as_view(), name='signup_user'), #Signup page
    path('accounts/edit/', homeapp.views.updateUser, name="updateUser"),
    path('accounts/delete/', homeapp.views.deleteUser, name="deleteUser"),
    path('workoutlog/add/', homeapp.views.addWorkout, name='addWorkout'),
    path('workoutlog/edit', homeapp.views.editWorkout, name='editWorkout'),
    path('workoutlog/delete', homeapp.views.deleteWorkout, name='deleteWorkout'),
]
