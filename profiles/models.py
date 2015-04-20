from django.db import models
from django.forms import ModelForm

from companies.models import Member

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

class ConflictForm(ModelForm):
    class Meta:
        model = Conflict
        fields = ['description', 'day_of_week', 'start_time', 'end_time']