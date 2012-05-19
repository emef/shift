from pprint import pprint


from django.contrib.auth.models import Group, Permission, ContentType
from django.core.exceptions import MiddlewareNotUsed
from shift import choice_rassoc
from shift.shift_settings import GROUPS, PUBLIC_ATTRIBUTES, PRIVATE_ATTRIBUTES, CONTRACTOR_ROLES
from shift.users.models import Attribute, ContractorRole, FIELD_TYPE_CHOICES

from south.modelsinspector import add_introspection_rules
add_introspection_rules([], ["^shift\.location\.LocationField"])


class EnsureDefaultsMiddleware:
    def __init__(self):
        self.ensure_groups(GROUPS)
        self.ensure_attributes(PUBLIC_ATTRIBUTES, False)
        self.ensure_attributes(PRIVATE_ATTRIBUTES, True)
        self.ensure_roles(CONTRACTOR_ROLES)
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

    def mk_attribute(self, field_name, field_type, is_private):
        if isinstance(field_type, tuple):
            choices = str(field_type)
            field_type = 'choices'
        else:
            choices = None
            
        field_id = choice_rassoc(field_type, FIELD_TYPE_CHOICES)
        
        attr = Attribute.objects.create(field_name=field_name,
                                        field_type=field_id,
                                        is_private=is_private,
                                        choices_str=choices)
        
        
    def ensure_attributes(self, attributes, is_private):
        keys = [attr[0] for attr in attributes]
        qs = Attribute.objects.all()
        existing = set(attr.field_name for attr in qs)
        for field_name, field_type in attributes:
            if not field_name in existing:
                self.mk_attribute(field_name, field_type, is_private)
                
                
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
        
        print 'to_add', (to_add)
                
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
        
                               
