from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.http import HttpResponse, HttpResponseRedirect

from companies.models import Company, Member, Admin
from profiles.models import ConflictForm, RehearsalTime, RehearsalForm
from profiles.forms import NameForm

# Create your views here.
@login_required
def profile(request, company_name, member_name):
    if member_name == request.user.username:
        company = get_object_or_404(Company, name=company_name)
        try:
            member = company.member_set.get(netid=request.user.username)
        # if you are not a member...
        except (KeyError, Member.DoesNotExist):
            logout(request)
            return HttpResponse("You are not a member of the company you are trying to log in to. Please log into a correct company.")
        # if you are a member ...
        else:
            # if you have already entered your first and last name ...
            if member.first_name and member.last_name:
                try:
                    admin = Admin.objects.get(member=member)
                except (KeyError, Admin.DoesNotExist):
                    return render(request, 'profiles/dancer.html', {'member':member, 'company':company})
                else:
                    return render(request, 'profiles/admin.html', {'member':member, 'company':company})
            # if you need to enter your information ...
            else:
                # process the form data
                if request.method == 'POST':
                    form = NameForm(request.POST)
                    if form.is_valid():
                        # process form.cleaned_data
                        member.first_name = form.cleaned_data['first_name']
                        member.last_name = form.cleaned_data['last_name']
                        member.save()
                        # refresh the page
                        return HttpResponseRedirect('')
                # get the form data
                else:
                    form = NameForm()
                return render(request, 'profiles/name.html', {'form':form})
    else:
        logout(request)
        return HttpResponse("You are trying to access the profile of...")

def conflicts(request, company_name, member_name):
    company = get_object_or_404(Company, name=company_name)

    # user must come from profile page to get here... don't need to reauthenticate
    if request.user.is_authenticated() and member_name == request.user.username:
        try:
            member = company.member_set.get(netid=member_name)
        except (KeyError, Member.DoesNotExist):
            return redirect('profiles:profile', company_name, member_name,)
        else:
            conflict_list = member.conflict_set.all()

            # process the form and conflict data of the user
            if request.method == 'POST':
                form = ConflictForm(request.POST)
                if form.is_valid():
                    new_conflict = form.save(commit=False)
                    new_conflict.member = member
                    new_conflict.save()
                    form.save_m2m()

                    return HttpResponseRedirect('')
            else:
                form = ConflictForm()
            return render(request, 'profiles/addconflict.html', {'company':company, 'member':member, 'conflict_list':conflict_list, 'form':form})
    else:
        return redirect('profiles:profile', company_name, member_name,)

def spaces(request, company_name, member_name):
    company = get_object_or_404(Company, name=company_name)

    # user must come from profile page to get here... don't need to reauthenticate
    if request.user.is_authenticated() and member_name == request.user.username:
        try:
            member = company.member_set.get(netid=member_name)
        except (KeyError, Member.DoesNotExist):
            return redirect('profiles:profile', company_name, member_name,)
        else:
            try:
                admin = Admin.objects.get(member=member)
            except (KeyError, Admin.DoesNotExist):
                return redirect('profiles:profile', company_name, member_name,)
            else:
                rehearsal_list = company.rehearsaltime_set.all()

                # process the form and conflict data of the user
                if request.method == 'POST':
                    form = RehearsalForm(request.POST)
                    if form.is_valid():
                        new_rehearsal = form.save(commit=False)
                        new_rehearsal.company = company
                        new_rehearsal.save()
                        form.save_m2m()

                        return HttpResponseRedirect('')
                else:
                    form = RehearsalForm()
                return render(request, 'profiles/addspace.html', {'company':company, 'member':member, 'rehearsal_list':rehearsal_list, 'form':form})
    else:
        return redirect('profiles:profile', company_name, member_name,)

def members(request, company_name, member_name):
    company = get_object_or_404(Company, name=company_name)

    # user must come from profile page to get here... don't need to reauthenticate
    if request.user.is_authenticated() and member_name == request.user.username:
        try:
            member = company.member_set.get(netid=member_name)
        except (KeyError, Member.DoesNotExist):
            return redirect('profiles:profile', company_name, member_name,)
        else:
            try:
                admin = Admin.objects.get(member=member)
            except (KeyError, Admin.DoesNotExist):
                return redirect('profiles:profile', company_name, member_name,)
            else:
                member_list = company.member_set.all()
                admin_list = company.admin_set.all()

                return render(request, 'profiles/members.html', {'company':company, 'member':member, 'member_list':member_list, 'admin_list':admin_list})
    else:
        return redirect('profiles:profile', company_name, member_name,)
