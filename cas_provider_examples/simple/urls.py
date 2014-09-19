from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
                       url(r'^', include('cas_provider.urls')),
                       url(r'^accounts/profile', TemplateView.as_view(template_name='login-success-redirect-target.html')),

                       )
