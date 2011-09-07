#-*- coding: utf-8 -*-

import random
import inspect
import profilehooks
from datetime import datetime, date, timedelta
from core.utils import slugify
from eventlet import GreenPool

LOG = False

def log():
    d = inspect.stack()[1]
    if LOG:
        print '%s(%s)' % (d[3], str(d[0].f_locals))

from django.db.models import Count, Avg

from infosys.models import *

def waiter(func, iters):
    pool = GreenPool(10)
    return pool.imap(func, iters)

def spawner(func, iters):
    pool = GreenPool(10)
    x = pool.imap(func, iters)
    x.waiters.get()

def lp(l):
    import string
    print '['
    line = '    '
    for x in sorted(map(string.capitalize, l)):
        new = 'u\'%s\', ' % x
        if len(line) + len(new) >= 80:
            print line
            line = '    '
        
        line += new
    
    print line
    print ']'

PRIIMKI = [
    u'Bezjak', u'Bizjak', u'Blatnik', u'Breznik', u'Cerar', u'Dolenc', u'Erjavec',
    u'Fras', u'Furlan', u'Golob', u'Horvat', u'Hren', u'Hribar', u'Hrovat', u'Jelen',
    u'Jenko', u'Jerman', u'Jug', u'Kastelic', u'Knez', u'Kokalj', u'Kolar', u'Koren',
    u'Kos', u'Kotnik', u'Krajnc', u'Kralj', u'Kranjc', u'Kuhar', u'Lah', u'Leban',
    u'Lesjak', u'Logar', u'Majcen', u'Marolt', u'Medved', u'Mlakar', u'Novak', u'Oblak',
    u'Pavlin', u'Perko', u'Petek', u'Pintar', u'Pirc', u'Rozman', u'Rupnik', u'Sever',
    u'Turk', u'Vidic', u'Vidmar', u'Zadravec', u'Zajc', u'Zorko', u'Zupan', u'Zupanc',
]

MOSKA_IMENA = [
    u'Alen', u'Aleš', u'Aljaž', u'Andraž', u'Andrej', u'Anže', u'Benjamin',
    u'Blaž', u'David', u'Dejan', u'Denis', u'Domen', u'Erik', u'Gašper',
    u'Gregor', u'Jaka', u'Jakob', u'Jan', u'Janez', u'Jernej', u'Jure',
    u'Klemen', u'Kristjan', u'Leon', u'Luka', u'Marko', u'Martin', u'Matej',
    u'Matevž', u'Matic', u'Matija', u'Matjaž', u'Miha', u'Mitja', u'Nejc',
    u'Nik', u'Patrik', u'Peter', u'Primož', u'Rok', u'Simon', u'Tadej',
    u'Tilen', u'Tim', u'Timotej', u'Tomaž', u'Urban', u'Uroš', u'Vid', u'Žan',
    u'Žiga',
]

ZENSKA_IMENA = [
    u'Ajda', u'Aleksandra', u'Ana', u'Andreja', u'Anja', u'Barbara', u'Eva',
    u'Ines', u'Janja', u'Kaja', u'Karin', u'Karmen', u'Katarina', u'Katja',
    u'Klara', u'Klavdija', u'Kristina', u'Lara', u'Laura', u'Lea', u'Lucija',
    u'Maja', u'Manca', u'Martina', u'Maruša', u'Mateja', u'Maša', u'Mojca',
    u'Monika', u'Nastja', u'Neža', u'Nika', u'Nina', u'Nuša', u'Patricija',
    u'Petra', u'Sabina', u'Sandra', u'Sara', u'Saša', u'Tamara', u'Tanja',
    u'Teja', u'Tina', u'Tjaša', u'Urša', u'Urška', u'Valentina', u'Veronika',
    u'Zala', u'Špela',
]

IMENA = MOSKA_IMENA + ZENSKA_IMENA

KRAJI = [
    u'Ljubljana', u'Maribor', u'Novo Mesto', u'Celje', u'Koper'
]

ULICE = [
    u'Cesta na gmajno', u'Ulica dveh cesarjev', u'Topniska cesta',
    u'Trubarjeva ulica', u'Slovenska cesta', u'Miklosiceva ulica',
]

