from django.http import HttpResponse
from django.template import loader
from django.shortcuts import get_object_or_404, render
from .forms import LogInForm, SignUpForm
from django.shortcuts import redirect



def home(request):
    return render(request, 'base.html')

def signup(request):
    form = SignUpForm()  # Creare un'istanza del form
    return render(request, 'myapp/signup.html', {'form': form})

def login(request):
    form = LogInForm()  # Creare un'istanza del form
    return render(request, 'myapp/login.html', {'form': form})

def index(request):
    return redirect("/home")
