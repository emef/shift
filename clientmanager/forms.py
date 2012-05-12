from pprint import pprint

from django import forms
from django.db import models
from shift.jobs.models import Job, Shift
from shift.users.models import AttributeSet


class JobForm(forms.ModelForm):
    class Meta:
        model = Job

class ShiftForm(forms.ModelForm):
    class Meta:
        model = Shift
        exclude = ('job',)


class DynForm(forms.Form):    
    """
    Dynamic form that allows the user to change and then verify the data that was parsed
    """
    class Meta:
        fields = None
    
    def set_fields(self, kwds, keys=None):
        """
        Set the fields in the form
        """
        if not keys:
            keys = kwds.keys()
            keys.sort()
        for k in keys:
            self.fields[k] = kwds[k]
            
    def set_data(self, kwds):
        """
        Set the data to include in the form
        """
        keys = kwds.keys()
        keys.sort()
        for k in keys:
            self.data[k] = kwds[k]
            
    def validate(self, post):
        """
        Validate the contents of the form
        """
        for name,field in self.fields.items():
            try:
                field.clean(post[name])
            except ValidationError, e:
                self.errors[name] = e.messages
                
    #att_form = DynForm()
    #att_form.setFields(fields)
    #return att_form

def mk_attribute_form(filters=None):
    fields = {}
    fieldorder = []

    choiceorder = []
    boolorder = []

    if not filters:
        filters = {}
     
    for field in AttributeSet._meta.fields:
        fieldname = field.attname        
        initial = filters.get(fieldname, None)
        if field._choices:
            choices = ((None, ' - ',),) + field._choices
            fields[fieldname] = forms.ChoiceField(choices=choices, 
                                                  required=False,
                                                  initial=initial)
            choiceorder.append(fieldname)
        elif isinstance(field, models.CharField):
            pass
        elif isinstance(field, models.IntegerField):
            min_name = '{0} min'.format(fieldname)
            max_name = '{0} max'.format(fieldname)
            fieldorder += [min_name, max_name]
            fields[min_name] = forms.IntegerField(required=False, initial=initial)
            fields[max_name] = forms.IntegerField(required=False, initial=initial)
        elif isinstance(field, models.FloatField):
            min_name = '{0} min'.format(fieldname)
            max_name = '{0} max'.format(fieldname)
            fieldorder += [min_name, max_name]
            fields[min_name] = forms.FloatField(required=False, initial=initial)
            fields[max_name] = forms.FloatField(required=False, initial=initial)
        elif isinstance(field, models.NullBooleanField):
            fields[fieldname] = forms.NullBooleanField(required=False, initial=initial)
            boolorder.append(fieldname)
        elif isinstance(field, models.AutoField):
            fields[fieldname] = forms.IntegerField(required=False, 
                                                   widget=forms.HiddenInput,
                                                   initial=initial)
            fieldorder.insert(0, fieldname)
        elif isinstance(field, models.OneToOneField):
            fields[fieldname] = forms.IntegerField(required=False, 
                                                   widget=forms.HiddenInput,
                                                   initial=initial)
            fieldorder.insert(0, fieldname)
            
    form = DynForm()
    form.set_fields(fields, fieldorder + choiceorder + boolorder)
    form.set_data(dict([('id', 1)]))

    return form
