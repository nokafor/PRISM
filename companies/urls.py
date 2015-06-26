from django.conf.urls import patterns, include, url

from django.conf import settings
from django.conf.urls.static import static

from companies import views
from profiles import views as profile_views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^accounts/login/', 'django_cas_ng.views.login'),
    url(r'logout/$', 'django_cas_ng.views.logout'),
    url(r'^(?P<company_name>[\w\ ]+)/$', views.detail, name='detail'),

    # profiles homepage
    
)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)