from django.db import models
from django.contrib.auth.models import User
from shift.shift_settings import INT_FIELD,FLOAT_FIELD,BOOL_FIELD,CHOICE_FIELD,CHAR_FIELD
from shift import choice_assoc, choice_rassoc, from_measurement

class Contractor(models.Model):
    user = models.OneToOneField(User)
    roles = models.ManyToManyField('ContractorRole')
    birthdate = models.DateField()
    contact_email = models.EmailField()
    payment_email = models.EmailField()
    phone = models.CharField(max_length=20)
    default_photo = models.ForeignKey('ContractorPhoto', related_name='default_photo', null=True)
    location = models.CharField(max_length=200)
    
    def __unicode__(self):
        return '%s %s' % (self.user.first_name, self.user.last_name)

class ContractorPhoto(models.Model):
    contractor = models.ForeignKey('Contractor', related_name='photos')
    photo = models.ImageField(upload_to='contractors')

class ContractorEducation(models.Model):
    contractor = models.ForeignKey('Contractor', related_name='educations')
    school = models.CharField(max_length=150)
    degree = models.CharField(max_length=100)
    is_major = models.BooleanField()
    description = models.CharField(max_length=300)
    
FIELD_TYPE_CHOICES = (
    (1, INT_FIELD),
    (2, FLOAT_FIELD),
    (3, BOOL_FIELD),
    (4, CHOICE_FIELD),
    (5, CHAR_FIELD),
)
    
class Attribute(models.Model):
    field_name = models.CharField(max_length=100)
    field_type = models.IntegerField(choices=FIELD_TYPE_CHOICES)
    choices_str = models.CharField(max_length=300, null=True, blank=True)
    is_private = models.BooleanField()

    def __unicode__(self):
        return self.field_name

    @property
    def choices(self):
        return eval(self.choices_str)

    def type(self):
        return choice_assoc(self.field_type, FIELD_TYPE_CHOICES)
    
    def mk_val(self, val):
        attr_val = ContractorAttributeVal(attribute=self)
        field_type = choice_assoc(self.field_type, FIELD_TYPE_CHOICES)
        if field_type == INT_FIELD:
            attr_val.int_val = int(from_measurement(val))
        elif field_type == FLOAT_FIELD:
            attr_val.float_val = float(from_measurement(val))
        elif field_type == BOOL_FIELD:
            attr_val.bool_val = (val.lower() == 'y')
        elif field_type == CHOICE_FIELD:
            attr_val.choice_val = choice_rassoc(val, self.choices)
            if attr_val.choice_val == None:
                raise ValueError('Invalid choice')
        elif field_type == CHAR_FIELD:
            attr_val.char_val = str(val)
        return attr_val
        

class ContractorRole(models.Model):
    name = models.CharField(max_length=100)
    attributes = models.ManyToManyField('Attribute')

    def __unicode__(self):
        return self.name
    
class ContractorAttributeVal(models.Model):
    attribute = models.ForeignKey('Attribute')
    contractor = models.ForeignKey('Contractor', related_name='attributes')
    char_val = models.CharField(max_length=100, null=True, blank=True)
    int_val = models.IntegerField(null=True, blank=True)
    float_val = models.FloatField(null=True, blank=True)
    bool_val = models.NullBooleanField(blank=True)
    choice_val = models.IntegerField(null=True, blank=True)

    @property
    def choices(self):
        return self.attribute.choices

    def val(self):
        t = self.attribute.type()
        if t == INT_FIELD:
            return self.int_val
        elif t == FLOAT_FIELD:
            return self.float_val
        elif t == BOOL_FIELD:
            return self.bool_val
        elif t == CHOICE_FIELD:
            return self.choice_val
        elif t == CHAR_FIELD:
            return self.char_val
        else:
            raise ValueError
    
    def __unicode__(self):
        fmt = '{0}={1}'
        field_name = self.attribute.field_name
        
        # normal values
        keys = ['char_val', 'int_val', 'float_val', 'bool_val']
        for k in keys:
            val = getattr(self, k)
            if val != None:
                return fmt.format(field_name, val)
            
        # choice value
        if self.choice_val != None:
            return fmt.format(field_name, choice_assoc(self.choice_val, self.choices))
    
        # all values = None
        return '{0} unset'.format(field_name)
                              
    
class Client(models.Model):
    user = models.OneToOneField(User)
    manager = models.ForeignKey('Manager', null=True, blank=True, related_name='clients')
    group_name = models.CharField(max_length=250)

    def __unicode__(self):
        return '%s %s' % (self.user.first_name, self.user.last_name)
    
class ClientContactInfo(models.Model):
    client = models.ForeignKey('Client', related_name='contacts')
    is_primary = models.BooleanField()
    name = models.CharField(max_length=150)
    role = models.CharField(max_length=100, blank=True)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=300, blank=True)
    industry = models.CharField(max_length=150, blank=True)
    notes = models.CharField(max_length=300, blank=True)

    def __unicode__(self):
        return 'Contact<%s>' % self.name

class Manager(models.Model):
    user = models.OneToOneField(User)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    
    def __unicode__(self):
        return 'Manager<%s %s>' % (self.user.first_name, self.user.last_name)
    

    
