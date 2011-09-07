#-*- coding: utf-8 -*-

from django import forms
from infosys.models import Naslov

class NaslovForm(forms.ModelForm):
    class Meta:
        model = Naslov
