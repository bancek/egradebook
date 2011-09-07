def poucuje_predmet_label(obj):
    return obj.predmet.ime

def dogodek_label(obj):
    return u'%s - %s (%s)' % (obj.poucuje.predmet.ime, obj.ime, obj.datum)
