# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'AttributeSet'
        db.delete_table('users_attributeset')

        # Adding model 'ContractorRole'
        db.create_table('users_contractorrole', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('users', ['ContractorRole'])

        # Adding M2M table for field attributes on 'ContractorRole'
        db.create_table('users_contractorrole_attributes', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('contractorrole', models.ForeignKey(orm['users.contractorrole'], null=False)),
            ('attribute', models.ForeignKey(orm['users.attribute'], null=False))
        ))
        db.create_unique('users_contractorrole_attributes', ['contractorrole_id', 'attribute_id'])

        # Adding model 'Attribute'
        db.create_table('users_attribute', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('field_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('field_type', self.gf('django.db.models.fields.IntegerField')()),
            ('is_private', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('users', ['Attribute'])

        # Adding model 'ContractorAttributeVal'
        db.create_table('users_contractorattributeval', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('attribute', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.Attribute'])),
            ('contractor', self.gf('django.db.models.fields.related.ForeignKey')(related_name='attributes', to=orm['users.Contractor'])),
            ('int_val', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('float_val', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('bool_val', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('choice_val', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('choices_str', self.gf('django.db.models.fields.CharField')(max_length=300, null=True, blank=True)),
        ))
        db.send_create_signal('users', ['ContractorAttributeVal'])

    def backwards(self, orm):
        # Adding model 'AttributeSet'
        db.create_table('users_attributeset', (
            ('nude_ready', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('hair_length', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('weight', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('waist', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('inseam', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('eye_color', self.gf('django.db.models.fields.IntegerField')(blank=True)),
            ('sex', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('dress_size', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('hair_color', self.gf('django.db.models.fields.IntegerField')(blank=True)),
            ('contractor', self.gf('django.db.models.fields.related.OneToOneField')(related_name='attributes', unique=True, to=orm['users.Contractor'])),
            ('cup_size', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('bust_chest', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('liquor_ready', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('hips', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('gaming_ready', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('swim_ready', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('height', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ethnicity', self.gf('django.db.models.fields.IntegerField')(blank=True)),
            ('lingerie_ready', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
        ))
        db.send_create_signal('users', ['AttributeSet'])

        # Deleting model 'ContractorRole'
        db.delete_table('users_contractorrole')

        # Removing M2M table for field attributes on 'ContractorRole'
        db.delete_table('users_contractorrole_attributes')

        # Deleting model 'Attribute'
        db.delete_table('users_attribute')

        # Deleting model 'ContractorAttributeVal'
        db.delete_table('users_contractorattributeval')

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
        'users.attribute': {
            'Meta': {'object_name': 'Attribute'},
            'field_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'field_type': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_private': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'users.client': {
            'Meta': {'object_name': 'Client'},
            'group_name': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'manager': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'clients'", 'null': 'True', 'to': "orm['users.Manager']"}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'})
        },
        'users.clientcontactinfo': {
            'Meta': {'object_name': 'ClientContactInfo'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'client': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'contacts'", 'to': "orm['users.Client']"}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'industry': ('django.db.models.fields.CharField', [], {'max_length': '150', 'blank': 'True'}),
            'is_primary': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'notes': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'role': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'})
        },
        'users.contractor': {
            'Meta': {'object_name': 'Contractor'},
            'birthdate': ('django.db.models.fields.DateField', [], {}),
            'contact_email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'default_photo': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'default_photo'", 'null': 'True', 'to': "orm['users.ContractorPhoto']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lat': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'lng': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'payment_email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'})
        },
        'users.contractorattributeval': {
            'Meta': {'object_name': 'ContractorAttributeVal'},
            'attribute': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['users.Attribute']"}),
            'bool_val': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'choice_val': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'choices_str': ('django.db.models.fields.CharField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'}),
            'contractor': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'attributes'", 'to': "orm['users.Contractor']"}),
            'float_val': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'int_val': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
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
        'users.contractorrole': {
            'Meta': {'object_name': 'ContractorRole'},
            'attributes': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['users.Attribute']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
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