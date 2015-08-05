from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.http import HttpResponse

from companies.models import Company, Member, Admin
from django.contrib.auth.models import User, Group

# Function to make sure user has access to the company and profile they are trying to access
def memberAuth(request, company_name, member_name):
    # make sure group exists
    company = get_object_or_404(Company, name=company_name)

    if request.user.is_authenticated() and member_name == request.user.username:
        # make sure user is a part of the group they are trying to access
        if request.user.groups.filter(name=company_name).exists():
            return Member.objects.get(username=member_name)
    return None

def adminAuth(request, company_name, member_name):
    company = get_object_or_404(Company, name=company_name)

    # if the user is authenticated, then the member exists in the system
    if request.user.is_authenticated() and member_name == request.user.username:
        if Admin.objects.filter(member__username=member_name, company=company).exists():
            return Admin.objects.get(member__username=member_name, company=company)
    
    return None


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
