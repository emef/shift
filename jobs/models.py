from django.db import models
from django.contrib.auth.models import User

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
        return 'Job<{0}>'.format(self.title)

class JobFile(models.Model):
    job = models.ForeignKey('Job', related_name='files')
    file = models.FileField(upload_to='jobfiles')

class Shift(models.Model):
    job = models.ForeignKey('Job', related_name='shifts')
    title = models.CharField(max_length=150)
    start = models.DateTimeField()
    end = models.DateTimeField()
    pays = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    location = models.CharField(max_length=250, blank=True)
    lat = models.FloatField(null=True, blank=True)
    lng = models.FloatField(null=True, blank=True)
    # filters...

    def __unicode__(self):
        return 'Shift<{0}>'.format(self.title)

class ShiftAssignment(models.Model):
    contractor = models.ForeignKey(User)
    shift = models.ForeignKey('Shift')
    standby = models.BooleanField()
    on_time = models.NullBooleanField()
    



