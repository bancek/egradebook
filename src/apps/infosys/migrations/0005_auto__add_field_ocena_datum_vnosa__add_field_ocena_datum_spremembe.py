# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Ocena.datum_vnosa'
        db.add_column('infosys_ocena', 'datum_vnosa', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True), keep_default=False)

        # Adding field 'Ocena.datum_spremembe'
        db.add_column('infosys_ocena', 'datum_spremembe', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True), keep_default=False)

    def backwards(self, orm):
        
        # Deleting field 'Ocena.datum_vnosa'
        db.delete_column('infosys_ocena', 'datum_vnosa')

        # Deleting field 'Ocena.datum_spremembe'
        db.delete_column('infosys_ocena', 'datum_spremembe')

    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'infosys.dijak': {
            'Meta': {'object_name': 'Dijak'},
            'datum_rojstva': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'emso': ('django.db.models.fields.CharField', [], {'max_length': '13', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mati': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'mati_dijaka'", 'null': 'True', 'to': "orm['infosys.Stars']"}),
            'mobitel': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'oce': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'oce_dijaka'", 'null': 'True', 'to': "orm['infosys.Stars']"}),
            'stalno_prebivalisce': ('django.db.models.fields.related.OneToOneField', [], {'blank': 'True', 'related_name': "'stalno_prebivalisce_dijaka'", 'unique': 'True', 'null': 'True', 'to': "orm['infosys.Naslov']"}),
            'uporabnik': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'v_dijaskem_domu': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'zacasno_prebivalisce': ('django.db.models.fields.related.OneToOneField', [], {'blank': 'True', 'related_name': "'zacasno_prebivalisce_dijaka'", 'unique': 'True', 'null': 'True', 'to': "orm['infosys.Naslov']"})
        },
        'infosys.naslov': {
            'Meta': {'object_name': 'Naslov'},
            'hisna_stevilka': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kraj': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'posta': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'ulica': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'infosys.ocena': {
            'Meta': {'object_name': 'Ocena'},
            'datum_spremembe': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'datum_vnosa': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'dijak': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['infosys.Dijak']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ocena': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'ocena_stevilka': ('django.db.models.fields.IntegerField', [], {}),
            'ocenjevalno_obdobje': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['infosys.OcenjevalnoObdobje']"}),
            'poucuje': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['infosys.Poucuje']"}),
            'zakljucena': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'infosys.ocenjevalnoobdobje': {
            'Meta': {'ordering': "('zacetek',)", 'object_name': 'OcenjevalnoObdobje'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ime': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'konec': ('django.db.models.fields.DateField', [], {}),
            'solsko_leto': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['infosys.SolskoLeto']"}),
            'zacetek': ('django.db.models.fields.DateField', [], {})
        },
        'infosys.poucuje': {
            'Meta': {'object_name': 'Poucuje'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'predmet': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['infosys.Predmet']"}),
            'profesor': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['infosys.Profesor']"}),
            'razred': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['infosys.Razred']"})
        },
        'infosys.predmet': {
            'Meta': {'ordering': "('ime',)", 'object_name': 'Predmet'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ime': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'predmet': ('django.db.models.fields.CharField', [], {'max_length': '5'})
        },
        'infosys.profesor': {
            'Meta': {'object_name': 'Profesor'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'uporabnik': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'infosys.razred': {
            'Meta': {'ordering': "('ime',)", 'object_name': 'Razred'},
            'dijaki': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['infosys.Dijak']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ime': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'predmeti': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'predmet_razredi'", 'blank': 'True', 'through': "orm['infosys.Poucuje']", 'to': "orm['infosys.Predmet']"}),
            'profesorji': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'profesor_razredi'", 'blank': 'True', 'through': "orm['infosys.Poucuje']", 'to': "orm['infosys.Profesor']"}),
            'razrednik': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['infosys.Profesor']"}),
            'smer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['infosys.Smer']"}),
            'solsko_leto': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['infosys.SolskoLeto']"})
        },
        'infosys.smer': {
            'Meta': {'ordering': "('smer',)", 'object_name': 'Smer'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'smer': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'infosys.solskoleto': {
            'Meta': {'ordering': "('zacetno_leto',)", 'object_name': 'SolskoLeto'},
            'aktivno': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'koncno_leto': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'zacetno_leto': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        'infosys.stars': {
            'Meta': {'object_name': 'Stars'},
            'domaci_telefon': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mobitel': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'prebivalisce': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['infosys.Naslov']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'sluzbeni_telefon': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'uporabnik': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        }
    }

    complete_apps = ['infosys']
