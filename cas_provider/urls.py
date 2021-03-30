from django.conf.urls import url
from cas_provider import views


urlpatterns = [
    url(r'^login/merge/', views.login, {'merge': True, 'template_name': 'cas/merge.html'}),
    url(r'^login/?$', views.login, name='cas_login'),
    url(r'^socialauth-login/$', views.login, name='cas_socialauth_login'),
    url(r'^validate/?$', views.validate, name='cas_validate'),
    url(r'^proxy/?$', views.proxy, name='proxy'),
    url(r'^serviceValidate/?$', views.service_validate, name='cas_service_validate'),
    url(r'^proxyValidate/?$', views.proxy_validate, name='cas_proxy_validate'),
    url(r'^logout/?$', views.logout, name='cas_logout'),
]
