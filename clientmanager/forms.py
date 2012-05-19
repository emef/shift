from pprint import pprint

from form_utils.forms import BetterForm
from django import forms
from django.db import models
from django.contrib.admin import widgets
from shift import choice_assoc
from shift.jobs.models import Job, Shift
from shift.users.models import ContractorRole

from shift.users.models import INT_FIELD, FLOAT_FIELD, BOOL_FIELD, CHOICE_FIELD, FIELD_TYPE_CHOICES


class JobForm(forms.ModelForm):
    class Meta:
        model = Job

class ShiftForm(forms.ModelForm):
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
        
        qs = ContractorRole.objects.all().exclude(name='default')
        self.fields['role'].queryset = qs
        
        
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
                
                
MIN_FMT = 'min. {0}'
MAX_FMT = 'max. {0}'
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
    
