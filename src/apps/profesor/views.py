#-*- coding: utf-8 -*-

from datetime import datetime
import time

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.db.models import Avg
from django.conf import settings
from django.core.mail import send_mail

from dacks.views import render, Resource
from auth.forms import NastavitveForm, UserForm
from dacks.utils import get_int_or_none
from core.utils import form_data_empty, not_none_or_404, get_object_or_none
from infosys.views import profesor_required
from profesor.utils import poucuje_predmet_label, dogodek_label

from infosys.models import Dogodek, Dijak

from profesor.forms import DijakForm, StarsForm, OcenaForm, DogodekForm,\
    DogodekPoucujeForm, OcenaPoucujeForm, ZakljucenaOcenaPoucujeForm
from infosys.forms import NaslovForm
from django.template.loader import render_to_string

resource = urlpatterns = Resource()

@resource(r'^/$', 'profesor')
@login_required
@profesor_required
@render('profesor/profesor.html')
def profesor(request):
    profesor = request.user_profile
    
    predmeti = profesor.predmeti
    razredi = profesor.razredi
    
    return locals()

@resource(r'^/nastavitve$', 'profesor_nastavitve')
@login_required
@profesor_required
@render('profesor/nastavitve.html')
def nastavitve(request):
    profesor = request.user_profile
    
    form = NastavitveForm(request, data=request.POST or None)
    
    if form.is_valid():
        form.save()
    
    return locals()

@resource(r'^/predmeti/(?P<predmet>\d+)$', 'profesor_predmeti_predmet')
@login_required
@profesor_required
@render('profesor/predmeti/predmet.html')
def predmeti_predmet(request, predmet):
    profesor = request.user_profile
    predmet = get_object_or_404(profesor.predmeti, id=predmet)
    
    razredi = profesor.get_predmet_razredi(predmet)
    
    return locals()

@resource(r'^/predmeti/(?P<predmet>\d+)/razredi/(?P<razred>\d+)$', 'profesor_predmeti_razredi_razred')
@login_required
@profesor_required
@render('profesor/predmeti/razredi/razred.html')
def predmeti_razredi_razred(request, predmet, razred):
    profesor = request.user_profile
    poucuje = get_object_or_404(profesor.poucuje, predmet=predmet, razred=razred)
    predmet = poucuje.predmet
    razred = poucuje.razred
    
    dijaki = razred.dijaki_cached
    
    prihajajoci_dogodki = razred.prihajajoci_dogodki[:5]
    
    return locals()

@resource(r'^/predmeti/(?P<predmet>\d+)/razredi/(?P<razred>\d+)/natisni$', 'profesor_predmeti_razredi_razred_natisni')
@login_required
@profesor_required
@render('print/razred.html')
def predmeti_razredi_razred_natisni(request, predmet, razred):
    profesor = request.user_profile
    poucuje = get_object_or_404(profesor.poucuje, predmet=predmet, razred=razred)
    predmet = poucuje.predmet
    razred = poucuje.razred
    
    dijaki = razred.dijaki_cached
    
    return locals()

@resource(r'^/predmeti/(?P<predmet>\d+)/razredi/(?P<razred>\d+)/dogodki$', 'profesor_predmeti_razredi_dogodki')
@login_required
@profesor_required
@render('profesor/predmeti/razredi/dogodki/dogodki.html')
def predmeti_razredi_dogodki(request, predmet, razred):
    profesor = request.user_profile
    poucuje = get_object_or_404(profesor.poucuje, predmet=predmet, razred=razred)
    predmet = poucuje.predmet
    razred = poucuje.razred
    
    prihajajoci_dogodki = razred.prihajajoci_dogodki
    pretekli_dogodki = razred.pretekli_dogodki
    
    return locals()

@resource(r'^/predmeti/(?P<predmet>\d+)/razredi/(?P<razred>\d+)/dogodki/(?P<dogodek>\d+)$', 'profesor_predmeti_razredi_dogodki_dogodek')
@login_required
@profesor_required
@render('profesor/predmeti/razredi/dogodki/dogodek.html')
def predmeti_razredi_dogodki_dogodek(request, predmet, razred, dogodek):
    profesor = request.user_profile
    poucuje = get_object_or_404(profesor.poucuje, predmet=predmet, razred=razred)
    predmet = poucuje.predmet
    razred = poucuje.razred
    
    dogodek = get_object_or_404(razred.dogodki, id=dogodek)
    
    ocene = dict([(x.dijak, x) for x in dogodek.ocene])
    
    dijaki = list(razred.dijaki.all())
    
    for dijak in dijaki:
        dijak.ocena = ocene.get(dijak, None)
    
    return locals()

