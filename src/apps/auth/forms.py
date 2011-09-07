#-*- coding: utf-8 -*-

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

class LoginForm(AuthenticationForm):
    remember = forms.BooleanField(initial=False, required=False)

class NastavitveForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput, required=False)
    password1 = forms.CharField(widget=forms.PasswordInput, required=False)
    password2 = forms.CharField(widget=forms.PasswordInput, required=False)
    
    def __init__(self, request, *args, **kwargs):
        kwargs['initial'] = {'email': request.user.email}
        
        super(NastavitveForm, self).__init__(*args, **kwargs)
        
        self.request = request
        self.user = request.user
        
        self.new_password = None
    
    def clean(self):
        password = self.cleaned_data.get('password', None)
        password1 = self.cleaned_data.get('password1', None)
        password2 = self.cleaned_data.get('password2', None)
        
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(u'Gesli se ne ujemata.')
            else:
                if not password:
                    raise forms.ValidationError(u'Za spremembo gesla morate vpisati staro geslo.')
                else:
                    if not authenticate(username=self.user.username, password=password):
                        raise forms.ValidationError(u'Vaše staro geslo ni pravilno.')
                    else:
                        if len(password1) < 6:
                            raise forms.ValidationError(u'Vaše geslo je prekratko (vsaj 6 znakov)')
                        else:
                            self.new_password = password1
        
        return self.cleaned_data
    
    def save(self):
        messages.info(self.request, u'Vaše nastavitve so shranjene.')
        
        if self.new_password:
            self.user.set_password(self.new_password)
            messages.info(self.request, u'Vaše geslo je spremenjeno.')
        
        self.user.email = self.cleaned_data['email']
        
        self.user.save()

class UserForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField(required=False)
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
