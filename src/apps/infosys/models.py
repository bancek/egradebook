#-*- coding: utf-8 -*-

from datetime import datetime
import random

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.db.models import Q, Avg

from authprofile.models import UserProfile
from core.utils import cached_property, slugify, months_range

PWCHARS = 'abcdefghijkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789'

def gen_username(self):
    oun = '%s%s' % (self.last_name[:4], self.first_name[:4])
    self.username = slugify(oun, instance=User, slug_field='username')

def gen_password(self):
    pw = ''.join(random.choice(PWCHARS) for _ in range(10))
    self.set_password(pw)
    return pw

User.gen_username = gen_username
User.gen_password = gen_password

OCENE = (
    ('5', '5'),
    ('4', '4'),
    ('3', '3'),
    ('2', '2'),
    ('1', '1'),
)

class OsebaManager(models.Manager):
    def get_query_set(self):
        qs = super(OsebaManager, self).get_query_set() \
                                      .select_related('uporabnik')
        return qs

class Naslov(models.Model):
    ulica = models.CharField(max_length=255, null=True, blank=True)
    hisna_stevilka = models.CharField(max_length=5, null=True, blank=True)
    posta = models.PositiveSmallIntegerField(null=True, blank=True)
    kraj = models.CharField(max_length=255, null=True, blank=True)
    
    class Meta:
        verbose_name = u'Naslov'
        verbose_name_plural = u'Naslovi'
    
    def __unicode__(self):
        return u'%s %s, %s %s' % (self.ulica, self.hisna_stevilka,
                                  int(self.posta) if self.posta else '',
                                  self.kraj)

class Oseba(models.Model):
    uporabnik = models.ForeignKey(User)
    
    class Meta:
        abstract = True
    
    def __unicode__(self):
        return u'%s %s (%s)' % (self.ime, self.priimek,
                                self.uporabnik.username)
    
    @property
    def ime(self):
        return self.uporabnik.first_name
    
    @property
    def priimek(self):
        return self.uporabnik.last_name

class SolskoLetoManager(models.Manager):
    def current(self):
        qs = self.filter(aktivno=True)
        
        return qs[0] if qs[:1] else None

class SolskoLeto(models.Model):
    zacetno_leto = models.PositiveIntegerField()
    koncno_leto = models.PositiveIntegerField()
    aktivno = models.BooleanField(default=True)
    
    objects = SolskoLetoManager()
    
    class Meta:
        verbose_name = u'Šolsko leto'
        verbose_name_plural = u'Šolska leta'
        ordering = ('zacetno_leto',)
    
    def __unicode__(self):
        return u'%d - %d' % (self.zacetno_leto, self.koncno_leto)

class Profesor(Oseba):
    objects = OsebaManager()
    
    class Meta:
        verbose_name = u'Profesor'
        verbose_name_plural = u'Profesorji'
        ordering = ('uporabnik__last_name', 'uporabnik__first_name')
    
    @cached_property
    def razredi(self):
        sl = SolskoLeto.objects.current()
        return self.razred_set.filter(solsko_leto=sl)
    
    @cached_property
    def predmeti(self):
        sl = SolskoLeto.objects.current()
        qs = Predmet.objects.filter(
            poucuje__profesor=self,
            poucuje__razred__solsko_leto=sl,
        )
        return qs.distinct()
    
    def get_predmet_razredi(self, predmet):
        sl = SolskoLeto.objects.current()
        qs = Razred.objects.filter(
            solsko_leto=sl,
            poucuje__profesor=self,
            poucuje__predmet=predmet
        )
        
        return qs.distinct()
    
    @cached_property
    def poucuje(self):
        return self.poucuje_set.all()

class Smer(models.Model):
    smer = models.CharField(max_length=100)
    
    class Meta:
        verbose_name = u'Smer'
        verbose_name_plural = u'Smeri'
        ordering = ('smer',)
    
    def __unicode__(self):
        return unicode(self.smer)

