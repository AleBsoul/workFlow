from django.http import HttpResponse
from django.template import loader
from django.shortcuts import get_object_or_404, render
from .forms import LogInForm, SignUpForm
from django.shortcuts import redirect





def intro(request):
    return render(request, 'myapp/intro.html')

def home(request):
    return render(request, 'myapp/home.html')

def signup(request):
    form = SignUpForm()  # Creare un'istanza del form    
    if request.method == 'POST':
        data=request.POST.dict()
        username = data.get('username')
        password = data.get('password')
        type = data.get('type')
        print(data)
    return render(request, 'myapp/signup.html', {'form': form})

def login(request):
    form = LogInForm()  # Creare un'istanza del form
    return render(request, 'myapp/login.html', {'form': form})

def index(request):
    return redirect("/intro")
