import datetime
import time
import random

from django.db import models
from django.contrib.auth.models import User, Group

from django.utils import timezone

import sys

# Create your models here.
class Founder(models.Model):
    api_user = models.CharField(max_length=255)
    api_key = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)

class Company(Group):
    logo = models.ImageField(upload_to='companies')
    short_description = models.CharField(max_length=255)
    has_schedule = models.BooleanField(default=False)
    conflicts_due = models.DateTimeField(blank=True, null=True)
    class Meta:
        ordering = ['name']
    def __str__(self):
        return self.name
    def conflicts_past_due(self):
        if self.conflicts_due <= timezone.now():
            return True
        return False
    def getSortedRehearsals(self):
        rehearsals = self.rehearsal_set.all()
        sortedRehearsals = sorted(rehearsals, key = lambda t : len(t.getAvailableCasts()) )
        return sortedRehearsals
    def unscheduleRehearsals(self):
        totalCasts = self.cast_set.all()

        members = Member.objects.filter(company=self)
        for mem in members:
            r = mem.conflict_set.filter(description__startswith="%s Rehearsal" % (self))
            r.delete()

        for cast in totalCasts:
            cast.is_scheduled = False
            cast.rehearsal = None
            cast.save()

        self.has_schedule = False
        self.save()
        return True
        
    def scheduleRehearsals(self):
        totalCasts = self.cast_set.all()
        totalRehearsals = self.rehearsal_set.all()
        # print >> sys.stderr, "Total Casts"
        # print >> sys.stderr, totalCasts

        # print >> sys.stderr, "Total Rehearsals:"
        # print >> sys.stderr, totalRehearsals

        for n in totalCasts:
            minNumCasts = len(totalCasts)

            # find unscheduled rehearsal with least number of available casts (greater than 0)
            for rehearsal in totalRehearsals:
                numCasts = len(rehearsal.getAvailableCasts())
                if numCasts > 0 and numCasts < minNumCasts:
                    minNumCasts = numCasts

            print "Min Number of Casts at Beginning:"
            print minNumCasts

            # add all unscheduled rehearsals with min number to a list
            rehearsal_list = []
            for rehearsal in totalRehearsals:
                if len(rehearsal.getAvailableCasts()) == minNumCasts:
                    rehearsal_list.append(rehearsal)

            print "Rehearsals with min number of casts:"
            print rehearsal_list

            # find unscheduled cast available during rehearsals above with least number of available rehearsals
            minNumRehearsals = len(totalRehearsals)

            for rehearsal in rehearsal_list:
                available_casts = rehearsal.getAvailableCasts()
                for cast in available_casts:
                    numRehearsals = len(cast.getAvailableRehearsals())
                    if numRehearsals < minNumRehearsals:
                        minNumRehearsals = numRehearsals

            print "Min Number of Rehearsals for each cast:"
            print minNumRehearsals


            # add all casts with min number to a list
            cast_list = []
            casts = {}
            for rehearsal in rehearsal_list:
                available_casts = rehearsal.getAvailableCasts()
                for cast in available_casts:
                    if len(cast.getAvailableRehearsals()) == minNumRehearsals:
                        cast_list.append(cast)
                        casts[cast] = rehearsal

            print "Cast-rehearsal pairs where cast has min number of rehearsals:"
            print casts

            if cast_list:
                # randomly pick a cast from the remaining cast_list
                # cast = random.choice(cast_list)
                cast = random.choice(casts.keys())

                print "Randomly chosen cast:"
                print cast
                print casts[cast]

                # schedule the cast to its respective rehearsal
                cast.scheduleRehearsal(casts[cast])
                # rehearsal.is_scheduled = True
                cast.save()
                rehearsal.save()

                print "Is cast scheduled?"
                print cast.is_scheduled

                # print >> sys.stderr, "Is rehearsal scheduled?"
                # print >> sys.stderr, rehearsal.is_scheduled

                #return True

            else:
                self.has_schedule = False
                self.save()
                return "Could not complete scheduling... Too many conflicts"

        self.has_schedule = True
        self.save()
        return "Iteration done"

        




class TimeBlock(models.Model):
    start_time = models.TimeField('Start Time')
    end_time = models.TimeField('End Time')
    MONDAY = 'Mon'
    TUESDAY = 'Tue'
    WEDNESDAY = 'Wed'
    THURSDAY = 'Thu'
    FRIDAY = 'Fri'
    SATURDAY = 'Sat'
    SUNDAY = 'Sun'
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
    def end_day(self):
        dow = time.strptime(self.day_of_week, "%a").tm_wday
        if self.end_time < self.start_time:
            return self.DAY_OF_WEEK_CHOICES[dow+1][0]
        return self.DAY_OF_WEEK_CHOICES[dow][0]

class Rehearsal(TimeBlock):
    company = models.ForeignKey(Company)
    place = models.CharField(max_length=200)
    # is_scheduled = models.BooleanField(default=False)
    
    def __str__(self):
        return "%s: %s - %s (%s)" % (self.place, self.start_time, self.end_time, self.day_of_week)
    
    class Meta:
        ordering = ['day_of_week', 'start_time']

    def getAvailableCasts(self):
        casts = Cast.objects.filter(company=self.company)

        cast_list = []
        for cast in casts:
            if cast.is_scheduled == False:
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
    is_scheduled = models.BooleanField(default=False)
    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

    def scheduleRehearsal(self, reh):
        self.rehearsal = reh     
        
        # add rehearsal as a conflict for all the cast members
        members = Member.objects.filter(cast=self)
        for mem in members:
            mem.conflict_set.create(description="%s Rehearsal (%s)" % (self.company, self.name), start_time=reh.start_time, end_time=reh.end_time, day_of_week=reh.day_of_week)

        self.is_scheduled = True
        # reh.is_scheduled = True

    def getAvailableRehearsals(self):
        rehearsals = self.company.rehearsal_set.all()
        members = self.member_set.all()

        rehearsal_list = []
        for rehearsal in rehearsals:
            available = True
            for member in members:
                for conflict in member.conflict_set.all():
                    if conflict.description != 'Rehearsal':
                        if conflict.conflictsWith(rehearsal):
                            available = False
                            break
                if available == False:
                    break

            if available == True:
                rehearsal_list.append(rehearsal)
        return list(rehearsal_list)

class Member(User):
    cast = models.ManyToManyField(Cast, blank=True)
    def __str__(self):
        # if self.first_name and self.last_name:
        #     return "%s %s" % (self.first_name, self.last_name)
        return "%s %s (%s)" % (self.first_name, self.last_name, self.username)
    class Meta:
        ordering = ['username', 'first_name']

class Admin(models.Model):
    member = models.ForeignKey(Member)
    company = models.ForeignKey(Company)
    def __str__(self):
        return self.member.username

    class Meta:
        ordering = ['member']
    
class Choreographer(models.Model):
    member = models.ForeignKey(Member)
    company = models.ForeignKey(Company)
    cast = models.ForeignKey(Cast)

    def __str__(self):
        return self.member
        
    class Meta:
        ordering = ['member']