class Predmet(models.Model):
    predmet = models.CharField(max_length=5)
    ime = models.CharField(max_length=50)
    
    class Meta:
        verbose_name = u'Predmet'
        verbose_name_plural = u'Predmeti'
        ordering = ('ime',)
    
    def __unicode__(self):
        return u'%s (%s)' % (self.ime, self.predmet)

class Stars(Oseba):
    prebivalisce = models.OneToOneField(Naslov, null=True, blank=True)
    domaci_telefon = models.CharField(max_length=20, null=True, blank=True)
    sluzbeni_telefon = models.CharField(max_length=20, null=True, blank=True)
    mobitel = models.CharField(max_length=20, null=True, blank=True)
    
    objects = OsebaManager()
    
    class Meta:
        verbose_name = u'Starš'
        verbose_name_plural = u'Starši'
        ordering = ('uporabnik__last_name', 'uporabnik__first_name')
    
    @cached_property
    def dijaki(self):
        sl = SolskoLeto.objects.current()
        qs = Dijak.objects.filter(
            Q(oce=self.id) | Q(mati=self.id),
            razred__solsko_leto=sl,
        )
        return  qs

class Dijak(Oseba):
    emso = models.CharField(max_length=13, null=True, blank=True)
    datum_rojstva = models.DateField(null=True, blank=True)
    stalno_prebivalisce = models.OneToOneField(Naslov, null=True, blank=True, related_name='stalno_prebivalisce_dijaka')
    zacasno_prebivalisce = models.OneToOneField(Naslov, null=True, blank=True, related_name='zacasno_prebivalisce_dijaka')
    v_dijaskem_domu = models.BooleanField(default=False)
    oce = models.ForeignKey(Stars, null=True, blank=True, related_name='oce_dijaka')
    mati = models.ForeignKey(Stars, null=True, blank=True, related_name='mati_dijaka')
    mobitel = models.CharField(max_length=20, null=True, blank=True)
    
    objects = OsebaManager()
    
    class Meta:
        verbose_name = u'Dijak'
        verbose_name_plural = u'Dijaki'
        ordering = ('uporabnik__last_name', 'uporabnik__first_name')
    
    @cached_property
    def razred(self):
        sl = SolskoLeto.objects.current()
        qs = self.razred_set.filter(solsko_leto=sl)
        
        return qs[0] if qs[:1] else None
    
    @cached_property
    def sosolci(self):
        return self.razred.dijaki_cached.exclude(id=self.id)
    
    @cached_property
    def profesorji(self):
        return self.razred.profesorji_cached
    
    @cached_property
    def poucuje(self):
        return self.razred.poucuje
    
    @cached_property
    def ocene_base(self):
        return Ocena.objects.filter(dijak=self).select_related('poucuje')
    
    @cached_property
    def zadnje_ocene(self):
        return self.ocene_base.order_by('-datum_pridobitve')
    
    @cached_property
    def zakljucene_ocene_base(self):
        return ZakljucenaOcena.objects.filter(dijak=self) \
                                      .select_related('poucuje')
    
    def get_ocene(self, predmet=None, ocenjevalno_obdobje=None):
        r = self.razred
        
        if r is None:
            return
        
        ps = r.predmeti.all()
        
        if predmet is not None:
            ps = ps.filter(id=predmet)
        
        oos = r.ocenjevalna_obdobja
        
        if ocenjevalno_obdobje is not None:
            oos = oos.filter(id=ocenjevalno_obdobje)
        
        os = self.ocene_base.filter(
            poucuje__predmet__in=ps,
            ocenjevalno_obdobje__in=oos,
        )
        
        zos = self.zakljucene_ocene_base.filter(
            poucuje__predmet__in=ps,
        )
        
        osd = dict((p.id, dict((oo.id, []) for oo in oos)) for p in ps)
        
        for o in os:
            x = osd[o.poucuje.predmet_id][o.ocenjevalno_obdobje_id]
            x.append(o)
        
        zosd = dict((p.id, []) for p in ps)
        
        for zo in zos:
            zosd[zo.poucuje.predmet_id].append(zo)
        
        data = {
            'ocenjevalna_obdobja': list(oos),
            'predmeti': []
        }
        
        for p in ps:
            pr = {
                'predmet': p,
                'ocene': [],
                'zakljucena_ocena': zosd[p.id]
            }
            
            for oo in oos:
                pr['ocene'].append(osd[p.id][oo.id])
            
            data['predmeti'].append(pr)
        
        return data
    
    @cached_property
    def dogodki(self):
        return self.razred.dogodki
    
    @cached_property
    def prihajajoci_dogodki(self):
        return self.razred.prihajajoci_dogodki
    
    @cached_property
    def pretekli_dogodki(self):
        return self.razred.pretekli_dogodki

