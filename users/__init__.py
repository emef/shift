from pprint import pprint


from django.contrib.auth.models import Group, Permission, ContentType
from django.core.exceptions import MiddlewareNotUsed
from shift import choice_rassoc
import shift.shift_settings as settings
from shift.users.models import Attribute, AttributeGroup, ContractorRole, FIELD_TYPE_CHOICES

from south.modelsinspector import add_introspection_rules
add_introspection_rules([], ["^shift\.location\.LocationField"])


class EnsureDefaultsMiddleware:
    def __init__(self):
        self.ensure_groups(settings.GROUPS)
        #self.ensure_attributes(settings.ATTRIBUTES)
        #self.ensure_roles(settings.CONTRACTOR_ROLES)
        raise MiddlewareNotUsed

    def mk_group(self, name, perms):
        group = Group(name=name)
        group.save()
        for app_label, model in perms:
            if model == '':
                whole_app = Permission.objects.filter(content_type__app_label=app_label)
                group.permissions.add(*whole_app)
            else:
                ct = ContentType.objects.get(app_label=app_label,
                                             model=model)
                group.permissions.add(*Permission.objects.filter(content_type=ct))
        group.save()
    
    def ensure_groups(self, groups):
        for name, perms in groups:
            if not Group.objects.filter(name=name).exists():
                self.mk_group(name, perms)

    def mk_attribute(self, field_name, field_type, group):
        if isinstance(field_type, tuple):
            choices = str(field_type)
            field_type = 'choices'
        else:
            choices = None
            
        field_id = choice_rassoc(field_type, FIELD_TYPE_CHOICES)
        
        attr = Attribute.objects.create(field_name=field_name,
                                        field_type=field_id,
                                        is_private=False,
                                        choices_str=choices,
                                        group=group)
        
        
    def ensure_attributes(self, attributes):
        for name, attrs in attributes:
            keys = [attr[0] for attr in attrs]
            group, created = AttributeGroup.objects.get_or_create(name=name)
            existing = set(attr.field_name for attr in group.attributes.all())
            for field_name, field_type in attrs:
                if not field_name in existing:
                    self.mk_attribute(field_name, field_type, group)
                else:
                    existing.remove(field_name)
        
            Attribute.objects.filter(field_name__in=existing).delete()
            
                
    def mk_role(self, name, attributes):
        attrs = Attribute.objects.filter(field_name__in=attributes)
        role = ContractorRole.objects.create(name=name)
        role.attributes.add(*attrs)
        role.save()
        
    def verify_role(self, role, attributes):
        existing = dict((r.field_name, r) for r in role.attributes.all())

        to_add = []
        for field_name in attributes:
            if field_name in existing:
                del existing[field_name]
            else:
                to_add.append(field_name)
                
        # remove old attributes
        old = role.attributes.filter(field_name__in=existing.keys())
        if old:
            role.attributes.remove(*old)
            
        new = Attribute.objects.filter(field_name__in=to_add)
        if new:
            role.attributes.add(*new)
            
    def ensure_roles(self, roles):
        qs = ContractorRole.objects.all()
        existing = dict((role.name, role) for role in qs)
        for name, attributes in roles:
            if not name in existing:
                self.mk_role(name, attributes)
            else:
                self.verify_role(existing[name], attributes)
                del existing[name]
            
        # remove old roles
        ContractorRole.objects.filter(name__in=existing).delete()
        
                               
