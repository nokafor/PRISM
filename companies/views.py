from django_cas_ng import views

from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from companies.models import Company, Member, Admin

# Create your views here.
def index(request):
    company_list = Company.objects.order_by('name')
    context = {'company_list': company_list}
    return render(request, 'companies/index.html', context)

@login_required
def detail(request, company_name):
    return redirect('%s/' % request.user.username)

