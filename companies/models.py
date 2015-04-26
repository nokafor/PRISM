import datetime

from django.db import models
from django.utils import timezone
from django.forms import ModelForm

# Create your models here.
class Company(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name

class TimeBlock(models.Model):
    start_time = models.TimeField('Start Time')
    end_time = models.TimeField('End Time')
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
    
    class Meta:
        abstract = True

class Rehearsal(TimeBlock):
    company = models.ForeignKey(Company)
    place = models.CharField(max_length=200)
    def __str__(self):
        return "%s: %s - %s (%s)" % (self.place, self.start_time, self.end_time, self.day_of_week)

class Cast(models.Model):
    name = models.CharField(max_length=255)
    rehearsal = models.ForeignKey(Rehearsal)

class Member(models.Model):
    first_name = models.CharField(max_length=200, blank=True)
    last_name = models.CharField(max_length=200, blank=True)
    netid = models.CharField(max_length=100)
    company = models.ManyToManyField(Company)
    cast = models.ManyToManyField(Cast, blank=True)
    def __str__(self):
        if self.first_name and self.last_name:
            return "%s %s" % (self.first_name, self.last_name)
        return self.netid

class Admin(models.Model):
    member = models.ForeignKey(Member)
    company = models.ForeignKey(Company)
    def __str__(self):
        return self.member
    
class Choreographer(models.Model):
    member = models.ForeignKey(Member)
    company = models.ForeignKey(Company)
    cast = models.ForeignKey(Cast)
    

class MemberForm(ModelForm):
    class Meta:
        model = Member
        fields = ['first_name', 'last_name', 'netid']

class AdminForm(ModelForm):
    class Meta:
        model = Admin
        fields = ['member']
    def __init__(self, *args, **kwargs):
        super(AdminForm, self).__init__(*args, **kwargs)
        if self.instance:
             self.fields['member'].queryset = Member.objects.filter(company=self.instance.company)