class RazredManager(models.Manager):
    def active(self):
        sl = SolskoLeto.objects.current()
        return self.filter(solsko_leto=sl)

class Razred(models.Model):
    solsko_leto = models.ForeignKey(SolskoLeto)
    ime = models.CharField(max_length=3)
    smer = models.ForeignKey(Smer)
    razrednik = models.ForeignKey(Profesor)
    dijaki = models.ManyToManyField(Dijak, blank=True)
    predmeti = models.ManyToManyField(Predmet, blank=True, through='Poucuje',
                                      related_name='predmet_razredi')
    profesorji = models.ManyToManyField(Profesor, blank=True, through='Poucuje',
                                        related_name='profesor_razredi')
    
    objects = RazredManager()
    
    class Meta:
        verbose_name = u'Razred'
        verbose_name_plural = u'Razredi'
        ordering = ('ime',)
    
    def __unicode__(self):
        return u'%s (%s)' % (self.ime, self.solsko_leto)
    
    @cached_property
    def ocenjevalna_obdobja(self):
        qs = OcenjevalnoObdobje.objects.filter(solsko_leto=self.solsko_leto)
        return qs
    
    @cached_property
    def dijaki_cached(self):
        return self.dijaki.all()
    
    def statistika_dijaki(self):
        qs = self.dijaki.all()
        qs = qs.annotate(povprecje=Avg('ocena__ocena_stevilka'))
        
        return qs
    
    def statistika_ocene(self):
        ocene = []
        
        qs = Ocena.objects.filter(dijak__razred=self)
        
        for ocena in [x[0] for x in OCENE]:
            st = qs.filter(ocena_stevilka=ocena).count()
            ocene.append((ocena, st))
        
        return ocene
    
    def statistika_po_mesecih(self):
        po_mesecih = []
        
        oos = self.ocenjevalna_obdobja
        
        mr = months_range(oos[0].zacetek, oos[1].konec)
        
        qs = Ocena.objects.filter(dijak__razred=self)
        
        for start, end in mr:
            tqs = qs.filter(datum_pridobitve__gte=start, datum_pridobitve__lt=end)
            p = tqs.aggregate(povprecje=Avg('ocena_stevilka'))['povprecje']
            po_mesecih.append(((start, end), p))
        
        return po_mesecih
    
    @cached_property
    def profesorji_cached(self):
        return self.profesorji.all()
    
    @cached_property
    def poucuje(self):
        return self.poucuje_set.all().order_by('predmet__ime')
    
    @cached_property
    def dogodki(self):
        return Dogodek.objects.filter(poucuje__razred=self).distinct()
    
    @cached_property
    def prihajajoci_dogodki(self):
        return self.dogodki.filter(datum__gte=datetime.now())
    
    @cached_property
    def pretekli_dogodki(self):
        return self.dogodki.filter(datum__lt=datetime.now()).order_by('-datum')

class Poucuje(models.Model):
    profesor = models.ForeignKey(Profesor)
    razred = models.ForeignKey(Razred)
    predmet = models.ForeignKey(Predmet)
    
    class Meta:
        verbose_name = u'Poučuje'
        verbose_name_plural = u'Poučuje'
    
    def __unicode__(self):
        return u'%s poučuje %s v %s' % (self.profesor, self.predmet,
                                        self.razred)

