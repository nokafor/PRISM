from django import forms

class NameForm(forms.Form):
    first_name = forms.CharField(label='First Name', max_length=200)
    last_name = forms.CharField(label='Last Name', max_length=200)

class ConflictForm(forms.Form):
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
    description = forms.CharField(label='Description', max_length=200)
    day_of_week = forms.ChoiceField(choices=DAY_OF_WEEK_CHOICES)
    start_time = forms.TimeField(label='Conflict Start Time')
    end_time = forms.TimeField(label='Conflict End Time')
