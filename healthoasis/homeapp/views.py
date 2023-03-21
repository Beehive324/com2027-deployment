from django.shortcuts import render

from django.views.generic import CreateView
from django.urls import reverse_lazy

from .models import *
from .forms import *
# Create your views here.


#View for homepage
def home(request):
    context = {}
    return render(request, 'homeapp/home.html', context)

#View to register a user
class RegisterUser(CreateView):
    model = User
    form_class = UserCreationWithEmailForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')