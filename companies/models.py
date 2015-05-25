import datetime

from django.db import models
from django.utils import timezone

# Create your models here.
class Company(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name
    def getSortedRehearsals(self):
        rehearsals = self.rehearsal_set.all()
        sortedRehearsals = sorted(rehearsals, key = lambda t : len(t.getAvailableCasts()) )
        return sortedRehearsals
    def scheduleRehearsals(self):
        N = len(self.cast_set.all())
        return N

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
    class Meta:
        ordering = ['day_of_week', 'start_time']
        
    def getAvailableCasts(self):
        casts = Cast.objects.filter(company=self.company)

        cast_list = []
        for cast in casts:
            members = cast.member_set.all()
            for member in members:
                available = True
                for conflict in member.conflict_set.all():
                    if conflict.conflictsWith(self):
                        available = False
                        break

                if available == False:
                    break

            if available == True:
                cast_list.append(cast)
        return list(cast_list)

class Cast(models.Model):
    company = models.ForeignKey(Company)
    name = models.CharField(max_length=255)
    rehearsal = models.ForeignKey(Rehearsal, blank=True, null=True)
    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

    def getAvailableRehearsals(self):
        rehearsals = self.company.rehearsal_set.all()
        members = self.member_set.all()

        rehearsal_list = []
        for rehearsal in rehearsals:
            available = True
            for member in members:
                for conflict in member.conflict_set.all():
                    if conflict.conflictsWith(rehearsal):
                        available = False
                        break
                if available == False:
                    break

            if available == True:
                rehearsal_list.append(rehearsal)
        return rehearsal_list

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
    class Meta:
        ordering = ['netid', 'first_name']

class Admin(models.Model):
    member = models.ForeignKey(Member)
    company = models.ForeignKey(Company)
    def __str__(self):
        return self.member.netid

    class Meta:
        ordering = ['member']
    
class Choreographer(models.Model):
    member = models.ForeignKey(Member)
    company = models.ForeignKey(Company)
    cast = models.ForeignKey(Cast)

    class Meta:
        ordering = ['member']
