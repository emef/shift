from pprint import pprint

from form_utils.forms import BetterForm
from django import forms
from django.db import models
from django.contrib.admin import widgets
from shift import choice_rassoc
from shift.jobs.models import Job, Shift
from shift.users.models import ContractorRole

from shift.users.models import INT_FIELD, FLOAT_FIELD, BOOL_FIELD, CHOICE_FIELD
from shift.users.models import CHAR_FIELD, FIELD_TYPE_CHOICES

import shift_settings as settings


class JobForm(forms.ModelForm):
    class Meta:
        model = Job

class ShiftForm(forms.ModelForm):
    id = forms.IntegerField(required=False, widget=forms.HiddenInput())
    class Meta:
        model = Shift
        exclude = ('job',)
        
    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.4.2/jquery.min.js',
            'http://maps.google.com/maps/api/js?sensor=false',
        )

    def __init__(self, *args, **kwargs):
        super(ShiftForm, self).__init__(*args, **kwargs)
        
        qs = ContractorRole.objects.all()
        self.fields['role'].queryset = qs
        self.fields['role'].initial = qs[0]
        
        
def dyn_form(fields, data, fieldsets):
    
    _Meta = type('Meta', (), {'fieldsets': fieldsets})
    
    class _dyn_form(BetterForm):
        Meta = _Meta
        
        def __new__(self, *args, **kwargs):
            self.Meta.fieldsets = fieldsets
            return BetterForm.__new__(self, *args, **kwargs)
            
        def __init__(self, *args, **kwargs):
            super(_dyn_form, self).__init__(*args, **kwargs)
            for k,v in fields.items():
                self.fields[k] = v
                
            for k,v in data.items():
                self.data[k] = v
                
        def validate(self, post):
            for name,field in self.fields.items():
                try:
                    field.clean(post[name])
                except ValidationError, e:
                    self.errors[name] = e.messages

    return _dyn_form()
                
                
MIN_FMT = 'min({0})'
MAX_FMT = 'max({0})'
BLANK_CHOICE = (-1, '----------')

def mk_null_choices(choices):
    return (BLANK_CHOICE,) + choices


def mk_role_form(role):
    fields = { }
    fieldsets = []
    
    for attr in role.attributes.all():
        fname = attr.field_name
        ftype = choice_assoc(attr.field_type, FIELD_TYPE_CHOICES)
        is_range = False
        if ftype == INT_FIELD:
            is_range = True
            field_class = forms.IntegerField
        elif ftype == FLOAT_FIELD:
            is_range = True
            field_class = forms.FloatField
        elif ftype == BOOL_FIELD:
            fields[fname] = forms.NullBooleanField(required=False)
            fieldsets.append( (None, {'fields': [fname]}) )
        elif ftype == CHOICE_FIELD:
            choices = mk_null_choices(attr.choices)
            fields[fname] = forms.ChoiceField(choices=choices, required=False)
            fieldsets.append( (None, {'fields': [fname]}) )
        else:
            raise ValueError('invalid field type: {0}'.format(ftype))
            
        if is_range:
            min_name, max_name = (MIN_FMT.format(fname), MAX_FMT.format(fname))
            fields[min_name] = field_class(required=False)
            fields[max_name] = field_class(required=False)
            fieldsets.append( (None, {'fields': [min_name, max_name]}) )
        
            
    return dyn_form(fields, {}, fieldsets)
    
def mk_fields(field, role):
    FIELD_MAP = {
        INT_FIELD: (forms.IntegerField, forms.HiddenInput),
        FLOAT_FIELD: (forms.FloatField, forms.HiddenInput),
        CHAR_FIELD: (forms.CharField, forms.TextInput),
        BOOL_FIELD: (forms.NullBooleanField, forms.NullBooleanSelect),
        CHOICE_FIELD: (forms.ChoiceField, forms.Select),
    }
    
    def mk_field (name, ftype, css_class, **kwargs): 
        fklass, wklass = FIELD_MAP[ftype]
        attrs = {'class': css_class}
        return (name, fklass(required=False, widget=wklass(attrs=attrs), **kwargs))
    
    def mk_range(fname, ftype, css_class):
        css_class = css_class + ' range'
        return [mk_field(fname, ftype, css_class)]
                
    fname, ftype = field
    
    if fname in settings.MALE_ONLY_ATTRIBUTES:
        css_class = "{0} male".format(role)
    elif fname in settings.FEMALE_ONLY_ATTRIBUTES:
        css_class = "{0} female".format(role)
    else:
        css_class = role
    
    if ftype in (INT_FIELD, FLOAT_FIELD):
        return mk_range(fname, ftype, css_class)
    elif isinstance(ftype, tuple):
        # tuple => choice field
        choices = mk_null_choices(ftype)
        return [mk_field(fname, CHOICE_FIELD, css_class, choices=choices)]
    else:
        return [mk_field(fname, ftype, css_class)]

_ATTR_MAP = {}
for grp_name, attrs in settings.ATTRIBUTES:
    for attr in attrs:
        _ATTR_MAP[attr[0]] = (grp_name, attr[1])
        
def attr_info(attr):
    "returns (group_name, field_type)"
    return _ATTR_MAP[attr]
    
def join(lists):
    return reduce(lambda u,v: u + v, lists)

def mk_role_forms():
    forms = []
    for rname, attrs in settings.CONTRACTOR_ROLES:
        # fdict = { '<group_name>', [(<fname>, <ftype>), ... ], ... }
        fdict = {}
        dynfields = {}
        dynfieldsets = []
        
        for attr in attrs:
            grp_name, ftype = attr_info(attr)
            if grp_name in fdict:
                fdict[grp_name].append((attr, ftype))
            else:
                fdict[grp_name] = [(attr, ftype)]
        
        for grp_name, _ in settings.ATTRIBUTES:
            if grp_name in fdict:
                fields = fdict[grp_name]
                newfields = dict(join(mk_fields(field, rname) for field in fields))
                dynfields.update(newfields)
                dynfieldsets.append( (grp_name, {'fields': newfields.keys()}) )
            
            
        forms.append( {'name': rname,
                       'form': dyn_form(dynfields, {}, dynfieldsets)} )

    return forms
