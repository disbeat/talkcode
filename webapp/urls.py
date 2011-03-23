from django.conf import settings
from django.conf.urls.defaults import *

from django.contrib.auth.views import login, logout
from django.views.generic.simple import direct_to_template
from talkcode.views import register, index

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^add$', 'talkcode.views.add' ),
    url(r'^get$', 'talkcode.views.get' ),
    url(r'^media/(.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),               
    url(r'^admin/(.*)', admin.site.root, name='admin'),
    url(r'^register/$', register, name='register'),
    url(r'^.*$', index, name="index"),
)
