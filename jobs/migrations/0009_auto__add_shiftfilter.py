# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ShiftFilter'
        db.create_table('jobs_shiftfilter', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('shift', self.gf('django.db.models.fields.related.ForeignKey')(related_name='filters', to=orm['jobs.Shift'])),
            ('field_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('char', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('min_int', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('max_int', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('min_float', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('max_float', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('bool_val', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('choice_val', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal('jobs', ['ShiftFilter'])

    def backwards(self, orm):
        # Deleting model 'ShiftFilter'
        db.delete_table('jobs_shiftfilter')

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
        'jobs.job': {
            'Meta': {'object_name': 'Job'},
            'amount_quoted': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '12', 'decimal_places': '2', 'blank': 'True'}),
            'amount_received': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '12', 'decimal_places': '2', 'blank': 'True'}),
            'client': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '1', 'max_length': '100'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '150'})
        },
        'jobs.jobfile': {
            'Meta': {'object_name': 'JobFile'},
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'job': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'files'", 'to': "orm['jobs.Job']"})
        },
        'jobs.shift': {
            'Meta': {'object_name': 'Shift'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'end': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'job': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'shifts'", 'to': "orm['jobs.Job']"}),
            'pays': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '12', 'decimal_places': '2', 'blank': 'True'}),
            'role': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['users.ContractorRole']"}),
            'start': ('django.db.models.fields.DateTimeField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '150'})
        },
        'jobs.shiftassignment': {
            'Meta': {'object_name': 'ShiftAssignment'},
            'contractor': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'on_time': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'shift': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['jobs.Shift']"}),
            'standby': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'jobs.shiftfilter': {
            'Meta': {'object_name': 'ShiftFilter'},
            'bool_val': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'char': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'choice_val': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'field_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'max_float': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'max_int': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'min_float': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'min_int': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'shift': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'filters'", 'to': "orm['jobs.Shift']"})
        },
        'users.attribute': {
            'Meta': {'object_name': 'Attribute'},
            'choices_str': ('django.db.models.fields.CharField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'}),
            'field_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'field_type': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_private': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'users.contractorrole': {
            'Meta': {'object_name': 'ContractorRole'},
            'attributes': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['users.Attribute']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['jobs']