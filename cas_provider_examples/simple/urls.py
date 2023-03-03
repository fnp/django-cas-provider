from django.urls import path, include
from django.contrib import admin
from django.views.generic import TemplateView
from django import VERSION

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('cas_provider.urls')),
    path('accounts/profile/', TemplateView.as_view(template_name='login-success-redirect-target.html')),
]
