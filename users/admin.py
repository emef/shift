from pprint import pprint
from django import forms
from django.contrib import admin
from django.contrib.auth.models import User, Group
from shift.users.models import *

class UserAdminForm(forms.ModelForm):
    first_name = forms.CharField()
    last_name = forms.CharField()
    username = forms.CharField()
    password = forms.CharField(required=False)
    
    def __init__(self, data=None, *args, **kwargs):
        super(UserAdminForm, self).__init__(data, *args, **kwargs)
        instance = kwargs.get('instance', None)
        if instance is not None:
            self['first_name'].field.initial = instance.user.first_name
            self['last_name'].field.initial = instance.user.last_name
            self['username'].field.initial = instance.user.username
            
        
    def is_valid(self):
        valid = super(UserAdminForm, self).is_valid()
        return valid
        
    def clean(self):
        cleaned_data = super(UserAdminForm, self).clean()
        if not self.is_valid():
            return cleaned_data
        
        try:
            if self.instance.user_id is None:
                user = User(username = cleaned_data['username'],
                            first_name = cleaned_data['first_name'],
                            last_name = cleaned_data['last_name'])
            else:
                user = User.objects.get(pk=self.instance.user_id)
                user.first_name = cleaned_data['first_name']
                user.last_name = cleaned_data['last_name']
                user.username = cleaned_data['username']
        except ValueError:
            raise forms.ValidationError('Could not create User')
        
        if len(cleaned_data['password']) > 0:
            user.set_password(cleaned_data['password'])
            
        user.save()
        
        cleaned_data['user'] = user.id
        self.instance.user_id = user.id
        
        return cleaned_data
     
    
class ClientAdminForm(UserAdminForm):
    class Meta:
        model = Client
        
class ContactInline(admin.StackedInline):
    model = ClientContactInfo
    extra = 1
    
class ClientAdmin(admin.ModelAdmin):
    exclude = ('user',)
    inlines = [ContactInline]
    form = ClientAdminForm
    fieldsets = (
        ('User Info', {
                'fields': ('username', 'password', 'first_name', 'last_name'),
        }),
        (None, {
            'fields': ('manager',),
        }),
    )

MANAGER_CHOICES = (
    ('clientmanager', 'Client Manager',),
    ('shiftleader', 'Shift Leader',),
    ('talentmanager', 'Talent Manager',),
)
    
class ManagerAdminForm(UserAdminForm):
    manager_roles = forms.MultipleChoiceField(choices=MANAGER_CHOICES)
    class Meta:
        model = Manager

    def clean(self):
        cleaned_data = super(ManagerAdminForm, self).clean()
        user = self.instance.user
        user.groups.all().delete()
        for role in cleaned_data['manager_roles']:
            print role
            user.groups.add(Group.objects.get(name=role))
        user.save()
        return cleaned_data
        
class ManagerAdmin(admin.ModelAdmin):
    exclude = ('user',)
    form = ManagerAdminForm
    fieldsets = (
        ('User Info', {
                'fields': ('username', 'password', 'first_name', 'last_name'),
        }),
        (None, {
            'fields': ('email', 'phone',),
        }),
        (None, {
            'fields': ('manager_roles',),
        }),
    )

class PhotoInline(admin.StackedInline):
    model = ContractorPhoto
    extra = 3

class AttributesInline(admin.StackedInline):
    model = AttributeSet
    classes = ('collapse open',)
    inline_classes = ('collapse open', 'hi')
    
class ContractorAdminForm(UserAdminForm):
    class Meta:
        model = Contractor
        extra = 0
        
class ContractorAdmin(admin.ModelAdmin):
    class Media:
        js = ('mezzanine/js/jquery-1.7.1.min.js', 'js/admin_photos.js',)
        
    exclude = ('user',)
    form = ContractorAdminForm
    inlines = [PhotoInline, AttributesInline]
    fieldsets = (
        ('User Info', {
                'fields': ('username', 'password', 'first_name', 'last_name'),
        }),
        ('Personal', {
            'fields': ('birthdate', 'is_female',),
        }),
        ('Contact', {
            'fields': ('phone', 'contact_email', 'payment_email'),
         }),
    )

admin.site.register(Client, ClientAdmin)
admin.site.register(Contractor, ContractorAdmin)
admin.site.register(Manager, ManagerAdmin)
admin.site.register(ClientContactInfo)
