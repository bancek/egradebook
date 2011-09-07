# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Naslov'
        db.create_table('infosys_naslov', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ulica', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('hisna_stevilka', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('posta', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('kraj', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('infosys', ['Naslov'])

        # Adding model 'SolskoLeto'
        db.create_table('infosys_solskoleto', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('zacetno_leto', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('koncno_leto', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('aktivno', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('infosys', ['SolskoLeto'])

        # Adding model 'Profesor'
        db.create_table('infosys_profesor', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('uporabnik', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('ime', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('priimek', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('infosys', ['Profesor'])

        # Adding model 'Smer'
        db.create_table('infosys_smer', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('smer', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('infosys', ['Smer'])

        # Adding model 'Predmet'
        db.create_table('infosys_predmet', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('predmet', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('ime', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('infosys', ['Predmet'])

        # Adding model 'Stars'
        db.create_table('infosys_stars', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('uporabnik', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('ime', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('priimek', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('prebivalisce', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['infosys.Naslov'], unique=True, null=True, blank=True)),
            ('domaci_telefon', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('sluzbeni_telefon', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('mobitel', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
        ))
        db.send_create_signal('infosys', ['Stars'])

        # Adding model 'Dijak'
        db.create_table('infosys_dijak', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('uporabnik', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('ime', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('priimek', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('emso', self.gf('django.db.models.fields.CharField')(max_length=13, null=True, blank=True)),
            ('datum_rojstva', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('stalno_prebivalisce', self.gf('django.db.models.fields.related.OneToOneField')(blank=True, related_name='stalno_prebivalisce_dijaka', unique=True, null=True, to=orm['infosys.Naslov'])),
            ('zacasno_prebivalisce', self.gf('django.db.models.fields.related.OneToOneField')(blank=True, related_name='zacasno_prebivalisce_dijaka', unique=True, null=True, to=orm['infosys.Naslov'])),
            ('v_dijaskem_domu', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('oce', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='oce_dijaka', null=True, to=orm['infosys.Stars'])),
            ('mati', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='mati_dijaka', null=True, to=orm['infosys.Stars'])),
            ('mobitel', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
        ))
        db.send_create_signal('infosys', ['Dijak'])

        # Adding model 'Razred'
        db.create_table('infosys_razred', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('solsko_leto', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['infosys.SolskoLeto'])),
            ('ime', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('smer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['infosys.Smer'])),
            ('razrednik', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['infosys.Profesor'])),
        ))
        db.send_create_signal('infosys', ['Razred'])

        # Adding M2M table for field dijaki on 'Razred'
        db.create_table('infosys_razred_dijaki', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('razred', models.ForeignKey(orm['infosys.razred'], null=False)),
            ('dijak', models.ForeignKey(orm['infosys.dijak'], null=False))
        ))
        db.create_unique('infosys_razred_dijaki', ['razred_id', 'dijak_id'])

        # Adding model 'Poucuje'
        db.create_table('infosys_poucuje', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('profesor', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['infosys.Profesor'])),
            ('razred', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['infosys.Razred'])),
            ('predmet', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['infosys.Predmet'])),
        ))
        db.send_create_signal('infosys', ['Poucuje'])

        # Adding model 'OcenjevalnoObdobje'
        db.create_table('infosys_ocenjevalnoobdobje', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('solsko_leto', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['infosys.SolskoLeto'])),
            ('ime', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('zacetek', self.gf('django.db.models.fields.DateField')()),
            ('konec', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal('infosys', ['OcenjevalnoObdobje'])

        # Adding model 'Ocena'
        db.create_table('infosys_ocena', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('dijak', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['infosys.Dijak'])),
            ('poucuje', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['infosys.Poucuje'])),
            ('ocenjevalno_obdobje', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['infosys.OcenjevalnoObdobje'])),
            ('ocena', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('ocena_stevilka', self.gf('django.db.models.fields.IntegerField')()),
            ('zakljucena', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('infosys', ['Ocena'])

    def backwards(self, orm):
        
        # Deleting model 'Naslov'
        db.delete_table('infosys_naslov')

        # Deleting model 'SolskoLeto'
        db.delete_table('infosys_solskoleto')

        # Deleting model 'Profesor'
        db.delete_table('infosys_profesor')

        # Deleting model 'Smer'
        db.delete_table('infosys_smer')

        # Deleting model 'Predmet'
        db.delete_table('infosys_predmet')

        # Deleting model 'Stars'
        db.delete_table('infosys_stars')

        # Deleting model 'Dijak'
        db.delete_table('infosys_dijak')

        # Deleting model 'Razred'
        db.delete_table('infosys_razred')

        # Removing M2M table for field dijaki on 'Razred'
        db.delete_table('infosys_razred_dijaki')

        # Deleting model 'Poucuje'
        db.delete_table('infosys_poucuje')

        # Deleting model 'OcenjevalnoObdobje'
        db.delete_table('infosys_ocenjevalnoobdobje')

        # Deleting model 'Ocena'
        db.delete_table('infosys_ocena')

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
            'ime': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'mati': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'mati_dijaka'", 'null': 'True', 'to': "orm['infosys.Stars']"}),
            'mobitel': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'oce': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'oce_dijaka'", 'null': 'True', 'to': "orm['infosys.Stars']"}),
            'priimek': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
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
            'dijak': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['infosys.Dijak']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ocena': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'ocena_stevilka': ('django.db.models.fields.IntegerField', [], {}),
            'ocenjevalno_obdobje': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['infosys.OcenjevalnoObdobje']"}),
            'poucuje': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['infosys.Poucuje']"}),
            'zakljucena': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'infosys.ocenjevalnoobdobje': {
            'Meta': {'object_name': 'OcenjevalnoObdobje'},
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
            'Meta': {'object_name': 'Predmet'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ime': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'predmet': ('django.db.models.fields.CharField', [], {'max_length': '5'})
        },
        'infosys.profesor': {
            'Meta': {'object_name': 'Profesor'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ime': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'priimek': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'uporabnik': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'infosys.razred': {
            'Meta': {'object_name': 'Razred'},
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
            'Meta': {'object_name': 'Smer'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'smer': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'infosys.solskoleto': {
            'Meta': {'object_name': 'SolskoLeto'},
            'aktivno': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'koncno_leto': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'zacetno_leto': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        'infosys.stars': {
            'Meta': {'object_name': 'Stars'},
            'domaci_telefon': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ime': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'mobitel': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'prebivalisce': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['infosys.Naslov']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'priimek': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'sluzbeni_telefon': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'uporabnik': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        }
    }

    complete_apps = ['infosys']
