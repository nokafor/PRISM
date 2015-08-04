from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect

from django.contrib.auth.models import Group, User
from companies.models import Founder, Company, Member, Admin

# Create your views here.
def index(request):
    group_list = Group.objects.all().order_by('name')
    founder = Founder.objects.get(id=1)
    return render(request, 'companies/index.html', {'group_list': group_list, 'user':request.user, 'founder':founder})

def signup(request):
    return render(request, 'companies/test.html')
    
def modal(request, company_name):
    # Since the template filters users logged into the company they are trying to access, if  the
    # user is logged in at this point, they are not part of the company
    if request.user.is_authenticated():
        return render(request, 'companies/otheruser.html', {'company_name': company_name, 'user':request.user})
    
    # If no user is logged in
    else:
        return render(request, 'companies/login.html', {'company_name':company_name})

@login_required
def detail(request, company_name):
    return redirect('%s/' % request.user.username)

def userLogin(request, company_name):
    # get POST data
    if request.method == 'POST':
        loginEmail = request.POST["loginEmail"]
        loginPwd = request.POST["loginPwd"]

        try:
            user = User.objects.get(email=loginEmail)
        except (KeyError, User.DoesNotExist):
            return HttpResponse('There is no user with that email')
        else:
            # if user password matches
            if user.check_password(loginPwd):
                # make sure account is active
                if user.is_active:
                    authUser = authenticate(username=user.username, password=loginPwd)
                    login(request, authUser)
                    # print "Login checkpoint."
                    return redirect('profiles:profile', company_name=company_name, member_name=user.username)
                # if account is disabled
                else:
                    return HttpResponse('Account is disabled. Please contact an administrator')
            
            # if user password doesn't match
            else:
                return HttpResponse('Password does not match')
    # if no post data, go back to homepage
    else: 
        return redirect('companies:index')

def logout_view(request):
    logout(request)
    return redirect('companies:index')

