from django.http import HttpResponse
from django.template import loader
from django.shortcuts import get_object_or_404, render
from .forms import LogInForm, SignUpForm, Compl_Signup_Cand, Compl_Signup_Datore
from .forms import LogInForm, SignUpForm, Compl_Signup_Cand, Compl_Signup_Datore
from django.shortcuts import redirect
from .models import Utente, Offerta, Candidatura, Messaggio
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


dati_utente={}

def intro(request):
    return render(request, 'myapp/intro.html')

def home(request):
    return render(request, 'myapp/home.html')

def signup(request):
    global dati_utente
    print(User.objects.all())
    if request.method == 'POST':
        data=request.POST.dict()
        if SignUpForm(request.POST).is_valid():
            nome = data.get('nome')
            cognome = data.get('cognome')
            email = data.get('email')
            username = data.get('username')
            password = data.get('password')
            type = data.get('type')
            try:
                dati_utente = {"nome":nome, "cognome":cognome,"email":email, "username":username, "password":password, "type":type}
                if type == 'candidato':
                    form = Compl_Signup_Cand()
                else:
                    form = Compl_Signup_Datore()
                return render(request, 'myapp/complSignup.html', {'form': form , 'alert':False})
            except:
                form = SignUpForm()
                return render(request, 'myapp/signup.html', {'form': form, "alert": True})

        elif Compl_Signup_Cand(request.POST).is_valid() or Compl_Signup_Datore(request.POST).is_valid():
            base_user = User.objects.create_user(username=dati_utente['username'], email=dati_utente['email'], password=dati_utente['password'], first_name=dati_utente['nome'], last_name=dati_utente['cognome'])
            dati_utente['competenze']=data.get('competenze')
            dati_utente['residenza']=data.get('residenza')
            dati_utente['azienda']=data.get('azienda')

            utente = Utente(user=base_user, tipo=dati_utente['type'],competenze=dati_utente['competenze'],residenza=dati_utente['residenza'], azienda=dati_utente['azienda'])   
            utente.save() 
            
            return HttpResponse(f"Username: {utente.user.username}, Password: {utente.user.email}")

    else:
        form = SignUpForm()  # Creare un'istanza del form    
        return render(request, 'myapp/signup.html', {'form': form , 'alert':False})
    
def login(request):
    form = LogInForm()  # Creare un'istanza del form
    if request.method == 'POST':
        if LogInForm(request.POST).is_valid():
            data=request.POST.dict()
            username = data.get('username')
            password = data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                utente = Utente.objects.get(user=user)
                print(utente)
                return render(request, 'myapp/home.html', {'tipo':"candidato", "user":utente})
            else:
                return render(request, 'myapp/login.html', {'form': form, 'alert':True})

    else:
        return render(request, 'myapp/login.html', {'form': form, 'alert':False})

def index(request):
    # Utente.objects.all().delete()
    # User.objects.all().delete()
    return redirect("/intro")
