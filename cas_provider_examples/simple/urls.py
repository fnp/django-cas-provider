from django.conf.urls import patterns, include, url

import cas_provider
from django.views.generic.simple import redirect_to, direct_to_template

urlpatterns = patterns('',
                       url(r'^', include('cas_provider.urls')),
                       url(r'^accounts/profile', direct_to_template, {'template': 'login-success-redirect-target.html'}),

                       )
