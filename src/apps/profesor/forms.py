#-*- coding: utf-8 -*-

from django import forms

from infosys.models import Ocena, Dijak, Stars, Dogodek, ZakljucenaOcena, OCENE

class OcenaForm(forms.ModelForm):
    ocena = forms.ChoiceField(OCENE)
    
    class Meta:
        model = Ocena
        exclude = ('dijak', 'ocena_stevilka')

class OcenaPoucujeForm(forms.ModelForm):
    ocena = forms.ChoiceField(OCENE)
    
    class Meta:
        model = Ocena
        exclude = ('dijak', 'ocena_stevilka', 'poucuje')

class ZakljucenaOcenaPoucujeForm(forms.ModelForm):
    ocena = forms.ChoiceField(OCENE)
    
    class Meta:
        model = ZakljucenaOcena
        exclude = ('dijak', 'ocena_stevilka', 'poucuje')

class DogodekForm(forms.ModelForm):
    class Meta:
        model = Dogodek

class DogodekPoucujeForm(forms.ModelForm):
    class Meta:
        model = Dogodek
        exclude = ('poucuje',)

class DijakForm(forms.ModelForm):
    class Meta:
        model = Dijak
        exclude = ('uporabnik', 'oce', 'mati')

class StarsForm(forms.ModelForm):
    class Meta:
        model = Stars
        exclude = ('uporabnik')