PREDMETI = [
    ('SLO', u'Slovenščina'),
    ('ANG', u'Angleščina'),
    ('MAT', u'Matematika'),
    ('ZGO', u'Zgodovina'),
    ('FIZ', u'Fizika'),
    ('SVZ', u'Športna vzgoja'),
    ('APJ', u'Algoritmi in programski jeziki'),
    ('ROM', u'Računalniška omrežja'),
    ('RKO', u'Računalniške komponente'),
    ('PKB', u'Podatkovne baze'),
    ('PRA', u'Praktični pouk'),
    ('UME', u'Umetnost'),
    ('GEO', u'Geografija'),
    ('NEM', u'Nemščina'),
    ('SOC', u'Sociologija'),
    ('RAC', u'Računalništvo'),
    ('VEZ', u'Računalniška vezja'),
    ('MIK', u'Mikrokrmilniki'),
    ('ELE', u'Elektrotehnika'),
    ('ENE', u'Energetika'),
]

SMERI = [{
    'smer': u'Gimnazija',
    'razred': 'G',
    'razredi': 2,
    'predmeti': [
        'SLO', 'ANG', 'MAT', 'ZGO', 'FIZ', 'SVZ', 'RAC', 'UME', 'GEO', 'NEM',
        'SOC',
    ]
}, {
    'smer': u'Elektrotehnik računalništva',
    'razred': 'R',
    'razredi': 4,
    'predmeti': [
        'SLO', 'ANG', 'MAT', 'ZGO', 'FIZ', 'SVZ', 'APJ', 'PKB', 'RKO',
        'ROM', 'PRA',
    ]
}, {
    'smer': u'Elektrotehnik elektronike',
    'razred': 'N',
    'razredi': 3,
    'predmeti': [
        'SLO', 'ANG', 'MAT', 'ZGO', 'FIZ', 'SVZ', 'MIK', 'ELE', 'PRA',
    ]
}, {
    'smer': u'Elektrotehnik energetike',
    'razred': 'L',
    'razredi': 2,
    'predmeti': [
        'SLO', 'ANG', 'MAT', 'ZGO', 'FIZ', 'SVZ', 'ENE', 'ELE',
    ]
}]

def clone(x):
    kwargs = dict(x.__dict__)
    if '_state' in kwargs:
        del kwargs['_state']
    
    del kwargs['id']
    
    entity = x._default_manager.create(
        **kwargs
    )
    
    return entity

def rand_telefon():
    return '0' + str(random.randint(1, 5)) + str(random.randint(1000000, 9999999))

def rand_mobitel():
    return '0' + random.choice(['31', '41', '51', '40']) + str(random.randint(100000, 999999))

def gen_naslov():
    return Naslov.objects.create(
            ulica=random.choice(ULICE),
            hisna_stevilka=random.randint(1, 120),
            posta=random.randint(1000, 8000),
            kraj=random.choice(KRAJI)
        )

def gen_ime(seq=None):
    if not seq:
        seq = IMENA
    
    return random.choice(seq)

def gen_priimek():
    return random.choice(PRIIMKI)

def gen_user(ime, priimek):
    log()
    oun = '%s%s' % (priimek[:4], ime[:4])
    
    username = slugify(oun, instance=User, slug_field='username')
    
    user = User.objects.create_user(
        username=username,
        email='',
        password='password',
    )
    
    user.first_name = ime
    user.last_name = priimek
    
    user.save()
    
    return user

def gen_user_ip(ime, priimek):
    return dict(
        uporabnik=gen_user(ime, priimek),
    )

def gen_profesor():
    log()
    return Profesor.objects.create(
            **gen_user_ip(gen_ime(), gen_priimek())
        )

def rand_razrednik():
    qs = Profesor.objects.annotate(razredi_count=Count('razred')).filter(razredi_count=0).order_by('?')
    return qs[0] if qs[:1] else None

def rand_profesor(razred):
    log()
    profesorji = Poucuje.objects.filter(razred=razred).values('profesor')
    qs = Profesor.objects.exclude(pk__in=profesorji).order_by('?')
    return qs[0] if qs[:1] else None 

def gen_dijak(letnik):
    log()
    priimek = gen_priimek()
    naslov = gen_naslov()
    domaci_telefon = rand_telefon()
    
    oce = Stars.objects.create(
        prebivalisce=clone(naslov),
        domaci_telefon=domaci_telefon,
        sluzbeni_telefon=rand_telefon(),
        **gen_user_ip(gen_ime(MOSKA_IMENA), priimek)
    )
    
    mati = Stars.objects.create(
        prebivalisce=clone(naslov),
        domaci_telefon=domaci_telefon,
        sluzbeni_telefon=rand_telefon(),
        **gen_user_ip(gen_ime(ZENSKA_IMENA), priimek)
    )
    
    dr = date(letnik, 1, 1) + timedelta(days=random.randint(4, 360))
    emso = '%.2d%.2d%s5%.3d' % (dr.day, dr.month, str(dr.year)[1:], random.randint(0, 200))
    
    dijak = Dijak.objects.create(
        emso=emso,
        datum_rojstva=dr,
        stalno_prebivalisce=naslov,
        zacasno_prebivalisce=None,
        v_dijaskem_domu=False,
        oce=oce,
        mati=mati,
        mobitel=rand_mobitel(),
        **gen_user_ip(gen_ime(), priimek)
    )
    
    return dijak

