from django.db import models
from django.contrib.auth.models import User
from shift.users.choices import ETHNICITY_CHOICES, HAIR_COLOR_CHOICES, EYE_COLOR_CHOICES

class Contractor(models.Model):
    user = models.OneToOneField(User)
    birthdate = models.DateField()
    contact_email = models.EmailField()
    payment_email = models.EmailField()
    phone = models.CharField(max_length=20)
    default_photo = models.ForeignKey('ContractorPhoto', related_name='default_photo', null=True)
    lat = models.FloatField(null=True)
    lng = models.FloatField(null=True)

    def __unicode__(self):
        return 'Contractor<%s %s>' % (self.user.first_name, self.user.last_name)

class ContractorPhoto(models.Model):
    contractor = models.ForeignKey('Contractor', related_name='photos')
    photo = models.ImageField(upload_to='contractors')

class ContractorEducation(models.Model):
    contractor = models.ForeignKey('Contractor', related_name='educations')
    school = models.CharField(max_length=150)
    degree = models.CharField(max_length=100)
    is_major = models.BooleanField()
    description = models.CharField(max_length=300)

class AttributeSet(models.Model):
    contractor = models.OneToOneField('Contractor', related_name='attributes')
    sex = models.IntegerField(choices=((1, 'Female',), (2, 'Male')), null=True, blank=True)
    height = models.FloatField(null=True, blank=True)
    weight = models.FloatField(null=True, blank=True)
    bust_chest = models.FloatField(null=True, blank=True)
    waist = models.FloatField(null=True, blank=True)
    hips = models.FloatField(null=True, blank=True)
    inseam = models.FloatField(null=True, blank=True)
    dress_size = models.IntegerField(null=True, blank=True)
    cup_size = models.CharField(max_length=20, blank=True)
    ethnicity = models.IntegerField(choices=ETHNICITY_CHOICES, blank=True)
    hair_color = models.IntegerField(choices=HAIR_COLOR_CHOICES, blank=True)
    hair_length = models.FloatField(null=True, blank=True)
    eye_color = models.IntegerField(choices=EYE_COLOR_CHOICES, blank=True)
    nude_ready = models.NullBooleanField(null=True, blank=True)
    swim_ready = models.NullBooleanField(null=True, blank=True)
    lingerie_ready = models.NullBooleanField(null=True, blank=True)
    liquor_ready = models.NullBooleanField(null=True, blank=True)
    gaming_ready = models.NullBooleanField(null=True, blank=True)


class Client(models.Model):
    user = models.OneToOneField(User)
    manager = models.ForeignKey('Manager', null=True, related_name='clients')
    group_name = models.CharField(max_length=250)

    def __unicode__(self):
        return 'Client<%s %s>' % (self.user.first_name, self.user.last_name)
    
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
    

    