@resource(r'^/predmeti/(?P<predmet>\d+)/razredi/(?P<razred>\d+)/dogodki/dodaj$', 'profesor_predmeti_razredi_dogodki_dodaj')
@login_required
@profesor_required
@render('profesor/predmeti/razredi/dogodki/dogodek_dodaj.html')
def predmeti_razredi_dogodki_dodaj(request, predmet, razred):
    profesor = request.user_profile
    poucuje = get_object_or_404(profesor.poucuje, predmet=predmet, razred=razred)
    predmet = poucuje.predmet
    razred = poucuje.razred
    
    form = DogodekPoucujeForm(data=request.POST or None)
    
    if form.is_valid():
        dogodek = form.save(commit=False)
        dogodek.poucuje = poucuje
        dogodek.save()
        
        messages.info(request, u'Dogodek je dodan.')
        
        return HttpResponseRedirect(reverse('profesor_predmeti_razredi_dogodki_dogodek', args=[predmet.id, razred.id, dogodek.id]))
    
    return locals()

@resource(r'^/predmeti/(?P<predmet>\d+)/razredi/(?P<razred>\d+)/dogodki/(?P<dogodek>\d+)/uredi$', 'profesor_predmeti_razredi_dogodki_uredi')
@login_required
@profesor_required
@render('profesor/predmeti/razredi/dogodki/dogodek_uredi.html')
def predmeti_razredi_dogodki_uredi(request, predmet, razred, dogodek):
    profesor = request.user_profile
    poucuje = get_object_or_404(profesor.poucuje, predmet=predmet, razred=razred)
    predmet = poucuje.predmet
    razred = poucuje.razred
    dogodki = Dogodek.objects.filter(poucuje=poucuje)
    
    dogodek = get_object_or_404(dogodki, id=dogodek)
    
    form = DogodekPoucujeForm(instance=dogodek, data=request.POST or None)
    
    if form.is_valid():
        dogodek = form.save(commit=False)
        dogodek.poucuje = poucuje
        dogodek.save()
        
        messages.info(request, u'Podatki o dogodku so shranjeni.')
        
        return HttpResponseRedirect(reverse('profesor_predmeti_razredi_dogodki_dogodek', args=[predmet.id, razred.id, dogodek.id]))
    
    return locals()

@resource(r'^/predmeti/(?P<predmet>\d+)/razredi/(?P<razred>\d+)/dogodki/(?P<dogodek>\d+)/izbrisi$', 'profesor_predmeti_razredi_dogodki_izbrisi')
@login_required
@profesor_required
def predmeti_razredi_dogodki_izbrisi(request, predmet, razred, dogodek):
    profesor = request.user_profile
    poucuje = get_object_or_404(profesor.poucuje, predmet=predmet, razred=razred)
    predmet = poucuje.predmet
    razred = poucuje.razred
    dogodki = Dogodek.objects.filter(poucuje=poucuje)
    dogodek = get_object_or_404(dogodki, id=dogodek)
    
    dogodek.delete()
    
    return HttpResponseRedirect(reverse('profesor_predmeti_razredi_dogodki', args=[predmet.id, razred.id]))

@resource(r'^/predmeti/(?P<predmet>\d+)/razredi/(?P<razred>\d+)/dijaki/(?P<dijak>\d+)$', 'profesor_predmeti_razredi_dijaki_dijak')
@resource(r'^/predmeti/(?P<predmet>\d+)/razredi/(?P<razred>\d+)/dijaki/(?P<dijak>\d+)/ocene$', 'profesor_predmeti_razredi_dijaki_ocene')
@login_required
@profesor_required
@render('profesor/predmeti/razredi/dijaki/ocene/ocene.html')
def predmeti_razredi_dijaki_ocene(request, predmet, razred, dijak):
    profesor = request.user_profile
    poucuje = get_object_or_404(profesor.poucuje, predmet=predmet, razred=razred)
    predmet = poucuje.predmet
    razred = poucuje.razred
    dijak = get_object_or_404(razred.dijaki_cached, id=dijak)
    
    ppredmet = get_int_or_none(request.GET, 'p')
    ocenjevalno_obdobje = get_int_or_none(request.GET, 'oo')
    
    ocene = dijak.get_ocene(predmet=ppredmet, ocenjevalno_obdobje=ocenjevalno_obdobje)
    
    return locals()

@resource(r'^/predmeti/(?P<predmet>\d+)/razredi/(?P<razred>\d+)/dijaki/(?P<dijak>\d+)/ocene/natisni$', 'profesor_predmeti_razredi_dijaki_ocene_natisni')
@login_required
@profesor_required
@render('print/ocene.html')
def predmeti_razredi_dijaki_ocene_natisni(request, predmet, razred, dijak):
    profesor = request.user_profile
    poucuje = get_object_or_404(profesor.poucuje, predmet=predmet, razred=razred)
    predmet = poucuje.predmet
    razred = poucuje.razred
    dijak = get_object_or_404(razred.dijaki_cached, id=dijak)
    
    ocene = dijak.get_ocene()
    
    return locals()

