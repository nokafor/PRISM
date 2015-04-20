import datetime

from django.db import models
from django.utils import timezone
from django.forms import ModelForm

from companies.models import Company, Member

# Create your models here.
class Conflict(models.Model):
    member = models.ForeignKey(Member)
    description = models.CharField(max_length=200)
    MONDAY = 'MON'
    TUESDAY = 'TUE'
    WEDNESDAY = 'WED'
    THURSDAY = 'THU'
    FRIDAY = 'FRI'
    SATURDAY = 'SAT'
    SUNDAY = 'SUN'
    DAY_OF_WEEK_CHOICES = (
        (MONDAY, 'Monday'),
        (TUESDAY, 'Tuesday'),
        (WEDNESDAY, 'Wednesday'),
        (THURSDAY, 'Thursday'),
        (FRIDAY, 'Friday'),
        (SATURDAY, 'Saturday'),
        (SUNDAY, 'Sunday'),
    )
    day_of_week = models.CharField(max_length=3, choices=DAY_OF_WEEK_CHOICES, default=MONDAY)
    start_time = models.TimeField('Conflict Start Time')
    end_time = models.TimeField('Conflict End Time')

class RehearsalTime(models.Model):
    company = models.ForeignKey(Company)
    place = models.CharField(max_length=200)
    start_time = models.TimeField('Rehearsal Start Time')
    end_time = models.TimeField('Rehearsal End Time')
    MONDAY = 'MON'
    TUESDAY = 'TUE'
    WEDNESDAY = 'WED'
    THURSDAY = 'THU'
    FRIDAY = 'FRI'
    SATURDAY = 'SAT'
    SUNDAY = 'SUN'
    DAY_OF_WEEK_CHOICES = (
        (MONDAY, 'Monday'),
        (TUESDAY, 'Tuesday'),
        (WEDNESDAY, 'Wednesday'),
        (THURSDAY, 'Thursday'),
        (FRIDAY, 'Friday'),
        (SATURDAY, 'Saturday'),
        (SUNDAY, 'Sunday'),
    )
    day_of_week = models.CharField(max_length=3, choices=DAY_OF_WEEK_CHOICES, default=MONDAY)

class ConflictForm(ModelForm):
    class Meta:
        model = Conflict
        fields = ['description', 'day_of_week', 'start_time', 'end_time']

class RehearsalForm(ModelForm):
    class Meta:
        model = RehearsalTime
        fields = ['place', 'day_of_week', 'start_time', 'end_time']