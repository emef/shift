from django.db import models
from shift.jobs.models import Job, Shift

RANGE_CHOICES = tuple(zip(range(1,5), range(1,5)))

class JobFeedback(models.Model):
    job = models.OneToOneField(Job)
    promotion_sales = models.IntegerField(choices=RANGE_CHOICES)
    promotion_sales_explain = models.CharField(max_length=200, blank=True)
    contractors = models.IntegerField(choices=RANGE_CHOICES)
    contractors_explain = models.CharField(max_length=200, blank=True)
    system = models.IntegerField(choices=RANGE_CHOICES)
    system_explain = models.CharField(max_length=200, blank=True)
    expectations_met = models.IntegerField(choices=RANGE_CHOICES)
    most_positive = models.CharField(max_length=200, blank=True)
    improvement = models.CharField(max_length=200, blank=True)
    
class ShiftFeedback(models.Model):
    shift = models.OneToOneField(Shift)
    overall = models.IntegerField(choices=RANGE_CHOICES)
    friendliness = models.IntegerField(choices=RANGE_CHOICES)
    sales_targets = models.IntegerField(choices=RANGE_CHOICES)
    appearance = models.IntegerField(choices=RANGE_CHOICES)
    expectations = models.IntegerField(choices=RANGE_CHOICES)
