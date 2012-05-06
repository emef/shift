from django.db import models
from django.contrib.auth.models import User
from shift.users.choices import ETHNICITY_CHOICES, HAIR_COLOR_CHOICES, EYE_COLOR_CHOICES

class Contractor(models.Model):
    user = models.OneToOneField(User)
    birthdate = models.DateField()
    is_female = models.BooleanField()
    contact_email = models.EmailField()
    payment_email = models.EmailField()
    phone = models.CharField(max_length=20)
    default_photo = models.ForeignKey('ContractorPhoto', related_name='default_photo', null=True)
    lat = models.FloatField()
    lng = models.FloatField()
    attributes = models.OneToOneField('AttributeSet')

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
    height = models.FloatField(null=True)
    weight = models.FloatField(null=True)
    bust_chest = models.FloatField(null=True)
    waist = models.FloatField(null=True)
    hips = models.FloatField(null=True)
    inseam = models.FloatField(null=True)
    dress_size = models.IntegerField(null=True)
    cup_size = models.CharField(max_length=20, blank=True)
    ethnicity = models.IntegerField(choices=ETHNICITY_CHOICES, blank=True)
    hair_color = models.IntegerField(choices=HAIR_COLOR_CHOICES, blank=True)
    hair_length = models.FloatField(null=True)
    eye_color = models.IntegerField(choices=EYE_COLOR_CHOICES, blank=True)
    nude_ready = models.NullBooleanField(null=True)
    swim_ready = models.NullBooleanField(null=True)
    lingerie_ready = models.NullBooleanField(null=True)
    liquor_ready = models.NullBooleanField(null=True)
    gaming_ready = models.NullBooleanField(null=True)


class Client(models.Model):
    user = models.OneToOneField(User)
    manager = models.ForeignKey('Manager', null=True, related_name='clients')
    group_name = models.CharField(max_length=250)
    primary_contact = models.ForeignKey('ClientContactInfo', related_name='primary_contact')
    
class ClientContactInfo(models.Model):
    client = models.ForeignKey('Client', related_name='contacts')
    name = models.CharField(max_length=150)
    role = models.CharField(max_length=100, blank=True)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=300, blank=True)
    industry = models.CharField(max_length=150, blank=True)
    notes = models.CharField(max_length=300, blank=True)
    
class Manager(models.Model):
    user = models.OneToOneField(User)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    
