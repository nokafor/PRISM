from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect

from companies.models import Company, Member, Admin, Rehearsal, Cast, Choreographer, TimeBlock, Founder
from profiles.models import Conflict
from updates.forms import MemberNameForm, UserForm

from profiles.functions import memberAuth, adminAuth
from django.contrib.auth.models import User, Group

from datetime import datetime, timedelta
from django.utils import timezone

# Create your views here.
def testing(request, company_name, member_name, date_string):
    member = memberAuth(request, company_name, member_name)
    if member:
        if request.method == 'POST':
            #
            description = request.POST['description']
            day_of_week = request.POST['dow']

            start = request.POST['startOptions'].split(", ")[2].replace(".", "")
            if ':' not in start:
                start = start.replace(" ", ":00 ")
            start_time = datetime.strptime(start, "%I:%M %p")
            # print start, start_time

            end = request.POST['endOptions'].split(", ")[2].replace(".", "")
            if ':' not in end:
                end = end.replace(" ", ":00 ")
            
            end_time = datetime.strptime(end, "%I:%M %p")

            conflict = Conflict(member=member, description=description, day_of_week=day_of_week, start_time=start_time.time(), end_time=end_time.time())
            conflict.save()

            # print description, day_of_week
            return redirect('profiles:conflicts', company_name, member_name,)
        else:
            event = date_string.replace("%20", " ").split('-')
            try:
                start_time1 = datetime.fromtimestamp(float(event[2])/1000.0) - timedelta(minutes=float(event[3]))
                start_time2 = datetime.fromtimestamp(float(event[2])/1000.0) + timedelta(minutes=float(event[3]))
                end_time1 = datetime.fromtimestamp(float(event[4])/1000.0) - timedelta(minutes=float(event[5]))
                end_time2 = datetime.fromtimestamp(float(event[4])/1000.0) + timedelta(minutes=float(event[5]))
                # print day_of_week, start_time, end_time

                return render(request, 'profiles/testing.html', {'company_name':company_name, 'member_name':member_name, 'start_time1':start_time1, 'start_time2':start_time2, 'end_time1':end_time1, 'end_time2':end_time2, 'dow':event[1], 'description':event[0]})
            except:
                return HttpResponse("Could not process your request")
    else:
        HttpResponse('Hello____, You do not have access to this page. Please log into the appropriate company, or sign out here.')        

def addUsers(request, company_name, member_name):
    # create dataset for users (w/o valid netid)
    # dataset = []
    # results = User.objects.filter(groups__isnull=True).exclude(username='admin')
    # for user in results:
    #     dataset.append("%s %s (%s)" % (user.first_name, user.last_name, user.email))
    # print dataset
    admin = adminAuth(request, company_name, member_name)

    if admin:
        company = Company.objects.get(name=company_name)

        # get any users w/o valid netids that are being added
        if request.method == 'POST':
            form = UserForm(request.POST)

            if form.is_valid():
                members = form.cleaned_data['users']

                for member in members:
                    member.groups.add(company)
                    member.save()

            return redirect('profiles:members', company_name=company_name, member_name=member_name)

        form = UserForm()
        return render(request, 'profiles/addmembers.html', {'form':form, 'company_name': company_name, 'member_name':member_name})
    else:
        HttpResponse('Hello____, You do not have access to this page. Please log into the appropriate company, or sign out here.')

def updateConflictsDue(request, company_name, member_name):
    # make sure member is an admin and has the right to access this information
    admin = adminAuth(request, company_name, member_name)

    if admin:
        # save posted data if available
        if request.method == 'POST':
            try: 
                valid_datetime = datetime.strptime(request.POST['datetimepicker4'], '%m/%d/%Y %I:%M %p')
                company = Company.objects.get(name=company_name)
                company.conflicts_due = valid_datetime.replace(tzinfo=timezone.LocalTimezone())
                company.save()
                return redirect('profiles:profile', company_name=company_name, member_name=member_name)
            except ValueError:
                return HttpResponse('You did not enter a valid date and time. So the information was not saved.')

        return render(request, 'profiles/datetimepicker.html', {'company_name':company_name, 'member_name':member_name})

    # admins and members logged in under the wrong name cannot access this page
    return HttpResponse('Hello____, You do not have access to this page. Please log into the appropriate company, or sign out here.')

    