@resource(r'^/predmeti/(?P<predmet>\d+)/razredi/(?P<razred>\d+)/dijaki/(?P<dijak>\d+)/ocene/(?P<ocena>\d+)$', 'profesor_predmeti_razredi_dijaki_ocene_ocena')
@login_required
@profesor_required
@render('profesor/predmeti/razredi/dijaki/ocene/ocena.html')
def predmeti_razredi_dijaki_ocene_ocena(request, predmet, razred, dijak, ocena):
    profesor = request.user_profile
    poucuje = get_object_or_404(profesor.poucuje, predmet=predmet, razred=razred)
    predmet = poucuje.predmet
    razred = poucuje.razred
    dijak = get_object_or_404(razred.dijaki_cached, id=dijak)
    
    ocena = get_object_or_404(dijak.ocene_base, id=ocena)
    
    return locals()

@resource(r'^/predmeti/(?P<predmet>\d+)/razredi/(?P<razred>\d+)/dijaki/(?P<dijak>\d+)/ocene/dodaj$', 'profesor_predmeti_razredi_dijaki_ocene_dodaj')
@resource(r'^/predmeti/(?P<predmet>\d+)/razredi/(?P<razred>\d+)/dijaki/(?P<dijak>\d+)/ocene/dodaj/dogodki/(?P<dogodek>\d+)$', 'profesor_predmeti_razredi_dijaki_ocene_dodaj_dogodek')
@login_required
@profesor_required
@render('profesor/predmeti/razredi/dijaki/ocene/ocena_dodaj.html')
def predmeti_razredi_dijaki_ocene_dodaj(request, predmet, razred, dijak, dogodek=None):
    profesor = request.user_profile
    poucuje = get_object_or_404(profesor.poucuje, predmet=predmet, razred=razred)
    predmet = poucuje.predmet
    razred = poucuje.razred
    dijak = get_object_or_404(razred.dijaki_cached, id=dijak)
    
    dogodki = Dogodek.objects.filter(poucuje=poucuje)
    
    initial = {
        'datum_pridobitve': datetime.today(),
    }
    
    if dogodek:
        dogodek = get_object_or_404(dogodki, id=dogodek)
        initial['dogodek'] = dogodek
    
    form = OcenaPoucujeForm(data=request.POST or None, initial=initial)
    form.fields['dogodek'].queryset = dogodki
    form.fields['dogodek'].label_from_instance = dogodek_label
    
    if form.is_valid():
        ocena = form.save(commit=False)
        ocena.dijak = dijak
        ocena.poucuje = poucuje
        ocena.save()
        
        messages.info(request, u'Ocena je dodana.')
        
        return HttpResponseRedirect(reverse('profesor_predmeti_razredi_dijaki_ocene_ocena', args=[predmet.id, razred.id, dijak.id, ocena.id]))
    
    return locals()

@resource(r'^/predmeti/(?P<predmet>\d+)/razredi/(?P<razred>\d+)/dijaki/(?P<dijak>\d+)/ocene/(?P<ocena>\d+)/uredi$', 'profesor_predmeti_razredi_dijaki_ocene_uredi')
@login_required
@profesor_required
@render('profesor/predmeti/razredi/dijaki/ocene/ocena_uredi.html')
def predmeti_razredi_dijaki_ocene_uredi(request, predmet, razred, dijak, ocena):
    profesor = request.user_profile
    poucuje = get_object_or_404(profesor.poucuje, predmet=predmet, razred=razred)
    predmet = poucuje.predmet
    razred = poucuje.razred
    dijak = get_object_or_404(razred.dijaki_cached, id=dijak)
    ocena = get_object_or_404(dijak.ocene_base, id=ocena)
    
    form = OcenaPoucujeForm(instance=ocena, data=request.POST or None)
    dogodki = Dogodek.objects.filter(poucuje=poucuje)
    form.fields['dogodek'].queryset = dogodki
    form.fields['dogodek'].label_from_instance = dogodek_label
    
    if form.is_valid():
        ocena = form.save(commit=False)
        ocena.dijak = dijak
        ocena.poucuje = poucuje
        ocena.save()
        
        messages.info(request, u'Podatki o oceni so shranjeni.')
        
        return HttpResponseRedirect(reverse('profesor_predmeti_razredi_dijaki_ocene_ocena', args=[predmet.id, razred.id, dijak.id, ocena.id]))
    
    return locals()

@resource(r'^/predmeti/(?P<predmet>\d+)/razredi/(?P<razred>\d+)/dijaki/(?P<dijak>\d+)/ocene/(?P<ocena>\d+)/izbrisi$', 'profesor_predmeti_razredi_dijaki_ocene_izbrisi')
@login_required
@profesor_required
def predmeti_razredi_dijaki_ocene_izbrisi(request, predmet, razred, dijak, ocena):
    profesor = request.user_profile
    poucuje = get_object_or_404(profesor.poucuje, predmet=predmet, razred=razred)
    predmet = poucuje.predmet
    razred = poucuje.razred
    dijak = get_object_or_404(razred.dijaki_cached, id=dijak)
    ocena = get_object_or_404(dijak.ocene_base, id=ocena)
    
    ocena.delete()
    
    return HttpResponseRedirect(reverse('profesor_predmeti_razredi_dijaki_ocene', args=[predmet.id, razred.id, dijak.id]))

