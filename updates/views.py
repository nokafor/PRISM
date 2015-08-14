# from django.core.files import File

from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse

from companies.models import Company, Member, Admin, Rehearsal, Cast, Choreographer, TimeBlock
from profiles.models import Conflict
# from updates.forms import ConflictForm, RehearsalForm, CastForm, MemberForm, MemberNameForm, ChoreographerForm
from updates.forms import RehearsalForm, ConflictForm

from django.views.generic import DetailView
from django.template.loader import render_to_string

from profiles.functions import memberAuth, adminAuth

from django.contrib.auth.models import Group, User

from datetime import datetime
import time


# Create your views here.
class ConflictView(DetailView):
    model = Member
    template_name = 'updates/conflicts.html'

class RehearsalView(DetailView):
    model = Cast
    template_name = 'updates/availableRehearsals.html'

class CastView(DetailView):
    model = Rehearsal
    template_name = 'updates/available.html'

def addCast(request, company_name, member_name):
    name = 'updates:addCast'

    # check if valid admin
    not_valid_admin = adminAuth(request, company_name, member_name)
    if not_valid_admin:
        return not_valid_admin
    else:
        company = Company.objects.get(name=company_name)
        member = company.member_set.get(username=member_name)

        new_cast = Cast(company=company)

        # save casting data
        if request.method == 'POST':
            form = CastForm(request.POST, instance=new_cast)
            if form.is_valid():
                form.save()

                return redirect('profiles:casts', company_name, member_name,)
        else:
            form = CastForm(instance=new_cast)
        return render(request, 'updates/add.html', {'company':company, 'member':member, 'form':form, 'redirect_name':name})

def updateCastName(request, company_name, member_name, cast_id):
    name = 'updates:updateCastName'

    # check if valid admin
    not_valid_admin = adminAuth(request, company_name, member_name)
    if not_valid_admin:
        return not_valid_admin
    else:
        company = Company.objects.get(name=company_name)
        member = company.member_set.get(username=member_name)
        cast = Cast.objects.get(id=cast_id)

        # save casting data
        if request.method == 'POST':
            form = CastForm(request.POST, instance=cast)
            if form.is_valid():
                form.save()

                return redirect('profiles:casts', company_name, member_name,)
        else:
            form = CastForm(instance=cast)
        return render(request, 'updates/update.html', {'company':company, 'member':member, 'curr':cast, 'form':form, 'redirect_name':name})

def addChoreographer(request, company_name, member_name, cast_id):
    name = 'updates:addChoreographer'

    # check if valid admin
    not_valid_admin = adminAuth(request, company_name, member_name)
    if not_valid_admin:
        return not_valid_admin
    else:
        company = Company.objects.get(name=company_name)
        member = company.member_set.get(username=member_name)
        cast = Cast.objects.get(id=cast_id)

        new_choreographer = Choreographer(company=company, cast=cast)

        # save choreographer data
        if request.method == 'POST':
            form = ChoreographerForm(request.POST, instance=new_choreographer)
            if form.is_valid():
                form.save()

                return redirect('profiles:casts', company_name, member_name,)
        else:
            form = ChoreographerForm(instance=new_choreographer)
        return render(request, 'updates/update.html', {'company':company, 'member':member, 'curr':cast, 'form':form, 'redirect_name':name})

def updateChoreographer(request, company_name, member_name, choreographer_id):
    name = 'updates:updateChoreographer'

    # check if valid admin
    not_valid_admin = adminAuth(request, company_name, member_name)
    if not_valid_admin:
        return not_valid_admin
    else:
        company = Company.objects.get(name=company_name)
        member = company.member_set.get(username=member_name)
        
        choreographer = Choreographer.objects.get(id=choreographer_id)

        # save choreographer data
        if request.method == 'POST':
            form = ChoreographerForm(request.POST, instance=choreographer)
            if form.is_valid():
                form.save()

                return redirect('profiles:casts', company_name, member_name,)
        else:
            form = ChoreographerForm(instance=choreographer)
        return render(request, 'updates/updateChoreographer.html', {'company':company, 'member':member, 'curr':choreographer, 'form':form, 'redirect_name':name})


def addCastMem(request, company_name, member_name, cast_id):
    name = 'updates:addCastMem'

    # check if valid admin
    not_valid_admin = adminAuth(request, company_name, member_name)
    if not_valid_admin:
        return not_valid_admin
    else:
        company = Company.objects.get(name=company_name)
        member = company.member_set.get(username=member_name)
        cast = Cast.objects.get(id=cast_id)

        new_choreographer = Choreographer(company=company, cast=cast)

        # save casting data
        if request.method == 'POST':
            form = ChoreographerForm(request.POST, instance=new_choreographer)
            if form.is_valid():
                false_choreographer = form.save(commit=False)
                cast.member_set.add(false_choreographer.member)

                return redirect('profiles:casts', company_name, member_name,)
        else:
            form = ChoreographerForm(instance=new_choreographer)
        return render(request, 'updates/update.html', {'company':company, 'member':member, 'curr':cast, 'form':form, 'redirect_name':name})

