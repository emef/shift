from django.db import models
from django.contrib.auth.models import User
from shift.users.models import ContractorRole, Contractor
from shift.shift_settings import attr_info
from shift import choice_assoc

from shift.shift_settings import CHAR_FIELD,INT_FIELD,FLOAT_FIELD,BOOL_FIELD,CHOICE_FIELD

BOOL_MAP = {
    2: True,
    3: False,
}

JOB_OPEN = 'open'
JOB_PENDING = 'pending'
JOB_IN_PROGRESS = 'in progress'
JOB_COMPLETED = 'completed'
JOB_FINALIZED = 'finalized'

JOB_STATUS_CHOICES = (
    (1, JOB_OPEN),
    (2, JOB_PENDING),
    (3, JOB_IN_PROGRESS),
    (4, JOB_COMPLETED),
    (5, JOB_FINALIZED)
)

class Job(models.Model):
    client = models.ForeignKey(User)
    title = models.CharField(max_length=150)
    description = models.TextField()
    amount_quoted = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    amount_received = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    status = models.IntegerField(max_length=100, choices=JOB_STATUS_CHOICES, default=1)

    def __unicode__(self):
        return self.title

    def open_shifts(self):
        return filter(lambda u: not u.is_assigned, self.shifts.all())
    
class JobFile(models.Model):
    job = models.ForeignKey('Job', related_name='files')
    file = models.FileField(upload_to='jobfiles')

class Shift(models.Model):
    job = models.ForeignKey('Job', related_name='shifts')
    contractor = models.ForeignKey(Contractor, related_name='shifts', null=True)
    standby_contractors = models.ManyToManyField(Contractor, related_name='standby_shifts')
    role = models.ForeignKey(ContractorRole)
    title = models.CharField(max_length=150)
    start = models.DateTimeField()
    end = models.DateTimeField()
    pays = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    
    def __unicode__(self):
        return self.title

    @property
    def is_assigned(self):
        return self.contractor != None

    def update_filters(self, attrs):
        self.filters.all().delete()
        errors = []

        for field_name, field_val in attrs.items():
            try:
                _, field_type = attr_info(field_name)
            except:
                print field_name
                return
            if attr_info == None:
                errors.append('{0} is not a valid field'.format(field_name))
            
            filter = ShiftFilter(field_name=field_name)
            
            if field_type == CHAR_FIELD:
                filter.char = field_val
            elif field_type == INT_FIELD:
                min_val, max_val = field_val.split(',')
                try:
                    filter.min_int = int(min_val)
                    filter.max_int = int(max_val)
                except:
                    errors.append('{0} had invalid values ({1})'.format(field_name, field_val))
                    continue
            elif field_type == FLOAT_FIELD:
                min_val, max_val = field_val.split(',')
                try:
                    filter.min_float = float(min_val)
                    filter.max_float = float(max_val)
                except:
                    errors.append('{0} had invalid values ({1})'.format(field_name, field_val))
                    continue
            elif field_type == BOOL_FIELD:
                bool_val = int(field_val)
                print bool_val, bool_val in BOOL_MAP
                if bool_val in BOOL_MAP:
                    print 'set!'
                    filter.bool = BOOL_MAP[bool_val]
                else:
                    # ignore the value, it is set to Unknown in the form
                    continue
            elif isinstance(field_type, tuple):
                try:
                    choice = int(field_val)
                    filter.choice = choice
                except:
                    errors.append('{0} had invalid choice value ({1})'.format(
                            field_name, field_val))
                    continue
            else:
                raise ValueError('Invalid field type')
            
            self.filters.add(filter)
            
        self.save()
        return errors

    def candidates(self, max_candidates):
        return [{'contractor': c, 'score': 1} for c in Contractor.objects.all()]
    

class ShiftFilter(models.Model):
    shift = models.ForeignKey('Shift', related_name='filters')
    field_name = models.CharField(max_length=100)
    char = models.CharField(max_length=100, null=True, blank=True)
    min_int = models.IntegerField(null=True, blank=True)
    max_int = models.IntegerField(null=True, blank=True)
    min_float = models.FloatField(null=True, blank=True)
    max_float = models.FloatField(null=True, blank=True)
    bool = models.NullBooleanField(blank=True)
    choice = models.IntegerField(null=True, blank=True)

    def type(self):
        if self.char != None:
            return CHAR_FIELD
        elif self.min_int != None:
            return INT_FIELD
        elif self.min_float != None:
            return FLOAT_FIELD
        elif self.bool != None:
            return BOOL_FIELD
        elif self.choice != None:
            return CHOICE_FIELD
        else:
            return None
    
    def val(self):
        t = self.type()
        if t == CHAR_FIELD:
            return self.char
        elif t == INT_FIELD:
            return (self.min_int, self.max_int)
        elif t == FLOAT_FIELD:
            return (self.min_float, self.max_float)
        elif t == BOOL_FIELD:
            return 2 if self.bool else 3
        elif t == CHOICE_FIELD:
            return self.choice
        else:
            return None
    
    def display_val(self):
        if self.type() == CHOICE_FIELD:
            grp, choices = attr_info(self.field_name)
            return choice_assoc(self.choice, choices)
        elif self.type() == BOOL_FIELD:
            return self.bool
        else:
            return self.val()
        
        
    def __unicode__(self):
        fmt = lambda x: '{0}={1}'.format(self.field_name, x)
        val = self.display_val()
        if isinstance(val, tuple):
            return fmt('{0}-{1}'.format(*val))
        else:
            return fmt(val)
        

class ShiftAssignment(models.Model):
    contractor = models.ForeignKey(User)
    shift = models.ForeignKey('Shift')
    standby = models.BooleanField()
    on_time = models.NullBooleanField()
    



