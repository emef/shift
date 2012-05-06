# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Contractor'
        db.create_table('users_contractor', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('birthdate', self.gf('django.db.models.fields.DateField')()),
            ('is_female', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('contact_email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('payment_email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('default_photo', self.gf('django.db.models.fields.related.ForeignKey')(related_name='default_photo', null=True, to=orm['users.ContractorPhoto'])),
            ('lat', self.gf('django.db.models.fields.FloatField')()),
            ('lng', self.gf('django.db.models.fields.FloatField')()),
            ('attributes', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['users.AttributeSet'], unique=True)),
        ))
        db.send_create_signal('users', ['Contractor'])

        # Adding model 'ContractorPhoto'
        db.create_table('users_contractorphoto', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('contractor', self.gf('django.db.models.fields.related.ForeignKey')(related_name='photos', to=orm['users.Contractor'])),
            ('photo', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
        ))
        db.send_create_signal('users', ['ContractorPhoto'])

        # Adding model 'ContractorEducation'
        db.create_table('users_contractoreducation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('contractor', self.gf('django.db.models.fields.related.ForeignKey')(related_name='educations', to=orm['users.Contractor'])),
            ('school', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('degree', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('is_major', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=300)),
        ))
        db.send_create_signal('users', ['ContractorEducation'])

        # Adding model 'AttributeSet'
        db.create_table('users_attributeset', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('height', self.gf('django.db.models.fields.FloatField')(null=True)),
            ('weight', self.gf('django.db.models.fields.FloatField')(null=True)),
            ('bust_chest', self.gf('django.db.models.fields.FloatField')(null=True)),
            ('waist', self.gf('django.db.models.fields.FloatField')(null=True)),
            ('hips', self.gf('django.db.models.fields.FloatField')(null=True)),
            ('inseam', self.gf('django.db.models.fields.FloatField')(null=True)),
            ('dress_size', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('cup_size', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('ethnicity', self.gf('django.db.models.fields.IntegerField')(blank=True)),
            ('hair_color', self.gf('django.db.models.fields.IntegerField')(blank=True)),
            ('hair_length', self.gf('django.db.models.fields.FloatField')(null=True)),
            ('eye_color', self.gf('django.db.models.fields.IntegerField')(blank=True)),
            ('nude_ready', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('swim_ready', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('lingerie_ready', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('liquor_ready', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('gaming_ready', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
        ))
        db.send_create_signal('users', ['AttributeSet'])

        # Adding model 'Client'
        db.create_table('users_client', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('manager', self.gf('django.db.models.fields.related.ForeignKey')(related_name='clients', null=True, to=orm['users.Manager'])),
            ('group_name', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('primary_contact', self.gf('django.db.models.fields.related.ForeignKey')(related_name='primary_contact', to=orm['users.ClientContactInfo'])),
        ))
        db.send_create_signal('users', ['Client'])

        # Adding model 'ClientContactInfo'
        db.create_table('users_clientcontactinfo', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('client', self.gf('django.db.models.fields.related.ForeignKey')(related_name='contacts', to=orm['users.Client'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('role', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=300, blank=True)),
            ('industry', self.gf('django.db.models.fields.CharField')(max_length=150, blank=True)),
            ('notes', self.gf('django.db.models.fields.CharField')(max_length=300, blank=True)),
        ))
        db.send_create_signal('users', ['ClientContactInfo'])

        # Adding model 'Manager'
        db.create_table('users_manager', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal('users', ['Manager'])

    def backwards(self, orm):
        # Deleting model 'Contractor'
        db.delete_table('users_contractor')

        # Deleting model 'ContractorPhoto'
        db.delete_table('users_contractorphoto')

        # Deleting model 'ContractorEducation'
        db.delete_table('users_contractoreducation')

        # Deleting model 'AttributeSet'
        db.delete_table('users_attributeset')

        # Deleting model 'Client'
        db.delete_table('users_client')

        # Deleting model 'ClientContactInfo'
        db.delete_table('users_clientcontactinfo')

        # Deleting model 'Manager'
        db.delete_table('users_manager')

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
        'users.attributeset': {
            'Meta': {'object_name': 'AttributeSet'},
            'bust_chest': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'cup_size': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'dress_size': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'ethnicity': ('django.db.models.fields.IntegerField', [], {'blank': 'True'}),
            'eye_color': ('django.db.models.fields.IntegerField', [], {'blank': 'True'}),
            'gaming_ready': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'hair_color': ('django.db.models.fields.IntegerField', [], {'blank': 'True'}),
            'hair_length': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'height': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'hips': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inseam': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'lingerie_ready': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'liquor_ready': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'nude_ready': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'swim_ready': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'waist': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'weight': ('django.db.models.fields.FloatField', [], {'null': 'True'})
        },
        'users.client': {
            'Meta': {'object_name': 'Client'},
            'group_name': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'manager': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'clients'", 'null': 'True', 'to': "orm['users.Manager']"}),
            'primary_contact': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'primary_contact'", 'to': "orm['users.ClientContactInfo']"}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'})
        },
        'users.clientcontactinfo': {
            'Meta': {'object_name': 'ClientContactInfo'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'client': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'contacts'", 'to': "orm['users.Client']"}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'industry': ('django.db.models.fields.CharField', [], {'max_length': '150', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'notes': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'role': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'})
        },
        'users.contractor': {
            'Meta': {'object_name': 'Contractor'},
            'attributes': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['users.AttributeSet']", 'unique': 'True'}),
            'birthdate': ('django.db.models.fields.DateField', [], {}),
            'contact_email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'default_photo': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'default_photo'", 'null': 'True', 'to': "orm['users.ContractorPhoto']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_female': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'lat': ('django.db.models.fields.FloatField', [], {}),
            'lng': ('django.db.models.fields.FloatField', [], {}),
            'payment_email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'})
        },
        'users.contractoreducation': {
            'Meta': {'object_name': 'ContractorEducation'},
            'contractor': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'educations'", 'to': "orm['users.Contractor']"}),
            'degree': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_major': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'school': ('django.db.models.fields.CharField', [], {'max_length': '150'})
        },
        'users.contractorphoto': {
            'Meta': {'object_name': 'ContractorPhoto'},
            'contractor': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'photos'", 'to': "orm['users.Contractor']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'})
        },
        'users.manager': {
            'Meta': {'object_name': 'Manager'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'})
        }
    }

    complete_apps = ['users']