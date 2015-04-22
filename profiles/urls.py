from django.conf.urls import patterns, url

from profiles import views

urlpatterns = patterns('',
    url(r'^$', views.profile, name='profile'),
    url(r'updatec/(?P<conflict_id>\d+)$', views.updateConflict, name='updateConflict'),
    url(r'^conflicts/$', views.conflicts, name='conflicts'),
    url(r'^casts/$', views.casts, name='casts'),
    url(r'^admin/spaces/$', views.spaces, name='spaces'),
    url(r'^admin/members/$', views.members, name='members')
)