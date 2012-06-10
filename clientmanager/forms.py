from pprint import pprint

from form_utils.forms import BetterForm
from django import forms
from django.db import models
from django.contrib.admin import widgets
from shift import choice_rassoc
from shift.jobs.models import Job, Shift
from shift.users.models import ContractorRole

# import constants
from shift.shift_settings import INT_FIELD, FLOAT_FIELD, BOOL_FIELD, CHOICE_FIELD
from shift.shift_settings import CHAR_FIELD, attr_info
from shift.users.models import FIELD_TYPE_CHOICES

import shift.shift_settings as settings


class JobForm(forms.ModelForm):
    class Meta:
        model = Job

class ShiftForm(forms.ModelForm):
    id = forms.IntegerField(required=False, widget=forms.HiddenInput())
    class Meta:
        model = Shift
        exclude = ('job', 'contractor', 'standby_contractors',)
        
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
                if k in data:
                    v.initial = data[k]
                self.fields[k] = v
                
            for k,v in data.items():
                if k in fields:
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


NULL_BOOL_CHOICES = (
    (1, 'N/A'),
    (2, 'Yes'),
    (3, 'No'),
)

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
            fields[fname] = forms.NullBooleanField(required=False, choices=NULL_BOOL_CHOICES)
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
        BOOL_FIELD: (forms.IntegerField, forms.Select),
        CHOICE_FIELD: (forms.ChoiceField, forms.Select),
    }
    
    def mk_field (name, ftype, css_class, **kwargs): 
        fklass, wklass = FIELD_MAP[ftype]
        attrs = {'class': css_class}
        if ftype == BOOL_FIELD:
            w = wklass(attrs=attrs, choices=NULL_BOOL_CHOICES)
        else:
            w = wklass(attrs=attrs)
        return (name, fklass(required=False, widget=w, **kwargs))
    
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
    
def join(lists):
    return reduce(lambda u,v: u + v, lists)

def mk_initial(shift):
    if shift == None:
        return {}
    
    initial = {}
    for f in shift.filters.all():
        t = f.type()
        if t == INT_FIELD or t == FLOAT_FIELD:
            minv, maxv = f.val()
            initial[f.field_name] = '{0},{1}'.format(minv, maxv)
        else:
            initial[f.field_name] = f.val()

    pprint(initial)
    return initial
            

def mk_role_forms(shift=None):
    forms = []
    initial = mk_initial(shift)
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
            
            
#        print initial
#        pprint(dynfields)
        forms.append( {'name': rname,
                       'form': dyn_form(dynfields, initial, dynfieldsets)} )
        
    return forms
