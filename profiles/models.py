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
        fields = '__all__'