@resource(r'^/predmeti/(?P<predmet>\d+)/razredi/(?P<razred>\d+)/dijaki/(?P<dijak>\d+)/ocene/zakljuci$', 'profesor_predmeti_razredi_dijaki_ocene_zakljuci')
@login_required
@profesor_required
@render('profesor/predmeti/razredi/dijaki/ocene/zakljuci.html')
def predmeti_razredi_dijaki_ocene_zakljuci(request, predmet, razred, dijak):
    profesor = request.user_profile
    poucuje = get_object_or_404(profesor.poucuje, predmet=predmet, razred=razred)
    predmet = poucuje.predmet
    razred = poucuje.razred
    dijak = get_object_or_404(razred.dijaki_cached, id=dijak)
    
    ocenjevalno_obdobje = get_int_or_none(request.GET, 'oo')
    ocene = dijak.get_ocene(predmet=predmet.id, ocenjevalno_obdobje=ocenjevalno_obdobje)
    
    povprecje = dijak.ocene_base.filter(poucuje=poucuje) \
                    .aggregate(povprecje=Avg('ocena_stevilka'))['povprecje']
    
    zakljucena_ocena = get_object_or_none(dijak.zakljucene_ocene_base, poucuje=poucuje)
    
    initial = {
        'datum_pridobitve': datetime.today(),
    }
    
    form = ZakljucenaOcenaPoucujeForm(instance=zakljucena_ocena, data=request.POST or None, initial=initial)
    
    if form.is_valid():
        zocena = form.save(commit=False)
        zocena.dijak = dijak
        zocena.poucuje = poucuje
        zocena.save()
        
        messages.info(request, u'Predmet je zaključen.')
        
        return HttpResponseRedirect(reverse('profesor_predmeti_razredi_dijaki_ocene', args=[predmet.id, razred.id, dijak.id]))
    
    return locals()

@resource(r'^/predmeti/(?P<predmet>\d+)/razredi/(?P<razred>\d+)/dijaki/(?P<dijak>\d+)/ocene/zakljuci/izbrisi$', 'profesor_predmeti_razredi_dijaki_ocene_zakljuci_izbrisi')
@login_required
@profesor_required
def predmeti_razredi_dijaki_ocene_zakljuci_izbrisi(request, predmet, razred, dijak):
    profesor = request.user_profile
    poucuje = get_object_or_404(profesor.poucuje, predmet=predmet, razred=razred)
    predmet = poucuje.predmet
    razred = poucuje.razred
    dijak = get_object_or_404(razred.dijaki_cached, id=dijak)
    
    zakljucena_ocena = get_object_or_404(dijak.zakljucene_ocene_base, poucuje=poucuje)
    
    zakljucena_ocena.delete()
    
    messages.info(request, u'Zaključena ocena je izbrisana.')
    
    return HttpResponseRedirect(reverse('profesor_predmeti_razredi_dijaki_ocene', args=[predmet.id, razred.id, dijak.id]))

@resource(r'^/predmeti/(?P<predmet>\d+)/razredi/(?P<razred>\d+)/dijaki/(?P<dijak>\d+)/podatki$', 'profesor_predmeti_razredi_dijaki_podatki')
@login_required
@profesor_required
@render('profesor/predmeti/razredi/dijaki/podatki.html')
def predmeti_razredi_dijaki_podatki(request, predmet, razred, dijak):
    profesor = request.user_profile
    poucuje = get_object_or_404(profesor.poucuje, predmet=predmet, razred=razred)
    predmet = poucuje.predmet
    razred = poucuje.razred
    
    dijak = get_object_or_404(razred.dijaki_cached, id=dijak)
    
    return locals()

@resource(r'^/razredi/(?P<razred>\d+)$', 'profesor_razredi_razred')
@login_required
@profesor_required
@render('profesor/razredi/razred.html')
def razredi_razred(request, razred):
    profesor = request.user_profile
    razred = get_object_or_404(profesor.razredi, id=razred)
    
    dijaki = razred.dijaki_cached
    
    prihajajoci_dogodki = razred.prihajajoci_dogodki[:5]
    
    return locals()

@resource(r'^/razredi/(?P<razred>\d+)/natisni$', 'profesor_razredi_razred_natisni')
@login_required
@profesor_required
@render('print/razred.html')
def razredi_razred_natisni(request, razred):
    profesor = request.user_profile
    razred = get_object_or_404(profesor.razredi, id=razred)
    
    dijaki = razred.dijaki_cached
    
    return locals()

