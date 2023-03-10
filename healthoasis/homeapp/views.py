from django.shortcuts import render

# Create your views here.


#View for homepage
def home(request):
    context = {}
    return render(request, 'homeapp/home.html', context)