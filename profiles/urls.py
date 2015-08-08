from django.conf.urls import patterns, url

from profiles import views

urlpatterns = patterns('',
    url(r'^$', views.profile, name='profile'),
    url(r'^conflicts/$', views.conflicts, name='conflicts'),
    url(r'^casts/$', views.casts, name='casts'),
    url(r'^admin/spaces/$', views.spaces, name='spaces'),
    url(r'^members/$', views.members, name='members'),
    url(r'^admin/scheduling/$', views.scheduling, name='scheduling'),
    url(r'^testing/$', views.testing, name='testing'),
    url(r'^conflicts_due/$', views.updateConflictsDue, name='updateConflictsDue')
)