@resource(r'^/razredi/(?P<razred>\d+)/statistika$', 'profesor_razredi_statistika')
@login_required
@profesor_required
@render('profesor/razredi/statistika.html')
def razredi_statistika(request, razred):
    profesor = request.user_profile
    razred = get_object_or_404(profesor.razredi, id=razred)
    
    ocene_data = razred.statistika_ocene()
    
    ocene = []
    
    for ocena, ds in ocene_data:
        ocene.append({
            'label': ocena,
            'data': ds
        })
    
    ocene_data = razred.statistika_ocene()
    
    po_mesecih_data = razred.statistika_po_mesecih()
    
    po_mesecih = []
    
    for range, povprecje in po_mesecih_data:
        po_mesecih.append([
            int(time.mktime(range[0].timetuple()) * 1000),
            povprecje
        ])
    
    dijaki = razred.statistika_dijaki()
    
    return locals()

@resource(r'^/razredi/(?P<razred>\d+)/dijaki/(?P<dijak>\d+)$', 'profesor_razredi_dijaki_dijak')
@login_required
@profesor_required
@render('profesor/razredi/dijaki/dijak.html')
def razredi_dijaki_dijak(request, razred, dijak):
    profesor = request.user_profile
    razred = get_object_or_404(profesor.razredi, id=razred)
    dijak = get_object_or_404(razred.dijaki_cached, id=dijak)
    
    zadnje_ocene = dijak.zadnje_ocene[:5]
    
    return locals()

@resource(r'^/razredi/(?P<razred>\d+)/dijaki/(?P<dijak>\d+)/ocene$', 'profesor_razredi_dijaki_ocene')
@login_required
@profesor_required
@render('profesor/razredi/dijaki/ocene/ocene.html')
def razredi_dijaki_ocene(request, razred, dijak):
    profesor = request.user_profile
    razred = get_object_or_404(profesor.razredi, id=razred)
    dijak = get_object_or_404(razred.dijaki_cached, id=dijak)
    
    predmet = get_int_or_none(request.GET, 'p')
    ocenjevalno_obdobje = get_int_or_none(request.GET, 'oo')
    
    ocene = dijak.get_ocene(predmet=predmet, ocenjevalno_obdobje=ocenjevalno_obdobje)
    
    return locals()

@resource(r'^/razredi/(?P<razred>\d+)/dijaki/(?P<dijak>\d+)/ocene/natisni$', 'profesor_razredi_dijaki_ocene_natisni')
@login_required
@profesor_required
@render('print/ocene.html')
def razredi_dijaki_ocene_natisni(request, razred, dijak):
    profesor = request.user_profile
    razred = get_object_or_404(profesor.razredi, id=razred)
    dijak = get_object_or_404(razred.dijaki_cached, id=dijak)
    
    ocene = dijak.get_ocene()
    
    return locals()

@resource(r'^/razredi/(?P<razred>\d+)/dijaki/(?P<dijak>\d+)/ocene/(?P<ocena>\d+)$', 'profesor_razredi_dijaki_ocene_ocena')
@login_required
@profesor_required
@render('profesor/razredi/dijaki/ocene/ocena.html')
def razredi_dijaki_ocene_ocena(request, razred, dijak, ocena):
    profesor = request.user_profile
    razred = get_object_or_404(profesor.razredi, id=razred)
    dijak = get_object_or_404(razred.dijaki_cached, id=dijak)
    
    ocena = get_object_or_404(dijak.ocene_base, id=ocena)
    
    return locals()

@resource(r'^/razredi/(?P<razred>\d+)/dijaki/(?P<dijak>\d+)/ocene/(?P<ocena>\d+)/uredi$', 'profesor_razredi_dijaki_ocene_uredi')
@login_required
@profesor_required
@render('profesor/razredi/dijaki/ocene/ocena_uredi.html')
def razredi_dijaki_ocene_uredi(request, razred, dijak, ocena):
    profesor = request.user_profile
    razred = get_object_or_404(profesor.razredi, id=razred)
    dijak = get_object_or_404(razred.dijaki_cached, id=dijak)
    ocena = get_object_or_404(dijak.ocene_base, id=ocena)
    
    form = OcenaForm(instance=ocena, data=request.POST or None)
    
    form.fields['dogodek'].queryset = dijak.dogodki
    form.fields['dogodek'].label_from_instance = dogodek_label
    form.fields['poucuje'].queryset = dijak.poucuje
    form.fields['poucuje'].label_from_instance = poucuje_predmet_label
    
    if form.is_valid():
        ocena = form.save(commit=False)
        ocena.dijak = dijak
        ocena.save()
        
        messages.info(request, u'Podatki o oceni so shranjeni.')
        
        return HttpResponseRedirect(reverse('profesor_razredi_dijaki_ocene_ocena', args=[razred.id, dijak.id, ocena.id]))
    
    return locals()

@resource(r'^/razredi/(?P<razred>\d+)/dijaki/(?P<dijak>\d+)/podatki$', 'profesor_razredi_dijaki_podatki')
@login_required
@profesor_required
@render('profesor/razredi/dijaki/podatki.html')
def razredi_dijaki_podatki(request, razred, dijak):
    profesor = request.user_profile
    razred = get_object_or_404(profesor.razredi, id=razred)
    
    dijak = get_object_or_404(razred.dijaki_cached, id=dijak)
    
    return locals()

