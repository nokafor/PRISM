from companies.models import Company, Member, Admin, Rehearsal, Cast, Choreographer
from profiles.models import Conflict

from django.forms import ModelForm

# Create your models here.
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

class ChoreographerForm(ModelForm):
    class Meta:
        model = Choreographer
        fields = ['member']
    def __init__(self, *args, **kwargs):
        super(ChoreographerForm, self).__init__(*args, **kwargs)
        if self.instance:
             self.fields['member'].queryset = Member.objects.filter(company=self.instance.company)

class ConflictForm(ModelForm):
    class Meta:
        model = Conflict
        fields = ['description', 'day_of_week', 'start_time', 'end_time']

class RehearsalForm(ModelForm):
    class Meta:
        model = Rehearsal
        fields = ['place', 'day_of_week', 'start_time', 'end_time']

class CastForm(ModelForm):
    class Meta:
        model = Cast
        fields = ['name']