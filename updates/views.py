from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse

from companies.models import Company, Member, Admin, Rehearsal, Cast, MemberForm
from profiles.models import ConflictForm, RehearsalForm, CreateCastForm

from django.views.generic import UpdateView, ListView
from django.template.loader import render_to_string

# Create your views here.
# class MemberListView(ListView):
#   model = Member
#   template_name = 'updates/member_list.html'

#   def get_query(self):
#       return Member.objects.all()

# class MemberUpdateView(UpdateView):
#   model = Member
#   form_class = MemberForm
#   template_name = 'updates/member_edit_form.html'

#   def dispatch(self, *args, **kwargs):
#       self.member_id = kwargs['pk']
#       return super(MemberUpdateView, self).dispatch(*args, **kwargs)

#   def form_valid(self, form):
#       form.save()
#       member = Member.objects.get(id=self.item_id)
#       return HttpResponse(render_to_string('updates/member_edit_form_success.html', {'member':member}))

def addConflict(request, company_name, member_name):
    company = get_object_or_404(Company, name=company_name)

    # user must come from profile page to get here... don't need to reauthenticate
    if request.user.is_authenticated() and member_name == request.user.username:
        try:
            member = company.member_set.get(netid=member_name)
        except (KeyError, Member.DoesNotExist):
            return redirect('profiles:profile', company_name, member_name,)
        else:
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
            return render(request, 'updates/add.html', {'company':company, 'member':member, 'form':form})
    else:
        return redirect('profiles:profile', company_name, member_name,)

def updateConflict(request, company_name, member_name, conflict_id):
    company = get_object_or_404(Company, name=company_name)

    # user must come from profile page to get here... don't need to reauthenticate
    if request.user.is_authenticated() and member_name == request.user.username:
        try:
            member = company.member_set.get(netid=member_name)
        except (KeyError, Member.DoesNotExist):
            return redirect('profiles:profile', company_name, member_name,)
        else:
            conflict = member.conflict_set.get(id=conflict_id)

            # process the form and conflict data of the user
            if request.method == 'POST':
                form = ConflictForm(request.POST, instance=conflict)
                if form.is_valid():
                    form.save()

                    return redirect('profiles:conflicts', company_name, member_name,)
            else:
                form = ConflictForm(instance=conflict)
            return render(request, 'updates/update.html', {'company':company, 'member':member, 'curr':conflict, 'form':form})
    else:
        return redirect('profiles:profile', company_name, member_name,)

def deleteConflict(request, company_name, member_name, conflict_id):
    company = get_object_or_404(Company, name=company_name)

    # user must come from profile page to get here... don't need to reauthenticate
    if request.user.is_authenticated() and member_name == request.user.username:
        try:
            member = company.member_set.get(netid=member_name)
        except (KeyError, Member.DoesNotExist):
            return redirect('profiles:profile', company_name, member_name,)
        else:
            conflict = member.conflict_set.get(id=conflict_id)
            conflict.delete()

            return redirect('profiles:conflicts', company_name, member_name,)
    else:
        return redirect('profiles:profile', company_name, member_name,)

def updateRehearsal(request, company_name, member_name, rehearsal_id):
    company = get_object_or_404(Company, name=company_name)

    # user must come from profile page to get here... don't need to reauthenticate
    if request.user.is_authenticated() and member_name == request.user.username:
        try:
            member = company.member_set.get(netid=member_name)
        except (KeyError, Member.DoesNotExist):
            return redirect('profiles:profile', company_name, member_name,)
        else:
            rehearsal = company.rehearsal_set.get(id=rehearsal_id)

            # process the form and conflict data of the user
            if request.method == 'POST':
                form = RehearsalForm(request.POST)
                if form.is_valid():
                    form.save()

                    return redirect('profiles:conflicts', company_name, member_name,)
            else:
                form = RehearsalForm(instance=rehearsal)
            return render(request, 'updates/update.html', {'company':company, 'member':member, 'form':form})
    else:
        return redirect('profiles:profile', company_name, member_name,)