@resource(r'^/razredi/(?P<razred>\d+)/dijaki/dodaj', 'profesor_razredi_dijaki_dijak_dodaj')
@login_required
@profesor_required
@render('profesor/razredi/dijaki/dijak_dodaj.html')
def razredi_dijaki_dijak_dodaj(request, razred):
    profesor = request.user_profile
    razred = get_object_or_404(profesor.razredi, id=razred)
    
    data = request.POST if request.method == 'POST' else None
    
    form = UserForm(data=data)
    
    if form.is_valid():
        user = form.save(commit=False)
        user.gen_username()
        user.set_unusable_password()
        user.save()
        
        dijak = Dijak.objects.create(uporabnik=user)
        
        razred.dijaki.add(dijak)
        
        messages.info(request, u'Dijak je dodan.')
        
        return HttpResponseRedirect(reverse('profesor_razredi_dijaki_dijak_uredi', args=[razred.id, dijak.id]))
    
    return locals()

@resource(r'^/razredi/(?P<razred>\d+)/dijaki/(?P<dijak>\d+)/uredi$', 'profesor_razredi_dijaki_dijak_uredi')
@login_required
@profesor_required
@render('profesor/razredi/dijaki/dijak_uredi.html')
def razredi_dijaki_dijak_uredi(request, razred, dijak):
    profesor = request.user_profile
    razred = get_object_or_404(profesor.razredi, id=razred)
    dijak = get_object_or_404(razred.dijaki_cached, id=dijak)
    
    data = request.POST if request.method == 'POST' else None
    
    user_form = UserForm(instance=dijak.uporabnik, data=data, prefix='user')
    dijak_form = DijakForm(instance=dijak, data=data, prefix='dijak')
    sp_form = NaslovForm(instance=dijak.stalno_prebivalisce, data=data, prefix='sp')
    zp_form = NaslovForm(instance=dijak.zacasno_prebivalisce, data=data, prefix='zp')
    
    valid = True
    
    if user_form.is_valid() and dijak_form.is_valid():
        user = user_form.save(commit=False)
        dijak = dijak_form.save(commit=False)
        
        sp = None
        zp = None
        
        if not form_data_empty(sp_form):
            if sp_form.is_valid():
                sp = sp_form.save(commit=False)
            else:
                valid = False
        
        if not form_data_empty(zp_form):
            if zp_form.is_valid():
                zp = zp_form.save(commit=False)
            else:
                valid = False
        
        if valid:
            if sp:
                sp.save()
            
            if zp:
                zp.save()
            
            dijak.stalno_prebivalisce = sp
            dijak.zacasno_prebivalisce = zp
            
            user.save()
            dijak.save()
        
    else:
        valid = False
            
    if valid:
        messages.info(request, u'Podatki o dijaku so shranjeni.')
        
        return HttpResponseRedirect(reverse('profesor_razredi_dijaki_podatki', args=[razred.id, dijak.id]))
    
    return locals()

@resource(r'^/razredi/(?P<razred>\d+)/dijaki/(?P<dijak>\d+)/izbrisi', 'profesor_razredi_dijaki_dijak_izbrisi')
@login_required
@profesor_required
def razredi_dijaki_dijak_izbrisi(request, razred, dijak):
    profesor = request.user_profile
    razred = get_object_or_404(profesor.razredi, id=razred)
    dijak = get_object_or_404(razred.dijaki_cached, id=dijak)
    
    oce_uporabnik = dijak.oce.uporabnik if dijak.oce else None
    mati_uporabnik = dijak.mati.uporabnik if dijak.mati else None
    dijak_uporabnik = dijak.uporabnik
    
    dijak_uporabnik.delete()
    
    if oce_uporabnik:
        oce_uporabnik.delete()
    
    if mati_uporabnik:
        mati_uporabnik.delete()
    
    return HttpResponseRedirect(reverse('profesor_razredi_razred', args=[razred.id]))

def poslji_novo_geslo(request, uporabnisko_ime, geslo, email):
    login_url = request.build_absolute_uri(reverse('home'))
    
    message = render_to_string('email/novo_geslo.html', dict(
        uporabnisko_ime=uporabnisko_ime,
        geslo=geslo,
        login_url=login_url
    ))
    
    send_mail(
        'Novo geslo v eRedovalnici',
        message,
        settings.SENDER_EMAIL,
        [email],
        fail_silently=False
    )

