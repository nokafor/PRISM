from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.http import HttpResponse

from companies.models import Company, Member, Admin

@login_required
def memberAuth(request, company_name, member_name):
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
            pass
    else:
        logout(request)
        return HttpResponse("You are trying to access the profile of...")

@login_required
def profileAuth(request, company_name, member_name):
    company = get_object_or_404(Company, name=company_name)

    # user must come from profile page to get here... don't need to reauthenticate
    if request.user.is_authenticated() and member_name == request.user.username:
        try:
            member = company.member_set.get(netid=member_name)
        except (KeyError, Member.DoesNotExist):
            return redirect('profiles:profile', company_name, member_name,)
        else:
            pass
    else:
        return redirect('profiles:profile', company_name, member_name,)

@login_required
def adminAuth(request, company_name, member_name):
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
                pass
    else:
        return redirect('profiles:profile', company_name, member_name,)
