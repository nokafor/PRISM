from django.conf.urls import patterns, url

from updates import views

urlpatterns = patterns('',
	# url(r'^(?P<pk>[0-9]+)/$', views.MemberUpdateView.as_view(), name='member_edit'),
    url(r'^m/name$', views.updateName, name='updateName'),
    url(r'^m/add$', views.addMember, name='addMember'),
    url(r'^m/(?P<pk>\d+)$', views.ConflictView.as_view(), name='ConflictView'),
    url(r'^a/add$', views.addAdmin, name='addAdmin'),
    url(r'^a/delete$', views.deleteAdmin, name='deleteAdmin'),
    url(r'^m/(?P<member_id>\d+)/delete$', views.deleteMember, name='deleteMember'),
    url(r'^c/add$', views.addConflict, name='addConflict'),
    url(r'^c/(?P<conflict_id>\d+)$', views.updateConflict, name='updateConflict'),
    url(r'^c/(?P<conflict_id>\d+)/delete$', views.deleteConflict, name='deleteConflict'),
    url(r'^r/add$', views.addRehearsal, name='addRehearsal'),
    url(r'^r/(?P<rehearsal_id>\d+)$', views.updateRehearsal, name='updateRehearsal'),
    url(r'^r/(?P<rehearsal_id>\d+)/delete$', views.deleteRehearsal, name='deleteRehearsal'),
    # url(r'^u/(?P<rehearsal_id>\d+)$', views.updateRehearsal, name='updateRehearsal'),
    # url(r'^practice/$', views.MemberListView.as_view(), name='member_list'),
)