@resource(r'^/razredi/(?P<razred>\d+)/dijaki/(?P<dijak>\d+)/novo-geslo$', 'profesor_razredi_dijaki_dijak_novo_geslo')
@login_required
@profesor_required
@render('profesor/razredi/dijaki/dijak_novo_geslo.html')
def razredi_dijaki_dijak_novo_geslo(request, razred, dijak):
    profesor = request.user_profile
    razred = get_object_or_404(profesor.razredi, id=razred)
    dijak = get_object_or_404(razred.dijaki_cached, id=dijak)
    
    uporabnisko_ime = dijak.uporabnik.username
    geslo = dijak.uporabnik.gen_password()
    dijak.uporabnik.save()
    
    poslji_novo_geslo(request, uporabnisko_ime, geslo, dijak.uporabnik.email)
    
    return locals()

@resource(r'^/razredi/(?P<razred>\d+)/dijaki/(?P<dijak>\d+)/oce/uredi$', 'profesor_razredi_dijaki_oce_uredi')
@login_required
@profesor_required
@render('profesor/razredi/dijaki/oce_uredi.html')
def razredi_dijaki_oce_uredi(request, razred, dijak):
    profesor = request.user_profile
    razred = get_object_or_404(profesor.razredi, id=razred)
    dijak = get_object_or_404(razred.dijaki_cached, id=dijak)
    
    stars = dijak.oce
    
    data = request.POST if request.method == 'POST' else None
    
    user_form = UserForm(instance=stars.uporabnik if stars else None, data=data, prefix='user')
    stars_form = StarsForm(instance=stars, data=data, prefix='stars')
    p_form = NaslovForm(instance=stars.prebivalisce if stars else None, data=data, prefix='p')
    
    valid = True
    
    if user_form.is_valid() and stars_form.is_valid():
        user = user_form.save(commit=False)
        stars = stars_form.save(commit=False)
        
        p = None
        
        if not form_data_empty(p_form):
            if p_form.is_valid():
                p = p_form.save(commit=False)
            else:
                valid = False
        
        if valid:
            if p:
                p.save()
            
            stars.prebivalisce = p
            
            if not user.id:
                user.gen_username()
                user.set_unusable_password()
            
            user.save()
            
            stars.uporabnik = user
            stars.save()
            
            dijak.oce = stars
            dijak.save()
        
    else:
        valid = False
            
    if valid:
        messages.info(request, u'Podatki o očetu so shranjeni.')
        
        return HttpResponseRedirect(reverse('profesor_razredi_dijaki_podatki', args=[razred.id, dijak.id]))
    
    return locals()

@resource(r'^/razredi/(?P<razred>\d+)/dijaki/(?P<dijak>\d+)/oce/izbrisi', 'profesor_razredi_dijaki_oce_izbrisi')
@login_required
@profesor_required
def razredi_dijaki_oce_izbrisi(request, razred, dijak):
    profesor = request.user_profile
    razred = get_object_or_404(profesor.razredi, id=razred)
    dijak = get_object_or_404(razred.dijaki_cached, id=dijak)
    stars = not_none_or_404(dijak.oce)
    
    dijak.oce = None
    dijak.save()
    
    su = stars.uporabnik
    stars.delete()
    su.delete()
    
    return HttpResponseRedirect(reverse('profesor_razredi_dijaki_podatki', args=[razred.id, dijak.id]))

@resource(r'^/razredi/(?P<razred>\d+)/dijaki/(?P<dijak>\d+)/oce/novo-geslo$', 'profesor_razredi_dijaki_oce_novo_geslo')
@login_required
@profesor_required
@render('profesor/razredi/dijaki/oce_novo_geslo.html')
def razredi_dijaki_oce_novo_geslo(request, razred, dijak):
    profesor = request.user_profile
    razred = get_object_or_404(profesor.razredi, id=razred)
    dijak = get_object_or_404(razred.dijaki_cached, id=dijak)
    stars = not_none_or_404(dijak.oce)
    
    uporabnisko_ime = stars.uporabnik.username
    geslo = stars.uporabnik.gen_password()
    stars.uporabnik.save()
    
    poslji_novo_geslo(request, uporabnisko_ime, geslo, stars.uporabnik.email)
    
    return locals()

@resource(r'^/razredi/(?P<razred>\d+)/dijaki/(?P<dijak>\d+)/mati/uredi$', 'profesor_razredi_dijaki_mati_uredi')
@login_required
@profesor_required
@render('profesor/razredi/dijaki/mati_uredi.html')
def razredi_dijaki_mati_uredi(request, razred, dijak):
    profesor = request.user_profile
    razred = get_object_or_404(profesor.razredi, id=razred)
    dijak = get_object_or_404(razred.dijaki_cached, id=dijak)
    
    stars = dijak.mati
    
    data = request.POST if request.method == 'POST' else None
    
    user_form = UserForm(instance=stars.uporabnik if stars else None, data=data, prefix='user')
    stars_form = StarsForm(instance=stars, data=data, prefix='stars')
    p_form = NaslovForm(instance=stars.prebivalisce if stars else None, data=data, prefix='p')
    
    valid = True
    
    if user_form.is_valid() and stars_form.is_valid():
        user = user_form.save(commit=False)
        stars = stars_form.save(commit=False)
        
        p = None
        
        if not form_data_empty(p_form):
            if p_form.is_valid():
                p = p_form.save(commit=False)
            else:
                valid = False
        
        if valid:
            if p:
                p.save()
            
            stars.prebivalisce = p
            
            if not user.id:
                user.gen_username()
                user.set_unusable_password()
            
            user.save()
            
            stars.uporabnik = user
            stars.save()
            
            dijak.mati = stars
            dijak.save()
        
    else:
        valid = False
            
    if valid:
        messages.info(request, u'Podatki o materi so shranjeni.')
        
        return HttpResponseRedirect(reverse('profesor_razredi_dijaki_podatki', args=[razred.id, dijak.id]))
    
    return locals()

