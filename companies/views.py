from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect

from django.contrib.auth.models import Group, User
from companies.models import Company, Member, Admin

# Create your views here.
def index(request):
    group_list = Group.objects.all().order_by('name')
    return render(request, 'companies/index.html', {'group_list': group_list, 'user':request.user})

def modal(request, company_name):
    # company = Company.objects.get(name=company_name)
    # Since the template filters users logged into the company they are trying to access, if  the
    # user is logged in at this point, they are not part of the company
    if request.user.is_authenticated():
        return render(request, 'companies/otheruser.html', {'company_name': company_name, 'user':request.user})
    
    # If no user is logged in
    else:
        company = Company.objects.get(name=company_name)
        return render(request, 'companies/login.html', {'company':company})

@login_required
def detail(request, company_name):
    return redirect('%s/' % request.user.username)
    # company = Company.objects.get(name=company_name)
    # return render(request, 'companies/test.html', {'company':company})

def userLogin(request, company_name):
    # get post code from updates app
    company = Company.objects.get(name=company_name)
    return render(request, 'companies/test.html', {'company':company})

def logout_view(request):
    logout(request)
    return redirect('companies:index')

