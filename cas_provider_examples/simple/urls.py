from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView
from django import VERSION

if VERSION >= (2,):
    from django.urls import path

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)) if VERSION < (2,) else path('admin/', admin.site.urls),
    url(r'^', include('cas_provider.urls')),
    url(r'^accounts/profile', TemplateView.as_view(template_name='login-success-redirect-target.html')),
]
