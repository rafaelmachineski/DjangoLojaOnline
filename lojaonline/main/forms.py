from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm



class AtualizarCadastroForm(forms.Form):
    nome = forms.CharField(max_length=65)
    sobrenome = forms.CharField(max_length=65)
    email = forms.EmailField()

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(AtualizarCadastroForm, self).__init__(*args, **kwargs)


        self.fields['nome'].widget.attrs['value'] = self.user.first_name
        self.fields['nome'].widget.attrs['class'] = 'form-control'
        self.fields['sobrenome'].widget.attrs['value'] = self.user.last_name
        self.fields['sobrenome'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['value'] = self.user.email
        self.fields['email'].widget.attrs['class'] = 'form-control'



class LoginForm(forms.Form):
    username = forms.CharField(max_length=65)
    password = forms.CharField(max_length=65, widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'password']:
            self.fields[fieldname].help_text = None
            self.fields[fieldname].widget.attrs['class'] = 'form-control'



class RegisterForm(UserCreationForm):
    class Meta:
        model=User
        fields = ['username','email','password1','password2']
   
    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'email', 'password1', 'password2']:
            self.fields[fieldname].help_text = None
            self.fields[fieldname].widget.attrs['class'] = 'form-control'
        


class AdicionarCarrinhoForm(forms.Form):
    quantidade = forms.IntegerField(required=True)
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)