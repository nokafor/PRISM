from django.conf.urls import patterns, url

from updates import views

urlpatterns = patterns('',
	# url(r'^(?P<pk>[0-9]+)/$', views.MemberUpdateView.as_view(), name='member_edit'),
    url(r'^c/(?P<conflict_id>\d+)$', views.updateConflict, name='updateConflict'),
    url(r'^c/(?P<conflict_id>\d+)/delete$', views.deleteConflict, name='deleteConflict'),
    url(r'^c/add$', views.addConflict, name='addConflict'),
    url(r'^u/(?P<rehearsal_id>\d+)$', views.updateRehearsal, name='updateRehearsal'),
    # url(r'^practice/$', views.MemberListView.as_view(), name='member_list'),
)
