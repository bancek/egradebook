from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

from dacks.views import render, Resource
from dacks.utils import get_int_or_none

from infosys.views import stars_required
from auth.forms import NastavitveForm

resource = urlpatterns = Resource()

@resource(r'^/$', 'stars')
@login_required
@stars_required
@render('stars/stars.html')
def stars(request):
    stars = request.user_profile
    
    dijaki = stars.dijaki
    
    return locals()

@resource(r'^/nastavitve$', 'stars_nastavitve')
@login_required
@stars_required
@render('stars/nastavitve.html')
def nastavitve(request):
    stars = request.user_profile
    
    form = NastavitveForm(request, data=request.POST or None)
    
    if form.is_valid():
        form.save()
    
    return locals()

@resource(r'^/dijak/(?P<dijak>\d+)$', 'stars_dijak')
@login_required
@stars_required
@render('stars/dijak/dijak.html')
def dijak(request, dijak):
    stars = request.user_profile
    dijak = get_object_or_404(stars.dijaki, id=dijak)
    
    zadnje_ocene = dijak.zadnje_ocene[:5]
    prihajajoci_dogodki = dijak.prihajajoci_dogodki[:5]
    
    return locals()

@resource(r'^/dijak/(?P<dijak>\d+)/ocene$', 'stars_dijak_ocene')
@login_required
@stars_required
@render('stars/dijak/ocene/ocene.html')
def dijak_ocene(request, dijak):
    stars = request.user_profile
    dijak = get_object_or_404(stars.dijaki, id=dijak)
    
    predmet = get_int_or_none(request.GET, 'p')
    ocenjevalno_obdobje = get_int_or_none(request.GET, 'oo')
    
    ocene = dijak.get_ocene(predmet=predmet, ocenjevalno_obdobje=ocenjevalno_obdobje)
    
    return locals()

@resource(r'^/dijak/(?P<dijak>\d+)/ocene/natisni$', 'stars_dijak_ocene_natisni')
@login_required
@stars_required
@render('print/ocene.html')
def dijak_ocene_natisni(request, dijak):
    stars = request.user_profile
    dijak = get_object_or_404(stars.dijaki, id=dijak)
    
    ocene = dijak.get_ocene()
    
    return locals()

@resource(r'^/dijak/(?P<dijak>\d+)/ocene/(?P<ocena>\d+)$', 'stars_dijak_ocene_ocena')
@login_required
@stars_required
@render('stars/dijak/ocene/ocena.html')
def dijak_ocene_ocena(request, dijak, ocena):
    stars = request.user_profile
    dijak = get_object_or_404(stars.dijaki, id=dijak)
    
    ocena = get_object_or_404(dijak.ocene_base, id=ocena)
    
    return locals()

@resource(r'^/dijak/(?P<dijak>\d+)/dogodki$', 'stars_dijak_dogodki')
@login_required
@stars_required
@render('stars/dijak/dogodki/dogodki.html')
def dijak_dogodki(request, dijak):
    stars = request.user_profile
    dijak = get_object_or_404(stars.dijaki, id=dijak)
    
    prihajajoci_dogodki = dijak.prihajajoci_dogodki
    pretekli_dogodki = dijak.pretekli_dogodki
    
    return locals()

@resource(r'^/dijak/(?P<dijak>\d+)/dogodki/dogodek/(?P<dogodek>\d+)$', 'stars_dijak_dogodki_dogodek')
@login_required
@stars_required
@render('stars/dijak/dogodki/dogodek.html')
def dijak_dogodki_dogodek(request, dijak, dogodek):
    stars = request.user_profile
    dijak = get_object_or_404(stars.dijaki, id=dijak)
    
    dogodek = get_object_or_404(dijak.dogodki, id=dogodek)
    
    return locals()

@resource(r'^/dijak/(?P<dijak>\d+)/podatki$', 'stars_dijak_podatki')
@login_required
@stars_required
@render('stars/dijak/podatki.html')
def dijak_dijak_podatki(request, dijak):
    stars = request.user_profile
    dijak = get_object_or_404(stars.dijaki, id=dijak)
    
    return locals()

@resource(r'^/dijak/(?P<dijak>\d+)/predmeti$', 'stars_dijak_predmeti')
@login_required
@stars_required
@render('stars/dijak/predmeti.html')
def dijak_dijak_predmeti(request, dijak):
    stars = request.user_profile
    dijak = get_object_or_404(stars.dijaki, id=dijak)
    
    poucuje = dijak.poucuje
    
    return locals()