class OcenjevalnoObdobjeManager(models.Manager):
    def active(self):
        sl = SolskoLeto.objects.current()
        return self.filter(solsko_leto=sl)

class OcenjevalnoObdobje(models.Model):
    solsko_leto = models.ForeignKey(SolskoLeto)
    ime = models.CharField(max_length=20)
    zacetek = models.DateField()
    konec = models.DateField()
    
    objects = OcenjevalnoObdobjeManager()
    
    class Meta:
        verbose_name = u'Ocenjevalno obdobje'
        verbose_name_plural = u'Ocenjevalna obdobja'
        ordering = ('zacetek',)
    
    def __unicode__(self):
        return u'%s (%s - %s)' % (self.ime, self.zacetek,
                                  self.konec)

class DogodekManager(models.Manager):
    def get_query_set(self):
        qs = super(DogodekManager, self).get_query_set() \
              .select_related('poucuje__predmet', 'poucuje__profesor')
        return qs

class Dogodek(models.Model):
    poucuje = models.ForeignKey(Poucuje)
    ocenjevalno_obdobje = models.ForeignKey(OcenjevalnoObdobje)
    ime = models.CharField(max_length=100)
    datum = models.DateField()
    
    objects = DogodekManager()
    
    class Meta:
        verbose_name = u'Dogodek'
        verbose_name_plural = u'Dogodki'
        ordering = ('datum',)
    
    def __unicode__(self):
        return u'%s - %s (%s)' % (self.ime, self.poucuje.predmet.ime, self.datum)
    
    @cached_property
    def ocene(self):
        return self.ocena_set.all()

class OcenaBase(models.Model):
    dijak = models.ForeignKey(Dijak)
    poucuje = models.ForeignKey(Poucuje)
    ocena = models.CharField(max_length=10)
    ocena_stevilka = models.IntegerField()
    datum_vnosa = models.DateTimeField(auto_now_add=True, null=True)
    datum_spremembe = models.DateTimeField(auto_now=True, null=True)
    datum_pridobitve = models.DateField(null=True, blank=True)
    
    class Meta:
        abstract = True

class Ocena(OcenaBase):
    ocenjevalno_obdobje = models.ForeignKey(OcenjevalnoObdobje)
    zakljucena = models.BooleanField(default=False)
    opomba = models.TextField(null=True, blank=True)
    dogodek = models.ForeignKey(Dogodek, null=True, blank=True)
    
    class Meta:
        verbose_name = u'Ocena'
        verbose_name_plural = u'Ocene'
        ordering = ('datum_vnosa',)
    
    def save(self, *args, **kwargs):
        try:
            ocena = int(self.ocena)
            self.ocena_stevilka = ocena
        except:
            self.ocena_stevilka = -1
        
        return super(Ocena, self).save(*args, **kwargs)
    
    def __unicode__(self):
        return u'%s: %s: %s' % (self.dijak, self.poucuje.predmet, self.ocena)

class ZakljucenaOcena(OcenaBase):
    class Meta:
        verbose_name = u'Zaključena ocena'
        verbose_name_plural = u'Zaključene ocene'
    
    def save(self, *args, **kwargs):
        try:
            ocena = int(self.ocena)
            self.ocena_stevilka = ocena
        except:
            self.ocena_stevilka = -1
        
        return super(ZakljucenaOcena, self).save(*args, **kwargs)

def on_dijak_created(sender, instance, created, **kwargs):
    if created:
        p = UserProfile.objects.get(user=instance.uporabnik)
        p.profile = instance
        p.save()

post_save.connect(on_dijak_created, Dijak)

def on_stars_created(sender, instance, created, **kwargs):
    if created:
        p = UserProfile.objects.get(user=instance.uporabnik)
        p.profile = instance
        p.save()

post_save.connect(on_stars_created, Stars)

def on_profesor_created(sender, instance, created, **kwargs):
    if created:
        p = UserProfile.objects.get(user=instance.uporabnik)
        p.profile = instance
        p.save()

post_save.connect(on_profesor_created, Profesor)