#@profilehooks.profile
def gen():
    pool = GreenPool(10)
    
    leto = datetime.now().year - 1
    
    solsko_leto = SolskoLeto.objects.create(
        zacetno_leto=leto,
        koncno_leto=leto + 1,
    )
    
    prvo_polletje = OcenjevalnoObdobje.objects.create(
        solsko_leto=solsko_leto,
        ime='1. polletje',
        zacetek=datetime(year=leto, month=9, day=1),
        konec=datetime(year=leto + 1, month=1, day=20),
    )
    
    drugo_polletje = OcenjevalnoObdobje.objects.create(
        solsko_leto=solsko_leto,
        ime='2. polletje',
        zacetek=datetime(year=leto + 1, month=1, day=21),
        konec=datetime(year=leto + 1, month=6, day=24),
    )
    
    gp = lambda i: gen_profesor()
    list(pool.imap(gp, xrange(60)))
    
    pc = lambda x: (x[0], Predmet.objects.create(predmet=x[0], ime=x[1]))
    predmeti = dict(pool.imap(pc, PREDMETI))
    
    for sm in SMERI:
        smer = Smer.objects.create(smer=sm['smer'])
        
        for l in range(4):
            for r in range(sm['razredi']):
                razrednik = rand_razrednik()
                
                razred = Razred.objects.create(
                    solsko_leto=solsko_leto,
                    ime='%s%d%s' % (sm['razred'], l + 1, chr(65 + r)),
                    smer=smer,
                    razrednik=razrednik,
                )
                
                for p in sm['predmeti']:
                    predmet = predmeti[p]
                    
                    poucuje = Poucuje.objects.create(
                        profesor=rand_profesor(razred),
                        razred=razred,
                        predmet=predmet,
                    )
                
                for _ in range(random.randint(28, 31)):
                    dijak = gen_dijak(leto - l - 14)
                    razred.dijaki.add(dijak)

def oo_rand_date(oo):
    return oo.zacetek + timedelta(days=random.randint(0, (oo.konec - oo.zacetek).days - 7))

def gen_dogodek(poucuje, oo):
    dogodek = Dogodek.objects.create(
        poucuje=poucuje,
        ocenjevalno_obdobje=oo,
        ime='Pisni preizkus',
        datum=oo_rand_date(oo),
    )
    
    return dogodek

def gen_ocena(oo, poucuje, dijak, dogodek=None, zakljucena=False, ocene=None):
    if ocene:
        o = sum(ocene) / len(ocene)
    else:
        o = random.randint(1, 5)
    
    datum = oo_rand_date(oo)
    
    ocena = Ocena.objects.create(
        dijak=dijak,
        poucuje=poucuje,
        ocenjevalno_obdobje=oo,
        ocena=str(o),
        ocena_stevilka=o,
        datum_pridobitve=datum,
        dogodek=dogodek,
        zakljucena=zakljucena,
    )
    
    return ocena

def gen_zak_ocena(oo, poucuje, dijak, ocene):
    o = sum(ocene) / len(ocene)
    zo = ZakljucenaOcena.objects.create(
        dijak=dijak,
        poucuje=poucuje,
        ocena=str(o),
        ocena_stevilka=o,
        datum_pridobitve=oo.konec - timedelta(days=random.randint(2, 7)),
    )
    return zo

#@profilehooks.profile
def gen_ocene():
    sl = SolskoLeto.objects.current()
    oos = OcenjevalnoObdobje.objects.filter(solsko_leto=sl)
    rs = Razred.objects.filter(solsko_leto=sl)
    

    for razred in rs:
        ps = razred.poucuje_set.all()
        ds = razred.dijaki.all()
    
        for poucuje in ps:
            dogodki = []
            
            for oo in oos:
                for _ in range(random.randint(1, 2)):
                    dogodki.append(gen_dogodek(poucuje, oo))
                
            for dijak in ds:
                vse_ocene = []

                for dogodek in dogodki:
                    ocena = gen_ocena(dogodek.ocenjevalno_obdobje, poucuje, dijak, dogodek)
                    vse_ocene.append(ocena.ocena_stevilka)
                
                for oo in oos:
                    for _ in range(random.randint(1, 2)):
                        ocena = gen_ocena(oo, poucuje, dijak)
                        vse_ocene.append(ocena.ocena_stevilka)
    
                gen_zak_ocena(oo, poucuje, dijak, vse_ocene)