def profile(request, company_name, member_name):
    # make sure member has access to this profile
    member = memberAuth(request, company_name, member_name)
    admin = adminAuth(request, company_name, member_name)

    if member:
        company = Company.objects.get(name=company_name)

        # process the form and conflict data of the user
        if request.method == 'POST':
            form = MemberNameForm(request.POST, instance=member)
            if form.is_valid():
                form.save()

                return redirect('profiles:profile', company_name, member_name,)
        else:
            form = MemberNameForm(instance=member)

        return render(request, 'profiles/hub.html', {'member':member, 'company':company, 'form':form, 'admin':admin})

    else:
        return HttpResponse('Hello____, You do not have access to this page. Please log into the appropriate company, or sign out here.')

def members(request, company_name, member_name):
    # make sure member has access to this profile
    member = memberAuth(request, company_name, member_name)

    if member:
        company = Company.objects.get(name=company_name)
        member_list = company.user_set.all()
        admin_list = company.admin_set.all()

        admin = adminAuth(request, company_name, member_name)

        return render(request, 'profiles/members.html', {'company':company, 'member':member, 'member_list':member_list, 'admin_list':admin_list, 'admin':admin})

    else:
        return HttpResponse('Hello____, You do not have access to this page. Please log into the appropriate company, or sign out here.')

def spaces(request, company_name, member_name):
    member = memberAuth(request, company_name, member_name)

    if member:
        company = Company.objects.get(name=company_name)
        admin = adminAuth(request, company_name, member_name)

        rehearsal_list = {}

        for rehearsal in company.rehearsal_set.all():
            try:
                rehearsal_list[rehearsal.day_of_week].append(rehearsal)
            except KeyError:
                rehearsal_list[rehearsal.day_of_week] = []
                rehearsal_list[rehearsal.day_of_week].append(rehearsal)
        # print rehearsal_list

        # events = [{
        #     'title' : '%s' % rehearsal.place,
        #     'start' : 'moment("%s", "hh:mm a").day("%s"),' % (rehearsal.start_time, rehearsal.day_of_week),
        #     'allDay': 'false'
        # }]

        print rehearsal_list

        return render(request, 'profiles/spaces.html', {'company':company, 'member':member, 'rehearsal_list':rehearsal_list, 'admin':admin})

    else:
        return HttpResponse('Hello____, You do not have access to this page. Please log into the appropriate company, or sign out here.')  

def conflicts(request, company_name, member_name):
    member = memberAuth(request, company_name, member_name)

    if member:
        company = Company.objects.get(name=company_name)
        founder = Founder.objects.get(id=1)

        # admin = adminAuth(request, company_name, member_name)

        conflict_list = {}
        for conflict in member.conflict_set.all():
            try:
                conflict_list[conflict.day_of_week].append(conflict)
            except KeyError:
                conflict_list[conflict.day_of_week] = []
                conflict_list[conflict.day_of_week].append(conflict)

        return render(request, 'profiles/conflicts.html', {'company':company, 'member':member, 'conflict_list':conflict_list, 'timeblock':TimeBlock, 'founder':founder})

    else:
        return HttpResponse('Hello____, You do not have access to this page. Please log into the appropriate company, or sign out here.')                  

def casts(request, company_name, member_name):
    member = memberAuth(request, company_name, member_name)

    if member:
        company = Company.objects.get(name=company_name)
        admin = adminAuth(request, company_name, member_name)

        cast_list = Cast.objects.filter(company=company)
        total_choreographers = Choreographer.objects.filter(company=company)
        return render(request, 'profiles/casts.html', {'company':company, 'member':member, 'admin':admin, 'cast_list':cast_list, 'total_choreographers':total_choreographers})
    else:
        return HttpResponse('Hello____, You do not have access to this page. Please log into the appropriate company, or sign out here.')                  

def scheduling(request, company_name, member_name):
    # check if valid admin
    not_valid_admin = adminAuth(request, company_name, member_name)
    if not_valid_admin:
        return not_valid_admin
    else:
        company = Company.objects.get(name=company_name)
        member = company.member_set.get(username=member_name)
        rehearsals = company.getSortedRehearsals()

        casts = Cast.objects.filter(company=company)

        return render(request, 'profiles/schedule.html', {'company':company, 'member':member, 'cast_list':casts, 'rehearsal_list':rehearsals})
