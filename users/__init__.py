from django.contrib.auth.models import Group, Permission, ContentType
from django.core.exceptions import MiddlewareNotUsed

class EnsureGroupsMiddleware:
    def __init__(self):
        self.ensure_group('clientmanager', [('users', 'client'),
                                            ('jobs', 'job'),
                                            ('jobs', 'shift')])
        self.ensure_group('talentmanager', [('users', 'contractor')])
        self.ensure_group('shiftleader', [('jobs', '')])
        self.ensure_group('contractor', [])
        self.ensure_group('client', [])
        raise MiddlewareNotUsed

    def ensure_group(self, name, perms):
        if not Group.objects.filter(name=name).exists():
            print 'Creating group: {0}'.format(name)
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
                                 
