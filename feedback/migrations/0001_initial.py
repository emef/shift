# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'JobFeedback'
        db.create_table('feedback_jobfeedback', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('job', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['jobs.Job'], unique=True)),
            ('promotion_sales', self.gf('django.db.models.fields.IntegerField')()),
            ('promotion_sales_explain', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('contractors', self.gf('django.db.models.fields.IntegerField')()),
            ('contractors_explain', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('system', self.gf('django.db.models.fields.IntegerField')()),
            ('system_explain', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('expectations_met', self.gf('django.db.models.fields.IntegerField')()),
            ('most_positive', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('improvement', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
        ))
        db.send_create_signal('feedback', ['JobFeedback'])

        # Adding model 'ShiftFeedback'
        db.create_table('feedback_shiftfeedback', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('shift', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['jobs.Shift'], unique=True)),
            ('overall', self.gf('django.db.models.fields.IntegerField')()),
            ('friendliness', self.gf('django.db.models.fields.IntegerField')()),
            ('sales_targets', self.gf('django.db.models.fields.IntegerField')()),
            ('appearance', self.gf('django.db.models.fields.IntegerField')()),
            ('expectations', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('feedback', ['ShiftFeedback'])

    def backwards(self, orm):
        # Deleting model 'JobFeedback'
        db.delete_table('feedback_jobfeedback')

        # Deleting model 'ShiftFeedback'
        db.delete_table('feedback_shiftfeedback')

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
        'feedback.jobfeedback': {
            'Meta': {'object_name': 'JobFeedback'},
            'contractors': ('django.db.models.fields.IntegerField', [], {}),
            'contractors_explain': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'expectations_met': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'improvement': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'job': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['jobs.Job']", 'unique': 'True'}),
            'most_positive': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'promotion_sales': ('django.db.models.fields.IntegerField', [], {}),
            'promotion_sales_explain': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'system': ('django.db.models.fields.IntegerField', [], {}),
            'system_explain': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'})
        },
        'feedback.shiftfeedback': {
            'Meta': {'object_name': 'ShiftFeedback'},
            'appearance': ('django.db.models.fields.IntegerField', [], {}),
            'expectations': ('django.db.models.fields.IntegerField', [], {}),
            'friendliness': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'overall': ('django.db.models.fields.IntegerField', [], {}),
            'sales_targets': ('django.db.models.fields.IntegerField', [], {}),
            'shift': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['jobs.Shift']", 'unique': 'True'})
        },
        'jobs.job': {
            'Meta': {'object_name': 'Job'},
            'amount_quoted': ('django.db.models.fields.DecimalField', [], {'max_digits': '12', 'decimal_places': '2'}),
            'amount_received': ('django.db.models.fields.DecimalField', [], {'max_digits': '12', 'decimal_places': '2'}),
            'client': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '1', 'max_length': '100'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '150'})
        },
        'jobs.shift': {
            'Meta': {'object_name': 'Shift'},
            'end': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'job': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['jobs.Job']"}),
            'lat': ('django.db.models.fields.FloatField', [], {}),
            'lng': ('django.db.models.fields.FloatField', [], {}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'pays': ('django.db.models.fields.DecimalField', [], {'max_digits': '12', 'decimal_places': '2'}),
            'start': ('django.db.models.fields.DateTimeField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '150'})
        }
    }

    complete_apps = ['feedback']