def updateCastMem(request, company_name, member_name, cast_id, mem_id):
    # check if valid admin
    not_valid_admin = adminAuth(request, company_name, member_name)
    if not_valid_admin:
        return not_valid_admin
    else:
        company = Company.objects.get(name=company_name)
        member = company.member_set.get(username=member_name)

        cast = Cast.objects.get(id=cast_id)
        mem = Member.objects.get(id=mem_id)

        return render(request, 'updates/updateCastMem.html', {'company':company, 'member':member, 'cast':cast, 'mem':mem})

def deleteCastMem(request, company_name, member_name, cast_id, mem_id):
    # check if valid admin
    not_valid_admin = adminAuth(request, company_name, member_name)
    if not_valid_admin:
        return not_valid_admin
    else:
        cast = Cast.objects.get(id=cast_id)
        mem = Member.objects.get(id=mem_id)
        # mem = cast.member_set.get(id=mem_id)
        cast.member_set.remove(mem)

        return redirect('profiles:casts', company_name, member_name,)

def addAdmin(request, company_name, member_name, member_id):
    # check if valid admin
    admin = adminAuth(request, company_name, member_name)
    if admin:
        company = Company.objects.get(name=company_name)
        member = Member.objects.get(username=member_name)
        
        # get post data if available
        mem = Member.objects.get(id=member_id)

        if not Admin.objects.filter(member=mem, company=company).exists():
            new_admin = Admin(member=mem, company=company)
            new_admin.save()

        return redirect('profiles:members', company_name, member_name,)

    else:
        return HttpResponse('You do not have access to this page')
        

def addStudents(request, company_name, member_name):
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
                    if email[1].lower() != 'princeton.edu':
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

    else:
        return HttpResponse('You do not have access to this page')

def deleteMember(request, company_name, member_name, member_id):
    # check if valid admin
    admin = adminAuth(request, company_name, member_name)
    if admin:
        if Member.objects.filter(id=member_id).exists():
            old_member = Member.objects.get(id=member_id)

            # make sure you can only delete people who are in your company
            if old_member.groups.filter(name=company_name).exists() and admin.member != old_member:
                # delete any admin models associated with this organization
                if Admin.objects.filter(member=old_member, company__name=company_name).exists():
                    old_admin = Admin.objects.get(member=old_member, company__name=company_name)
                    old_admin.delete()

                # delete person from company set
                company = Company.objects.get(name='BAC')
                company.user_set.remove(old_member)

                # if user is a student and is no longer associated with any companies, remove them from system to clear space
                if not old_member.has_usable_password() and old_member.groups.all().count() == 0:
                    old_member.delete()

        return redirect('profiles:members', company_name, member_name,)

    else:
        return HttpResponse('You do not have access to this page')

        

def deleteCast(request, company_name, member_name, cast_id):
    # check if valid admin
    not_valid_admin = adminAuth(request, company_name, member_name)
    if not_valid_admin:
        return not_valid_admin
    else:
        cast = Cast.objects.get(id=cast_id)
        cast.delete()

        return redirect('profiles:casts', company_name, member_name,)

def deleteChoreographer(request, company_name, member_name, choreographer_id):
    # check if valid admin
    not_valid_admin = adminAuth(request, company_name, member_name)
    if not_valid_admin:
        return not_valid_admin
    else:
        choreographer = Choreographer.objects.get(id=choreographer_id)
        choreographer.delete()

        return redirect('profiles:casts', company_name, member_name,)

def deleteAdmin(request, company_name, member_name):
    # check if valid admin
    admin = adminAuth(request, company_name, member_name)
    if admin:
        admin.delete()

        return redirect('profiles:profile', company_name, member_name,)
    else:
        return HttpResponse('You do not have access to this page')

def updateName(request, company_name, member_name):
    # make sure member has access to this profile
    member = memberAuth(request, company_name, member_name)

    if member:
        company = Company.objects.get(name=company_name)

        # process the form and update user's name
        if request.method == 'POST':
            form = MemberNameForm(request.POST, instance=member)
            if form.is_valid():
                form.save()

                return redirect('profiles:profile', company_name, member_name,)
        else:
            form = MemberNameForm(instance=member)
        
        if member.first_name:
            header = 'Edit Name'
            return render(request, 'profiles/name.html', {'company':company, 'member':member, 'form':form, 'dismiss':"modal", 'header':header})
        else:
            header = 'Enter Name Before Continuing'
            return render(request, 'profiles/name.html', {'company':company, 'member':member, 'form':form, 'dismiss':"", 'header':header})

    else:
        return redirect('profiles:profile', company_name, member_name,)

