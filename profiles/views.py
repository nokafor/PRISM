from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect

from companies.models import Company, Member, Admin, Rehearsal, Cast, Choreographer, TimeBlock
from updates.forms import MemberNameForm, TestForm

from profiles.functions import memberAuth, adminAuth
from django.contrib.auth.models import User, Group

from datetime import datetime
from django.utils import timezone

# Create your views here.
def testing(request, company_name, member_name):
    # create dataset for users (w/o valid netid)
    # dataset = []
    # results = User.objects.filter(groups__isnull=True).exclude(username='admin')
    # for user in results:
    #     dataset.append("%s %s (%s)" % (user.first_name, user.last_name, user.email))
    # print dataset
    admin = adminAuth(request, company_name, member_name)

    if admin:

        company = Company.objects.get(name=company_name)

        if request.method == 'POST':
            # check if there are any 'students' being inputted
            student_list = request.POST['student_list']
            student_list = [l for l in student_list.split("\n") if l]

            # initialize error message for any processing errors
            error_message = "The following lines could not be processed:"

            for line in student_list:
                info = line.split()

                # make sure line is specified length
                if len(info) != 3:
                    error_message += "\n" + line + " (Each line should have exactly 3 words)"
                    continue

                # check to see if you have email or username
                if '@' in info[0]:
                    email = info[0].split('@')
                    if email[1] != 'princeton.edu':
                        # print line
                        error_message += "\n" + line + " (First word in line must be a NetID or a valid Princeton email address)"
                        continue
                    username = email[0]
                else:
                    username = info[0]

                print username, info[1], info[2]

                # check if the member already exists
                if Member.objects.filter(username=username).exists():
                    member = Member.objects.get(username=username)
                    # if there is a  member with the same username in this group
                    if member.groups.filter(name=company_name).exists():
                        # check if student
                        if not member.has_usable_password():
                            error_message += "\n" + line + " (There is already a member of this company with this username)"
                            continue
                        # if not student
                        # else:
                            # change the 'nonstudents' username
                    
                    # if member is not a part of this group
                    else:
                        # add them to this company
                        member.groups.add(company)
                        member.save()
                        continue

                # add the member to the company
                mem = Member(username=username, first_name=info[1], last_name=info[2], email="%s@princeton.edu" % username)
                mem.set_unusable_password()
                mem.save()
                mem.groups.add(company)

            if "\n" in error_message:
                print error_message
            return redirect('profiles:members', company_name=company_name, member_name=member_name)

        form = TestForm()
        return render(request, 'profiles/test.html', {'form':form, 'company_name': company_name, 'member_name':member_name})
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

def conflicts(request, company_name, member_name):
    member = memberAuth(request, company_name, member_name)

    if member:
        company = Company.objects.get(name=company_name)
        admin = adminAuth(request, company_name, member_name)

        conflict_list = member.conflict_set.all()

        return render(request, 'profiles/addconflict.html', {'company':company, 'member':member, 'conflicts':conflict_list, 'timeblock':TimeBlock})

    else:
        return HttpResponse('Hello____, You do not have access to this page. Please log into the appropriate company, or sign out here.')          

def spaces(request, company_name, member_name):
    member = memberAuth(request, company_name, member_name)

    if member:
        company = Company.objects.get(name=company_name)
        admin = adminAuth(request, company_name, member_name)

        rehearsal_list = company.rehearsal_set.all()

        return render(request, 'profiles/addspace.html', {'company':company, 'member':member, 'rehearsals':rehearsal_list, 'timeblock':TimeBlock})

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
