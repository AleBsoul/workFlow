from django.http import HttpResponse
from django.template import loader
from django.shortcuts import get_object_or_404, render
from .forms import *
from django.shortcuts import redirect
from .models import Utente, Offerta, Candidatura, Messaggio, Preferiti
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib import messages


def intro(request):
    return render(request, 'myapp/intro.html')

def home(request):
    if request.session.get('username'):
        username = request.session['username']
        user = User.objects.get(username=username)
        utente = Utente.objects.get(user=user)
        if utente.tipo=='candidato':
            favs = Preferiti.objects.filter(id_candidato=utente)
            print(favs)
            offerte = Offerta.objects.all()
            candidature = Candidatura.objects.filter(id_candidato=utente)
            print(candidature)
            return render(request, 'myapp/home.html', {'tipo':utente.tipo, 'offerte': offerte, 'candidature':candidature,'favs':favs})
        else:
            offerte = Offerta.objects.filter(id_datore=utente.id) 
            return render(request, 'myapp/home.html', {'tipo':utente.tipo, 'offerte': offerte})
    else:
        return redirect("login")


def favourite(request, offerta_id):
    if request.session.get('username'):
        username = request.session['username']
        user = User.objects.get(username=username)
        utente = Utente.objects.get(user=user)
        offerta = Offerta.objects.get(id=offerta_id)
        if Preferiti.objects.filter(id_candidato=utente, id_offerta=offerta).exists():
            Preferiti.objects.filter(id_candidato=utente, id_offerta=offerta).delete()
            return redirect("home")
        else:
            fav = Preferiti(id_candidato=utente, id_offerta=offerta)
            fav.save()
            return redirect("home")
    else:
        return redirect("login")
    

def addOfferta(request):
    if request.session.get('username'):
        username = request.session['username']
        user = User.objects.get(username=username)
        utente = Utente.objects.get(user=user)
        if request.method == 'POST':
            data=request.POST.dict()
            if formOfferta(request.POST).is_valid():
                giorno = data.get('data')
                descrizione = data.get('descrizione')
                requisiti = data.get('requisiti')
                impiego = data.get('impiego')
                stipendio = data.get('stipendio')
                luogo = data.get('luogo')
                offerta = Offerta(data=giorno,descrizione=descrizione,requisiti=requisiti, luogo=luogo, impiego=impiego, stipendio=stipendio, id_datore=utente)   
                offerta.save()

            return render(request, 'myapp/nuovaOfferta.html', {'form': formOfferta(), 'tipo': utente.tipo})
        else:
            form = formOfferta()
            return render(request, 'myapp/nuovaOfferta.html', {'form': form, 'tipo': utente.tipo})
    else:
        return redirect("login")

def signup(request):
    global dati_utente
    form = SignUpForm()
    if request.method == 'POST':
        data=request.POST.dict()
        if SignUpForm(request.POST).is_valid():
            nome = data.get('nome')
            cognome = data.get('cognome')
            email = data.get('email')
            username = data.get('username')
            password = data.get('password')
            type = data.get('type')

            if User.objects.filter(username=username).exists():
                return render(request, 'myapp/signup.html', {'form': form, 'message': "Username già in uso"})
            
            user = authenticate(username=username, password=password)
            if user is None:
                dati_utente = {"nome":nome, "cognome":cognome,"email":email, "username":username, "password":password, "type":type}
                if type == 'candidato':
                    form = Compl_Signup_Cand()
                else:
                    form = Compl_Signup_Datore()
                return render(request, 'myapp/complSignup.html', {'form': form})
            else:
                return render(request, 'myapp/complSignup.html', {'form': form , 'message': "Username già in uso"})

            
        elif Compl_Signup_Cand(request.POST).is_valid() or Compl_Signup_Datore(request.POST).is_valid():
            base_user = User.objects.create_user(username=dati_utente['username'], email=dati_utente['email'], password=dati_utente['password'], first_name=dati_utente['nome'], last_name=dati_utente['cognome'])
            dati_utente['competenze']=data.get('competenze')
            dati_utente['residenza']=data.get('residenza')
            dati_utente['azienda']=data.get('azienda')

            utente = Utente(user=base_user, tipo=dati_utente['type'],competenze=dati_utente['competenze'],residenza=dati_utente['residenza'], azienda=dati_utente['azienda'])   
            utente.save() 
            
            return redirect('login')
    else:
        return render(request, 'myapp/signup.html', {'form': form })

def login(request):
    if 'username' in request.session:
        del request.session['username']
    form = LogInForm()  # Creare un'istanza del form
    if request.method == 'POST':
        if LogInForm(request.POST).is_valid():
            data=request.POST.dict()
            username = data.get('username')
            password = data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                request.session['username'] = username
                utente = Utente.objects.get(user=user)
                return redirect('home')
            else:
                return render(request, 'myapp/login.html', {'form': form, 'message': "credenziali errate"})

    else:
        return render(request, 'myapp/login.html', {'form': form})


def cancella_offerta(request, offerta_id):
    if request.session.get('username'):
        username = request.session['username']
        user = User.objects.get(username=username)
        utente = Utente.objects.get(user=user)
        Offerta.objects.get(id=offerta_id).delete()
        offerte = Offerta.objects.all()
        return redirect("home")
    else:
        return redirect("login")


def candidati(request, offerta_id):
    if request.session.get('username'):
        username = request.session['username']
        user = User.objects.get(username=username)
        utente = Utente.objects.get(user=user)
        offerta = Offerta.objects.get(id=offerta_id)
        if Candidatura.objects.filter(id_candidato=utente, id_offerta=offerta).exists():
            Candidatura.objects.filter(id_candidato=utente, id_offerta=offerta).delete()
        else:
            candidatura= Candidatura(id_candidato=utente, id_offerta=offerta)
            candidatura.save()
        return redirect("home")

    else:
        return redirect("login")

def candidature(request):
    if request.session.get('username'):
        username = request.session['username']
        user = User.objects.get(username=username)
        utente = Utente.objects.get(user=user)
        if utente.tipo=='candidato':
            cand = Candidatura.objects.filter(id_candidato=utente)
        else:
            cand = Candidatura.objects.filter(id_offerta__id_datore=utente)
        return render(request, 'myapp/candidature.html', {"tipo":utente.tipo, 'candidature':cand})
    else:
        return redirect("login")
    
def accetta_candidatura(request, cand_id):
    if request.session.get('username'):
        cand = Candidatura.objects.get(id=cand_id)
        cand.stato="accettata"
        print(cand.stato)
        cand.save()
        return redirect("candidature")
    else:
        return redirect("login")


def cancella_candidatura(request, cand_id):
    if request.session.get('username'):
        Candidatura.objects.get(id=cand_id).delete()
        return redirect("candidature")
    else:
        return redirect("login")


def chat(request):
    if request.session.get('username'):
        username = request.session['username']
        user = User.objects.get(username=username)
        utente = Utente.objects.get(user=user)
        chats = [
                {"nome": "prova"},
                {"nome": "prova2"}
            ]
        if request.method == 'GET':
            return render(request, 'myapp/chats.html', {"tipo":utente.tipo,"chats": chats, "open":False})
        else:
            
            return render(request, 'myapp/chats.html', {"tipo":utente.tipo,"chats": chats, "open":True})
    else:
        return redirect("login")

def index(request):
    # Utente.objects.all().delete()
    # User.objects.all().delete()
    return redirect("intro")


def logout(request):
    if 'username' in request.session:
        del request.session['username']
    return redirect('login')
