from django.http import HttpResponse
from django.template import loader
from django.shortcuts import get_object_or_404, render
from .forms import *
from django.shortcuts import redirect
from .models import Utente, Offerta, Candidatura, Messaggio, Preferiti
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib import messages
from django.http import JsonResponse


def intro(request):
    return render(request, 'myapp/intro.html')

def home(request):
    if request.session.get('username'):
        username = request.session['username']
        user = User.objects.get(username=username)
        utente = Utente.objects.get(user=user)
        if utente.tipo=='candidato':
            favs = Preferiti.objects.filter(id_candidato=utente)
            offerte = Offerta.objects.all()
            candidature = Candidatura.objects.filter(id_candidato=utente)
            id_cands = []
            for cand in candidature:
                for offerta in offerte:
                    if offerta.id == cand.id_offerta.id:
                        id_cands.append(cand.id_offerta.id)
            id_favs = []
            for fav in favs:
                for offerta in offerte:
                    if offerta.id == fav.id_offerta.id:
                        id_favs.append(fav.id_offerta.id)
            return render(request, 'myapp/home.html', {'tipo':utente.tipo, 'offerte': offerte, 'candidature':candidature,'favs':favs, 'id_cands': id_cands, 'id_favs':id_favs})
        else:
            offerte = Offerta.objects.filter(id_datore=utente.id) 
            return render(request, 'myapp/home.html', {'tipo':utente.tipo, 'offerte': offerte})
    else:
        return redirect("login")

def favourite_2(request, offerta_id):
    if request.session.get('username'):
        username = request.session['username']
        user = User.objects.get(username=username)
        utente = Utente.objects.get(user=user)
        offerta = Offerta.objects.get(id=offerta_id)
        if Preferiti.objects.filter(id_candidato=utente, id_offerta=offerta).exists():
            Preferiti.objects.filter(id_candidato=utente, id_offerta=offerta).delete()
            return redirect("preferiti")
        else:
            fav = Preferiti(id_candidato=utente, id_offerta=offerta)
            fav.save()
            return redirect("preferiti")
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

def candidati_2(request, offerta_id):
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
        return redirect("preferiti")

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


def preferiti(request):
    if request.session.get('username'):
        username = request.session['username']
        user = User.objects.get(username=username)
        utente = Utente.objects.get(user=user)
        if utente.tipo=='candidato':
            favs = Preferiti.objects.filter(id_candidato=utente)
            candidature = Candidatura.objects.filter(id_candidato=utente)
            id_cands = []
            for cand in candidature:
                for fav in favs:
                    if fav.id_offerta.id == cand.id_offerta.id:
                        id_cands.append(cand.id_offerta.id)
            return render(request, 'myapp/preferiti.html',  {'tipo':utente.tipo, 'offerte': favs, 'candidature':candidature,'favs':favs, 'id_cands': id_cands})
    else:
        return redirect("login")



def get_new_messages(request, cand_id, last_message_id):
    if request.session.get('username'):
        candidatura = Candidatura.objects.get(id=cand_id)
        new_messages = Messaggio.objects.filter(
            id_candidato=candidatura.id_candidato,
            id_datore=candidatura.id_offerta.id_datore,
            id__gt=last_message_id
        ).order_by('id')
        
        if new_messages.exists():
            return JsonResponse({
                'new_messages': True,
                'messages': [
                    {
                        'id': msg.id,
                        'contenuto': msg.contenuto,
                        'id_mittente': msg.id_mittente
                    } for msg in new_messages
                ]
            })
        else:
            return JsonResponse({'new_messages': False})
    else:
        return JsonResponse({'new_messages': False, 'error': 'Not authenticated'}, status=401)

def chat(request, cand_id):
    if request.session.get('username'):
        form = formChat()
        username = request.session['username']
        user = User.objects.get(username=username)
        utente = Utente.objects.get(user=user)
        candidatura = Candidatura.objects.get(id=cand_id)
        
        if utente.tipo == 'candidato':
            interlocutore = candidatura.id_offerta.id_datore.user.first_name + " " + candidatura.id_offerta.id_datore.user.last_name
        else:
            interlocutore = candidatura.id_candidato.user.first_name + " " + candidatura.id_candidato.user.last_name
        
        if request.method == "POST":
            form = formChat(request.POST)
            if form.is_valid():
                contenuto = form.cleaned_data['messaggio']
                messaggio = Messaggio(id_datore=candidatura.id_offerta.id_datore, id_candidato=candidatura.id_candidato, contenuto=contenuto, id_mittente=utente.id)
                messaggio.save()
                return redirect('chat', cand_id=cand_id)
        
        messaggi = Messaggio.objects.filter(id_candidato=candidatura.id_candidato, id_datore=candidatura.id_offerta.id_datore).order_by('id')
        last_message_id = messaggi.last().id if messaggi.exists() else 0
        
        return render(request, "myapp/chat.html", {
            'form': form,
            'interlocutore': interlocutore,
            'candidatura': candidatura,
            'messaggi': messaggi,
            'id': utente.id,
            'last_message_id': last_message_id
        })
    else:
        return redirect("login")


def index(request):
    Messaggio.objects.all().delete()
    # User.objects.all().delete()
    return redirect("intro")


def logout(request):
    if 'username' in request.session:
        del request.session['username']
    return redirect('login')
