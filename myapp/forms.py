from django import forms

class SignUpForm(forms.Form):
    username = forms.CharField(max_length=20, label="username")
    password = forms.CharField(widget=forms.PasswordInput, label="password")
    nome = forms.CharField(max_length=20, label="nome")
    cognome = forms.CharField(max_length=20, label="cognome")
    email = forms.CharField(widget=forms.EmailInput, label="email")
    nome = forms.CharField(max_length=20, label="nome")
    cognome = forms.CharField(max_length=20, label="cognome")
    email = forms.CharField(widget=forms.EmailInput, label="email")
    type = forms.ChoiceField(label='type', 
        choices=[('candidato','1'),('datore','2')]
    )


class LogInForm(forms.Form):
    username = forms.CharField(max_length=20, label="username")
    password = forms.CharField(widget=forms.PasswordInput, label="password")

class Compl_Signup_Cand(forms.Form):
    residenza = forms.CharField(max_length=30, label='residenza')
    competenze = forms.CharField(max_length=200, widget=forms.Textarea, label='competenze')

class Compl_Signup_Datore(forms.Form):
    azienda = forms.CharField(max_length=30, label="azienda")