def addConflicts(request, company_name, member_name):
    member = memberAuth(request, company_name, member_name)
    if member:
        company = Company.objects.get(name=company_name)

        if request.method == 'POST':
            conflicts = request.POST['conflicts']
            conflicts = [l for l in conflicts.split("\n") if l]
            print conflicts

            # initialize error message for any processing errors
            error_message = "The following lines could not be processed:"

            for line in conflicts:
                info = line.split()
                print info

                # make sure line is specified length
                if len(info) != 4:
                    error_message += "\n" + line + " (Each line should have exactly 4 words)"
                    continue

                # check start time
                try:
                    start = datetime.strptime(info[2], "%I:%M%p")
                    print start.time()

                    end = datetime.strptime(info[3], "%I:%M%p")
                    print end.time()
                except ValueError:
                    error_message += "\n" + line + " (Does not contain valid time parameters)"
                    continue

                # get day of week information
                dow = time.strptime(info[1], "%A").tm_wday

                conflict = Conflict(member=member, description=info[0], day_of_week=TimeBlock.DAY_OF_WEEK_CHOICES[dow][0], start_time=start.time(), end_time=end.time())
                conflict.save()
                # print rehearsal

            print error_message
        return redirect('profiles:conflicts', company_name=company_name, member_name=member_name)
    else:
        return HttpResponse('You do not have access to this page')

def updateConflict(request, company_name, member_name, conflict_id):
    name = 'updates:updateConflict'
    
    # check if valid member
    member = memberAuth(request, company_name, member_name)
    if member:
        company = Company.objects.get(name=company_name)
        
        if member.conflict_set.filter(id=conflict_id).exists():
            conflict = member.conflict_set.get(id=conflict_id)
                    
            # process the form and rehearsal data
            if request.method == 'POST':
                form = ConflictForm(request.POST, instance=conflict)
                if form.is_valid():
                    form.save()

                    return redirect('profiles:conflicts', company_name, member_name,)
            else:
                form = ConflictForm(instance=conflict)
            return render(request, 'updates/update.html', {'company':company, 'member':member, 'curr':conflict, 'form':form, 'redirect_name':name})
        return redirect('profiles:conflicts', company_name, member_name,)
    else:
        return HttpResponse('You do not have access to this page')

def deleteConflict(request, company_name, member_name, conflict_id):
    # check if came from profile
    member = memberAuth(request, company_name, member_name)
    if member:
        company = Company.objects.get(name=company_name)

        if member.conflict_set.filter(id=conflict_id).exists():
            conflict = member.conflict_set.get(id=conflict_id)
            conflict.delete()

        return redirect('profiles:conflicts', company_name, member_name,)
    else:
        return HttpResponse('You do not have access to this page')

def addRehearsals(request, company_name, member_name):
    admin = adminAuth(request, company_name, member_name)
    if admin:
        company = Company.objects.get(name=company_name)

        if request.method == 'POST':
            rehearsals = request.POST['rehearsals']
            rehearsals = [l for l in rehearsals.split("\n") if l]
            print rehearsals

            # initialize error message for any processing errors
            error_message = "The following lines could not be processed:"

            for line in rehearsals:
                info = line.split()
                print info

                # make sure line is specified length
                if len(info) != 4:
                    error_message += "\n" + line + " (Each line should have exactly 4 words)"
                    continue

                # check start time
                try:
                    start = datetime.strptime(info[2], "%I:%M%p")
                    print start.time()

                    end = datetime.strptime(info[3], "%I:%M%p")
                    print end.time()
                except ValueError:
                    error_message += "\n" + line + " (Does not contain valid time parameters)"
                    continue

                # get day of week information
                dow = time.strptime(info[1], "%A").tm_wday

                rehearsal = Rehearsal(company=company, place=info[0], day_of_week=TimeBlock.DAY_OF_WEEK_CHOICES[dow][0], start_time=start.time(), end_time=end.time())
                rehearsal.save()
                # print rehearsal

            print error_message
        return redirect('profiles:spaces', company_name=company_name, member_name=member_name)
    else:
        return HttpResponse('You do not have access to this page')

def updateRehearsal(request, company_name, member_name, rehearsal_id):
    name = 'updates:updateRehearsal'
    
    # check if valid admin
    admin = adminAuth(request, company_name, member_name)
    if admin:
        company = Company.objects.get(name=company_name)
        member = admin.member
        
        if company.rehearsal_set.get(id=rehearsal_id).exists():
            rehearsal = company.rehearsal_set.get(id=rehearsal_id)
                    
            # process the form and rehearsal data
            if request.method == 'POST':
                form = RehearsalForm(request.POST, instance=rehearsal)
                if form.is_valid():
                    form.save()

                    return redirect('profiles:spaces', company_name, member_name,)
            else:
                form = RehearsalForm(instance=rehearsal)
            return render(request, 'updates/update.html', {'company':company, 'member':member, 'curr':rehearsal, 'form':form, 'redirect_name':name})
        return redirect('profiles:spaces', company_name, member_name,)
    else:
        return HttpResponse('You do not have access to this page')

def deleteRehearsal(request, company_name, member_name, rehearsal_id):
    # check if valid admin
    admin = adminAuth(request, company_name, member_name)
    if admin:
        company = Company.objects.get(name=company_name)

        if company.rehearsal_set.filter(id=rehearsal_id).exists():
            rehearsal = company.rehearsal_set.get(id=rehearsal_id)
            rehearsal.delete()

        return redirect('profiles:spaces', company_name, member_name,)
    else:
        return HttpResponse('You do not have access to this page')
