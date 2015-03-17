from __future__ import unicode_literals

from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('cas_provider.urls')),
    url(r'^accounts/profile', TemplateView.as_view(template_name='login-success-redirect-target.html')),
]
