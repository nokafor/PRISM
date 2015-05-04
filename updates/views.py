from django.core.files import File

from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse

from companies.models import Company, Member, Admin, Rehearsal, Cast, Choreographer
from updates.forms import ConflictForm, RehearsalForm, CastForm, MemberForm, AdminForm, ChoreographerForm

from django.views.generic import DetailView
from django.template.loader import render_to_string

from profiles.functions import memberAuth, profileAuth, adminAuth

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
        member = company.member_set.get(netid=member_name)

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
        member = company.member_set.get(netid=member_name)
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
        member = company.member_set.get(netid=member_name)
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
        member = company.member_set.get(netid=member_name)
        
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
        member = company.member_set.get(netid=member_name)
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
        member = company.member_set.get(netid=member_name)

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

def addAdmin(request, company_name, member_name):
    name = 'updates:addAdmin'

    # check if valid admin
    not_valid_admin = adminAuth(request, company_name, member_name)
    if not_valid_admin:
        return not_valid_admin
    else:
        company = Company.objects.get(name=company_name)
        member = company.member_set.get(netid=member_name)

        admin = Admin(company=company)

        # process the form and add new admin
        if request.method == 'POST':
            form = AdminForm(request.POST, instance=admin)
            if form.is_valid():
                form.save()

                return redirect('profiles:members', company_name, member_name,)
        else:
            form = AdminForm(instance=admin)
        return render(request, 'updates/add.html', {'company':company, 'member':member, 'form':form, 'redirect_name':name})

    # check if valid admin
def addMember(request, company_name, member_name):
    name = 'updates:addMember'
    
    # check if valid admin
    not_valid_admin = adminAuth(request, company_name, member_name)
    if not_valid_admin:
        return not_valid_admin
    else:
        company = Company.objects.get(name=company_name)
        member = company.member_set.get(netid=member_name)

        # process the form and add new member
        if request.method == 'POST':
            form = MemberForm(request.POST)
            if form.is_valid():
                new_member = form.save()
                company.member_set.add(new_member)

                return redirect('profiles:members', company_name, member_name,)
        else:
            form = MemberForm()
        return render(request, 'updates/add.html', {'company':company, 'member':member, 'form':form, 'redirect_name':name})

def deleteMember(request, company_name, member_name, member_id):
    # check if valid admin
    not_valid_admin = adminAuth(request, company_name, member_name)
    if not_valid_admin:
        return not_valid_admin
    else:
        company = Company.objects.get(name=company_name)
        member = company.member_set.get(netid=member_name)

        old_member = company.member_set.get(id=member_id)

        if member == old_member:
            pass
        else:
            old_member.delete()

        return redirect('profiles:members', company_name, member_name,)

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
    not_valid_admin = adminAuth(request, company_name, member_name)
    if not_valid_admin:
        return not_valid_admin
    else:
        admin = Admin.objects.get(member=member)
        admin.delete()

        return redirect('profiles:profile', company_name, member_name,)

def updateName(request, company_name, member_name):
    # check if came from profile
    not_from_profile = profileAuth(request, company_name, member_name)
    if not_from_profile:
        return not_from_profile
    else:
        company = Company.objects.get(name=company_name)
        member = company.member_set.get(netid=member_name) 

        # process the form and update user's name
        if request.method == 'POST':
            form = MemberForm(request.POST, instance=member)
            if form.is_valid():
                form.save()

                return redirect('profiles:profile', company_name, member_name,)
        else:
            form = MemberForm(instance=member)
        return render(request, 'profiles/name.html', {'company':company, 'member':member, 'form':form})

def addConflict(request, company_name, member_name):
    name = 'updates:addConflict'

    # check if came from profile
    not_from_profile = profileAuth(request, company_name, member_name)
    if not_from_profile:
        return not_from_profile
    else:
        company = Company.objects.get(name=company_name)
        member = company.member_set.get(netid=member_name) 
        
        # process the form and conflict data of the user
        if request.method == 'POST':
            form = ConflictForm(request.POST)
            if form.is_valid():
                new_conflict = form.save(commit=False)
                new_conflict.member = member
                new_conflict.save()
                form.save_m2m()

                return redirect('profiles:conflicts', company_name, member_name,)
        else:
            form = ConflictForm()
        return render(request, 'updates/add.html', {'company':company, 'member':member, 'form':form, 'redirect_name':name})


def updateConflict(request, company_name, member_name, conflict_id):
    name = 'updates:updateConflict'
    
    # check if came from profile
    not_from_profile = profileAuth(request, company_name, member_name)
    if not_from_profile:
        return not_from_profile
    else:
        company = Company.objects.get(name=company_name)
        member = company.member_set.get(netid=member_name)

        conflict = member.conflict_set.get(id=conflict_id)

        # process the form and conflict data of the user
        if request.method == 'POST':
            form = ConflictForm(request.POST, instance=conflict)
            if form.is_valid():
                form.save()

                return redirect('profiles:conflicts', company_name, member_name,)
        else:
            form = ConflictForm(instance=conflict)
        return render(request, 'updates/update.html', {'company':company, 'member':member, 'curr':conflict, 'form':form, 'redirect_name':name})

def deleteConflict(request, company_name, member_name, conflict_id):
    # check if came from profile
    not_from_profile = profileAuth(request, company_name, member_name)
    if not_from_profile:
        return not_from_profile
    else:
        company = Company.objects.get(name=company_name)
        member = company.member_set.get(netid=member_name)

        conflict = member.conflict_set.get(id=conflict_id)
        conflict.delete()

        return redirect('profiles:conflicts', company_name, member_name,)

def addRehearsal(request, company_name, member_name):
    name = 'updates:addRehearsal'
    
    # check if valid admin
    not_valid_admin = adminAuth(request, company_name, member_name)
    if not_valid_admin:
        return not_valid_admin
    else:
        company = Company.objects.get(name=company_name)
        member = company.member_set.get(netid=member_name)

        # process the form and rehearsal data
        if request.method == 'POST':
            form = RehearsalForm(request.POST)
            if form.is_valid():
                new_rehearsal = form.save(commit=False)
                new_rehearsal.company = company
                new_rehearsal.save()
                form.save_m2m()

                return redirect('profiles:spaces', company_name, member_name,)
        else:
            form = RehearsalForm()
        return render(request, 'updates/add.html', {'company':company, 'member':member, 'form':form, 'redirect_name':name})

def updateRehearsal(request, company_name, member_name, rehearsal_id):
    name = 'updates:updateRehearsal'
    
    # check if valid admin
    not_valid_admin = adminAuth(request, company_name, member_name)
    if not_valid_admin:
        return not_valid_admin
    else:
        company = Company.objects.get(name=company_name)
        member = company.member_set.get(netid=member_name)
        
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

def deleteRehearsal(request, company_name, member_name, rehearsal_id):
    # check if valid admin
    not_valid_admin = adminAuth(request, company_name, member_name)
    if not_valid_admin:
        return not_valid_admin
    else:
        company = Company.objects.get(name=company_name)
        member = company.member_set.get(netid=member_name)

        rehearsal = company.rehearsal_set.get(id=rehearsal_id)
        rehearsal.delete()

        return redirect('profiles:spaces', company_name, member_name,)
