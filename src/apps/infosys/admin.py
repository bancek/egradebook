from django.contrib import admin
from django.utils.text import truncate_words
from django.core import urlresolvers
from django.utils.html import escape

from infosys.models import *

def uni_tr_10(field_name):
    def func(obj):
        return truncate_words(unicode(getattr(obj, field_name)), 10)
    
    func.short_description = field_name
    func.admin_order_field = field_name
    
    return func

def uni_fk_tr_10(field_name, order_field=None):
    fnparts = field_name.split('__')
    
    def func(obj):
        f = getattr(obj, fnparts[0])
        
        for part in fnparts[1:]:
            f = getattr(f, part)
        
        url_name = 'admin:%s_%s_change' % (f._meta.app_label,
                                              f._meta.module_name)
        
        url = urlresolvers.reverse(url_name, args=(f.pk,))
        name = escape(truncate_words(unicode(f), 10))
        return u'<a href="%s">%s</a>' % (url, name)
    
    func.allow_tags = True
    func.short_description = fnparts[-1]
    
    if order_field is not False:
        func.admin_order_field = order_field or field_name
    
    return func

class NaslovAdmin(admin.ModelAdmin):
    search_fields = ['ulica', 'hisna_stevilka', 'posta', 'kraj']
    list_display = ['id', 'ulica', 'hisna_stevilka', 'posta', 'kraj']

class SolskoLetoAdmin(admin.ModelAdmin):
    search_fields = []
    list_display = ['id', 'zacetno_leto', 'koncno_leto', 'aktivno']
    raw_id_fields = []

class ProfesorAdmin(admin.ModelAdmin):
    search_fields = ['uporabnik__username', 'uporabnik__first_name',
                     'uporabnik__last_name']
    list_display = ['id', uni_fk_tr_10('uporabnik', 'uporabnik__username'),
                    'ime', 'priimek']
    raw_id_fields = ['uporabnik']
    
    def ime(self, obj):
        return obj.uporabnik.first_name
    ime.admin_order_field = 'uporabnik__first_name'
    
    def priimek(self, obj):
        return obj.uporabnik.last_name
    priimek.admin_order_field = 'uporabnik__last_name'

class SmerAdmin(admin.ModelAdmin):
    search_fields = ['smer']
    list_display = ['id', 'smer']

class PredmetAdmin(admin.ModelAdmin):
    search_fields = ['predmet', 'ime']
    list_display = ['id', 'ime', 'predmet']

class StarsAdmin(admin.ModelAdmin):
    search_fields = ['uporabnik__username', 'uporabnik__first_name',
                     'uporabnik__last_name']
    list_display = ['id', uni_fk_tr_10('uporabnik', 'uporabnik__username'),
                    'ime', 'priimek', uni_fk_tr_10('prebivalisce')]
    raw_id_fields = ['uporabnik', 'prebivalisce']
    
    def ime(self, obj):
        return obj.uporabnik.first_name
    ime.admin_order_field = 'uporabnik__first_name'
    
    def priimek(self, obj):
        return obj.uporabnik.last_name
    priimek.admin_order_field = 'uporabnik__last_name'

class DijakAdmin(admin.ModelAdmin):
    search_fields = ['uporabnik__username', 'uporabnik__first_name',
                     'uporabnik__last_name', 'emso']
    list_display = ['id', uni_fk_tr_10('uporabnik', 'uporabnik__username'),
                    'ime', 'priimek', 'emso']
    raw_id_fields = ['uporabnik', 'stalno_prebivalisce',
                     'zacasno_prebivalisce', 'oce', 'mati']
    list_filter = ['v_dijaskem_domu']
    
    def ime(self, obj):
        return obj.uporabnik.first_name
    ime.admin_order_field = 'uporabnik__first_name'
    
    def priimek(self, obj):
        return obj.uporabnik.last_name
    priimek.admin_order_field = 'uporabnik__last_name'

class RazredAdmin(admin.ModelAdmin):
    search_fields = ['ime']
    list_display = ['id', 'ime', uni_fk_tr_10('solsko_leto'), uni_fk_tr_10('smer'), uni_fk_tr_10('razrednik')]
    raw_id_fields = ['razrednik']
    filter_horizontal = ['dijaki']

class PoucujeAdmin(admin.ModelAdmin):
    search_fields = []
    list_display = ['id', uni_fk_tr_10('profesor'), uni_fk_tr_10('razred'),
                    uni_fk_tr_10('predmet')]
    raw_id_fields = ['profesor', 'razred', 'predmet']

class OcenjevalnoObdobjeAdmin(admin.ModelAdmin):
    search_fields = ['ime']
    list_display = ['id', 'ime', uni_fk_tr_10('solsko_leto'),
                    'zacetek', 'konec']

class DogodekAdmin(admin.ModelAdmin):
    search_fields = ['ime']
    list_display = ['id', uni_tr_10('ime'), uni_tr_10('datum'),
                    uni_fk_tr_10('poucuje__predmet', 'poucuje__predmet__ime'),
                    uni_fk_tr_10('poucuje__profesor', False),
                    'ocenjevalno_obdobje']
    raw_id_fields = ['poucuje']

class OcenaAdmin(admin.ModelAdmin):
    search_fields = ['ocena', 'opomba', 'dijak__uporabnik__first_name',
                     'dijak__uporabnik__last_name',
                     'dijak__uporabnik__username']
    list_display = ['id', uni_fk_tr_10('dijak', False),
                    uni_fk_tr_10('poucuje__profesor', False),
                    uni_fk_tr_10('poucuje__razred', False),
                    'ocena', 'datum_pridobitve',
                    uni_fk_tr_10('ocenjevalno_obdobje'),
                    uni_fk_tr_10('dogodek')]
    raw_id_fields = ['dijak', 'poucuje', 'dogodek']

class ZakljucenaOcenaAdmin(admin.ModelAdmin):
    search_fields = ['ocena', 'dijak__uporabnik__first_name',
                     'dijak__uporabnik__last_name',
                     'dijak__uporabnik__username']
    list_display = ['id', uni_fk_tr_10('dijak'),
                    uni_fk_tr_10('poucuje__profesor', False),
                    uni_fk_tr_10('poucuje__razred', False),
                    'ocena', 'datum_pridobitve']
    raw_id_fields = ['dijak', 'poucuje']

admin.site.register(Naslov, NaslovAdmin)
admin.site.register(SolskoLeto, SolskoLetoAdmin)
admin.site.register(Profesor, ProfesorAdmin)
admin.site.register(Smer, SmerAdmin)
admin.site.register(Predmet, PredmetAdmin)
admin.site.register(Stars, StarsAdmin)
admin.site.register(Dijak, DijakAdmin)
admin.site.register(Razred, RazredAdmin)
admin.site.register(Poucuje, PoucujeAdmin)
admin.site.register(OcenjevalnoObdobje, OcenjevalnoObdobjeAdmin)
admin.site.register(Dogodek, DogodekAdmin)
admin.site.register(Ocena, OcenaAdmin)
admin.site.register(ZakljucenaOcena, ZakljucenaOcenaAdmin)