@resource(r'^/razredi/(?P<razred>\d+)/dijaki/(?P<dijak>\d+)/mati/izbrisi', 'profesor_razredi_dijaki_mati_izbrisi')
@login_required
@profesor_required
def razredi_dijaki_mati_izbrisi(request, razred, dijak):
    profesor = request.user_profile
    razred = get_object_or_404(profesor.razredi, id=razred)
    dijak = get_object_or_404(razred.dijaki_cached, id=dijak)
    stars = not_none_or_404(dijak.mati)
    
    dijak.mati = None
    dijak.save()
    
    su = stars.uporabnik
    stars.delete()
    su.delete()
    
    return HttpResponseRedirect(reverse('profesor_razredi_dijaki_podatki', args=[razred.id, dijak.id]))

@resource(r'^/razredi/(?P<razred>\d+)/dijaki/(?P<dijak>\d+)/mati/novo-geslo$', 'profesor_razredi_dijaki_mati_novo_geslo')
@login_required
@profesor_required
@render('profesor/razredi/dijaki/mati_novo_geslo.html')
def razredi_dijaki_mati_novo_geslo(request, razred, dijak):
    profesor = request.user_profile
    razred = get_object_or_404(profesor.razredi, id=razred)
    dijak = get_object_or_404(razred.dijaki_cached, id=dijak)
    stars = not_none_or_404(dijak.mati)
    
    uporabnisko_ime = stars.uporabnik.username
    geslo = stars.uporabnik.gen_password()
    stars.uporabnik.save()
    
    poslji_novo_geslo(request, uporabnisko_ime, geslo, stars.uporabnik.email)
    
    return locals()

@resource(r'^/razredi/(?P<razred>\d+)/dogodki$', 'profesor_razredi_dogodki')
@login_required
@profesor_required
@render('profesor/razredi/dogodki/dogodki.html')
def razredi_dogodki(request, razred):
    profesor = request.user_profile
    razred = get_object_or_404(profesor.razredi, id=razred)
    
    prihajajoci_dogodki = razred.prihajajoci_dogodki
    pretekli_dogodki = razred.pretekli_dogodki
    
    return locals()

@resource(r'^/razredi/(?P<razred>\d+)/dogodki/(?P<dogodek>\d+)$', 'profesor_razredi_dogodki_dogodek')
@login_required
@profesor_required
@render('profesor/razredi/dogodki/dogodek.html')
def razredi_dogodki_dogodek(request, razred, dogodek):
    profesor = request.user_profile
    razred = get_object_or_404(profesor.razredi, id=razred)
    
    dogodek = get_object_or_404(razred.dogodki, id=dogodek)
    
    ocene = dict([(x.dijak, x) for x in dogodek.ocene])
    
    dijaki = list(razred.dijaki.all())
    
    for dijak in dijaki:
        dijak.ocena = ocene.get(dijak, None)
    
    return locals()

@resource(r'^/razredi/(?P<razred>\d+)/dogodki/(?P<dogodek>\d+)/uredi$', 'profesor_razredi_dogodki_uredi')
@login_required
@profesor_required
@render('profesor/razredi/dogodki/dogodek_uredi.html')
def razredi_dogodki_uredi(request, razred, dogodek):
    profesor = request.user_profile
    razred = get_object_or_404(profesor.razredi, id=razred)
    dogodek = get_object_or_404(razred.dogodki, id=dogodek)
    
    form = DogodekForm(instance=dogodek, data=request.POST or None)
    
    form.fields['poucuje'].queryset = razred.poucuje
    form.fields['poucuje'].label_from_instance = poucuje_predmet_label
    
    if form.is_valid():
        form.save()
        
        messages.info(request, u'Podatki o dogodku so shranjeni.')
        
        return HttpResponseRedirect(reverse('profesor_razredi_dogodki_dogodek', args=[razred.id, dogodek.id]))
    
    return locals()

@resource(r'^/razredi/(?P<razred>\d+)/predmeti$', 'profesor_razredi_predmeti')
@login_required
@profesor_required
@render('profesor/razredi/predmeti.html')
def razredi_predmeti(request, razred):
    profesor = request.user_profile
    razred = get_object_or_404(profesor.razredi, id=razred)
    
    poucuje = razred.poucuje
    
    return locals()
