import datetime

from django.db import models
from django.utils import timezone
from django.forms import ModelForm

from companies.models import Company, Member, Rehearsal, Cast, TimeBlock

# Create your models here.
class Conflict(TimeBlock):
    member = models.ForeignKey(Member)
    description = models.CharField(max_length=200)
    def __str__(self):
        return "%s: %s - %s (%s)" % (self.description, self.start_time, self.end_time, self.day_of_week)
    
    def conflictsWith(self, that):
        if that.start_time == self.end_time or that.end_time == self.start_time:
            return False
        if that.start_time >= self.start_time and that.start_time <= self.end_time:
            return True
        if that.end_time >= self.start_time and that.end_time <= self.end_time:
            return True

        # check if other event wraps around military clock
        if that.end_time < that.start_time:
            # if both wrap, eevents conflict
            if self.end_time < self.start_time:
                return True
            # if this event starts after that ends, then events conflict
            elif self.end_time > that.start_time:
                return True

        # check if this event wraps around military clock and 
        # other event ends after this starts
        if self.end_time < self.start_time and that.end_time > self.start_time:
            return True

        return False
        
class ConflictForm(ModelForm):
    class Meta:
        model = Conflict
        fields = ['description', 'day_of_week', 'start_time', 'end_time']

class RehearsalForm(ModelForm):
    class Meta:
        model = Rehearsal
        fields = ['place', 'day_of_week', 'start_time', 'end_time']

class CreateCastForm(ModelForm):
    class Meta:
        model = Cast
        fields = ['name']