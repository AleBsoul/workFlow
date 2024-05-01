from django.http import HttpResponse
from django.template import loader
from django.shortcuts import get_object_or_404, render
from .forms import LogInForm, SignUpForm, Compl_Signup_Cand, Compl_Signup_Datore
from django.shortcuts import redirect
from .models import Datore, Candidato, Offerta, Candidatura, Messaggio


def intro(request):
    return render(request, 'myapp/intro.html')

def home(request):
    return render(request, 'myapp/home.html')

def signup(request):
    utente = ''
    if request.method == 'POST':
        if SignUpForm(request.POST).is_valid():
            data=request.POST.dict()
            nome = data.get('nome')
            cognome = data.get('cognome')
            email = data.get('email')
            username = data.get('username')
            password = data.get('password')
            type = data.get('type')
            if type == 'candidato':
                utente = Candidato(nome=nome, cognome=cognome, email=email, username=username, password=password)
                form = Compl_Signup_Cand()
            else:
                utente = Datore(nome=nome, cognome=cognome, email=email, username=username, password=password)
                form = Compl_Signup_Datore()
            return render(request, 'myapp/complSignup.html', {'form': form})
        elif Compl_Signup_Cand(request.POST).is_valid():
            print(utente)
            form = Compl_Signup_Cand()
            return render(request, 'myapp/complSignup.html', {'form': form})
    else:
        form = SignUpForm()  # Creare un'istanza del form    
        return render(request, 'myapp/signup.html', {'form': form})

def login(request):
    form = LogInForm()  # Creare un'istanza del form
    if request.method == 'POST':
        if LogInForm(request.POST).is_valid():
            data=request.POST.dict()
            username = data.get('username')
            password = data.get('password')
            return render(request, 'myapp/signup.html')
    
    return render(request, 'myapp/login.html', {'form': form})

def index(request):
    return redirect("/intro")
