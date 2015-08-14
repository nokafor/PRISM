from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect

from companies.models import Company, Member, Admin, Rehearsal, Cast, Choreographer, TimeBlock
from updates.forms import MemberNameForm, UserForm

from profiles.functions import memberAuth, adminAuth
from django.contrib.auth.models import User, Group

from datetime import datetime
from django.utils import timezone

# Create your views here.
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
        # admin = adminAuth(request, company_name, member_name)

        conflict_list = {}
        for conflict in member.conflict_set.all():
            try:
                conflict_list[conflict.day_of_week].append(conflict)
            except KeyError:
                conflict_list[conflict.day_of_week] = []
                conflict_list[conflict.day_of_week].append(conflict)

        return render(request, 'profiles/conflicts.html', {'company':company, 'member':member, 'conflict_list':conflict_list, 'timeblock':TimeBlock})

    else:
        return HttpResponse('Hello____, You do not have access to this page. Please log into the appropriate company, or sign out here.')                  

def casts(request, company_name, member_name):
    # check if valid admin
    not_valid_admin = adminAuth(request, company_name, member_name)

    company = Company.objects.get(name=company_name)
    member = company.member_set.get(username=member_name)

    total_casts = Cast.objects.filter(company=company)
    total_choreographers = Choreographer.objects.filter(company=company)

    if not_valid_admin:
        not_valid_member = memberAuth(request, company_name, member_name)
        if not_valid_member:
            return not_valid_member
        else:
            return render(request, 'profiles/viewcasts.html', {'company':company, 'member':member, 'total_casts':total_casts, 'total_choreographers':total_choreographers})
    else:
        return render(request, 'profiles/casts.html', {'company':company, 'member':member, 'total_casts':total_casts, 'total_choreographers':total_choreographers})

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
