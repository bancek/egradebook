from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

from dacks.views import render, Resource
from dacks.utils import get_int_or_none

from infosys.views import dijak_required
from auth.forms import NastavitveForm

resource = urlpatterns = Resource()

@resource(r'^/$', 'dijak')
@login_required
@dijak_required
@render('dijak/dijak.html')
def dijak(request):
    dijak = request.user_profile
    
    zadnje_ocene = dijak.zadnje_ocene[:5]
    prihajajoci_dogodki = dijak.prihajajoci_dogodki[:5]
    
    return locals()

@resource(r'^/nastavitve$', 'dijak_nastavitve')
@login_required
@dijak_required
@render('dijak/nastavitve.html')
def nastavitve(request):
    dijak = request.user_profile
    
    form = NastavitveForm(request, data=request.POST or None)
    
    if form.is_valid():
        form.save()
    
    return locals()

@resource(r'^/ocene$', 'dijak_ocene')
@login_required
@dijak_required
@render('dijak/ocene/ocene.html')
def ocene(request):
    dijak = request.user_profile
    
    predmet = get_int_or_none(request.GET, 'p')
    ocenjevalno_obdobje = get_int_or_none(request.GET, 'oo')
    
    ocene = dijak.get_ocene(predmet=predmet, ocenjevalno_obdobje=ocenjevalno_obdobje)
    
    return locals()

@resource(r'^/ocene/natisni$', 'dijak_ocene_natisni')
@login_required
@dijak_required
@render('print/ocene.html')
def ocene_natisni(request):
    dijak = request.user_profile
    
    ocene = dijak.get_ocene()
    
    return locals()

@resource(r'^/ocene/(?P<ocena>\d+)$', 'dijak_ocene_ocena')
@login_required
@dijak_required
@render('dijak/ocene/ocena.html')
def ocene_ocena(request, ocena):
    dijak = request.user_profile
    ocena = get_object_or_404(dijak.ocene_base, id=ocena)
    
    return locals()

@resource(r'^/dogodki$', 'dijak_dogodki')
@login_required
@dijak_required
@render('dijak/dogodki/dogodki.html')
def dogodki(request):
    dijak = request.user_profile
    
    prihajajoci_dogodki = dijak.prihajajoci_dogodki
    pretekli_dogodki = dijak.pretekli_dogodki
    
    return locals()

@resource(r'^/dogodki/dogodek/(?P<dogodek>\d+)$', 'dijak_dogodki_dogodek')
@login_required
@dijak_required
@render('dijak/dogodki/dogodek.html')
def dogodki_dogodek(request, dogodek):
    dijak = request.user_profile
    dogodek = get_object_or_404(dijak.dogodki, id=dogodek)
    
    return locals()

@resource(r'^/podatki$', 'dijak_podatki')
@login_required
@dijak_required
@render('dijak/podatki.html')
def podatki(request):
    dijak = request.user_profile
    
    return locals()

@resource(r'^/sosolci$', 'dijak_sosolci')
@login_required
@dijak_required
@render('dijak/sosolci.html')
def sosolci(request):
    dijak = request.user_profile
    
    sosolci = dijak.sosolci
    
    return locals()

@resource(r'^/sosolci/natisni$', 'dijak_sosolci_natisni')
@login_required
@dijak_required
@render('print/razred.html')
def razredi_razred_natisni(request):
    dijak = request.user_profile
    
    razred = dijak.razred
    dijaki = dijak.sosolci
    
    return locals()

@resource(r'^/predmeti$', 'dijak_predmeti')
@login_required
@dijak_required
@render('dijak/predmeti.html')
def predmeti(request):
    dijak = request.user_profile
    
    poucuje = dijak.poucuje
    
    return locals()
