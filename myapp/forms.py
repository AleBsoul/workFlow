from django import forms

class SignUpForm(forms.Form):
    username = forms.CharField(max_length=20, label="username")
    password = forms.CharField(widget=forms.PasswordInput, label="password")
    competenze = forms.CharField(widget=forms.Textarea, label="descrizione")
    type = forms.ChoiceField(label='type', 
        choices=[('1','candidato'),('2','datore di lavoro')], 
    )


class LogInForm(forms.Form):
    username = forms.CharField(max_length=20, label="username")
    password = forms.CharField(widget=forms.PasswordInput, label="password")
