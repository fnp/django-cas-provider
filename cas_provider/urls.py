from django.urls import path
from cas_provider import views


urlpatterns = [
    path('login/merge/', views.login, {'merge': True, 'template_name': 'cas/merge.html'}),
    path('login/', views.login, name='cas_login'),
    path('socialauth-login/', views.login, name='cas_socialauth_login'),
    path('validate/', views.validate, name='cas_validate'),
    path('proxy/', views.proxy, name='proxy'),
    path('serviceValidate/', views.service_validate, name='cas_service_validate'),
    path('proxyValidate/', views.proxy_validate, name='cas_proxy_validate'),
    path('logout/', views.logout, name='cas_logout'),
]
